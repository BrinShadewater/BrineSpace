extends SceneTree
var failures := 0
var game
func _initialize() -> void: run.call_deferred()
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func escape() -> void:
	for down in [true, false]:
		var event := InputEventKey.new()
		event.keycode = KEY_ESCAPE
		event.pressed = down
		Input.parse_input_event(event)
		await process_frame
	for i in range(3): await process_frame
func run() -> void:
	if DisplayServer.get_name() == "headless": quit(2); return
	if not preload("res://tests/test_synergy_geometry.gd").configure_test_window(root).get("secondary_available", false): quit(2); return
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\", "/").trim_suffix("/")
	if expected.is_empty() or expected.to_lower() != ProjectSettings.globalize_path("user://").replace("\\", "/").trim_suffix("/").to_lower(): quit(2); return
	preload("res://scripts/title_settings.gd").reduced_motion = true
	root.size = Vector2i(1600,900)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://tutorial-gameplay.meta"
	game.run_save_path = "user://tutorial-gameplay.loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.crew_comms.opening_enabled = false
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	for initially_paused in [false, true]:
		game._set_paused(initially_paused)
		game._open_menu()
		check(game.menu_open and game.paused and game.tick_timer.paused, "Menu pauses the real expedition")
		var cycle_before: int = game.cycle
		var resources_before: Dictionary = game.resources.duplicate(true)
		var hand_before: Array = game.hand.duplicate()
		var selection_before: String = game.selected_card_id
		game._open_shared_menu("settings")
		var archive = game.menu_archive
		var panel = archive.find_child("SettingsPanel", true, false)
		panel.tabs["TUTORIAL GUIDE"].pressed.emit()
		for i in range(4): await process_frame
		var guide: Control = panel.pages["TUTORIAL GUIDE"]
		var picture = guide.get_child(4).get_child(0).get_child(3)
		picture._enlarge()
		for i in range(4): await process_frame
		check(is_instance_valid(picture.expanded_dialog) and picture.expanded_dialog.visible, "Illustration opens above the expedition menu")
		await escape()
		check(not is_instance_valid(picture.expanded_dialog) and is_instance_valid(game.menu_archive), "First Escape closes only the picture")
		check(game.paused and game.tick_timer.paused, "Picture exit does not resume the station")
		await escape()
		check(not is_instance_valid(game.menu_archive) and game.menu_open and game.menu_center.visible, "Second Escape returns to pause menu")
		check(game.cycle == cycle_before and game.resources == resources_before and game.hand == hand_before, "Reading guide does not advance economy or draft")
		await escape()
		check(not game.menu_open and not game.menu_layer.visible, "Third Escape returns to station")
		check(game.paused == initially_paused and game.tick_timer.paused == initially_paused, "Original running or paused state is restored")
		check(game.selected_card_id == selection_before and not game._gameplay_input_blocked(), "Selection and gameplay input return")
	game.set_process(false)
	game.tick_timer.stop()
	current_scene = null
	game.free()
	await process_frame
	var music := root.get_node_or_null("StationMusic")
	if music != null: music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	print("Tutorial gameplay: %s (%d failures)" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(0 if failures == 0 else 1)
