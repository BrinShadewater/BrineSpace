extends RefCounted
## One mission and launch chamber per Moonbay. State is persisted on the room.

const ORDERS := ["survey","recover","deep_access"]
const REPAIR_METAL := 4
const Architects = preload("res://scripts/architects.gd")
const DURATIONS := {"approach":12.0,"seal":3.0,"flood":6.0,"launch":3.0,
	"work":10.0,"drain":6.0,"unload":3.0}
const PHASES := ["idle","approach","seal","flood","launch","outbound","work","return","drain","unload"]

static func valid_rooms(rooms: Array, crew: Variant) -> bool:
	if crew != null and not crew is Dictionary: return false
	var active_crews := {}
	for room in rooms:
		if not room is Dictionary: return false
		if room.get("id","")!="moonbay":
			if room.has("moonbay_mission"): return false
			continue
		if not room.has("moonbay_mission"): continue # Old checkpoint: dry, idle hangar.
		var state: Variant = room.moonbay_mission
		if not state is Dictionary or not state.get("phase","") in PHASES: return false
		if not state.get("progress") is float and not state.get("progress") is int: return false
		if not is_finite(float(state.progress)) or float(state.progress)<0: return false
		if not state.get("target") is Vector2i or not state.get("cargo") is Dictionary: return false
		if not state.get("crew") is String or not state.get("order") is String: return false
		if not state.get("credited") is bool or not state.get("recall") is bool: return false
		if not state.get("station_open") is bool or not state.get("ocean_open") is bool: return false
		if state.station_open and state.ocean_open: return false
		if not (state.get("chamber_water") is float or state.get("chamber_water") is int): return false
		if not is_finite(float(state.chamber_water)) or float(state.chamber_water)<0 or float(state.chamber_water)>1: return false
		if not state.get("damage") is int or int(state.damage)<0 or int(state.damage)>1: return false
		if not (state.get("hazard_roll") is float or state.get("hazard_roll") is int): return false
		if not is_finite(float(state.hazard_roll)) or float(state.hazard_roll)<0 or float(state.hazard_roll)>1: return false
		if not state.get("last_result") is String or str(state.last_result).length()>160: return false
		for id in state.cargo:
			if id not in ["metal","data","rare_minerals"] or not state.cargo[id] is int or state.cargo[id]<0 or state.cargo[id]>100: return false
		if state.phase=="idle":
			if state.crew!="" or state.order!="" or state.chamber_water!=0.0 or not state.station_open or state.ocean_open: return false
			continue
		if state.crew not in Architects.IDS or state.order not in ORDERS or active_crews.has(state.crew): return false
		if state.target.x<0 or state.target.y<0 or state.target.x>=40 or state.target.y>=40: return false
		if float(state.progress)>_duration(room,state)+0.001: return false
		active_crews[state.crew] = room.pos
	# Pre-crew checkpoints can only contain idle Moonbays.
	if crew == null: return active_crews.is_empty()
	for id in Architects.IDS:
		var snapshot: Variant = crew.get(id,{})
		if not snapshot is Dictionary: continue
		var assignment: Variant = snapshot.get("moonbay_assignment",{})
		if not assignment is Dictionary: return false
		if active_crews.has(id) != (not assignment.is_empty()): return false
		if active_crews.has(id) and assignment.get("home")!=active_crews[id]: return false
	return true

static func station_visible(game, actor) -> bool:
	if actor.moonbay_assignment.is_empty() or not actor.moonbay_assignment.get("onboard",false): return true
	var room: Dictionary = game.occupied.get(actor.moonbay_assignment.get("home",Vector2i(-1,-1)),{})
	if room.is_empty(): return true
	return mission_state(room).phase in ["idle","approach","unload"]

static func on_crew_death(game, actor) -> void:
	if actor.moonbay_assignment.is_empty(): return
	var home: Vector2i = actor.moonbay_assignment.home
	if not game.occupied.has(home): return
	var state := mission_state(game.occupied[home])
	if state.phase=="idle": return
	state.damage = 1
	state.recall = true
	state.cargo = {}
	state.credited = true
	state.last_result = "Pilot lost. Mini-sub returning under autopilot."
	if state.phase in ["approach","seal"]:
		state.phase = "unload"
		state.progress = 0.0
		state.station_open = true
	elif state.phase=="flood":
		state.phase = "drain"
		state.progress = (1.0-clampf(float(state.chamber_water),0.0,1.0))*float(DURATIONS.drain)
		state.ocean_open = false
	elif state.phase in ["launch","outbound","work"]:
		state.phase = "return"
		state.progress = 0.0
		state.ocean_open = false

static func exterior_position(room: Dictionary, state: Dictionary) -> Vector2:
	var sides := [Vector2.UP,Vector2.RIGHT,Vector2.DOWN,Vector2.LEFT]
	var names := ["north","east","south","west"]
	var side_index: int = names.find(str(room.get("ocean_side","west")))
	var outward: Vector2 = sides[posmod(side_index+int(room.get("rotation",0)),4)]
	var center: Vector2 = Vector2(room.pos)+Vector2.ONE
	var hatch: Vector2 = center+outward
	var launch: Vector2 = hatch+outward*0.6
	var target: Vector2 = Vector2(state.target)+Vector2.ONE*0.5
	var amount: float = clampf(float(state.progress)/maxf(1.0,_duration(room,state)),0.0,1.0)
	match str(state.phase):
		"launch": return hatch.lerp(launch,amount)
		"outbound": return launch.lerp(target,amount)
		"work": return target+Vector2(cos(amount*TAU),sin(amount*TAU))*0.15
		"return": return target.lerp(launch,amount)
	return launch

static func draw_exterior(canvas: CanvasItem, game, cell_size: float) -> void:
	for room in game.placed_rooms:
		if room.get("id","")!="moonbay" or not room.has("moonbay_mission"): continue
		var state: Dictionary = room.moonbay_mission
		if state.phase not in ["launch","outbound","work","return"]: continue
		var point: Vector2 = exterior_position(room,state)*cell_size
		var hatch: Vector2 = (Vector2(room.pos)+Vector2.ONE)*cell_size
		var direction: Vector2 = point-hatch
		if state.phase=="outbound" or state.phase=="work": direction=(Vector2(state.target)+Vector2.ONE*0.5)*cell_size-point
		if state.phase=="return": direction=hatch-point
		if direction.length_squared()<0.001: direction=Vector2.LEFT.rotated(deg_to_rad(float(int(room.get("rotation",0))*90)))
		var angle: float = direction.angle()-PI
		canvas.draw_circle(point,cell_size*0.19,Color(0.08,0.55,0.7,0.10))
		canvas.draw_set_transform(point,angle,Vector2.ONE)
		preload("res://rooms/large-rooms/common.gd").sprite(canvas,"res://rooms/large-rooms/art/mini_sub.png",Rect2(-cell_size*0.23,-cell_size*0.11,cell_size*0.46,cell_size*0.22),Color("#b0a8a5") if int(state.get("damage",0))>0 else Color.WHITE)
		canvas.draw_set_transform(Vector2.ZERO,0.0,Vector2.ONE)

static func mission_state(room: Dictionary) -> Dictionary:
	if not room.has("moonbay_mission"):
		room["moonbay_mission"] = {"phase":"idle","progress":0.0,"crew":"","target":Vector2i(-1,-1),
			"order":"","cargo":{},"credited":true,"damage":0,"chamber_water":0.0,
			"station_open":true,"ocean_open":false,"recall":false,"hazard_roll":1.0,"last_result":""}
	return room.moonbay_mission

static func crew_problem(game, room: Dictionary, crew_id: String) -> String:
	if not Architects.IDS.has(crew_id): return "Choose an available crew member."
	var actor = Architects.actor_for(game,crew_id)
	if game.is_inside_tree() and not Architects.present(game,crew_id): return "That crew member is not aboard the station."
	if actor.dead or not actor.active: return "That crew member is unavailable."
	if not actor.expedition.is_empty() or not actor.moonbay_assignment.is_empty(): return "That crew member is already on a mission."
	if actor.goal not in ["","curiosity"] or actor.primary_room != Vector2i(-1,-1) or not actor.stage.is_empty() or not actor.locker_request.is_empty():
		return "That crew member has another job. Clear it before assignment."
	if actor.movement_medium != "dry": return "Crew must board from a dry room."
	if room.get("id","") != "moonbay": return "Select a Moonbay."
	return ""

static func _boarding_route(game, actor, room: Dictionary) -> PackedVector2Array:
	actor.rebuild(game)
	var start_cell: Vector2i = actor.cell_at(actor.foot)
	var board_cell: Vector2i = room.pos + Vector2i.ONE
	var start: int = actor.nearest_in_room(actor.foot,start_cell)
	var finish: int = actor.nearest_in_room((Vector2(board_cell)+Vector2.ONE*0.5)*actor.CELL,board_cell)
	if start<0 or finish<0: return PackedVector2Array()
	var route: PackedVector2Array = actor.graph.get_point_path(start,finish)
	if route.is_empty(): return route
	var previous: Vector2 = actor.foot
	for point in route:
		if not actor.segment_clear(previous,point): return PackedVector2Array()
		previous = point
	return actor.smooth_route(route)

static func dispatch(game, room: Dictionary, crew_id: String, target: Vector2i, order: String) -> String:
	if room.get("id","") != "moonbay": return "Select a Moonbay."
	if not game._ocean_face_problem(room).is_empty(): return "The ocean launch wall is obstructed. Clear it before dispatch."
	if not ORDERS.has(order): return "Choose Survey, Recover, or Deep Access."
	var state := mission_state(room)
	if state.phase != "idle": return "The mini-sub is already assigned."
	if int(state.damage)>0: return "The mini-sub needs repair before another launch."
	if not game.drone_fleet.sites.has(target): return "That site is no longer available."
	var site: Dictionary = game.drone_fleet.sites[target]
	if not site.get("active",false) or int(site.get("units",0))<=0: return "That site is depleted."
	if order == "survey" and site.get("discovered",false): return "That site is already surveyed."
	if order == "recover" and not site.get("discovered",false): return "Survey the site before recovery."
	if order == "deep_access" and (not site.get("moonbay_deep",false) or not site.get("discovered",false)):
		return "Survey a deep site before access."
	var crew_issue := crew_problem(game,room,crew_id)
	if not crew_issue.is_empty(): return crew_issue
	if not game.running or game.paused or not game.hardware.power or game.unpowered_room_cells.has(room.pos):
		return "Restore power and resume the station before launch."
	var actor = Architects.actor_for(game,crew_id)
	var route := PackedVector2Array()
	if game.is_inside_tree():
		route = _boarding_route(game,actor,room)
		if route.is_empty(): return "No safe route to the mini-sub boarding point."
	actor.path = route
	actor.goal = "moonbay"
	actor.goal_cell = room.pos + Vector2i.ONE
	actor.activity = "heading to the Moonbay" if not route.is_empty() else "aboard mini-sub"
	actor.moonbay_assignment = {"home":room.pos,"onboard":route.is_empty(),"arrival":route[-1] if not route.is_empty() else actor.foot}
	state["phase"] = "approach"
	state["progress"] = 0.0
	state["crew"] = crew_id
	state["target"] = target
	state["order"] = order
	state["cargo"] = {}
	state["credited"] = false
	state["recall"] = false
	state["hazard_roll"] = game.rng.randf()
	state["last_result"] = ""
	state["chamber_water"] = 0.0
	state["station_open"] = true
	state["ocean_open"] = false
	return ""

static func recall(_game, room: Dictionary) -> bool:
	var state := mission_state(room)
	if state.phase == "idle" or state.get("recall",false): return false
	state.recall = true
	state.last_result = "Mission recalled."
	if state.phase in ["approach","seal"]:
		state.phase = "unload"
		state.progress = 0.0
		state.station_open = true
	elif state.phase == "flood":
		state.phase = "drain"
		state.progress = (1.0-clampf(float(state.chamber_water),0.0,1.0))*float(DURATIONS.drain)
		state.ocean_open = false
	return true

static func repair(game, room: Dictionary) -> String:
	var state := mission_state(room)
	if state.phase != "idle": return "Wait for the mini-sub to return."
	if int(state.damage)<=0: return "The mini-sub is ready."
	if int(game.resources.get("metal",0))<REPAIR_METAL: return "Need 4 Metal to repair the mini-sub."
	game.resources.metal -= REPAIR_METAL
	state.damage = 0
	state.last_result = "Mini-sub repaired."
	return ""

static func tick(game, delta: float) -> void:
	if not game.running or game.paused or not game.hardware.power: return
	for room in game.placed_rooms:
		if room.get("id","") != "moonbay" or game.unpowered_room_cells.has(room.pos): continue
		var state := mission_state(room)
		if state.phase == "idle": continue
		var pilot = Architects.actor_for(game,str(state.crew))
		if pilot.dead and not str(state.last_result).begins_with("Pilot lost."): on_crew_death(game,pilot)
		if state.phase == "approach" and not Architects.actor_for(game,str(state.crew)).moonbay_assignment.get("onboard",false): continue
		_advance(game,room,state,maxf(0.0,delta))

static func advance_crew(game, actor, delta: float) -> void:
	if actor.dead or actor.moonbay_assignment.is_empty(): return
	var home: Vector2i = actor.moonbay_assignment.home
	if not game.occupied.has(home) or game.occupied[home].get("id","") != "moonbay":
		actor.moonbay_assignment.clear()
		actor.goal = ""
		return
	if not actor.moonbay_assignment.onboard:
		if not actor.path.is_empty(): actor.move(delta)
		if actor.path.is_empty():
			if actor.foot.distance_to(actor.moonbay_assignment.get("arrival",actor.foot))>4.0:
				var interrupted: Dictionary = mission_state(game.occupied[home])
				interrupted.phase = "idle"
				interrupted.progress = 0.0
				interrupted.crew = ""
				interrupted.order = ""
				interrupted.target = Vector2i(-1,-1)
				interrupted.cargo = {}
				interrupted.credited = true
				interrupted.last_result = "Boarding route obstructed. Mission cancelled."
				actor.moonbay_assignment.clear()
				actor.goal = ""
				return
			actor.moonbay_assignment.onboard = true
			actor.state = "idle"
			actor.activity = "aboard mini-sub"
	else:
		actor.activity = "mini-sub / " + str(mission_state(game.occupied[home]).phase)

static func _travel_duration(room: Dictionary, state: Dictionary) -> float:
	return 12.0 + float(absi(state.target.x-room.pos.x)+absi(state.target.y-room.pos.y))*1.2

static func _duration(room: Dictionary, state: Dictionary) -> float:
	if state.phase == "outbound" or state.phase == "return": return _travel_duration(room,state)
	if state.phase == "work" and state.order == "deep_access": return 18.0
	if state.phase == "work" and state.order == "recover": return 14.0
	return float(DURATIONS.get(state.phase,1.0))

static func _advance(game, room: Dictionary, state: Dictionary, delta: float) -> void:
	if state.phase == "work" and not state.recall and game.drone_fleet.sites.has(state.target):
		var target_site: Dictionary = game.drone_fleet.sites[state.target]
		if target_site.get("hazardous",false) and float(state.hazard_roll)<0.35:
			state.damage = 1
			state.last_result = "Hazard damaged the mini-sub. Early return."
			state.phase = "return"
			state.progress = 0.0
			return
	state.progress = minf(float(state.progress)+delta,_duration(room,state))
	var fraction: float = float(state.progress)/_duration(room,state)
	if state.phase == "flood": state.chamber_water = fraction
	if state.phase == "drain": state.chamber_water = 1.0-fraction
	if float(state.progress)<_duration(room,state): return
	state.progress = 0.0
	match str(state.phase):
		"approach": state.phase = "seal"; state.station_open = false
		"seal": state.phase = "flood"
		"flood": state.phase = "launch"; state.chamber_water = 1.0; state.ocean_open = true
		"launch": state.phase = "outbound"; state.ocean_open = false
		"outbound": state.phase = "return" if state.recall else "work"
		"work":
			_resolve_work(game,state)
			state.phase = "return"
		"return": state.phase = "drain"; state.ocean_open = false
		"drain": state.phase = "unload"; state.chamber_water = 0.0; state.station_open = true
		"unload":
			if not state.credited:
				for resource_id in state.cargo:
					game.resources[resource_id] = int(game.resources.get(resource_id,0)) + int(state.cargo[resource_id])
				state.credited = true
			state.phase = "idle"
			var actor = Architects.actor_for(game,str(state.crew))
			actor.moonbay_assignment.clear()
			if not actor.dead:
				actor.goal = ""
				actor.goal_cell = Vector2i(-1,-1)
				actor.activity = "returned from mini-sub mission"
			state.crew = ""
			state.order = ""
			state.target = Vector2i(-1,-1)
			state.cargo = {}
			state.recall = false
	# An open station entrance and an open ocean hatch can never coexist.
	assert(not state.station_open or not state.ocean_open)

static func _resolve_work(game, state: Dictionary) -> void:
	if state.recall:
		state.last_result = "Mission recalled."
		return
	if not game.drone_fleet.sites.has(state.target):
		state.last_result = "Target absent. Returning safely."
		return
	var site: Dictionary = game.drone_fleet.sites[state.target]
	if not site.get("active",false) or int(site.get("units",0))<=0:
		state.last_result = "Target depleted. Returning safely."
		return
	match str(state.order):
		"survey":
			preload("res://scripts/site_discovery.gd").reveal_moonbay_target(game,state.target)
			state.last_result = "Survey complete. Site identified."
		"recover":
			site.units -= 1
			state.cargo = {"metal":4,"data":2} if site.kind == "salvage" else {"metal":6}
			if site.get("hazardous",false):
				state.cargo.metal = int(state.cargo.get("metal",0))+2
				state.cargo.data = int(state.cargo.get("data",0))+1
			state.last_result = "Cargo secured. Returning."
		"deep_access":
			site.units -= 1
			site.deep_accessed = true
			state.cargo = {"data":6,"rare_minerals":2} if site.get("hazardous",false) else {"data":4,"rare_minerals":1}
			state.last_result = "Deep site reached. Returning."
