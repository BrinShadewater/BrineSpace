extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
const Save = preload("res://scripts/run_save.gd")
var failures := 0

func _init() -> void:
	call_deferred("_run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func key(code: int) -> InputEventKey:
	var event := InputEventKey.new()
	event.keycode = code
	event.pressed = true
	return event

func _run() -> void:
	Preferences.save_path = "user://menu_recovery_test.cfg"
	Preferences.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://menu_recovery_test.json"
	game.run_save_path = "user://menu_recovery_test.loop"
	root.add_child(game)
	current_scene = game
	await process_frame
	game._set_paused(true, false)
	game._open_overlay_settings()
	await process_frame
	check(game._gameplay_input_blocked(), "Overlay settings must block station input")
	var archive = game.menu_archive
	var settings = archive.find_child("SettingsPanel", true, false)
	var before := root.size
	var old_saved_size := Preferences.window_size
	Preferences.save(root)
	settings._preview_display(func() -> void: root.size = Vector2i(1280,720))
	check(not settings.display_previous.is_empty(), "Display preview must await confirmation")
	if OS.has_feature("editor") and DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/display-confirmation.png")
	var config := ConfigFile.new()
	config.load(Preferences.save_path)
	check(config.get_value("display", "size") == old_saved_size, "Display preview must not persist before confirmation")
	settings.display_seconds = 1
	settings.display_timer.timeout.emit()
	await process_frame
	check(root.size == before, "Expired display preview must restore the previous window")
	settings = archive.find_child("SettingsPanel", true, false)
	settings._preview_display(func() -> void: root.size = Vector2i(1280,720))
	await create_timer(0.1).timeout
	Input.parse_input_event(key(KEY_ESCAPE))
	await process_frame
	check(root.size == before, "Cancel must revert the display")
	settings._preview_display(func() -> void: root.size = Vector2i(1280,720))
	archive.show_section("codex")
	await process_frame
	check(root.size == before, "Leaving the settings panel must revert an unconfirmed display")
	archive.show_section("settings")
	await process_frame
	settings = archive.find_child("SettingsPanel", true, false)
	settings._preview_display(func() -> void: root.size = Vector2i(1280,720))
	settings._keep_display()
	await process_frame
	config.load(Preferences.save_path)
	if DisplayServer.get_name() != "headless":
		check(config.get_value("display", "size") == Vector2i(1280,720), "Keep Changes must persist the new display")
	else:
		# The headless DisplayServer never applies window resizes; Preferences.save
		# re-reads the live size, so the persisted value is checked natively only.
		check(config.get_value("display", "size") == Preferences.window_size, "Keep Changes persists the live window size")
	settings.find_child("BindPause", true, false).pressed.emit()
	root.push_input(key(KEY_J), true)
	check(settings.binding_action == "Pause" and settings.feedback.text.contains("KEY IN USE"), "Binding conflicts must be explained without overwriting another action")
	root.push_input(key(KEY_P), true)
	await process_frame
	check(Preferences.keys["Pause"] == KEY_P, "An available key must bind the selected action")
	Preferences.initialized = false
	Preferences.initialize(root)
	check(Preferences.keys["Pause"] == KEY_P, "Bindings must survive preference reload")
	settings._defaults("AUDIO")
	await process_frame
	check(not Preferences.muted and is_equal_approx(AudioServer.get_bus_volume_linear(0), 1.0), "Audio defaults must restore mute and volume")
	archive._close()
	await create_timer(0.2).timeout
	check(game.running and not game.doctrine_layer.visible, "Settings Back must return to the active station")

	game._close_menu()
	game._set_paused(false, false)
	game._unhandled_input(key(KEY_P))
	check(game.paused, "Rebound pause key must drive the real game handler")
	# This also runs in the exported executable, covering real paid construction
	# and checkpoint restoration of the architect's in-flight job outside the checkout.
	game.hand.assign(["solar_array"])
	game.selected_card_id = "solar_array"
	game.selected_rotation = 2
	game._on_grid_clicked(Vector2i(19,20))
	check(game.drone_fleet.reserved(Vector2i(19,20)), "Packaged game must queue paid construction")
	var paid_resources: Dictionary = game.resources.duplicate(true)
	check(Save.write(game, game.run_save_path) == OK, "In-flight construction checkpoint must write")
	check(Save.restore(game, Save.read(game.run_save_path)), "In-flight construction checkpoint must restore")
	game.paused = false
	for frame in range(1200):
		game._process(0.1)
		if game.occupied.has(Vector2i(19,20)): break
	game.paused = true
	check(game.occupied.has(Vector2i(19,20)) and game.resources == paid_resources, "Restored construction must finish without charging twice")
	game._advance_cycle()
	check(game.cycle == 1 and game.powered_room_cells.has(Vector2i(19,20)), "Constructed room must participate in the next economy cycle")
	game._open_menu()
	game._open_shared_menu("settings")
	await process_frame
	settings = game.menu_archive.find_child("SettingsPanel", true, false)
	settings._defaults("CONTROLS & PAUSE")
	await process_frame
	check(Preferences.keys == Preferences.DEFAULT_KEYS and is_equal_approx(Preferences.zoom_sensitivity, 1.0), "Controls defaults must restore keys and zoom")
	Preferences.text_scale = 1.3
	settings._defaults("ACCESSIBILITY")
	await process_frame
	check(is_equal_approx(Preferences.text_scale, 1.0) and not Preferences.reduced_motion, "Accessibility defaults must restore text and motion")
	game.menu_archive._close()
	await create_timer(0.2).timeout
	game.run_save_path = "user://menu_recovery_missing_dir/checkpoint"
	game._menu_return_title()
	check(current_scene == game and game.menu_save_feedback.text.begins_with("SAVE FAILED"), "Failed Save & Return must retain the game and show the reason")
	game._menu_quit_game()
	check(current_scene == game, "Failed Save & Quit must retain the game")
	game.run_save_path = "user://menu_recovery_test.loop"
	game._close_menu()
	game._show_reboot_summary("Menu recovery fixture.", false)
	game._open_overlay_settings()
	await process_frame
	game.menu_archive._close()
	await create_timer(0.2).timeout
	check(game.summary_layer.visible, "Settings Back must restore the summary")
	game.queue_free()
	await process_frame
	var corrupt := FileAccess.open("user://menu_recovery_test.loop", FileAccess.WRITE)
	corrupt.store_string("damaged")
	corrupt.close()
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.run_save_path = "user://menu_recovery_test.loop"
	root.add_child(title)
	current_scene = title
	await process_frame
	check(not title.continue_button.visible and title.error_label.text.contains("CHECKPOINT UNAVAILABLE"), "Broken checkpoints must have an explicit title error")
	for dimensions in [Vector2i(960,540), Vector2i(1024,768), Vector2i(1440,900), Vector2i(2560,1080)]:
		root.size = dimensions
		await create_timer(0.2).timeout
		check(not title.error_label.text.is_empty() and title.error_label.is_visible_in_tree(), "Title errors must survive resizing")
		check(title.get_rect().encloses(title.controls.get_rect()), "Title actions must fit " + str(dimensions))
	title.about_button.pressed.emit()
	await process_frame
	check(title.archive.mode == "about", "Credits entry must open build information")
	title.archive.show_section("progression")
	await process_frame
	check(title.archive.mode == "progression", "Credits must share the archive navigation")
	title.archive._close()
	await create_timer(0.2).timeout
	for path in [Preferences.save_path, "user://menu_recovery_test.json", "user://menu_recovery_test.loop", "user://menu_recovery_test.loop.bak"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("MENU RECOVERY: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
