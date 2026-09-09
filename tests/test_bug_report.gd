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
	var save_file := FileAccess.open("user://brine_save.json", FileAccess.WRITE)
	save_file.store_string('{"fixture":true}'); save_file.close()
	var key := InputEventKey.new(); key.keycode = KEY_F8; key.pressed = true
	report._input(key)
	check(paused and report.overlay.visible, "F8 opens and pauses")
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("user://report-overlay.png")
	var first: String = report.save_report("fixture note")
	var second: String = report.save_report("second report")
	check(first != second and not first.is_empty() and not second.is_empty(), "Unique report paths")
	var zip := ZIPReader.new()
	check(zip.open(first) == OK, "Valid ZIP")
	check(zip.read_file("report.txt").get_string_from_utf8().contains("fixture note"), "Tester note retained")
	check(zip.read_file("logs/current.log").size() == 2097152, "Log tail capped at 2 MiB")
	check(zip.read_file("logs/current.log").get_string_from_utf8().ends_with("END"), "Log keeps newest bytes")
	check(zip.read_file("logs/previous.log").get_string_from_utf8() == "previous session", "Previous log included")
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
