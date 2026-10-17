extends SceneTree
const OUT="res://output/veld-rest-family-station-v1/"
const LIFE=preload("res://scripts/crew_life.gd")
var checks:=0
var failures:=0
var game
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init():
	var uid_path="res://tests/test_veld_rest_family_station.gd.uid"
	if not FileAccess.file_exists(uid_path):
		var uid=FileAccess.open(uid_path,FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://veld-rest-station.meta";game.run_save_path="user://veld-rest-station.loop";root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:npc.active=false
	var cell:=Vector2i(20,20);var npc=game.veld_npc;var grid=game.grid_view;var player=grid.veld_player
	var records:=[]
	var station_audit:=[]
	for rotation in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.selected_rotation=rotation;game._place_room("crew_hab",cell,true);game.powered_room_cells[cell]=true
		await npc.rebuild(game)
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(not stations.is_empty(),"Actual habitation provides a rest service")
		station_audit.append({"rotation":rotation,"stations":stations,"props":npc.geometry[cell].get("props",[])})
		game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
		game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		for k in stations.size():
			var station:Dictionary=stations[k]
			if station.get("mode","")!="sleep":continue
			npc.active=true;npc.dead=false;npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear();npc.helmet_equipped=false;npc.movement_medium="dry";npc.goal_cell=cell;npc.direction=station.facing;npc.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0
			check(npc.can_stand(npc.foot),"Actual berth approach clear")
			check(LIFE.begin(npc,station) and npc.bunk_motion_active() and npc.direction=="east" and not station.has("rest_head"),"Current habitation selects specialised east bunk, no generic cardinal target")
			var foot:Vector2=npc.foot
			for phase in [["entry","life_lie",npc.BUNK_SECONDS],["rest","life_sleep",10.4]]:
				npc.stage=phase[1];npc.timer=phase[2];game.visual_time_seconds=400;player.current_key="";player.last_time=-1
				var texture:Texture2D=grid._get_veld_live_frame_source(game)
				check(texture!=null and texture.get_meta("crew_standing_height")==148.0,"Existing selected bunk frame remains available")
				check(npc.foot==foot and npc.bunk_motion_active(),"Selected bunk keeps physical approach")
				var shift:Vector2=LIFE.head_alignment(npc,player)
				check(shift==Vector2.ZERO,"Optional rest-head hook bypasses specialised bunk")
				grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
				var filename:String="rotation-%d-berth-%d-%s.png"%[rotation,k,phase[0]]
				check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Actual habitation rest capture")
				records.append({"rotation":rotation,"berth":k,"phase":phase[0],"station":station,"headShift":shift,"lifeOffset":LIFE.offset(npc),"physicalFoot":foot,"screenshot":filename})
			npc.active=false
	var file:=FileAccess.open(OUT+"contacts.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"current habitation station availability audit and selected east bunk regression, NOT generic cardinal furniture proof; routing/survival/save/helmet not proven","records":records,"stationAudit":station_audit},"\t"));file.close()
	check(records.size()==8,"Four actual rotations/two selected east bunk poses")
	check(root.get_texture().get_image().save_png(OUT+"loaded-water-carry.png")==OK,"Fresh final actual room capture")
	print("VELD REST FAMILY STATION: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
