extends RefCounted
## Josh assists already paid hull/ward jobs; their architect retains ownership.
const BONUS := 0.25

static func target(game, josh) -> Dictionary:
	if not game.running or game.paused or game.hardware.doors:return {}
	# Without a welding architect no room can yield a hull target. Check four
	# actors before allocating/scanning station cells; do not cache mutable state.
	for worker in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
		if worker!=null and worker.active and not worker.dead and worker.goal=="hull-repair" and worker.state=="weld" and worker.expedition.is_empty():
			return _target_with_hull_worker(game,josh)
	return ward_target(game,josh)

static func _target_with_hull_worker(game,josh) -> Dictionary:
	var cells: Array=game.occupied.keys()
	if cells.has(josh.interest_cell):
		cells.erase(josh.interest_cell);cells.push_front(josh.interest_cell)
	for cell in cells:
		var room: Dictionary=game.occupied[cell]
		if float(room.get("water_level",0))>=0.5 or room.get("suspended",false):continue
		var job: Dictionary=room.get("leak_repair",{})
		if job.is_empty() or str(job.get("worker","")).is_empty() or not job.has("point"):continue
		var worker=game.Architects.actor_for(game,job.worker)
		if worker==null or not worker.active or worker.dead or worker.goal!="hull-repair" or worker.state!="weld":continue
		if not worker.expedition.is_empty() or worker.foot.distance_to(job.point)>2:continue
		if josh.foot.distance_to(job.point)>384:continue
		return {"cell":cell,"point":job.point}
	return ward_target(game,josh)

static func ward_target(game,josh) -> Dictionary:
	# Read transient assignment only; looking for work must not create/claim a job.
	var job: Dictionary=game.get_meta("ward_repair_job",{})
	if not job.has("cell") or not job.has("point") or str(job.get("worker","" )).is_empty():return {}
	var ward: Dictionary=game.wrecks.get(job.cell,{})
	if not ward.get("paid",false) or not ward.get("active",false) or ward.get("cleared",false):return {}
	var worker=game.Architects.actor_for(game,job.worker)
	if worker==null or not worker.active or worker.dead or worker.goal!="ward-repair" or worker.state!="weld":return {}
	if worker.movement_medium!="dry" or not worker.expedition.is_empty() or not worker.path.is_empty() or worker.foot.distance_to(job.point)>1:return {}
	# Load at call time: WardRepair -> Companions -> CompanionNPC already uses us.
	var site: Dictionary=load("res://scripts/ward_repair.gd").worksite(game,job.cell)
	if site.is_empty() or worker.cell_at(worker.foot)!=site.room or not worker.can_stand(worker.foot):return {}
	var room: Dictionary=game.occupied[site.room]
	if float(room.get("water_level",0))>=0.5 or float(room.get("fire",0))>0 or room.get("suspended",false):return {}
	if josh.foot.distance_to(job.point)>384:return {}
	return {"cell":site.room,"point":job.point,"kind":"ward","job_cell":job.cell}

static func multiplier(game,cell: Vector2i,kind: String="hull",job_cell: Vector2i=Vector2i(-1,-1)) -> float:
	var josh=game.companion_actors.get("josh")
	if josh==null or not josh.active or josh.dead or josh.behavior!="torch":return 1.0
	if josh.movement_medium!="dry" or not josh.can_stand(josh.foot):return 1.0
	if not game.running or game.paused or game.hardware.doors:return 1.0
	if josh.interest_cell!=cell or josh.cell_at(josh.foot)!=cell or not josh.path.is_empty():return 1.0
	var found:=target(game,josh)
	if found.is_empty() or found.cell!=cell or josh.foot.distance_to(found.point)>95:return 1.0
	if str(found.get("kind","hull"))!=kind or (kind=="ward" and found.get("job_cell")!=job_cell):return 1.0
	var enter: float=josh.poses.cycle_seconds("torch-enter-"+josh.direction)
	var leave: float=josh.poses.cycle_seconds("torch-exit-"+josh.direction)
	if josh.behavior_elapsed<enter or josh.behavior_elapsed>=josh.behavior_duration-leave:return 1.0
	return 1.0+BONUS
