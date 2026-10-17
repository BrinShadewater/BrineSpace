extends SceneTree
const OUT := "res://character/james-meal-interrupt-north-v1/"
const Service=preload("res://scripts/airlock_service.gd")
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func capture(label:String,npc)->String:
	var screen:=Rect2();var visible:=false
	for attempt in range(120):
		var center:Vector2=npc.foot/384.0*game.get_cell_size()
		game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
		game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var world:=Rect2(npc.foot/384.0*game.get_cell_size()-Vector2.ONE*game.get_cell_size()*.45,Vector2.ONE*game.get_cell_size()*.9)
		screen=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
		var viewport:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
		if viewport.encloses(screen):visible=true;break
	check(visible,"Entire locker review region visibly inside station viewport")
	var screenshot:=root.get_texture().get_image()
	var image:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var path:String=OUT+"captures/"+label+".png"
	check(image.save_png(path)==OK,"Native locker capture")
	return path
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-locker.meta";game.run_save_path="user://james-locker.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	game.recovered_crew.append({"architect_id":"bill","alive":true,"id":"architect_bill","name":"Bill","origin":cell})
	var peer=game.bill_npc
	peer.decision_rng=RandomNumberGenerator.new()
	for phase in ["eat","drink"]:
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
		for offset in [Vector2i.ZERO,Vector2i.DOWN]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		peer.active=false;peer.rebuild(game);npc.rebuild(game);npc.meal_return.clear()
		for actor in [npc,peer]:
			actor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.avoidance_positions.clear();actor.avoidance_position=Vector2.INF;actor.path.clear();actor.goal="";actor.state="idle";actor.timer=0;actor.helmet_equipped=false;actor.movement_medium="dry";actor.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0}
		peer.active=false;npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2.DOWN*384,cell+Vector2i.DOWN));npc.direction="north";npc.needs.hunger=95;npc.decision_rng.seed=1;npc.choose_goal(game);game.resources.food=1000
		game.test_walker_cell=Vector2i(-1,-1)
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);var planned_contact:Vector2=center+Vector2(stations[0].point)
		peer.foot=planned_contact-Vector2(32,0);peer.direction="east";peer.needs.curiosity=95;peer.visits.clear();peer.avoidance_positions.clear();peer.avoidance_position=Vector2.INF
		var seed_used:=0
		for seed in range(1,129):
			peer.goal="";peer.path.clear();peer.timer=0;peer.decision_rng.seed=seed;peer.choose_goal(game)
			if peer.goal_cell==cell and not peer.path.is_empty() and peer.path[-1].distance_to(planned_contact)<1:seed_used=seed;break
		check(seed_used>0,"Peer normal chooser queues same contact before James occupies it")
		var reached:=false
		for tick in range(3000):
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
			var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
			if npc.animation_state()==phase and player.frames[phase+"-north"].find(texture)==3:reached=true;break
		check(reached,"Normal James meal reaches held gesture")
		game.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
		check(npc.meal_return_active(),"Genuine service-loss return starts")
		game.powered_room_cells[cell]=true
		var contact:Vector2=npc.foot;peer.active=true;peer.foot=contact-Vector2(32,0);peer.direction="east";peer.needs.curiosity=95
		check(peer.can_stand(peer.foot) and peer.foot.distance_to(contact)>=32,"Real peer starts on clear adjacent floor")
		check(not peer.path.is_empty() and peer.path[-1].distance_to(contact)<1,"Queued real peer service intent remains intact")
		var minimum:=32.0;var moved_while_return:=false;var unfinished_drop:=false;var max_wait:=0.0;var return_ticks:=0;var pictures:Array=[await capture("crowd-"+phase+"-start",npc)]
		while return_ticks<240 and npc.meal_return_active():
			var old:Vector2=npc.foot;var old_elapsed:float=npc.meal_return.elapsed;var duration:float=npc.meal_return_seconds(npc.meal_return.source,npc.meal_return.index)
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;return_ticks+=1
			minimum=minf(minimum,npc.foot.distance_to(peer.foot));max_wait=maxf(max_wait,peer.traffic_wait)
			if npc.foot!=old:moved_while_return=true
			if not npc.meal_return_active() and old_elapsed+1.0/120<duration-.0001:unfinished_drop=true
		check(not moved_while_return and not unfinished_drop,"Nearby traffic preserves complete stationary held-prop return")
		check(minimum>=32-.02,"Two real crew maintain clearance")
		var peer_service:=false;var follow_ticks:=0
		while follow_ticks<1200 and not peer_service:
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;follow_ticks+=1
			minimum=minf(minimum,npc.foot.distance_to(peer.foot));max_wait=maxf(max_wait,peer.traffic_wait)
			peer_service=peer.goal_cell==cell and peer.stage in ["life_eat","life_drink"]
		check(peer_service,"Queued peer reaches actual galley service after return gives way")
		check(minimum>=32-.02,"Follow-up passage keeps real crew clearance")
		pictures.append(await capture("crowd-"+phase+"-end",npc))
		results.append({"phase":phase,"seed":seed_used,"ticks":return_ticks,"peerService":peer_service,"peerFollowTicks":follow_ticks,"movedWhileReturning":moved_while_return,"unfinishedDrop":unfinished_drop,"minimumSeparation":minimum,"maxPeerWait":max_wait,"captures":pictures,"James":npc.snapshot(),"peer":peer.snapshot()})
		peer.active=false
	var file:=FileAccess.open(OUT+"native-crowd-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two normal James held-meal/cup interruptions with real Bill peer normal chooser targeting same contact during return. Actual shared updates/passage, fixed return and separation checked. Other gear/layouts and final peer service completion separate."},"  "));file.close()
	print("JAMES MEAL RETURN CROWD: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
