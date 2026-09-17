extends SceneTree
## Locking a room's doors (owner call, Sept 16): crew can't route through it in either
## direction, its doors stay shut, and unlocking restores the route.
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func route_length(game, actor, from: Vector2i, to: Vector2i) -> int:
	if actor.topology(game) != actor.signature: actor.rebuild(game)
	var start: int = actor.nearest_in_room((Vector2(from) + Vector2.ONE * 0.5) * 384.0, from, false)
	var goal: int = actor.nearest_in_room((Vector2(to) + Vector2.ONE * 0.5) * 384.0, to, false)
	if start < 0 or goal < 0: return -1
	return actor.route_between(start, goal).size()

func run() -> void:
	var prefix := "user://room_lock_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix + ".meta"
	game.run_save_path = prefix + ".loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.crew_comms.archive_path = prefix + ".comms.json"
	game.set_process(false); game.tick_timer.stop()
	game.testing_free_build = true
	for cell in [Vector2i(20,19), Vector2i(20,18)]:
		game.wrecks.erase(cell)
		game.selected_rotation = 0
		game._place_room("corridor", cell, true, true)
	check(game.occupied.has(Vector2i(20,18)) and game.occupied.has(Vector2i(20,19)), "Fixture corridors are built")
	var actor = game.bill_npc
	var open := route_length(game, actor, Vector2i(20,20), Vector2i(20,18))
	check(open > 0, "Crew can route from the core through the corridor: %d" % open)
	game.selected_room_cell = Vector2i(20,19)
	game.running = true
	game._refresh_inspector()
	check(game.room_lock_button.visible and game.room_lock_button.text == "LOCK DOORS", "The inspector offers LOCK DOORS")
	game.room_lock_button.set_meta("cell", Vector2i(20,19))
	game._toggle_inspected_room_lock()
	check(game.occupied[Vector2i(20,19)].get("doors_locked", false), "The switch locks the room")
	check(route_length(game, actor, Vector2i(20,20), Vector2i(20,18)) <= 0, "No crew route passes through a locked room")
	check(route_length(game, actor, Vector2i(20,18), Vector2i(20,20)) <= 0, "Locked doors block crew in the other direction too")
	check(game.grid_view._compute_door_frame_for_pair(game, Vector2i(20,20), Vector2i(20,19)) == 0, "A locked room's doors stay shut")
	game._refresh_inspector()
	check(game.room_lock_button.text == "UNLOCK DOORS", "The switch then offers UNLOCK DOORS")
	game._toggle_inspected_room_lock()
	check(route_length(game, actor, Vector2i(20,20), Vector2i(20,18)) > 0, "Unlocking restores the route")
	game.queue_free()
	await process_frame
	for suffix in [".cfg", ".meta", ".loop", ".comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(prefix + suffix)
	print("ROOM LOCK %s" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
