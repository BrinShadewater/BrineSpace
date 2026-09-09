extends RefCounted
## Paid orders own progress; crew only advance it while at a reachable sealed connection.
const Architects = preload("res://scripts/architects.gd")
const WORK_SECONDS := 10.0
const DIRS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
const NAMES := ["north","east","south","west"]

static func reconcile(game) -> void:
	for order in game.drone_fleet.orders:
		var id: String = order.get("builder","")
		if id.is_empty(): continue
		var actor = game.get(id+"_npc")
		if not Architects.present(game,id) or actor.dead or actor.movement_medium!="dry" or actor.helmet_equipped or not actor.expedition.is_empty() or actor.helmet_action_active() or not actor.locker_request.is_empty():
			order.erase("builder")
			order.erase("work_point")
			order.erase("work_cell")
			order.erase("facing")
			if actor.goal=="construction": release(actor)

static func release(actor) -> void:
	actor.goal=""
	actor.path.clear()
	actor.state="idle"
	actor.timer=0.5
	actor.activity="construction paused"

static func approach(game,actor,order: Dictionary) -> Dictionary:
	var start: int = actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0: return {}
	var best: Dictionary={}
	var best_distance:=INF
	for side in range(4):
		var cell: Vector2i=order.pos-DIRS[side]
		if not game.occupied.has(cell): continue
		if not game._doors_connect(order.id,int(order.rotation),-DIRS[side],game.occupied[cell]): continue
		var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*actor.CELL
		var desired: Vector2=center+Vector2(DIRS[side])*160.0
		for node in actor.room_nodes.get(cell,[]):
			var point: Vector2=actor.graph.get_point_position(node)
			if point.distance_to(desired)>44 or not actor.can_stand(point): continue
			var route: PackedVector2Array=actor.graph.get_point_path(start,node)
			if route.is_empty() or not actor.segment_clear(actor.foot,route[0]): continue
			var distance: float=actor.foot.distance_to(route[0])
			for i in range(1,route.size()): distance+=route[i-1].distance_to(route[i])
			distance+=point.distance_to(desired)*4
			if distance>=best_distance: continue
			best_distance=distance
			best={"work_point":point,"work_cell":cell,"facing":NAMES[side],"route":actor.smooth_route(route)}
	return best

static func advance(game,actor,delta: float) -> bool:
	if game.drone_fleet.orders.is_empty():
		if actor.goal=="construction": release(actor)
		return false
	var id: String="bill" if actor==game.bill_npc else "veld" if actor==game.veld_npc else "marsh" if actor==game.marsh_npc else "branforth"
	var order: Dictionary={}
	for candidate in game.drone_fleet.orders:
		if candidate.get("builder","")==id: order=candidate; break
	if order.is_empty():
		if actor.goal=="construction": release(actor)
		if actor.helmet_equipped or actor.helmet_action_active() or not actor.locker_request.is_empty() or not actor.stage.is_empty() or actor.movement_medium!="dry": return false
		if not game.running or game.paused or not game.hardware.power or game.hardware.doors: return false
		var has_bay: bool=game.drone_fleet.drones.values().any(func(d): return d.kind=="construction" and not d.bootstrap)
		if has_bay and game.drone_fleet._dedicated_builder_ready(game._simulate_room_economy().working_cells): return false
		# One manual builder at a time; dedicated bays can take the other orders.
		for candidate in game.drone_fleet.orders:
			if not str(candidate.get("builder","")).is_empty(): return false
		for candidate in game.drone_fleet.orders:
			var found:=approach(game,actor,candidate)
			if found.is_empty(): continue
			order=candidate
			order["builder"]=id
			for key in ["work_point","work_cell","facing"]: order[key]=found[key]
			actor.path=found.route
			actor.stage=""
			actor.timer=0.0
			break
	if order.is_empty(): return false
	actor.goal="construction"
	actor.goal_cell=order.work_cell
	actor.activity="assembling room / "+str(roundi(float(order.get("work",0.0))/WORK_SECONDS*100))+"%"
	if not game.running or game.paused or not game.hardware.power or game.hardware.doors or game.occupied.get(order.work_cell,{}).get("suspended",false):
		actor.state="idle"
		actor.activity="construction held / restore station access"
		return true
	if not game.occupied.has(order.work_cell) or not actor.can_stand(order.work_point) or not game._doors_connect(order.id,int(order.rotation),order.work_cell-order.pos,game.occupied.get(order.work_cell,{})):
		order.erase("builder")
		release(actor)
		return true
	if actor.foot.distance_to(order.work_point)>1.0:
		actor.activity="heading to construction seal"
		if actor.path.is_empty():
			var found:=approach(game,actor,order)
			if found.is_empty(): actor.state="idle"; actor.activity="construction / approach blocked"; return true
			for key in ["work_point","work_cell","facing"]: order[key]=found[key]
			actor.path=found.route
		actor.move(delta)
		return true
	actor.path.clear()
	actor.direction=order.facing
	actor.state="weld"
	order["work"]=minf(WORK_SECONDS,float(order.get("work",0.0))+maxf(delta,0.0))
	actor.timer=float(order.work)
	if order.work>=WORK_SECONDS:
		game.drone_fleet.orders.erase(order)
		release(actor)
		actor.activity="construction complete"
		var prior: int=game.selected_rotation
		game.selected_rotation=order.rotation
		game._place_room(order.id,order.pos,false,true)
		game.selected_rotation=prior
		game._refresh_all()
	return true
