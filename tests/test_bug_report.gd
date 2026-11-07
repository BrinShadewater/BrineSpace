extends SceneTree
# Run in an isolated user-data project with scripts/bug_report.gd copied to res://bug_report.gd.
var failures := 0
var report
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok:
		failures += 1
		push_error(message)
func run():
	report = load("res://bug_report.gd").new()
	root.add_child(report)
	for i in range(3): await process_frame
	DirAccess.make_dir_recursive_absolute("user://logs")
	var log_file := FileAccess.open("user://logs/godot.log", FileAccess.WRITE)
	log_file.store_string("x".repeat(3 * 1024 * 1024) + "END"); log_file.close()
	var old_log := FileAccess.open("user://logs/godot2026-09-09.log", FileAccess.WRITE)
	old_log.store_string("previous session"); old_log.close()
	DirAccess.remove_absolute("user://dialogue_trace.log")
	var missing_trace_files: Array = []
	report._add_logs(missing_trace_files)
	check(not missing_trace_files.any(func(entry): return entry.name == "logs/dialogue_trace.log"), "Missing optional dialogue trace is omitted")
	check(not FileAccess.file_exists("user://dialogue_trace.log"), "Reporting does not create a dialogue trace")
	var trace := FileAccess.open("user://dialogue_trace.log", FileAccess.WRITE)
	trace.store_string("x".repeat(3 * 1024 * 1024) + "COMPLETE crew_hab\n(built/crew_hab)\n"); trace.close()
	var save_file := FileAccess.open("user://brine_save.json", FileAccess.WRITE)
	save_file.store_string('{"fixture":true}'); save_file.close()
	var key := InputEventKey.new(); key.keycode = KEY_F8; key.pressed = true
	report._input(key)
	check(paused and report.overlay.visible, "F8 opens and pauses")
	check(not report.pending_captured_at.is_empty(), "F8 captures diagnostics at the key press, not at save")
	var captured_at: String = report.pending_captured_at
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("user://report-overlay.png")
	report.note_field.text = "enter note"
	report.note_field.text_submitted.emit("enter note")
	check(not report.last_report_path.is_empty() and report.overlay.visible and not report.note_field.visible, "Enter in the note saves the report")
	report._hide_overlay()
	report._input(key)
	var first: String = report.save_report("fixture note")
	var second: String = report.save_report("second report")
	check(first != second and not first.is_empty() and not second.is_empty(), "Unique report paths")
	var zip := ZIPReader.new()
	check(zip.open(first) == OK, "Valid ZIP")
	check(zip.read_file("report.txt").get_string_from_utf8().contains("fixture note"), "Tester note retained")
	check(zip.read_file("report.txt").get_string_from_utf8().contains("captured at F8: " + captured_at), "Report records when F8 was pressed")
	check(zip.read_file("logs/current.log").size() == 2097152, "Log tail capped at 2 MiB")
	check(zip.read_file("logs/current.log").get_string_from_utf8().ends_with("END"), "Log keeps newest bytes")
	check(zip.read_file("logs/previous.log").get_string_from_utf8() == "previous session", "Previous log included")
	check(zip.file_exists("logs/dialogue_trace.log"), "Construction dialogue trace included")
	check(zip.read_file("logs/dialogue_trace.log").size() == report.LOG_TAIL_BYTES, "Dialogue trace uses the bounded log tail")
	check(zip.read_file("logs/dialogue_trace.log").get_string_from_utf8().ends_with("COMPLETE crew_hab\n(built/crew_hab)\n"), "Dialogue trace keeps the newest ordered events")
	check(zip.file_exists("saves/brine_save.json"), "Save included")
	var image := Image.new()
	check(image.load_png_from_buffer(zip.read_file("screenshot.png")) == OK and not image.is_empty(), "Screenshot decodes")
	zip.close()
	report._hide_overlay(); check(not paused, "Closing restores running state")
	paused = true
	report._input(key); check(report.overlay.visible, "F8 works while paused")
	report._hide_overlay(); check(paused, "Closing preserves prior pause")
	paused = false
	check(not report._write_folder("user://partial", [{"name":"ok.txt","data":PackedByteArray([1])},{"name":"ok.txt/no.txt","data":PackedByteArray([2])}]), "Partial folder is not success")
	check(report._write_folder("user://fallback", [{"name":"crash/example.dmp","data":PackedByteArray([1])}]), "Folder fallback writes nested file")
	check(report._report_contains_dump("user://fallback"), "Folder dump disclosure")
	# Simulate a stale session, then verify the automatic bundle and overlay.
	report._write_lock()
	check(FileAccess.file_exists(report.LOCK_PATH), "Session lock written")
	report._detect_previous_session()
	await process_frame
	check(not report.last_report_path.is_empty() and report.overlay.visible, "Unclean session automatically reports")
	report._hide_overlay(); report._remove_lock()
	check(not FileAccess.file_exists(report.LOCK_PATH), "Clean shutdown removes lock")
	report.queue_free(); await process_frame
	print("BUG REPORT TEST: %d failures" % failures)
	quit(1 if failures else 0)
