extends "package_transitions.gd"
## External actual-package real-play observation autoload. Not shipped.
## Copy the reviewed package_transitions.gd and FROZEN release_smoke_base.gd
## beside this file. Use a physical EXE/PCK QA copy, empty initial scene, guarded
## BugReport autoload, and PackageSoak autoload. No runtime source replacements.
## --user-dir=<resolved scratch profile> --save=<immutable copied checkpoint>
## --out=<absolute JSON> --seconds=600 --speed=4 --qa-screen=2
## Scratch APPDATA; BRINE_SILENT=1; visible windowed secondary screen; Dummy audio.
## Parent owns package/adapter identities, owner fingerprints, process/log guards,
## external timeout and JSON acceptance. Normal renderer, _process and timers.
## Uses real Continue, speed, Resume, comms Minimize, Return and Quit handlers.
## No actor edits, manual simulation, free-building or disabled failure flags.
## Scope: a bounded real-play smoke/soak. Not two-hour, GPU, physical-input,
## behavior-equivalence, normal-entry, or whole-game acceptance. Early loop end
## is a recorded legitimate outcome, never a completed-duration soak pass.
const Architects = preload("res://scripts/architects.gd")
const Stuck = preload("res://scripts/stuck_watch.gd")
const FRAME_CAP := 1500000
const PERIODIC_CAP := 2048
const COMMS_ACTION_CAP := 4096
const PERIODIC_USEC := 5000000
var requested_seconds := 600
var requested_speed := 4
var observed_game
var reporter
var monitor
var measuring := false
var measurement_started_usec := 0
var measurement_ended_usec := 0
var previous_frame_usec := 0
var deadline_usec := 0
var next_periodic_usec := 0
var stop_reason := "not_started"
var frame_usec: Array[int] = []
var frame_flags: Array[int] = []
var periodic: Array = []
var comms_actions: Array = []
var actor_observations: Dictionary = {}
var over_50 := 0
var over_100 := 0
var over_400 := 0

func configure() -> bool:
	if not super.configure(): return false
	requested_seconds = int(options.get("seconds", "600"))
	requested_speed = int(options.get("speed", "4"))
	check(requested_seconds >= 1 and requested_seconds <= 7200, "Wall-duration request is bounded to1..7200seconds")
	check(requested_speed in [1, 2, 4], "Normal1x/2x/4x speed selected")
	evidence["schema"] = "brinespace.package-soak.v1"
	evidence.erase("transitions")
	evidence.erase("requested_transitions")
	evidence["scope"] = "Actual-package normal-process/timer real play, with scripted UI Continue/speed/Resume/comms-Minimize/Return/Quit. Not two-hour, GPU, physical-input, behavior-equivalence or normal-entry acceptance."
	evidence["requested_seconds"] = requested_seconds
	evidence["requested_speed"] = requested_speed
	evidence["frame_scope"] = "Every interval between this observer's process callbacks; includes render/wait, pauses, diagnostics and observer work. Flags are sampled at interval end, not a complete attribution of the interval. No rows excluded."
	evidence["periodic_scope"] = "Approximately5second observations plus initial/final state. Sampled actor displacement is a lower bound and can miss motion returning to the same point; no displacement alone does not prove a stuck actor."
	evidence["retention"] = {"frame_cap": FRAME_CAP, "periodic_cap": PERIODIC_CAP, "comms_action_cap": COMMS_ACTION_CAP, "overflow": false,
		"monitor": "Packaged monitor retains latest120 approximately1second buckets and32 hitches; final snapshot is not a whole-soak percentile source."}
	return failures == 0

func _process(delta: float) -> void:
	super._process(delta)
	if not measuring: return
	var now := Time.get_ticks_usec()
	# Anchor at an observer callback, so the first retained interval is also
	# callback-to-callback rather than a partial setup/continuation interval.
	if measurement_started_usec == 0:
		measurement_started_usec = now
		previous_frame_usec = now
		deadline_usec = now + requested_seconds * 1000000
		next_periodic_usec = now + PERIODIC_USEC
		evidence["measurement_start_utc"] = Time.get_datetime_string_from_system(true, true)
		if not healthy(): stop_measurement("guard_failed", now)
		return
	if frame_usec.size() >= FRAME_CAP:
		evidence.retention.overflow = true
		check(false, "Per-frame retention cap reached; no silent truncation")
		stop_measurement("frame_cap", previous_frame_usec)
		return
	var elapsed: int = now - previous_frame_usec
	check_frame_elapsed(elapsed)
	frame_usec.append(elapsed)
	var flags := 0
	var scene_valid: bool = is_instance_valid(observed_game) and get_tree().current_scene == observed_game
	if get_tree().paused or (scene_valid and observed_game.paused): flags |= 1
	if not get_window().has_focus(): flags |= 2
	if scene_valid and not observed_game.running: flags |= 4
	if reporter.get("_report_thread") != null or not reporter.get("_report_jobs").is_empty(): flags |= 8
	if scene_valid and is_instance_valid(observed_game.crew_comms) and observed_game.crew_comms.holds_pause: flags |= 16
	if not healthy(): flags |= 32
	if not scene_valid: flags |= 64
	frame_flags.append(flags)
	previous_frame_usec = now
	if elapsed >= 50000: over_50 += 1
	if elapsed >= 100000: over_100 += 1
	if elapsed >= 400000: over_400 += 1
	if not healthy():
		stop_measurement("guard_failed", now)
	elif not scene_valid:
		check(false, "Measured station remained the current live scene")
		stop_measurement("unexpected_scene_change", now)
	elif not observed_game.running:
		stop_measurement("loop_ended", now)
	elif not release_errors.messages.is_empty():
		stop_measurement("engine_or_script_error", now)
	elif now - last_render_usec > 10000000:
		check(false, "Native rendering stopped for more than10seconds")
		stop_measurement("render_timeout", now)
	elif now >= deadline_usec:
		stop_measurement("duration_completed", now)

func check_frame_elapsed(elapsed: int) -> void:
	if elapsed <= 0:
		check(false, "Monotonic measured frame interval must be positive")

func stop_measurement(reason: String, at_usec: int) -> void:
	measuring = false
	stop_reason = reason
	measurement_ended_usec = at_usec

func actor_rows() -> Dictionary:
	var result: Dictionary = {}
	var ids: Array = Architects.IDS.duplicate()
	ids.append_array(observed_game.companion_actors.keys())
	for value in ids:
		var id := str(value)
		var actor = Architects.actor_for(observed_game, id) if id in Architects.IDS else observed_game.companion_actors.get(id)
		if actor == null: continue
		var foot: Vector2 = actor.foot
		var goal := str(actor.goal)
		var state := str(actor.state)
		var history: Dictionary = actor_observations.get(id, {"last_foot": foot, "last_goal": goal, "last_state": state,
			"sampled_displacement": 0.0, "moved_observations": 0, "goal_changes": 0, "state_changes": 0, "observations": 0})
		var distance: float = Vector2(history.last_foot).distance_to(foot)
		history.sampled_displacement += distance
		if distance > 0.01: history.moved_observations += 1
		if goal != history.last_goal: history.goal_changes += 1
		if state != history.last_state: history.state_changes += 1
		history.observations += 1
		history.last_foot = foot; history.last_goal = goal; history.last_state = state
		actor_observations[id] = history
		var cell: Vector2i = actor.goal_cell
		result[id] = {"active": actor.active, "dead": actor.dead, "foot": [foot.x, foot.y],
			"goal": goal, "goal_cell": [cell.x, cell.y], "state": state, "activity": str(actor.activity),
			"path_points": actor.path.size(), "stage": actor.stage, "needs": actor.needs.duplicate(true),
			"sampled_displacement": history.sampled_displacement, "moved_observations": history.moved_observations,
			"goal_changes": history.goal_changes, "state_changes": history.state_changes, "observations": history.observations}
	return result

func observation(label: String) -> Dictionary:
	var now := Time.get_ticks_usec()
	var comms_held: bool = is_instance_valid(observed_game.crew_comms) and observed_game.crew_comms.holds_pause
	return {"label": label, "ticks_usec": now, "since_measurement_ms": float(now - measurement_started_usec) / 1000.0 if measurement_started_usec > 0 else null,
		"run_id": observed_game.run_save_id, "cycle": observed_game.cycle, "running": observed_game.running,
		"paused": observed_game.paused, "tree_paused": get_tree().paused, "comms_holds_pause": comms_held,
		"visual_time_seconds": observed_game.visual_time_seconds, "speed_index": observed_game.time_speed_index,
		"timer_stopped": observed_game.tick_timer.is_stopped(), "timer_paused": observed_game.tick_timer.paused,
		"production_process_enabled": observed_game.is_processing(), "rooms": observed_game.placed_rooms.size(),
		"testing_free_build": observed_game.testing_free_build, "testing_disable_failures": observed_game.testing_disable_failures,
		"visible_rooms": observed_game.grid_view.visible_draw_rooms.size(), "crew_count": observed_game.crew_count,
		"resources": observed_game.resources.duplicate(true), "actors": actor_rows(),
		"memory": monitor.memory_stats(), "errors": monitor.errors.summary(),
		"stuck_reported": Stuck.reported.duplicate(true),
		"latest_monitor_bucket": monitor.latest.duplicate(true),
		"reports": {"attempts": monitor.auto_reports, "notes": monitor.auto_notes.duplicate(true),
			"worker_active": reporter.get("_report_thread") != null, "queued": reporter.get("_report_jobs").size(),
			"last_path": reporter.last_report_path, "last_timings": reporter.last_report_timings.duplicate(true)}}

func append_periodic(label: String) -> void:
	if periodic.size() >= PERIODIC_CAP:
		evidence.retention.overflow = true
		check(false, "Periodic retention cap reached; no silent truncation")
		if measuring: stop_measurement("periodic_cap", previous_frame_usec)
		return
	periodic.append(observation(label))
	if periodic.size()%6==0:
		print("PACKAGE_SOAK_PROGRESS elapsed_seconds=",float(Time.get_ticks_usec()-measurement_started_usec)/1000000.0," cycle=",observed_game.cycle," frames=",frame_usec.size()," over100=",over_100)

func handle_comms(label: String) -> void:
	if not is_instance_valid(observed_game.crew_comms) or not observed_game.crew_comms.holds_pause: return
	if comms_actions.size() >= COMMS_ACTION_CAP:
		evidence.retention.overflow = true
		check(false, "Comms-action retention cap reached; no silent truncation")
		if measuring: stop_measurement("comms_action_cap", previous_frame_usec)
		return
	var row := {"ticks_usec": Time.get_ticks_usec(), "context": label, "paused_before": observed_game.paused,
		"holds_pause_before": observed_game.crew_comms.holds_pause}
	observed_game.crew_comms.minimize()
	row["paused_after"] = observed_game.paused
	row["holds_pause_after"] = observed_game.crew_comms.holds_pause
	comms_actions.append(row)

func retain_frames() -> void:
	var total_usec := 0
	for duration in frame_usec: total_usec += duration
	var ordered: Array[int] = frame_usec.duplicate()
	ordered.sort()
	var paused_samples := 0
	var unfocused_samples := 0
	var writer_samples := 0
	for flags in frame_flags:
		if flags & 1: paused_samples += 1
		if flags & 2: unfocused_samples += 1
		if flags & 8: writer_samples += 1
	var count := frame_usec.size()
	evidence["measurement"] = {"stop_reason": stop_reason, "duration_completed": stop_reason == "duration_completed",
		"start_ticks_usec": measurement_started_usec, "end_ticks_usec": measurement_ended_usec,
		"wall_seconds": float(measurement_ended_usec - measurement_started_usec) / 1000000.0 if measurement_started_usec > 0 else 0.0,
		"frames": count, "sum_frame_usec": total_usec,
		"mean_ms": float(total_usec) / float(count) / 1000.0 if count > 0 else null,
		"fps_including_pauses": float(count) * 1000000.0 / float(total_usec) if total_usec > 0 else null,
		"p95_ms": float(ordered[ceili(count * 0.95) - 1]) / 1000.0 if count > 0 else null,
		"p99_ms": float(ordered[ceili(count * 0.99) - 1]) / 1000.0 if count > 0 else null,
		"max_ms": float(ordered.back()) / 1000.0 if count > 0 else null,
		"frames_at_least50ms": over_50, "frames_at_least100ms": over_100, "frames_at_least400ms": over_400,
		"paused_flag_samples": paused_samples, "unfocused_flag_samples": unfocused_samples, "writer_active_flag_samples": writer_samples,
		"frame_usec": frame_usec, "frame_flags": frame_flags,
		"flags": {"1": "paused_at_interval_end", "2": "unfocused_at_interval_end", "4": "loop_not_running_at_interval_end",
			"8": "report_writer_or_queue_active_at_interval_end", "16": "comms_holds_pause_at_interval_end",
			"32": "visibility_or_input_guard_failed", "64": "measured_scene_no_longer_current_or_valid"}}
	evidence["periodic"] = periodic
	evidence["comms_minimize_actions"] = comms_actions
	check(count == frame_flags.size(), "Every retained frame has a state flag row")
	check(measurement_started_usec == 0 or total_usec == measurement_ended_usec - measurement_started_usec, "All measured wall time is represented by retained intervals")

func finish(normal_quit: bool) -> void:
	if finished: return
	finished = true
	if is_instance_valid(monitor):
		monitor.errors.poll(Time.get_ticks_msec())
		check(monitor.errors.total == 0, "Packaged error watcher recorded no engine/script errors")
	check(SafeImage.failures.is_empty(), "No safe-image placeholders in exercised soak")
	evidence["safe_image_failures"] = SafeImage.failures.duplicate(true)
	evidence["engine_script_errors"] = release_errors.messages.duplicate()
	check(release_errors.messages.is_empty(), "No captured engine/script errors")
	evidence["guard_failure"] = guard_failure
	evidence["failures"] = failures
	evidence["full_duration_soak_pass"] = stop_reason == "duration_completed" and failures == 0
	evidence["shutdown"] = {"normal_title_quit_planned": normal_quit and failures == 0, "report_writer_idle_verified": normal_quit,
		"scope": "Return/save, reporter completion and final JSON I/O follow measured soak; their time is not included in frame_usec. Exit warnings reviewed externally."}
	var written := false
	if not out_path.is_empty():
		var file := FileAccess.open(out_path, FileAccess.WRITE)
		if file != null:
			file.store_string(JSON.stringify(evidence)); file.flush()
			written = file.get_error() == OK
			file.close()
	if not written: failures += 1
	print("ACTUAL_PACKAGE_SOAK_COMPLETE outcome=", stop_reason, " failures=", failures, " debug=", OS.is_debug_build(), " evidence_flushed=", written)
	call_deferred("_quit_after_evidence", normal_quit and failures == 0)

func _quit_after_evidence(normal_quit: bool) -> void:
	var title = get_tree().current_scene
	OS.remove_logger(release_errors)
	if normal_quit and title != null and title.has_method("_continue_loop") and is_instance_valid(title.quit_button) and not title.quit_button.disabled:
		print("ACTUAL_PACKAGE_SOAK_NORMAL_QUIT title_button=true audio_drain_handler=true")
		title.quit_button.pressed.emit()
	else:
		print("ACTUAL_PACKAGE_SOAK_FALLBACK_QUIT failures=", failures)
		get_tree().quit(1)

func run():
	if not configure(): finish(false); return
	var copy_error: Error = DirAccess.copy_absolute(source_path, ProjectSettings.globalize_path(LOOP))
	check(copy_error == OK, "Copied immutable input to writable scratch loop")
	if copy_error != OK: finish(false); return
	var scene_error: Error = get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	check(scene_error == OK, "Packaged title scene requested after isolation guard")
	if scene_error != OK: finish(false); return
	var title = await wait_title()
	if title == null: finish(false); return
	check(title.continue_button.visible and not title.continue_button.disabled, "Packaged Continue is offered")
	if not title.continue_button.visible or title.continue_button.disabled: finish(false); return
	title.continue_button.pressed.emit()
	observed_game = await wait_station(title)
	title = null
	if observed_game == null: finish(false); return
	observed_game.run_save_path = LOOP
	observed_game.meta.save_path = META
	if is_instance_valid(observed_game.crew_comms): observed_game.crew_comms.archive_path = LOOP + ".comms.json"
	check(observed_game.placed_rooms.size() == expected_rooms and observed_game.run_save_id == expected_run_id, "Continue restored expected station/run identity")
	check(not observed_game.testing_free_build and not observed_game.testing_disable_failures, "Normal costs/failure flags remain enabled")
	check(observed_game.is_processing(), "Production _process remains enabled")
	reporter = get_tree().root.get_node_or_null("BugReport")
	monitor = reporter.performance_monitor if reporter != null else null
	check(is_instance_valid(monitor), "Packaged performance/error monitor remains active")
	if failures > 0: finish(false); return
	handle_comms("entry")
	if observed_game.running:
		var speed_index: int = observed_game.time_speeds.find(float(requested_speed))
		evidence["speed_selection_probe"]={"speeds":observed_game.time_speeds,"requested":requested_speed,"requested_type":typeof(requested_speed),"element_type":typeof(observed_game.time_speeds[0]),"index":speed_index,"button_count":observed_game.speed_buttons.size()}
		print("PACKAGE_SOAK_SPEED_PROBE ",JSON.stringify(evidence.speed_selection_probe))
		check(speed_index >= 0 and speed_index < observed_game.speed_buttons.size(), "Requested speed has a real UI handler")
		if speed_index < 0 or speed_index >= observed_game.speed_buttons.size(): finish(false); return
		observed_game.speed_buttons[speed_index].pressed.emit()
		if observed_game.paused: observed_game.pause_button.pressed.emit()
		check(observed_game.time_speed_index == speed_index, "Normal speed handler selected requested speed")
		check(not observed_game.paused and not observed_game.tick_timer.is_stopped(), "Normal Resume/timer starts real play")
	if failures > 0: finish(false); return
	if not await fresh_render(): finish(false); return
	evidence["initial"] = observation("initial_before_measurement")
	if not observed_game.running:
		stop_reason = "loop_not_running_on_entry"
	else:
		measuring = true
		while measuring:
			await get_tree().process_frame
			if not measuring: break
			handle_comms("measured_play")
			if measurement_started_usec > 0 and Time.get_ticks_usec() >= next_periodic_usec:
				append_periodic("periodic")
				next_periodic_usec = Time.get_ticks_usec() + PERIODIC_USEC
	if not is_instance_valid(observed_game) or get_tree().current_scene != observed_game:
		evidence["final"] = {"available": false, "reason": "Measured station no longer current/valid"}
		retain_frames()
		finish(false)
		return
	monitor.errors.poll(Time.get_ticks_msec())
	evidence["final"] = observation("final_after_measurement")
	evidence["monitor_final"] = monitor.snapshot()
	evidence["crew_progress_scope"] = "Initial/final and periodic sampled state/displacement plus native stuck watcher; no route, target, foot, actor or failure flags changed by observer."
	evidence["cycle_delta"] = int(evidence.final.cycle) - int(evidence.initial.cycle)
	evidence["visual_time_delta"] = float(evidence.final.visual_time_seconds) - float(evidence.initial.visual_time_seconds)
	check(evidence.initial.run_id == evidence.final.run_id, "Observed loop identity remained stable")
	check(not observed_game.testing_free_build and not observed_game.testing_disable_failures, "Normal costs/failure flags remained enabled at soak end")
	if stop_reason == "duration_completed":
		check(evidence.visual_time_delta > 0.0, "Normal simulation advanced during completed-duration soak")
	retain_frames()
	evidence["source_after_sha256"] = FileAccess.get_sha256(source_path)
	check(evidence.source_after_sha256 == evidence.source_sha256, "Immutable source checkpoint preserved")
	if not healthy(): finish(false); return
	handle_comms("after_measurement")
	observed_game._menu_return_title()
	observed_game = null
	title = await wait_title()
	if title == null: finish(false); return
	var idle: bool = await writers_idle()
	check(idle, "Report writers completed before evidence flush/normal Quit")
	if is_instance_valid(monitor):
		evidence["reports_after_shutdown_wait"] = {"attempts": monitor.auto_reports, "notes": monitor.auto_notes.duplicate(true),
			"last_path": reporter.last_report_path, "last_timings": reporter.last_report_timings.duplicate(true), "errors": monitor.errors.summary()}
	finish(idle)
