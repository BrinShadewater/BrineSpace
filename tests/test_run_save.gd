extends SceneTree
const Save = preload("res://scripts/run_save.gd")
const Main = preload("res://scenes/main.tscn")
const PATH := "user://brine_save_test.loop"
var failures := 0
func _init() -> void:
	call_deferred("_run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _run() -> void:
	var game = Main.instantiate()
	game.meta.save_path = "user://brine_save_test_meta.json"
	game.run_save_path = PATH
	root.add_child(game)
	current_scene = game
	check(game.running and not game.doctrine_layer.visible, "New Loop starts directly without selection")
	check(game.selected_doctrines.is_empty() and game.run_directives.is_empty(), "New loops have no scenarios or deadlines")
	var deck: Array = game.RunManagerScript.build_deck([], game.meta.unlocked_room_ids)
	# The current deck offers one unlocked rare specialist, not all three.
	var specialists := ["pressure_control","listening_post","isolation_vault"]
	var eligible_specialists := 0
	var dealt_specialists := 0
	for id in game.meta.unlocked_room_ids:
		if id in specialists:
			eligible_specialists += 1
			if deck.has(id): dealt_specialists += 1
		elif id != "brine_core" and not game.RoomDatabaseScript.get_room(str(id)).is_empty():
			check(deck.has(id), "Neutral draft includes unlocked blueprint " + str(id))
	check(dealt_specialists == mini(1,eligible_specialists),"Neutral draft offers exactly one available rare specialist")
	game.run_directives = [{"name":"Legacy expired directive", "deadline":0, "target":99, "metric":"rooms"}]
	game._check_directive_progress()
	check(game.running and not game.summary_layer.visible, "Retired deadlines cannot end a loop")
	game.run_directives.clear()
	game._set_paused(true, false)
	game.selected_card_id = "solar_array"
	game.selected_rotation = 2
	game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
	game._on_grid_clicked(Vector2i(19, 20))
	check(game.drone_fleet.reserved(Vector2i(19,20)), "Paid placement must reserve construction before completion")
	game.paused = false
	# Opening orders now require the architect's real approach and work updates.
	for frame in range(1200):
		game._process(.1)
		if game.placed_rooms.size()==2: break
	game.paused = true
	check(game.placed_rooms.size() == 2, "Paid placement fixture should build a room")
	if game.placed_rooms.size()!=2:
		print("BUILD DIAGNOSTIC ",game.drone_fleet.orders," hardware=",game.hardware," crew=",game.recovered_crew)
		for actor in [game.bill_npc,game.veld_npc,game.branforth_npc]: print(actor.activity," active=",actor.active," foot=",actor.foot," goal=",actor.goal)
		quit(1)
		return
	game.cycle = 7
	game.reroll_recovery_progress = 2
	game.synergy_stabilization_progress = {"test_pattern": 2}
	game.placed_rooms[1]["suspended"] = true
	check(Save.write(game, PATH) == OK, "Save should write successfully")
	var data := Save.read(PATH)
	check(not data.is_empty(), "Checkpoint must load")
	var expected_resources: Dictionary = game.resources.duplicate(true)
	check(not Save.restore(game, {}), "Empty checkpoint must fail without throwing")
	check(not Save.restore(game, {"state": {}}), "Incomplete checkpoint must fail without throwing")
	check(game.resources == expected_resources, "Rejected checkpoint must preserve current resources")
	var expected_hand: Array = game.hand.duplicate()
	var expected_rng: int = game.rng.state
	game.resources.metal = 0
	game.hand.clear()
	game.placed_rooms.clear()
	data.state.selected_doctrines = ["industry", "biosphere"]
	data.state.run_directives = [{"name":"Legacy", "deadline":0}]
	check(Save.restore(game, data), "Checkpoint should restore")
	check(game.selected_doctrines.is_empty() and game.run_directives.is_empty(), "Old checkpoint scenarios are retired on Continue")
	check(game.cycle == 7 and game.reroll_recovery_progress == 2, "Cycle and reroll recovery must survive")
	check(game.resources == expected_resources and game.hand == expected_hand, "Resources and draft must survive")
	check(game.placed_rooms.size() == 2 and game.occupied.size() == 2, "Station and occupancy must restore")
	check(game.placed_rooms[1].suspended, "Room suspension must survive")
	check(game.synergy_stabilization_progress.test_pattern == 2, "Pattern progress must survive")
	check(game.rng.state == expected_rng, "64-bit RNG state must survive exactly")
	check(game.paused and not game.doctrine_layer.visible, "Continue must resume the station paused")
	check(game.tick_timer.time_left > 0 and game.tick_timer.time_left <= game._cycle_wait_seconds(), "Partial cycle timer must survive")
	check(Save.write(game, PATH) == OK, "Second save should keep a backup")
	var corrupt := FileAccess.open(PATH, FileAccess.WRITE)
	corrupt.store_string("damaged")
	corrupt.close()
	check(not Save.read(PATH).is_empty(), "Damaged checkpoint should recover backup")
	check(Save.read(PATH).get("_recovered_backup", false), "Backup recovery must be exposed to the title UI")
	check(Save.read(PATH).get("saved_at", 0) > 0, "New checkpoints must retain their save time")
	check(Save.write(game, "user://missing-save-directory/checkpoint") != OK, "Write failure must be reported")
	game.testing_free_build = true
	check(Save.write(game, PATH) == ERR_UNAVAILABLE, "Fixtures must not overwrite real checkpoints")
	game.testing_free_build = false
	# A fresh scene consumes the checkpoint, as the title's Continue action does.
	check(Save.write(game, PATH) == OK, "Checkpoint should be ready for title Continue")
	root.remove_child(game)
	game.free()
	var title = load("res://scenes/title_screen.tscn").instantiate()
	title.run_save_path = PATH
	root.add_child(title)
	current_scene = title
	check(title.continue_button.visible, "Title must offer Continue for a valid save")
	if DisplayServer.get_name() != "headless":
		root.size = Vector2i(1600, 900)
		await create_timer(0.5).timeout
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/title-continue.png")
	title.continue_button.pressed.emit()
	await create_timer(0.5).timeout
	game = current_scene
	game.meta.save_path = "user://brine_save_test_meta.json"
	check(Save.pending.is_empty(), "Continue request must be consumed only once")
	check(game.cycle == 7 and game.placed_rooms.size() == 2 and game.paused, "Fresh scene must resume checkpoint instead of resetting it")
	check(game.run_save_path == PATH, "Continue must retain its checkpoint destination")
	game._open_menu()
	if DisplayServer.get_name() != "headless":
		await create_timer(0.2).timeout
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/save-menu.png")
	Save.clear_run(game.run_save_id, PATH)
	check(Save.read(PATH).is_empty(), "Completing a loop must clear checkpoint and backup")
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(PATH + suffix):
			DirAccess.remove_absolute(PATH + suffix)
	if FileAccess.file_exists(game.meta.save_path):
		DirAccess.remove_absolute(game.meta.save_path)
	print("SAVE GAME: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(failures)
