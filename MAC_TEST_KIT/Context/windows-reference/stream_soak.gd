extends "router_growth.gd"
## QA-only fixed-memory recorder. Production process/timers/actors remain live.
const HIST_LIMIT := 50000
const HITCH_CAP := 512
var histogram := PackedInt32Array()
var hitches: Array = []
var raw_validation := PackedInt32Array()
var validate_raw := false
var stream: FileAccess
var stream_path := ""
var stream_rows := 0
var write_max_usec := 0
var started_progress_usec := 0

func configure() -> bool:
	if not super.configure(): return false
	check(observer_mode == "minimal" and episodes == 1, "Streaming recorder requires one minimal-observer episode")
	validate_raw = str(options.get("validate-raw", "false")) == "true"
	check(not validate_raw or requested_seconds <= 60, "Raw recorder validation limited to60seconds")
	histogram.resize(HIST_LIMIT)
	stream_path = out_path + ".periodic.jsonl"
	stream = FileAccess.open(stream_path, FileAccess.WRITE)
	check(stream != null, "Opened external periodic observation stream")
	evidence["schema"] = "brinespace.stream-soak.v1"
	evidence["scope"] = "Actual unchanged release, normal-process/timer12-room4x soak; all callback intervals included. Handler-driven Continue/Resume/comms-Minimize/Return/Quit. Not40-room, physical-input/audio, GPU or behavior-equivalence acceptance."
	evidence["retention"] = {"histogram_buckets": HIST_LIMIT, "histogram_unit": "microseconds", "hitch_rows_cap": HITCH_CAP,
		"periodic": "JSONL stream; no periodic history retained", "raw_canary_only": validate_raw, "overflow": false,
		"monitor": "Packaged bounded monitor/error watcher stays active; observer records its own write timings."}
	return failures == 0

func _process(delta: float) -> void:
	var prior_count := aggregate_count
	var prior_ticks := previous_frame_usec
	super._process(delta)
	if aggregate_count == prior_count: return
	var elapsed := previous_frame_usec - prior_ticks
	if elapsed <= 0: return
	if validate_raw: raw_validation.append(elapsed)
	if elapsed < HIST_LIMIT:
		histogram[elapsed] += 1
	else:
		if hitches.size() >= HITCH_CAP:
			evidence.retention.overflow = true
			check(false, "Hitch retention cap exceeded; no silent truncation")
			stop_measurement("hitch_cap", previous_frame_usec)
			return
		var valid: bool = is_instance_valid(observed_game)
		hitches.append({"usec": elapsed, "ticks_usec": previous_frame_usec, "frame": aggregate_count,
			"cycle": observed_game.cycle if valid else -1, "render_gap_usec": previous_frame_usec - last_render_usec,
			"writer_active": reporter.get("_report_thread") != null or not reporter.get("_report_jobs").is_empty()})

func observation(label: String) -> Dictionary:
	var row := super.observation(label)
	row["memory"] = monitor.memory_stats()
	row["actors"] = actor_rows()
	row["normal_state"] = {"running": observed_game.running, "paused": observed_game.paused,
		"tree_paused": get_tree().paused, "speed_index": observed_game.time_speed_index,
		"timer_stopped": observed_game.tick_timer.is_stopped(), "timer_paused": observed_game.tick_timer.paused,
		"process_enabled": observed_game.is_processing(), "testing_free_build": observed_game.testing_free_build,
		"testing_disable_failures": observed_game.testing_disable_failures}
	row["reports"] = {"attempts": monitor.auto_reports, "worker_active": reporter.get("_report_thread") != null,
		"queued": reporter.get("_report_jobs").size(), "last_path": reporter.last_report_path}
	row["errors"] = monitor.errors.summary()
	row["stuck_reported"] = Stuck.reported.duplicate(true)
	return row

func append_periodic(label: String) -> void:
	var row := observation(label)
	var stamp := Time.get_ticks_usec()
	stream.store_line(JSON.stringify(row))
	stream.flush()
	write_max_usec = maxi(write_max_usec, Time.get_ticks_usec() - stamp)
	check_stream_error()
	stream_rows += 1
	if stream_rows % 6 == 0:
		print("STREAM_SOAK_PROGRESS seconds=", snappedf(float(Time.get_ticks_usec() - measurement_started_usec) / 1000000.0, 0.1),
			" objects=", row.census.objects, " expired=", row.census.crew_router.expired_canvas_refs,
			" nodes=", row.census.nodes, " frames=", aggregate_count, " hitches50=", hitches.size())
	if FileAccess.file_exists(out_path + ".stop"):
		stop_measurement("cancel_requested", previous_frame_usec)

func check_stream_error() -> void:
	if stream.get_error() != OK:
		check(false, "Periodic observation write failed")
		stop_measurement("stream_write_error", previous_frame_usec)

func retain_frames() -> void:
	super.retain_frames()
	var sparse: Array = []
	var count := 0
	var sum_usec := 0
	for usec in range(1, HIST_LIMIT):
		var occurrences := histogram[usec]
		if occurrences > 0:
			sparse.append([usec, occurrences])
			count += occurrences
			sum_usec += usec * occurrences
	var above: Array[int] = []
	var over100 := 0
	var over400 := 0
	for row in hitches:
		above.append(int(row.usec))
		count += 1; sum_usec += int(row.usec)
		if row.usec >= 100000: over100 += 1
		if row.usec >= 400000: over400 += 1
	above.sort()
	evidence.measurement.merge({"mean_ms": float(aggregate_sum) / aggregate_count / 1000.0 if aggregate_count > 0 else null,
		"fps": float(aggregate_count) * 1000000.0 / aggregate_sum if aggregate_sum > 0 else null,
		"histogram_usec_count": sparse, "hitch_rows": hitches, "frames_at_least50ms": hitches.size(),
		"frames_at_least100ms": over100, "frames_at_least400ms": over400,
		"p95_ms": percentile_ms(sparse, above, 0.95), "p99_ms": percentile_ms(sparse, above, 0.99)})
	if validate_raw: evidence.measurement["canary_raw_usec"] = raw_validation
	evidence["stream"] = {"path": stream_path, "rows": stream_rows, "max_write_usec": write_max_usec,
		"retained_periodic_rows": periodic.size(), "retained_raw_frames": raw_validation.size()}
	check(count == aggregate_count and sum_usec == aggregate_sum, "Histogram plus all hitch rows accounts for every measured interval exactly")

func percentile_ms(sparse: Array, above: Array[int], quantile: float) -> float:
	var rank := ceili(aggregate_count * quantile)
	var cumulative := 0
	for pair in sparse:
		cumulative += int(pair[1])
		if cumulative >= rank: return float(pair[0]) / 1000.0
	return float(above[rank - cumulative - 1]) / 1000.0 if rank > cumulative and rank - cumulative <= above.size() else 0.0

func finish(normal_quit: bool) -> void:
	if stream != null:
		stream.flush(); stream.close(); stream = null
	if not out_path.is_empty() and FileAccess.file_exists(stream_path):
		evidence["stream_sha256"] = FileAccess.get_sha256(stream_path)
	super.finish(normal_quit)
