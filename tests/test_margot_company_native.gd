extends "res://tests/test_margot_company.gd"
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var setup:Dictionary=preload("res://tests/test_synergy_geometry.gd").configure_test_window(root)
	if not setup.get("secondary_available",false):quit(2);return
	await super.run()
func presentation()->void:
	root.size=Vector2i(1600,900)
	game._update_interface_scale();game._resize_grid_view();game._set_grid_zoom(1.0)
	game._toggle_hand_collapsed();game._refresh_all()
	await process_frame;await process_frame
	game.grid_scroll.scroll_horizontal=int((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x*.5)
	game.grid_scroll.scroll_vertical=int((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y*.5)
	# Let the existing nap-entry animation settle; the crew fixture remains asleep.
	for i in range(30):game.companion_actors.margot.update(game,.05)
	await process_frame;game.grid_view.queue_redraw();await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("res://output/margot-company-20261020")
	root.get_texture().get_image().save_png("res://output/margot-company-20261020/resting-together.png")
	check(game.companion_actors.margot.texture(0)!=null,"Existing nap artwork renders")
