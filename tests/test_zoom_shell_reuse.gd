extends SceneTree
var game
var failures := 0
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(5): await process_frame
	await RenderingServer.frame_post_draw
func run() -> void:
	var prefix := "user://zoom_shell_%d" % OS.get_process_id()
	preload("res://scripts/title_settings.gd").save_path = prefix+".cfg"
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized = true
	var index := 0
	for id in ["reactor","life_support","hydroponics_bay","storage_bay","crew_hab"]:
		game._place_room(id,Vector2i(17+index,19),true)
		index += 1
	game._set_paused(true,false)
	game.grid_view.cull_room_drawing = false
	game._refresh_all()
	await settle()
	var counts := {}
	for room in game.placed_rooms:
		var view = game.grid_view._bill_room_view(room)
		if view != null: counts[view] = view.shell_queue_builds
	for zoom in [0.85,0.65,1.0]:
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*zoom)
		await settle()
		for view in counts:
			if view.shell_queue_builds != counts[view]:
				failures += 1
				push_error("Zoom rebuilt room-space wall assembly")
	var built := 0
	for count in counts.values(): built += count
	if built==0: failures += 1
	for suffix in [".cfg",".meta",".meta.bak",".loop",".loop.bak"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("ZOOM SHELL REUSE: ",counts.size()," room views, three zoom transitions, ",failures," failures")
	quit(1 if failures else 0)
