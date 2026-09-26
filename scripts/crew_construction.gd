extends RefCounted
## Paid orders own progress; crew only advance it while at a reachable sealed connection.
const Architects = preload("res://scripts/architects.gd")
const WORK_SECONDS := 10.0
const APPROACH_RETRY_SECONDS := 1.0
const DIRS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
const NAMES := ["north","east","south","west"]

# A failed approach is a full route search per candidate node. Repeating it every
# frame for an unreachable order cost ~5 ms per eligible crew member, so retry on
# a short timer or as soon as the actor's station topology changes.
static func approach_deferred(actor,order: Dictionary) -> bool:
	var entry = actor.get_meta("construction_approach_retry",{}).get(order_key(order))
	return entry != null and entry[1] == actor.signature and float(entry[0]) > 0.0

static func defer_approach(actor,order: Dictionary) -> void:
	var retry: Dictionary = actor.get_meta("construction_approach_retry",{})
	retry[order_key(order)] = [APPROACH_RETRY_SECONDS,actor.signature]
	actor.set_meta("construction_approach_retry",retry)

static func tick_approach_retries(actor,delta: float) -> void:
	var retry: Dictionary = actor.get_meta("construction_approach_retry",{})
	for key in retry.keys():
		retry[key][0] = float(retry[key][0]) - maxf(delta,0.0)
		if retry[key][0] <= 0.0: retry.erase(key)

static func order_key(order: Dictionary) -> String:
	return "%s@%s/%d" % [order.id,order.pos,int(order.rotation)]

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
			var route: PackedVector2Array=actor.route_between(start,node)
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
		actor.remove_meta("construction_approach_retry")
		return false
	tick_approach_retries(actor,delta)
	var id: String="bill" if actor==game.bill_npc else "veld" if actor==game.veld_npc else "marsh" if actor==game.marsh_npc else "branforth"
	var order: Dictionary={}
	for candidate in game.drone_fleet.orders:
		if candidate.get("builder","")==id: order=candidate; break
	if order.is_empty():
		if actor.goal=="construction": release(actor)
		if actor.helmet_equipped or actor.helmet_action_active() or not actor.locker_request.is_empty() or not actor.stage.is_empty() or actor.movement_medium!="dry": return false
		if not game.running or game.paused or not game.hardware.power or game.hardware.doors: return false
		var has_bay: bool=game.drone_fleet.drones.values().any(func(d): return d.kind=="construction" and not d.bootstrap)
		if has_bay and game.drone_fleet._dedicated_builder_ready(game.powered_room_cells): return false
		# One manual builder at a time; dedicated bays can take the other orders.
		for candidate in game.drone_fleet.orders:
			if not str(candidate.get("builder","")).is_empty(): return false
		# Only a crew member about to claim a new build needs this route search.
		# Empty queues and ineligible swimmers previously searched every meal/bed
		# node each frame. Existing builders still finish before taking a break.
		if preload("res://scripts/crew_primary_work.gd").break_needed(game,actor): return false
		for candidate in game.drone_fleet.orders:
			if approach_deferred(actor,candidate): continue
			var found:=approach(game,actor,candidate)
			if found.is_empty():
				defer_approach(actor,candidate)
				continue
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
			var found:={} if approach_deferred(actor,order) else approach(game,actor,order)
			if found.is_empty():
				if not approach_deferred(actor,order): defer_approach(actor,order)
				actor.state="idle"; actor.activity="construction / approach blocked"; return true
			for key in ["work_point","work_cell","facing"]: order[key]=found[key]
			actor.path=found.route
		actor.move(delta)
		return true
	actor.path.clear()
	actor.direction=order.facing
	actor.state="weld"
	order["work"]=minf(WORK_SECONDS,float(order.get("work",0.0))+maxf(delta,0.0)*preload("res://scripts/research_tree.gd").build_rate(game.get("meta")))
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
