extends SceneTree
const OUT := "res://character/james-console-water-exit-turn-v1/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000
	for mode in ["bare","helmet"]:
		for phase_goal in ["entry","console","exit","egress"]:
			for event in ["power","low-air","drain","gear","fire","death"]:
				game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear();game.running=true;game.paused=false;game.crew_count=4;game.summary_layer.hide()
				game.recovered_crew[0].alive=true
				for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
					var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
					room.pos=cell+offset;room.rotation=0;room.water_level=.65 if mode=="bare" else .95
					game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
				npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
				npc.foot=center+Vector2(0,384);npc.direction="north";npc.goal="";npc.goal_cell=cell;npc.path.clear();npc.state="idle";npc.timer=0;npc.activity="choosing service";npc.air_recovery=0;npc.air_was_low=false
				npc.set_meta("flood_safety_wait",0.0);npc.set_meta("flood_blocked_warning",false);npc.set_meta("fire_retry",0.0)
				npc.needs={"maintenance":80.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0;npc.helmet_equipped=mode=="helmet"
				player.motion.clear();player.current_key="";player.last_time=-1;player.current_equipment="" if mode=="bare" else "diving-helmet";game.visual_time_seconds=100
				preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",0);npc.choose_goal(game)
				var ticks:=0;var ready:=false
				while ticks<8000 and not ready and not npc.dead:
					preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);ticks+=1;game.visual_time_seconds+=1.0/120
					ready=npc.console_motion.get("phase","")==phase_goal and (phase_goal=="egress" or float(npc.console_motion.elapsed)>.25)
				check(ready,"Actual controller reaches interruption phase")
				if not ready:continue
				var before:Dictionary=npc.snapshot();var before_pixels:PackedByteArray=game.grid_view._get_branforth_frame(game).get_image().get_data();var before_need:float=npc.needs.maintenance
				for malformed in ["phase","elapsed","contact","helmet","path"]:
					var invalid:Dictionary=before.duplicate(true)
					if malformed=="path":invalid.path="not a path"
					else:invalid.branforth_console[malformed]={"phase":"missing","elapsed":INF,"contact":Vector2(INF,0),"helmet":"helmet"}[malformed]
					check(not preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(invalid),"Malformed console snapshot rejected: "+malformed)
				match event:
					"power":game.powered_room_cells.erase(cell)
					"low-air","death":
						for room in game.placed_rooms:room.water_level=.95
						if npc.helmet_equipped:npc.tank_oxygen=.5 if event=="low-air" else 0
						else:npc.breath_oxygen=.5 if event=="low-air" else 0
					"drain":
						for room in game.placed_rooms:room.water_level=0.0
					"gear":
						for room in game.placed_rooms:room.water_level=.65
						npc.helmet_equipped=not npc.helmet_equipped
					"fire":game.occupied[cell].fire=.1
				preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);game.visual_time_seconds+=1.0/120
				var texture:Texture2D=game.grid_view._get_branforth_frame(game);check(texture!=null,"Interrupted native selected frame")
				var body_clear:=true
				if texture!=null and npc.movement_medium=="flooded":
					var used:Rect2=texture.get_meta("crew_alpha_extent");body_clear=npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,[used.position.x,used.position.y,used.end.x,used.end.y])
					if not npc.dead:check(body_clear,"Interrupted live body/pose clears geometry")
				if event=="power":
					if phase_goal=="entry":
						check(npc.console_motion.get("phase","")=="entry" and npc.console_motion.get("aborted",false),"Interrupted entry finishes coherent quarter before leaving")
						check(npc.foot==before.foot,"Power loss keeps partial entry stationary")
					if phase_goal in ["entry","console"]:check(npc.needs.maintenance>=before_need,"Interrupted console grants no work credit")
					var resumed:=0
					while not npc.console_motion.is_empty() and resumed<2000:
						preload("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/120);npc.update(game,1.0/120);game.visual_time_seconds+=1.0/120;resumed+=1
					check(npc.console_motion.is_empty() and npc.foot.distance_to(center+Vector2(32,144))<.1,"Interrupted service safely exits to graph")
				elif event=="gear":
					check(not npc.console_motion.is_empty() and npc.console_motion.helmet==npc.helmet_equipped,"Gear switches retain validated phase")
					check(preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(npc.snapshot()),"Gear-switched phase snapshot valid")
				elif event=="death":check(npc.dead and npc.console_motion.is_empty() and not npc.console_turn_active(),"Actual oxygen exhaustion cancels held action")
				else:check(npc.console_motion.is_empty(),"Safety/medium change cancels obsolete hold")
				if event=="low-air":check(npc.activity.begins_with("LOW AIR") and npc.goal=="","Normal low-air safety takes priority")
				if event=="fire":check(npc.goal=="fire-retreat","Normal fire evacuation takes priority")
				results.append({"mode":mode,"phase":phase_goal,"event":event,"bodyClear":body_clear,"dead":npc.dead,"state":npc.state,"goal":npc.goal})
	var file:=FileAccess.open(OUT+"native-interruption-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"48 actual chooser/update phase interruptions, four phases/two gear/six events; normal unpower/low-air/fire/drain/gear and natural oxygen death, malformed console snapshots. Live flooded poses clear; corpse geometry recorded diagnostically, not asserted or polished here. No owner profile use."},"  "));file.close()
	print("JAMES CONSOLE INTERRUPTIONS: ",checks," checks; ",failures," failures; ",results.size()," actual scenarios")
	quit(1 if failures else 0)
