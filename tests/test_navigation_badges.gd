extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1600,900)
	root.gui_disable_input = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = "user://badge-test.loop"
	game.meta.save_path = "user://badge-test.meta"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	# Let normal camera processing run: a spurious slider signal used to cancel centering.
	for i in range(8): await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.crew_comms.minimize()
	game.meta.guide_completed = false
	game._refresh_learning_ui()
	assert(not game.guide_box.visible, "Tutorial remains absent for new players")
	game.selected_card_id = ""
	game._refresh_placement_status()
	for i in range(4): await process_frame
	var initial_center: Vector2 = game._grid_view_center_ratio() * game.GRID_SIZE
	assert(initial_center.distance_to(Vector2(20.5,20.5)) * game.get_cell_size() < 2.0, "Startup centers the core after initial viewport layout")
	assert(game.journal_button.get_meta("navigation_badge") == "journal")
	assert(game.diagnostics_button.get_meta("navigation_badge") == "diagnostics")
	assert(game.discovery_review_button.get_meta("navigation_badge") == "archive")
	var row = game.discovery_review_button.get_parent()
	assert(row.name == "NavigationRow" and row.get_child_count() == 4)
	assert(row.get_child(1) == game.diagnostics_button and row.get_child(2) == game.journal_button)
	assert(game.find_child("CycleLabel",true,false) == null) # No duplicate counter in the top bar.
	game.cycle = 12
	game._refresh_solar_meter()
	assert(game.cycle_counter_label.text == "CYCLE 012")
	assert(game.solar_time_label.text == "HOLD")
	game.cycle = 13
	game._refresh_solar_meter()
	assert(game.cycle_counter_label.text == "CYCLE 013")
	assert(game.find_child("ResonanceChip",true,false) == null)
	var badge = game.journal_button.get_node("NavigationBadge")
	var draws := [0]
	badge.draw.connect(func(): draws[0] += 1)
	for i in range(4): await process_frame
	draws[0] = 0
	for i in range(8): await process_frame
	assert(draws[0] == 0, "Unchanged badge retains its drawing across idle frames")
	game.journal_button.disabled = true
	for i in range(3): await process_frame
	assert(draws[0] > 0, "Disabled button redraws the badge tint")
	game.journal_button.disabled = false
	for extent in [Vector2i(1600,900),Vector2i(960,540)]:
		root.size = extent
		for i in range(12): await process_frame
		assert(game._grid_view_center_ratio().distance_to(initial_center / game.GRID_SIZE) * game.GRID_SIZE * game.get_cell_size() < 3.0, "Window resize preserves the station camera center")
		var widths := []
		for button in row.get_children():
			widths.append(button.size.x)
			var icon = button.get_node("NavigationBadge")
			assert(absf(icon.position.x + icon.size.x / 2.0 - button.size.x / 2.0) < 1.0, "Badge is centered")
			assert(icon.position.y >= 8 and icon.position.y + icon.size.y <= 64, "Badge retains breathing room above its caption")
		assert(absf(widths.max() - widths.min()) < 1.0, "Navigation buttons share equal space")
		var panel = game.find_child("ControlsPanel",true,false)
		assert(panel.get_global_rect().end.y <= game.get_node("Root").size.y, "Time and cycle panel fits the window")
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/navigation-%d.png" % extent.x)
	game._finish_guide()
	for i in range(12): await process_frame
	assert(game.find_child("PreviewPanel",true,false).custom_minimum_size.y == 520.0, "Inspector regains its full reading height when the guide closes")
	var cycle_panel = game.find_child("ControlsPanel",true,false)
	cycle_panel.get_parent().get_parent().scroll_vertical = 10000
	root.size = Vector2i(1600,900)
	for i in range(12): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/hud-size-polish/cycle-panel.png")
	game.diagnostics_button.pressed.emit()
	assert(game.journal_tabs.current_tab == 1)
	game._toggle_journal()
	game.journal_button.pressed.emit()
	game._toggle_journal()
	game.queue_free()
	await process_frame
	root.size = Vector2i(1600,900)
	var title = load("res://scenes/title_screen.tscn").instantiate()
	root.add_child(title)
	for i in range(12): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/navigation-title.png")
	print("NAVIGATION PASS: badge bindings, diagnostics tab, journal actions, two HUD sizes and title capture")
	quit()
