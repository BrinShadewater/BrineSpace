extends SceneTree
var game
var views: Array = []
var failures := 0
func _init() -> void: call_deferred("run")
func settle() -> void:
	for frame in range(6): await process_frame
	await RenderingServer.frame_post_draw
func mode(cached: bool) -> void:
	game.grid_view.reuse_door_parts = cached
	game.grid_view.surface_key = []
	game.grid_view.queue_redraw()
func changed_state(label: String) -> void:
	# Capture the already-retained renderer first: comparing after a fresh toggle
	# alone would miss stale-cache invalidation bugs.
	# Panning may retain the same visible floor set and only move its transform.
	var before: int = game.grid_view.floor_rebuilds
	game.grid_view.queue_redraw()
	await RenderingServer.frame_post_draw
	if game.grid_view.floor_rebuilds <= before and label != "pan":
		failures += 1
		push_error("State did not invalidate in the next rendered frame: " + label)
	await settle()
	root.get_texture().get_image().save_png("res://output/hitch-parity-%s-cached.png" % label)
	mode(false)
	await settle()
	root.get_texture().get_image().save_png("res://output/hitch-parity-%s-direct.png" % label)
	mode(true)
	await settle()
func run() -> void:
	preload("res://scripts/title_settings.gd").save_path = "user://hitch_parity.cfg"
	var main = load("res://scenes/main.tscn")
	game = main.instantiate()
	game.meta.save_path = "user://hitch_parity.meta"
	game.run_save_path = "user://hitch_parity.loop"
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
			root.get_texture().get_image().save_png("res://output/hitch-parity-q%d-%s.png" % [q,"cached" if enabled else "direct"])
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
	await settle()
	game.grid_scroll.scroll_horizontal = int(20.5*game.get_cell_size()-game.grid_scroll.size.x*0.5)
	game.grid_scroll.scroll_vertical = int(20.5*game.get_cell_size()-game.grid_scroll.size.y*0.5)
	for enabled in [false,true]:
		mode(enabled)
		await settle()
		root.get_texture().get_image().save_png("res://output/hitch-parity-close-%s.png" % ("cached" if enabled else "direct"))
	var static_before := 0
	var live_before := 0
	for canvas in game.grid_view.content_canvases.values():
		static_before += canvas.static_redraws
		live_before += canvas.live_redraws
	var before := Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)
	for frame in range(12):
		game.visual_time_seconds += 0.1
		game.grid_view.queue_redraw()
		await settle()
	assert(before == Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds),"Stable surfaces must remain retained as animation time advances")
	var static_after := 0
	var live_after := 0
	for canvas in game.grid_view.content_canvases.values():
		static_after += canvas.static_redraws
		live_after += canvas.live_redraws
	assert(static_before>0 and static_after==static_before,"Static content must actually remain retained")
	assert(live_after>live_before,"Animated content must keep drawing")
	print("STATIC CONTENT REUSE / LIVE ANIMATION PASS")
	game._fit_station_view()
	await settle()
	for q in range(4):
		for room in game.placed_rooms:
			room.rotation = q
			game.powered_room_cells[room.pos] = true
		for tick in range(3):
			# Warm retention before advancing time, so misclassified animations fail.
			mode(true)
			await settle()
			game.visual_time_seconds = 12.3+tick*0.37
			for enabled in [true,false]:
				mode(enabled)
				await settle()
				root.get_texture().get_image().save_png("res://output/hitch-parity-motion-%d-%d-%s.png" % [q,tick,"cached" if enabled else "direct"])
	mode(true)
	await settle()
	game.placed_rooms[0].rotation = (int(game.placed_rooms[0].rotation)+1)%4
	await changed_state("rotate-live")
	game.powered_room_cells.erase(Vector2i(20,20))
	game.grid_view.queue_redraw()
	await settle()
	game.powered_room_cells[Vector2i(20,20)] = true
	await changed_state("power-on")
	game.powered_room_cells.clear()
	game.grid_view.room_light_levels.clear()
	await changed_state("power-off")
	game.grid_view.room_light_levels[Vector2i(20,20)] = 0.43
	await changed_state("light-fade")
	preload("res://scripts/title_settings.gd").raised_walls = not preload("res://scripts/title_settings.gd").raised_walls
	await changed_state("raised-walls")
	game._place_room("corridor",Vector2i(23,19),true)
	await changed_state("place")
	var removed: Dictionary = game.occupied[Vector2i(23,19)]
	game.placed_rooms.erase(removed)
	game.occupied.erase(Vector2i(23,19))
	await changed_state("remove")
	game.drone_fleet.synchronize(game.placed_rooms)
	var drone: Dictionary = game.drone_fleet.drones[Vector2i(20,20)]
	drone.phase = "outbound"
	drone.last_cell = Vector2i(20,20)
	drone.route = [Vector2i(21,20)]
	drone.position = Vector2(20.5,20)
	await changed_state("door-open")
	drone.position = Vector2(20,20)
	await changed_state("door-close")
	drone.phase = "docked"
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
	await settle()
	game.grid_view.cull_room_drawing = true
	await changed_state("cull")
	game.grid_scroll.scroll_horizontal += int(game.get_cell_size()*2)
	await changed_state("pan")
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.8)
	await changed_state("zoom")
	# Exercise live NPC updates and the actual construction-drone state machine.
	preload("res://scripts/title_settings.gd").pause_unfocused = false
	game._place_room("construction_drone_bay",Vector2i(26,20),true)
	game.drone_fleet.synchronize(game.placed_rooms)
	game.drone_fleet.enqueue("corridor",Vector2i(26,19),0)
	for room in game.placed_rooms:
		game.powered_room_cells[room.pos] = true
	game._fit_station_view()
	await settle()
	var saw_drone := false
	var saw_movement := false
	var start_foot: Vector2 = game.bill_npc.foot
	for frame in range(160):
		game.paused = false
		game.visual_time_seconds += 0.1
		game._update_test_walker(0.1)
		var built: Array = game.drone_fleet.advance(0.1,game.placed_rooms,game.powered_room_cells,game.wrecks,1000)
		for order in built: game._place_room(order.id,order.pos,true)
		for active_drone in game.drone_fleet.drones.values():
			if active_drone.phase != "docked": saw_drone = true
		if game.bill_npc.foot.distance_to(start_foot)>1.0: saw_movement = true
		game.paused = true
		game.grid_view.queue_redraw()
		await process_frame
		if frame in [19,59,99,159]:
			for enabled in [true,false]:
				mode(enabled)
				await settle()
				root.get_texture().get_image().save_png("res://output/hitch-parity-busy-%d-%s.png" % [frame,"cached" if enabled else "direct"])
			mode(true)
	assert(saw_drone,"Busy fixture must launch a drone")
	assert(saw_movement,"Busy fixture must actually move crew")
	assert(game.occupied.has(Vector2i(26,19)),"Construction must finish in the busy fixture")
	print("BUSY CONTENT PASS: crew moved, drone launched, room constructed")
	var meshes := 0
	for view in views:
		assert(view.prop_meshes.size() <= 256)
		assert(view.embedded_edge_cache.size() <= 64)
		meshes += view.prop_meshes.size()
	assert(meshes > 0,"Cache must actually be exercised")
	print("Retained meshes: ",meshes)
	print("BRINE BATCH PARITY CAPTURE %s: %d rooms, %d views, four rotations" % ["PASS" if failures==0 else "FAIL",game.placed_rooms.size(),views.size()])
	game.queue_free()
	await process_frame
	quit(failures)
