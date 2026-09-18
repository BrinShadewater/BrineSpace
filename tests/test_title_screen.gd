extends SceneTree
const ArchitectPicker = preload("res://scripts/architect_selection.gd")
const ButtonStyle = preload("res://scripts/title_button_style.gd")

var failures := 0
# The title and the game it opens must never write the player's progress or checkpoint. This
# test used to save its seeded codex state over user://brine_save.json on every native run,
# replacing real discovered and stabilized patterns and unlocked blueprints.
const TEST_META := "user://title_screen_test.meta"
const TEST_LOOP := "user://title_screen_test.loop"

func _init() -> void:
	call_deferred("_run")

func _check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _run() -> void:
	var test_preferences = preload("res://scripts/title_settings.gd")
	test_preferences.save_path = "user://brine_settings_test.cfg"
	test_preferences.reduced_motion = false
	var scene := load("res://scenes/title_screen.tscn") as PackedScene
	_remove_test_saves()
	var title = scene.instantiate()
	title.meta_state.save_path = TEST_META
	title.run_save_path = TEST_LOOP
	node_added.connect(_isolate_game_saves)
	root.add_child(title)
	current_scene = title
	await create_timer(0.5).timeout
	_check(title.layout_button.position.y >= title.badges.position.y + title.badges.size.y, "Layout Studio sits below archive badges")
	_check(title.layout_button.get_parent()==title, "Layout Studio is outside central start controls")
	_check(title.cover.elapsed > 0.0, "Native cover must start animating")
	_check(title.start_button.has_focus(), "Start must receive keyboard focus")
	# A real mouse click must reach a styled button. Dropping focus on the press cancelled it:
	# Godot cancels a press whose control loses focus, so the button emitted button_down and
	# button_up and never pressed, and every menu in the game stopped answering the mouse while the
	# keyboard still worked (owner report, Sept 17).
	# A lambda captures an int by value, so the tally lives in an array the closure shares.
	var clicks: Array = []
	var probe := Button.new()
	probe.text = "CLICK PROBE"
	probe.position = Vector2(600, 500)
	probe.size = Vector2(240, 48)
	probe.custom_minimum_size = Vector2(240, 48)
	ButtonStyle.apply(probe, 240, 48)
	probe.pressed.connect(func(): clicks.append(1))
	title.add_child(probe)
	# A Control needs a frame or two before the viewport picks it up under the pointer.
	for i in range(5): await process_frame
	var to_window: Vector2 = Vector2(DisplayServer.window_get_size()) / root.get_visible_rect().size
	var at: Vector2 = probe.get_global_rect().get_center() * to_window
	for round in range(2):
		var motion := InputEventMouseMotion.new()
		motion.position = at
		motion.global_position = at
		Input.parse_input_event(motion)
		await process_frame
		if round == 0:
			_check(root.gui_get_hovered_control() == probe, "The probe button is under the pointer (hovered %s, probe rect %s, point %s)" % [str(root.gui_get_hovered_control()), probe.get_global_rect(), at])
		for down in [true, false]:
			var click := InputEventMouseButton.new()
			click.button_index = MOUSE_BUTTON_LEFT
			click.position = at
			click.global_position = at
			click.pressed = down
			Input.parse_input_event(click)
			for i in range(3): await process_frame
	_check(clicks.size() == 2, "A styled button answers repeated mouse clicks (got %d of 2)" % clicks.size())
	_check(not probe.has_focus() and is_zero_approx(ButtonStyle._focus().border_color.a), "A clicked button keeps no focus ring")
	probe.queue_free()
	await process_frame

	var first: float = title.cover.character.position.y
	await create_timer(0.8).timeout
	_check(first != title.cover.character.position.y, "Character must float independently")
	for dimensions in [Vector2i(1280, 720), Vector2i(1600, 900), Vector2i(2560, 1440)]:
		root.size = dimensions
		await create_timer(0.2).timeout
		_check(absf(title.cover.size.x / title.cover.size.y - title.COVER_RATIO) < 0.001, "Cover aspect ratio must be preserved")
		_check(title.controls.position.y + title.controls.size.y <= title.size.y, "Controls must remain visible")
		var bar_center: float = (title.cover.position.y + title.cover.size.y + title.size.y) * 0.5
		_check(absf((title.badges.position.y + title.layout_button.position.y + title.layout_button.size.y) * 0.5 - bar_center) < 1.0, "Archive and studio group must center in the footer")
		_check(absf(title.controls.position.y + title.controls.size.y * 0.5 - bar_center) < 1.0, "Primary actions must share the footer center")
		_check(title.quit_button.position.y > title.settings_button.position.y, "Quit must remain below Settings")
		if dimensions.x == 1600:
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/title-screen.png")
	await create_timer(title.COVER_DURATION).timeout
	_check(title.cover.elapsed > title.COVER_DURATION, "Native cover must continue beyond one float cycle")
	root.size = Vector2i(1600, 900)
	# Seed in-memory progress only. Never write or unlock the player's save.
	title.meta_state.unlocked_room_ids = {"reactor": true, "hydroponics_bay": true, "obsolete_id": true}
	title.meta_state.doctrine_mastery = {"industry": 5}
	title.codex_button.pressed.emit()
	await create_timer(0.3).timeout
	_check(title.archive.room_ids.size() == 3, "Codex must show valid unlocked rooms plus the known core")
	_check(title.archive.visible_entries.size() == preload("res://scripts/room_database.gd").all_rooms().size(), "All rooms must have an entry")
	_check(not title.archive.room_ids.has("xeno_lab"), "Codex must not reveal locked rooms")
	for index in range(title.archive.room_ids.size()):
		_check(title.archive.visible_entries[index].known, "Recovered entries must precede hidden signals")
	_check(title.start_button.disabled, "Modal must block New Loop")
	title._start_game()
	_check(not title.starting, "Open archive must reject direct game activation")
	# A page must hand the title back even if its fade never finishes. Closing used to wait on the
	# fade tween's finished signal, and a killed tween left a transparent page over the title with
	# every button disabled behind it: the game looked alive and answered no clicks (owner report,
	# Sept 17).
	var stranded = title.archive
	stranded._close()
	await process_frame
	if stranded.transition != null: stranded.transition.kill()
	await create_timer(0.35).timeout
	_check(not is_instance_valid(title.archive) or title.archive == null, "A closed page lets go of the title")
	_check(not title.start_button.disabled and not title.codex_button.disabled, "The title takes its buttons back after a page closes")
	_check(not is_instance_valid(stranded), "The page frees itself even with its fade killed")
	title.codex_button.pressed.emit()
	await create_timer(0.3).timeout
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/title-codex.png")
	title.archive.search.text = "reactor"
	title.archive.search.text_changed.emit("reactor")
	_check(title.archive.room_ids == ["reactor"], "Codex search must filter recovered rooms")
	title.archive.search.text = "xeno lab"
	title.archive.search.text_changed.emit("xeno lab")
	_check(title.archive.visible_entries.is_empty(), "Search must not expose a hidden room name")
	var reset = title.archive.find_child("ResetCodexSearch", true, false)
	_check(reset != null, "An empty search must offer a reset action")
	reset.pressed.emit()
	_check(title.archive.search.text.is_empty() and not title.archive.visible_entries.is_empty(), "Reset must restore archive entries")
	title.archive.search.text = ""
	title.meta_state.discovered_synergy_ids = {"closed_air_loop": true}
	title.meta_state.stabilized_synergy_ids.clear()
	title.archive.codex_tabs.current_tab = 1
	await create_timer(0.3).timeout
	_check(title.archive.visible_entries.size() == preload("res://scripts/synergy_manager.gd").all_synergies().size(), "Every synergy must have an entry")
	title.archive.codex_filter.select(1)
	title.archive.codex_filter.item_selected.emit(1)
	_check(title.archive.visible_entries.size() == 1 and title.archive.visible_entries[0].id == "closed_air_loop", "Discovered filter must respect saved knowledge")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/title-synergies.png")
	title.archive.codex_filter.select(2)
	title.archive.codex_filter.item_selected.emit(2)
	for entry in title.archive.visible_entries:
		_check(not entry.known and not entry.clue.is_empty(), "Hidden synergies must have clues")
		_check(entry.title != entry.data.name, "Hidden synergy names must remain concealed")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/title-hidden-synergies.png")
	title.archive.close_button.pressed.emit()
	await create_timer(0.2).timeout
	_check(title.archive == null, "Closing must release the active modal after fading")
	_check(title.codex_button.has_focus(), "Closing Codex restores badge focus")
	title.progression_button.pressed.emit()
	await create_timer(0.3).timeout
	_check(title.archive.mode == "progression", "Progression badge must open progression")
	_check(title.archive.meta_state.get_doctrine_rank("industry") == 2, "Progression must use saved mastery thresholds")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/title-progression.png")
	var cancel := InputEventAction.new()
	cancel.action = "ui_cancel"
	cancel.pressed = true
	title.archive._unhandled_key_input(cancel)
	await create_timer(0.2).timeout
	_check(not title.start_button.disabled, "Closing progression restores New Loop")
	title.start_button.grab_focus()
	title.settings_button.pressed.emit()
	await create_timer(0.3).timeout
	_check(title.archive.mode == "settings", "Settings button must open Settings")
	_check(title.archive.find_child("Resolution", true, false) != null, "Settings must offer resolution")
	_check(title.archive.find_child("MasterVolume", true, false) != null, "Settings must offer volume")
	var music_volume = title.archive.find_child("MusicVolume", true, false)
	_check(music_volume != null, "Settings must offer independent music volume")
	for setting in ["EffectsVolume","AmbienceVolume"]:
		var control = title.archive.find_child(setting,true,false)
		_check(control != null,"Settings must offer "+setting)
		if control != null: control.value = 62
	_check(is_equal_approx(test_preferences.effects_volume,0.62) and is_equal_approx(test_preferences.ambience_volume,0.62),"Audio sliders update both preferences")
	if music_volume != null:
		music_volume.value = 37
		_check(is_equal_approx(test_preferences.music_volume,0.37), "Music slider changes soundtrack preference")
	var preferences = preload("res://scripts/title_settings.gd")
	preferences.save_path = "user://brine_settings_test.cfg"
	var original_volume := AudioServer.get_bus_volume_linear(0)
	var volume = title.archive.find_child("MasterVolume", true, false)
	volume.value = 37
	var saved := ConfigFile.new()
	_check(saved.load(preferences.save_path) == OK, "Settings must persist to disk")
	_check(is_equal_approx(float(saved.get_value("audio", "volume", -1)), 0.37), "Volume setting must be persisted")
	var original_size := root.size
	var original_vsync := DisplayServer.window_get_vsync_mode()
	var resolution = title.archive.find_child("Resolution", true, false)
	resolution.select(0)
	resolution.item_selected.emit(0)
	await create_timer(0.2).timeout
	_check(root.size == Vector2i(1280, 720), "Resolution selection must resize the window")
	title.archive.find_child("SettingsPanel", true, false)._keep_display()
	await process_frame
	var vsync = title.archive.find_child("VSync", true, false)
	vsync.button_pressed = not vsync.button_pressed
	var expected_vsync: bool = vsync.button_pressed
	_check(saved.load(preferences.save_path) == OK, "Display settings must persist")
	_check(saved.get_value("display", "size") == Vector2i(1280, 720), "Saved resolution must match selection")
	_check(saved.get_value("display", "vsync") == expected_vsync, "V-sync toggle must persist")
	var motion = title.archive.find_child("ReducedMotion", true, false)
	motion.button_pressed = true
	var paused_time: float = title.cover.elapsed
	var paused_position: Vector2 = title.cover.character.position
	await create_timer(0.25).timeout
	_check(title.cover.elapsed == paused_time and title.cover.character.position == paused_position, "Reduced motion must freeze ambient layers")
	_check(saved.load(preferences.save_path) == OK and saved.get_value("accessibility", "reduced_motion", false), "Reduced motion must persist")
	AudioServer.set_bus_volume_linear(0, 0.8)
	preferences.initialized = false
	preferences.initialize(root)
	_check(is_equal_approx(AudioServer.get_bus_volume_linear(0), 0.37), "Saved volume must restore on initialization")
	_check(preferences.reduced_motion, "Reduced motion must restore on initialization")
	motion.button_pressed = false
	await create_timer(0.15).timeout
	_check(title.cover.elapsed > paused_time, "Ambient animation must resume when reduced motion is disabled")
	root.size = original_size
	preferences.window_size = original_size
	DisplayServer.window_set_vsync_mode(original_vsync)
	AudioServer.set_bus_volume_linear(0, original_volume)
	DirAccess.remove_absolute(preferences.save_path)
	preferences.save_path = preferences.PATH
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/title-settings.png")
	title.archive.close_button.pressed.emit()
	await create_timer(0.2).timeout
	_check(title.settings_button.has_focus(), "Closing Settings restores its button focus")
	if "--menu-only" in OS.get_cmdline_user_args():
		_remove_test_saves()
		print("TITLE SCREEN: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
		quit(failures)
		return
	title.start_button.grab_focus()
	var press := InputEventAction.new()
	press.action = "ui_accept"
	press.pressed = true
	Input.parse_input_event(press)
	await create_timer(0.2).timeout
	press = InputEventAction.new()
	press.action = "ui_accept"
	press.pressed = false
	Input.parse_input_event(press)
	await create_timer(1.0).timeout
	_check(current_scene == title and title.archive is ArchitectPicker, "Keyboard New Loop opens architect selection")
	if title.archive is ArchitectPicker:
		title.archive.confirm.pressed.emit()
		# Threaded scene loading depends on asset-cache and disk speed, not a fixed second.
		var deadline:=Time.get_ticks_msec()+20000
		while current_scene==title and Time.get_ticks_msec()<deadline:
			await create_timer(0.1).timeout
	_check(current_scene != title, "Confirming architect must open the game")
	if current_scene != title:
		_check(current_scene.scene_file_path == "res://scenes/main.tscn", "Start must open the existing game scene")
		_check(current_scene.get("doctrine_layer") != null, "Game script must load successfully")
		if current_scene.get("doctrine_layer") != null:
			_check(not current_scene.doctrine_layer.visible, "Retired doctrine selection stays hidden")
			_check(current_scene.running, "Confirmed architect starts the open expedition")
	print("TITLE SCREEN: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	if is_instance_valid(current_scene): current_scene.queue_free()
	_remove_test_saves()
	var music := root.get_node_or_null("StationMusic")
	if music != null: music.queue_free()
	await process_frame
	await create_timer(0.15).timeout
	quit(failures)

func _isolate_game_saves(node: Node) -> void:
	# The game scene the title opens is redirected before its _ready can load or save anything.
	if node.scene_file_path == "res://scenes/main.tscn":
		node.meta.save_path = TEST_META
		node.run_save_path = TEST_LOOP

func _remove_test_saves() -> void:
	for path in [TEST_META, TEST_META + ".bak", TEST_META + ".tmp", TEST_LOOP, TEST_LOOP + ".bak", TEST_LOOP + ".tmp", TEST_LOOP + ".comms.json"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
