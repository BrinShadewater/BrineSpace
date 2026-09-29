extends RefCounted
## One mission and launch chamber per Moonbay. State is persisted on the room.

const ORDERS := ["survey","recover","deep_access"]
const REPAIR_METAL := 4
const Architects = preload("res://scripts/architects.gd")
const DURATIONS := {"approach":12.0,"seal":3.0,"flood":6.0,"launch":3.0,
	"work":10.0,"drain":6.0,"unload":3.0}

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
	actor.moonbay_assignment = {"home":room.pos,"onboard":route.is_empty()}
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
		if state.phase == "approach" and not Architects.actor_for(game,str(state.crew)).moonbay_assignment.get("onboard",false): continue
		_advance(game,room,state,maxf(0.0,delta))

static func advance_crew(game, actor, delta: float) -> void:
	if actor.moonbay_assignment.is_empty(): return
	var home: Vector2i = actor.moonbay_assignment.home
	if not game.occupied.has(home) or game.occupied[home].get("id","") != "moonbay":
		actor.moonbay_assignment.clear()
		actor.goal = ""
		return
	if not actor.moonbay_assignment.onboard:
		if not actor.path.is_empty(): actor.move(delta)
		if actor.path.is_empty():
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
			state.last_result = "Cargo secured. Returning."
		"deep_access":
			site.deep_accessed = true
			state.cargo = {"data":4,"rare_minerals":1}
			state.last_result = "Deep site reached. Returning."
