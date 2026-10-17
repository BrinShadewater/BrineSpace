extends RefCounted
const Motion=preload("res://scripts/james_construction_motion.gd")
static func target(work:float,duration:float,facing:String) -> Array:
	var key:String="torch-draw-"+facing;var elapsed:float=work
	if work>=duration-.52:key="torch-stow-"+facing;elapsed=work-(duration-.52)
	elif work>=.52:
		key="weld-"+facing
		var cycle:=0.0
		for milliseconds in Motion.timings()[key]:cycle+=float(milliseconds)/1000.0
		var budget:float=duration-1.04
		elapsed=fposmod((work-.52)/budget*maxi(1,roundi(budget/cycle))*cycle,cycle)
	var rows:Array=[]
	for i in range(Motion.timings()[key].size()):rows.append([key,i,Motion.timings()[key][i]])
	return [key,Motion.slot(rows,elapsed)]
static func sequence(key:String,index:int) -> Array:
	var rows:=Motion.exit_path(key,index);rows.reverse();return rows
static func equipment(actor) -> String:
	return "diving-helmet" if actor.helmet_equipped else ""
static func frames(game,actor) -> Dictionary:
	return game.grid_view.branforth_player.frames if equipment(actor).is_empty() else game.grid_view.branforth_player.equipment_frames.get(equipment(actor),{})
static func eligible(actor) -> bool:
	return actor.active and not actor.dead and actor.movement_medium=="dry" and actor.hull_resume.get("equipment","")==equipment(actor) and actor.goal in ["hull-repair","ward-repair"] and actor.goal==actor.hull_resume.get("goal","hull-repair") and actor.state in ["idle","weld"] and actor.stage.is_empty() and actor.path.is_empty() and actor.expedition.is_empty() and actor.locker_request.is_empty() and not actor.hull_resume.is_empty() and actor.foot==actor.hull_resume.foot and actor.direction==actor.hull_resume.direction and actor.can_stand(actor.foot)
static func sync(actor,job:Dictionary) -> void:
	if actor.goal=="ward-repair":actor.sync_ward_animation(float(job.progress))
	else:actor.sync_hull_animation(job)
static func active(actor) -> bool:
	return actor.ward_animation_active() if actor.goal=="ward-repair" else actor.hull_animation_active()
static func advance(game,actor,job:Dictionary,delta:float) -> bool:
	if not actor.hull_resume.is_empty():
		if not eligible(actor) or job.progress!=actor.hull_resume.work or job.duration!=actor.hull_resume.duration:
			actor.hull_resume.clear();return false
	else:
		if actor.timer!=0 or (actor.hull_animation_duration!=0 or actor.ward_animation_duration!=0) or job.progress<=0 or job.progress>=job.duration:return false
		sync(actor,job)
		if not active(actor):return false
		var key:String=actor.animation_state()+"-"+actor.direction
		var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
		var index:int=frames(game,actor).get(key,[]).find(source)
		var rows:=sequence(key,index)
		if rows.is_empty():return false
		actor.hull_resume={"equipment":equipment(actor),"goal":actor.goal,"source":key,"index":index,"sequence":rows,"elapsed":0.0,"foot":actor.foot,"direction":actor.direction,"work":float(job.progress),"duration":float(job.duration)}
		actor.state="idle";actor.activity="drawing repair torch"
		return true
	var motion:Dictionary=actor.hull_resume
	if not game.paused:motion.elapsed=minf(Motion.seconds(motion.sequence),float(motion.elapsed)+maxf(0,delta))
	actor.state="idle";actor.activity="drawing repair torch"
	if motion.elapsed>=Motion.seconds(motion.sequence):
		motion.clear();actor.state="weld";sync(actor,job)
	return true
static func texture(game,actor) -> Texture2D:
	var motion:Dictionary=actor.hull_resume
	var row:Array=motion.sequence[Motion.slot(motion.sequence,motion.elapsed)]
	game.grid_view.branforth_player.current_key=""
	return frames(game,actor)[row[0]][row[1]]
static func valid(data:Dictionary) -> bool:
	var motion:Variant=data.get("branforth_hull_resume",{})
	if not motion is Dictionary:return false
	if motion.is_empty():return true
	if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","")!="dry":return false
	if motion.get("equipment","")!=("diving-helmet" if data.get("helmet_equipped",false) else ""):return false
	if data.get("goal","") not in ["hull-repair","ward-repair"] or motion.get("goal","hull-repair")!=data.get("goal","") or data.get("state","")!="idle" or data.get("stage","")!="" or not data.get("path") is PackedVector2Array or not data.path.is_empty() or data.get("expedition",{})!={} or data.get("locker_request",{})!={}:return false
	if not motion.get("source") is String or not motion.get("index") is int:return false
	if motion.get("direction","") not in ["north","east","south","west"] or motion.direction!=data.get("direction","") or motion.source.get_slice("-",motion.source.get_slice_count("-")-1)!=motion.direction:return false
	var rows:=sequence(motion.source,motion.index)
	if rows.is_empty() or motion.get("sequence")!=rows:return false
	for field in ["elapsed","work","duration"]:
		if not (motion.get(field) is float or motion.get(field) is int) or not is_finite(float(motion[field])):return false
	if motion.elapsed<0 or motion.elapsed>=Motion.seconds(rows) or motion.work<=0 or motion.work>=motion.duration or motion.duration not in ([18.0] if data.goal=="ward-repair" else [3.0,6.0,10.0,14.0,16.0]) or motion.work!=data.get("timer"):return false
	if target(motion.work,motion.duration,motion.direction)!=[motion.source,motion.index]:return false
	return motion.get("foot") is Vector2 and motion.foot.is_finite() and motion.foot==data.get("foot")
