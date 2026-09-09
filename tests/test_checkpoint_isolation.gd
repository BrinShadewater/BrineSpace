extends SceneTree
const Save = preload("res://scripts/run_save.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://checkpoint-isolation.meta"
	game.run_save_path = "user://checkpoint-isolation.loop"
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = true
	var checkpoint := Save.capture(game)
	var expected := checkpoint.duplicate(true)
	game.resources.metal += 1
	game.hand.clear()
	game.placed_rooms[0].water_level = 0.4
	check(checkpoint == expected, "Captured checkpoint must not change with live resources, draft or rooms")
	check(Save.restore(game, expected), "Independent checkpoint restores")
	var pristine := expected.duplicate(true)
	game.resources.metal += 1
	game.hand.clear()
	game.placed_rooms[0].water_level = 0.6
	check(expected == pristine, "Restored station must not mutate its source checkpoint")
	check(Save.restore(game, pristine), "Same checkpoint remains reusable")
	check(game.resources.metal == pristine.state.resources.metal and game.hand == pristine.state.hand, "Repeated restore returns original resources and draft")
	check(game.placed_rooms[0].get("water_level", 0.0) == pristine.state.placed_rooms[0].get("water_level", 0.0), "Repeated restore returns original water level")
	for change in [["time_speed_index", -1], ["time_speed_index", 3], ["grid_zoom", NAN], ["grid_zoom", 0.0], ["visual_time_seconds", INF]]:
		var invalid := pristine.duplicate(true)
		invalid.state[change[0]] = change[1]
		var bytes := var_to_bytes(invalid)
		var file := FileAccess.open(game.run_save_path, FileAccess.WRITE)
		file.store_string(bytes.hex_encode().sha256_text()+"\n")
		file.store_buffer(bytes)
		file.close()
		check(Save.read(game.run_save_path).is_empty(), "Invalid saved control value is rejected: "+str(change[0]))
		check(not Save.restore(game,invalid) and not Save.last_error.is_empty(), "Direct restore rejects invalid controls with a reason")
		check(Save.capture(game).state == pristine.state, "Rejected controls leave the station untouched")
	var invalid_clock := pristine.duplicate(true)
	invalid_clock.timer_left = INF
	check(not Save.restore(game,invalid_clock), "Infinite saved cycle timer is rejected")
	check(Save.restore(game,pristine) and Save.last_error.is_empty(), "Successful recovery clears an earlier restore error")
	var backup_bytes := var_to_bytes(pristine)
	var backup := FileAccess.open(game.run_save_path+".bak",FileAccess.WRITE)
	backup.store_string(backup_bytes.hex_encode().sha256_text()+"\n")
	backup.store_buffer(backup_bytes)
	backup.close()
	check(Save.read(game.run_save_path).get("_recovered_backup",false), "Invalid primary control state falls back to a valid backup")
	print("CHECKPOINT ISOLATION: ", "PASS" if failures == 0 else "FAIL")
	quit(failures)
