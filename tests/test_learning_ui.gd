extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
const Insights = preload("res://scripts/station_ui_insights.gd")
var failures := 0
func _init() -> void:
	call_deferred("_run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _run() -> void:
	Preferences.save_path = "user://learning_ui_test.cfg"
	Preferences.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://learning_ui_test.json"
	game.run_save_path = "user://learning_ui_test.loop"
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.unread_records.clear()
	game.meta.guide_completed = false
	game.meta.unlocked_room_ids.erase("biodome")
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600,900)
	game.pending_doctrines.assign(["industry", "biosphere"])
	game._confirm_doctrines()
	game._set_paused(true, false)
	check(game.guide_box.visible and game.guide_label.text.begins_with("1 / 4"), "New-loop guide must start with paid placement")
	game.hand.assign(["solar_array"])
	game.selected_card_id = "solar_array"
	game.selected_rotation = 2
	game._on_grid_clicked(Vector2i(19,20))
	check(game.guide_label.text.contains("CONSTRUCTION"), "Guide must explain pending drone construction")
	game.paused = false
	game._update_wreck_clearance(30.0)
	game.paused = true
	check(game.placed_rooms.size() == 2, "Guide fixture must use a real paid placement")
	game._refresh_learning_ui()
	check(not game.guide_label.text.begins_with("1 / 4"), "Guide must respond to placement")
	game.selected_card_id = ""
	game.hover_cell = Vector2i(19,20)
	game.selected_room_cell = game.hover_cell
	game._refresh_inspector()
	check(game.inspector_label.text.contains("NEXT CYCLE FORECAST"), "Built-room inspector must separate forecast from observed status")
	check(not game.inspector_label.text.contains("Closed Air Loop"), "Inspector must not reveal an undiscovered recipe")
	game._focus_inspected_room()
	check(game.selected_room_cell == Vector2i(19,20), "Locate must retain the inspected room")
	game._toggle_inspected_room()
	game._refresh_inspector()
	check(game.inspector_label.text.contains("Resume this room"), "Suspension must have an actionable remedy")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/learning-ui-inspector.png")
	check(Insights.remedy("NEEDS POWER + WATER").contains("shared") or Insights.remedy("NEEDS POWER + WATER").contains("share"), "Shortage guidance must explain the actual shared budget")
	game._handle_synergy_discovery("closed_air_loop")
	game._refresh_learning_ui()
	check(game.meta.unread_records.has("synergy:closed_air_loop") and game.discovery_review_button.visible, "Discovery must create a persistent review action")
	var restored = preload("res://scripts/meta_state.gd").new()
	restored.save_path = game.meta.save_path
	restored.unread_records.clear()
	restored.load_from_disk()
	check(restored.unread_records.has("synergy:closed_air_loop"), "Unread discoveries must survive profile reload")
	check(game.current_toast_record == "synergy:closed_air_loop", "Discovery notification must retain its exact archive target")
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	game.cascade_toast.gui_input.emit(click)
	await process_frame
	check(game.menu_archive.mode == "codex" and game.menu_archive.codex_tabs.current_tab == 1, "Review must open the synergy Codex")
	check(game.menu_archive.search.text == "Closed Air Loop", "Review must target the discovered entry")
	check(not game.meta.unread_records.has("synergy:closed_air_loop"), "Opening a discovery must mark it reviewed")
	game.menu_archive._close()
	await create_timer(0.2).timeout
	game._close_menu()
	game._award_synergy_stabilization(preload("res://scripts/synergy_manager.gd").get_synergy("closed_air_loop"))
	game._refresh_learning_ui()
	check(game.meta.unread_records.has("room:biodome"), "Decrypted blueprints must have their own unread record")
	game._review_latest_discovery()
	await process_frame
	check(game.menu_archive.codex_tabs.current_tab == 0 and game.menu_archive.search.text == "Biodome", "Blueprint review must target its room card")
	game.menu_archive._close()
	await create_timer(0.2).timeout
	game._close_menu()
	game._finish_guide()
	check(not game.guide_box.visible, "Skip must dismiss the guide")
	restored.load_from_disk()
	check(restored.guide_completed, "Skipping the guide must persist")
	game.meta.doctrine_mastery = {"industry": 1, "biosphere": 1}
	game.resonance_score = 50
	game._show_reboot_summary("Station supplies exhausted.", false)
	check(game.summary_text.text.contains("WHAT SURVIVES") and game.summary_text.text.contains("Station supplies exhausted."), "Summary must explain the outcome and retained rewards")
	check(game.meta.unread_records.has("mastery:industry"), "A mastery rank gain must be marked unread")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/learning-ui-summary.png")
	game._review_latest_discovery()
	await process_frame
	check(game.menu_archive.mode == "progression", "Summary rank review must open Meta Progression")
	game.menu_archive._close()
	await create_timer(0.2).timeout
	check(game.summary_layer.visible, "Closing rank review must return to the summary")
	for path in [Preferences.save_path, game.meta.save_path, game.run_save_path]:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(path)
	print("LEARNING UI: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
