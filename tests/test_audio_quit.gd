extends SceneTree
## Native --script test_audio_quit.gd -- --mode=title|game. Uses isolated fixture saves.
func _init() -> void: call_deferred("run")
func run() -> void:
	var mode := "title"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--mode="): mode = arg.trim_prefix("--mode=")
	preload("res://scripts/title_settings.gd").save_path = "user://quit_fixture.cfg"
	var scene = load("res://scenes/main.tscn" if mode == "game" else "res://scenes/title_screen.tscn").instantiate()
	if mode == "game":
		scene.meta.save_path = "user://quit_fixture.meta"
		scene.run_save_path = "user://quit_fixture.loop"
	root.add_child(scene)
	current_scene = scene
	if mode == "game":
		while not scene.startup_complete: await process_frame
	await create_timer(0.5).timeout
	if mode == "game":
		scene._menu_quit_game()
		if not FileAccess.file_exists(scene.run_save_path):
			push_error("Save & Quit did not record the loop")
			quit(1)
			return
	else:
		scene.quit_button.pressed.emit()
	if not root.get_meta("audio_quitting",false):
		push_error("Normal quit did not enter audio cleanup")
		quit(1)
		return
	print("AUDIO QUIT PASS: "+mode)
