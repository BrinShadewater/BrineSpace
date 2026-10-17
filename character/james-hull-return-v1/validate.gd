extends "res://character/james-hull-lifecycle-v1/validate.gd"
const RESULT:="res://character/james-hull-return-v1/"
const Return=preload("res://scripts/james_hull_return.gd")
const Motion=preload("res://scripts/james_construction_motion.gd")
var return_cases:Array=[]
func observe(label:String,previous:String) -> String:
	var actor=game.branforth_npc;var player=game.grid_view.branforth_player
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var index:int=player.frames.get(key,[]).find(source)
	if Return.eligible(actor):
		var row:Array=actor.hull_return.sequence[Motion.slot(actor.hull_return.sequence,actor.hull_return.elapsed)];key=row[0];index=row[1]
	var token:String=key+"/"+str(index)
	if token==previous:return token
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:String=RESULT+"native/"+label+"-%04d.png"%records.size()
	check(root.get_texture().get_image().save_png(path)==OK,"Actual return native capture")
	records.append({"path":path,"label":label,"key":key,"index":index,"elapsed":actor.hull_return.get("elapsed",-1),"returning":Return.eligible(actor),"foot":[actor.foot.x,actor.foot.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text()})
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
		await start_scene("user://james-hull-return.loop")
		game.running=true;game.paused=false;game.Architects.advance_core(game,10)
		var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		for peer in game.companion_actors.values():peer.active=false
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		var core:=Vector2i(20,20);var room:Dictionary=game.occupied[core];room.hull_crack=.8;room.water_level=0.0;room.erase("leak_repair")
		check(Hull.request(game,core),"Actual paid cancellation job")
		await settle()
		for step in range(3000):
			game._process(1.0/60.0)
			if actor.hull_animation_active() and actor.timer>=threshold:break
		check(actor.hull_animation_active(),"Actual cancellation reaches work phase")
		var phase:String=actor.animation_state();var label:String=phase
		var before:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();var foot:Vector2=actor.foot
		await observe(label+"-working","")
		var job:Dictionary=room.leak_repair;var refund:int=int(floor(float(job.cost)*(1-float(job.progress)/float(job.duration))));var paid:float=game.resources.metal
		check(Hull.cancel(game,core),"Normal hull cancellation")
		check(game.resources.metal==paid+refund and not room.has("leak_repair"),"Original cancellation refund retained")
		check(Return.eligible(actor),"Cancelled work retracts before claiming another task")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before,"Cancellation first source exact")
		var previous:String=await observe(label+"-cancelled","");var saved:=false;var new_paid:float=-1
		for step in range(120):
			game._process(1.0/60.0);actor=game.branforth_npc;room=game.occupied[core]
			check(actor.foot==foot,"Retraction preserves physical contact")
			check(not Effects.torch_actors(game).has(actor),"Sparks stop during cancellation return")
			if room.has("leak_repair"):
				check(room.leak_repair.worker=="" and room.leak_repair.progress==0,"Legitimate replacement job waits while torch stows")
				if new_paid<0:new_paid=game.resources.metal
				check(game.resources.metal==new_paid,"Requeue paid once, no repeated cancellation charge")
			previous=await observe(label+"-return",previous)
			if Return.eligible(actor):
				check(Return.valid(actor.snapshot()) and actor.valid_branforth_snapshot(actor.snapshot()),"Actual return snapshot admissible")
				if not saved and actor.hull_return.elapsed>=.06:
					saved=true;await return_checkpoint(label);previous=""
			else:break
		check(saved and actor.hull_return.is_empty(),"Mid-return Continue finishes cancellation")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==game.grid_view.branforth_player.frames["torch-draw-north"][0].get_image().get_data(),"Exact neutral end source")
		game._process(1.0/60.0);actor=game.branforth_npc;room=game.occupied[core]
		var replacement:String="draw" if actor.hull_animation_active() else "air-budget-wait"
		if replacement=="draw":
			check(actor.goal=="hull-repair" and actor.animation_state()=="torch-draw" and actor.timer<=1.0/60.0,"Eligible fresh auto-queued work draws from entry")
		else:
			check(actor.goal.is_empty() and actor.state=="idle" and room.leak_repair.worker=="" and room.leak_repair.progress==0 and room.leak_repair.status=="Unsafe air budget / helmet or refill needed","Original air-budget safety keeps replacement unclaimed")
			check(not Effects.torch_actors(game).has(actor),"Air-budget wait has no torch effects")
		check(game.resources.metal==new_paid,"Resumption does not recharge pending job")
		await observe(label+"-new-job","")
		return_cases.append({"phase":phase,"savedReturn":saved,"refund":refund,"replacementMetal":new_paid,"entryExact":true,"neutralExact":true,"replacement":replacement,"replacementStatus":room.leak_repair.status})
		print("JAMES HULL RETURN CASE ",phase," saved=",saved)
	var file:=FileAccess.open(RESULT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":return_cases,"records":records,"scope":"Three actual paid North rupture repair cancellations during draw/held/stow; exact current source, whole-source return to neutral, paused real disk Continue in each return, fixed foot, original refund and once-paid auto-queued replacement held until stow completes then fresh draw when eligible, or original air-budget safety wait. Bare only; no reassignment/other-facing/critical hazard claim."},"  "));file.close()
	for path:String in [RESULT+"validate.gd","res://scripts/james_hull_return.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES HULL RETURN: ",checks," checks, ",failures," failures, ",records.size()," captures")
	game.queue_free();quit(1 if failures else 0)
