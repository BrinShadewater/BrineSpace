extends RefCounted
const Architects=preload("res://scripts/architects.gd")
const Service=preload("res://scripts/airlock_service.gd")

static func seek_locker(game,actor,id: String) -> bool:
	if not actor.needs_air(): return false
	if actor.movement_medium!="dry" or not actor.locker_request.is_empty() or actor.helmet_action_active(): return false
	for room in game.placed_rooms:
		if room.id!="airlock" or float(room.get("water_level",0))>=0.25: continue
		if Service.request(game,id,room.pos,actor.helmet_equipped):
			var distance := 0.0
			var exposed := false
			var from: Vector2=actor.foot
			for point in actor.path:
				var length: float=from.distance_to(point)
				distance+=length
				for i in range(int(ceil(length/48.0))+1):
					var sample: Vector2=from.lerp(point,minf(1,i*48.0/maxf(1,length)))
					if float(game.occupied.get(actor.cell_at(sample),{}).get("water_level",0))>=0.85: exposed=true
				from=point
			var available: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
			if not exposed or distance/25.3+5<available: return true
			actor.locker_request.clear()
			actor.path.clear()
			actor.goal=""
			actor.state="idle"
			actor.activity="locker route exceeds air reserve"
	return false

static func escape_route(game,actor) -> Dictionary:
	var start: int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0: return {}
	var best := INF
	var found := {}
	for room in game.placed_rooms:
		if float(room.get("water_level",0))>=0.25 or float(room.get("hull_crack",0))>0: continue
		for node in actor.room_nodes.get(room.pos,[]):
			var point: Vector2=actor.graph.get_point_position(node)
			var distance: float=actor.foot.distance_to(point)
			if distance>=best: continue
			var route: PackedVector2Array=actor.smooth_route(actor.route_between(start,node))
			if route.is_empty(): continue
			var length := 0.0
			var from: Vector2=actor.foot
			for step in route:
				length+=from.distance_to(step)
				from=step
			if length>=best: continue
			best=length
			found={"cell":room.pos,"route":route,"seconds":length/25.3}
	return found

static func advance(game,actor,dt: float) -> bool:
	if not actor.needs_air(): return false
	if not actor.expedition.is_empty(): return false
	var id: String="bill" if actor==game.bill_npc else "veld" if actor==game.veld_npc else "marsh" if actor==game.marsh_npc else "branforth"
	if actor.goal=="flood-retreat":
		if not actor.path.is_empty(): actor.move(dt); return true
		actor.goal=""
		actor.state="idle"
		actor.activity="reached flood refuge"
		seek_locker(game,actor,id)
		return true
	var room: Dictionary=game.occupied.get(actor.cell_at(actor.foot),{})
	var air: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
	if float(room.get("water_level",0))<0.85 or air>35:
		actor.set_meta("flood_blocked_warning",false)
		return false
	var cooldown: float=actor.get_meta("flood_safety_wait",0.0)
	actor.set_meta("flood_safety_wait",maxf(0,cooldown-dt))
	if cooldown>0 and actor.get_meta("flood_blocked_warning",false): return true
	if cooldown>0 and air>12: return false
	actor.set_meta("flood_safety_wait",0.5)
	var route := escape_route(game,actor)
	if not route.is_empty() and air>float(route.seconds)+5: return false
	if route.is_empty() and air>12: return false
	for target in game.placed_rooms:
		if target.get("leak_repair",{}).get("worker","")==id:
			target.leak_repair.worker=""
			target.leak_repair.status="Repair paused / crew needs air"
	if route.is_empty():
		actor.goal=""
		actor.path.clear()
		actor.state="idle"
		actor.activity="LOW AIR / escape path blocked"
		if not actor.get_meta("flood_blocked_warning",false):
			game._log("%s: LOW AIR. No reachable dry refuge. Open a route or drain the room." % Architects.NAMES[id],true)
		actor.set_meta("flood_blocked_warning",true)
		return true
	actor.cancel_helmet_action()
	actor.locker_request.clear()
	actor.stage=""
	actor.goal="flood-retreat"
	actor.goal_cell=route.cell
	actor.path=route.route
	actor.state="walk"
	actor.activity="retreating for air"
	game._log("%s abandoning flooded worksite. Air reserve critical." % Architects.NAMES[id],true)
	return true
