extends SceneTree
## Native lifecycle evidence. Use an isolated profile; --user-dir must match the
## resolved directory before a scene is instantiated or any save is written.
var options := {}
var results := []
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--") and "=" in arg: options[arg.get_slice("=", 0).trim_prefix("--")] = arg.substr(arg.find("=") + 1)
	call_deferred("run")
func run() -> void:
	if str(options.get("user-dir", "")).replace("\\", "/").simplify_path() != OS.get_user_data_dir().replace("\\", "/").simplify_path():
		push_error("Transition probe refused: profile mismatch"); quit(1); return
	if DisplayServer.get_name() == "headless": quit(2); return
	var input: String = options.get("save", "")
	if not FileAccess.file_exists(input): quit(3); return
	root.size = Vector2i(1600, 900)
	root.child_entered_tree.connect(func(node):
		if node.get_script() != null and node.get_script().resource_path == "res://scripts/main.gd":
			node.run_save_path = "user://transition.loop"
			node.meta.save_path = "user://transition.meta"
	)
	var title = load("res://scenes/title_screen.tscn").instantiate()
	root.add_child(title); current_scene = title
	for iteration in range(int(options.get("transitions", "10"))):
		if DirAccess.copy_absolute(input, ProjectSettings.globalize_path("user://transition.loop")) != OK: quit(4); return
		title.run_save_path = "user://transition.loop"
		title._continue_loop()
		var deadline := Time.get_ticks_msec() + 90000
		var game
		while Time.get_ticks_msec() < deadline:
			await process_frame
			for child in root.get_children():
				if child.has_method("finish_after_scene_change"):
					child.type_skipped = true
					if not child.continue_button.disabled: child.continue_button.pressed.emit()
			game = current_scene
			if game != null and game != title and game.get("startup_complete") == true and game.process_mode != Node.PROCESS_MODE_DISABLED:
				var loading := false
				for child in root.get_children():
					if child.has_method("finish_after_scene_change"): loading = true
				if not loading: break
		if game == null or game == title or game.get("startup_complete") != true:
			push_error("Continue did not finish"); quit(5); return
		game.run_save_path = "user://transition.loop"
		game.crew_comms.minimize()
		game._set_paused(true, false)
		var settled := 0
		deadline = Time.get_ticks_msec() + 15000
		while settled < 30 and Time.get_ticks_msec() < deadline:
			await process_frame
			settled = settled + 1 if not game.camera_zoom_moving and not game.grid_view.settle_backlog and game.grid_view.pending_layers.is_empty() else 0
		if settled < 30: push_error("Station did not settle"); quit(6); return
		await RenderingServer.frame_post_draw
		var row := {"iteration": iteration + 1, "rooms": game.placed_rooms.size(), "texture_mb": Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED) / 1048576.0,
			"static_mb": Performance.get_monitor(Performance.MEMORY_STATIC) / 1048576.0, "nodes": Performance.get_monitor(Performance.OBJECT_NODE_COUNT), "orphans": Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT)}
		results.append(row)
		print("TRANSITION ", JSON.stringify(row))
		game._menu_return_title()
		deadline = Time.get_ticks_msec() + 15000
		while Time.get_ticks_msec() < deadline:
			await process_frame
			title = current_scene
			if title != null and title.has_method("_continue_loop"): break
		if title == null or not title.has_method("_continue_loop"): quit(7); return
	var growth := 100.0 * (float(results.back().texture_mb) / float(results[0].texture_mb) - 1.0)
	var report := {"debug": OS.is_debug_build(), "transitions": results, "texture_growth_percent": growth, "texture_growth_pass": growth <= 5.0}
	var file := FileAccess.open(options["out"], FileAccess.WRITE)
	file.store_string(JSON.stringify(report)); file.close()
	print("TRANSITION PROBE COMPLETE growth=", growth)
	# Match the application's normal shutdown: stop processing before draining audio.
	for child in root.get_children(): child.process_mode = Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	await create_timer(0.2, true, false, true).timeout
	quit(0 if growth <= 5.0 else 8)
