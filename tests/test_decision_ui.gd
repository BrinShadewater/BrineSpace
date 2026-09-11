extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
const Saves = preload("res://scripts/run_save.gd")
var failures := 0
func _init() -> void:
	call_deferred("_run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _run() -> void:
	Preferences.save_path = "user://decision_ui_test.cfg"
	Preferences.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://decision_ui_test.json"
	game.run_save_path = "user://decision_ui_test.loop"
	game.meta.discovered_synergy_ids.clear()
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1280,720)
	game.pending_doctrines.assign(["industry", "biosphere"])
	game._confirm_doctrines()
	game._set_paused(true, false)
	game.tick_timer.start(game._cycle_wait_seconds() * 0.4)
	game.tick_timer.wait_time = game._cycle_wait_seconds()
	game._set_time_speed(1)
	check(is_equal_approx(game.tick_timer.time_left / game.tick_timer.wait_time, 0.4) and game.tick_timer.paused, "Changing speed must preserve cycle progress and pause state")
	game._set_time_speed(0)
	check(is_equal_approx(game.tick_timer.time_left / game.tick_timer.wait_time, 0.4), "Repeated speed changes must not restart the cycle")
	await process_frame
	game.grid_scroll.scroll_horizontal = 500
	game.camera_pan_remainder = Vector2.ZERO
	for step in range(240):
		game._pan_grid(Vector2.RIGHT, 1.0 / 240.0)
	check(absi(game.grid_scroll.scroll_horizontal - 1550) <= 1, "High-frame-rate pan must retain fractional movement")
	game.hand.assign(["solar_array"])
	game.selected_card_id = "solar_array"
	game.selected_rotation = 2
	if DisplayServer.get_name() != "headless":
		game._toggle_menu()
		await create_timer(0.1).timeout
		var draws := [0]
		var count_draw := func(): draws[0] += 1
		game.grid_view.draw.connect(count_draw)
		await create_timer(0.1).timeout
		check(draws[0] == 0, "Paused menu must not continuously redraw a selected blueprint")
		game._toggle_menu()
		await create_timer(0.1).timeout
		check(draws[0] > 0, "Closing the menu must resume blueprint preview drawing")
		game.grid_view.draw.disconnect(count_draw)
	var before: Dictionary = game.resources.duplicate(true)
	check(game._placement_connections("solar_array", Vector2i(19,20)).contains("1 door matches"), "Preview must identify a real matching door")
	var original_chip_style = game.resource_chips.power.get_theme_stylebox("panel")
	game._refresh_resources()
	check(game.resource_chips.power.get_theme_stylebox("panel") == original_chip_style, "HUD refresh must reuse its resource styles")
	check(game.resources == before, "Forecast must not mutate reserves")
	var room_forecast: Dictionary = game._simulate_room_economy(true, game.cycle + 1)
	var raw_delta: Dictionary = room_forecast.delta.duplicate(true)
	var original_crew: int = game.crew_count
	game.crew_count = 1
	var projected_once: Dictionary = game._project_cycle_delta(room_forecast)
	var projected_twice: Dictionary = game._project_cycle_delta(room_forecast)
	check(projected_once == projected_twice and room_forecast.delta == raw_delta, "Reusing a forecast must not accumulate crew upkeep or mutate the room result")
	check(int(projected_once.get("food", 0)) == int(raw_delta.get("food", 0)) - 1, "Projection must still include crew upkeep")
	game.crew_count = original_crew
	check(not game._placement_connections("solar_array", Vector2i(19,20)).contains("Known links"), "Undiscovered recipes must stay hidden")
	game.meta.discovered_synergy_ids["core_diagnostics"] = true
	var found_known := false
	var found_mismatch := false
	for rotation in range(4):
		game.selected_rotation = rotation
		var preview: String = game._placement_connections("research_lab", Vector2i(19,20))
		found_known = found_known or preview.contains("Core Diagnostics")
		found_mismatch = found_mismatch or preview.contains("1 unmatched")
	check(found_known, "A learned recipe must appear for a matching placement")
	check(found_mismatch, "Rotated nonmatching doors must be identified")
	game.meta.discovered_synergy_ids.clear()
	game.selected_rotation = 2
	game._on_grid_clicked(Vector2i(19,20))
	check(game.drone_fleet.reserved(Vector2i(19,20)), "Paid placement must first reserve the construction cell")
	game.paused = false
	# Architects build paid orders since the Sept 8 construction pass: finish the
	# core thaw, then advance crew construction until the room completes.
	game.Architects.advance_core(game, game.Architects.DURATION)
	for step in range(900):
		game._update_test_walker(0.1)
		game._update_wreck_clearance(0.1)
		if game.occupied.has(Vector2i(19,20)): break
	game.paused = true
	check(game.placed_rooms.size() == 2 and game.resources != before, "Fixture must pay normal room costs")
	game.selected_card_id = ""
	game.selected_room_cell = Vector2i(19,20)
	game.hover_cell = game.selected_room_cell
	game._refresh_inspector()
	game._toggle_inspected_room()
	# The Sept 8 badge redesign shows only the alert count, which already
	# excludes deliberately suspended rooms (risk minus suspended in main.gd).
	check(game.diagnostics_button.text.contains("0 ALERTS"), "Deliberately suspended rooms must be separate from supply alerts")
	game.diagnostics_button.grab_focus()
	game.diagnostics_button.pressed.emit()
	check(game.paused and game.journal_tabs.current_tab == 1, "Diagnostics must open the pausing journal")
	check(game.archive_label.text.contains("SUSPENDED") and game.archive_label.text.contains("19,20"), "Health must explain the problem and link its exact room")
	game.archive_label.meta_clicked.emit("19,20")
	check(not game._journal_is_open() and game.selected_room_cell == Vector2i(19,20) and game.paused, "Locate must restore pause state and select the room")
	check(game.diagnostics_button.has_focus(), "Closing diagnostics must return focus to its opener")
	game._toggle_journal()
	game.journal_tabs.current_tab = 2
	check(game.archive_label.text.contains("next reserve") and game.archive_label.text.contains("events"), "Forecast must expose reserves and uncertainty")
	game.resources.food = 8
	check(game._reserve_forecast("food", -3).contains("~3 cycles"), "Depletion estimate must round up fractional cycles")
	game._log("Solar Array diagnostic test", false)
	game.journal_tabs.current_tab = 3
	game.history_search.text = "solar array"
	game._refresh_archive()
	check(game.archive_label.text.contains("diagnostic test"), "History search must be case insensitive and include quiet events")
	game.history_search.text = "no such event"
	game._refresh_archive()
	check(game.archive_label.text.contains("No matching records"), "History must explain empty searches")
	check(Saves.write(game, game.run_save_path) == OK, "Checkpoint must save diagnostics history")
	var saved := Saves.read(game.run_save_path)
	check(saved.get("event_history", []).has(game.event_history.back()), "Written checkpoint must retain history")
	game.event_history.clear()
	check(Saves.restore(game, saved) and not game.event_history.is_empty(), "History must survive restore")
	saved.erase("event_history")
	check(Saves.restore(game, saved) and game.event_history.is_empty(), "Older checkpoints must load without history")
	if not game._journal_is_open():
		game._toggle_journal()
	check(game._journal_is_open(), "Layout capture must show the journal")
	for index in range(70):
		game._log("Built history scroll fixture %d" % index, false)
	game.journal_tabs.current_tab = 3
	game.history_search.text = ""
	game._refresh_archive()
	await create_timer(0.15).timeout
	game.archive_label.get_v_scroll_bar().value = 160
	var reading_position: float = game.archive_label.get_v_scroll_bar().value
	game._refresh_archive()
	await process_frame
	check(is_equal_approx(game.archive_label.get_v_scroll_bar().value, reading_position), "Refreshing unchanged history must retain reading position")
	game.journal_tabs.current_tab = 2
	await process_frame
	game.journal_tabs.current_tab = 3
	await process_frame
	check(is_equal_approx(game.archive_label.get_v_scroll_bar().value, reading_position), "Journal tabs must restore reading position")
	game.history_filter.select(2)
	game._refresh_archive()
	check(game.archive_label.text.contains("No matching records"), "Discovery filter must exclude construction events")
	game.history_filter.select(3)
	game._refresh_archive()
	check(game.archive_label.text.contains("70 matching"), "Construction filter must show matching count")
	game.history_filter.select(0)
	var shortcut := InputEventKey.new()
	shortcut.pressed = true
	shortcut.ctrl_pressed = true
	shortcut.keycode = KEY_F
	game._input(shortcut)
	check(game.history_search.has_focus(), "Ctrl+F must focus history search")
	game.history_search.text = "fixture"
	shortcut.ctrl_pressed = false
	shortcut.keycode = KEY_ESCAPE
	game._input(shortcut)
	check(game.history_search.text.is_empty() and game._journal_is_open(), "Escape must clear focused search before closing journal")
	Preferences.text_scale = 1.3
	Preferences.apply_menu_text(game.journal_layer)
	for index in range(5):
		game.journal_tabs.current_tab = index
		game._refresh_archive()
		await create_timer(0.15).timeout
		check(root.get_visible_rect().encloses(game.archive_label.get_parent().get_parent().get_global_rect()), "Journal page %d must fit at 130%% text" % index)
		if DisplayServer.get_name() != "headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/decision-ui-page-%d.png" % index)
	game._toggle_journal()
	var activate := InputEventAction.new()
	activate.action = "ui_accept"
	activate.pressed = true
	game.resource_chips.power.gui_input.emit(activate)
	check(game._journal_is_open() and game.journal_tabs.current_tab == 2 and game.inspected_resource == "power", "Resource keyboard activation must open its details")
	check(game.archive_label.text.contains("ROOM CONTRIBUTIONS") and game.archive_label.text.contains("Solar Array") and game.archive_label.text.contains("SUSPENDED"), "Resource details must show room rates and operation status")
	check(not game.archive_label.text.contains("Core Diagnostics"), "Resource breakdown must not reveal hidden patterns")
	if DisplayServer.get_name() != "headless":
		await create_timer(0.15).timeout
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/decision-ui-resource.png")
	game.archive_label.meta_clicked.emit("all_resources")
	check(game.inspected_resource.is_empty() and not game.archive_label.text.contains("ROOM CONTRIBUTIONS"), "All reserves link must clear resource selection")
	game.journal_tabs.current_tab = 4
	check(game.archive_label.text.contains("INSTALLED ROOMS // 2") and game.archive_label.text.contains("19,20"), "Room directory must include exact installed room locations")
	game.archive_label.meta_clicked.emit("19,20")
	check(not game._journal_is_open() and game.resource_chips.power.has_focus() and game.selected_room_cell == Vector2i(19,20), "Directory locate must restore resource opener focus and select the correct room")
	game._refresh_cards()
	var closed_text: String = game.archive_label.text
	game._refresh_all()
	check(game.archive_label.text == closed_text, "Closed journal must not rebuild during HUD refresh")
	game.history_search.text = "old loop"
	game.history_filter.select(2)
	game.journal_scroll_positions[3] = 160.0
	game._start_reboot_cycle()
	check(game.history_search.text.is_empty() and game.history_filter.selected == 0 and game.journal_scroll_positions.is_empty(), "A new loop must clear stale history navigation")
	for path in [Preferences.save_path, game.meta.save_path, game.run_save_path, game.run_save_path + ".bak"]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("DECISION UI: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
