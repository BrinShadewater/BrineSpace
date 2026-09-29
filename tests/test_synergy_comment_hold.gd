extends SceneTree
## BRINE's line about a new synergy waits until the discovery card is gone (owner playtest, Sept 29).
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	TitleSettings.save_path = "user://comment_hold_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://comment_hold_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://comment_hold_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	var id := "chilled_air_recovery"
	var key := "discovery/" + id
	game.crew_comms.seen.erase(key)
	game._handle_synergy_discovery(id)
	expect(not game.crew_comms.seen.has(key), "BRINE stays quiet while the discovery card is up")
	expect(game.held_comments.has("synergy:" + id), "The line is held for the card")
	game._finish_center_toast()
	expect(game.crew_comms.seen.has(key), "The line is spoken once the card is gone")
	expect(not game.held_comments.has("synergy:" + id), "Nothing is left held")
	# A card pushed out of a full queue must not swallow its line.
	for name in ["one", "two", "three", "four"]:
		game._queue_center_toast("FILLER " + name)
	game.held_comments["synergy:test"] = ["brine", "Held line.", "discovery/test"]
	game.toast_record_keys["FILLER two"] = "synergy:test"
	game._queue_center_toast("FILLER five")
	game._queue_center_toast("FILLER six")
	expect(not game.held_comments.has("synergy:test"), "An evicted card releases its line")
	print("SYNERGY COMMENT HOLD: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
