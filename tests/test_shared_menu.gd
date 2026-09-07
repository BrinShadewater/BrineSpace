extends SceneTree

const Preferences = preload("res://scripts/title_settings.gd")
const Save = preload("res://scripts/run_save.gd")
const SETTINGS_PATH := "user://shared_menu_test.cfg"
const SAVE_PATH := "user://shared_menu_test.loop"
const META_PATH := "user://shared_menu_test_meta.json"
var failures := 0

func _init() -> void:
	call_deferred("_run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func control(panel: Node, id: String):
	return panel.find_child(id, true, false)

func check_modal_focus(scope: Node) -> void:
	for reverse in [false, true]:
		for index in range(28):
			var key := InputEventKey.new()
			key.keycode = KEY_TAB
			key.pressed = true
			key.shift_pressed = reverse
			root.push_input(key, true)
			await process_frame
			var focused := root.gui_get_focus_owner()
			check(focused != null and scope.is_ancestor_of(focused), "Tab traversal must remain inside " + scope.name)
	for action in ["ui_up", "ui_down", "ui_left", "ui_right"]:
		for index in range(8):
			var direction := InputEventAction.new()
			direction.action = action
			direction.pressed = true
			root.push_input(direction, true)
			await process_frame
			var focused := root.gui_get_focus_owner()
			check(focused != null and scope.is_ancestor_of(focused), "Directional focus must remain inside " + scope.name)

func _run() -> void:
	Preferences.save_path = SETTINGS_PATH
	Preferences.initialized = false
	Preferences.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = META_PATH
	game.run_save_path = SAVE_PATH
	root.add_child(game)
	current_scene = game
	await process_frame
	check(game.running and not game.doctrine_layer.visible, "New loop skips retired doctrine modal")
	game._set_paused(false, false)
	game._toggle_journal()
	await check_modal_focus(game.journal_layer)
	game._toggle_journal()
	check(game.journal_button.has_focus() and not game.paused, "Journal must restore focus and the running state")
	game._open_menu()
	await check_modal_focus(game.menu_center)
	check(game.menu_open and game.paused, "Pause menu must pause the station")
	var settings_button = control(game.menu_center, "Settings")
	settings_button.grab_focus()
	settings_button.pressed.emit()
	await process_frame
	var panel = game.menu_archive
	await check_modal_focus(panel)
	check(panel.mode == "settings" and panel.in_game, "In-game Settings must use the shared panel")
	check(not game.menu_center.visible, "Shared panel must hide pause-menu controls")
	if DisplayServer.get_name() != "headless" and "--window-modes" in OS.get_cmdline_user_args():
		var windowed_size := root.size
		var window_mode = control(panel, "WindowMode")
		window_mode.select(1)
		window_mode.item_selected.emit(1)
		await create_timer(0.3).timeout
		check(root.borderless and root.size == DisplayServer.screen_get_size(root.current_screen), "Borderless fullscreen must fill the current display")
		check(control(panel, "Resolution").disabled, "Borderless fullscreen must disable window-size selection")
		control(panel, "SettingsPanel")._keep_display()
		await process_frame
		Preferences.initialized = false
		Preferences.initialize(root)
		check(Preferences.get_window_mode(root) == 1 and Preferences.window_size == windowed_size, "Borderless mode must persist without overwriting the windowed resolution (mode %d, saved %s, expected %s)" % [Preferences.get_window_mode(root), Preferences.window_size, windowed_size])
		window_mode = control(panel, "WindowMode")
		window_mode.select(2)
		window_mode.item_selected.emit(2)
		await create_timer(0.3).timeout
		check(root.mode == Window.MODE_EXCLUSIVE_FULLSCREEN, "Exclusive fullscreen must remain available")
		control(panel, "SettingsPanel")._keep_display()
		await process_frame
		window_mode = control(panel, "WindowMode")
		window_mode.select(0)
		window_mode.item_selected.emit(0)
		await create_timer(0.3).timeout
		check(root.mode == Window.MODE_WINDOWED and not root.borderless and root.size == windowed_size, "Windowed mode must restore borders and the previous resolution")
		check(not control(panel, "Resolution").disabled, "Windowed mode must re-enable resolution selection")
		control(panel, "SettingsPanel")._keep_display()
		await process_frame
	control(panel, "FrameLimit").select(2)
	control(panel, "FrameLimit").item_selected.emit(2)
	check(Engine.max_fps == 60, "Frame limit must affect the engine")
	var original_volume := AudioServer.get_bus_volume_linear(0)
	control(panel, "MasterMute").button_pressed = true
	check(AudioServer.is_bus_mute(0) and is_equal_approx(AudioServer.get_bus_volume_linear(0), original_volume), "Mute must preserve the volume level")
	control(panel, "MuteUnfocused").button_pressed = true
	control(panel, "MasterMute").button_pressed = false
	Preferences._on_focus(false)
	check(AudioServer.is_bus_mute(0), "Focus loss must mute audio when enabled")
	Preferences._on_focus(true)
	check(not AudioServer.is_bus_mute(0), "Focus return must restore audio")
	control(panel, "ZoomSensitivity").value = 180
	control(panel, "InvertZoom").button_pressed = true
	control(panel, "PauseUnfocused").button_pressed = true
	control(panel, "TooltipDelay").value = 300
	control(panel, "MenuTextSize").value = 130
	check(is_equal_approx(Preferences.zoom_step(), -0.09), "Zoom options must produce the correct wheel step")
	check(panel.close_button.get_theme_font_size("font_size") > 16, "Panel text must resize live")
	var config := ConfigFile.new()
	check(config.load(SETTINGS_PATH) == OK, "Expanded settings must persist")
	check(config.get_value("controls", "invert_zoom", false), "Zoom direction must persist")
	check(is_equal_approx(config.get_value("accessibility", "tooltip_delay", 0.0), 0.3), "Tooltip delay must persist")
	if DisplayServer.get_name() != "headless":
		root.size = Vector2i(1600,900)
		await create_timer(0.3).timeout
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/shared-settings.png")
	control(panel, "NavigateCodex").pressed.emit()
	check(panel.mode == "codex" and not panel.visible_entries.is_empty(), "Shared navigation must open the live Codex")
	await check_modal_focus(panel)
	var find_key := InputEventKey.new()
	find_key.keycode = KEY_F
	find_key.pressed = true
	find_key.ctrl_pressed = true
	root.push_input(find_key, true)
	check(panel.search.has_focus(), "Ctrl+F must focus Codex search")
	panel.search.text = "reactor"
	panel.search.text_changed.emit("reactor")
	panel.codex_filter.select(1)
	panel.codex_filter.item_selected.emit(1)
	control(panel, "NavigateSettings").pressed.emit()
	control(panel, "NavigateCodex").pressed.emit()
	check(panel.search.text == "reactor" and panel.codex_filter.selected == 1, "Codex must preserve browsing state between sections")
	control(panel, "NavigateProgression").pressed.emit()
	check(panel.mode == "progression" and panel.meta_state == game.meta, "Progression must show the active saved meta state")
	panel._close()
	await create_timer(0.2).timeout
	check(game.menu_archive == null and game.menu_open and game.paused, "Back must return to the still-paused menu")
	check(settings_button.has_focus(), "Back must restore focus to the originating menu button")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/shared-pause-menu.png")
	game._close_menu()
	check(not game.paused, "Resume must restore the pre-menu running state")
	game._set_grid_zoom((game.MIN_GRID_ZOOM + game.DEFAULT_GRID_ZOOM) * 0.5)
	var before: float = game.grid_zoom
	var wheel := InputEventMouseButton.new()
	wheel.button_index = MOUSE_BUTTON_WHEEL_UP
	wheel.shift_pressed = true
	wheel.pressed = true
	game.grid_view._gui_input(wheel)
	check(is_equal_approx(game.grid_zoom, before - 0.09), "Station wheel input must use the saved sensitivity and inversion")
	game._notification(Control.NOTIFICATION_WM_WINDOW_FOCUS_OUT)
	check(game.paused, "Focus loss must pause the running station")
	game._open_menu()
	game._close_menu()
	check(game.paused, "Opening and closing the menu must preserve an already-paused station")
	check(game.menu_resume_button.text.contains("Paused"), "Return action must describe the preserved pause state")
	game._open_menu()
	game._menu_save_game()
	check(not Save.read(SAVE_PATH).is_empty(), "Unified menu must still save the loop")
	check(game.menu_save_feedback.text.begins_with("LOOP RECORDED"), "Save feedback must confirm the checkpoint beside the save action")
	check(game.menu_status_label.text.contains("Integrity"), "Saving must preserve the station status summary")
	game._menu_return_title()
	await create_timer(0.4).timeout
	var title = current_scene
	check(title.scene_file_path == "res://scenes/title_screen.tscn", "Return to Title must still work")
	Preferences.initialized = false
	Preferences.initialize(root)
	check(Engine.max_fps == 60 and Preferences.invert_zoom and Preferences.text_scale == 1.3, "Expanded settings must restore across scene transitions")
	title.settings_button.pressed.emit()
	await process_frame
	check(control(title.archive, "InvertZoom").button_pressed, "Title Settings must reflect in-game changes")
	title.archive._close()
	await create_timer(0.2).timeout
	if DisplayServer.get_name() != "headless" and "--window-modes" not in OS.get_cmdline_user_args():
		var hover := InputEventMouseMotion.new()
		hover.position = Vector2(5, 5)
		root.push_input(hover, true)
		await create_timer(0.5).timeout
		hover = InputEventMouseMotion.new()
		hover.position = title.codex_button.get_global_rect().get_center()
		root.push_input(hover, true)
		await create_timer(0.1).timeout
		check(not title.codex_button.has_meta("tooltip_layer"), "Menu tooltip must wait for its configured delay")
		await create_timer(0.35).timeout
		check(title.codex_button.has_meta("tooltip_layer"), "Menu tooltip must appear after its configured delay")
		hover = InputEventMouseMotion.new()
		hover.position = Vector2(5,5)
		root.push_input(hover, true)
		await process_frame
		check(not title.codex_button.has_meta("tooltip_layer"), "Leaving the button must dismiss its tooltip")
	for path in [SETTINGS_PATH, SAVE_PATH, SAVE_PATH + ".bak", SAVE_PATH + ".tmp", META_PATH]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("SHARED MENU: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
