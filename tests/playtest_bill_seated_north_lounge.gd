extends SceneTree
var OUT="res://output/bill-seated-north-lounge-v1/"
var selected_runtime:=false
const LIFE=preload("res://scripts/crew_life.gd")
var game
var checks:=0
var failures:=0
var samples:=[]
func check(ok: bool,why: String):
	checks+=1
	if not ok:failures+=1;push_error(why)
func _init():
	selected_runtime=OS.get_cmdline_user_args().has("--selected")
	if selected_runtime:OUT="res://output/bill-seated-north-selected-lounge-v1/"
	call_deferred("run")
func capture(label: String,npc) -> void:
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(OUT+label+".png")==OK,"Native furniture capture")
	var frame: Texture2D=game.grid_view._get_human_frame_source(npc.animation_state(),npc.direction)
	samples.append({"file":label+".png","stage":npc.stage,"timer":npc.timer,"elapsed":npc.action_elapsed(),"foot":[npc.foot.x,npc.foot.y],"offset":[LIFE.offset(npc).x,LIFE.offset(npc).y],"pivot":str(frame.get_meta("crew_pivot")),"height":frame.get_meta("crew_standing_height")})
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures:quit(1);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-lounge-review.meta";game.run_save_path=game.meta.save_path+".loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:npc.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.selected_rotation=0;game._place_room("crew_lounge",cell,true);game.powered_room_cells[cell]=true
	var player=game.grid_view.human_water_player
	if not selected_runtime:
		player.load_manifest("res://character/bill-seated-north-coherent-v1/manifest.json",true)
		player.load_manifest("res://character/bill-seated-idle-north-v1/bare-manifest.json",true)
		check(player.load_equipment_manifest("diving-helmet","res://character/bill-seated-helmet-north-coherent-v1/manifest.json"),"Transition equipment injection")
		check(player.load_equipment_manifest("diving-helmet","res://character/bill-seated-idle-north-v1/helmet-manifest.json"),"Breathing equipment injection")
		for state in ["sit-down","sit-idle","sit-rise"]:
			game.grid_view.human_animations[state]["north"]=player.frames[state+"-north"]
			game.grid_view.human_animation_timing[state+"-north"]=player.timing[state+"-north"]
		game.grid_view.human_equipment_frames=player.equipment_frames
	for spec in [["res://character/bill-seated-north-family-v1/bare-manifest.json",""],["res://character/bill-seated-north-family-v1/helmet-manifest.json","diving-helmet"]]:
		var family: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]));var clips: Dictionary=player.frames if spec[1].is_empty() else player.equipment_frames[spec[1]]
		for state in family.states:
			for i in 6:
				check(clips[state.id][i].get_image().get_data()==Image.load_from_file(state.frameFiles[i]).get_data(),"Normal selected source pixels")
				check(clips[state.id][i].get_meta("crew_pivot")==Vector2(128,224) and clips[state.id][i].get_meta("crew_standing_height")==148.0,"Normal selected pivot/density")
				check(game.grid_view.human_animations[state.id.trim_suffix("-north")]["north"][i]==player.frames[state.id][i],"Normal cosmetic-loop array binding")
		var idle: Image=clips["idle-north"][0].get_image();var plane:=Image.create(256,256,false,Image.FORMAT_RGBA8);plane.blit_rect(idle,Rect2i(Vector2i.ZERO,idle.get_size()),Vector2i(36,52))
		check(clips["sit-down-north"][0].get_image().get_data()==plane.get_data(),"Exact currently selected standing idle entry")
		check(clips["sit-rise-north"][-1].get_image().get_data()==plane.get_data(),"Exact currently selected standing idle exit")
		check(clips["sit-down-north"][-1].get_image().get_data()==clips["sit-idle-north"][0].get_image().get_data(),"Selected sitting joins breathing")
		check(clips["sit-rise-north"][0].get_image().get_data()==clips["sit-idle-north"][-1].get_image().get_data(),"Selected breathing joins rising")
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var npc=game.bill_npc
	for gear in [false,true]:
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.goal="";npc.path.clear();npc.timer=0;npc.state="idle";npc.movement_medium="dry";npc.helmet_equipped=gear
		npc.decision_rng=RandomNumberGenerator.new();npc.decision_rng.seed=881
		var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384;var entry: int=npc.nearest_in_room(center,cell,false)
		check(entry>=0,"Actual lounge navigation entry")
		if entry<0:quit(1);return
		npc.foot=npc.graph.get_point_position(entry)
		for key in npc.needs:npc.needs[key]=0.0
		npc.needs.fatigue=100.0;npc.service_preferences.fatigue=["crew_lounge"];npc.choose_goal(game)
		for step in range(1000):
			if npc.path.is_empty():break
			npc.move(.1)
		check(npc.path.is_empty(),"Actual approach completes");check(npc.begin_room_activity(),"Actual lounge service begins");check(npc.stage=="life_sit" and npc.direction=="north","Authored north chair selected")
		var name: String="helmet" if gear else "bare"
		await capture(name+"-standing",npc)
		for i in range(1,8):
			npc.update(game,.1);check(npc.stage=="life_sit","Sit simulation remains finite");await capture(name+"-sit-%02d"%i,npc)
		check(npc.valid_snapshot(npc.snapshot()),"Intermediate sit snapshot")
		npc.update(game,.11);check(npc.stage=="life_seated","Actual sit reaches rest")
		for i in 6:
			game.visual_time_seconds+=.16;await capture(name+"-breath-%02d"%i,npc)
		check(npc.valid_snapshot(npc.snapshot()),"Seated snapshot")
		npc.update(game,7.41);check(npc.stage=="life_rise","Actual rest reaches rise")
		for i in 8:
			await capture(name+"-rise-%02d"%i,npc);npc.update(game,.1)
		npc.update(game,.02);check(npc.stage!="life_rise","Rise completes")
		for elapsed in [.05,.1,.22,.36,.44,.6,.7,.79]:
			game.powered_room_cells[cell]=true;npc.goal="fatigue";npc.goal_cell=cell;npc.stage="life_sit";npc.state="idle";npc.path.clear();npc.direction="north";npc.timer=.8-elapsed
			check(npc.valid_snapshot(npc.snapshot()),"Interrupted sitting starts from valid actor state")
			var before: Texture2D=game.grid_view._get_human_frame_source("sit-down","north");var offset_before: Vector2=LIFE.offset(npc)
			# update deliberately ignores delta<=0. Use a real minimal simulation tick.
			game.powered_room_cells.erase(cell);npc.update(game,.000000001)
			check(npc.stage=="life_rise" and npc.goal.is_empty(),"Actual power loss starts rise")
			var after: Texture2D=game.grid_view._get_human_frame_source("sit-rise","north")
			check(before.get_image().get_data()==after.get_image().get_data(),"Interrupted sitting preserves exact pose at "+str(elapsed))
			check(offset_before.distance_to(LIFE.offset(npc))<.0001,"Interrupted sitting preserves furniture contact at "+str(elapsed))
			check(absf(npc.timer-elapsed)<.00001,"Interrupted rise only reverses performed motion")
			if is_equal_approx(elapsed,.36):await capture(name+"-interrupted-rise",npc)
			npc.update(game,elapsed+.001);check(npc.stage!="life_rise","Interrupted rise completes at retained standing endpoint")
		game.powered_room_cells[cell]=true
	var f:=FileAccess.open(OUT+"furniture-samples.json",FileAccess.WRITE);f.store_string(JSON.stringify(samples,"\t"));f.close()
	print("BILL LOUNGE: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
