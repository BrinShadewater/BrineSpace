extends RefCounted
const Architects = preload("res://scripts/architects.gd")
const Cycle = preload("res://scripts/airlock_cycle.gd")
const Service = preload("res://scripts/airlock_service.gd")
const Routes = preload("res://scripts/drone_routes.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")
const PHASES := ["approach","enter","pressurize","leave","outbound","salvage","pickup","return","entry","drain","exit","unload"]
const OXYGEN_COST := 2

static func point(room: Dictionary,local: Vector2) -> Vector2:
	return (Vector2(room.pos)+Vector2.ONE*0.5)*384 + Geometry.turn(local,int(room.rotation))

static func blockers(game) -> Dictionary:
	var result := {}
	for room in game.placed_rooms: result[room.pos] = true
	for cell in game.wrecks:
		if preload("res://scripts/wreck_field.gd").blocks(game.wrecks,cell): result[cell] = true
	for cell in game.drone_fleet.sites:
		if game.drone_fleet.Sites.blocks(game.drone_fleet.sites,cell): result[cell] = true
	for order in game.drone_fleet.orders: result[order.pos] = true
	for drone in game.drone_fleet.drones.values():
		if not drone.order.is_empty(): result[drone.order.pos] = true
	return result

static func reserved(game,cell: Vector2i) -> bool:
	for id in Architects.IDS:
		var actor = Architects.actor_for(game,id)
		if actor.expedition.is_empty(): continue
		if cell == actor.expedition.home or cell == actor.expedition.target or cell == actor.cell_at(actor.foot): return true
		for p in actor.expedition.sea_route:
			if actor.cell_at(p) == cell: return true
		for p in actor.expedition.route:
			if actor.cell_at(p) == cell: return true
	return false

static func reason(game,id: String,cell: Vector2i) -> String:
	var actor = Architects.actor_for(game,id)
	if not actor.expedition.is_empty(): return "Expedition in progress. Recall remains available."
	if not Architects.present(game,id) or not actor.active or actor.dead: return "Choose an awake architect."
	if not Service.ready(game,cell): return "Restore power and resume the airlock."
	if not actor.needs_air() and (actor.battery<=actor.RETURN_AT or actor.returning_to_pod): return "Recharge Marsh at his pod before dispatch."
	if actor.needs_air() and not actor.helmet_equipped: return "Fit a diving helmet at the locker first."
	if actor.needs_air() and actor.tank_oxygen < 55: return "Refill the helmet tank at the diving locker before dispatch."
	if actor.helmet_action_active() or not actor.locker_request.is_empty() or not actor.stage.is_empty(): return "Wait for the current crew action."
	if Cycle.state(game.occupied[cell]).phase != "dry": return "Drain the chamber before dispatch."
	if not Cycle.exterior_clear(game,game.occupied[cell]): return "Clear the exterior hatch approach."
	if actor.needs_air() and int(game.resources.oxygen) < OXYGEN_COST: return "Reserve 2 Oxygen for the complete outward and return trip."
	for other in Architects.IDS:
		var peer = Architects.actor_for(game,other)
		if not peer.expedition.is_empty() and peer.expedition.home == cell: return "Airlock reserved by another expedition."
	return ""

static func dispatch(game,id: String,cell: Vector2i) -> bool:
	if not reason(game,id,cell).is_empty(): return false
	var actor = Architects.actor_for(game,id)
	actor.rebuild(game)
	var room: Dictionary = game.occupied[cell]
	var approach := point(room,Vector2(0,68))
	var a: int = actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	var b: int = actor.nearest_in_room(approach,cell)
	if a < 0 or b < 0 or not actor.can_stand(approach): return false
	var route: PackedVector2Array = actor.graph.get_point_path(a,b)
	if route.is_empty(): return false
	route.append(approach)
	var previous: Vector2 = actor.foot
	for p in route:
		if not actor.segment_clear(previous,p): return false
		previous = p
	var outside: Vector2i = actor.cell_at(point(room,Vector2(0,-384)))
	var blocked := blockers(game)
	if blocked.has(outside): return false
	var target := Vector2i(-1,-1)
	var sea: Array = []
	var candidates: Array = game.drone_fleet.sites.keys()
	candidates.sort_custom(func(x,y): return Vector2(x).distance_squared_to(Vector2(outside)) < Vector2(y).distance_squared_to(Vector2(outside)))
	for candidate in candidates:
		var site: Dictionary = game.drone_fleet.sites[candidate]
		if site.kind != "salvage" or not site.discovered or not site.active or site.units <= 0 or reserved(game,candidate): continue
		sea = Routes.find_path(outside,candidate,blocked,true)
		if not sea.is_empty() and (float(sea.size())*384.0+314.0)*2.0/72.0+18.0 <= (actor.tank_oxygen if actor.needs_air() else actor.battery*actor.BATTERY_SECONDS/100.0-30.0):
			target = candidate
			break
	if target.x < 0: return false
	var sea_route := PackedVector2Array([point(room,Vector2(0,-384))])
	for p in sea: sea_route.append((Vector2(p)+Vector2.ONE*0.5)*384)
	if actor.needs_air(): game.resources.oxygen -= OXYGEN_COST
	actor.path.clear()
	actor.goal = ""
	actor.expedition = {"phase":"approach","home":cell,"target":target,"route":route,"sea_route":sea_route,"elapsed":0.0,"cargo":{},"recall":false}
	game.play_station_sound("crew_dispatch",Vector2(cell))
	game._log("Marsh dispatched without breathing gear. Watch his battery; his pod is the return destination after unloading." if not actor.needs_air() else "%s dispatched. Tank endurance: 60 seconds underwater. Watch the return distance. Cargo is credited only after safe return." % Architects.NAMES[id],false)
	game._refresh_all()
	return true

static func request_recall(game,actor) -> bool:
	if actor.expedition.is_empty() or actor.expedition.recall: return false
	actor.expedition.recall = true
	game.play_station_sound("ui_recall")
	return true

static func move(actor,e: Dictionary,delta: float) -> bool:
	var route: PackedVector2Array = e.route
	var remaining := delta*72.0*(0.25 if not actor.needs_air() and actor.battery<=0 else 1.0)
	actor.state = "walk"
	while remaining > 0 and not route.is_empty():
		var distance: float = actor.foot.distance_to(route[0])
		actor.direction = actor.travel_heading(actor.foot,route[0],actor.direction)
		actor.foot = actor.foot.move_toward(route[0],remaining)
		remaining -= distance
		if actor.foot.is_equal_approx(route[0]): route.remove_at(0)
	e.route = route
	return route.is_empty()

static func set_route(e: Dictionary,phase: String,route: PackedVector2Array) -> void:
	e.phase = phase
	e.route = route
	e.elapsed = 0.0

static func advance(game,actor,delta: float) -> void:
	if actor.expedition.is_empty() or actor.dead: return
	var e: Dictionary = actor.expedition
	if actor.needs_air() and actor.tank_oxygen <= 25 and e.phase in ["outbound","salvage","pickup"] and not e.recall:
		request_recall(game,actor)
		game._log("Diver recalled: oxygen reserve is falling. The return journey still requires breathing.",true)
	if not actor.needs_air() and e.phase in ["outbound","salvage","pickup"] and not e.recall:
		var return_seconds: float=float(e.sea_route.size())*384.0/72.0+30.0
		if actor.battery<=actor.RETURN_AT or actor.battery*actor.BATTERY_SECONDS/100.0<=return_seconds:
			request_recall(game,actor)
			actor.returning_to_pod=true
			game._log("Marsh recalled: battery reserve is needed for the return to his charging pod.",true)
	actor.activity = "expedition / " + e.phase
	if not game.occupied.has(e.home):
		actor.activity = "return airlock missing / awaiting recovery"
		return
	var room: Dictionary = game.occupied[e.home]
	var operational := Service.ready(game,e.home)
	if not operational and e.phase not in ["outbound","salvage","pickup","return"]:
		actor.activity = "airlock power lost / safe hold"
		actor.state = "idle"
		return
	match e.phase:
		"approach":
			if move(actor,e,delta): set_route(e,"enter",PackedVector2Array([point(room,Vector2(0,-70))]))
		"enter":
			if Cycle.state(room).phase != "dry": return
			if move(actor,e,delta) and Cycle.request(game,e.home,true):
				e.phase = "pressurize"
				actor.state = "idle"
		"pressurize":
			if Cycle.pose(room).water >= 0.55: actor.set_movement_medium("flooded")
			if Cycle.state(room).phase == "exterior":
				actor.set_movement_medium("exterior")
				set_route(e,"leave",PackedVector2Array([point(room,Vector2(0,-384))]))
		"leave":
			if move(actor,e,delta): set_route(e,"outbound",e.sea_route.duplicate())
		"outbound":
			if e.recall:
				var back := PackedVector2Array()
				back.append((Vector2(actor.cell_at(actor.foot))+Vector2.ONE*0.5)*384)
				var path := Routes.find_path(actor.cell_at(actor.foot),actor.cell_at(point(room,Vector2(0,-384))),blockers(game),true)
				for p in path: back.append((Vector2(p)+Vector2.ONE*0.5)*384)
				if not path.is_empty(): set_route(e,"return",back)
			elif move(actor,e,delta):
				e.phase = "salvage"
				actor.state = "idle"
		"salvage":
			e.elapsed += delta
			if e.elapsed>=5.48 or e.recall:
				set_route(e,"pickup",PackedVector2Array())
		"pickup":
			e.elapsed+=delta
			if e.elapsed >= 0.52 or e.recall:
				if not e.recall and game.drone_fleet.sites.has(e.target):
					var site: Dictionary = game.drone_fleet.sites[e.target]
					if site.units > 0 and site.active:
						site.units -= 1
						e.cargo = game.drone_fleet.Sites.LOADS.salvage.duplicate()
				var back: PackedVector2Array = e.sea_route.duplicate()
				back.reverse()
				set_route(e,"return",back)
		"return":
			if move(actor,e,delta): set_route(e,"entry",PackedVector2Array([point(room,Vector2(0,-70))]))
		"entry":
			if Cycle.state(room).phase != "exterior": return
			if move(actor,e,delta) and Cycle.request(game,e.home,false):
				e.phase = "drain"
				actor.state = "idle"
		"drain":
			if Cycle.state(room).phase == "dry":
				actor.set_movement_medium("dry")
				set_route(e,"exit",PackedVector2Array([point(room,Vector2(0,68))]))
		"exit":
			if move(actor,e,delta):
				set_route(e,"unload",PackedVector2Array())
				actor.state="idle"
		"unload":
			e.elapsed+=delta
			if e.elapsed>=0.52:
				var recovered: bool = not e.cargo.is_empty()
				game._apply_delta(e.cargo)
				if recovered: game.play_station_sound("cargo",Vector2(e.home))
				else: game.play_station_sound("crew_return",Vector2(e.home))
				game._clamp_resource_storage()
				actor.expedition.clear()
				actor.state = "idle"
				actor.timer = 1.0
				actor.activity = "returned safely from exterior"
				if recovered: preload("res://scripts/transmission_archive.gd").recover(game,"survey")
				game._log("Exterior crew returned through a dry chamber. " + ("Salvage delivered to storage." if recovered else "No cargo recovered."),false)
				game._refresh_all()

static func valid(e: Variant) -> bool:
	if not e is Dictionary: return false
	if e.is_empty(): return true
	if not PHASES.has(e.get("phase")) or not e.get("recall") is bool: return false
	for key in ["home","target"]:
		if not e.get(key) is Vector2i or e[key].x<0 or e[key].y<0 or e[key].x>=40 or e[key].y>=40: return false
	for key in ["route","sea_route"]:
		if not e.get(key) is PackedVector2Array or e[key].size()>1602: return false
		for p in e[key]:
			if not p.is_finite() or p.x<0 or p.y<0 or p.x>15360 or p.y>15360: return false
	if not e.get("elapsed") is float or not is_finite(e.elapsed) or e.elapsed<0 or e.elapsed>7: return false
	if not e.get("cargo") is Dictionary: return false
	if not e.cargo.is_empty() and not e.phase in ["return","entry","drain","exit","unload"]: return false
	return e.cargo.is_empty() or e.cargo == {"metal":1,"data":1}

static func valid_crew_rooms(crew: Variant,rooms: Array) -> bool:
	if crew == null: return true # Legacy checkpoint without crew simulation.
	if not crew is Dictionary: return false
	var homes := {}
	for id in Architects.IDS:
		var member: Dictionary = crew.get(id,{})
		var e: Dictionary = member.get("expedition",{})
		if e.is_empty(): continue
		if not valid(e) or homes.has(e.home): return false
		homes[e.home] = true
		var found := false
		for room in rooms:
			if room.get("pos") == e.home and room.get("id") == "airlock":
				found = true
				var phase: String = Cycle.state(room).phase
				if e.phase in ["approach","enter","exit","unload"] and phase != "dry": return false
				if e.phase in ["leave","outbound","salvage","pickup","return","entry"] and phase != "exterior": return false
		if not found: return false
	return true

