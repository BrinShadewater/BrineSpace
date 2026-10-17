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
	var phases:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
	for issue in ["power-loss"]:
		for phase in (phases if issue!="complete" else ["cup-deposit"]):
			game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			for offset in [Vector2i.ZERO,Vector2i.DOWN]:
				var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
				room.pos=cell+offset;room.rotation=0;room.water_level=0
				game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
			npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.helmet_returning=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
			npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2.DOWN*384,cell+Vector2i.DOWN));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry"
			npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.visits.clear();player.motion.clear();player.current_key="";player.last_time=-1;game.resources.food=1000;game.visual_time_seconds=100
			npc.decision_rng.seed=1;npc.choose_goal(game)
			check(npc.goal=="hunger" and npc.goal_cell==cell and not npc.path.is_empty(),"Actual normal hunger chooser enters galley")
			var ticks:=0;var reached:=false
			while ticks<3000 and not reached:
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
				var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
				if npc.animation_state()==phase:
					var slot:int=player.frames[phase+"-north"].find(texture)
					if slot==3:reached=true
			check(reached,"Actual normal meal reaches requested interruption pose")
			var before:Dictionary=npc.snapshot();var before_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
			var pictures:Array=[await capture(issue+"-"+phase+"-before",npc)]
			if issue=="power-loss":game.powered_room_cells.erase(cell)
			if issue=="food-empty":game.resources.food=0
			var credited:=0.0;var left:=false;var after_ticks:=0;var restored:=false;var contact:Vector2=npc.foot
			while after_ticks<1600 and not left:
				var hunger:float=npc.needs.hunger;var old_stage:String=npc.stage
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;after_ticks+=1
				var relief:float=hunger-float(npc.needs.hunger)
				if relief>1:credited+=relief+.12*preload("res://scripts/research_tree.gd").needs_rate(game.meta)/120
				if after_ticks==1:
					var after_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
					pictures.append(await capture(issue+"-"+phase+"-after",npc))
					results.append({"issue":issue,"phase":phase,"before":before,"after":npc.snapshot(),"samePixels":after_pixels==before_pixels,"captures":pictures})
				if after_ticks==1:
					check(npc.meal_return_active() and results[-1].samePixels,"Power loss begins exact current-pose return")
					game.powered_room_cells[cell]=true
				if npc.meal_return_active():
					check(npc.foot==contact and npc.direction=="north" and npc.stage=="" and npc.goal=="" and not npc.helmet_equipped,"Interrupted return stays fixed and uncommitted despite restored power")
					var clip:String=npc.animation_state()+"-north"
					check(player.frames[clip].has(game.grid_view._get_branforth_frame_source(game)),"Production return uses selected whole source pose")
				if not restored and npc.meal_return_active() and float(npc.meal_return.elapsed)>=npc.meal_return_seconds(npc.meal_return.source,npc.meal_return.index)*.35:
					game.paused=true;var before_actor:Dictionary=npc.snapshot();var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();var clock:float=game.visual_time_seconds
					var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-meal-return.loop"
					check(save.problem(save.capture(game)).is_empty(),"Meal return checkpoint valid")
					check(save.write(game,scratch_path)==OK,"Actual meal return checkpoint writes")
					var data:Dictionary=save.read(scratch_path)
					root.remove_child(game);game.queue_free();await process_frame
					game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
					game.meta.save_path="user://james-locker.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
					root.add_child(game);current_scene=game
					while not game.startup_complete:await process_frame
					game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
					check(await save.restore_staged(game,data),"Actual fresh-scene mid-return disk Continue")
					game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
					game._set_grid_zoom(1.256,true,Vector2(.5125,.5125))
					check(npc.snapshot()==before_actor and game.paused and game.visual_time_seconds==clock,"Interrupted meal Continue retains actor/clock/pause")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Interrupted meal Continue retains exact selected pixels")
					game._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused return does not advance")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Paused return retains exact pose pixels")
					game.paused=false;game.set_process(false);restored=true
				left=not npc.meal_return_active()

			check(left,"Meal completes or is genuinely cancelled")
			check(absf(credited-(45.0 if issue=="complete" else 0.0))<.001,"Exactly one normal meal relief; no cancelled/empty-food relief")
			results[-1]["credited"]=credited;results[-1]["afterTicks"]=after_ticks;results[-1]["freshSceneRestore"]=restored
			check(restored and npc.stage=="" and npc.state=="idle" and npc.goal=="" and npc.foot==contact,"Uncredited return reaches empty standing state")
			var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
			var image:Image=player.frames["idle-north"][0].get_image()
			check(texture.get_image().get_region(Rect2i(Vector2i.ZERO,image.get_size())).get_data()==image.get_data(),"Return ends at exact selected idle pixels")
			results[-1].captures.append(await capture(issue+"-"+phase+"-finished",npc))
			game.resources.food=0;npc.needs.curiosity=95;npc.decision_rng.seed=17
			var walking:=false
			for tick in range(2000):
				var previous:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
				if npc.foot!=previous and npc.animation_state()=="walk":walking=true;break
			check(walking,"Normal chooser moves to next available task after return")
	var file:=FileAccess.open(OUT+"native-return-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Six actual normal North meal services interrupted mid each of six source clips by power loss. Exact current-pose return, fixed foot/facing, no credit or restart despite restored power, selected whole return frames, six fresh-scene mid-return disk Continues with exact actor/clock/pixels/pause, exact idle completion and normal next task. Hazards/changed furniture remain separate."},"  "));file.close()
	print("JAMES MEAL RETURNS: ",checks," checks; ",failures," failures; ",results.size()," actual journeys")
	quit(1 if failures else 0)
