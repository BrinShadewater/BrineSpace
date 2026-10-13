extends "res://tests/test_veld_read_south_continue.gd"
const INTERRUPT_OUT="res://output/veld-read-south-interrupt-v1/"
func _init():
	var path="res://tests/test_veld_read_south_interrupt.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run")
func capture_exit(game,name:String,texture:Texture2D):
	game.selected_card_id="";game.selected_room_cell=CELL
	game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var submitted:=false
	for attempt in 90:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		submitted=false
		if game.grid_view.content_canvases.has(CELL):
			for slot in game.grid_view.content_canvases[CELL].slots:
				if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:submitted=true
		var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		if submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4:break
	check(submitted,"Actual exit source retained in sofa drawing")
	check(texture.get_image().save_png(INTERRUPT_OUT+name+"-source.png")==OK,"Exit source capture")
	check(root.get_texture().get_image().save_png(INTERRUPT_OUT+name+"-room.png")==OK,"Exit native capture")
func run():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	DirAccess.make_dir_recursive_absolute(INTERRUPT_OUT);DirAccess.make_dir_recursive_absolute(READ_OUT)
	var game=await fresh()
	game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant sofa fixture")
	game.selected_rotation=0;game._place_room("observation_room",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var station:Dictionary={}
	for value in game.veld_npc.RoomActivity.stations(game.veld_npc.geometry[CELL]):
		if value.get("mode","")=="read" and value.facing=="south":station=value;break
	if station.is_empty():check(false,"Actual South sofa");quit(1);return
	var records:Array=[]
	for equipped in [false,true]:
		for loss in ["power","suspended"]:
			for elapsed in [.2,3.0,4.4,11.8]:
				game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
				var actor=game.veld_npc;var player=game.grid_view.veld_player
				actor.active=true;actor.dead=false;actor.state="idle";actor.stage="";actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear();actor.expedition.clear();actor.bunk_motion.clear();actor.direction="south";actor.helmet_equipped=equipped;actor.movement_medium="dry"
				actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":90.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
				actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point)
				check(actor.begin_room_activity(),"Actual reading service dispatch")
				game.visual_time_seconds=400;player.current_key="";player.last_time=-1;player.motion.clear()
				for tick in 1600:
					game.grid_view._get_veld_live_frame_source(game)
					if actor.stage=="observation_read" and 12.0-actor.timer>=elapsed:break
					actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
				var before=game.grid_view._get_veld_live_frame_source(game)
				var foot:Vector2=actor.foot;var offset:Vector2=actor.observation_visual_offset()
				if loss=="power":game.powered_room_cells.erase(CELL)
				else:game.occupied[CELL].suspended=true
				check(not actor.service_available(game,CELL),"Actual service lost")
				actor.update(game,.00001)
				var after=game.grid_view._get_veld_live_frame_source(game)
				var exact:bool=before.get_image().get_data()==after.get_image().get_data()
				check(exact,"Actual interrupted reader preserves displayed hand/tablet pose")
				check(actor.foot==foot and actor.observation_visual_offset().distance_to(offset)<.001,"Actual interrupted contact held")
				check(actor.valid_veld_snapshot(actor.snapshot()),"Actual interrupted reader snapshot admissible")
				var name=("helmet" if equipped else "bare")+"-"+loss+"-"+str(elapsed)
				check(before.get_image().save_png(INTERRUPT_OUT+name+"-before.png")==OK,"Before actual source saved")
				check(after.get_image().save_png(INTERRUPT_OUT+name+"-after.png")==OK,"After actual source saved")
				records.append({"name":name,"exact":exact,"stage":actor.stage,"timer":actor.timer,"pose":actor.tablet_exit_pose})
				if loss=="power" and elapsed==3.0:
					var pixels=after.get_image().get_data();var timer:float=actor.timer;var pose:int=actor.tablet_exit_pose
					await capture_exit(game,name+"-save",after)
					check(SAVE.write(game,game.run_save_path)==OK,"Interrupted exit disk write")
					var disk:Dictionary=SAVE.read(game.run_save_path);check(not disk.is_empty(),"Interrupted exit disk read")
					game.queue_free();await process_frame;game=await fresh()
					check(await SAVE.restore_staged(game,disk),"Fresh interrupted exit staged Continue")
					game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game.run_save_path="user://veld-read-interrupt.loop"
					actor=game.veld_npc
					check(actor.stage=="observation_read_exit" and actor.timer==timer and actor.tablet_exit_pose==pose,"Fresh interrupted exit timer and retained pose")
					check(actor.foot==foot and actor.observation_visual_offset()==offset,"Fresh interrupted exit contact")
					after=game.grid_view._get_veld_live_frame_source(game)
					check(after.get_image().get_data()==pixels,"Fresh interrupted exit exact pixels")
					await capture_exit(game,name+"-restore",after)
					game._process(.5)
					check(actor.timer==timer and game.grid_view._get_veld_live_frame_source(game).get_image().get_data()==pixels,"Paused interrupted Continue freezes source")
					restores+=1
				var previous:Texture2D=after;var previous_stage:String=actor.stage
				for tick in 160:
					if actor.stage.is_empty():break
					var shown:Texture2D=game.grid_view._get_veld_live_frame_source(game)
					if actor.stage=="observation_rise" and previous_stage=="observation_read_exit":check(shown.get_image().get_data()==previous.get_image().get_data(),"Actual stowed exit joins rising exactly")
					previous=shown;previous_stage=actor.stage
					actor.update(game,1.0/120);game.visual_time_seconds+=1.0/120
				check(actor.stage.is_empty(),"Actual interrupted stow/rise completes")
				interruptions+=1
	game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
	var file=FileAccess.open(INTERRUPT_OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"records":records,"scope":"actual NPC power/suspend guard and timed exit, prescribed sofa entry with staged source overrides"},"\t"));file.close()
	check(root.get_texture().get_image().save_png(INTERRUPT_OUT+"final.png")==OK,"Final native capture")
	check(restores==2,"Both gears interrupted exit disk Continue")
	print("VELD READ SOUTH INTERRUPT: %d checks,%d failures; %d interruptions; %d fresh-scene disk restores"%[checks,failures,interruptions,restores]);quit(1 if failures else 0)
