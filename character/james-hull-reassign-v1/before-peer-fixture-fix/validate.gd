extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-hull-reassign-v1/"
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
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(RESULT+"native")
	for threshold in [.2,3.0,13.8]:
		if game!=null:root.remove_child(game);game.queue_free();await process_frame
		await start_scene("user://james-hull-reassign.loop")
		game.running=true;game.paused=false;game.Architects.advance_core(game,10)
		var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
		# Prescribed recovered waiting peer, not a Bill service/animation proof.
		var peer:Dictionary=game.recovered_crew[0].duplicate(true)
		peer.id="architect_bill";peer.architect_id="bill";peer.name="Major Bill";peer.erase("thawed_at");peer.erase("thaw_foot")
		game.recovered_crew.append(peer);game.crew_count+=1
		for other in [game.bill_npc,game.veld_npc,game.marsh_npc]:other.active=false
		for other in game.companion_actors.values():other.active=false
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		var core:=Vector2i(20,20);var room:Dictionary=game.occupied[core];room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
		check(Hull.request(game,core),"Actual paid reassignment job");await settle()
		for step in range(3000):
			game._process(1.0/60.0)
			if actor.hull_animation_active() and actor.timer>=threshold:break
		check(actor.hull_animation_active(),"Actual work phase reached")
		var phase:String=actor.animation_state();var foot:Vector2=actor.foot;var paid:float=game.resources.metal
		var job:Dictionary=room.leak_repair;var work:float=job.progress
		var source:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
		var before:Dictionary=actor.snapshot();var order:Dictionary=job.duplicate(true)
		check(Hull.reassign(game,core,"branforth"),"Same worker accepted")
		check(actor.snapshot()==before and job==order,"Same-worker selection preserves exact live actor/order")
		await observe(phase+"-working","")
		check(Hull.reassign(game,core,"bill"),"Normal reassignment to prescribed waiting peer")
		check(Return.eligible(actor) and job.preferred=="bill" and job.worker=="","Reassignment retracts outgoing worker")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Outgoing first whole source exact")
		var previous:String=""
		for step in range(100):
			game._process(1.0/60.0)
			check(actor.foot==foot and job.progress==work and game.resources.metal==paid,"Outgoing pose preserves foot/paid work/charge")
			check(not Effects.torch_actors(game).has(actor),"Outgoing reassignment no sparks")
			previous=await observe(phase+"-outgoing",previous)
			if not Return.eligible(actor):break
		check(actor.hull_return.is_empty(),"Outgoing stow completes")
		check(Hull.reassign(game,core,"branforth"),"Assign partly completed work back to James")
		game._process(1.0/60.0)
		check(Resume.eligible(actor) and job.worker=="branforth" and job.progress==work,"Returning worker draws before progressing paid job")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==game.grid_view.branforth_player.frames["torch-draw-north"][0].get_image().get_data(),"Resume begins at exact neutral whole source")
		previous=await observe(phase+"-resume","");var saved:=false
		for step in range(100):
			game._process(1.0/60.0);actor=game.branforth_npc;room=game.occupied[core];job=room.leak_repair
			check(actor.foot==foot and job.progress==work and game.resources.metal==paid,"Entry keeps physical foot/paid progress/charge")
			previous=await observe(phase+"-resume",previous)
			if Resume.eligible(actor):
				check(not Effects.torch_actors(game).has(actor),"No sparks during resume entry")
				check(Resume.valid(actor.snapshot()) and actor.valid_branforth_snapshot(actor.snapshot()),"Resume snapshot valid")
				if not saved and actor.hull_resume.elapsed>=.06:
					saved=true;await return_checkpoint(phase);previous=""
			else:break
		check(saved and actor.hull_resume.is_empty() and actor.hull_animation_active(),"Saved resume entry finishes at original work phase")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==source,"Exact original paid-pose join")
		game._process(1.0/60.0)
		check(job.progress>work and game.resources.metal==paid,"Normal paid progress resumes without recharging")
		await observe(phase+"-resumed-work","")
		return_cases.append({"phase":phase,"paidProgress":work,"metal":paid,"freshContinue":saved})
		print("JAMES HULL REASSIGN CASE ",phase)
	var file:=FileAccess.open(RESULT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":return_cases,"records":records,"scope":"Three actual paid North draw/held/stow repairs: same-worker no-op, outgoing reassignment to prescribed recovered inactive Bill, James reclaims same paid work with whole-pose entry and three fresh disk Continues. Not incoming Bill claim/service animation, other facing, all interruptions or completion proof."},"  "));file.close()
	for path:String in [RESULT+"validate.gd","res://scripts/james_hull_resume.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL REASSIGN: ",checks," checks, ",failures," failures, ",records.size()," captures")
	game.queue_free();quit(1 if failures else 0)
