extends SceneTree
const OUT := "res://character/james-meal-pickup-north-v1/"
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
	for q in [0]:
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for helmet in [false]:
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			for offset in [Vector2i.ZERO,inside]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.helmet_returning=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
			npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(inside)*384,cell+inside));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=helmet;npc.movement_medium="dry"
			npc.needs={"maintenance":0.0,"hunger":0.0 if helmet else 95.0,"fatigue":0.0,"curiosity":95.0 if helmet else 0.0};npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0
			npc.visits.clear();player.motion.clear();player.current_key="";player.last_time=-1;game.visual_time_seconds=100
			var seed_used:=0
			for candidate_seed in range(1,65):
				npc.decision_rng.seed=candidate_seed;npc.choose_goal(game)
				if npc.goal_cell==cell and not npc.path.is_empty():seed_used=candidate_seed;break
				npc.goal="";npc.path.clear();npc.timer=0
			check(seed_used>0,"Normal chooser selects actual galley service")
			var mode:String="helmet" if helmet else "bare";var equipment:String="diving-helmet" if helmet else ""
			var ticks:=0;var began:=false;var complete:=false;var restored:=false;var restore_exact:=false;var contact:=Vector2.INF;var facing:="";var arrival:="";var captures:Array=[];var slots:Dictionary={};var stages:Array=[]
			while ticks<10000 and not complete:
				var before:Vector2=npc.foot;var old_stage:String=npc.stage;var intended:String=npc.direction
				if not npc.path.is_empty():intended=npc.movement_heading.get("direction",npc.travel_heading(npc.foot,npc.path[0],npc.direction))
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
				check(npc.can_stand(npc.foot) and npc.segment_clear(before,npc.foot),"Actual meal journey foot and traveled leg clear")
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"Selected James production meal journey frame")
				if npc.stage in ["life_eat","life_drink"]:
					if not began:
						began=true;contact=npc.foot;facing=npc.direction;arrival=intended
						check(arrival==facing,"Galley approach arrives facing counter without meal snap")
						var station:Dictionary=npc.RoomActivity.at(npc.geometry[cell],npc.foot-center)
						check(not station.is_empty() and station.room=="galley" and station.facing==facing,"Normal arrival reaches real galley station")
					check(npc.foot==contact and npc.direction==facing and npc.helmet_equipped==helmet,"Meal remains grounded at selected facing with unchanged gear")
					check(npc.animation_state()==("meal-acquire" if npc.meal_acquire_active() else "eat" if npc.stage=="life_eat" else "drink"),"Pickup stays within original bare meal budget")
					var key:String=npc.animation_state()+"-"+facing
					var clips:Dictionary=player.equipment_frames[equipment] if helmet else player.frames
					check(clips[key].has(texture),"Actual meal selects source pose from installed family")
					if npc.stage not in stages:stages.append(npc.stage)
					var slot:int=clips[key].find(texture);var sample:String=npc.animation_state()+"-"+str(slot)
					if not slots.has(sample):
						slots[sample]=true
						if (npc.meal_acquire_active() or (not helmet and slot in [0,3,5])) or (helmet and npc.timer<=3 and not captures.any(func(path):return "held" in path)):
							captures.append(await capture("q%d-%s-%s-%02d-held"%[q,mode,npc.stage,slot],npc))
					if not restored and npc.stage=="life_eat" and npc.timer<=5.62:
						game.paused=true;var before_actor:Dictionary=npc.snapshot();var pixels:PackedByteArray=texture.get_image().get_data();var clock:float=game.visual_time_seconds
						var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-meal.loop"
						check(save.problem(save.capture(game)).is_empty(),"Meal checkpoint valid")
						check(save.write(game,scratch_path)==OK,"Actual meal checkpoint writes")
						var data:Dictionary=save.read(scratch_path)
						root.remove_child(game);game.queue_free();await process_frame
						game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
						game.meta.save_path="user://james-locker.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
						root.add_child(game);current_scene=game
						while not game.startup_complete:await process_frame
						game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
						check(await save.restore_staged(game,data),"Actual fresh-scene meal disk Continue restores")
						game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
						game._set_grid_zoom(1.256,true,Vector2(.5125,.5125))
						check(npc.snapshot()==before_actor and game.paused and game.visual_time_seconds==clock,"Meal Continue keeps actor and paused simulation clock")
						restore_exact=game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels
						check(restore_exact,"Fresh-scene Continue keeps exact meal pose pixels")
						game._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused meal does not advance")
						check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused fresh-scene Continue holds exact meal pixels")
						game.set_process(false);game.paused=false;restored=true
				elif began and old_stage=="life_drink":complete=true
			check(began and complete and restored and stages==["life_eat","life_drink"],"Actual galley eat/drink stages complete")
			for slot in range(6):check(slots.has("meal-acquire-"+str(slot)),"Real journey observes each acquisition source slot")
			var acquired:Array=player.frames["meal-acquire-north"]
			var idle_image:Image=player.frames["idle-north"][0].get_image()
			var padded:=Image.create(184,192,false,Image.FORMAT_RGBA8);padded.blit_rect(idle_image,Rect2i(Vector2i.ZERO,idle_image.get_size()),Vector2i.ZERO)
			check(acquired[0].get_image().get_data()==padded.get_data(),"Native acquisition begins with exact accepted idle pixels")
			check(acquired[-1].get_image().get_data()==player.frames["eat-north"][0].get_image().get_data(),"Native acquisition ends with exact accepted held meal pixels")
			npc.needs.curiosity=95;npc.timer=0;npc.decision_rng.seed=17
			var next_ticks:=0;var moved:=false
			while next_ticks<2000 and not moved:
				var before:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;next_ticks+=1
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				if npc.foot!=before and npc.animation_state()=="walk":
					moved=true
					if player.current_key!="walk-"+npc.direction or player.current_equipment!=equipment:print("MEAL DEPARTURE DIAGNOSTIC ",JSON.stringify({"rotation":q,"mode":mode,"delta":str(npc.foot-before),"actor":npc.snapshot(),"playerKey":player.current_key,"playerEquipment":player.current_equipment}))
					check(player.current_key=="walk-"+npc.direction and player.current_equipment==equipment,"Meal departure joins selected walk and unchanged gear")
			check(moved,"Normal next task moves after meal")
			results.append({"rotation":q,"mode":mode,"seed":seed_used,"arrivalHeading":arrival,"facing":facing,"restorePixelsExact":restore_exact,"ticks":ticks,"nextWalkingTicks":next_ticks,"slots":slots.keys(),"captures":captures})
	var file:=FileAccess.open(OUT+"native-journey-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"One actual default North bare galley journey through installed900ms acquisition, eating/drinking and next walk; normal chooser/native crew update, all six acquisition slots, fixed contact/gear/facing, exact selected endpoints, one real mid-pickup disk Continue into a fresh scene and pause. Other room rotations/equipped stages, dish/cup transitions and interruptions remain separate."},"  "));file.close()
	print("JAMES PICKUP JOURNEY: ",checks," checks; ",failures," failures; ",results.size()," actual meal/inspection journeys")
	quit(1 if failures else 0)
