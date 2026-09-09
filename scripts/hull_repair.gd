extends RefCounted
const Architects = preload("res://scripts/architects.gd")
const NAMES := ["Hairline crack","Split seam","Hull rupture"]
const SEVERITIES := [0.2,0.5,0.8]
const COSTS := [2,3,5]
const SECONDS := [6.0,10.0,14.0]

static func variant(room: Dictionary) -> int:
	var severity := float(room.get("hull_crack",0))
	return 0 if severity<=0.35 else 1 if severity<=0.7 else 2

static func request(game,cell: Vector2i) -> bool:
	if not game.running or not game.occupied.has(cell): return false
	var room: Dictionary=game.occupied[cell]
	if float(room.get("hull_crack",0))<=0 or room.has("leak_repair"): return false
	var index := variant(room)
	if int(game.resources.metal)<COSTS[index]: return false
	game.resources.metal-=COSTS[index]
	room.leak_repair={"cost":COSTS[index],"duration":SECONDS[index],"progress":0.0,"worker":"","status":"Waiting for reachable crew"}
	game._log("Hull repair queued at %s. %d Metal reserved." % [cell,COSTS[index]],false)
	return true

static func cancel(game,cell: Vector2i) -> bool:
	if not game.occupied.has(cell) or not game.occupied[cell].has("leak_repair"): return false
	var room: Dictionary=game.occupied[cell]
	var job: Dictionary=room.leak_repair
	if not str(job.worker).is_empty():
		var actor=Architects.actor_for(game,job.worker)
		if actor.goal=="hull-repair": release(actor)
	# Used patch material is consumed; unstarted orders refund in full.
	var refund := int(floor(float(job.cost)*(1.0-float(job.progress)/float(job.duration))))
	game.resources.metal+=refund
	room.erase("leak_repair")
	game._log("Hull repair cancelled. %d Metal returned." % refund,false)
	return true

static func reassign(game,cell: Vector2i,id: String) -> bool:
	if id not in Architects.IDS or not Architects.present(game,id) or not game.occupied.has(cell): return false
	var room: Dictionary=game.occupied[cell]
	if not room.has("leak_repair"): return false
	var job: Dictionary=room.leak_repair
	if not str(job.worker).is_empty():
		var actor=Architects.actor_for(game,job.worker)
		if actor.goal=="hull-repair": release(actor)
	job.worker=""
	job.preferred=id
	job.status="Waiting for assigned crew"
	return true

static func air_needed(room: Dictionary,job: Dictionary,travel: float,drain := 0.0) -> float:
	var duration := travel+float(job.duration)-float(job.progress)
	var water := float(room.get("water_level",0))
	var rate := maxf(0,float(room.get("hull_crack",0))*0.04-drain)
	var projected := minf(1,water+rate*duration)
	if projected<0.85: return 0.0
	var until_critical := maxf(0,(0.85-water)/rate) if rate>0 else (0.0 if water>=0.85 else INF)
	var exposure := maxf(0,duration-until_critical)
	# Include recovery while a powered pump lowers water below breathing height.
	var recovery := (projected-0.84)/drain+3.0 if drain>0 else 12.0
	return exposure+maxf(3,recovery)

static func release(actor) -> void:
	actor.goal=""
	actor.path.clear()
	actor.state="idle"
	actor.timer=0.5
	actor.activity="hull repair waiting"

static func approach(actor,cell: Vector2i) -> Dictionary:
	var desired := (Vector2(cell)+Vector2.ONE*0.5)*384+Vector2(-70,-115)
	# Already at the worksite: no synthetic navigation turn is needed to resume.
	if actor.cell_at(actor.foot)==cell and actor.foot.distance_to(desired)<30 and actor.can_stand(actor.foot):
		return {"point":actor.foot,"route":PackedVector2Array()}
	var start: int=actor.nearest_in_room(actor.foot,actor.cell_at(actor.foot))
	if start<0: return {}
	var best := INF
	var found := {}
	for node in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(node)
		if point.distance_to(desired)>50 or not actor.can_stand(point): continue
		var path: PackedVector2Array=actor.route_between(start,node)
		if path.is_empty() or not actor.segment_clear(actor.foot,path[0]): continue
		var score: float = point.distance_to(desired)*4+actor.foot.distance_to(point)
		if score>=best: continue
		var route: PackedVector2Array=actor.smooth_route(path)
		if route.is_empty(): continue
		best=score
		found={"point":point,"route":route}
	return found

static func advance(game,actor,dt: float) -> bool:
	var id: String="bill" if actor==game.bill_npc else "veld" if actor==game.veld_npc else "marsh" if actor==game.marsh_npc else "branforth"
	var eligible: bool=actor.expedition.is_empty() and not actor.helmet_action_active() and actor.locker_request.is_empty() and actor.goal!="construction" and not (actor.activity=="refilling oxygen tank" and actor.timer>0)
	for room in game.placed_rooms:
		if not room.has("leak_repair"): continue
		var job: Dictionary=room.leak_repair
		if actor.goal=="hull-repair" and actor.goal_cell!=room.pos: continue
		var worker: String=job.worker
		if not worker.is_empty():
			var assigned=Architects.actor_for(game,worker)
			if assigned.dead or not Architects.present(game,worker) or assigned.goal!="hull-repair":
				job.worker=""
		if not eligible or (not str(job.worker).is_empty() and job.worker!=id): continue
		if not str(job.get("preferred","")).is_empty() and job.preferred!=id: continue
		if not game.running or game.paused: return actor.goal=="hull-repair"
		if job.worker.is_empty():
			var found := approach(actor,room.pos)
			if found.is_empty():
				job.status="Path blocked / waiting for access"
				continue
			var travel := 0.0
			var from: Vector2=actor.foot
			for point in found.route:
				travel+=from.distance_to(point)/25.3
				from=point
			var drain := 0.008 if game.hardware.power and game.hardware.pumps and game.powered_room_cells.has(room.pos) and not room.get("suspended",false) else 0.0
			var needed := air_needed(room,job,travel,drain)
			if int(game.resources.oxygen)<=0: needed=travel+float(job.duration)-float(job.progress)+12
			var available: float=actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen
			if actor.needs_air() and needed>available:
				job.status="Unsafe air budget / helmet or refill needed"
				preload("res://scripts/flood_safety.gd").seek_locker(game,actor,id)
				continue
			job.worker=id
			job.point=found.point
			actor.path=found.route
			actor.stage=""
			actor.timer=0
			actor.goal="hull-repair"
			actor.goal_cell=room.pos
		if not actor.can_stand(job.point):
			job.worker=""
			release(actor)
			return true
		if actor.foot.distance_to(job.point)>1:
			actor.activity="heading to hull leak"
			job.status="Crew travelling"
			if actor.path.is_empty():
				var found := approach(actor,room.pos)
				if found.is_empty(): job.worker=""; release(actor); return true
				job.point=found.point
				actor.path=found.route
			actor.move(dt)
			return true
		actor.path.clear()
		job.status="Welding"
		actor.direction="north"
		actor.state="weld" if actor.movement_medium=="dry" and not actor.helmet_equipped else "repair"
		actor.activity="sealing hull / %d%%" % roundi(float(job.progress)/float(job.duration)*100)
		job.progress=minf(job.duration,float(job.progress)+dt)
		if job.progress>=job.duration:
			room.hull_crack=0.0
			room.erase("local_incident")
			room.erase("leak_repair")
			release(actor)
			actor.activity="hull sealed"
			game._log("Hull sealed at %s. Pumps must clear the remaining water." % room.pos,false)
			game._refresh_all()
		return true
	if actor.goal=="hull-repair": release(actor)
	return false

static func valid(job: Variant) -> bool:
	if not job is Dictionary: return false
	if not job.get("cost") is int or job.cost not in COSTS: return false
	if not job.get("worker") is String or job.worker not in ["","bill","veld","branforth","marsh"]: return false
	for key in ["duration","progress"]:
		if not (job.get(key) is float or job.get(key) is int) or not is_finite(float(job[key])): return false
	if job.get("preferred","") not in ["","bill","veld","branforth","marsh"]: return false
	if not job.get("status","") is String or str(job.get("status","")).length()>96: return false
	if (job.duration not in SECONDS and job.duration!=16.0) or job.progress<0 or job.progress>job.duration: return false
	if not job.worker.is_empty() and (not job.get("point") is Vector2 or not job.point.is_finite()): return false
	return true
