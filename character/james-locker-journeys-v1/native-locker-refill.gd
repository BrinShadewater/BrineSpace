extends SceneTree
const OUT := "res://character/james-locker-journeys-v1/"
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
	var path:String=OUT+"refill-captures/"+label+".png"
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
	DirAccess.make_dir_recursive_absolute(OUT+"refill-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for offset in [Vector2i.ZERO,inside]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("airlock" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(inside)*384,cell+inside));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=true;npc.movement_medium="dry"
		npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};npc.tank_oxygen=0;npc.breath_oxygen=15;npc.starvation=0
		player.motion.clear();player.current_key="";player.last_time=-1;game.visual_time_seconds=100
		var target:Dictionary=Service.locker(game,cell);check(not target.is_empty(),"Actual locker discovered")
		check(Service.request(game,"branforth",cell,true),"Actual refill request accepted")
		var ticks:=0;var started:=false;var contact:=Vector2.INF;var arrival_oxygen:=0.0
		while ticks<8000 and not started:
			var before:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
			check(npc.can_stand(npc.foot) and npc.segment_clear(before,npc.foot),"Actual refill approach clear")
			if npc.activity=="refilling oxygen tank":started=true;contact=npc.foot;arrival_oxygen=npc.tank_oxygen
		check(started and npc.direction=="east" and contact.distance_to(target.interaction_point)<.1,"Refill arrives at selected east contact")
		var reservation:bool=Service.busy(game,cell,game.bill_npc)
		check(reservation,"Actual refill holds locker reservation for another actor")
		check(not Service.request(game,"branforth",cell,true) and not Service.request(game,"branforth",cell),"Repeated refill and helmet-change requests refused during hold")
		var elapsed:=0.0;var restored:=false;var captures:Array=[]
		while npc.activity=="refilling oxygen tank" and elapsed<6:
			var before_oxygen:float=npc.tank_oxygen;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;elapsed+=1.0/120
			if npc.activity!="refilling oxygen tank":break
			check(npc.foot==contact and npc.helmet_equipped and npc.movement_medium=="dry","Refill keeps registered contact and fitted gear")
			check(npc.tank_oxygen>=before_oxygen and npc.tank_oxygen<=60,"Normal vitals refill monotonically")
			check(player.equipment_frames["diving-helmet"]["idle-east"].has(game.grid_view._get_branforth_frame_source(game)),"Selected matte east idle cycle throughout current refill")
			if not restored and elapsed>=2.5:
				captures.append(await capture("q%d-refill-held"%q,npc))
				game.paused=true;var before_actor:Dictionary=npc.snapshot();var clock:float=game.visual_time_seconds;var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-refill.loop"
				check(save.problem(save.capture(game)).is_empty(),"Refill checkpoint valid")
				check(save.write(game,scratch_path)==OK,"Actual refill disk write")
				check(await save.restore_staged(game,save.read(scratch_path)),"Actual refill disk Continue")
				game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==before_actor and game.paused and game.visual_time_seconds==clock,"Refill Continue keeps full actor and clock")
				check(Service.busy(game,cell,game.bill_npc) and not Service.request(game,"branforth",cell,true),"Continue retains refill reservation and rejects duplicate request")
				game._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused refill does not advance")
				game.set_process(false);game.paused=false;restored=true
		check(restored and npc.tank_oxygen>=59.9 and npc.activity!="refilling oxygen tank","Refill completes full tank and leaves finite hold")
		check(not Service.busy(game,cell,game.bill_npc),"Completed refill releases reservation")
		npc.path.clear();npc.goal="";npc.stage="";npc.state="idle";npc.timer=0;npc.foot=contact;npc.tank_oxygen=20
		check(Service.request(game,"branforth",cell,true),"New refill accepted after completion")
		game._update_test_walker(1.0/120)
		check(Service.refilling(npc),"Contact refill begins normally")
		game.powered_room_cells.erase(cell);Service.check_service(game,npc)
		var offline_oxygen:float=npc.tank_oxygen
		check(not Service.refilling(npc) and not Service.busy(game,cell,game.bill_npc),"Offline service ends hold and releases reservation")
		game._update_test_walker(1.0/120)
		check(npc.tank_oxygen==offline_oxygen and not Service.request(game,"branforth",cell,true),"Offline refill grants no oxygen and refuses restart")
		results.append({"rotation":q,"reservationDuringHold":reservation,"arrivalOxygen":arrival_oxygen,"refillElapsed":elapsed,"restored":restored,"captures":captures})
	var file:=FileAccess.open(OUT+"native-locker-refill-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Four actual standard rotated airlock refill routes with equipped James, normal vitals and five-second idle hold, four actual disk Continue restores, pause and selected equipped idle-cycle pixels. Reservation, duplicate request rejection, post-completion release and power-loss/no-credit checks. No new refill animation authored; crowd body journeys/exterior return not exercised."},"  "));file.close()
	print("JAMES LOCKER REFILL: ",checks," checks; ",failures," failures; ",results.size()," actual refill journeys")
	quit(1 if failures else 0)
