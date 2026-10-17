extends "res://character/james-construction-controller-v2/validate.gd"
const RESULT := "res://character/james-construction-interrupt-v1/"
const Save = preload("res://scripts/run_save.gd")
func start_scene(path: String):
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-construction-continue.meta";game.run_save_path=path
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
func settle(target: Vector2i):
	game.selected_card_id="";game.selected_room_cell=target;game._refresh_all();game._set_grid_zoom(1.2,true,(Vector2(target)+Vector2(20,20)+Vector2.ONE)/80.0)
	for attempt in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:return
	check(false,"Fresh scene camera settles")
func capture(label: String, actor):
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var path:=RESULT+"continue-native/"+label+".png"
	check(root.get_texture().get_image().save_png(path)==OK,"Fresh Continue native capture")
	var key:String=actor.animation_state()+"-"+actor.direction
	records.append({"label":label,"capture":path,"key":key,"index":game.grid_view.branforth_player.frames.get(key,[]).find(source),"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text()})
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	await start_scene("user://james-construction-continue.loop")
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.branforth_npc.active,"Genuine James core release")
	var initial:Vector2=game.branforth_npc.foot;var core:=Vector2i(20,20);var core_room:Dictionary=game.occupied[core].duplicate(true)
	DirAccess.make_dir_recursive_absolute(RESULT+"continue-native")
	for side in range(3):
		var direction:String=["north","east","south"][side];var threshold:float=[.23,2.75,9.71][side]
		game.placed_rooms.assign([core_room.duplicate(true)]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0];game.drone_fleet.restore(null);game.drone_fleet.sites_initialized=true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100;game.paused=false
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		var actor=game.branforth_npc;actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;actor.helmet_equipped=false
		var target:Vector2i=core+Construction.DIRS[side];game.wrecks.erase(target);game.drone_fleet.sites.erase(target)
		game.hand.assign(["life_support"]);game._on_card_pressed("life_support")
		for rotation in range(4):
			game.selected_rotation=rotation
			if game.get_placement_problem("life_support",target).is_empty():break
		game._on_grid_clicked(target);check(game.drone_fleet.reserved(target),"Actual paid Continue job")
		await settle(target)
		for step in range(2400):
			game._process(1.0/60.0);game.grid_view._get_branforth_frame_source(game)
			if actor.goal=="construction" and actor.state=="weld" and actor.timer>=threshold:break
		check(actor.goal=="construction" and actor.state=="weld","Actual checkpoint reaches phase")
		game.paused=true;var phase:String=actor.animation_state();var label:String=direction+"-"+phase
		await capture(label+"-before",actor)
		var before_actor:Dictionary=actor.snapshot();var player=game.grid_view.branforth_player;var before_playback:Dictionary=player.snapshot()
		var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();var clock:float=game.visual_time_seconds
		var fleet:Dictionary=game.drone_fleet.snapshot();var metal:float=game.resources.metal;var path:String="user://james-construction-case%d.loop"%side
		var data:Dictionary=Save.capture(game);var problem:String=Save.problem(data)
		check(problem.is_empty(),"Actual construction checkpoint valid: "+problem)
		if not problem.is_empty():quit(2);return
		check(Save.write(game,path)==OK,"Actual construction checkpoint writes")
		data=Save.read(path);check(not data.is_empty(),"Actual disk checkpoint reads")
		root.remove_child(game);game.queue_free();await process_frame
		await start_scene(path)
		check(await Save.restore_staged(game,data),"Actual disk checkpoint restores into fresh main scene")
		game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
		actor=game.branforth_npc;player=game.grid_view.branforth_player
		check(actor.snapshot()==before_actor,"Fresh Continue actor exact")
		check(player.snapshot()==before_playback,"Fresh Continue playback exact")
		check(game.visual_time_seconds==clock and game.paused,"Fresh Continue visual clock and pause exact")
		check(game.drone_fleet.snapshot()==fleet and game.resources.metal==metal,"Fresh Continue paid work and metal exact")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Fresh Continue source RGBA exact")
		game._process(.5)
		check(actor.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused Continue actor and clock do not advance")
		check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused Continue source exact")
		await settle(target);await capture(label+"-after",actor)
		game.paused=false;var previous:=-1;var captures:=0;var foot:Vector2=actor.foot
		for step in range(700):
			game._process(1.0/60.0)
			var source:Texture2D=game.grid_view._get_branforth_frame_source(game);var token:int=hash(source.get_image().get_data())
			if captures<5 and token!=previous:
				await capture(label+"-resumed"+str(captures),actor);captures+=1
			previous=token
			if actor.goal=="construction":check(actor.foot==foot,"Resumed work stays at original contact")
			if game.occupied.has(target):break
		check(game.occupied.has(target) and not game.drone_fleet.reserved(target),"Fresh Continue finishes paid job")
		check(game.resources.metal==metal,"Fresh Continue does not charge again")
		var count:int=game.placed_rooms.size()
		for step in range(30):game._process(1.0/60.0)
		check(game.placed_rooms.size()==count,"Completed room not replayed")
		cases.append({"direction":direction,"phase":phase,"sourceExact":true,"completed":game.occupied.has(target),"captures":captures+2})
		print("JAMES CONSTRUCTION CONTINUE CASE ",label," completed=",game.occupied.has(target))
	var report:=FileAccess.open(RESULT+"continue-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"Three actual disk checkpoints into fresh main scenes: North partial draw, East held weld, South partial stow. Exact actor/playback/source/clock/pause/paid order, normal60Hz update to paid completion. Bare only. Not all facing-phase combinations or interrupted transition checkpoints."},"  "))
	if not FileAccess.file_exists(RESULT+"continue.gd.uid"):
		var uid:=FileAccess.open(RESULT+"continue.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CONSTRUCTION CONTINUE: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
