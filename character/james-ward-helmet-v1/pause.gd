extends "res://character/james-ward-helmet-v1/north.gd"
const Return=preload("res://scripts/james_hull_return.gd")
const Resume=preload("res://scripts/james_hull_resume.gd")
const Motion=preload("res://scripts/james_construction_motion.gd")
func capture(label:String):
	var actor=game.branforth_npc;var source:Texture2D=game.grid_view._get_branforth_frame_source(game);var key:String=actor.animation_state()+"-"+actor.direction;var index:int=game.grid_view.branforth_player.equipment_frames["diving-helmet"][key].find(source)
	for motion in [actor.hull_return,actor.hull_resume]:
		if not motion.is_empty():
			var row:Array=motion.sequence[Motion.slot(motion.sequence,motion.elapsed)];key=row[0];index=row[1]
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:String=OUT+"pause-native/"+label+"-%04d.png"%records.size();check(root.get_texture().get_image().save_png(path)==OK,"Ward paused-work native capture")
	var foot_view:Vector2=root.get_stretch_transform()*(game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0))
	records.append({"helmet":actor.helmet_equipped,"footViewport":[foot_view.x,foot_view.y],"path":path,"label":label,"key":key,"index":index,"work":game.wrecks[Vector2i(19,18)].progress,"foot":[actor.foot.x,actor.foot.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"returning":Return.eligible(actor),"resuming":Resume.eligible(actor)})
func run():
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(OUT+"pause-native")
	await setup_job();var cell:=Vector2i(19,18);var actor=game.branforth_npc
	for step in range(7000):
		game._process(1.0/60.0)
		if actor.ward_animation_active() and actor.timer>=3:break
	check(actor.ward_animation_active(),"Actual held ward repair reached")
	var work:float=game.wrecks[cell].progress;var foot:Vector2=actor.foot;var original:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();await capture("working")
	game._toggle_wreck_work(cell);game._process(1.0/60.0)
	check(Return.eligible(actor) and actor.ward_animation_duration==0,"Pausing paid ward retracts tool")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==original,"Ward pause retains exact first whole source")
	var saved:=false;var previous:String=""
	for step in range(100):
		game._process(1.0/60.0);actor=game.branforth_npc
		check(actor.foot==foot and game.wrecks[cell].progress==work and game.resources.metal==92,"Pause return preserves foot/paid progress/charge")
		check(not Effects.torch_actors(game).has(actor),"No paused-return torch effects")
		var pixels:String=game.grid_view._get_branforth_frame_source(game).get_image().get_data().hex_encode().sha256_text()
		if pixels!=previous:await capture("return");previous=pixels
		if Return.eligible(actor):
			var bad_gear:Dictionary=actor.snapshot();bad_gear.branforth_hull_return.equipment="";check(not Return.valid(bad_gear),"Reject wrong return equipment")
			check(Return.valid(actor.snapshot()),"Paused ward return snapshot valid")
			if not saved and actor.hull_return.elapsed>=.06:saved=true;await checkpoint("ward-return");previous=""
		else:break
	check(saved and actor.hull_return.is_empty(),"Saved ward return reaches neutral")
	game._toggle_wreck_work(cell);game._process(1.0/60.0);actor=game.branforth_npc
	check(Resume.eligible(actor) and actor.hull_resume.goal=="ward-repair" and game.resources.metal==92,"Ward resume draws without recharging")
	saved=false;previous=""
	for step in range(100):
		game._process(1.0/60.0);actor=game.branforth_npc
		check(actor.foot==foot and game.wrecks[cell].progress==work and game.resources.metal==92,"Resume entry preserves foot/paid progress/charge")
		var pixels:String=game.grid_view._get_branforth_frame_source(game).get_image().get_data().hex_encode().sha256_text()
		if pixels!=previous:await capture("resume");previous=pixels
		if Resume.eligible(actor):
			check(Resume.valid(actor.snapshot()) and not Effects.torch_actors(game).has(actor),"Ward resume snapshot/effects valid")
			var wrong_gear:Dictionary=actor.snapshot();wrong_gear.branforth_hull_resume.equipment="";check(not Resume.valid(wrong_gear),"Reject wrong resume equipment")
			var bad:Dictionary=actor.snapshot();bad.branforth_hull_resume.goal="hull-repair";check(not Resume.valid(bad),"Reject wrong saved paid-work family")
			if not saved and actor.hull_resume.elapsed>=.06:saved=true;await checkpoint("ward-resume");previous=""
		else:break
	check(saved and actor.hull_resume.is_empty() and actor.ward_animation_active(),"Saved ward resume returns to paid work")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==original,"Ward resume joins exact original paid pose")
	game._process(1.0/60.0);check(game.wrecks[cell].progress>work and game.resources.metal==92,"Normal ward work resumes with paid progress retained")
	# Death must supersede the new work presentation immediately.
	actor.die();check(not actor.ward_animation_active(),"Death disables ward presentation immediately")
	check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()!=original,"Death renderer does not retain ward torch")
	game._process(1.0/60.0);check(not Effects.torch_actors(game).has(actor),"Death has no stale ward sparks")
	var file:=FileAccess.open(OUT+"pause-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"paidProgress":work,"records":records,"checkpoints":checkpoints,"scope":"Actual paid North held ward paused/resumed through normal UI toggle; exact current source return/neutral/paid re-entry, two paused real disk fresh Continues, fixed foot/paid progress/cost, wrong-family rejection and immediate death. No other-facing/critical flood/power/door interruption claim."},"  "));file.close()
	if not FileAccess.file_exists("res://character/james-ward-helmet-v1/pause.gd.uid"):
		var uid:=FileAccess.open("res://character/james-ward-helmet-v1/pause.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid.close()
	print("JAMES WARD HELMET PAUSE: ",checks," checks, ",failures," failures, ",records.size()," captures");game.queue_free();quit(1 if failures else 0)
