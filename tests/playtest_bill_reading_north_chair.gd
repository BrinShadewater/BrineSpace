extends SceneTree
const OUT="res://output/bill-reading-north-sofa-v1/"
var game
var checks:=0
var failures:=0
var samples:=[]
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func capture(label: String,npc):
	check(npc.helmet_equipped==label.begins_with("helmet"),"Retained review gear")
	if npc.stage=="life_seated":
		var player=game.grid_view.human_water_player
		var row: Array=player.equipment_frames["diving-helmet"]["read-seated-north"] if npc.helmet_equipped else player.frames["read-seated-north"]
		check(row.has(game.grid_view._get_human_frame_source("sit-idle","north")),"Actual renderer uses candidate reading texture")
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
	player.load_manifest("res://character/bill-reading-north-v1/bare-manifest.json",true)
	check(player.load_equipment_manifest("diving-helmet","res://character/bill-reading-north-v1/helmet-manifest.json"),"Candidate reading gear injection")
	game.grid_view.human_animations["sit-idle"]["north"]=player.frames["read-seated-north"]
	game.grid_view.human_animation_timing["sit-idle-north"]=player.timing["read-seated-north"]
	player.equipment_frames["diving-helmet"]["sit-idle-north"]=player.equipment_frames["diving-helmet"]["read-seated-north"]
	game.grid_view.human_equipment_frames=player.equipment_frames
	game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
	game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
	var npc=game.bill_npc
	for gear in [false,true]:
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.state="idle";npc.timer=0;npc.path.clear();npc.movement_medium="dry";npc.helmet_equipped=gear;npc.goal="fatigue";npc.goal_cell=cell
		var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384;var stations: Array=npc.RoomActivity.stations(npc.geometry[cell]).filter(func(s):return s.get("mode","")=="sit")
		check(not stations.is_empty(),"Actual north lounge chair station")
		if stations.is_empty():quit(1);return
		var station: Dictionary=stations[0];check(station.facing=="north" and station.has("rest_point"),"Actual north lounge chair geometry")
		var start: int=npc.nearest_in_room(center,cell,false);var target: int=npc.nearest_in_room(center+Vector2(station.point),cell,false);check(start>=0 and target>=0,"Actual sofa navigation points")
		npc.foot=npc.graph.get_point_position(start);npc.path=npc.route_between(start,target);npc.state="walk"
		for unused in 1000:
			if npc.path.is_empty():break
			npc.move(.1)
		check(npc.path.is_empty() and npc.begin_room_activity(),"Actual route arrives and starts reading service");check(npc.stage=="life_sit" and npc.direction=="north","Actual lounge sitting chooser")
		var name: String="helmet" if gear else "bare"
		for i in 7:
			await capture(name+"-sit-%02d"%i,npc);npc.update(game,.125)
		check(npc.stage=="life_seated","Sit reaches seated stage with candidate reading presentation");check(npc.valid_bill_snapshot(npc.snapshot()),"Seated snapshot valid")
		for i in 6:
			game.visual_time_seconds+=.16;await capture(name+"-read-%02d"%i,npc)
		npc.update(game,7.41);check(npc.stage=="life_rise","Actual seated hold reaches rise")
		for i in 7:
			await capture(name+"-rise-%02d"%i,npc);npc.update(game,.125)
		check(npc.stage!="life_rise","Actual rise completes")
	var f:=FileAccess.open(OUT+"sofa-samples.json",FileAccess.WRITE);f.store_string(JSON.stringify(samples,"\t"));f.close();print("BILL SOFA: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
