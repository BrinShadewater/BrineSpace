extends "res://tests/test_veld_seated_north_continue.gd"
const READ_OUT="res://output/veld-seated-south-selected-v1/"
var read_records:Array=[]
func _init():
	var path="res://tests/test_veld_seated_south_selected.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func fresh():
	var game=load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://veld-selected.meta";game.run_save_path="user://veld-selected.loop";game.Preferences.save_path="user://veld-selected.cfg"
	game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
	var expected=preload("res://scripts/crew_sprite_player.gd").new()
	expected.load_manifest("res://character/veld-seated-south-selected-v1/bare-manifest.json",true)
	check(expected.load_equipment_manifest("diving-helmet","res://character/veld-seated-south-selected-v1/helmet-manifest.json"),"Expected selected paired profile")
	var actual=game.grid_view.veld_player
	for gear in ["","diving-helmet"]:
		var pool:Dictionary=expected.frames if gear.is_empty() else expected.equipment_frames[gear]
		var loaded:Dictionary=actual.frames if gear.is_empty() else actual.equipment_frames[gear]
		var clock:Dictionary=expected.timing if gear.is_empty() else expected.equipment_timing[gear]
		var live_clock:Dictionary=actual.timing if gear.is_empty() else actual.equipment_timing[gear]
		for key in pool:
			check(loaded.has(key) and loaded[key].size()==pool[key].size(),"Normal loader selects complete South state")
			check(live_clock[key]==clock[key],"Normal selected South source clock")
			for index in pool[key].size():
				check(loaded[key][index].get_image().get_data()==pool[key][index].get_image().get_data(),"Normal loader exact selected source")
				check(loaded[key][index].get_meta("crew_pivot")==Vector2(128,224) and loaded[key][index].get_meta("crew_standing_height")==148 and loaded[key][index].get_meta("crew_seat_contact_depth"),"Normal selected calibration and seat ordering metadata")
	return game
func capture_read(game,name:String,texture:Texture2D):
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var ready:=false
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var submitted:=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:submitted=true
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
		if ready:break
	check(ready,"Retained actual reading source and centered sofa")
	check(texture.get_image().save_png(READ_OUT+name+"-source.png")==OK,"Actual reading source saved")
	check(root.get_texture().get_image().save_png(READ_OUT+name+"-room.png")==OK,"Actual native reading capture saved")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(READ_OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant actual sofa fixture")
	game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for value in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if value.get("mode","")=="read" and value.facing=="south":station=value;break
	check(not station.is_empty(),"Actual South observation read service")
	if failures:quit(1);return
	for equipped in [false,true]:
		for elapsed in [3.0,.2,11.8]:
			var actor=game.veld_npc;var player=game.grid_view.veld_player
			actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.direction="south";actor.helmet_equipped=equipped;actor.movement_medium="dry"
			actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
			actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point)
			check(actor.begin_room_activity() and actor.stage=="observation_sit","Normal activity dispatch at prescribed sofa contact")
			game.visual_time_seconds=400;player.current_key="";player.last_time=-1;player.motion.clear()
			for tick in 1600:
				game.grid_view._get_veld_live_frame_source(game)
				if actor.stage=="observation_read" and 12.0-actor.timer>=elapsed:break
				actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
			check(actor.stage=="observation_read","Actual reading clock reached sample")
			var texture:Texture2D=game.grid_view._get_veld_live_frame_source(game)
			var gear:String="diving-helmet" if equipped else ""
			var expected=player.frame_at_elapsed("read-seated-south",12.0-actor.timer,gear)
			check(texture.get_image().get_data()==expected.get_image().get_data(),"Source follows actual persisted reading clock before save")
			var pixels=texture.get_image().get_data();var timer:float=actor.timer;var foot:Vector2=actor.foot;var offset:Vector2=actor.observation_visual_offset()
			var name=("helmet" if equipped else "bare")+"-"+str(elapsed)
			await capture_read(game,name+"-before",texture)
			check(SAVE.write(game,game.run_save_path)==OK,"Actual disk checkpoint write")
			var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Actual disk checkpoint read")
			if failures:quit(1);return
			game.queue_free();await process_frame;game=await fresh()
			check(await SAVE.restore_staged(game,disk),"Actual fresh-scene staged Continue")
			game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-read-continue.loop"
			actor=game.veld_npc
			check(actor.stage=="observation_read" and actor.timer==timer and actor.helmet_equipped==equipped,"Restored action clock and gear")
			check(actor.foot==foot and actor.observation_visual_offset()==offset,"Restored physical foot and sofa contact")
			var after=game.grid_view._get_veld_live_frame_source(game)
			check(after.get_image().get_data()==pixels,"Fresh Continue keeps exact displayed reading pose")
			await capture_read(game,name+"-after",after)
			check(actor.valid_veld_snapshot(actor.snapshot()),"Restored Veld snapshot valid")
			game._process(.5)
			check(actor.timer==timer and game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==pixels,"Paused Continue retains reading pose")
			restores+=1;read_records.append({"gear":gear,"elapsed":12.0-timer,"timer":timer,"name":name})
			print("READ CONTINUE ",name," restores=",restores," failures=",failures)
			if elapsed==11.8:
				var previous:Texture2D=game.grid_view._get_veld_live_frame_source(game);var previous_stage:String=actor.stage
				for tick in 300:
					var shown:Texture2D=game.grid_view._get_veld_live_frame_source(game)
					if actor.stage=="observation_rise" and previous_stage=="observation_read":check(shown.get_image().get_data()==previous.get_image().get_data(),"Normal selected last read/first rise exact join")
					previous=shown;previous_stage=actor.stage
					if actor.stage.is_empty():break
					actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
				check(actor.stage.is_empty(),"Normal selected complete stow/rise service exit")
				await capture_read(game,name+"-completed",game.grid_view._get_veld_live_frame_source(game))
			if failures:quit(1);return
	var file=FileAccess.open(READ_OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":read_records,"scope":"actual timed reading and disk/fresh-scene Continue; prescribed actual sofa contact, normal selected loader, actual timed reading/exit and disk Continue; no natural chooser or interruption dispatch"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(READ_OUT+"final.png")==OK,"Fresh final native capture")
	check(restores==6,"Both gears and draw/hold/stow fresh Continue")
	print("VELD SEATED SOUTH SELECTED: %d checks,%d failures; %d fresh-scene disk restores"%[checks,failures,restores]);quit(1 if failures else 0)
