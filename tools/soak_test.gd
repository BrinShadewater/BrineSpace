extends SceneTree
## Headless soak run (owner request, Sept 17): run a station for many cycles with no window and
## report where the time went, so a slowdown shows up before it reaches a playtest. Uses its own
## save and profile paths; it never touches the player's files.
##   godot --headless --path . -s res://tools/soak_test.gd -- [--cycles=120] [--save=<path>]
##       [--dt=0.05] [--out=res://output/soak.json] [--fail-ms=250]
const SYSTEMS := ["crew", "drones_wrecks", "cryo", "airlocks", "interface", "station_total"]

func _init() -> void: call_deferred("run")

func run() -> void:
	var cycles := 120
	var dt := 0.05
	var save_path := ""
	var out_path := ""
	var fail_ms := 0.0
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--cycles="): cycles = int(argument.trim_prefix("--cycles="))
		if argument.begins_with("--dt="): dt = float(argument.trim_prefix("--dt="))
		if argument.begins_with("--save="): save_path = argument.trim_prefix("--save=")
		if argument.begins_with("--out="): out_path = argument.trim_prefix("--out=")
		if argument.begins_with("--fail-ms="): fail_ms = float(argument.trim_prefix("--fail-ms="))
	var pid := OS.get_process_id()
	var prefix := "user://soak_%d" % pid
	preload("res://scripts/title_settings.gd").save_path = prefix + ".cfg"
	var game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = prefix + ".loop"
	game.meta.save_path = prefix + ".json"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	if not save_path.is_empty():
		var data = game.RunSave.read(save_path)
		if data.is_empty() or not game.RunSave.restore(game, data):
			print("SOAK: could not restore ", save_path)
			quit(1)
			return
		game.tick_timer.stop()
	game.running = true
	game.paused = false
	var errors = preload("res://scripts/error_watch.gd").new()
	var totals := {}
	for key in SYSTEMS: totals[key] = 0.0
	var frames := 0
	var worst := 0.0
	var worst_at := 0
	var slow_frames := 0
	var simulated_ms := 0.0
	var pauses := 0
	var ended_at := -1
	var started := Time.get_ticks_usec()
	var crew = preload("res://scripts/bill_npc.gd")
	crew.route_searches = 0
	crew.route_failures = 0
	for cycle in range(cycles):
		for step in range(int(round(1.0 / dt))):
			# Dialogue and warnings pause a real game; a soak keeps simulating and counts them.
			if game.paused:
				game.paused = false
				pauses += 1
			var frame_started := Time.get_ticks_usec()
			game._process(dt)
			var used := float(Time.get_ticks_usec() - frame_started) / 1000.0
			frames += 1
			if used > worst:
				worst = used
				worst_at = cycle
				if used >= 33.3: slow_frames += 1
			simulated_ms += used
			for key in SYSTEMS: totals[key] = float(totals[key]) + float(game.frame_timing_usec.get(key, 0)) / 1000.0
		game._on_tick_timer_timeout()
		if not game.running:
			# The station failed (or won); timings past this point would be idle frames.
			ended_at = cycle
			break
		if cycle % 10 == 0: await process_frame
	var wall := simulated_ms
	errors.poll(0.0)
	var report := {"cycles": cycles, "frames": frames, "dt": dt, "save": save_path,
		"simulated_ms": wall, "mean_frame_ms": wall / maxf(1.0, float(frames)), "max_frame_ms": worst, "run_ended_at_cycle": ended_at,
		"max_frame_cycle": worst_at, "frames_over_33ms": slow_frames,
		"pauses_cleared": pauses, "route_searches": crew.route_searches, "route_failures": crew.route_failures,
		"errors": errors.summary(), "rooms": game.placed_rooms.size(), "crew": game.crew_count,
		"systems_ms": totals}
	print("SOAK: %d cycles / %d frames / %.0f ms simulating / mean %.2f ms / max %.2f ms at cycle %d / %d frames over 33 ms%s" % [cycles, frames, wall, report.mean_frame_ms, worst, worst_at, slow_frames, "" if ended_at < 0 else " / the run ended at cycle %d" % ended_at])
	for key in SYSTEMS:
		print("  %-14s %8.1f ms total  %6.3f ms per frame" % [key, totals[key], float(totals[key]) / maxf(1.0, float(frames))])
	print("  pauses cleared %d" % pauses)
	print("  route searches %d (%d failed) / errors logged %d in %d kinds" % [crew.route_searches, crew.route_failures, errors.total, errors.groups.size()])
	for line in errors.report_lines(): print("  " + line)
	if not out_path.is_empty():
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out_path.get_base_dir()))
		var file := FileAccess.open(out_path, FileAccess.WRITE)
		if file != null:
			file.store_string(JSON.stringify(report, "\t"))
			file.close()
	for suffix in [".cfg", ".loop", ".json", ".json.bak", ".json.tmp", ".loop.comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix + suffix))
	var failed: bool = fail_ms > 0.0 and worst > fail_ms
	if failed: print("SOAK FAIL: a frame took %.1f ms (limit %.1f ms)" % [worst, fail_ms])
	quit(1 if failed else 0)
