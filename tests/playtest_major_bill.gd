extends "res://tests/playtest_nursery_art.gd"

func run() -> void:
	capture_dir = "res://character/major-bill-v2/qa/native"
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.meta.save_path = "user://major_bill_meta_fixture_%d.json" % OS.get_process_id()
	game.run_save_path = "user://major_bill_run_fixture_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600, 900)
	await settle()
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	for info in [["storage_bay",Vector2i(20,20)],["corridor",Vector2i(20,21)],["mycelium_nursery",Vector2i(20,22)]]:
		game._place_room(info[0],info[1],true)
		game.powered_room_cells[info[1]]=true
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game.test_walker_previous_cell = Vector2i(-1,-1)
	game.test_walker_next_cell = Vector2i(-1,-1)
	game.test_walker_cell = Vector2i(20,20)
	game.test_walker_state = "idle"
	game.test_walker_direction = "east"
	game._refresh_all()
	await settle()
	game._fit_station_view()
	await settle()
	var grid = game.grid_view
	game.visual_time_seconds = 20.0
	game.test_walker_next_cell = Vector2i(20,21)
	game.test_walker_progress = 0.0
	var first: Texture2D = grid._get_human_frame("walk","south")
	game.visual_time_seconds = 20.4
	game.test_walker_progress = 0.035
	expect(grid._get_human_frame("walk","south") != first, "Animation advances")
	var paused_frame: Texture2D = grid._get_human_frame("walk","south")
	expect(grid._get_human_frame("walk","south") == paused_frame, "Frozen visual clock preserves frame")
	expect(grid._get_human_frame("run","south") == grid.human_animations.run.south[0], "State change starts frame zero")
	expect(grid._get_human_frame("run","north") == grid.human_animations.run.north[0], "Facing change starts frame zero")
	game.visual_time_seconds = 0.0
	expect(grid._get_human_frame("run","north") == grid.human_animations.run.north[0], "Clock reset starts frame zero")
	game.test_walker_next_cell = Vector2i(-1,-1)
	for info in [["storage",Vector2i(20,20)],["corridor",Vector2i(20,21)],["nursery",Vector2i(20,22)]]:
		game.test_walker_cell = info[1]
		game.test_walker_state = "idle"
		game.test_walker_direction = "south"
		game.visual_time_seconds = 1.0
		await capture(info[0]+"-idle")
		room_pixels(info[1]).save_png(capture_dir.path_join(info[0]+"-crop.png"))
	game.test_walker_cell = Vector2i(20,20)
	game.test_walker_direction = "east"
	for state in ["kneel","repair","stand"]:
		game.test_walker_state = state
		game.visual_time_seconds += 2.0
		grid._get_human_frame(state,"east")
		game.visual_time_seconds += 0.5
		await capture("action-"+state)
	# Close-up movement review through the real layered station renderer.
	game.placed_rooms.clear()
	game.occupied.clear()
	game._place_room("storage_bay",Vector2i(20,20),true)
	for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
		game._place_room("storage_bay",Vector2i(20,20)+offset,true)
	game._refresh_all()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	for state in ["idle","walk","run"]:
		for direction in ["south","north","east","west"]:
			game.test_walker_state = state
			game.test_walker_direction = direction
			var offsets := {"south":Vector2i.DOWN,"north":Vector2i.UP,"east":Vector2i.RIGHT,"west":Vector2i.LEFT}
			game.test_walker_next_cell = Vector2i(-1,-1) if state=="idle" else Vector2i(20,20)+offsets[direction]
			game.test_walker_progress = 0.0
			game.visual_time_seconds += 3.0
			grid._get_human_frame(state,direction)
			await capture("close-"+state+"-"+direction)
			var before := room_pixels(Vector2i(20,20))
			before.save_png(capture_dir.path_join(state+"-"+direction+"-a.png"))
			game.visual_time_seconds += 0.51 if state=="idle" else 0.23
			if state!="idle": game.test_walker_progress = 0.035
			grid.queue_redraw()
			await settle()
			var after := room_pixels(Vector2i(20,20))
			after.save_png(capture_dir.path_join(state+"-"+direction+"-b.png"))
			expect(before.get_data()!=after.get_data(),state+"-"+direction+" changes rendered pixels")
	var saves: Array = [game.meta.save_path,game.run_save_path]
	game.free()
	for path: String in saves:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("MAJOR BILL NATIVE: playback reset/pause, storage/corridor/nursery render, action sequence: %d failures" % failures)
	quit(1 if failures else 0)
