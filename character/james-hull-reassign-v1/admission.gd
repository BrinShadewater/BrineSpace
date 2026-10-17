extends "res://character/james-hull-reassign-v1/validate.gd"
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-resume-admission.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;var samples:=0
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
	var file:=FileAccess.open(RESULT+"admission-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"samples":samples,"scope":"Prescribed source-clock/recipe/snapshot comparisons in native main scene: four bare facings x five duration budgets x nine entry/held/stow seam samples. No other-facing physical job/Continue/visual acceptance proof."},"  "));file.close()
	if not FileAccess.file_exists(RESULT+"admission.gd.uid"):
		var uid:=FileAccess.open(RESULT+"admission.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL REASSIGN ADMISSION: ",checks," checks, ",failures," failures, ",samples," samples")
	game.queue_free();quit(1 if failures else 0)
