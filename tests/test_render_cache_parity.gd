extends SceneTree
var game
var views: Array = []
func _init() -> void: call_deferred("run")
func settle() -> void:
	for frame in range(6): await process_frame
	await RenderingServer.frame_post_draw
func mode(cached: bool) -> void:
	for view in views:
		view.reuse_prop_meshes = cached
		view.reuse_embedded_geometry = cached
	game.grid_view.queue_redraw()
func run() -> void:
	preload("res://scripts/title_settings.gd").save_path = "user://render_parity.cfg"
	var main = load("res://scenes/main.tscn")
	game = main.instantiate()
	game.meta.save_path = "user://render_parity.meta"
	game.run_save_path = "user://render_parity.loop"
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600,900)
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.set_process(false)
	game.tick_timer.stop()
	game.selected_card_id = ""
	game.wrecks.clear()
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized = true
	var index := 0
	for id in game.RoomDatabaseScript.all_rooms():
		if id == "brine_core": continue
		var cell := Vector2i(16+index%7,16+index/7)
		if cell == Vector2i(20,20): cell = Vector2i(23,20)
		game._place_room(id,cell,true)
		index += 1
	for room in game.placed_rooms:
		var view = game.grid_view._bill_room_view(room)
		if view != null and not views.has(view): views.append(view)
	game.Architects.advance_core(game,10.0)
	game._set_paused(true,false)
	game.grid_view.cull_room_drawing = false
	game._refresh_all()
	await settle()
	game._fit_station_view()
	await settle()
	game._center_grid_on_station_now()
	for q in range(4):
		for room in game.placed_rooms: room.rotation = q
		game.visual_time_seconds = 2.75+q
		game._refresh_all()
		await settle()
		for enabled in [false,true]:
			mode(enabled)
			await settle()
			root.get_texture().get_image().save_png("res://output/render-parity-q%d-%s.png" % [q,"cached" if enabled else "direct"])
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
	await settle()
	game.grid_scroll.scroll_horizontal = int(20.5*game.get_cell_size()-game.grid_scroll.size.x*0.5)
	game.grid_scroll.scroll_vertical = int(20.5*game.get_cell_size()-game.grid_scroll.size.y*0.5)
	for enabled in [false,true]:
		mode(enabled)
		await settle()
		root.get_texture().get_image().save_png("res://output/render-parity-close-%s.png" % ("cached" if enabled else "direct"))
	var meshes := 0
	for view in views:
		assert(view.prop_meshes.size() <= 256)
		assert(view.embedded_edge_cache.size() <= 64)
		meshes += view.prop_meshes.size()
	assert(meshes > 0,"Cache must actually be exercised")
	print("Retained meshes: ",meshes)
	print("RENDER PARITY CAPTURE PASS: %d rooms, %d views, four rotations" % [game.placed_rooms.size(),views.size()])
	game.queue_free()
	await process_frame
	quit()
