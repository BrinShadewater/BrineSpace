extends SceneTree
const Insights = preload("res://scripts/station_ui_insights.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	Preferences.save_path = "user://operations_test.cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://operations_test.meta"
	game.run_save_path = "user://operations_test.loop"
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	root.add_child(game)
	current_scene = game
	game.tick_timer.stop()
	game.set_process(false)
	game._set_paused(true,false)
	game.hand.assign(["solar_array"])
	game.selected_card_id = "solar_array"
	game.selected_rotation = 2
	game._on_grid_clicked(Vector2i(19,20))
	check(game.drone_fleet.reserved(Vector2i(19,20)), "Queue contains actual paid placement")
	check(Insights.construction(game)[0].contains("PAUSED"), "Queue explains global pause")
	game._refresh_construction_button()
	check(game.construction_button.text.contains("1"), "HUD reports paid orders")
	game._toggle_journal()
	game.journal_tabs.current_tab = 6
	game._refresh_archive()
	check(game.archive_label.text.contains("Materials already paid"), "Construction page renders order details")
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/operations-queue.png")
	game._locate_diagnostic_room("19,20")
	check(game.selected_room_cell == Vector2i(19,20) and not game._journal_is_open(), "Queue link locates unbuilt footprint")
	game.paused = false
	game._update_wreck_clearance(4.0)
	check(not Insights.construction(game)[0].contains("awaiting builder"), "Assigned builder reports live phase")
	for drone in game.drone_fleet.drones.values():
		if drone.order.is_empty(): continue
		drone.bootstrap = false
		game.powered_room_cells.erase(drone.home)
		check(Insights.construction(game)[0].contains("OFFLINE"), "Unpowered assigned builder explains blockage")
		drone.bootstrap = true
		drone["route_wait"] = true
		check(Insights.construction(game)[0].contains("ROUTE BLOCKED"), "Queue exposes blocked exterior route")
		drone["route_wait"] = false
	# The opening builder must thaw, walk to the doorway and weld the paid order.
	for frame in range(1200):
		game._process(0.1)
		if game.occupied.has(Vector2i(19,20)): break
	check(not game.drone_fleet.reserved(Vector2i(19,20)), "Completed order leaves queue")
	check(Insights.learning(game).is_empty(), "Unknown pattern names remain hidden")
	game.connected_synergy_links = [{"id":"closed_air_loop"}]
	game.meta.discovered_synergy_ids["closed_air_loop"] = true
	game.synergy_stabilization_progress["closed_air_loop"] = 2
	check(Insights.learning(game)[0].contains("2 of 3"), "Learned pattern exposes stabilization progress")
	game.meta.stabilized_synergy_ids["closed_air_loop"] = true
	check(Insights.learning(game).is_empty(), "Completed pattern leaves stabilization watch")
	var forecast: Dictionary = game._simulate_room_economy(true,game.cycle+1)
	forecast.offline = {Vector2i(20,20):"SUSPENDED",Vector2i(19,20):"NEEDS POWER"}
	var priorities: Array[String] = Insights.priorities(game,forecast)
	check(priorities.size()<=3 and not " ".join(priorities).contains("SUSPENDED"), "Priorities exclude deliberate holds and cap at three")
	check(" ".join(priorities).contains("19,20"), "Priority links to affected room")
	# Seeded draft sampling: all unlocked pool, actual build/deal methods.
	var unlocks := {}
	for id in game.RoomDatabaseScript.all_rooms():
		if id != "brine_core": unlocks[id] = true
	game.meta.unlocked_room_ids = unlocks
	var total_first_support := 0
	var worst_support := 0
	for seed_value in range(500):
		game.rng.seed = seed_value
		game._build_run_deck()
		var deck: Array = game.draw_pile.duplicate()
		deck.reverse()
		var first_support := deck.size()
		for i in range(deck.size()):
			if deck[i] in ["hydroponics_bay","life_support"]:
				first_support = i+1
				break
		total_first_support += first_support
		worst_support = maxi(worst_support,first_support)
		check(first_support<=3, "Food arrives in opening hand across seeds")
		check(deck.find("current_turbine")==3, "Second affordable generator follows the opening hand")
		check(deck.find("life_support")<6, "Oxygen support arrives in opening six cards")
		game._draw_hand()
		check(game.hand.has("solar_array") and game.hand.has("mining_drone_bay"), "Starting draft retains power and extraction")
	print("DRAFT SAMPLE: 500 full-pool seeds; first life-support/food card mean draw %.2f, worst %d" % [float(total_first_support)/500.0,worst_support])
	for path in [Preferences.save_path,game.meta.save_path,game.run_save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("STATION OPERATIONS: PASS" if failures==0 else "STATION OPERATIONS: %d failures" % failures)
	quit(0 if failures==0 else 1)
