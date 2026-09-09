extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	root.gui_disable_input = true
	Preferences.save_path = "user://ui_workspace.cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://ui_workspace.meta"
	game.run_save_path = "user://ui_workspace.loop"
	root.add_child(game)
	current_scene = game
	game._set_paused(true,false)
	game.tick_timer.stop()
	root.size = Vector2i(1280,720)
	await process_frame
	game._fit_station_view()
	await process_frame
	await process_frame
	var fit_center: Vector2 = (Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)+game.grid_scroll.size*0.5)/game.get_cell_size()
	check(fit_center.distance_to(Vector2(20.5,20.5))*game.get_cell_size()<2.0,"Fit settles directly on the station center")
	game._on_grid_clicked(Vector2i(20,20))
	var original: String = game.preview_name_label.text
	game._on_grid_hovered(Vector2i(18,21))
	game._refresh_all()
	check(game.preview_name_label.text == original, "Crossing map preserves clicked inspector selection")
	var card := PanelContainer.new()
	game.add_child(card)
	game._on_card_hovered("life_support",card)
	check(game.preview_name_label.text == original, "Passing over a blueprint preserves clicked room")
	card.queue_free()
	check(not game.inspector_label.mouse_force_pass_scroll_events, "Inspector wheel does not escape into parent")
	check(game.construction_button.get_parent().name == "SidePanel", "Construction access is outside the playfield")
	game.inspector_label.get_v_scroll_bar().value = 20.0
	var previous: float = game.inspector_label.get_v_scroll_bar().value
	game._refresh_inspector()
	await process_frame
	check(is_equal_approx(game.inspector_label.get_v_scroll_bar().value,previous), "Refreshing current selection preserves scroll")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/ui-workspace-1280.png")
	game._set_grid_zoom(0.0001)
	await process_frame
	await process_frame
	check(game.get_cell_size()*game.GRID_SIZE+1>=maxf(game.grid_scroll.size.x,game.grid_scroll.size.y), "Minimum zoom cannot expose canvas beyond seabed square")
	game._pan_grid(Vector2(-1,-1),100)
	check(game.grid_scroll.scroll_horizontal>=0 and game.grid_scroll.scroll_vertical>=0,"Camera remains inside map at near corner")
	game._pan_grid(Vector2(1,1),100)
	await process_frame
	check(game.grid_scroll.scroll_horizontal<=game.GRID_SIZE*game.get_cell_size()-game.grid_scroll.size.x+2,"Camera remains inside far map edge")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/ui-workspace-map.png")
	game._open_menu()
	check(game.pause_page=="main" and game.pause_pages.main.get_child_count()==5,"Main pause menu has five actions")
	var opener: Button = game.pause_pages.main.get_child(3)
	opener.grab_focus()
	opener.pressed.emit()
	check(game.pause_page=="station" and not game.pause_pages.main.visible,"Station tools occupy their own page")
	var escape := InputEventKey.new()
	escape.keycode = KEY_ESCAPE
	escape.pressed = true
	game._unhandled_input(escape)
	check(game.menu_open and game.pause_page=="main" and opener.has_focus(),"Escape backs out and restores submenu opener focus")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/pause-menu-streamlined.png")
	game._show_pause_page("exit")
	check(game.end_expedition_button.is_visible_in_tree(),"Conclude action is available under End or Leave")
	game._pause_page_back()
	game._menu_save_game()
	check(game.menu_save_feedback.text.begins_with("LOOP RECORDED"),"Save feedback remains visible on root page")
	game._close_menu()
	check(game.paused,"Closing nested menu retains prior pause state")
	game.set_process(false)
	game.crew_comms.set_process(false)
	game.crew_comms.dismiss()
	game._set_paused(true,false)
	game.resources = {"metal":100,"power":12,"oxygen":30,"water":30,"food":30,"data":100,"biomass":100,"rare_minerals":100,"integrity":100}
	# This placement fixture needs an empty neighbor, independent of generated wrecks.
	game.wrecks.erase(Vector2i(19,21))
	game._place_room("solar_array",Vector2i(19,20),true,true)
	var Insights = preload("res://scripts/station_ui_insights.gd")
	game.run_discovered_synergy_ids.clear()
	var guide_without_hidden: String = Insights.guide(game)
	game.connected_synergy_links.append({"id":"field_notes"})
	check(Insights.guide(game)==guide_without_hidden,"Guide does not reveal a connected but undiscovered recipe")
	game.connected_synergy_links.pop_back()
	game.drone_fleet.orders.append({"id":"life_support","pos":Vector2i(19,21)})
	check(Insights.guide(game).contains("already paid") and Insights.guide(game).contains("resume"),"Guide reacts to paused paid construction")
	game.drone_fleet.orders.clear()
	game.run_discovered_synergy_ids.append("field_notes")
	game.synergy_stabilization_progress["field_notes"] = 2
	check(Insights.guide(game).contains("2 / 3"),"Guide explains discovered pattern progress")
	game.run_discovered_synergy_ids.clear()
	game.resources.oxygen = 0
	game.crew_count = 2
	game.hand = ["life_support"]
	check(Insights.guide(game).contains("OXYGEN IS FALLING") and Insights.guide(game).contains("Life Support"),"Low oxygen suggests an affordable supply card")
	game.resources.oxygen = 30
	game.crew_count = 0
	game.hand = ["life_support"]
	game.selected_card_id = "life_support"
	game.selected_room_cell = Vector2i(-1,-1)
	game.hover_cell = Vector2i(19,21)
	game.resources.metal = 0
	game._refresh_inspector()
	game._refresh_placement_status()
	check(game.placement_feedback.visible and game.placement_feedback.text.contains("Need Metal 5"),"Placement reports the exact material shortfall visibly")
	check(game.inspector_label.text.find("Build cost:") < game.inspector_label.text.find("Room details"),"Inspector prioritizes build decision before description")
	game.resources.metal = 100
	game._refresh_placement_status()
	check(game.placement_feedback.text.contains("READY TO BUILD"),"Affordable matched door gives ready feedback")
	game.hover_cell = Vector2i(0,0)
	game._refresh_placement_status()
	check(game.placement_feedback.text.contains("adjacent door"),"Disconnected placement explains connection requirement")
	game.hover_cell = Vector2i(19,21)
	game.resources.metal = 0
	game._refresh_all()
	root.size = Vector2i(1600,900)
	game._fit_station_view()
	for frame in range(12): await process_frame
	game._position_placement_feedback()
	game.inspector_label.scroll_to_line(0)
	check(game.guide_label.size.y > 20 and not game.guide_label.text.is_empty(),"Adaptive guide has visible text area")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/build-decisions/placement.png")
	for path in [Preferences.save_path,game.meta.save_path,game.run_save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("UI WORKSPACE PASS" if failures==0 else "UI WORKSPACE FAILURES: %d" % failures)
	quit(0 if failures==0 else 1)
