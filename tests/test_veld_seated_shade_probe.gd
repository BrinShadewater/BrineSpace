extends "res://tests/test_veld_seated_north_continue.gd"
const PROBE_OUT="res://output/veld-seated-shade-probe-v1/"
func _init():
	var path="res://tests/test_veld_seated_shade_probe.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	call_deferred("run_probe")
func run_probe():
	check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA")
	if failures:quit(2);return
	DirAccess.make_dir_recursive_absolute(PROBE_OUT)
	var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
	game.selected_rotation=0;game._place_room("crew_lounge",CELL,true);game.powered_room_cells[CELL]=true
	await game.veld_npc.rebuild(game)
	var actor=game.veld_npc;var grid=game.grid_view;var station:Dictionary={}
	for candidate in actor.RoomActivity.stations(actor.geometry[CELL]):
		if candidate.get("mode","")=="sit" and candidate.has("seat_depth") and actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(candidate.point)):station=candidate;break
	check(not station.is_empty(),"Same default lounge chair")
	if failures:quit(1);return
	# Reproduce first Continue capture after real power/suspend interruptions.
	for loss in ["power","suspended"]:
		for elapsed in [.04,.12,.25,.40,.55,.70,1.0]:
			game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true;prepare(actor,station,false)
			actor.stage="life_seated" if elapsed==1.0 else "life_sit";actor.timer=7.4 if elapsed==1.0 else .8-elapsed
			game.visual_time_seconds=400;grid.veld_player.current_key="";grid.veld_player.last_time=-1
			if loss=="power":game.powered_room_cells.erase(CELL)
			else:game.occupied[CELL].suspended=true
			actor.update(game,.00001)
	game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
	prepare(actor,station,false);actor.stage="life_sit";actor.timer=.4;game.visual_time_seconds=400
	grid.veld_player.current_key="";grid.veld_player.last_time=-1
	var source:Texture2D=grid._get_veld_live_frame_source(game);var source_pixels:PackedByteArray=source.get_image().get_data()
	game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
	var records:=[]
	for sample in 24:
		game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
		game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
		grid.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var photo:Image=root.get_texture().get_image();var crop:Image=photo.get_region(Rect2i(270,280,78,122))
		var center:Vector2=grid.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size())
		check(grid._get_veld_live_frame_source(game).get_image().get_data()==source_pixels and actor.timer==.4,"Unchanged source/action while probing shade")
		check(crop.save_png(PROBE_OUT+"%02d.png"%sample)==OK,"Unmodified native room crop")
		var light_key:Variant=[]
		for key in grid.light_surface_key:
			if key is Array and key.size()>=2 and key[0]==CELL:light_key=key
		records.append({"sample":sample,"cameraReady":center.distance_to(game.grid_scroll.get_global_rect().get_center())<4,"paused":game.paused,"visualClock":game.visual_time_seconds,"quality":game.Preferences.effects_quality,"roomLight":grid._room_light_level(game.occupied[CELL]),"targetLight":grid._room_light_target(game.occupied[CELL]),"flicker":grid._power_flicker(game.occupied[CELL]),"lightingKey":light_key,"pendingLayerCount":grid.pending_layers.size(),"zoomSettling":grid.zoom_settling,"zoomPreparing":grid.zoom_preparing,"sourceSha256":source_pixels.hex_encode().sha256_text()})
	var file=FileAccess.open(PROBE_OUT+"samples.json",FileAccess.WRITE);file.store_string(JSON.stringify(records,"\t"));file.close()
	check(root.get_texture().get_image().save_png(PROBE_OUT+"final.png")==OK,"Final native shade probe")
	print("VELD SEATED SHADE PROBE: %d checks,%d failures;24 same-pose samples"%[checks,failures]);quit(1 if failures else 0)
