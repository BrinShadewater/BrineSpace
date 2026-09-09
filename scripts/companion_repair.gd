extends RefCounted
## Josh assists an already paid hull job; its architect retains ownership.
const BONUS := 0.25

static func target(game, josh) -> Dictionary:
	if not game.running or game.paused or game.hardware.doors:return {}
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
	return {}

static func multiplier(game,cell: Vector2i) -> float:
	var josh=game.companion_actors.get("josh")
	if josh==null or not josh.active or josh.dead or josh.behavior!="torch":return 1.0
	if josh.movement_medium!="dry" or not josh.can_stand(josh.foot):return 1.0
	if not game.running or game.paused or game.hardware.doors:return 1.0
	if josh.interest_cell!=cell or josh.cell_at(josh.foot)!=cell or not josh.path.is_empty():return 1.0
	var found:=target(game,josh)
	if found.is_empty() or found.cell!=cell or josh.foot.distance_to(found.point)>95:return 1.0
	var enter: float=josh.poses.cycle_seconds("torch-enter-"+josh.direction)
	var leave: float=josh.poses.cycle_seconds("torch-exit-"+josh.direction)
	if josh.behavior_elapsed<enter or josh.behavior_elapsed>=josh.behavior_duration-leave:return 1.0
	return 1.0+BONUS
