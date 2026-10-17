extends "package_soak.gd"
## External observer only; inherits the frozen-package isolation/window guards.
var observer_mode := "minimal"
var episodes := 2
var aggregate_count := 0
var aggregate_sum := 0
var aggregate_max := 0
var aggregate_flags: Dictionary = {}

func configure() -> bool:
	if not super.configure(): return false
	observer_mode = str(options.get("observer", "minimal"))
	episodes = int(options.get("episodes", "2"))
	check(observer_mode in ["minimal", "full"], "Explicit minimal/full observer selected")
	check(episodes >= 1 and episodes <= 3, "Episode count bounded to1..3")
	evidence["schema"] = "brinespace.object-growth.v1"
	evidence["observer"] = observer_mode
	evidence["episodes"] = []
	evidence["scope"] = "Actual unchanged release, normal-process4x play and title return; object lifetime diagnosis, not FPS or behavior-equivalence acceptance."
	evidence["metric_scope"] = "Objects are live ObjectDB count. Resources counts path-cached resources only. Release orphan/static-memory zeros are unavailable. Node census includes scene tree only; processed Tweens is partial RefCounted census."
	return failures == 0

func census(label: String, game = null) -> Dictionary:
	var row := counters(label, game)
	row.erase("orphan_nodes")
	row.erase("static_bytes")
	row["processed_tweens"] = get_tree().get_processed_tweens().size()
	var classes: Dictionary = {}
	var pending: Array[Node] = [get_tree().root]
	while not pending.is_empty():
		var node: Node = pending.pop_back()
		var kind := node.get_class()
		classes[kind] = int(classes.get(kind, 0)) + 1
		pending.append_array(node.get_children())
	row["tree_node_classes"] = classes
	return row

func observation(label: String) -> Dictionary:
	if observer_mode == "full":
		var row := super.observation(label)
		row["census"] = census(label, observed_game)
		return row
	return {"label": label, "ticks_usec": Time.get_ticks_usec(), "cycle": observed_game.cycle,
		"run_id": observed_game.run_save_id, "visual_time_seconds": observed_game.visual_time_seconds,
		"census": census(label, observed_game)}

func _process(delta: float) -> void:
	if observer_mode == "full":
		super._process(delta)
		return
	# Keep inherited visibility/input/audio guards; skip only recorder retention.
	var was_measuring := measuring
	measuring = false
	super._process(delta)
	measuring = was_measuring
	if not measuring: return
	var now := Time.get_ticks_usec()
	if measurement_started_usec == 0:
		measurement_started_usec = now
		previous_frame_usec = now
		deadline_usec = now + requested_seconds * 1000000
		next_periodic_usec = now + PERIODIC_USEC
		return
	var elapsed := now - previous_frame_usec
	check_frame_elapsed(elapsed)
	aggregate_count += 1
	aggregate_sum += elapsed
	aggregate_max = maxi(aggregate_max, elapsed)
	previous_frame_usec = now
	var flags := 0
	var valid: bool = is_instance_valid(observed_game) and get_tree().current_scene == observed_game
	if get_tree().paused or (valid and observed_game.paused): flags |= 1
	if not get_window().has_focus(): flags |= 2
	if valid and not observed_game.running: flags |= 4
	if reporter.get("_report_thread") != null or not reporter.get("_report_jobs").is_empty(): flags |= 8
	if valid and is_instance_valid(observed_game.crew_comms) and observed_game.crew_comms.holds_pause: flags |= 16
	if not healthy(): flags |= 32
	if not valid: flags |= 64
	aggregate_flags[str(flags)] = int(aggregate_flags.get(str(flags), 0)) + 1
	if not healthy(): stop_measurement("guard_failed", now)
	elif not valid: stop_measurement("unexpected_scene_change", now)
	elif not observed_game.running: stop_measurement("loop_ended", now)
	elif not release_errors.messages.is_empty(): stop_measurement("engine_or_script_error", now)
	elif now - last_render_usec > 10000000: stop_measurement("render_timeout", now)
	elif now >= deadline_usec: stop_measurement("duration_completed", now)

func retain_frames() -> void:
	if observer_mode == "full":
		super.retain_frames()
		return
	evidence["measurement"] = {"stop_reason": stop_reason, "duration_completed": stop_reason == "duration_completed",
		"wall_seconds": float(measurement_ended_usec - measurement_started_usec) / 1000000.0,
		"frames": aggregate_count, "sum_frame_usec": aggregate_sum, "max_ms": aggregate_max / 1000.0,
		"aggregate_flag_counts": aggregate_flags, "frame_arrays_retained": false}
	evidence["periodic"] = periodic
	evidence["comms_minimize_actions"] = comms_actions
	check(aggregate_sum == measurement_ended_usec - measurement_started_usec, "All minimal-observer measured intervals accounted")

func title_quiescence(title, label: String) -> Dictionary:
	if not await settle(title, false): return {}
	if not await writers_idle(): return {}
	var row := {"start": census(label + "_settled")}
	var deadline := Time.get_ticks_usec() + 10000000
	while healthy() and Time.get_ticks_usec() < deadline:
		if not is_instance_valid(title) or get_tree().current_scene != title or loading_present() or title.starting:
			check(false, "Title remains quiescent")
			return row
		if not await fresh_render(): return row
	row["end"] = census(label + "_after10s")
	return row

func reset_episode() -> void:
	frame_usec = []; frame_flags = []; periodic = []; comms_actions = []; actor_observations = {}
	aggregate_count = 0; aggregate_sum = 0; aggregate_max = 0; aggregate_flags = {}
	measurement_started_usec = 0; measurement_ended_usec = 0; previous_frame_usec = 0
	deadline_usec = 0; next_periodic_usec = 0; stop_reason = "not_started"
	over_50 = 0; over_100 = 0; over_400 = 0

func run():
	if not configure(): finish(false); return
	check(DirAccess.copy_absolute(source_path, ProjectSettings.globalize_path(LOOP)) == OK, "Copied scratch checkpoint")
	check(get_tree().change_scene_to_file("res://scenes/title_screen.tscn") == OK, "Requested packaged title")
	if failures > 0: finish(false); return
	var title = await wait_title()
	if title == null: finish(false); return
	evidence["title_baseline"] = await title_quiescence(title, "baseline_title")
	for iteration in range(episodes):
		reset_episode()
		check(DirAccess.copy_absolute(source_path, ProjectSettings.globalize_path(LOOP)) == OK, "Reset identical input checkpoint")
		title.run_save_path = LOOP
		check(title.continue_button.visible and not title.continue_button.disabled, "Continue offered")
		if failures > 0: finish(false); return
		title.continue_button.pressed.emit()
		observed_game = await wait_station(title)
		title = null
		if observed_game == null: finish(false); return
		var old_game_id: int = observed_game.get_instance_id()
		observed_game.run_save_path = LOOP
		observed_game.meta.save_path = META
		if is_instance_valid(observed_game.crew_comms): observed_game.crew_comms.archive_path = LOOP + ".comms.json"
		reporter = get_tree().root.get_node_or_null("BugReport")
		monitor = reporter.performance_monitor if reporter != null else null
		check(is_instance_valid(monitor), "Packaged performance monitor active")
		check(observed_game.placed_rooms.size() == expected_rooms and observed_game.run_save_id == expected_run_id, "Expected station/run restored")
		check(not observed_game.testing_free_build and not observed_game.testing_disable_failures and observed_game.is_processing(), "Normal costs/failures/process enabled")
		handle_comms("entry")
		var speed_index: int = observed_game.time_speeds.find(float(requested_speed))
		check(speed_index >= 0 and speed_index < observed_game.speed_buttons.size(), "Real speed handler available")
		if failures > 0: finish(false); return
		observed_game.speed_buttons[speed_index].pressed.emit()
		if observed_game.paused: observed_game.pause_button.pressed.emit()
		check(observed_game.running and not observed_game.paused and not observed_game.tick_timer.is_stopped(), "Real Resume starts normal play")
		if not await fresh_render(): finish(false); return
		var episode := {"index": iteration, "initial": observation("initial"), "actors_initial": actor_rows()}
		measuring = true
		while measuring:
			await get_tree().process_frame
			if not measuring: break
			handle_comms("measured_play")
			if measurement_started_usec > 0 and Time.get_ticks_usec() >= next_periodic_usec:
				append_periodic("periodic")
				next_periodic_usec = Time.get_ticks_usec() + PERIODIC_USEC
		if not is_instance_valid(observed_game) or not healthy(): finish(false); return
		episode["final"] = observation("final")
		episode["actors_final"] = actor_rows()
		check(stop_reason == "duration_completed", "Full episode duration completed")
		check(episode.final.cycle > episode.initial.cycle, "Normal simulation advanced")
		retain_frames()
		for key in ["measurement", "periodic", "comms_minimize_actions"]:
			episode[key] = evidence[key]
			evidence.erase(key)
		observed_game._menu_return_title()
		observed_game = null
		title = await wait_title()
		if title == null: finish(false); return
		episode["title_return"] = await title_quiescence(title, "return_" + str(iteration))
		episode["game_instance_freed"] = not is_instance_id_valid(old_game_id)
		check(episode.game_instance_freed, "Returned gameplay Node instance is freed")
		evidence.episodes.append(episode)
		print("OBJECT_GROWTH_EPISODE ", observer_mode, " index=", iteration, " objects=", episode.initial.census.objects, "->", episode.final.census.objects, " title=", episode.title_return.end.objects)
		if failures > 0: finish(false); return
	evidence["source_after_sha256"] = FileAccess.get_sha256(source_path)
	check(evidence.source_after_sha256 == evidence.source_sha256, "Input checkpoint unchanged")
	finish(await writers_idle())
