extends Node
## Bug report bundles for testers. Two triggers: the previous session did not
## close normally (session lock still present at launch), or F8. Either way the
## result is one zip under user://bug_reports that a tester can send along.
## Engine APIs only; this script must never be the thing that crashes.

const REPORT_DIR := "user://bug_reports"
const LOCK_DIR := "user://bug_report"
const LOCK_PATH := "user://bug_report/session.lock"
const LOG_DIR := "user://logs"
const LOG_TAIL_BYTES := 2 * 1024 * 1024
const DUMP_LIMIT_BYTES := 64 * 1024 * 1024
const DUMP_COUNT := 2
const SAVE_FILES := [
	"brine_save.json", "brine_save.json.bak", "brine_save.json.tmp",
	"brine_loop.save", "brine_loop.save.bak", "brine_loop.save.tmp",
	"brine_loop.save.comms.json", "brine_settings.cfg",
]

var last_report_path := ""
var pending_screenshot: Image = null
var crashed_at := ""
var lock_unix := 0
var skipped_dumps: Array = []
var overlay: CanvasLayer = null
var title_label: Label = null
var body_label: Label = null
var note_field: LineEdit = null
var button_row: HBoxContainer = null

func _enter_tree() -> void:
	if OS.has_feature("editor"):
		return
	_detect_previous_session()
	_write_lock()

func _exit_tree() -> void:
	if OS.has_feature("editor"):
		return
	_remove_lock()

func _detect_previous_session() -> void:
	if not FileAccess.file_exists(LOCK_PATH):
		return
	crashed_at = FileAccess.get_file_as_string(LOCK_PATH).strip_edges()
	for line in crashed_at.split("\n"):
		if line.begins_with("unix="):
			lock_unix = int(line.trim_prefix("unix="))
	var path := save_report("", true)
	call_deferred("_show_crash_overlay", path)

func _write_lock() -> void:
	if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(LOCK_DIR)) != OK:
		return
	var file := FileAccess.open(LOCK_PATH, FileAccess.WRITE)
	if file == null:
		return
	file.store_string("unix=%d\nstarted=%s\nversion=%s\n" % [
		int(Time.get_unix_time_from_system()),
		Time.get_datetime_string_from_system(false, true),
		str(ProjectSettings.get_setting("application/config/version", "unknown")),
	])

func _remove_lock() -> void:
	var dir := DirAccess.open(LOCK_DIR)
	if dir != null and dir.file_exists("session.lock"):
		dir.remove("session.lock")

func save_report(note: String, after_crash: bool = false) -> String:
	last_report_path = ""
	skipped_dumps.clear()
	var files: Array = []
	_add_logs(files)
	_add_saves(files)
	if pending_screenshot != null and not pending_screenshot.is_empty():
		files.append({"name": "screenshot.png", "data": pending_screenshot.save_png_to_buffer()})
	var dumps_found := 0
	if after_crash:
		dumps_found = _add_crash_dumps(files)
	var summary := _report_text(note, after_crash, files, dumps_found)
	files.push_front({"name": "report.txt", "data": summary.to_utf8_buffer()})
	pending_screenshot = null
	var stamp := Time.get_datetime_string_from_system(false, true).replace("-", "").replace(":", "").replace(" ", "-")
	var base := REPORT_DIR + "/brinespace-report-" + stamp
	if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(REPORT_DIR)) != OK:
		push_warning("BugReport: could not create " + REPORT_DIR)
		return ""
	if _write_zip(base + ".zip", files):
		last_report_path = base + ".zip"
	elif _write_folder(base, files):
		last_report_path = base
	return last_report_path

func _write_zip(path: String, files: Array) -> bool:
	var packer := ZIPPacker.new()
	if packer.open(path) != OK:
		push_warning("BugReport: ZIPPacker could not open " + path)
		return false
	var ok := true
	for entry in files:
		if packer.start_file(entry.name) != OK or packer.write_file(entry.data) != OK or packer.close_file() != OK:
			ok = false
	if packer.close() != OK:
		ok = false
	return ok

func _write_folder(path: String, files: Array) -> bool:
	if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path)) != OK:
		return false
	var written := 0
	for entry in files:
		var target: String = path + "/" + entry.name
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(target.get_base_dir()))
		var file := FileAccess.open(target, FileAccess.WRITE)
		if file == null:
			continue
		file.store_buffer(entry.data)
		written += 1
	return written > 0

func _add_logs(files: Array) -> void:
	files.append({"name": "logs/current.log", "data": _tail(LOG_DIR + "/godot.log")})
	var previous := _previous_log_name()
	if not previous.is_empty():
		files.append({"name": "logs/previous.log", "data": _tail(LOG_DIR + "/" + previous)})

func _previous_log_name() -> String:
	# Godot copies the previous session into godot<launch time>.log at startup,
	# so the newest timestamped file is the previous session.
	var dir := DirAccess.open(LOG_DIR)
	if dir == null:
		return ""
	var names: Array = []
	for name in dir.get_files():
		if name != "godot.log" and name.begins_with("godot") and name.ends_with(".log"):
			names.append(name)
	names.sort()
	return "" if names.is_empty() else str(names[names.size() - 1])

func _tail(path: String) -> PackedByteArray:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return ("(could not read %s: error %d)" % [path.get_file(), FileAccess.get_open_error()]).to_utf8_buffer()
	var length := file.get_length()
	var wanted := mini(length, LOG_TAIL_BYTES)
	if length > wanted:
		file.seek(length - wanted)
	return file.get_buffer(wanted)

func _add_saves(files: Array) -> void:
	for name in SAVE_FILES:
		var path: String = "user://" + name
		if FileAccess.file_exists(path):
			files.append({"name": "saves/" + name, "data": FileAccess.get_file_as_bytes(path)})

func _add_crash_dumps(files: Array) -> int:
	var base := OS.get_environment("LOCALAPPDATA")
	if base.is_empty():
		return 0
	var dump_dir := base.path_join("CrashDumps")
	var dir := DirAccess.open(dump_dir)
	if dir == null:
		return 0
	var candidates: Array = []
	for name in dir.get_files():
		if not (name.begins_with("BrineSpace") and name.ends_with(".dmp")):
			continue
		var full := dump_dir.path_join(name)
		var modified := FileAccess.get_modified_time(full)
		if modified < lock_unix:
			continue
		candidates.append({"name": name, "time": modified, "path": full})
	candidates.sort_custom(func(a, b): return a.time > b.time)
	var added := 0
	for entry in candidates.slice(0, DUMP_COUNT):
		var file := FileAccess.open(entry.path, FileAccess.READ)
		if file == null:
			continue
		if file.get_length() > DUMP_LIMIT_BYTES:
			skipped_dumps.append(entry.name)
			continue
		files.append({"name": "crash/" + entry.name, "data": file.get_buffer(file.get_length())})
		added += 1
	return added

func _show_crash_overlay(path: String) -> void:
	var body := "A bug report was saved as %s. Send the zip to Yuri." % path.get_file()
	if path.is_empty():
		body = "A bug report could not be written. The log folder may still help: it is next to the bug_reports folder."
	elif _report_contains_dump(path):
		body += "\nIt includes a crash dump, which can contain data from the game's memory."
	_show_overlay("LAST SESSION DID NOT CLOSE NORMALLY", body, false, [["Open folder", _open_report_folder], ["Dismiss", _hide_overlay]])

func _report_contains_dump(path: String) -> bool:
	var reader := ZIPReader.new()
	if reader.open(path) != OK:
		return false
	var found := false
	for name in reader.get_files():
		if str(name).begins_with("crash/"):
			found = true
	reader.close()
	return found

func _build_overlay() -> void:
	overlay = CanvasLayer.new()
	overlay.name = "BugReportOverlay"
	overlay.layer = 1000
	overlay.process_mode = Node.PROCESS_MODE_ALWAYS
	var backdrop := Control.new()
	backdrop.set_anchors_preset(Control.PRESET_FULL_RECT)
	backdrop.mouse_filter = Control.MOUSE_FILTER_STOP
	overlay.add_child(backdrop)
	var panel := PanelContainer.new()
	panel.set_anchors_preset(Control.PRESET_CENTER)
	panel.grow_horizontal = Control.GROW_DIRECTION_BOTH
	panel.grow_vertical = Control.GROW_DIRECTION_BOTH
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.03, 0.06, 0.09, 0.97)
	style.border_color = Color(0.36, 0.72, 0.78)
	style.set_border_width_all(2)
	style.set_content_margin_all(20)
	panel.add_theme_stylebox_override("panel", style)
	backdrop.add_child(panel)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	panel.add_child(box)
	title_label = Label.new()
	title_label.add_theme_font_size_override("font_size", 18)
	box.add_child(title_label)
	body_label = Label.new()
	body_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body_label.custom_minimum_size = Vector2(520, 0)
	box.add_child(body_label)
	note_field = LineEdit.new()
	note_field.placeholder_text = "What were you doing?"
	note_field.max_length = 300
	box.add_child(note_field)
	button_row = HBoxContainer.new()
	button_row.add_theme_constant_override("separation", 8)
	button_row.alignment = BoxContainer.ALIGNMENT_END
	box.add_child(button_row)
	add_child(overlay)

func _show_overlay(title: String, body: String, with_note: bool, buttons: Array) -> void:
	if overlay == null:
		_build_overlay()
	title_label.text = title
	body_label.text = body
	note_field.visible = with_note
	note_field.text = ""
	for child in button_row.get_children():
		child.queue_free()
	for spec in buttons:
		var button := Button.new()
		button.text = str(spec[0])
		button.custom_minimum_size = Vector2(120, 36)
		button.pressed.connect(spec[1])
		button_row.add_child(button)
	overlay.visible = true

func _hide_overlay() -> void:
	if overlay != null:
		overlay.visible = false

func _open_report_folder() -> void:
	var folder := ProjectSettings.globalize_path(REPORT_DIR)
	if OS.shell_show_in_file_manager(folder, true) != OK:
		OS.shell_open(folder)

func _report_text(note: String, after_crash: bool, files: Array, dumps_found: int) -> String:
	var lines: Array = []
	lines.append("BrineSpace bug report")
	lines.append("trigger: " + ("previous session did not close normally" if after_crash else "manual (F8)"))
	lines.append("note: " + (note if not note.is_empty() else "(none)"))
	lines.append("bundle time: " + Time.get_datetime_string_from_system(false, true))
	lines.append("previous session lock: " + (crashed_at.replace("\n", " | ") if not crashed_at.is_empty() else "(none)"))
	lines.append("game version: " + str(ProjectSettings.get_setting("application/config/version", "unknown")))
	lines.append("godot: " + str(Engine.get_version_info().get("string", "unknown")))
	lines.append("template: " + ("debug" if OS.is_debug_build() else "release"))
	lines.append("os: %s %s" % [OS.get_name(), OS.get_version()])
	lines.append("cpu: " + OS.get_processor_name())
	var memory := OS.get_memory_info()
	lines.append("memory MB physical/free: %d / %d" % [int(memory.get("physical", 0)) / 1048576, int(memory.get("free", 0)) / 1048576])
	lines.append("gpu: %s (%s)" % [RenderingServer.get_video_adapter_name(), RenderingServer.get_video_adapter_vendor()])
	lines.append("graphics api: " + RenderingServer.get_video_adapter_api_version())
	lines.append("renderer: %s / %s" % [RenderingServer.get_current_rendering_method(), RenderingServer.get_current_rendering_driver_name()])
	lines.append("window: %s screen: %s" % [DisplayServer.window_get_size(), DisplayServer.screen_get_size()])
	lines.append("uptime seconds: %d" % (Time.get_ticks_msec() / 1000))
	var scene: Node = get_tree().current_scene if is_inside_tree() else null
	lines.append("scene: " + (scene.scene_file_path if scene != null else "none"))
	if after_crash:
		lines.append("crash dumps packed: %d" % dumps_found)
		for name in skipped_dumps:
			lines.append("crash dump skipped (over size limit): " + str(name))
	lines.append("")
	lines.append("files:")
	for entry in files:
		lines.append("  %8d  %s" % [PackedByteArray(entry.data).size(), entry.name])
	return "\n".join(lines) + "\n"
