extends "res://tests/test_construction_preview.gd"
## Same functional controls, plus normal and compact presentation; no desktop input.
func presentation()->void:
	for dimensions in [Vector2i(1600,900),Vector2i(1280,720)]:
		root.size=dimensions;game._update_interface_scale();game._resize_grid_view()
		game._refresh_all();await process_frame
		game._position_placement_feedback();game.grid_view.queue_redraw()
		await process_frame;await RenderingServer.frame_post_draw
		var area:Rect2=game.station_clear_rect()
		var panel:Rect2=game.placement_feedback.get_global_rect()
		check(game.placement_feedback.is_visible_in_tree(),"Native floating warning is visible")
		check(area.grow(1).encloses(panel),"Native warning fits within station at %s"%str(dimensions))
		root.get_texture().get_image().save_png("res://output/construction-preview-20261020/warning-%dx%d.png"%[dimensions.x,dimensions.y])
