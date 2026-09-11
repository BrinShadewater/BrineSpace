extends RefCounted
## Shared crew locomotion and activities; room_flooding advances survival and population losses.
const Geometry = preload("res://tools/modular_room_geometry.gd")
const Corridor = preload("res://rooms/underwater/corridor_geometry.gd")
const Life=preload("res://scripts/crew_life.gd")
const RoomActivity=preload("res://scripts/crew_room_activity.gd")
const CELL := 384.0
const STEP := 16
const INVALID := Vector2i(-1, -1)
const SERVICES := {
	"hunger": ["galley", "hydroponics_bay", "crew_lounge", "mycelium_nursery"],
	"fatigue": ["crew_hab", "med_bay", "med_center", "crew_lounge"],
	"maintenance": ["cold_store", "maintenance_bay", "life_support", "reactor", "storage_bay", "pressure_control", "listening_post"]
}
var needs := {"hunger": 25.0, "fatigue": 15.0, "curiosity": 60.0, "maintenance": 35.0}
var active := false
var dead := false
var movement_medium := "dry"
var helmet_equipped := false
var tank_oxygen := 60.0
var breath_oxygen := 15.0
var air_recovery:=0.0
var air_was_low:=false
var starvation := 0.0
var flood_speed := 1.0
var locker_request: Dictionary = {}
var expedition: Dictionary = {}
var swim_clearance: Dictionary = {}
var tread_clearance: Dictionary = {}
var action_clearance: Dictionary = {}
var foot := Vector2.ZERO # Station coordinates at canonical 384 units/cell; zoom independent.
var state := "idle"
var direction := "south"
var activity := "looking around"
var completed_activity: Dictionary={}
var goal := ""
var goal_cell := INVALID
var path := PackedVector2Array()
var timer := 0.0
var stage := ""
var graph := AStar2D.new()
var points := {}
var room_nodes := {}
var geometry := {}
var signature := ""
var hardware_doors_locked:=false
var visits := {}
var room_cache := {}
var layout_geometry_revision:=-1
var service_preferences: Dictionary = SERVICES.duplicate(true)
var spawn_offset := Vector2.ZERO
var decision_rng: RandomNumberGenerator
const CREW_CLEARANCE := 20.0
var avoidance_position := Vector2.INF
var avoidance_positions := PackedVector2Array()
var traffic_wait := 0.0
var traffic_retry := 0.0
var traffic_activity := ""

func needs_air() -> bool: return true

func set_movement_medium(value: String) -> bool:
	if dead or value not in ["dry", "flooded", "exterior"]: return false
	if helmet_action_active() or not locker_request.is_empty(): return false
	if value == "exterior" and needs_air() and not helmet_equipped: return false
	movement_medium = value
	return true

func set_helmet_equipped(value: bool) -> bool:
	if dead or (not value and movement_medium == "exterior"): return false
	if helmet_action_active() or not locker_request.is_empty(): return false
	helmet_equipped = value
	return true

func helmet_action_active() -> bool:
	return state in ["equip-helmet", "remove-helmet"]

func begin_helmet_action(equip: bool) -> bool:
	if dead or not active or movement_medium != "dry" or helmet_action_active(): return false
	if helmet_equipped == equip or not path.is_empty() or not stage.is_empty(): return false
	var actor: String = {"veld_npc.gd":"veld", "branforth_npc.gd":"branforth"}.get(get_script().resource_path.get_file(), "bill")
	var action := "equip-helmet" if equip else "remove-helmet"
	var manifest: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-underwater-v1/locker/%s-%s-east/manifest.json" % [actor, action]))
	if not manifest is Dictionary: return false
	var duration := 0.0
	for milliseconds in manifest.states[0].frameDurationsMs: duration += float(milliseconds) / 1000.0
	if duration <= 0.0: return false
	state = action
	direction = "east"
	goal = ""
	locker_request.clear()
	timer = duration
	activity = "securing diving helmet" if equip else "removing diving helmet"
	return true

func begin_helmet_action_at_locker(equip: bool, locker: Dictionary) -> bool:
	# Authored interaction points use canonical station units, not screen pixels.
	if not locker.get("id") is String or locker.id.is_empty(): return false
	if not locker.get("cell") is Vector2i or not locker.get("interaction_point") is Vector2: return false
	var point: Vector2 = locker.interaction_point
	if not point.is_finite() or cell_at(point) != locker.cell or cell_at(foot) != locker.cell: return false
	# Only east-facing equipment actions are authored at present.
	if locker.get("facing", "") != "east": return false
	if foot.distance_to(point) > 12.0 or not can_stand(point) or not segment_clear(foot, point): return false
	return begin_helmet_action(equip)

static func valid_locker(locker: Variant) -> bool:
	if not locker is Dictionary: return false
	if not locker.get("id") is String or locker.id.is_empty() or locker.id.length() > 128: return false
	if not locker.get("cell") is Vector2i or not locker.get("interaction_point") is Vector2: return false
	var point: Vector2 = locker.interaction_point
	return point.is_finite() and Vector2i(floori(point.x / CELL), floori(point.y / CELL)) == locker.cell and locker.get("facing", "") == "east"

func request_helmet_at_locker(equip: bool, locker: Dictionary, refill := false) -> bool:
	if dead or not active or movement_medium != "dry" or helmet_action_active() or (helmet_equipped == equip and not refill) or not stage.is_empty(): return false
	if not valid_locker(locker): return false
	var point: Vector2 = locker.interaction_point
	if not can_stand(point): return false
	var start := nearest_in_room(foot, cell_at(foot))
	var target := nearest_in_room(point, locker.cell)
	if start < 0 or target < 0: return false
	var route := graph.get_point_path(start, target)
	if route.is_empty(): return false
	route.append(point)
	route = smooth_route(route)
	var previous := foot
	for step in route:
		if not segment_clear(previous, step): return false
		previous = step
	locker_request = {"refill":refill,"equip":equip, "locker":locker.duplicate(true)}
	goal = "diving-locker"
	goal_cell = locker.cell
	path = route
	state = "walk"
	timer = 0.0
	activity = "heading to diving locker"
	return true

func advance_helmet_action(delta: float) -> void:
	if dead or not helmet_action_active() or delta <= 0.0: return
	timer = maxf(0.0, timer - delta)
	if timer > 0.0: return
	helmet_equipped = state == "equip-helmet"
	state = "idle"
	activity = "looking around"

func cancel_helmet_action() -> void:
	if not helmet_action_active(): return
	# Interrupted work never grants or removes equipment before completion.
	state = "idle"
	timer = 0.0
	activity = "helmet action interrupted"

func action_elapsed() -> float:
	var life_elapsed:=Life.elapsed(self)
	if life_elapsed>=0: return life_elapsed
	if dead: return -1.0
	if not expedition.is_empty() and expedition.phase=="pickup": return float(expedition.elapsed)
	if not expedition.is_empty() and expedition.phase=="unload" and not expedition.cargo.is_empty(): return float(expedition.elapsed)
	if movement_medium!="dry": return -1.0
	if state=="weld" and goal=="construction":
		if timer<0.52: return timer
		if timer>=9.48: return timer-9.48
	if stage=="workshop_unload": return 2.0-timer
	return -1.0

func animation_state() -> String:
	var life_pose:=Life.pose(self)
	if not life_pose.is_empty(): return life_pose
	if dead: return state
	if not expedition.is_empty():
		if expedition.phase=="salvage": return "salvage"
		if expedition.phase=="pickup": return "swim-pickup"
		if expedition.phase=="unload": return "idle" if expedition.cargo.is_empty() else "unload"
		if not expedition.cargo.is_empty(): return "carry" if movement_medium=="dry" else "swim-carry"
	if movement_medium == "dry":
		if state=="weld" and goal=="construction":
			if timer<0.52: return "torch-draw"
			if timer>=9.48: return "torch-stow"
		if stage=="workshop_carry": return "carry"
		if stage=="workshop_unload": return "unload"
		return state
	if state == "weld" and action_pose_clear("salvage"): return "salvage"
	if state == "walk": return "swim"
	# Retain a horizontal hold where standing upright in water would hit a wall.
	if not geometry.is_empty() and not swim_segment_clear(foot,foot,direction,direction,true): return "swim"
	return "tread"

func die() -> void:
	if dead: return
	expedition.clear()
	dead = true
	state = "death-ground" if movement_medium == "dry" else "death-water"
	activity = "deceased"
	path.clear()
	goal = ""
	locker_request.clear()
	stage = ""
	timer = 0.0
	traffic_wait = 0.0
	traffic_retry = 0.0
	traffic_activity = ""

func snapshot() -> Dictionary:
	return {"air_recovery":air_recovery,"air_was_low":air_was_low,"tank_oxygen":tank_oxygen,"breath_oxygen":breath_oxygen,"starvation":starvation,"expedition":expedition.duplicate(true),"helmet_equipped": helmet_equipped, "movement_medium": movement_medium, "dead": dead, "active": active, "foot": foot, "state": state, "direction": direction,
		"activity": activity, "goal": goal, "goal_cell": goal_cell, "path": path.duplicate(), "locker_request": locker_request.duplicate(true),
		"timer": timer, "stage": stage, "needs": needs.duplicate(true), "visits": visits.duplicate(true),
		"traffic_wait": traffic_wait, "traffic_retry": traffic_retry, "traffic_activity": traffic_activity,
		"decision_rng": decision_rng.state if decision_rng != null else null}

static func valid_snapshot(data: Variant, breathes := true) -> bool:
	if not data is Dictionary: return false
	if not data.get("air_was_low",false) is bool: return false
	var recovery: Variant=data.get("air_recovery",0.0)
	if not (recovery is float or recovery is int) or not is_finite(float(recovery)) or recovery<0 or recovery>3: return false
	for key in {"tank_oxygen":60.0,"breath_oxygen":15.0,"starvation":90.0}:
		if data.has(key):
			if not (data[key] is float or data[key] is int) or not is_finite(float(data[key])) or data[key]<0 or data[key]>{"tank_oxygen":60.0,"breath_oxygen":15.0,"starvation":90.0}[key]: return false
	if not preload("res://scripts/crew_expedition.gd").valid(data.get("expedition",{})): return false
	if not data.get("expedition",{}).is_empty() and ((breathes and not data.get("helmet_equipped",false)) or not data.get("active",false)): return false
	for key in ["active", "foot", "state", "direction", "activity", "goal", "goal_cell", "path", "timer", "stage", "needs", "visits", "decision_rng"]:
		if not data.has(key): return false
	if not data.active is bool or not data.foot is Vector2 or not data.foot.is_finite(): return false
	if not data.goal_cell is Vector2i or not data.path is PackedVector2Array or data.path.size() > 4096: return false
	if not data.get("movement_medium", "dry") in ["dry", "flooded", "exterior"]: return false
	if not data.get("helmet_equipped", false) is bool: return false
	if breathes and data.get("movement_medium", "dry") == "exterior" and not data.get("helmet_equipped", false) and not data.get("dead",false): return false
	if not data.state in ["idle", "walk", "kneel", "repair", "stand", "interact", "weld", "death-ground", "death-water", "equip-helmet", "remove-helmet"]: return false
	if data.state=="weld" and (data.goal not in ["construction","hull-repair"] or data.get("movement_medium","dry")!="dry" or data.get("helmet_equipped",false) or not data.path.is_empty()): return false
	if data.state in ["equip-helmet", "remove-helmet"]:
		if not data.active or data.get("movement_medium", "dry") != "dry" or data.direction != "east" or not data.path.is_empty() or data.stage != "" or data.goal != "": return false
		if data.get("helmet_equipped", false) != (data.state == "remove-helmet"): return false
	if not data.get("dead", false) is bool: return false
	if data.get("dead", false):
		var death_state := "death-ground" if data.get("movement_medium", "dry") == "dry" else "death-water"
		if data.state != death_state or not data.path.is_empty() or data.goal != "" or data.stage != "": return false
	elif data.state in ["death-ground", "death-water"]: return false
	if not data.direction in ["north", "south", "east", "west"]: return false
	if not data.goal in ["", "hunger", "fatigue", "curiosity", "maintenance", "diving-locker", "construction", "hull-repair", "flood-retreat"] and not (not breathes and data.goal=="recharge"): return false
	var request: Variant = data.get("locker_request", {})
	if not request is Dictionary: return false
	if data.goal == "diving-locker":
		if not request.get("equip") is bool or not valid_locker(request.get("locker")): return false
		if not data.active or data.get("dead", false) or data.state != "walk" or data.stage != "" or data.get("movement_medium", "dry") != "dry": return false
		if (request.equip == data.get("helmet_equipped", false) and not request.get("refill",false)) or data.goal_cell != request.locker.cell or data.path.is_empty(): return false
		if data.path[data.path.size() - 1] != request.locker.interaction_point: return false
	elif not request.is_empty(): return false
	if not Life.STAGES.has(data.stage) and not data.stage in ["", "kneel", "repair", "stand", "observation_sit", "observation_read", "observation_rise", "observation_watch", "workshop_inspect", "workshop_work", "workshop_carry", "workshop_unload"]: return false
	if str(data.stage).begins_with("observation_"):
		if not data.active or data.state!="idle" or data.direction!="north" or not data.path.is_empty(): return false
		if data.goal not in ["curiosity","fatigue","maintenance"] and not (data.goal.is_empty() and data.stage=="observation_rise"): return false
	if str(data.stage).begins_with("workshop_"):
		if not data.active or data.goal not in ["curiosity","maintenance","fatigue"]: return false
		if data.stage!="workshop_carry" and not data.path.is_empty(): return false
	if not data.activity is String or data.activity.length() > 128: return false
	if not (data.timer is float or data.timer is int) or not is_finite(float(data.timer)) or data.timer < 0 or data.timer > 3600: return false
	if str(data.stage).begins_with("life_"):
		if not data.active or data.state!="idle" or not data.path.is_empty() or float(data.timer)>float(Life.STAGES[data.stage]): return false
		if data.goal.is_empty() and data.stage not in ["life_rise","life_get_up"]: return false
	if not data.needs is Dictionary or data.needs.size() != 4 or not data.visits is Dictionary or data.visits.size() > 1600: return false
	for key in ["hunger", "fatigue", "curiosity", "maintenance"]:
		var value: Variant = data.needs.get(key)
		if not (value is float or value is int) or not is_finite(float(value)) or value < 0 or value > 100: return false
	for point in data.path:
		if not point.is_finite(): return false
	for cell in data.visits:
		if not cell is Vector2i or not data.visits[cell] is int or data.visits[cell] < 0: return false
	for key in ["traffic_wait", "traffic_retry"]:
		var value: Variant = data.get(key, 0.0)
		if not (value is float or value is int) or not is_finite(float(value)) or value < 0: return false
	if not data.get("traffic_activity", "") is String or data.get("traffic_activity", "").length() > 128: return false
	return data.decision_rng == null or data.decision_rng is int

func restore_snapshot(main, data: Dictionary, staged := false) -> void:
	# Rebuild from current art/topology, never deserialize navigation objects.
	dead = false
	if data.active and not data.get("dead",false):
		if staged: await rebuild(main,true)
		else: rebuild(main)
	else:
		# Dormant/dead crew do not need a station graph. Release/update builds it
		# against current geometry before an inactive architect can take a step.
		signature = ""
		graph.clear()
		points.clear()
		room_nodes.clear()
		geometry.clear()
	tank_oxygen = float(data.get("tank_oxygen",60.0))
	breath_oxygen = float(data.get("breath_oxygen",15.0))
	starvation = float(data.get("starvation",0.0))
	dead = data.get("dead", false)
	movement_medium = data.get("movement_medium", "dry")
	helmet_equipped = data.get("helmet_equipped", false)
	locker_request = data.get("locker_request", {}).duplicate(true)
	expedition = data.get("expedition",{}).duplicate(true)
	active = data.active
	foot = data.foot
	air_recovery=float(data.get("air_recovery",0))
	air_was_low=bool(data.get("air_was_low",false))
	state = data.state
	direction = data.direction
	activity = data.activity
	goal = data.goal
	goal_cell = data.goal_cell
	path = data.path.duplicate()
	timer = float(data.timer)
	stage = data.stage
	needs = data.needs.duplicate(true)
	visits = data.visits.duplicate(true)
	traffic_wait = float(data.get("traffic_wait", 0.0))
	traffic_retry = float(data.get("traffic_retry", 0.0))
	traffic_activity = data.get("traffic_activity", "")
	if data.decision_rng is int:
		if decision_rng == null: decision_rng = RandomNumberGenerator.new()
		decision_rng.state = data.decision_rng
	if dead or not active or not expedition.is_empty(): return
	# A changed room asset may invalidate an old route. Keep a valid position,
	# but discard unsafe travel instead of stepping through new furniture.
	if active and not can_stand(foot):
		active = false
		path.clear()
		goal = ""
		locker_request.clear()
		stage = ""
		state = "idle"
		timer = 0.0
		return
	var previous := foot
	for point in path:
		if not segment_clear(previous, point):
			path.clear()
			goal = ""
			locker_request.clear()
			stage = ""
			state = "idle"
			timer = 0.0
			break
		previous = point

func cell_at(point: Vector2) -> Vector2i:
	return Vector2i(floori(point.x / CELL), floori(point.y / CELL))

func topology(main) -> String:
	var entries: Array[String] = []
	for cell in main.occupied:
		var room: Dictionary = main.occupied[cell]
		entries.append("%s:%s:%s:%s:%s" % [cell, room.id, room.get("rotation", 0), main.get_room_doors(room),room.get("branch_owner",Vector2i(-1,-1))])
	entries.sort()
	return str(hardware_doors_locked)+"/"+"|".join(entries)+"/layouts:"+str(preload("res://scripts/room_layout_store.gd").geometry_revision)

func can_stand(point: Vector2) -> bool:
	var cell := cell_at(point)
	if not geometry.has(cell): return false
	var data: Dictionary = geometry[cell]
	var local := point - (Vector2(cell) + Vector2.ONE * 0.5) * CELL
	# Closed sockets remain walls even in the corridor and legacy renderers.
	for side in range(4):
		var normal: Vector2 = Vector2(Geometry.DIRS[side])
		if local.dot(normal) > 176 and not data.open.has(side): return false
	if data.get("corridor", false):
		return Corridor.contains_foot(data.room, local, 10.0)
	if data.get("legacy", false):
		# Legacy art has no authored prop map. Retain conservative perimeter lanes
		# around its central equipment instead of inventing a clear room interior.
		if maxf(absf(local.x), absf(local.y)) > 174 and minf(absf(local.x), absf(local.y)) > 26: return false
		return maxf(absf(local.x), absf(local.y)) >= 104
	for rect in data.blockers:
		if rect.has_point(local): return false
	return true

var sample_all_segments := OS.get_cmdline_user_args().has("--sample-all-navigation-segments")
func segment_clear(a: Vector2, b: Vector2) -> bool:
	if hardware_doors_locked and cell_at(a)!=cell_at(b): return false
	# Inside one authored room, cell and closed-door half-planes are convex.
	# Clear endpoints plus the exact blocker sweep below prove the whole segment.
	# Keep sampling for corridor/legacy shapes and all cell-boundary crossings.
	var start_cell := cell_at(a)
	var local_authored: bool = not sample_all_segments and start_cell == cell_at(b) and geometry.has(start_cell) and not geometry[start_cell].get("corridor",false) and not geometry[start_cell].get("legacy",false)
	var count := 1 if local_authored else maxi(1, ceili(a.distance_to(b) / 4.0))
	for i in range(count + 1):
		if not can_stand(a.lerp(b, float(i) / count)): return false
	# Spaced samples can miss a short intersection near a rectangle corner.
	# Sweep registered blockers exactly, clipped to the cell that owns them:
	# can_stand uses that same ownership at shared doorway boundaries.
	var first := cell_at(Vector2(minf(a.x,b.x),minf(a.y,b.y)))
	var last := cell_at(Vector2(maxf(a.x,b.x),maxf(a.y,b.y)))
	for y in range(first.y,last.y+1):
		for x in range(first.x,last.x+1):
			var cell := Vector2i(x,y)
			if not geometry.has(cell): continue
			var data: Dictionary = geometry[cell]
			if data.get("corridor",false) or data.get("legacy",false): continue
			var cell_rect := Rect2(Vector2(cell)*CELL,Vector2.ONE*CELL)
			if not segment_hits_rect(a,b,cell_rect): continue
			var center := cell_rect.get_center()
			for blocker in data.blockers:
				# Incremental float movement can drift across an exactly tangent
				# planned line. Reserve a subpixel planning margin, not smaller collision.
				var rect: Rect2 = Rect2(blocker.position+center,blocker.size).grow(0.05).intersection(cell_rect)
				if rect.has_area() and segment_hits_rect(a,b,rect): return false
	return true

func action_pose_clear(action: String) -> bool:
	if movement_medium=="exterior": return true
	if action_clearance.is_empty():
		var actor: String={"veld_npc.gd":"veld","branforth_npc.gd":"branforth"}.get(get_script().resource_path.get_file(),"bill")
		action_clearance=JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-actions-v1/clearance.json"))[actor]
	var extent: Array=action_clearance["helmet" if helmet_equipped else "bare"][action+"-"+direction]
	return swim_segment_clear(foot,foot,direction,direction,false,extent)

func swim_segment_clear(a: Vector2, b: Vector2, facing: String, previous_facing: String = "", treading: bool = false, additional_extent: Array = []) -> bool:
	if previous_facing.is_empty(): previous_facing = direction
	if swim_clearance.is_empty():
		# Companions never inherit a human diver silhouette: Josh has no swim profile by design,
		# and Margot/River preload theirs, so this lazy path must not fall back to Bill's.
		if get_script().resource_path.get_file() == "companion_npc.gd": return false
		var data: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-underwater-v1/swim-clearance.json"))
		if not data is Dictionary: return false
		var actor: String = {"veld_npc.gd":"veld", "branforth_npc.gd":"branforth"}.get(get_script().resource_path.get_file(), "bill")
		swim_clearance = data.actors[actor]
		tread_clearance = data.treading[actor]
	var profile: Dictionary = (tread_clearance if treading else swim_clearance)["helmet" if helmet_equipped else "bare"]
	if not profile.has(facing) or not profile.has(previous_facing): return false
	var extent: Array = profile[facing].duplicate()
	# A turn must also accommodate the outgoing silhouette at the start.
	for axis in range(2):
		extent[axis] = minf(extent[axis], profile[previous_facing][axis])
		extent[axis+2] = maxf(extent[axis+2], profile[previous_facing][axis+2])
	if not additional_extent.is_empty():
		for axis in range(2):
			extent[axis]=minf(extent[axis],additional_extent[axis])
			extent[axis+2]=maxf(extent[axis+2],additional_extent[axis+2])
	var footprint := Rect2(Vector2(extent[0],extent[1]),Vector2(extent[2]-extent[0],extent[3]-extent[1]))
	var swept := Rect2(a+footprint.position,footprint.size).merge(Rect2(b+footprint.position,footprint.size))
	# Sweep the whole bounding rectangle against registered padded blockers.
	for cell in geometry:
		var center := (Vector2(cell)+Vector2.ONE*0.5)*CELL
		if geometry[cell].has("swim_blocker_bounds"):
			var local_bounds: Rect2 = geometry[cell].swim_blocker_bounds
			if not Rect2(local_bounds.position+center,local_bounds.size).intersects(swept,true): continue
		for blocker in geometry[cell].get("blockers", []):
			# The visible envelope replaces the standing radius; retain a small
			# clearance margin instead of adding that radius a second time.
			var obstacle: Rect2 = blocker.grow(-maxf(0.0,float(geometry[cell].get("blocker_padding",0.0))-2.0))
			var expanded := Rect2(obstacle.position+center-footprint.end,obstacle.size+footprint.size)
			if segment_hits_rect(a,b,expanded): return false
	# Authored room blockers already provide an exact rectangle sweep. Only
	# corridor/legacy floor shapes need the more expensive envelope sampling.
	var first := cell_at(swept.position)
	var last := cell_at(swept.end-Vector2.ONE*0.0001)
	var sample_floor := false
	for y in range(first.y,last.y+1):
		for x in range(first.x,last.x+1):
			var cell := Vector2i(x,y)
			if not geometry.has(cell):
				var missing := Rect2(Vector2(cell)*CELL-footprint.end,Vector2.ONE*CELL+footprint.size)
				if segment_hits_rect(a,b,missing): return false
			elif geometry[cell].get("corridor",false) or geometry[cell].get("legacy",false): sample_floor=true
	if not sample_floor: return true
	# Sample the envelope as well for corridor shapes and missing station floor.
	var columns := maxi(1,ceili(footprint.size.x/8.0))
	var rows := maxi(1,ceili(footprint.size.y/8.0))
	for y in range(rows+1):
		for x in range(columns+1):
			var offset := footprint.position+footprint.size*Vector2(float(x)/columns,float(y)/rows)
			if not segment_clear(a+offset,b+offset): return false
	return true

static func segment_hits_rect(a: Vector2,b: Vector2,rect: Rect2) -> bool:
	var enter := 0.0
	var leave := 1.0
	for axis in range(2):
		var delta: float = b[axis]-a[axis]
		if delta == 0.0:
			if a[axis]<rect.position[axis] or a[axis]>=rect.end[axis]: return false
			continue
		var t0: float = (rect.position[axis]-a[axis])/delta
		var t1: float = (rect.end[axis]-a[axis])/delta
		enter=maxf(enter,minf(t0,t1))
		leave=minf(leave,maxf(t0,t1))
		if enter>leave: return false
	# Match Rect2.has_point's half-open maximum edges, including stationary paths.
	return rect.has_point(a.lerp(b,(enter+leave)*0.5))

func rebuild(main, staged := false) -> void:
	if dead: return
	var revision: int=preload("res://scripts/room_layout_store.gd").geometry_revision
	if revision!=layout_geometry_revision:
		room_cache.clear(); layout_geometry_revision=revision
	cancel_helmet_action()
	graph.clear()
	points.clear()
	room_nodes.clear()
	geometry.clear()
	path.clear()
	goal = ""
	locker_request.clear()
	stage = ""
	state = "idle"
	var slice_started := Time.get_ticks_usec()
	var room_keys := {}
	for cell in main.occupied:
		if staged and Time.get_ticks_usec()-slice_started>=4000:
			await main.get_tree().process_frame
			slice_started = Time.get_ticks_usec()
		var room: Dictionary = main.occupied[cell]
		var sides: Array = []
		for neighbor in main._connected_neighbor_cells(cell):
			sides.append(Geometry.DIRS.find(neighbor - cell))
		var key := "%s:%s:%s" % [room.id, room.get("rotation", 0), sides]
		# Fixed recovery furniture is part of geometry, not interchangeable blueprint art.
		if room.id=="brine_core": key+="/pod:"+str(not main.architect_run.is_empty())
		if room.get("recovered_derelict",false): key+="/pods:"+str(main.wrecks.get(cell,{}).get("pods",[]).size())
		if main.wrecks.get(cell,{}).get("kind","") in ["river","josh","margot"]:key+="/companion-container"
		room_keys[cell] = key
		var data: Dictionary = room_cache[key].data if room_cache.has(key) else main.grid_view.bill_room_geometry(room, sides)
		if data.is_empty(): continue
		data.activity_room = str(room.id)
		data.open = sides
		if not data.has("blockers"):
			data.blockers = []
			data.blocker_padding = 10.0
			for prop in data.props:
				for rect in Geometry.prop_collision_rects(prop): data.blockers.append(rect.grow(10))
			for edge in data.edges:
				for rect in Geometry.wall_rects(edge): data.blockers.append(rect.grow(10))
		if not data.blockers.is_empty():
			var bounds: Rect2 = data.blockers[0]
			for blocker in data.blockers: bounds = bounds.merge(blocker)
			data.swim_blocker_bounds = bounds
		geometry[cell] = data
		room_nodes[cell] = []
	for cell in geometry:
		if staged and Time.get_ticks_usec()-slice_started>=4000:
			await main.get_tree().process_frame
			slice_started = Time.get_ticks_usec()
		var center := (Vector2(cell) + Vector2.ONE * 0.5) * CELL
		var key: String = room_keys[cell]
		if not room_cache.has(key):
			var local_points := {}
			var links: Array = []
			for y in range(-176, 177, STEP):
				for x in range(-176, 177, STEP):
					var local := Vector2i(x, y)
					if can_stand(center + Vector2(local)): local_points[local] = true
			for local in local_points:
				if staged and Time.get_ticks_usec()-slice_started>=4000:
					await main.get_tree().process_frame
					slice_started = Time.get_ticks_usec()
				for offset in [Vector2i(STEP, 0), Vector2i(0, STEP), Vector2i(STEP, STEP), Vector2i(-STEP, STEP)]:
					var other: Vector2i = local + offset
					if local_points.has(other) and segment_clear(center + Vector2(local), center + Vector2(other)):
						links.append([local, other])
			room_cache[key] = {"data": geometry[cell], "points": local_points.keys(), "links": links}
		for local in room_cache[key].points:
			var point := center + Vector2(local)
			var id := graph.get_available_point_id()
			graph.add_point(id, point, 1.0 if mini(absi(local.x), absi(local.y)) < 24 else 1.08)
			points[Vector2i(point)] = id
			room_nodes[cell].append(id)
		for link in room_cache[key].links:
			graph.connect_points(points[Vector2i(center) + link[0]], points[Vector2i(center) + link[1]])
	# Cross cell boundaries only at reciprocal, connected door centers.
	for cell in geometry:
		if staged and Time.get_ticks_usec()-slice_started>=4000:
			await main.get_tree().process_frame
			slice_started = Time.get_ticks_usec()
		var center := (Vector2(cell) + Vector2.ONE * 0.5) * CELL
		for side in geometry[cell].open:
			var a := Vector2i(center + Vector2(Geometry.DIRS[side]) * 176)
			var b: Vector2i = a + Geometry.DIRS[side] * 32
			if points.has(a) and points.has(b) and segment_clear(Vector2(a), Vector2(b)):
				graph.connect_points(points[a], points[b])
	signature = topology(main)

func nearest_in_room(point: Vector2, cell: Vector2i, require_clear := true) -> int:
	var best := -1
	var distance := INF
	for id in room_nodes.get(cell, []):
		var target := graph.get_point_position(id)
		var candidate := point.distance_squared_to(target)
		if candidate < distance and (not require_clear or segment_clear(point, target)):
			best = id
			distance = candidate
	return best

func update(main, delta: float) -> void:
	if dead: return
	if delta <= 0: return
	if topology(main) != signature: rebuild(main)
	if not active:
		var initial: Vector2 = main._room_idle_anchor(main.test_walker_cell) / main.get_cell_size() * CELL + Vector2(0, CELL * 0.038) + spawn_offset
		var id := nearest_in_room(initial, main.test_walker_cell, false)
		if id >= 0 and not spawn_clear(graph.get_point_position(id)):
			id = -1
			var closest := INF
			for candidate in room_nodes.get(main.test_walker_cell, []):
				var point := graph.get_point_position(candidate)
				if spawn_clear(point) and point.distance_squared_to(initial) < closest:
					closest = point.distance_squared_to(initial)
					id = candidate
		if id < 0: return
		foot = graph.get_point_position(id)
		active = true
	# If construction invalidates the occupied floor, stop rather than teleport
	# across furniture. A fresh run explicitly creates a new NPC instance.
	if not can_stand(foot):
		cancel_helmet_action()
		goal = ""
		locker_request.clear()
		path.clear()
		state = "idle"
		activity = "route obstructed"
		return
	if preload("res://scripts/flood_safety.gd").advance(main,self,delta): return
	if preload("res://scripts/hull_repair.gd").advance(main,self,delta): return
	if preload("res://scripts/crew_construction.gd").advance(main,self,delta): return
	for need in needs:
		var rate := 0.12 if need == "hunger" else (0.10 if need == "fatigue" else 0.22)
		needs[need] = minf(100.0, needs[need] + delta * rate)
	if helmet_action_active():
		advance_helmet_action(delta)
		return
	if not goal.is_empty() and (goal not in ["curiosity", "diving-locker"] or geometry.get(goal_cell,{}).get("activity_room","") in ["observation_room","salvage_workshop","galley","cold_store","crew_lounge","crew_hab"]) and not service_available(main, goal_cell):
		path.clear()
		goal = ""
		locker_request.clear()
		# Stand up before choosing a new destination if work was interrupted.
		if stage in ["life_lie","life_sleep"]:
			stage="life_get_up";state="idle";timer=0.8
		elif stage in ["life_sit","life_seated"]:
			stage="life_rise";state="idle";timer=0.8
		elif stage in ["observation_sit","observation_read"]:
			stage="observation_rise";state="idle";timer=0.65
		elif stage in ["kneel", "repair"]:
			stage = "stand"
			state = "stand"
			timer = 1.0
		else:
			stage = ""
			state = "idle"
			timer = 0.0
	if not path.is_empty():
		move(delta)
		return
	if timer > 0:
		timer = maxf(0.0, timer - delta)
		if timer > 0: return
		if Life.next(self): return
		if stage=="workshop_inspect":
			stage="workshop_work"
			state="interact"
			activity="sorting recovered components"
			timer=5.0
			return
		if stage=="workshop_work":
			stage="workshop_pickup"
			state="idle"
			timer=0.52
			return
		if stage=="workshop_pickup":
			var target: Vector2=(Vector2(goal_cell)+Vector2.ONE*.5)*CELL+Vector2(-112,144)
			var target_id:=nearest_in_room(target,goal_cell,false)
			var start_id:=nearest_in_room(foot,goal_cell,false)
			path=smooth_route(route_between(start_id,target_id))
			if not path.is_empty():
				stage="workshop_carry"
				state="walk"
				activity="carrying recovered parts"
				return
		if stage == "observation_sit":
			stage="observation_read"
			timer=12.0
			return
		if stage == "observation_read":
			stage="observation_rise"
			timer=0.65
			return
		if stage == "kneel":
			stage = "repair"
			state = "repair"
			timer = 4.0
			return
		if stage == "repair":
			stage = "stand"
			state = "stand"
			timer = 1.0
			return
		if not goal.is_empty():
			if activity in ["checking manifold gauges","monitoring sonar returns","resting beside the berth","resting in the berth"]:
				completed_activity={"serial":int(completed_activity.get("serial",0))+1,"activity":activity,"cell":goal_cell}
			needs[goal] = maxf(0.0, float(needs[goal]) - (45.0 if goal != "curiosity" else 65.0))
		goal = ""
		locker_request.clear()
		stage = ""
		state = "idle"
	if not goal.is_empty():
		arrive()
		return
	choose_goal(main)

func move(delta: float) -> void:
	if dead: return
	var remaining := delta * 46.0 * flood_speed
	traffic_retry = maxf(0.0, traffic_retry - delta)
	state = "walk"
	while remaining > 0 and not path.is_empty():
		var target: Vector2 = path[0]
		var distance := foot.distance_to(target)
		var next := foot.move_toward(target, remaining)
		if not crew_clear(foot, next):
			if traffic_activity.is_empty(): traffic_activity = activity
			activity = "waiting for passage"
			state = "idle"
			traffic_wait += delta
			if traffic_retry <= 0:
				traffic_retry = 0.5
				if detour_around_crew(): return
			if traffic_wait > 3.0:
				# A colleague may be resting at the destination. Pick another
				# reachable spot instead of permanently reserving this route.
				path.clear()
				goal = ""
				locker_request.clear()
				timer = 0.5
				traffic_wait = 0.0
				traffic_activity = ""
			return
		var heading := direction
		var travel := next-foot
		if travel.length_squared() > 0.001:
			heading = ("east" if travel.x > 0 else "west") if absf(travel.x) > absf(travel.y) else ("south" if travel.y > 0 else "north")
		if not segment_clear(foot, next) or (movement_medium != "dry" and not swim_segment_clear(foot,next,heading)):
			path.clear()
			goal = ""
			locker_request.clear()
			state = "idle"
			activity = "route obstructed"
			timer = 1.0
			return
		var offset := next - foot
		if offset.length_squared() > 0.001:
			direction = ("east" if offset.x > 0 else "west") if absf(offset.x) > absf(offset.y) else ("south" if offset.y > 0 else "north")
		foot = next
		traffic_wait = 0.0
		if not traffic_activity.is_empty():
			activity = traffic_activity
			traffic_activity = ""
		remaining -= distance
		if foot.is_equal_approx(target): path.remove_at(0)
	if path.is_empty(): arrive()

func avoidance_peers() -> PackedVector2Array:
	var peers := avoidance_positions.duplicate()
	if avoidance_position.is_finite(): peers.append(avoidance_position)
	return peers

func spawn_clear(point: Vector2) -> bool:
	for peer in avoidance_peers():
		if point.distance_to(peer) < CREW_CLEARANCE: return false
	return true

func crew_clear(a: Vector2, b: Vector2) -> bool:
	for peer in avoidance_peers():
		if a.distance_to(peer) < CREW_CLEARANCE - 0.01:
			if (b - a).dot(a - peer) < 0 or b.distance_to(peer) <= a.distance_to(peer): return false
		elif Geometry2D.get_closest_point_to_segment(peer, a, b).distance_to(peer) < CREW_CLEARANCE - 0.01:
			return false
	return true

func detour_around_crew() -> bool:
	if path.is_empty() or avoidance_peers().is_empty(): return false
	# A clear join may still be isolated by the padded peer exclusion. Try safe
	# joins nearest-first until one has a complete usable route, not just access.
	var starts: Array[int] = []
	for id in room_nodes.get(cell_at(foot), []):
		var point := graph.get_point_position(id)
		if travel_segment_clear(foot,point,direction) and crew_clear(foot,point): starts.append(id)
	starts.sort_custom(func(a,b): return foot.distance_squared_to(graph.get_point_position(a)) < foot.distance_squared_to(graph.get_point_position(b)))
	var target := nearest_in_room(path[path.size() - 1], cell_at(path[path.size() - 1]))
	if target < 0: return false
	for start in starts:
		var candidate := crew_detour_from(start, target)
		if not candidate.is_empty():
			var endpoint := path[path.size() - 1]
			var last := candidate[candidate.size() - 1]
			var previous := foot if candidate.size() < 2 else candidate[candidate.size()-2]
			var facing := travel_heading(previous,last,direction)
			if not travel_segment_clear(last,endpoint,facing) or not crew_clear(last, endpoint): continue
			candidate.append(endpoint)
			path = candidate
			return true
	return false

func crew_detour_from(start: int, target: int) -> PackedVector2Array:
	var disabled: Array[int] = []
	for peer in avoidance_peers():
		var peer_cell := cell_at(peer)
		for cell in room_nodes:
			if absi(cell.x - peer_cell.x) > 1 or absi(cell.y - peer_cell.y) > 1: continue
			for id in room_nodes[cell]:
				# Padding covers diagonal grid links as well as node centers.
				var point := graph.get_point_position(id)
				var front_lane := false
				var room_data: Dictionary = geometry[cell]
				if room_data.get("corridor", false) and room_data.room.id == "corridor" and Corridor.rotation(room_data.room) % 2 == 0:
					# Pass along the front half of horizontal corridors: the tall
					# sprite then stays clear of the back hull's visual silhouette.
					front_lane = point.y < (float(cell.y) + 0.5) * CELL and id != target
				if id != start and (point.distance_to(peer) < 32.0 or front_lane):
					graph.set_point_disabled(id, true)
					disabled.append(id)
	var route := route_between(start, target, true)
	for id in disabled: graph.set_point_disabled(id, false)
	if route.is_empty(): return PackedVector2Array()
	var result := PackedVector2Array()
	var from := foot
	var facing := direction
	var index := 0
	while index < route.size():
		var farthest := -1
		for probe in range(index, route.size()):
			if travel_segment_clear(from,route[probe],facing) and crew_clear(from, route[probe]): farthest = probe
		if farthest < 0: return PackedVector2Array()
		result.append(route[farthest])
		facing = travel_heading(from,route[farthest],facing)
		from = route[farthest]
		index = farthest + 1
	return result

func arrive() -> void:
	if dead: return
	state = "idle"
	if goal in ["construction","hull-repair","flood-retreat","recharge"]: return
	if stage=="workshop_carry":
		stage="workshop_unload"
		direction="north"
		activity="stowing recovered parts"
		timer=2.0
		return
	if goal == "diving-locker":
		var request := locker_request.duplicate(true)
		goal = ""
		locker_request.clear()
		timer = 0.0
		if request.get("refill",false):
			state="idle"
			timer=5.0
			activity="refilling oxygen tank"
			return
		if request.is_empty() or not begin_helmet_action_at_locker(request.equip, request.locker):
			activity = "locker approach interrupted"
		return
	visits[goal_cell] = int(visits.get(goal_cell, 0)) + 1
	if begin_room_activity(): return
	timer = 6.0
	match goal:
		"hunger": activity = "taking a meal break"; timer = 9.0
		"fatigue": activity = "resting"; timer = 12.0
		"maintenance":
			activity = "checking equipment"
			var facing:=equipment_facing(goal_cell,foot-(Vector2(goal_cell)+Vector2.ONE*.5)*CELL)
			if not facing.is_empty(): direction=facing
			state = "kneel"
			stage = "kneel"
			timer = 1.0
		_: activity = "looking around"

func choose_goal(main) -> void:
	if dead: return
	var npc_rng: RandomNumberGenerator = decision_rng if decision_rng != null else main.rng
	var start := nearest_in_room(foot, cell_at(foot))
	if start < 0:
		activity = "waiting for a clear route"
		timer = 2.0
		return
	var candidates: Array = []
	for cell in room_nodes:
		var room: Dictionary = main.occupied[cell]
		var id := str(room.id)
		if id in ["corridor", "corner", "tee_corridor"]: continue
		for need in needs:
			if need != "curiosity" and not service_preferences.get(need, []).has(id): continue
			if (need != "curiosity" or id in ["observation_room","salvage_workshop","galley","cold_store","crew_lounge","crew_hab"]) and not service_available(main, cell): continue
			var score := float(needs[need]) - Vector2(cell - cell_at(foot)).length() * 2.0
			if need == "curiosity": score -= mini(20, int(visits.get(cell, 0)) * 4)
			candidates.append({"cell": cell, "need": need, "score": score + npc_rng.randf_range(0, 8)})
	candidates.sort_custom(func(a, b): return a.score > b.score)
	for candidate in candidates:
		var targets: Array = room_nodes[candidate.cell].duplicate()
		# Use the station RNG so seeded playtests can reproduce decisions.
		for i in range(targets.size() - 1, 0, -1):
			var j: int = npc_rng.randi_range(0, i)
			var swap = targets[i]
			targets[i] = targets[j]
			targets[j] = swap
		var stations:=RoomActivity.stations(geometry[candidate.cell])
		if geometry[candidate.cell].get("activity_room","")=="observation_room" and int(visits.get(candidate.cell,0))%2==1: stations.reverse()
		var wants_station: bool=not stations.is_empty() and (candidate.need in ["maintenance","fatigue","curiosity"] or (candidate.need=="hunger" and geometry[candidate.cell].get("activity_room","") in ["galley","crew_lounge"]))
		if wants_station:
			var center: Vector2=(Vector2(candidate.cell)+Vector2.ONE*0.5)*CELL
			targets.sort_custom(func(a,b): return graph.get_point_position(a).distance_squared_to(center+stations[0].point)<graph.get_point_position(b).distance_squared_to(center+stations[0].point))
		var attempted := 0
		for target_id in targets:
			var target := graph.get_point_position(target_id)
			var local := target - (Vector2(candidate.cell) + Vector2.ONE * 0.5) * CELL
			if absf(local.x) > 144 or absf(local.y) > 144 or target.distance_to(foot) < 32: continue
			if wants_station and RoomActivity.at(geometry[candidate.cell],local).is_empty(): continue
			if wants_station and not spawn_clear(target): continue
			if candidate.need == "maintenance" and not wants_station and not equipment_spot(candidate.cell, local): continue
			var route := route_between(start, target_id)
			attempted += 1
			if route.is_empty():
				if attempted >= 8: break
				continue
			goal = candidate.need
			goal_cell = candidate.cell
			path = smooth_route(route)
			state = "walk"
			activity = {"hunger": "looking for food", "fatigue": "looking for rest", "maintenance": "heading to equipment", "curiosity": "exploring"}[goal]
			return
	# A corridor-only station still permits pacing along its safe floor.
	var available: Array = room_nodes.get(cell_at(foot), [])
	if not available.is_empty():
		var target: int = available[npc_rng.randi_range(0, available.size() - 1)]
		path = smooth_route(route_between(start, target))
		goal = "curiosity"
		goal_cell = cell_at(foot)
	activity = "waiting for suitable rooms" if path.is_empty() else "stretching his legs"
	timer = 2.0 if path.is_empty() else 0.0

func begin_room_activity() -> bool:
	if stage.begins_with("workshop_"): return true
	if goal not in ["maintenance","fatigue","curiosity","hunger"] or not geometry.has(goal_cell): return false
	var local:=foot-(Vector2(goal_cell)+Vector2.ONE*0.5)*CELL
	var station:=RoomActivity.at(geometry[goal_cell],local)
	if station.is_empty(): return false
	direction=station.facing
	if Life.begin(self,station): return true
	if station.room=="cold_store":
		stage=""
		state="idle"
		activity="checking chilled supplies"
		timer=6.0
		return true
	if station.room=="galley":
		stage=""
		state="idle"
		activity="taking a hot meal break"
		timer=9.0
		return true
	if station.room=="salvage_workshop":
		stage="workshop_inspect"
		state="idle"
		activity="inspecting recovered machinery"
		timer=2.0
		return true
	if station.room=="observation_room":
		state="idle"
		stage="observation_sit" if station.mode=="read" else "observation_watch"
		activity="reading by lamplight" if station.mode=="read" else "watching the ocean"
		timer=0.65 if station.mode=="read" else 8.0
		return true
	stage=""
	state="interact" if station.room!="crew_hab" else "idle"
	activity={"pressure_control":"checking manifold gauges","listening_post":"monitoring sonar returns","crew_hab":"resting beside the berth"}[station.room]
	timer=10.0 if station.room=="crew_hab" else 6.0
	return true

func equipment_spot(cell: Vector2i, local: Vector2) -> bool:
	return not equipment_facing(cell,local).is_empty()

func equipment_facing(cell: Vector2i, local: Vector2) -> String:
	for prop in geometry.get(cell,{}).get("props",[]):
		var rect: Rect2=prop.rect
		if local.y>=rect.position.y and local.y<=rect.end.y:
			if local.x<rect.position.x-10 and local.x>rect.position.x-34: return "east"
			if local.x>rect.end.x+10 and local.x<rect.end.x+34: return "west"
		if local.x>=rect.position.x and local.x<=rect.end.x:
			if local.y<rect.position.y-10 and local.y>rect.position.y-34: return "south"
			if local.y>rect.end.y+10 and local.y<rect.end.y+34: return "north"
	return ""

func service_available(main, cell: Vector2i) -> bool:
	return main.occupied.has(cell) and not main.occupied[cell].get("suspended", false) and main.powered_room_cells.has(cell)

func travel_segment_clear(a: Vector2, b: Vector2, facing: String) -> bool:
	return segment_clear(a,b) and (movement_medium == "dry" or swim_segment_clear(a,b,travel_heading(a,b,facing),facing))

func travel_heading(a: Vector2, b: Vector2, fallback: String) -> String:
	var offset := b-a
	if offset.length_squared() <= 0.001: return fallback
	return ("east" if offset.x > 0 else "west") if absf(offset.x) > absf(offset.y) else ("south" if offset.y > 0 else "north")

func route_between(start: int, target: int, avoid_crew: bool = false) -> PackedVector2Array:
	if movement_medium == "dry": return graph.get_point_path(start,target)
	if not graph.has_point(start) or not graph.has_point(target): return PackedVector2Array()
	var facings := ["east","south","west","north"]
	var initial := Vector2i(start,facings.find(direction))
	var frontier: Array[Vector2i] = [initial]
	var costs := {initial:0.0}
	var parents := {}
	var destination := graph.get_point_position(target)
	while not frontier.is_empty():
		var best := 0
		var priority := INF
		for i in range(frontier.size()):
			var candidate: Vector2i = frontier[i]
			var score: float = costs[candidate]+graph.get_point_position(candidate.x).distance_to(destination)
			if score < priority: priority=score; best=i
		var current: Vector2i = frontier[best]
		frontier.remove_at(best)
		if current.x == target:
			var route := PackedVector2Array([destination])
			while parents.has(current):
				current = parents[current]
				route.insert(0,graph.get_point_position(current.x))
			return route
		var from := graph.get_point_position(current.x)
		for next_id in graph.get_point_connections(current.x):
			if graph.is_point_disabled(next_id): continue
			var to := graph.get_point_position(next_id)
			var heading := travel_heading(from,to,facings[current.y])
			var next_state := Vector2i(next_id,facings.find(heading))
			var cost: float = costs[current]+from.distance_to(to)
			if cost >= costs.get(next_state,INF): continue
			if avoid_crew and not crew_clear(from,to): continue
			if not swim_segment_clear(from,to,heading,facings[current.y]): continue
			costs[next_state]=cost
			parents[next_state]=current
			if not frontier.has(next_state): frontier.append(next_state)
	return PackedVector2Array()

func smooth_route(route: PackedVector2Array) -> PackedVector2Array:
	# Remove grid stair-steps only when the entire shortcut has foot clearance.
	var result := PackedVector2Array()
	var from := foot
	var facing := direction
	var index := 0
	while index < route.size():
		var farthest := -1
		for probe in range(index, route.size()):
			var heading := travel_heading(from,route[probe],facing)
			if segment_clear(from, route[probe]) and (movement_medium == "dry" or swim_segment_clear(from,route[probe],heading,facing)): farthest = probe
		if farthest < 0: return PackedVector2Array()
		result.append(route[farthest])
		facing = travel_heading(from,route[farthest],facing)
		from = route[farthest]
		index = farthest + 1
	return result

func observation_visual_offset() -> Vector2:
	if stage.begins_with("life_"): return Life.offset(self)
	var amount:=0.0
	if stage=="observation_sit": amount=1.0-clampf(timer/0.65,0,1)
	elif stage=="observation_read": amount=1.0
	elif stage=="observation_rise": amount=clampf(timer/0.65,0,1)
	return Vector2(0,8.0*amount)
