extends SceneTree
const MainScene = preload("res://scenes/main.tscn")
const Save = preload("res://scripts/run_save.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		if failures < 15: push_error(message)

func _init() -> void: call_deferred("run")

func run() -> void:
	var game = MainScene.instantiate()
	var prefix := "user://branforth_crew_%d" % OS.get_process_id()
	game.meta.save_path = prefix + "_meta.json"
	game.run_save_path = prefix + ".loop"
	game.Preferences.save_path = prefix + ".cfg"
	root.add_child(game)
	current_scene = game
	game.architect_run = {} # Existing three-person encounter; startup is tested separately.
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.occupied.clear()
	game.placed_rooms.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	for offset in range(3):
		var room: Dictionary = game.RoomDatabaseScript.get_room("corridor" if offset == 1 else "storage_bay").duplicate(true)
		room.pos = origin + Vector2i(offset, 0)
		room.rotation = 1 if offset == 1 else 0
		game.occupied[room.pos] = room
		game.placed_rooms.append(room)
		game.powered_room_cells[room.pos] = true
	game.test_walker_cell = origin + Vector2i.RIGHT
	var center := (Vector2(game.test_walker_cell) + Vector2.ONE * 0.5) * 384.0
	var bill = game.bill_npc
	var veld = game.veld_npc
	var engineer = game.branforth_npc
	bill.rebuild(game)
	veld.rebuild(game)
	engineer.rebuild(game)
	for info in [[bill, -1], [veld, 1]]:
		var npc = info[0]
		npc.active = true
		npc.foot = center + Vector2(info[1] * 100, 0)
		npc.path = PackedVector2Array([center - Vector2(info[1] * 100, 0)])
		npc.goal = "curiosity"
		npc.goal_cell = game.test_walker_cell
		npc.timer = 0.0
		npc.state = "walk"
	engineer.active = true
	engineer.foot = center + Vector2(0, 32)
	engineer.path = PackedVector2Array([center + Vector2(150, 32)])
	engineer.goal = "curiosity"
	engineer.goal_cell = game.test_walker_cell
	engineer.state = "walk"
	engineer.decision_rng.seed = 953
	game.rng.seed = 951
	veld.decision_rng.seed = 952
	var native := DisplayServer.get_name() != "headless"
	var capture_dir := "res://character/chief-engineer-branforth-v1/qa/native/crew-passing"
	if native:
		DirAccess.make_dir_recursive_absolute(capture_dir)
		root.mode = Window.MODE_WINDOWED
		root.borderless = false
		root.size = Vector2i(1600, 900)
		game.selected_card_id = ""
		game.hover_cell = Vector2i(-1, -1)
		game._refresh_all()
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
		for unused in range(4): await process_frame
		game._center_grid_on_station_now()
		for unused in range(4): await process_frame
	var crossed_bill := false
	var crossed_veld := false
	var minimum := INF
	var engineer_travel := 0.0
	for i in range(600):
		game.visual_time_seconds += 0.1
		var old_engineer: Vector2 = engineer.foot
		var old_bill: Vector2 = bill.foot
		var old_veld: Vector2 = veld.foot
		game._update_test_walker(0.1)
		engineer_travel += old_engineer.distance_to(engineer.foot)
		check(engineer.segment_clear(old_engineer, engineer.foot), "Engineer swept movement clears props/walls")
		check(old_engineer.distance_to(engineer.foot) <= 4.601, "Engineer does not teleport")
		for peer in [bill, veld]:
			check(engineer.foot.distance_to(peer.foot) >= 19.99, "Engineer maintains both peer clearances")
		minimum = minf(minimum, bill.foot.distance_to(veld.foot))
		check(bill.foot.distance_to(veld.foot) >= 19.99, "Crew feet overlap")
		check(bill.segment_clear(old_bill, bill.foot) and veld.segment_clear(old_veld, veld.foot), "Avoidance clips room geometry")
		check(old_bill.distance_to(bill.foot) <= 4.601 and old_veld.distance_to(veld.foot) <= 4.601, "Avoidance teleports")
		crossed_bill = crossed_bill or bill.foot.x > center.x + 50
		crossed_veld = crossed_veld or veld.foot.x < center.x - 50
		if native and i in [0, 17, 25, 35, 45, 65]:
			game.grid_view.queue_redraw()
			for unused in range(3): await process_frame
			await RenderingServer.frame_post_draw
			var image := root.get_texture().get_image()
			check(image.get_size() == Vector2i(1600, 900) and not game.menu_open, "Native capture is unobstructed at requested size")
			image.save_png(capture_dir.path_join("passing-%03d.png" % i))
			var size: float = game.get_cell_size()
			var room_rect := Rect2(Vector2(origin + Vector2i.RIGHT) * size, Vector2.ONE * size)
			var screen: Rect2 = root.get_stretch_transform() * game.grid_view.get_global_transform_with_canvas() * room_rect
			image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO, image.get_size())))).save_png(capture_dir.path_join("passing-%03d-crop.png" % i))
	check(crossed_bill and crossed_veld, "Both crew pass in a head-on narrow corridor encounter")
	check(engineer_travel > 200.0, "Third crew member makes progress through traffic")
	# Save partway through an action, not only at an idle endpoint.
	game.visual_time_seconds = 100.0
	game.grid_view._get_human_frame("kneel", "east")
	game.grid_view.veld_player.frame("kneel", "east", 100.0, game.get_dr_veld_position() / game.get_cell_size())
	game.visual_time_seconds = 100.44
	var bill_pose: PackedByteArray = game.grid_view._get_human_frame("kneel", "east").get_image().get_data()
	var veld_pose: PackedByteArray = game.grid_view.veld_player.frame("kneel", "east", 100.44, game.get_dr_veld_position() / game.get_cell_size()).get_image().get_data()
	game.grid_view.branforth_player.frame("kneel", "east", 100.0, game.get_chief_branforth_position() / game.get_cell_size())
	var engineer_pose: PackedByteArray = game.grid_view.branforth_player.frame("kneel", "east", 100.44, game.get_chief_branforth_position() / game.get_cell_size()).get_image().get_data()
	var expected_engineer: Dictionary = engineer.snapshot()
	var expected_playback: Dictionary = game.grid_view.crew_playback_snapshot()
	# Actual disk serialization must retain vector paths and 64-bit RNG state.
	var expected_bill: Dictionary = bill.snapshot()
	var expected_veld: Dictionary = veld.snapshot()
	check(Save.write(game, game.run_save_path) == OK, "Crew checkpoint writes")
	var data := Save.read(game.run_save_path)
	check(not data.is_empty(), "Crew checkpoint reads")
	engineer.needs.hunger = 99.0
	game.grid_view.branforth_player.phase = 777.0
	bill.needs.hunger = 99.0
	veld.needs.fatigue = 99.0
	game.grid_view.human_animation_phase = 777.0
	game.grid_view.veld_player.phase = 777.0
	check(Save.restore(game, data), "Crew checkpoint restores")
	check(game.bill_npc.snapshot() == expected_bill, "Bill position, needs, route and activity survive Continue")
	check(game.veld_npc.snapshot() == expected_veld, "Veld position, needs, route, activity and RNG survive Continue")
	check(game.branforth_npc.snapshot() == expected_engineer, "Engineer state and RNG survive disk round trip")
	check(game.grid_view.branforth_player.frame("kneel", "east", 100.44, game.get_chief_branforth_position() / game.get_cell_size()).get_image().get_data() == engineer_pose, "Engineer resumes saved action frame")
	check(game.paused, "Continue remains paused")
	check(game.grid_view.crew_playback_snapshot() == expected_playback, "Both animation clocks survive Continue")
	check(game.grid_view._get_human_frame("kneel", "east").get_image().get_data() == bill_pose, "Bill resumes on the saved action frame")
	check(game.grid_view.veld_player.frame("kneel", "east", 100.44, game.get_dr_veld_position() / game.get_cell_size()).get_image().get_data() == veld_pose, "Veld resumes on the saved action frame")
	var malformed: Dictionary = data.duplicate(true)
	malformed.crew.branforth.needs.hunger = NAN
	var before: Dictionary = game.veld_npc.snapshot()
	check(not Save.restore(game, malformed), "Malformed crew checkpoint is rejected")
	check(game.veld_npc.snapshot() == before, "Rejected checkpoint does not mutate crew")
	var legacy: Dictionary = data.duplicate(true)
	legacy.crew.erase("branforth")
	legacy.crew.playback.erase("branforth")
	check(Save.restore(game, legacy), "Two-crew checkpoint remains compatible")
	check(not game.branforth_npc.active, "Old checkpoint initializes engineer fresh")
	legacy.erase("crew")
	check(Save.restore(game, legacy), "Older checkpoint without crew remains compatible")
	check(not game.bill_npc.active and not game.veld_npc.active, "Older checkpoint starts fresh NPC loops")
	game._update_test_walker(0.1)
	check(game.bill_npc.foot.distance_to(game.veld_npc.foot) >= 19.99, "Legacy spawn does not overlap")
	for path in [game.meta.save_path, game.Preferences.save_path, game.run_save_path, game.run_save_path + ".bak", game.run_save_path + ".tmp"]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	game.free()
	print("BRANFORTH THREE CREW: %s; minimum separation %.2f" % ["PASS" if failures == 0 else "%d failures" % failures, minimum])
	quit(0 if failures == 0 else 1)
