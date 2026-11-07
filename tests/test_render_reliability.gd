extends SceneTree
var failures := 0
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func run():
	preload("res://scripts/title_settings.gd").save_path="user://render-reliability.cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://render-reliability.meta";game.run_save_path="user://render-reliability.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.crew_comms.minimize();game.crew_comms.set_process(false);game.set_process(false);game.tick_timer.stop();game.paused=true
	var view=game.grid_view.cryo_view
	var wards: Array=[{}]
	for ward in game.wrecks.values():
		if ward.kind in ["cryo","charging"]:wards.append(game.Architects.ward_for_display(game,ward))
	for q in range(4):
		for ward in wards:
			view.reuse_recovery_geometry=false;view.recovery=ward;view.layout.clear()
			view.configure_embedded(q,[0,2],false,2.5,[3])
			var expected: Dictionary={"layout":view.layout.duplicate(true),"props":view.props.duplicate(true),"edges":view.edges.duplicate(true)}
			view.reuse_recovery_geometry=true;view.configured_geometry.clear();view.layout.clear()
			view.configure_embedded(q,[0,2],false,2.5,[3])
			view.layout.clear();view.configure_embedded(q,[0,2],true,9.5,[3])
			check(expected=={"layout":view.layout,"props":view.props,"edges":view.edges},"Cached geometry matches original q%d, pods%d"%[q,ward.get("pods",[]).size()])
			check(view.machine_clock==9.5 and view.operating,"Clock and operating state remain live")
	var old_revision: int=preload("res://scripts/room_layout_store.gd").revision
	preload("res://scripts/room_layout_store.gd").revision=old_revision+1
	view.configure_embedded(0,[],false,0,[])
	check(view.configured_revision==old_revision+1,"Layout revision invalidates cache")
	preload("res://scripts/room_layout_store.gd").revision=old_revision
	for zoom in [game.DEFAULT_GRID_ZOOM,game.DEFAULT_GRID_ZOOM*0.25]:
		var label: String="near" if zoom==game.DEFAULT_GRID_ZOOM else "wide"
		game._set_grid_zoom(zoom);game._center_grid_on_station_now()
		for i in range(30):await process_frame
		view.reuse_recovery_geometry=false;game.grid_view.cull_room_drawing=false;game.grid_view.queue_redraw()
		for i in range(3):await process_frame
		await RenderingServer.frame_post_draw
		var reference:=root.get_texture().get_image()
		view.reuse_recovery_geometry=true;game.grid_view.cull_room_drawing=true;game.grid_view.queue_redraw()
		for i in range(3):await process_frame
		await RenderingServer.frame_post_draw
		var actual:=root.get_texture().get_image()
		reference.save_png("res://output/render-reference-%s.png"%label);actual.save_png("res://output/render-optimized-%s.png"%label)
		check(reference.get_data()==actual.get_data(),"Native cache/culling pixel parity "+label)
	game.queue_free();await process_frame
	print("RENDER RELIABILITY: %d failures"%failures);quit(1 if failures else 0)
