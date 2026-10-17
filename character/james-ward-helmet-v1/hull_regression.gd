extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-ward-helmet-v1/"
const Return=preload("res://scripts/james_hull_return.gd")
const Motion=preload("res://scripts/james_construction_motion.gd")
const Resume=preload("res://scripts/james_hull_resume.gd")
var return_cases:Array=[]
func observe(label:String,previous:String) -> String:
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var index:int=player.frames.get(key,[]).find(source)
	if Return.eligible(actor):
		var row:Array=actor.hull_return.sequence[Motion.slot(actor.hull_return.sequence,actor.hull_return.elapsed)];key=row[0];index=row[1]
	if Resume.eligible(actor):
		var row:Array=actor.hull_resume.sequence[Motion.slot(actor.hull_resume.sequence,actor.hull_resume.elapsed)];key=row[0];index=row[1]
	var token:String=key+"/"+str(index)
	if token==previous:return token
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:String=RESULT+"native/"+label+"-%04d.png"%records.size()
	check(root.get_texture().get_image().save_png(path)==OK,"Actual return native capture")
	records.append({"path":path,"label":label,"key":key,"index":index,"elapsed":actor.hull_return.get("elapsed",-1),"returning":Return.eligible(actor),"resuming":Resume.eligible(actor),"foot":[actor.foot.x,actor.foot.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text()})
	return token
func return_checkpoint(label:String):
	game.paused=true;await observe(label+"-before","")
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var before:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot();var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
	var room:Dictionary=game.occupied[Vector2i(20,20)].duplicate(true);var metal:float=game.resources.metal;var clock:float=game.visual_time_seconds
	var path:String="user://james-hull-return-"+label+".loop";var data:Dictionary=Save.capture(game);var problem:String=Save.problem(data)
	check(problem.is_empty(),"Actual cancelled repair checkpoint valid: "+problem)
	if not problem.is_empty():quit(2);return
	check(Save.write(game,path)==OK,"Cancelled repair checkpoint writes")
	data=Save.read(path);check(not data.is_empty(),"Cancelled repair disk checkpoint reads")
	root.remove_child(game);game.queue_free();await process_frame
	await start_scene(path);check(await Save.restore_staged(game,data),"Cancelled repair fresh Continue restores")
	game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.dismiss();game.crew_comms.set_process(false)
	actor=game.branforth_npc;player=game.grid_view.branforth_player
	check(actor.snapshot()==before and player.snapshot()==playback,"Cancelled repair actor/player exact")
	check(game.occupied[Vector2i(20,20)]==room and game.resources.metal==metal,"Cancelled/refunded/requeued room exact")
	check(game.visual_time_seconds==clock and game.paused,"Cancelled repair paused clock exact")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Cancelled repair source RGBA exact")
	game._process(.5);check(actor.snapshot()==before and game.visual_time_seconds==clock,"Paused return does not advance")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused cancelled source exact")
	await settle();await observe(label+"-after","");game.paused=false
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-resume-admission.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;var samples:=0
	var admission_cases:Array=[]
	for facing in ["north","east","south","west"]:
		var data:Dictionary=actor.snapshot();data.direction=facing;data.helmet_equipped=true;data.state="weld";data.goal="ward-repair";data.stage="";data.path=PackedVector2Array();data.timer=3.0
		check(actor.valid_branforth_snapshot(data),"James helmet ward admitted")
		check(not preload("res://scripts/bill_npc.gd").valid_snapshot(data),"Default shared helmet-weld rejection retained")
		for other_goal in ["construction","hull-repair"]:
			var wrong:Dictionary=data.duplicate(true);wrong.goal=other_goal;check(not actor.valid_branforth_snapshot(wrong),"Helmet ward admission does not admit other repair families")
		var wet:Dictionary=data.duplicate(true);wet.movement_medium="flooded";check(not actor.valid_branforth_snapshot(wet),"Ward helmet admission does not admit flooded welding")
		admission_cases.append({"direction":facing,"helmetWardAdmitted":true,"defaultSharedRejected":true,"otherFamiliesAndWetRejected":true})
	actor.goal="hull-repair";actor.stage="";actor.path.clear();actor.movement_medium="dry";actor.helmet_equipped=false
	for facing in ["north","east","south","west"]:
		actor.direction=facing
		for duration in [3.0,6.0,10.0,14.0,16.0]:
			for work in [.017,.2,.519,.52,duration*.5,duration-.521,duration-.52,duration-.2,duration-.017]:
				actor.hull_resume.clear();actor.state="weld";actor.sync_hull_animation({"duration":duration,"progress":work})
				var target:Array=Resume.target(work,duration,facing)
				var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
				check(game.grid_view.branforth_player.frames[target[0]][target[1]].get_image().get_data()==pixels,"Paid target matches ordinary normal source clock")
				actor.hull_resume={"source":target[0],"index":target[1],"sequence":Resume.sequence(target[0],target[1]),"elapsed":0.0,"foot":actor.foot,"direction":facing,"work":work,"duration":duration};actor.state="idle"
				check(Resume.valid(actor.snapshot()) and actor.valid_branforth_snapshot(actor.snapshot()),"Supported clock target snapshot admitted")
				check(Resume.texture(game,actor).get_image().get_data()==game.grid_view.branforth_player.frames["torch-draw-"+facing][0].get_image().get_data(),"Whole-source entry begins neutral")
				actor.hull_resume.elapsed=Motion.seconds(actor.hull_resume.sequence)-.0001
				check(Resume.texture(game,actor).get_image().get_data()==pixels,"Whole-source entry ends at exact paid target")
				samples+=1
	var file:=FileAccess.open(RESULT+"hull-regression-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"helmetWardAdmissionCases":admission_cases,"scope":"720 prescribed bare hull source-clock/recipe/legacy snapshot comparisons: four facings x five duration budgets x nine seams. Twenty separate family/admission checks preserve default shared rejection while admitting dry helmet James ward, rejecting other repair families and flooded welding. No full physical hull job/Continue/visual acceptance proof."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"hull_regression.gd.uid"):
		var uid:=FileAccess.open(RESULT+"hull_regression.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL REASSIGN ADMISSION: ",checks," checks, ",failures," failures, ",samples," samples")
	game.queue_free();quit(1 if failures else 0)
