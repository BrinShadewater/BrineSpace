extends "res://tests/test_construction_preview.gd"
func run():
	if DisplayServer.get_name()=="headless": quit(2); return
	var setup: Dictionary = preload("res://tests/test_synergy_geometry.gd").configure_test_window(root)
	if not setup.get("secondary_available",false): quit(2); return
	DirAccess.make_dir_recursive_absolute("res://output/placement-experiments-20261020")
	await super.run()

func presentation()->void:
	var previous_id: String = game.selected_card_id
	var previous_cell: Vector2i = game.hover_cell
	var warning_height := 0.0
	for dimensions in [Vector2i(1600,900),Vector2i(1280,720)]:
		root.size=dimensions;game._update_interface_scale();game._resize_grid_view()
		for sample in ["warning","connected"]:
			game.selected_card_id=previous_id if sample=="warning" else "cold_store"
			game.hover_cell=previous_cell if sample=="warning" else Vector2i(20,19)
			game._refresh_all();await process_frame
			game._position_placement_feedback();game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var area: Rect2 = game.station_clear_rect()
			var panel: Rect2 = game.placement_feedback.get_global_rect()
			if sample=="warning": warning_height=panel.size.y
			else: check(panel.size.y<warning_height,"Short cue shrinks after long warning")
			check(game.placement_feedback.is_visible_in_tree(),"Experiment preview visible")
			check(area.grow(1).encloses(panel),"Preview fits station at %s"%str(dimensions))
			var text: String = game.placement_feedback.text
			check(text.contains("Experiment"),"Generic cue appears in actual preview")
			if sample=="warning":check(text.find("NO SAFE CREW ROUTE")<text.find("Experiment"),"Construction warning precedes experiment")
			root.get_texture().get_image().save_png("res://output/placement-experiments-20261020/%s-%dx%d.png"%[sample,dimensions.x,dimensions.y])
	game.selected_card_id=previous_id;game.hover_cell=previous_cell;game._refresh_all()
