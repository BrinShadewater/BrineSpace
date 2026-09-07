extends SceneTree

# Deterministic draft order; purchases, doors, cycle economy, rewards and input
# handlers are the real game paths. Loaded meta is cleared before play, and all
# test writes go to an isolated save path, never the player's save.
const MainScene := preload("res://scenes/main.tscn")
const Rooms := preload("res://scripts/room_database.gd")
const Orbit := preload("res://scripts/orbit_manager.gd")
const Synergies := preload("res://scripts/synergy_manager.gd")
const Discovery := preload("res://scripts/discovery_manager.gd")
const SAVE_PATH := "user://brine_polish_scene_test.json"
var failures := 0
var capture_dir := ""
var viewport_width := 1600
var game

func _init() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-dir="):
			capture_dir = argument.trim_prefix("--capture-dir=")
		elif argument.begins_with("--viewport-width="):
			viewport_width = int(argument.trim_prefix("--viewport-width="))
	call_deferred("_run")

func _run() -> void:
	seed(4404)
	game = MainScene.instantiate()
	game.meta.save_path = SAVE_PATH
	game.meta.unlocked_room_ids.clear()
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.doctrine_mastery.clear()
	game.meta.total_research_points = 0
	game.meta.total_victories = 0
	for id in Rooms.STARTING_UNLOCKS:
		game.meta.unlocked_room_ids[id] = true
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(viewport_width, roundi(viewport_width * 9.0 / 16.0))
	await _settle()
	await _capture("01-doctrines-1600")
	game.pending_doctrines.assign(["industry", "biosphere"])
	game.rng.seed = 4404
	game._confirm_doctrines()
	game._set_paused(true)
	game.orbit.rng.seed = 4404
	game.orbit.current_poi = Orbit.POIS[0].duplicate(true)
	game.orbit.timer = 6
	game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
	game.draw_pile.assign(["life_support", "solar_array", "storage_bay"])
	_build("solar_array", Vector2i(19, 20), 2)
	_build("mining_drone_bay", Vector2i(20, 19))
	_build("hydroponics_bay", Vector2i(21, 20))
	_cycle_with_drone_returns()
	_build("life_support", Vector2i(21, 21), 2)
	_build("solar_array", Vector2i(21, 19))
	game.selected_card_id = ""
	game.hover_cell = Vector2i(21, 20)
	game._refresh_all()
	game._fit_station_view()
	_drain_feedback()
	_expect(game.meta.discovered_synergy_ids.is_empty(), "placement alone must not teach a pattern")
	await _capture("02-unknown-1600")
	_cycle_with_drone_returns()
	_expect(game.meta.discovered_synergy_ids.has("closed_air_loop"), "real purchases reveal a functioning pattern")
	_expect(not game.discovery_bursts.is_empty(), "discovery creates room-local visual feedback")
	await _capture("03-discovery-1600")
	_drain_feedback()
	_cycle_with_drone_returns()
	_expect(game.synergy_stabilization_progress.get("closed_air_loop", 0) == 2, "second functioning cycle is still stabilizing")
	await _capture("03b-stabilizing-1600")
	_cycle_with_drone_returns()
	_expect(game.meta.unlocked_room_ids.has("biodome"), "three cycles decrypt the real blueprint")
	_expect(game.draw_pile.back() == "biodome", "the prototype is placed on top of the live deck")
	game._discard_card(str(game.hand[0]))
	_expect(game.hand.has("biodome"), "a normal reroll draws the prototype")
	await _capture("04-prototype-1600")
	_drain_feedback()
	while not game._can_afford(Rooms.get_room("biodome")["cost"]) and game.cycle < 12 and game.running:
		_cycle_with_drone_returns()
	_build("biodome", Vector2i(20, 21), 1) # Connect east to Life Support; old location contains a seeded cryo ward.
	for _tick in range(3):
		_cycle_with_drone_returns()
	_expect(game.meta.unlocked_room_ids.has("bio_lab"), "building the prototype starts a second discovery chain")
	_expect(game.resources["water"] >= 0, "the expanded bio economy remains water-positive")
	_expect(game.running, "the station survives its two-step discovery chain")
	game.selected_card_id = ""
	game.hover_cell = Vector2i(21, 21)
	game._refresh_all()
	game._fit_station_view()
	_drain_feedback()
	game.visual_time_seconds = 0.35
	game.grid_view.queue_redraw()
	await _capture("05-expanded-1600")
	var hand_before: Array = game.hand.duplicate()
	var rerolls_before: int = game.rerolls_remaining
	game.reroll_button.grab_focus()
	game._toggle_journal()
	game._discard_all_cards()
	game._on_card_pressed("solar_array")
	_expect(game.hand == hand_before and game.rerolls_remaining == rerolls_before, "journal blocks the underlying draft controls")
	_expect(game.paused and game._journal_is_open(), "journal pauses the station")
	_expect(game.archive_label.text.contains("Biodome") and not game.archive_label.text.contains("Impossible Model"), "journal explains learned rewards without future recipe spoilers")
	await _capture("06-journal-1600")
	game._toggle_journal()
	_expect(game.paused, "closing journal restores a previously paused station")
	game._set_paused(false)
	game._toggle_journal()
	game._toggle_journal()
	_expect(not game.paused, "closing journal restores a previously running station")
	game._set_paused(true)
	game.hover_cell = Vector2i(21, 20)
	game.selected_card_id = ""
	game._refresh_inspector()
	game._toggle_inspected_room()
	_expect(not game.powered_room_cells.has(Vector2i(21, 20)), "suspension immediately stops a room's functioning effects")
	_cycle_with_drone_returns()
	_expect(game._active_synergy_link_count("closed_air_loop") == 0, "a suspended room cannot contribute a link")
	await _capture("07-dormant-1600")
	game._toggle_inspected_room()
	_cycle_with_drone_returns()
	_expect(game._active_synergy_link_count("closed_air_loop") == 1, "resuming restores a learned pattern on the next cycle")
	for resolution in [Vector2i(1280, 720), Vector2i(2560, 1440), Vector2i(1920, 1080)]:
		root.size = resolution
		await _settle()
		game._fit_station_view()
		await _capture("08-layout-%d" % resolution.x)
		_expect(game.get_node("Root/BottomHand").get_global_rect().end.x <= game.size.x + 1, "draft fits at %d" % resolution.x)
		_expect(game.journal_button.get_global_rect().end.x <= game.size.x + 1, "HUD fits at %d" % resolution.x)
	game.completed_directives.assign(["ONE", "TWO", "THREE"])
	game._show_reboot_summary("Sector secured. Your next experiment is waiting.", true)
	var research_before: int = game.meta.total_research_points
	var mastery_before: Dictionary = game.meta.doctrine_mastery.duplicate()
	for resolution in [Vector2i(1600, 900), Vector2i(2560, 1440), Vector2i(1920, 1080)]:
		root.size = resolution
		await _capture("09-victory-%d" % resolution.x)
	game._continue_expedition()
	_expect(game.running and game.expedition_mode and game._current_directive().is_empty(), "victory can continue without directive deadlines")
	game.cycle = 100
	game._check_directive_progress()
	_expect(game.running, "old directive deadlines cannot end an expedition")
	game._open_menu()
	game._end_expedition()
	_expect(not game.running and not game.menu_open and game.summary_layer.visible, "expedition can be concluded safely from the menu")
	_expect(game.meta.total_victories == 1 and game.meta.doctrine_mastery == mastery_before, "extended expedition cannot award victory/mastery twice")
	_expect(game.meta.total_research_points == research_before, "reopening the same summary cannot duplicate research")
	game._start_reboot_cycle()
	_expect(not game.expedition_mode and not game.run_rewards_recorded and game.discovery_bursts.is_empty(), "reboot clears transient state")
	_expect(game.meta.unlocked_room_ids.has("bio_lab"), "reboot retains learned blueprints")
	if not capture_dir.is_empty():
		for id in ["closed_air_loop", "field_clinic", "load_balancing", "core_diagnostics", "ore_buffer", "sterile_observation"]:
			await _capture_profile(id)
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))
	if failures == 0:
		print("Scene playtest passed: paid builds, two discoveries, prototype reuse, suspension, journal input, responsive layout, expedition and reboot.")
	else:
		push_error("Scene playtest failures: %d" % failures)
	quit(1 if failures > 0 else 0)

func _build(id: String, cell: Vector2i, rotation := 0) -> void:
	_expect(game.hand.has(id), "draft contains %s" % id)
	game._on_card_pressed(id)
	game.selected_rotation = rotation
	var problem: String = game.get_placement_problem(id, cell)
	_expect(problem.is_empty(), "build %s: %s" % [id, problem])
	if not problem.is_empty():
		return
	game._on_grid_clicked(cell)
	_expect(game.drone_fleet.reserved(cell),"purchased %s reserves its cell" % id)
	var was_paused: bool = game.paused
	game.paused = false
	# This fixture controls economy ticks explicitly; exercise the real builder
	# between assertions. Full elapsed-time pacing is covered by playtest_balance.
	for step in range(1200):
		if game.occupied.has(cell): break
		game._update_wreck_clearance(0.1)
	game.paused = was_paused
	_expect(game.occupied.has(cell), "purchased %s is built" % id)

func _cycle_with_drone_returns() -> void:
	game._advance_cycle()
	# The discrete-cycle fixture must wait for earned cargo before spending it.
	var was_paused: bool = game.paused
	game.paused = false
	game._update_wreck_clearance(20.0)
	game.paused = was_paused

func _settle() -> void:
	for _frame in range(4):
		await process_frame

func _drain_feedback() -> void:
	# Advance the real tween queue between accelerated test cycles.
	for _toast in range(24):
		if game.cascade_toast_tween != null and game.cascade_toast_tween.is_valid():
			game.cascade_toast_tween.custom_step(3.0)
		else:
			break
	game._update_discovery_bursts(1.3)

func _capture_profile(id: String) -> void:
	await _settle()
	game.doctrine_layer.visible = false
	game.running = true
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	game.offline_reasons.clear()
	game.meta.discovered_synergy_ids.clear()
	game.meta.discovered_synergy_ids[id] = true
	game.meta.stabilized_synergy_ids[id] = true
	var recipe := Synergies.get_synergy(id)
	for index in range(2):
		var room_id := str(recipe["rooms"][index])
		var cell := Vector2i(20 + index, 20)
		game._place_room(room_id, cell, true)
		for rotation in range(4):
			if game._room_doors(room_id, rotation).has("east" if index == 0 else "west"):
				game.occupied[cell]["rotation"] = rotation
				break
		game.powered_room_cells[cell] = true
	game._check_synergies()
	game.active_synergy_links = Discovery.functioning_links(game.connected_synergy_links, game.powered_room_cells)
	game.active_synergies = {id: recipe}
	game.hand.assign([str(recipe["rooms"][0]), str(recipe["rooms"][1])])
	game.selected_card_id = ""
	game.hover_cell = Vector2i(20, 20)
	game.visual_time_seconds = 0.35
	game._refresh_all()
	await _settle()
	game._fit_station_view()
	await _settle()
	var first_center: Vector2 = (Vector2(20, 20) + Vector2.ONE * 0.5) * game.get_cell_size()
	var visible_grid := Rect2(Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical), game.grid_scroll.size)
	_expect(visible_grid.has_point(first_center), "effect fixture must be on screen: " + id)
	await _capture("10-fx-" + str(recipe["fx_profile"]))
	if id == "closed_air_loop":
		game.visual_time_seconds = 1.15
		game.grid_view.queue_redraw()
		await _capture("11-fx-flow-next-frame")

func _capture(label: String) -> void:
	await _settle()
	if capture_dir.is_empty():
		return
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute(capture_dir)
	if label.ends_with("-1600") and not label.begins_with("09-"):
		label = label.replace("-1600", "-%d" % viewport_width)
	var path := capture_dir.path_join(label + ".png")
	var result := root.get_texture().get_image().save_png(path)
	_expect(result == OK, "capture saves " + label)
	print("Capture: ", path)

func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)
