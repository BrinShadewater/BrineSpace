extends SceneTree
const MainScene = preload("res://scenes/main.tscn")
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _init() -> void: call_deferred("run")

func run() -> void:
	var player = Player.new()
	player.load_manifest("res://character/chief-engineer-branforth-v1/final/manifest.json")
	check(player.frames.size() == 12, "Twelve animation states load")
	for key in player.frames:
		check(player.frames[key].size() == 6, key + " has six frames")
		for texture in player.frames[key]:
			check(texture.get_size() == Vector2(92, 92), "Crew frame geometry")
			check(texture.get_meta("crew_frame_92", false), "Crew renderer tag")
	var resource: SpriteFrames = load("res://character/chief-engineer-branforth-v1/final/chief-engineer-branforth.tres")
	check(resource.get_animation_names().size() == 12, "Native SpriteFrames imports")
	var first = player.frame("walk", "east", 1.0, Vector2.ZERO)
	check(player.frame("walk", "east", 2.0, Vector2.ZERO) == first, "Stationary gait holds")
	player.frame("walk", "east", 3.0, Vector2(0.04, 0))
	check(player.phase > 0.0, "Travel advances gait")
	var phase: float = player.phase
	player.frame("walk", "east", 3.0, Vector2(0.04, 0))
	check(player.phase == phase, "Repeated draws do not advance gait")
	player.frame("idle", "north", 4.0, Vector2(0.04, 0))
	check(player.phase == 0.0, "State changes reset playback")
	player.frame("interact", "east", 5.0, Vector2.ZERO)
	check(player.frame("interact", "east", 15.0, Vector2.ZERO) == player.frames["interact-east"].back(), "Scanner one-shot holds its endpoint")
	for pair in [["idle-east",0,"kneel-east",0],["kneel-east",5,"repair-east",0],["repair-east",5,"stand-east",0],["stand-east",5,"idle-east",0]]:
		check(player.frames[pair[0]][pair[1]].get_image().get_data() == player.frames[pair[2]][pair[3]].get_image().get_data(), "Work transitions share exact endpoint pixels")
	var game = MainScene.instantiate()
	game.Preferences.save_path = "user://branforth_test_settings_%d.cfg" % OS.get_process_id()
	game.meta.save_path = "user://branforth_test_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://branforth_test_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.occupied.clear()
	game.placed_rooms.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	for info in [["storage_bay",origin],["maintenance_bay",origin+Vector2i.RIGHT],["hydroponics_bay",origin+Vector2i.DOWN],["crew_hab",origin+Vector2i.LEFT]]:
		game._place_room(info[0], info[1], true)
		game.powered_room_cells[info[1]] = true
	game.test_walker_cell = origin
	game.branforth_npc.decision_rng.seed = 5012
	game._update_test_walker(0.1)
	var branforth = game.branforth_npc
	check(game.has_chief_branforth() and game.has_test_walker(), "Both characters spawn")
	check(game.bill_npc != branforth, "Independent NPC instances")
	check(game.bill_npc.needs != branforth.needs, "Independent needs")
	check(branforth.foot.distance_to(game.bill_npc.foot) > 20, "Separate spawn positions")
	var station_rng: int = game.rng.state
	branforth.path.clear()
	branforth.goal = ""
	branforth.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":95.0}
	branforth.choose_goal(game)
	check(game.rng.state == station_rng, "Branforth decisions do not consume station RNG")
	check(branforth.goal == "maintenance" and branforth.goal_cell != origin, "Engineering work chooses a service room instead of storage")
	var states := {}
	var moved_bill := false
	var moved_branforth := false
	var b0: Vector2 = game.bill_npc.foot
	var v0: Vector2 = branforth.foot
	for i in range(2400):
		var old: Vector2 = branforth.foot
		game._update_test_walker(0.1)
		check(branforth.segment_clear(old, branforth.foot), "Branforth movement clears room props and walls")
		check(old.distance_to(branforth.foot) <= 4.601, "Branforth does not teleport")
		states[branforth.state] = true
		moved_bill = moved_bill or game.bill_npc.foot.distance_to(b0) > 20
		moved_branforth = moved_branforth or branforth.foot.distance_to(v0) > 20
	check(moved_bill and moved_branforth, "Both characters move independently")
	for state in ["walk", "kneel", "repair", "stand", "interact"]:
		check(states.has(state), "Autonomous Branforth plays " + state)
	var paused_foot: Vector2 = branforth.foot
	var paused_needs: Dictionary = branforth.needs.duplicate()
	game._process(5.0)
	check(branforth.foot == paused_foot and branforth.needs == paused_needs, "Pause freezes Branforth")
	var bill_phase: float = game.grid_view.human_animation_phase
	game.grid_view._get_branforth_frame(game)
	check(game.grid_view.human_animation_phase == bill_phase, "Branforth playback leaves Bill's clock untouched")
	game.bill_npc.foot = (Vector2(origin + Vector2i.LEFT) + Vector2.ONE * 0.5) * 384
	game.veld_npc.active = false
	var connected: Vector2i = game._connected_neighbor_cells(origin)[0]
	branforth.foot = (Vector2(origin + connected) * 0.5 + Vector2.ONE * 0.5) * 384
	check(game.grid_view._door_frame_for_pair(game, origin, connected) == game.grid_view.DOOR_OPEN_FRAMES - 1, "Branforth opens a connected door independently of Bill")
	check(game.grid_view._door_frame_for_pair(game, origin, origin + Vector2i.UP) == 0, "Missing room cannot open a door")
	for path in [game.meta.save_path,game.run_save_path,game.Preferences.save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	game.free()
	print("BRANFORTH: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(0 if failures == 0 else 1)
