extends SceneTree
const OUT="res://output/bill-seated-north-selected-reading-chair-v1/"
const SAVE=preload("res://scripts/run_save.gd")
var game
var checks:=0
var failures:=0
var samples:=[]
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func capture(label: String,npc):
	game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(root.get_texture().get_image().save_png(OUT+label+".png")==OK,"Native sofa capture")
	var offset: Vector2=npc.observation_visual_offset()
	samples.append({"file":label+".png","stage":npc.stage,"timer":npc.timer,"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"offset":[offset.x,offset.y]})
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch profile")
	if failures or DisplayServer.get_name()=="headless":quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-sofa-review.meta";game.run_save_path=game.meta.save_path+".loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
	var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("crew_lounge",cell,true);game.powered_room_cells[cell]=true
	var player=game.grid_view.human_water_player
	for spec in [["res://character/bill-seated-north-family-v1/bare-manifest.json",""],["res://character/bill-seated-north-family-v1/helmet-manifest.json","diving-helmet"]]:
		var family: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(spec[0]));var clips: Dictionary=player.frames if spec[1].is_empty() else player.equipment_frames[spec[1]]
		for state in family.states:
			for i in 6:
				check(clips[state.id][i].get_image().get_data()==Image.load_from_file(state.frameFiles[i]).get_data(),"Normal selected pixels")
				check(clips[state.id][i].get_meta("crew_pivot")==Vector2(128,224) and clips[state.id][i].get_meta("crew_standing_height")==148.0,"Normal selected figure plane")
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var npc=game.bill_npc
	for gear in [false,true]:
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.state="idle";npc.timer=0;npc.path.clear();npc.movement_medium="dry";npc.helmet_equipped=gear;npc.goal="fatigue";npc.goal_cell=cell
		var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384;var stations: Array=npc.RoomActivity.stations(npc.geometry[cell]).filter(func(s):return s.get("mode","")=="sit")
		check(not stations.is_empty(),"Actual lounge seated station")
		if stations.is_empty():quit(1);return
		var station: Dictionary=stations[0];check(station.facing=="north" and station.has("rest_point"),"Actual north chair geometry")
		var start: int=npc.nearest_in_room(center,cell,false);var target: int=npc.nearest_in_room(center+Vector2(station.point),cell,false);check(start>=0 and target>=0,"Actual sofa navigation points")
		npc.foot=npc.graph.get_point_position(start);npc.path=npc.route_between(start,target);npc.state="walk"
		for unused in 1000:
			if npc.path.is_empty():break
			npc.move(.1)
		check(npc.path.is_empty() and npc.begin_room_activity(),"Actual route arrives and starts seated service");check(npc.stage=="life_sit" and npc.direction=="north","Actual lounge sitting chooser")
		# Reading is explicitly scripted at the real lounge seat. This tests selected
		# pose clocks/renderer/restores, not an autonomous lounge-reading chooser.
		npc.stage="observation_sit";npc.timer=.65
		var approach: Vector2=npc.foot
		var name: String="helmet" if gear else "bare"
		for i in 7:
			await capture(name+"-sit-%02d"%i,npc);npc.update(game,.1)
		check(npc.stage=="observation_read_enter","Actual sit reaches tablet entry")
		var seated_offset: Vector2=npc.observation_visual_offset()
		var previous:=0.0
		for i in 6:
			var elapsed: float=[.03,.10,.19,.29,.38,.45][i];npc.update(game,elapsed-previous);previous=elapsed
			check(npc.animation_state()=="read-seated-enter" and is_equal_approx(npc.action_elapsed(),elapsed),"Actual tablet entry chooser/clock")
			check(npc.observation_visual_offset().distance_to(seated_offset)<.0001,"Entry keeps sofa contact")
			check(npc.valid_bill_snapshot(npc.snapshot()),"Entry snapshot valid");await capture(name+"-enter-%02d"%i,npc)
		npc.update(game,.031);check(npc.stage=="observation_read" and is_equal_approx(npc.timer,11.04),"Actual entry reaches reading with retained budget")
		for i in 6:
			game.visual_time_seconds+=.16;await capture(name+"-read-%02d"%i,npc)
		var before: Texture2D=game.grid_view._get_human_frame_source(npc.animation_state(),npc.direction)
		npc.update(game,11.041);check(npc.stage=="observation_read_exit","Actual reading reaches tablet exit")
		check(game.grid_view._get_human_frame_source(npc.animation_state(),npc.direction).get_image().get_data()==before.get_image().get_data(),"Actual exit preserves current whole reading pose")
		check(is_equal_approx(.48+11.04+npc.timer,12.0),"Existing12-second reading budget")
		previous=0
		for i in 6:
			var elapsed: float=[.03,.10,.19,.29,.38,.45][i];npc.update(game,elapsed-previous);previous=elapsed
			check(npc.animation_state()=="read-seated-exit" and is_equal_approx(npc.action_elapsed(),elapsed),"Actual tablet exit chooser/clock")
			check(npc.observation_visual_offset().distance_to(seated_offset)<.0001,"Exit keeps sofa contact")
			check(npc.valid_bill_snapshot(npc.snapshot()),"Exit snapshot valid");await capture(name+"-exit-%02d"%i,npc)
		npc.update(game,.031);check(npc.stage=="observation_rise","Put-away reaches actual rise")
		for i in 7:
			await capture(name+"-rise-%02d"%i,npc);npc.update(game,.1)
		check(npc.stage!="observation_rise","Actual rise completes")
		for initial in ["observation_sit","observation_read_enter"]:
			var ages: Array=[.05,.08125,.17875,.2925,.43875,.56875,.649] if initial=="observation_sit" else [.01,.06,.14,.24,.34,.42,.479]
			for elapsed in ages:
				game.powered_room_cells[cell]=true;npc.active=true;npc.dead=false;npc.foot=approach;npc.path.clear();npc.goal="fatigue";npc.goal_cell=cell;npc.state="idle";npc.stage=initial;npc.direction="north";npc.timer=(.65 if initial=="observation_sit" else .48)-elapsed;npc.tablet_exit_pose=-1
				check(npc.valid_bill_snapshot(npc.snapshot()),"Valid partial sitting/tablet checkpoint")
				var before_pose: PackedByteArray=game.grid_view._get_human_frame_source(npc.animation_state(),"north").get_image().get_data();var before_offset: Vector2=npc.observation_visual_offset()
				game.powered_room_cells.erase(cell);npc.update(game,.000000001)
				check(npc.stage==("observation_rise" if initial=="observation_sit" else "observation_read_exit") and npc.goal.is_empty(),"Actual power loss reverses current transition")
				check(game.grid_view._get_human_frame_source(npc.animation_state(),"north").get_image().get_data()==before_pose,"Interrupted transition preserves exact source pose at "+str(elapsed))
				check(npc.observation_visual_offset().distance_to(before_offset)<.0001,"Interrupted transition preserves sofa contact")
				check(absf(npc.timer-elapsed)<.00001 and npc.valid_bill_snapshot(npc.snapshot()),"Only performed motion reverses and remains restorable")
				npc.update(game,npc.timer+.001)
				if initial=="observation_read_enter":check(npc.stage=="observation_rise","Interrupted tablet put-away precedes rise");npc.update(game,.651)
		for pose in 6:
			game.powered_room_cells[cell]=true;npc.active=true;npc.foot=approach;npc.goal="fatigue";npc.goal_cell=cell;npc.path.clear();npc.state="idle";npc.stage="observation_read";npc.direction="north";npc.timer=7.0;npc.tablet_exit_pose=-1
			game.grid_view.human_animation_key="";game.grid_view._get_human_frame_source("read-seated","north");game.visual_time_seconds+=(pose+.5)*.16
			var before_pose: PackedByteArray=game.grid_view._get_human_frame_source("read-seated","north").get_image().get_data()
			game.powered_room_cells.erase(cell);npc.update(game,.000000001)
			check(npc.stage=="observation_read_exit" and npc.tablet_exit_pose==pose,"Arbitrary reading phase is retained for cleanup")
			check(game.grid_view._get_human_frame_source(npc.animation_state(),"north").get_image().get_data()==before_pose,"Interrupted reading has exact first cleanup pose")
			npc.update(game,.481);check(npc.stage=="observation_rise","Reading interruption puts away tablet before rising")
		game.powered_room_cells[cell]=true
		for record in [["observation_read_enter",.25,-1],["observation_read",4.0,-1],["observation_read_exit",.47,3],["observation_read_exit",.25,3],["observation_rise",.4,-1]]:
			npc=game.bill_npc;npc.active=true;npc.foot=approach;npc.goal="fatigue";npc.goal_cell=cell;npc.path.clear();npc.state="idle";npc.stage=record[0];npc.direction="north";npc.timer=record[1];npc.tablet_exit_pose=record[2];npc.helmet_equipped=gear
			var expected: PackedByteArray=game.grid_view._get_human_frame_source(npc.animation_state(),"north").get_image().get_data();var offset: Vector2=npc.observation_visual_offset()
			game.run_save_path="user://bill-reading-selected.loop"
			check(SAVE.write(game,game.run_save_path)==OK,"Actual reading disk checkpoint: "+SAVE.last_error);var data: Dictionary=SAVE.read(game.run_save_path);check(not data.is_empty(),"Readable reading checkpoint")
			if not data.is_empty():
				check(await SAVE.restore(game,data),"Actual reading checkpoint restore: "+SAVE.last_error);game.set_process(false);game.tick_timer.stop();game.run_save_path="user://bill-reading-selected.loop";npc=game.bill_npc
				check(npc.stage==record[0] and is_equal_approx(npc.timer,record[1]) and npc.tablet_exit_pose==record[2] and npc.helmet_equipped==gear,"Saved reading state/clock/cached pose restored")
				check(game.grid_view._get_human_frame_source(npc.animation_state(),"north").get_image().get_data()==expected,"Exact selected reading pixels after disk restore")
				check(npc.observation_visual_offset().distance_to(offset)<.0001,"Saved reading furniture contact restored")
		var invalid: Dictionary=npc.snapshot();invalid.stage="observation_read_enter";invalid.timer=.2;invalid.tablet_exit_pose=6;check(not npc.valid_bill_snapshot(invalid),"Reject invalid cached reading pose")
		invalid.tablet_exit_pose=-1;invalid.timer="bad";check(not npc.valid_bill_snapshot(invalid),"Reject invalid tool timer without coercion")
	var f:=FileAccess.open(OUT+"sofa-samples.json",FileAccess.WRITE);f.store_string(JSON.stringify(samples,"\t"));f.close();print("BILL NORTH READING CONTRACT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
