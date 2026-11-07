extends SceneTree
## Owner playtest (Sept 17): every character died but the run went on (a Crew Hab's unseen
## survivor kept crew_count above zero), and nobody noticed them dying. The run ends once every
## recovered character is dead, and BRINE warns before a death and reports it.
const Preferences = preload("res://scripts/title_settings.gd")
const Flood = preload("res://scripts/room_flooding.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	var prefix := "user://crew_loss_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix + ".meta"
	game.run_save_path = prefix + ".loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.crew_comms.archive_path = prefix + ".comms.json"
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.set_process(false)
	game.running = true
	game.paused = false
	game.testing_disable_failures = false
	var actor = game.bill_npc
	actor.active = true; actor.dead = false
	game.recovered_crew = [{"architect_id":"bill","id":"architect_bill","name":"Major Bill","origin":Vector2i(20,20),"alive":true}]
	game.had_crew = true
	game.crew_count = 3 # one character plus two unseen Crew Hab survivors

	# Warning before a death: low air in unsafe water, spoken once.
	game.crew_comms.pending.clear(); game.crew_comms.current = {}
	actor.foot = (Vector2(20,20) + Vector2.ONE * 0.5) * 384.0
	game.occupied[Vector2i(20,20)].water_level = 0.95
	actor.helmet_equipped = false
	actor.breath_oxygen = 7.0
	Flood.step_crew(game, actor, "bill", 0.1)
	var warned := 0
	for entry in game.crew_comms.pending + ([game.crew_comms.current] if not game.crew_comms.current.is_empty() else []):
		if "running out of air" in str(entry.get("text","")): warned += 1
	check(warned == 1, "BRINE warns that Bill is running out of air")
	Flood.step_crew(game, actor, "bill", 0.1)
	var repeats := 0
	for entry in game.crew_comms.pending:
		if "running out of air" in str(entry.get("text","")): repeats += 1
	check(repeats <= 1, "The warning is not repeated while the danger lasts")

	# Death: reported, and the run ends although crew_count is still above zero.
	Flood.kill(game, actor, "bill", "oxygen exhausted")
	var reported := false
	for entry in game.crew_comms.pending + ([game.crew_comms.current] if not game.crew_comms.current.is_empty() else []):
		if "Major Bill is gone" in str(entry.get("text","")): reported = true
	check(reported, "BRINE reports the death")
	check(game.crew_count > 0, "Fixture keeps unseen survivors in the count")
	check(not game.running, "The run ends once every character is dead")

	game.queue_free()
	await process_frame
	for suffix in [".cfg", ".meta", ".loop", ".comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(prefix + suffix)
	print("CREW LOSS %s" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
