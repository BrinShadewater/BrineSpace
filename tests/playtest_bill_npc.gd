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
	_stand_bill_up(origin)
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

# A loop now starts with its architect asleep in the core pod, and the crew update skips anyone
# who is not aboard. This fixture builds its own station with no core pod to wake out of, so
# register Bill as recovered crew and stand him up in the centre room.
func _stand_bill_up(origin: Vector2i) -> void:
	var Architects = preload("res://scripts/architects.gd")
	if not game.architect_run.is_empty():
		var occupant: Dictionary = game.architect_run.core
		occupant.recovered = true
		game.recovered_crew.append({"id": occupant.id, "architect_id": occupant.architect_id,
			"name": occupant.name, "origin": origin, "alive": true})
		game.crew_count += 1
		game.had_crew = true
	expect(Architects.present(game, "bill"), "the fixture's architect is aboard before it watches him work")
	game.bill_npc.rebuild(game)
	var nodes: Array = game.bill_npc.room_nodes.get(origin, [])
	expect(not nodes.is_empty(), "the centre room is walkable")
	if not nodes.is_empty():
		game.bill_npc.foot = game.bill_npc.graph.get_point_position(nodes[0])
	game.bill_npc.active = true
	game.bill_npc.direction = "south"
	game.bill_npc.state = "idle"
