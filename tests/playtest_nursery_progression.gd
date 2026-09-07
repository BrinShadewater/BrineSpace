extends "res://tests/playtest_nursery_art.gd"

const Rooms = preload("res://scripts/room_database.gd")

# Controlled foundation draft only. No resource grants, free construction, or
# disabled failures. Exercise the real scene's purchases and complete cycles.
func build(id: String, cell: Vector2i, q := 0) -> void:
	expect(game.hand.has(id), "Draft contains " + id)
	game._on_card_pressed(id)
	game.selected_rotation = q
	var problem: String = game.get_placement_problem(id, cell)
	expect(problem.is_empty(), "Paid placement: " + problem)
	if not problem.is_empty():
		return
	var before: Dictionary = game.resources.duplicate()
	game._on_grid_clicked(cell)
	expect(game.occupied.has(cell), "Built " + id)
	# Foundation placements can also pay a directive reward in the same click.
	if id == "mycelium_nursery":
		for resource in Rooms.get_room(id).cost:
			expect(game.resources[resource] == before[resource] - Rooms.get_room(id).cost[resource], "Exact nursery purchase cost: " + resource)

func run() -> void:
	if capture_dir.is_empty() or DirAccess.dir_exists_absolute(capture_dir):
		push_error("Use a new --capture-dir")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.meta.save_path = "user://brine_nursery_progression_%d.json" % viewport_width
	for state in [game.meta.unlocked_room_ids, game.meta.discovered_synergy_ids, game.meta.stabilized_synergy_ids, game.meta.doctrine_mastery, game.meta.brine_upgrades, game.meta.recovered_memory_ids]:
		state.clear()
	game.meta.total_research_points = 0
	game.meta.total_victories = 0
	for id in Rooms.STARTING_UNLOCKS:
		game.meta.unlocked_room_ids[id] = true
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(viewport_width, roundi(viewport_width * 9.0 / 16.0))
	await settle()
	game.pending_doctrines.assign(["industry", "biosphere"])
	game.rng.seed = 4404
	game._confirm_doctrines()
	game._set_paused(true)
	game.orbit.rng.seed = 4404
	game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
	game.draw_pile.assign(["storage_bay", "solar_array", "quarantine_cell"])
	build("solar_array", Vector2i(19, 20), 2)
	build("mining_drone_bay", Vector2i(20, 19))
	build("hydroponics_bay", Vector2i(21, 20))
	game._advance_cycle()
	game._advance_cycle()
	build("quarantine_cell", Vector2i(22, 20))
	game.selected_card_id = ""
	game.hover_cell = Vector2i(21, 20)
	game._refresh_all()
	await settle()
	game._fit_station_view()
	expect(not game.meta.discovered_synergy_ids.has("substrate_recovery"), "Placement does not reveal nursery recipe")
	await capture("01-undiscovered")
	for cycle_index in range(3):
		game._advance_cycle()
		expect(game.running, "Normal run survives discovery")
		expect(game.synergy_stabilization_progress.get("substrate_recovery", 0) == cycle_index + 1, "Consecutive functioning progress")
		await capture("02-discovery-cycle-%d" % (cycle_index + 1))
	expect(game.meta.unlocked_room_ids.has("mycelium_nursery"), "Nursery earned through three functioning cycles")
	expect(game.draw_pile.back() == "mycelium_nursery", "Prototype on live deck")
	game._discard_card(str(game.hand[0]))
	expect(game.hand.has("mycelium_nursery"), "Normal reroll draws prototype")
	await capture("03-prototype")
	game._on_card_pressed("mycelium_nursery")
	# Window mouse queries use the native cursor, not only injected GUI events.
	# Restore its original screen position immediately after preview captures.
	var target := Vector2i(23, 20)
	var original_pointer := DisplayServer.mouse_get_position()
	var motion := InputEventMouseMotion.new()
	motion.position = game.grid_view.get_global_transform_with_canvas() * game._cell_center(target)
	root.warp_mouse(motion.position)
	root.push_input(motion, true)
	await settle()
	var actual: Vector2 = game.grid_view.get_local_mouse_position() / game.get_cell_size()
	print("PREVIEW POINTER: event=%s actual_cell=%s target=%s" % [motion.position, actual, target])
	expect(Vector2i(floori(actual.x), floori(actual.y)) == target, "Preview pointer reaches target cell")
	for q in range(4):
		expect(game.selected_rotation == q, "Rotate action advances preview")
		expect(game.get_placement_problem("mycelium_nursery", target).is_empty() == (q != 3), "Preview validity follows rotated west port")
		await capture("04-preview-q%d" % q)
		game._rotate_selected_room()
	DisplayServer.warp_mouse(original_pointer)
	build("mycelium_nursery", target)
	game.selected_card_id = ""
	game.hover_cell = target
	game._advance_cycle()
	expect(game.powered_room_cells.has(target), "Paid nursery functions in real economy")
	game._fit_station_view()
	await capture("05-built-functioning")
	game._toggle_inspected_room()
	expect(not game.powered_room_cells.has(target), "Inspector suspension stops nursery")
	await capture("06-suspended")
	game._toggle_inspected_room()
	expect(not game.occupied[target].get("suspended", false), "Inspector resumes nursery")
	var save: String = game.meta.save_path
	game.free()
	if FileAccess.file_exists(save):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save))
	print("NURSERY PROGRESSION %s: paid foundations, full cycles, earned prototype, four previews, paid functioning nursery" % ("PASS" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
