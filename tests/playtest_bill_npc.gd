extends "res://tests/playtest_nursery_art.gd"
const NPC = preload("res://scripts/bill_npc.gd")

func run() -> void:
	capture_dir = "res://character/major-bill-v2/qa/npc-native"
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.meta.save_path = "user://bill_npc_visual_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://bill_npc_visual_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600, 900)
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	game._place_room("storage_bay", origin, true)
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		game._place_room("storage_bay", origin + offset, true)
	for cell in game.occupied: game.powered_room_cells[cell] = true
	game.test_walker_cell = origin
	game.bill_npc = NPC.new()
	game.rng.seed = 2231
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1, -1)
	game._refresh_all()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	var captured := {}
	for i in range(1800):
		game.visual_time_seconds += 0.1
		game._update_test_walker(0.1)
		var npc = game.bill_npc
		if npc.cell_at(npc.foot) != origin: continue
		var local: Vector2 = npc.foot - (Vector2(origin) + Vector2.ONE * 0.5) * 384
		var key: String = npc.state
		if key == "walk":
			if absf(local.x) < 40 or absf(local.y) < 30: continue
			key += "-" + npc.direction
		if captured.has(key): continue
		# Let each action's first pose advance before capturing it.
		game.grid_view._get_human_frame(npc.state, npc.direction)
		game.visual_time_seconds += 0.4
		await capture(key)
		room_pixels(origin).save_png(capture_dir.path_join(key + "-crop.png"))
		captured[key] = true
	expect(captured.has("repair"), "Native renderer displays Bill's autonomous work animation")
	for save_path in [game.meta.save_path, game.run_save_path]:
		if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
	print("BILL NPC NATIVE: %s; %s" % ["PASS" if failures == 0 else "FAIL", captured.keys()])
	game.free()
	quit(0 if failures == 0 else 1)
