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
	for issue in ["power-loss","food-empty","complete"]:
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
			var credited:=0.0;var left:=false;var after_ticks:=0
			while after_ticks<1600 and not left:
				var hunger:float=npc.needs.hunger;var old_stage:String=npc.stage
				game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;after_ticks+=1
				var relief:float=hunger-float(npc.needs.hunger)
				if relief>1:credited+=relief+.12*preload("res://scripts/research_tree.gd").needs_rate(game.meta)/120
				if after_ticks==1:
					var after_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
					pictures.append(await capture(issue+"-"+phase+"-after",npc))
					results.append({"issue":issue,"phase":phase,"before":before,"after":npc.snapshot(),"samePixels":after_pixels==before_pixels,"captures":pictures})
				left=npc.stage not in ["life_eat","life_drink"]
			check(left,"Meal completes or is genuinely cancelled")
			check(absf(credited-(45.0 if issue=="complete" else 0.0))<.001,"Exactly one normal meal relief; no cancelled/empty-food relief")
			results[-1]["credited"]=credited;results[-1]["afterTicks"]=after_ticks
	var file:=FileAccess.open(OUT+"native-audit-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Thirteen actual default North galley journeys from normal hunger chooser: six power losses, six depleted-food continuations, one normal completion. Audit immediate pose continuity and hunger credit; no abort choreography or Continue proof claimed."},"  "));file.close()
	print("JAMES MEAL INTERRUPTION AUDIT: ",checks," checks; ",failures," failures; ",results.size()," actual journeys")
	quit(1 if failures else 0)
