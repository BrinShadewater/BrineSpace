extends SceneTree
const OUT := "res://character/james-meal-service-south-open-v1/"
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
	var path:String=OUT+"contact-captures/"+label+".png"
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
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[64.0,126.0]}};store.revision+=1;store.geometry_revision+=1;store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"contact-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	for phase in ["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]:
		for hazard in ["moved-counter","removed-room","replaced-room","helmet","displaced-foot"]:
			print("HAZARD SETUP ",phase,"/",hazard," prior running=",game.running," paused=",game.paused," crew=",game.crew_count)
			game.running=true;game.paused=false;game.crew_count=1;game.summary_layer.visible=false
			store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[64.0,126.0]}};store.revision+=1;store.geometry_revision+=1
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			for member in game.recovered_crew:
				if member.get("architect_id","")=="branforth":member.alive=true
			for offset in [Vector2i.ZERO,Vector2i.DOWN]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=0;room.water_level=0;room.fire=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			npc.fire_cells.clear();npc.foot=center+Vector2(-32,-48);npc.dead=false;npc.movement_medium="dry";npc.rebuild(game);npc.meal_return.clear();npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
			npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(-32,-48),cell));npc.direction="south";npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.breath_oxygen=15;npc.starvation=0;npc.visits.clear();npc.decision_rng.seed=1
			game.resources.food=1000;game.resources.oxygen=1000;game.resources.water=0;game.hardware.pumps=false;game.hardware.doors=false
			npc.set_meta("flood_safety_wait",0.0);npc.set_meta("flood_retreat_check",0.0);npc.set_meta("flood_blocked_warning",false);npc.choose_goal(game)
			var reached:=false
			for tick in range(3000):
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				if npc.animation_state()==phase and player.frames[phase+"-south"].find(texture)==4:reached=true;break
			check(reached,"Normal meal reaches held pose before genuine hazard")
			game.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;check(npc.meal_return_active(),"Normal power-loss return begins")
			game.powered_room_cells[cell]=true
			for tick in range(24):game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
			check(npc.meal_return_active(),"Hazard interrupts unfinished return")
			var saved:Dictionary=npc.snapshot();var hunger:float=npc.needs.hunger
			check(npc.valid_branforth_snapshot(saved),"Actual current South return snapshot valid")
			check(not npc.can_step_aside(),"Physical crowd policy holds active return contact")
			if hazard=="moved-counter":
				store.data["room-galley/0"]["library/sp-generated-counter-galley-prep"]=[80.0,126.0];store.revision+=1;store.geometry_revision+=1
				npc.rebuild(game)
			elif hazard=="removed-room":
				game.occupied.erase(cell);game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=cell);npc.rebuild(game)
			elif hazard=="replaced-room":
				var replacement:Dictionary=game.RoomDatabaseScript.get_room("storage_bay").duplicate(true)
				replacement.pos=cell;replacement.rotation=0;replacement.water_level=0;replacement.fire=0
				game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=cell);game.placed_rooms.append(replacement);game.occupied[cell]=replacement;npc.rebuild(game)
			elif hazard=="helmet":npc.helmet_equipped=true
			else:
				npc.foot+=Vector2(-16,0)
				check(npc.can_stand(npc.foot),"Controlled displaced foot remains clear floor")
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
			check(npc.meal_return.is_empty(),"Changed physical/profile context clears obsolete return")
			check(npc.needs.hunger>=hunger-.001,"Changed context never grants abandoned meal relief")
			var first:Dictionary=npc.snapshot();var pictures:Array=[await capture("contact-"+phase+"-"+hazard,npc)]
			if hazard in ["moved-counter","removed-room","replaced-room"]:
				await npc.restore_snapshot(game,saved)
				check(npc.meal_return.is_empty(),"Actual restore rejects obsolete furniture/room contact")
			results.append({"phase":phase,"change":hazard,"first":first,"restored":npc.snapshot(),"captures":pictures})

	var file:=FileAccess.open(OUT+"native-context-changes-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Thirty actual South service/power-loss return journeys: all six phases x moved counter, removed room, replaced room, controlled equipped-profile change, controlled clear-floor displacement. Active-return crowd step-aside policy holds contact. Runtime stale-return cleanup/no meal relief; obsolete furniture/room restores rejected. Gear/displacement are controlled state changes, not actual locker/crowd trips; no disk layout-change Continue claim."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"native-context-changes.gd.uid"):
		var uid_file=FileAccess.open(OUT+"native-context-changes.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("JAMES SOUTH RETURN CONTEXT CHANGES: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
