extends RefCounted
const Motion=preload("res://scripts/james_construction_motion.gd")
const Resume=preload("res://scripts/james_hull_resume.gd")
static func eligible(actor) -> bool:
	return actor.active and not actor.dead and actor.movement_medium=="dry" and actor.hull_return.get("equipment","")==Resume.equipment(actor) and actor.goal.is_empty() and actor.state=="idle" and actor.stage.is_empty() and actor.path.is_empty() and actor.expedition.is_empty() and actor.locker_request.is_empty() and not actor.hull_return.is_empty() and actor.foot==actor.hull_return.foot and actor.direction==actor.hull_return.direction and actor.can_stand(actor.foot)
static func prepare(game,actor) -> void:
	var resuming:bool=preload("res://scripts/james_hull_resume.gd").eligible(actor)
	if (not actor.hull_animation_active() and not actor.ward_animation_active() and not resuming) or not actor.can_stand(actor.foot):return
	var key:String=actor.animation_state()+"-"+actor.direction
	if resuming:key=actor.hull_resume.sequence[Motion.slot(actor.hull_resume.sequence,actor.hull_resume.elapsed)][0]
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var index:int=Resume.frames(game,actor).get(key,[]).find(source)
	var sequence:=Motion.exit_path(key,index)
	if sequence.is_empty():return
	actor.hull_return={"equipment":Resume.equipment(actor),"source":key,"index":index,"sequence":sequence,"elapsed":0.0,"foot":actor.foot,"direction":actor.direction}
static func advance(game,actor,delta:float) -> bool:
	if not eligible(actor):actor.hull_return.clear();return false
	if game.paused:return true
	var returning:Dictionary=actor.hull_return
	returning.elapsed=minf(Motion.seconds(returning.sequence),float(returning.elapsed)+maxf(0,delta))
	actor.activity="putting away repair torch"
	if returning.elapsed>=Motion.seconds(returning.sequence):returning.clear()
	return true
static func texture(game,actor) -> Texture2D:
	var returning:Dictionary=actor.hull_return
	var row:Array=returning.sequence[Motion.slot(returning.sequence,returning.elapsed)]
	game.grid_view.branforth_player.current_key=""
	return Resume.frames(game,actor)[row[0]][row[1]]
static func valid(data:Dictionary) -> bool:
	var returning:Variant=data.get("branforth_hull_return",{})
	if not returning is Dictionary:return false
	if returning.is_empty():return true
	if not data.get("active",false) or data.get("dead",false) or data.get("movement_medium","")!="dry":return false
	if returning.get("equipment","")!=("diving-helmet" if data.get("helmet_equipped",false) else ""):return false
	if data.get("goal","")!="" or data.get("state","")!="idle" or data.get("stage","")!="" or not data.get("path") is PackedVector2Array or not data.path.is_empty() or data.get("timer")!=.5:return false
	if data.get("expedition",{})!={} or data.get("locker_request",{})!={}:return false
	if not returning.get("source") is String or not returning.get("index") is int:return false
	var key:String=returning.source
	if returning.get("direction","") not in ["north","east","south","west"] or returning.direction!=data.get("direction","") or key.get_slice("-",key.get_slice_count("-")-1)!=returning.direction:return false
	var sequence:=Motion.exit_path(key,returning.index)
	if sequence.is_empty() or returning.get("sequence")!=sequence:return false
	if not (returning.get("elapsed") is float or returning.get("elapsed") is int) or not is_finite(float(returning.elapsed)) or returning.elapsed<0 or returning.elapsed>=Motion.seconds(sequence):return false
	return returning.get("foot") is Vector2 and returning.foot.is_finite() and returning.foot==data.get("foot")
