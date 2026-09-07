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
	if id == "tidal_condenser":
		for resource in Rooms.get_room(id).cost:
			expect(game.resources[resource] == before[resource] - Rooms.get_room(id).cost[resource], "Exact condenser purchase cost: " + resource)

func run() -> void:
	if capture_dir.is_empty() or DirAccess.dir_exists_absolute(capture_dir):
		push_error("Use a new --capture-dir")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.run_save_path = "user://brine_condenser_loop_fixture_%d.json"%OS.get_process_id()
	game.meta.save_path = "user://brine_condenser_progression_%d_%d.json" % [viewport_width,OS.get_process_id()]
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
	game.hand.assign(["reactor", "mining_drone_bay", "life_support"])
	game.draw_pile.assign(["storage_bay", "solar_array", "hydroponics_bay"])
	build("reactor", Vector2i(19,20))
	build("mining_drone_bay", Vector2i(20,19))
	game._advance_cycle()
	game._advance_cycle()
	build("life_support", Vector2i(18,20))
	game.selected_card_id = ""
	game.hover_cell = Vector2i(18, 20)
	game._refresh_all()
	await settle()
	game._fit_station_view()
	expect(not game.meta.discovered_synergy_ids.has("thermal_reclamation"), "Placement does not reveal condenser recipe")
	await capture("01-undiscovered")
	for cycle_index in range(3):
		game._advance_cycle()
		expect(game.running, "Normal run survives discovery")
		expect(game.synergy_stabilization_progress.get("thermal_reclamation", 0) == cycle_index + 1, "Consecutive functioning progress")
		await capture("02-discovery-cycle-%d" % (cycle_index + 1))
	expect(game.meta.unlocked_room_ids.has("tidal_condenser"), "Condenser earned through three functioning cycles")
	expect(game.draw_pile.back() == "tidal_condenser", "Prototype on live deck")
	game._discard_card(str(game.hand[0]))
	expect(game.hand.has("tidal_condenser"), "Normal reroll draws prototype")
	await capture("03-prototype")
	var target := Vector2i(17,20)
	build("tidal_condenser", target)
	game.selected_card_id = ""
	game.hover_cell = target
	game._advance_cycle()
	expect(game.powered_room_cells.has(target), "Paid condenser functions in real economy")
	game._fit_station_view()
	await capture("05-built-functioning")
	game._toggle_inspected_room()
	expect(not game.powered_room_cells.has(target), "Inspector suspension stops condenser")
	await capture("06-suspended")
	game._toggle_inspected_room()
	expect(not game.occupied[target].get("suspended", false), "Inspector resumes condenser")
	var save: String = game.meta.save_path
	game.free()
	if FileAccess.file_exists(save):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save))
	print("CONDENSER PROGRESSION %s: paid foundations, full cycles, earned prototype, paid functioning condenser and inspector suspension" % ("PASS" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)

