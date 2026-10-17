extends "release_smoke_base.gd"
## External actual-package lifecycle adapter, based on the frozen
## tools/release_transition_probe.gd. Not shipped; not a loading/FPS benchmark.
## Driver copies frozen tests/release_new_game_smoke.gd beside this file as
## release_smoke_base.gd, installs its pre-write BugReport profile guard, and
## overrides only run/main_scene to its empty scene plus this autoload.
## The fixture then uses packaged title/Continue/Return to Title/Quit handlers.
## --user-dir=<resolved scratch profile> --save=<copied checkpoint>
## --out=<absolute JSON> --transitions=10 [--qa-screen=2]
## Native windowed secondary display, Dummy audio, BRINE_SILENT=1, scratch APPDATA.
## Pause/minimize dialogue only for repeatable lifecycle observations. No free
## building/failure flags, alternate renderer, source replacements, or uploads.
## Parent owns owner-save fingerprints, package hashes, log review and timeout.
const Saves = preload("res://scripts/run_save.gd")
const SafeImage = preload("res://scripts/safe_image.gd")
const LOOP := "user://transition.loop"
const META := "user://transition.meta"
var options: Dictionary = {}
var evidence: Dictionary = {"schema": "brinespace.package-transitions.v1", "checks": [], "transitions": []}
var out_path := ""
var source_path := ""
var qa_screen := -1
var transition_count := 10
var expected_rooms := 0
var expected_run_id := ""
var last_render_usec := 0
var guard_failure := ""
var guarded := false
var finished := false

func check(ok: bool, message: String):
	evidence.checks.append({"ok": ok, "message": message})
	super.check(ok, message)

func _record_render() -> void:
	last_render_usec = Time.get_ticks_usec()

func _process(_delta: float) -> void:
	if not guarded or finished or not guard_failure.is_empty(): return
	var window: Window = get_window()
	if window.mode == Window.MODE_MINIMIZED: guard_failure = "QA window minimized"
	elif window.current_screen != qa_screen: guard_failure = "QA window left selected secondary screen"
	elif not window.is_input_disabled(): guard_failure = "Physical viewport input unexpectedly enabled"
	elif not AudioServer.is_bus_mute(AudioServer.get_bus_index("Master")): guard_failure = "QA audio unexpectedly unmuted"
	if not guard_failure.is_empty(): check(false, guard_failure)

func healthy() -> bool:
	return not finished and guard_failure.is_empty()

func _route_scratch_paths(node: Node) -> void:
	var script = node.get_script()
	if script == null: return
	if script.resource_path == "res://scripts/main.gd":
		node.run_save_path = LOOP
		node.meta.save_path = META
	elif script.resource_path == "res://scripts/title_screen.gd":
		node.run_save_path = LOOP

func configure() -> bool:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--") and "=" in arg:
			var bits: PackedStringArray = arg.trim_prefix("--").split("=", true, 1)
			options[bits[0]] = bits[1]
	var expected: String = str(options.get("user-dir", "")).replace(char(92), "/").simplify_path()
	var profile: String = OS.get_user_data_dir().replace(char(92), "/").simplify_path()
	out_path = str(options.get("out", ""))
	source_path = str(options.get("save", ""))
	transition_count = int(options.get("transitions", "10"))
	check(not expected.is_empty() and profile == expected, "Resolved profile matches explicitly isolated scratch profile")
	check(out_path.is_absolute_path() and source_path.is_absolute_path(), "Absolute evidence and copied-checkpoint paths supplied")
	check(FileAccess.file_exists(source_path), "Copied source checkpoint exists")
	check(transition_count >= 2 and transition_count <= 10, "Bounded transition count selected (2..10)")
	check(not OS.is_debug_build() and DisplayServer.get_name() != "headless", "Actual release template with native display")
	check(OS.get_environment("BRINE_SILENT") == "1", "Driver selected silent fixture mode")
	if failures > 0: return false
	var checkpoint: Dictionary = Saves.read(source_path)
	check(not checkpoint.is_empty() and not checkpoint.get("_recovered_backup", false), "Copied primary checkpoint is readable without backup recovery")
	if checkpoint.is_empty(): return false
	expected_rooms = checkpoint.state.placed_rooms.size()
	expected_run_id = str(checkpoint.get("run_id", ""))
	check(expected_rooms > 0 and not expected_run_id.is_empty(), "Copied checkpoint has station/run identity")
	var build: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://build_info.json"))
	check(build is Dictionary, "Actual package build metadata is readable")
	if failures > 0: return false
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), true)
	var window: Window = get_window()
	window.set_disable_input(true)
	var primary: int = DisplayServer.get_primary_screen()
	if options.has("qa-screen"): qa_screen = int(options["qa-screen"])
	else:
		for index in range(DisplayServer.get_screen_count()):
			if index != primary and DisplayServer.screen_get_size(index).x >= window.size.x and DisplayServer.screen_get_size(index).y >= window.size.y:
				qa_screen = index
				break
	check(qa_screen >= 0 and qa_screen < DisplayServer.get_screen_count() and qa_screen != primary, "Usable secondary display selected")
	if failures > 0: return false
	window.current_screen = qa_screen
	var extent: Vector2i = DisplayServer.screen_get_size(qa_screen)
	check(extent.x >= window.size.x and extent.y >= window.size.y, "QA client fits selected display")
	if failures > 0: return false
	window.position = DisplayServer.screen_get_position(qa_screen) + Vector2i(maxi(0, (extent.x - window.size.x) / 2), maxi(0, (extent.y - window.size.y) / 2))
	evidence.merge({"debug": OS.is_debug_build(), "pid": OS.get_process_id(), "profile": profile, "build": build,
		"source_checkpoint": source_path, "source_sha256": FileAccess.get_sha256(source_path), "source_rooms": expected_rooms,
		"source_run_id": expected_run_id, "requested_transitions": transition_count,
		"window": {"screen": qa_screen, "primary": primary, "size": str(window.size), "muted": true},
		"scope": "Actual-package title/Continue/Return lifecycle with paused stations; not normal-entry, physical-input, gameplay-behavior, FPS, or loading-time acceptance.",
		"metric_scope": "Raw post-loading and settled counters; warmed caches and generic exit warnings alone do not establish leaks. Orphan monitor counts Nodes, not all RefCounted objects."})
	get_tree().root.child_entered_tree.connect(_route_scratch_paths)
	RenderingServer.frame_post_draw.connect(_record_render)
	guarded = true
	return true

func fresh_render() -> bool:
	var previous := last_render_usec
	var deadline := Time.get_ticks_msec() + 10000
	while healthy() and Time.get_ticks_msec() < deadline:
		if last_render_usec > previous: return true
		await get_tree().process_frame
	check(false, "Native rendered frame observed within10s")
	return false

func loading_present() -> bool:
	for child in get_tree().root.get_children():
		if child.has_method("finish_after_scene_change"): return true
	return false

func advance_loading() -> void:
	for child in get_tree().root.get_children():
		if child.has_method("type_transmission") and child.get("typing") == true:
			var accept := InputEventAction.new()
			accept.action = "ui_accept"; accept.pressed = true
			child._input(accept)
		if child.has_method("finish_after_scene_change"):
			var button = child.get("continue_button")
			if is_instance_valid(button) and button.visible and not button.disabled: button.pressed.emit()

func wait_title():
	var deadline := Time.get_ticks_msec() + 30000
	while healthy() and Time.get_ticks_msec() < deadline:
		var title = get_tree().current_scene
		if title != null and title.has_method("_continue_loop") and not loading_present(): return title
		await get_tree().process_frame
	check(false, "Packaged title is observable within30s")
	return null

func wait_station(previous_title):
	var deadline := Time.get_ticks_msec() + 120000
	while healthy() and Time.get_ticks_msec() < deadline:
		advance_loading()
		var game = get_tree().current_scene
		if game != null and game != previous_title and game.get("startup_complete") == true and game.process_mode != Node.PROCESS_MODE_DISABLED and not loading_present(): return game
		await get_tree().process_frame
	check(false, "Continue restored an uncovered station within120s")
	return null

func counters(label: String, game = null) -> Dictionary:
	return {"stage": label, "ticks_usec": Time.get_ticks_usec(), "process_frame": Engine.get_process_frames(),
		"rooms": game.placed_rooms.size() if is_instance_valid(game) else 0,
		"visible_rooms": game.grid_view.visible_draw_rooms.size() if is_instance_valid(game) else 0,
		"texture_bytes": int(Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)),
		"static_bytes": int(Performance.get_monitor(Performance.MEMORY_STATIC)),
		"objects": int(Performance.get_monitor(Performance.OBJECT_COUNT)),
		"resources": int(Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT)),
		"nodes": int(Performance.get_monitor(Performance.OBJECT_NODE_COUNT)),
		"orphan_nodes": int(Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT))}

func settle(scene, station: bool) -> bool:
	var stable_frames := 0
	var deadline := Time.get_ticks_msec() + 20000
	while healthy() and Time.get_ticks_msec() < deadline:
		if not is_instance_valid(scene) or get_tree().current_scene != scene: break
		if not await fresh_render(): return false
		var stable := not loading_present()
		if station: stable = stable and not scene.camera_zoom_moving and not scene.grid_view.settle_backlog and scene.grid_view.pending_layers.is_empty()
		else: stable = stable and not scene.starting
		stable_frames = stable_frames + 1 if stable else 0
		if stable_frames >= 30: return true
	check(false, "Scene maintained30 observable settled rendered frames within20s")
	return false

func writers_idle() -> bool:
	var report = get_tree().root.get_node_or_null("BugReport")
	check(report != null, "Packaged guarded reporter is present")
	if report == null: return false
	var deadline := Time.get_ticks_msec() + 30000
	while healthy() and Time.get_ticks_msec() < deadline:
		if report.get("_report_thread") == null and report.get("_report_jobs").is_empty() and report.get("_ui_report_pending") == false:
			return true
		await get_tree().process_frame
	check(false, "Accepted report writers/UI completion became idle within30s")
	return false

func finish(normal_quit: bool) -> void:
	if finished: return
	finished = true
	check(SafeImage.failures.is_empty(), "No safe-image placeholders in exercised lifecycle")
	evidence["safe_image_failures"] = SafeImage.failures.duplicate(true)
	evidence["engine_script_errors"] = release_errors.messages.duplicate()
	check(release_errors.messages.is_empty(), "No captured engine/script errors")
	evidence["guard_failure"] = guard_failure
	evidence["failures"] = failures
	evidence["shutdown"] = {"normal_title_quit_planned": normal_quit and failures == 0,
		"report_writer_idle_verified": normal_quit, "exit_warnings_reviewed_externally": true}
	var written := false
	if not out_path.is_empty():
		var file := FileAccess.open(out_path, FileAccess.WRITE)
		if file != null:
			file.store_string(JSON.stringify(evidence, "\t")); file.flush()
			written = file.get_error() == OK
			file.close()
	if not written: failures += 1
	print("ACTUAL_PACKAGE_TRANSITIONS_COMPLETE count=", evidence.transitions.size(), " failures=", failures, " debug=", OS.is_debug_build(), " evidence_flushed=", written)
	# Unwind this completion stack before invoking the application's own Quit.
	call_deferred("_quit_after_evidence", normal_quit and failures == 0)

func _quit_after_evidence(normal_quit: bool) -> void:
	var title = get_tree().current_scene
	OS.remove_logger(release_errors)
	if normal_quit and title != null and title.has_method("_continue_loop") and is_instance_valid(title.quit_button) and not title.quit_button.disabled:
		print("ACTUAL_PACKAGE_TRANSITIONS_NORMAL_QUIT title_button=true audio_drain_handler=true")
		title.quit_button.pressed.emit()
	else:
		print("ACTUAL_PACKAGE_TRANSITIONS_FALLBACK_QUIT failures=", failures)
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
	for iteration in range(transition_count):
		if not healthy(): finish(false); return
		copy_error = DirAccess.copy_absolute(source_path, ProjectSettings.globalize_path(LOOP))
		check(copy_error == OK, "Reset scratch loop from identical immutable checkpoint")
		if copy_error != OK: finish(false); return
		title.run_save_path = LOOP
		check(title.continue_button.visible and not title.continue_button.disabled, "Packaged Continue is offered")
		if not title.continue_button.visible or title.continue_button.disabled: finish(false); return
		title.continue_button.pressed.emit()
		var game = await wait_station(title)
		if game == null: finish(false); return
		title = null
		# Restore may retarget autosave at a loaded path. Always restore the
		# explicit writable scratch destination before any normal save handler.
		game.run_save_path = LOOP
		game.meta.save_path = META
		if is_instance_valid(game.crew_comms): game.crew_comms.archive_path = LOOP + ".comms.json"
		check(game.placed_rooms.size() == expected_rooms and game.run_save_id == expected_run_id, "Continue restored expected station/run identity")
		check(not game.testing_free_build and not game.testing_disable_failures, "Normal costs/failure flags remain enabled")
		if not await fresh_render(): finish(false); return
		var row := {"iteration": iteration + 1, "station_postloading": counters("station_postloading", game)}
		if is_instance_valid(game.crew_comms): game.crew_comms.minimize()
		game._set_paused(true, false)
		if not await settle(game, true): finish(false); return
		row["station_settled"] = counters("station_settled", game)
		game._menu_return_title()
		game = null
		title = await wait_title()
		if title == null: finish(false); return
		if not await fresh_render(): finish(false); return
		row["title_postreturn"] = counters("title_postreturn")
		if not await settle(title, false): finish(false); return
		row["title_settled"] = counters("title_settled")
		evidence.transitions.append(row)
		print("PACKAGE_TRANSITION ", JSON.stringify(row))
	var rows: Array = evidence.transitions
	var first: float = rows[0].station_settled.texture_bytes
	var last: float = rows.back().station_settled.texture_bytes
	var growth: float = 100.0 * (last / first - 1.0) if first > 0.0 else 0.0
	evidence["texture_growth_percent"] = growth
	evidence["texture_growth_pass"] = first > 0.0 and growth <= 5.0
	check(first > 0.0 and growth <= 5.0, "Frozen transition-probe texture growth guard <=5percent")
	evidence["source_after_sha256"] = FileAccess.get_sha256(source_path)
	check(evidence.source_after_sha256 == evidence.source_sha256, "Immutable copied source checkpoint preserved")
	var idle: bool = await writers_idle()
	check(idle, "Report writers completed before final evidence/normal Quit")
	finish(idle)
