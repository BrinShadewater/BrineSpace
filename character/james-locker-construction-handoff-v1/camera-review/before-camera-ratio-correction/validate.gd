extends "res://character/james-construction-controller-v2/validate.gd"
const DEST := "res://character/james-locker-construction-handoff-v1/camera-review/"
const Service = preload("res://scripts/airlock_service.gd")
var serial:=0
var capture_paths:Dictionary={}
func capture(leg:String,actor,force:=false):
	var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var gear:String="diving-helmet" if actor.helmet_equipped and not actor.helmet_action_active() else ""
	var pool:Dictionary=game.grid_view.branforth_player.frames if gear.is_empty() else game.grid_view.branforth_player.equipment_frames[gear]
	var index:int=pool.get(key,[]).find(source)
	check(index>=0,"Exact selected source admitted "+key)
	if index<0:return
	var token:String=leg+":"+key+":"+str(index)
	if capture_paths.has(token) and not force:return
	var screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)
	var size:Vector2=root.get_texture().get_size()
	if screen.x<450 or screen.x>size.x-180 or screen.y<300 or screen.y>size.y-100:
		game._set_grid_zoom(1.2,true,actor.foot/384.0/80.0)
		for attempt in range(120):
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:break
	var path:String=DEST+"native/"+"%04d.png"%serial;serial+=1
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(path)==OK,"Native handoff capture")
	capture_paths[token]=path
	var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)
	records.append({"leg":leg,"key":key,"index":index,"gear":gear,"helmet":actor.helmet_equipped,"timer":actor.timer,"foot":[actor.foot.x,actor.foot.y],"footViewport":[foot_screen.x,foot_screen.y],"sourceHash":source.get_image().get_data().hex_encode().sha256_text(),"capture":path,"pivot":[source.get_meta("crew_pivot").x,source.get_meta("crew_pivot").y],"standingHeight":source.get_meta("crew_standing_height")})
func settle(cell:Vector2i):
	game.selected_card_id="";game.selected_room_cell=cell;game._refresh_all()
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	game._set_grid_zoom(1.2,true,(Vector2(cell)+Vector2(20,20)+Vector2.ONE)/80.0)
	for attempt in range(120):
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:return
	check(false,"Native camera settles")
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:String=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	DirAccess.make_dir_recursive_absolute(DEST+"native")
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-locker-construction.meta";game.run_save_path="user://james-locker-construction.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.running=true;game.paused=false;game.crew_comms.dismiss();game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	var actor=game.branforth_npc;check(actor.active,"Genuine James core release")
	var initial:Vector2=actor.foot;var core:=Vector2i(20,20);var air_cell:=core+Vector2i.DOWN;var core_room:Dictionary=game.occupied[core].duplicate(true)
	for side in range(4):
		var direction:String=["north","east","south","west"][side]
		air_cell=core+Construction.DIRS[(side+1)%4]
		var air:Dictionary=game.RoomDatabaseScript.get_room("airlock");air.pos=air_cell
		for rotation in range(4):
			air.rotation=rotation
			if game._ports_connect(air,core_room,air_cell,core):break
		check(game._ports_connect(air,core_room,air_cell,core),"Prescribed airlock fixture connects to core")
		game.placed_rooms.assign([core_room.duplicate(true),air]);game.occupied.clear();game.occupied[core]=game.placed_rooms[0];game.occupied[air_cell]=air
		game.drone_fleet.restore(null);game.drone_fleet.sites_initialized=true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;actor.construction_motion.clear();check(actor.set_helmet_equipped(false),"Initial bare setup only")
		game._apply_room_economy();await settle(air_cell)
		var locker:Dictionary=Service.locker(game,air_cell)
		check(Service.ready(game,air_cell) and not locker.is_empty(),"Actual powered airlock exposes locker")
		check(Service.request(game,"branforth",air_cell),"Actual service request routes James to real locker")
		if failures>0:print("JAMES LOCKER SETUP ",locker," foot=",actor.foot," rooms=",game.placed_rooms);quit(2);return
		var visited_fitting:=false;var fit_foot:=Vector2.INF;var fit_slots:Dictionary={};var travel:=0.0
		for step in range(4800):
			var old:Vector2=actor.foot;game._process(1.0/60.0);travel+=old.distance_to(actor.foot)
			check(actor.segment_clear(old,actor.foot) and old.distance_to(actor.foot)<1.01,"Locker approach has no teleport or obstruction")
			if actor.helmet_action_active():
				visited_fitting=true
				if not fit_foot.is_finite():fit_foot=actor.foot
				check(actor.foot==fit_foot and not actor.helmet_equipped and actor.direction=="east","Actual fitting keeps contact and grants helmet only at completion")
				var source:Texture2D=game.grid_view._get_branforth_frame_source(game);fit_slots[game.grid_view.branforth_player.frames["equip-helmet-east"].find(source)]=true
			await capture(direction+"-locker",actor)
			if visited_fitting and actor.helmet_equipped and not actor.helmet_action_active():break
		check(visited_fitting and actor.helmet_equipped and actor.locker_request.is_empty() and travel>80,"Real route and timed fitting complete")
		check(fit_slots.size()==game.grid_view.branforth_player.frames["equip-helmet-east"].size(),"Every selected fitting slot exercised")
		await capture(direction+"-equipped-join",actor,true)
		if failures>0:quit(2);return
		# Actual airlock is on a different adjacent port from this paid core job.
		var target:Vector2i=core+Construction.DIRS[side]
		game.wrecks.erase(target);game.drone_fleet.sites.erase(target);game.hand.assign(["life_support"]);game._on_card_pressed("life_support")
		for rotation in range(4):
			game.selected_rotation=rotation
			if game.get_placement_problem("life_support",target).is_empty():break
		var metal:float=game.resources.metal;game._on_grid_clicked(target)
		check(game.resources.metal<metal and game.drone_fleet.reserved(target),"Actual paid job queued after locker fitting")
		if failures>0:quit(2);return
		await settle(target)
		var phases:Dictionary={};var contact:=Vector2.INF
		for step in range(4800):
			game._process(1.0/60.0)
			check(actor.helmet_equipped,"Fitted equipment persists through actual construction")
			if actor.goal=="construction" and actor.state=="weld":
				if not contact.is_finite():contact=actor.foot
				check(actor.foot==contact and actor.direction==direction,"Fitted construction contact/facing exact")
				check(actor.valid_branforth_snapshot(actor.snapshot()),"Fitted construction snapshot admissible")
				phases[actor.animation_state()]=true
			await capture(direction+"-build",actor)
			if game.occupied.has(target):break
		check(game.occupied.has(target) and not game.drone_fleet.reserved(target),"Locker-fitted paid build completes")
		check(phases.has("torch-draw") and phases.has("weld") and phases.has("torch-stow"),"All fitted construction phases traversed")
		check(game.resources.metal==metal-5,"Original paid cost retained")
		check(actor.goal!="construction" and not Effects.torch_actors(game).has(actor),"Completed job releases tool effects")
		cases.append({"direction":direction,"locker":str(locker),"fittingSlots":fit_slots.size(),"lockerTravel":travel,"phases":phases.keys(),"completed":game.occupied.has(target)})
		print("JAMES LOCKER CONSTRUCTION CASE ",direction," completed=",game.occupied.has(target)," fittingSlots=",fit_slots.size())
		if failures>0:quit(2);return
	var f:=FileAccess.open(DEST+"evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"Four actual AirlockService requests to existing prescribed connected powered airlock fixture: ordinary routes/all fitting slots/equipped join/actual paid four-direction construction. Initial room/physical-foot reset and bare gear reset per case; no prescribed helmet grant. Distinct source slots captured once per journey leg, not every chronological visit. No disk Continue, removal, interrupted locker fitting, natural owner-layout or continuous native motion acceptance."},"  "))
	if not FileAccess.file_exists(get_script().resource_path+".uid"):
		var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES LOCKER CONSTRUCTION: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
