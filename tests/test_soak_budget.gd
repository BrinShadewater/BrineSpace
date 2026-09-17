extends SceneTree
## Performance gate (owner request, Sept 17): build a modest station, run it for a stretch of
## cycles and fail when a frame crosses the budget. Timings differ between machines, so the
## limits are generous; the point is to catch a regression like the repair-path stall that made
## single frames take over a second. Uses its own save and profile paths.
const BUDGET_MS := 90.0 # A single station frame; the station itself measures about 14 ms worst.
const MEAN_BUDGET_MS := 8.0
const CYCLES := 40
const DT := 0.05
const ROOMS := ["corridor", "storage_bay", "crew_hab", "hydroponics_bay", "life_support", "reactor", "solar_array", "research_lab", "galley", "mining_drone_bay", "salvage_workshop", "airlock"]
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	var prefix := "user://soak_budget_%d" % OS.get_process_id()
	preload("res://scripts/title_settings.gd").save_path = prefix + ".cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = prefix + ".loop"
	game.meta.save_path = prefix + ".json"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.testing_free_build = true
	var cell := Vector2i(20, 19)
	for index in range(ROOMS.size()):
		game._place_room(ROOMS[index], cell, true)
		cell += Vector2i.RIGHT if index % 2 == 0 else Vector2i.UP
	game.crew_comms.minimize()
	# Scanning a room type's walkable points happens once per type and is paid while a station
	# loads, so warm it here rather than measuring twelve first-time scans in one frame.
	var warm_started := Time.get_ticks_usec()
	game.bill_npc.rebuild(game)
	var warm_ms := float(Time.get_ticks_usec() - warm_started) / 1000.0
	check(warm_ms < 1500.0, "The first navigation build for a new station took %.0f ms" % warm_ms)
	game.running = true
	game.paused = false
	var crew = preload("res://scripts/bill_npc.gd")
	crew.route_searches = 0
	var worst := 0.0
	var worst_cycle := 0
	var total := 0.0
	var frames := 0
	for cycle in range(CYCLES):
		for step in range(int(round(1.0 / DT))):
			if game.paused: game.paused = false
			var started := Time.get_ticks_usec()
			game._process(DT)
			var used := float(Time.get_ticks_usec() - started) / 1000.0
			frames += 1
			total += used
			if used > worst:
				worst = used
				worst_cycle = cycle
		game._on_tick_timer_timeout()
		if not game.running: break
		if cycle % 10 == 0: await process_frame
	var mean := total / maxf(1.0, float(frames))
	check(worst <= BUDGET_MS, "A station frame took %.1f ms at cycle %d (budget %.0f ms)" % [worst, worst_cycle, BUDGET_MS])
	check(mean <= MEAN_BUDGET_MS, "Station frames averaged %.2f ms (budget %.0f ms)" % [mean, MEAN_BUDGET_MS])
	check(crew.route_searches < frames, "Crew searched for a route %d times in %d frames; a search every frame is the pathing stall" % [crew.route_searches, frames])
	var stuck: Array = preload("res://scripts/stuck_watch.gd").reported.keys()
	check(stuck.is_empty(), "Nothing should be stuck in a healthy station: %s" % str(stuck))
	game.queue_free()
	await process_frame
	for suffix in [".cfg", ".loop", ".json", ".json.bak", ".json.tmp", ".loop.comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix + suffix))
	print("SOAK BUDGET %s: %d cycles, %d frames, mean %.2f ms, worst %.1f ms at cycle %d, %d route searches" % ["PASS" if failures == 0 else "FAIL %d" % failures, CYCLES, frames, mean, worst, worst_cycle, crew.route_searches])
	quit(1 if failures else 0)
