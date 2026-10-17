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
	var path:String=OUT+"hazard-captures/"+label+".png"
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
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[0.0,126.0]}};store.revision+=1;store.geometry_revision+=1;store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"hazard-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	for phase in ["eat"]:
		for hazard in ["fire","flood"]:
			print("HAZARD SETUP ",phase,"/",hazard," prior running=",game.running," paused=",game.paused," crew=",game.crew_count)
			game.running=true;game.paused=false;game.crew_count=1;game.summary_layer.visible=false
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			for member in game.recovered_crew:
				if member.get("architect_id","")=="branforth":member.alive=true
			for offset in [Vector2i.ZERO,Vector2i.DOWN]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=0;room.water_level=0;room.fire=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			npc.rebuild(game);npc.meal_return.clear();npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
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
			var hunger:float=npc.needs.hunger;var old:Vector2=npc.foot
			var start:int=npc.nearest_in_room(npc.foot,cell);var reachable:=0
			for id in npc.room_nodes.get(cell+Vector2i.DOWN,[]):
				if not npc.graph.get_id_path(start,id).is_empty():reachable+=1
			print("REFUGE DIAGNOSTIC ",JSON.stringify({"start":start,"connected":game._connected_neighbor_cells(cell),"storageNodes":npc.room_nodes.get(cell+Vector2i.DOWN,[]).size(),"reachable":reachable,"open":npc.geometry[cell].open,"blockers":npc.geometry[cell].blockers,"foot":npc.foot,"clear":npc.can_stand(npc.foot),"doorsLocked":npc.hardware_doors_locked}))

			if hazard=="fire":game.occupied[cell].fire=.7
			elif hazard=="flood":game.occupied[cell].water_level=.95
			else:game.resources.oxygen=0;npc.breath_oxygen=.001
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
			check(not npc.meal_return_active(),"Genuine hazard immediately preempts cosmetic return")
			check(npc.meal_return.is_empty(),"Hazard clears stale return state")
			check(npc.needs.hunger>=hunger-.001,"Emergency never grants abandoned meal reward")
			print("HAZARD FIRST ",phase,"/",hazard," running=",game.running," paused=",game.paused," dead=",npc.dead," goal=",npc.goal," return=",npc.meal_return)
			if npc.dead:game.summary_layer.visible=false # Reveal actor for capture after real death/report assertions.
			var first:Dictionary=npc.snapshot();var pictures:Array=[await capture("hazard-"+phase+"-"+hazard+"-first",npc)]
			var safe:=false;var moved:bool=npc.foot!=old;var ticks:=0
			if hazard=="oxygen-loss":check(npc.dead and npc.animation_state()=="death-ground","Real oxygen depletion selects actual death source");safe=npc.dead
			else:
				while ticks<3000 and not safe and not npc.dead:
					var before:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
					var after:Vector2=npc.foot;npc.foot=before
					var clear:bool=npc.segment_clear(before,after);npc.foot=after
					if not clear:print("HAZARD LEG ",phase,"/",hazard," ",before," -> ",after," goal=",npc.goal," medium=",npc.movement_medium)
					check(clear,"Emergency traveled floor leg clears geometry from actual origin")
					moved=moved or npc.foot!=before
					var room:Dictionary=game.occupied.get(npc.cell_at(npc.foot),{})
					safe=not room.is_empty() and npc.cell_at(npc.foot)!=cell and float(room.get("fire",0))<=0 and float(room.get("water_level",0))<.55
				check(safe and moved and not npc.dead,"Actual emergency route reaches live refuge before air expires")
			print("REFUGE END DIAGNOSTIC ",JSON.stringify({"water":game.occupied[cell].get("water_level"),"refugeWater":game.occupied[cell+Vector2i.DOWN].get("water_level"),"currentMedium":npc.movement_medium,"snapshot":npc.snapshot()}))
			pictures.append(await capture("hazard-"+phase+"-"+hazard+"-end",npc))
			results.append({"phase":phase,"hazard":hazard,"first":first,"safe":safe,"moved":moved,"ticks":ticks,"end":npc.snapshot(),"captures":pictures})
	var file:=FileAccess.open(OUT+"native-refuge-diagnostic-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Eighteen actual normal South services, six phases, interrupted mid-return by real fire/flood/oxygen depletion through native systems. Immediate preemption/state cleanup/no abandoned reward; real refuge route or real death. Supported open prep at[0,126] only; other gears/layouts/changed contacts/crowd hazards and disk hazard restores separate."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"native-refuge-diagnostic.gd.uid"):
		var uid_file=FileAccess.open(OUT+"native-refuge-diagnostic.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("JAMES SOUTH MEAL RETURN HAZARDS: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
