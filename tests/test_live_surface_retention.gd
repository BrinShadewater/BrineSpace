extends SceneTree
var game
var failures:=0
const OUT="res://output/performance-pass-20260912/"
func _init() -> void: call_deferred("run")
func check(ok: bool,message: String) -> void:
	if not ok: failures+=1;push_error(message)
func rendered() -> void:
	game.grid_view.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	game=load("res://scenes/main.tscn").instantiate()
	var prefix: String="user://surface-pass-%d"%OS.get_process_id()
	game.meta.save_path=prefix+".meta";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	root.size=Vector2i(1600,900);root.gui_disable_input=true
	game.set_process(false);game.grid_view.set_process(false);game.tick_timer.stop()
	game.crew_comms.set_process(false);game.crew_comms.minimize();game.paused=false
	game.Architects.advance_core(game,10);game.paused=true
	game.wrecks.clear();game.drone_fleet.sites.clear()
	var cell:=Vector2i(20,19)
	game._place_room("airlock",cell,true);game.powered_room_cells[cell]=true
	game.selected_card_id="";game.selected_room_cell=cell
	game.grid_view.room_light_levels[cell]=1.0
	game.grid_view.room_light_levels[Vector2i(20,20)]=1.0
	for i in range(6): await rendered()
	game._fit_station_view()
	for i in range(6): await rendered()
	var room: Dictionary=game.occupied[cell]
	room.airlock_cycle={"phase":"opening_outer","elapsed":0.0}
	room.fire=0.1;room.fire_water_seconds=1.0;room.electrical_repair_progress=0.0
	await rendered();await rendered()
	var before:=Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)
	var start:=Time.get_ticks_usec()
	for i in range(60):
		room.airlock_cycle.elapsed=float(i)/60.0
		room.fire=0.1+float(i)*0.001
		room.fire_water_seconds=1.0-float(i)*0.001
		room.electrical_repair_progress=float(i)*0.01
		await rendered()
	var delta:=Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)-before
	print("LIVE SURFACE SAMPLE: floor=",delta.x," wall=",delta.y," mean_frame_ms=",float(Time.get_ticks_usec()-start)/60000.0)
	check(delta==Vector2i.ZERO,"Live hatch/fire progress must not rebuild unchanged floors and walls")
	var cached:=root.get_texture().get_image()
	cached.save_png(OUT+"live-state-cached.png")
	game.grid_view.surface_key=[]
	await rendered();await rendered()
	var rebuilt:=root.get_texture().get_image()
	rebuilt.save_png(OUT+"live-state-rebuilt.png")
	check(cached.get_data()==rebuilt.get_data(),"Retained pixels match forced floor/wall rebuild at same live state")
	var previous: Array=game.grid_view._surface_state().duplicate(true)
	room.airlock_cycle={"phase":"flooding","elapsed":1.0}
	check(previous!=game.grid_view._surface_state(),"Chamber water still invalidates its floor")
	previous=game.grid_view._surface_state().duplicate(true)
	room.rotation=1
	check(previous!=game.grid_view._surface_state(),"Rotation still invalidates structural state")
	room.rotation=0;room.fire=0.0;room.airlock_cycle={"phase":"dry","elapsed":0.0}
	var blocked_cell:=cell+Vector2i.UP
	game.drone_fleet.sites[blocked_cell]=game.drone_fleet.Sites.make_site("mining",2)
	game.drone_fleet.sites[blocked_cell].discovered=true
	game._refresh_all()
	var panel
	for node in game.find_children("*","VBoxContainer",true,false):
		if node.get_script()==preload("res://scripts/airlock_panel.gd"): panel=node;break
	check(panel!=null,"Airlock inspector exists")
	if panel!=null:
		panel.refresh()
		check(panel.cycle_status.text.contains("resource deposit at (20, 18)"),"Inspector identifies the actual exterior obstruction")
		check(panel.cycle_button.disabled,"Blocked exterior control is disabled")
	await rendered();await rendered()
	root.get_texture().get_image().save_png(OUT+"airlock-blocker-feedback.png")
	# An animated camera zoom scales retained layers instead of rebuilding them every frame,
	# and the settled frame matches a station that rebuilt on every zoom step.
	game.drone_fleet.sites.erase(blocked_cell)
	game.selected_room_cell=Vector2i(-1,-1)
	game._refresh_all()
	await rendered();await rendered()
	var zoom_start: float=game.grid_zoom
	var rebuilds_before: int=game.grid_view.floor_rebuilds
	game.camera_zoom_center=Vector2(cell)/40.0
	game.camera_zoom_target=clampf(zoom_start*0.6,game._minimum_map_zoom(),game.DEFAULT_GRID_ZOOM)
	var animated_frames:=0
	var saw_freeze:=false
	while game.camera_zoom_target>=0.0 and animated_frames<240:
		game._update_camera_zoom(1.0/60.0) # This fixture does not run main._process.
		await rendered()
		animated_frames+=1
		if game.grid_view.zoom_reuse_active: saw_freeze=true
	# Layers that only changed size repaint over a few frames after the zoom lands.
	var settle_frames:=0
	while (settle_frames<2 or game.grid_view.zoom_settling) and settle_frames<60:
		await rendered()
		settle_frames+=1
	check(not game.grid_view.zoom_settling,"The landed zoom finishes settling: "+str(settle_frames)+" frames")
	check(saw_freeze and animated_frames>=4 and not is_equal_approx(game.grid_zoom,zoom_start),"Animated zoom engages the retained-layer freeze")
	check(game.grid_view.floor_rebuilds-rebuilds_before<=2,"Animated zoom rebuilds floors at most at start and settle, not per frame: "+str(game.grid_view.floor_rebuilds-rebuilds_before)+" over "+str(animated_frames))
	var settled:=root.get_texture().get_image()
	game.grid_view.reuse_layers_while_zooming=false
	game.grid_view.surface_key=[];game.grid_view.env_below_key=[];game.grid_view.env_foundations_key=[];game.grid_view.env_terrain_key=[];game.grid_view.env_derelict_key=[];game.grid_view.room_frame_keys.clear()
	game.grid_view.queue_redraw()
	await rendered();await rendered();await rendered()
	check(settled.get_data()==root.get_texture().get_image().get_data(),"Settled zoom pixels match a full rebuild")
	game.grid_view.reuse_layers_while_zooming=true
	# A zoom-out from close up must keep the floor and walls of a room that starts off
	# screen: its mid-zoom frame matches a station that rebuilds on every step.
	var far:=cell+Vector2i(3,0)
	game._place_room("airlock",far,true);game.powered_room_cells[far]=true
	game.grid_view.room_light_levels[far]=1.0
	var zoom_center:=(Vector2(cell)+Vector2.ONE*0.5)/40.0
	var mid_zoom:=[]
	var rooms_area:=Rect2i()
	var revealed:=true
	for reuse in [true,false]:
		game.grid_view.reuse_layers_while_zooming=reuse
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM,true,zoom_center)
		await rendered();await rendered()
		game._restore_grid_view_center(zoom_center) # The scroll clamp settles a frame after the zoom.
		for i in range(3): await rendered()
		var started_off_screen: bool=not game.grid_view.visible_draw_rooms.has(game.occupied[far])
		game.camera_zoom_center=zoom_center
		game.camera_zoom_target=game._minimum_map_zoom()
		# The room must first enter the view on a frame after the zoom's first step.
		var first_visible_step:=-1
		for step in range(1,6):
			game._update_camera_zoom(1.0/60.0)
			await rendered()
			if first_visible_step<0 and game.grid_view.visible_draw_rooms.has(game.occupied[far]): first_visible_step=step
		revealed=revealed and started_off_screen and first_visible_step>=2
		mid_zoom.append(root.get_texture().get_image())
		# Both rooms and the risers above them, clear of the panels that overlap the map.
		var cell_px: float=game.get_cell_size()
		var to_screen: Transform2D=game.grid_view.get_viewport().get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()
		var map_rect: Rect2=game.grid_scroll.get_viewport().get_stretch_transform()*game.grid_scroll.get_global_rect()
		rooms_area=Rect2i((to_screen*Rect2(Vector2(cell)*cell_px,Vector2(4,1)*cell_px)).grow(24.0).intersection(map_rect))
		game.camera_zoom_target=-1.0
		await rendered();await rendered()
	mid_zoom[0].save_png(OUT+"zoom-out-reveal-reused.png")
	mid_zoom[1].save_png(OUT+"zoom-out-reveal-rebuilt.png")
	check(revealed,"The far room starts off screen and enters the view mid-zoom")
	var strong:=0
	var sampled:=0
	for y in range(rooms_area.position.y,rooms_area.end.y,2):
		for x in range(rooms_area.position.x,rooms_area.end.x,2):
			sampled+=1
			var a: Color=mid_zoom[0].get_pixel(x,y)
			var b: Color=mid_zoom[1].get_pixel(x,y)
			if absf(a.r-b.r)+absf(a.g-b.g)+absf(a.b-b.b)>0.4: strong+=1
	print("ZOOM REVEAL: area=",rooms_area," strongly differing sampled pixels=",strong," of ",sampled)
	check(sampled>2000 and strong*100<sampled,"A room revealed by a zoom-out keeps its shell mid-zoom: "+str(strong)+" of "+str(sampled)+" sampled pixels differ strongly")
	print("LIVE SURFACE RETENTION: ","PASS" if failures==0 else "FAIL"," failures=",failures)
	quit(0 if failures==0 else 1)
