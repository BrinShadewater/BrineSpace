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
	var targets := {}
	for room in game.placed_rooms:
		if float(room.get("water_level",0))>=0.25 or float(room.get("hull_crack",0))>0: continue
		for node in actor.room_nodes.get(room.pos,[]): targets[node]=true
	if targets.is_empty(): return {}
	# One search to the nearest refuge node. A search per refuge node never finished when
	# no route existed, and a swimmer standing where its swim outline did not fit had none.
	var facing: String=actor.direction
	for start in escape_starts(actor):
		for avoid_crew in [true,false]:
			var route: PackedVector2Array=actor.route_to_any(start.node,targets,avoid_crew,start.point if start.squeeze else actor.foot)
			if route.is_empty(): continue
			# Smooth with the facing the route starts with (it may begin with an in-place turn).
			actor.direction=actor.route_facing
			var smooth: PackedVector2Array=actor.smooth_route(route,start.point if start.squeeze else Vector2.INF)
			actor.direction=facing
			if smooth.is_empty(): continue
			if start.squeeze: smooth.insert(0,start.point)
			var length := 0.0
			var from: Vector2=actor.foot
			for step in smooth:
				length+=from.distance_to(step)
				from=step
			return {"cell":actor.cell_at(route[route.size()-1]),"route":smooth,"seconds":length/25.3,"squeeze":start.point if start.squeeze else Vector2.INF,"facing":actor.route_facing}
	return {}

# Where an escape may begin: the nearest node the actor reaches with its current body, then
# nearby nodes it can squeeze to on standing clearance, when water caught it somewhere its
# swim outline does not fit (beside a doorway, say).
static func escape_starts(actor) -> Array:
	var starts := []
	var cell: Vector2i=actor.cell_at(actor.foot)
	var normal: int=actor.nearest_in_room(actor.foot,cell)
	var normal_clear := false
	if normal>=0:
		var point: Vector2=actor.graph.get_point_position(normal)
		normal_clear=actor.travel_segment_clear(actor.foot,point,actor.direction)
		if normal_clear: starts.append({"node":normal,"point":point,"squeeze":false})
	var nearby := []
	for dy in range(-1,2):
		for dx in range(-1,2):
			for node in actor.room_nodes.get(cell+Vector2i(dx,dy),[]):
				if node==normal and normal_clear: continue
				var point: Vector2=actor.graph.get_point_position(node)
				var distance: float=actor.foot.distance_to(point)
				if distance<=192.0: nearby.append([distance,node,point])
	nearby.sort_custom(func(a,b): return a[0]<b[0])
	for entry in nearby.slice(0,8):
		if actor.segment_clear(actor.foot,entry[2]): starts.append({"node":entry[1],"point":entry[2],"squeeze":true})
	return starts

static func advance(game,actor,dt: float) -> bool:
	if not actor.needs_air(): return false
	if not actor.expedition.is_empty(): return false
	var id: String="bill" if actor==game.bill_npc else "veld" if actor==game.veld_npc else "marsh" if actor==game.marsh_npc else "branforth"
	if actor.goal=="flood-retreat":
		if not actor.path.is_empty():
			# The swimmer's own transit opens doors that spread water forward, so the
			# chosen refuge can flood mid-route; re-check it and re-route while air remains.
			var recheck: float=actor.get_meta("flood_retreat_check",0.0)
			actor.set_meta("flood_retreat_check",maxf(0,recheck-dt))
			if recheck<=0:
				actor.set_meta("flood_retreat_check",1.0)
				var refuge: Dictionary=game.occupied.get(actor.goal_cell,{})
				if float(refuge.get("water_level",0))>=0.25 or float(refuge.get("hull_crack",0))>0:
					var replacement := escape_route(game,actor)
					if not replacement.is_empty():
						actor.goal_cell=replacement.cell
						actor.path=replacement.route
						actor.squeeze_point=replacement.squeeze
						actor.direction=replacement.facing
			actor.move(dt); return true
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
	actor.squeeze_point=route.squeeze
	actor.direction=route.facing
	actor.state="walk"
	actor.activity="retreating for air"
	game._log("%s abandoning flooded worksite. Air reserve critical." % Architects.NAMES[id],true)
	return true
