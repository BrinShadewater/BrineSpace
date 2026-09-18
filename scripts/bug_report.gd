extends Node
## Bug report bundles for testers. Two triggers: the previous session did not
## close normally (session lock still present at launch), or F8. Either way the
## result is one zip under user://bug_reports that a tester can send along.
## Engine APIs only; this script must never be the thing that crashes.

const REPORT_DIR := "user://bug_reports"
# Fixtures point this at their own folder so test runs never add reports to the player's.
var report_dir := REPORT_DIR
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

var owns_session_lock := false
var was_paused := false
var last_report_path := ""
var pending_screenshot: Image = null
# Diagnostics captured the moment F8 is pressed, so a report shows the moment being
# reported rather than the idle frames spent typing the note (owner playtest).
var pending_files: Array = []
var pending_captured_at := ""
var pending_uptime := -1
# "The game will not answer a click" leaves no error behind, so the state that decides whether a
# click can land is written down at F8: the pause flag, the mouse mode, what has focus, what sits
# under the pointer, and anything full-screen that swallows input (owner report, Sept 17).
var pending_input: Array = []
var stuck_pause_recoveries := 0
var crashed_at := ""
var lock_unix := 0
var skipped_dumps: Array = []
var overlay: CanvasLayer = null
var title_label: Label = null
var body_label: Label = null
var note_field: LineEdit = null
var button_row: HBoxContainer = null
var performance_monitor: Node

func _ready() -> void:
	performance_monitor=preload("res://scripts/performance_monitor.gd").new()
	add_child(performance_monitor)

func _enter_tree() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	if OS.has_feature("editor"):
		return
	# A second running copy must not report a crash or remove the first copy's lock.
	if FileAccess.file_exists(LOCK_PATH):
		for line in FileAccess.get_file_as_string(LOCK_PATH).split("\n"):
			if line.begins_with("pid=") and OS.is_process_running(int(line.trim_prefix("pid="))):
				return
	_detect_previous_session()
	_write_lock()

func _exit_tree() -> void:
	if owns_session_lock:
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
	file.store_string("pid=%d\nunix=%d\nstarted=%s\nversion=%s\n" % [
		OS.get_process_id(),
		int(Time.get_unix_time_from_system()),
		Time.get_datetime_string_from_system(false, true),
		str(ProjectSettings.get_setting("application/config/version", "unknown")),
	])

	file.flush()
	owns_session_lock = file.get_error() == OK

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
	if not after_crash:
		if pending_captured_at.is_empty(): _capture_diagnostics()
		files.append_array(pending_files)
	# Breadcrumbs from the session that died: the crash report is the only place they show up.
	if after_crash and FileAccess.file_exists("user://last_session.json"):
		files.append({"name":"diagnostics/previous_session.json","data":FileAccess.get_file_as_bytes("user://last_session.json")})
	var artwork: Dictionary = preload("res://scripts/safe_image.gd").failures
	if not artwork.is_empty(): files.append({"name":"diagnostics/artwork.json","data":JSON.stringify(artwork,"\t").to_utf8_buffer()})
	if pending_screenshot != null and not pending_screenshot.is_empty():
		files.append({"name": "screenshot.png", "data": pending_screenshot.save_png_to_buffer()})
	var dumps_found := 0
	if after_crash:
		dumps_found = _add_crash_dumps(files)
	var summary := _report_text(note, after_crash, files, dumps_found)
	files.push_front({"name": "report.txt", "data": summary.to_utf8_buffer()})
	_clear_pending()
	var stamp := Time.get_datetime_string_from_system(false, true).replace("-", "").replace(":", "").replace(" ", "-")
	var base := report_dir + "/brinespace-report-" + stamp + "-%d-%d" % [OS.get_process_id(), Time.get_ticks_usec()]
	var suffix := 0
	var candidate := base
	while FileAccess.file_exists(candidate + ".zip") or DirAccess.dir_exists_absolute(candidate):
		suffix += 1
		candidate = base + "-%d" % suffix
	base = candidate
	if DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(report_dir)) != OK:
		push_warning("BugReport: could not create " + report_dir)
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
		if packer.start_file(entry.name) != OK:
			ok = false
			continue
		if packer.write_file(entry.data) != OK:
			ok = false
		if packer.close_file() != OK:
			ok = false
	if packer.close() != OK:
		ok = false
	if not ok:
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
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
		file.flush()
		if file.get_error() == OK:
			written += 1
	return written == files.size() and written > 0

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

func _build_info() -> Dictionary:
	return preload("res://scripts/build_version.gd").build()

func _capture_diagnostics() -> void:
	pending_files = []
	_add_live_snapshot(pending_files)
	if is_instance_valid(performance_monitor):
		pending_files.append({"name":"diagnostics/performance.json","data":JSON.stringify(performance_monitor.snapshot(),"\t").to_utf8_buffer()})
	pending_captured_at = Time.get_datetime_string_from_system(false, true)
	pending_uptime = Time.get_ticks_msec() / 1000
	pending_input = _input_state()

func _input_state() -> Array:
	var lines: Array = []
	if not is_inside_tree(): return lines
	var tree := get_tree()
	lines.append("tree paused: %s" % tree.paused)
	lines.append("mouse mode: %d (0 visible, 2 captured, 3 confined)" % Input.get_mouse_mode())
	var viewport := get_viewport()
	if viewport == null: return lines
	var pointer: Vector2 = viewport.get_mouse_position()
	lines.append("pointer: %s  window: %s  viewport: %s" % [pointer, DisplayServer.window_get_size(), viewport.get_visible_rect().size])
	lines.append("focus owner: %s" % _node_name(viewport.gui_get_focus_owner()))
	lines.append("hovered control: %s" % _node_name(viewport.gui_get_hovered_control()))
	# Anything visible, full-screen and click-stopping, wherever it lives in the tree.
	var screen: Vector2 = viewport.get_visible_rect().size
	for node in tree.root.find_children("*", "Control", true, false):
		if not node.is_visible_in_tree() or node.mouse_filter == Control.MOUSE_FILTER_IGNORE: continue
		var rect: Rect2 = node.get_global_rect()
		if rect.size.x < screen.x * 0.9 or rect.size.y < screen.y * 0.9: continue
		lines.append("covers the screen: %s filter=%d alpha=%.2f rect=%s" % [_node_name(node), node.mouse_filter, node.get_modulate().a * node.get_self_modulate().a, rect])
	for node in tree.root.find_children("*", "CanvasLayer", true, false):
		if node.visible and node.layer >= 100:
			lines.append("layer %d visible: %s" % [node.layer, _node_name(node)])
	return lines

func _node_name(node) -> String:
	if node == null or not is_instance_valid(node): return "(none)"
	return "%s (%s)" % [str(node.get_path()).replace("/root/", ""), node.get_class()]

func _clear_pending() -> void:
	pending_screenshot = null
	pending_files = []
	pending_captured_at = ""
	pending_uptime = -1
	pending_input = []

func _add_live_snapshot(files: Array) -> void:
	var scene := get_tree().current_scene if is_inside_tree() else null
	var result: Dictionary = {"status":"unavailable", "reason":"no active station"}
	if scene != null and scene.has_method("capture_bug_report_snapshot"):
		result = scene.capture_bug_report_snapshot()
	if result.has("snapshot"):
		var bytes := var_to_bytes(result.snapshot)
		result.erase("snapshot")
		if bytes.size() <= 16 * 1024 * 1024:
			# Same checksum envelope as RunSave, under a distinct diagnostic name.
			var data := (bytes.hex_encode().sha256_text()+"\n").to_utf8_buffer()
			data.append_array(bytes)
			files.append({"name":"diagnostics/live_station.save","data":data})
		else:
			result = {"status":"unavailable", "reason":"snapshot exceeds 16 MiB limit"}
	files.append({"name":"diagnostics/live_station.json","data":JSON.stringify(result,"\t").to_utf8_buffer()})

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
	var body := "A bug report was saved as %s. Send it to Alex at Shadewater Labs (brinshadewater@gmail.com)." % path.get_file()
	if path.is_empty():
		body = "A bug report could not be written. The log folder may still help: it is next to the bug_reports folder."
	elif _report_contains_dump(path):
		body += "\nIt includes a crash dump, which can contain data from the game's memory."
	_show_overlay("LAST SESSION DID NOT CLOSE NORMALLY", body, false, [["Open folder", _open_report_folder], ["Dismiss", _hide_overlay]])

func _report_contains_dump(path: String) -> bool:
	if DirAccess.dir_exists_absolute(path):
		return not DirAccess.get_files_at(path.path_join("crash")).is_empty() if DirAccess.dir_exists_absolute(path.path_join("crash")) else false
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
	# Enter saves the report, like the Save report button (owner playtest).
	note_field.text_submitted.connect(func(_text: String) -> void:
		if overlay.visible and note_field.visible: _on_save_pressed())
	box.add_child(note_field)
	button_row = HBoxContainer.new()
	button_row.add_theme_constant_override("separation", 8)
	button_row.alignment = BoxContainer.ALIGNMENT_END
	box.add_child(button_row)
	overlay.visible = false
	add_child(overlay)

func _show_overlay(title: String, body: String, with_note: bool, buttons: Array) -> void:
	if overlay == null:
		_build_overlay()
	if not overlay.visible:
		was_paused = get_tree().paused
		get_tree().paused = true
	title_label.text = title
	body_label.text = body
	note_field.visible = with_note
	note_field.text = ""
	for child in button_row.get_children():
		button_row.remove_child(child)
		child.queue_free()
	for spec in buttons:
		var button := Button.new()
		button.text = str(spec[0])
		button.custom_minimum_size = Vector2(120, 36)
		button.pressed.connect(spec[1])
		button_row.add_child(button)
	overlay.visible = true

func _hide_overlay() -> void:
	if overlay != null and overlay.visible:
		overlay.visible = false
		get_tree().paused = was_paused
	_clear_pending()

func _open_report_folder() -> void:
	var folder := ProjectSettings.globalize_path(report_dir)
	if OS.shell_show_in_file_manager(folder, true) != OK:
		OS.shell_open(folder)

# A paused tree stops every pausable node from receiving input, so the game keeps drawing at full
# speed and answers no click, with nothing logged to explain it (owner report, Sept 17). Only this
# reporter's overlay and the layout Studio are meant to pause the title screen. If the title is up,
# the tree is paused and neither of those is on screen, the pause is a leak: take it back, and
# leave a warning the next report will carry.
func _process(_delta: float) -> void:
	if not is_inside_tree() or not get_tree().paused: return
	var scene: Node = get_tree().current_scene
	if scene == null or not str(scene.scene_file_path).ends_with("title_screen.tscn"): return
	if overlay != null and overlay.visible: return
	for node in get_tree().root.find_children("*", "CanvasLayer", true, false):
		if node.visible and node.layer >= 100 and node != overlay: return
	get_tree().paused = false
	stuck_pause_recoveries += 1
	push_warning("Title screen was left paused with nothing on top of it; unpaused it (recovery %d)." % stuck_pause_recoveries)

func _input(event: InputEvent) -> void:
	if not (event is InputEventKey):
		return
	var key := event as InputEventKey
	if not key.pressed or key.echo:
		return
	if key.keycode==KEY_F7 and is_instance_valid(performance_monitor):
		get_viewport().set_input_as_handled()
		performance_monitor.toggle_overlay()
		return
	if key.keycode == KEY_ESCAPE and overlay != null and overlay.visible:
		get_viewport().set_input_as_handled()
		_hide_overlay()
		return
	if key.keycode != KEY_F8:
		return
	get_viewport().set_input_as_handled()
	if overlay != null and overlay.visible:
		_hide_overlay()
		return
	var texture := get_viewport().get_texture()
	pending_screenshot = texture.get_image() if texture != null else null
	_capture_diagnostics()
	_show_overlay("REPORT A BUG", "Saves the game log, your last station save, a separate live diagnostic snapshot and a screenshot into a report you can send to Alex at Shadewater Labs (brinshadewater@gmail.com).", true, [["Save report", _on_save_pressed], ["Cancel", _hide_overlay]])
	if note_field != null:
		note_field.grab_focus()

func _on_save_pressed() -> void:
	var note := note_field.text if note_field != null else ""
	var path := save_report(note)
	if path.is_empty():
		_show_overlay("REPORT NOT SAVED", "The report could not be written. Check that the game can write to its user data folder.", false, [["Close", _hide_overlay]])
		return
	_show_overlay("REPORT SAVED", "Saved as %s in the bug_reports folder. Send it to Alex at Shadewater Labs (brinshadewater@gmail.com)." % path.get_file(), false, [["Open folder", _open_report_folder], ["Close", _hide_overlay]])

func _report_text(note: String, after_crash: bool, files: Array, dumps_found: int) -> String:
	var lines: Array = []
	lines.append("BrineSpace bug report")
	lines.append("build: " + JSON.stringify(_build_info()))
	lines.append("trigger: " + ("previous session did not close normally" if after_crash else "manual (F8)"))
	lines.append("note: " + (note if not note.is_empty() else "(none)"))
	if not pending_captured_at.is_empty():
		lines.append("captured at F8: %s (uptime %d s)" % [pending_captured_at, pending_uptime])
	if stuck_pause_recoveries > 0:
		lines.append("recovered from a leaked pause on the title screen: %d time(s)" % stuck_pause_recoveries)
	if not pending_input.is_empty():
		lines.append("")
		lines.append("input state when F8 was pressed:")
		for line in pending_input: lines.append("  " + str(line))
		lines.append("")
	lines.append("bundle time: " + Time.get_datetime_string_from_system(false, true))
	# Errors logged this session, counted by kind, so a silent flood of them is obvious here.
	if is_instance_valid(performance_monitor) and "errors" in performance_monitor:
		performance_monitor.errors.poll(float(Time.get_ticks_msec()))
		for line in performance_monitor.errors.report_lines(): lines.append(line)
		if int(performance_monitor.auto_reports) > 0: lines.append("automatic captures this session: %d" % performance_monitor.auto_reports)
	lines.append("previous session lock: " + (crashed_at.replace("\n", " | ") if not crashed_at.is_empty() else "(none)"))
	lines.append("game version: " + preload("res://scripts/build_version.gd").title())
	lines.append("godot: " + str(Engine.get_version_info().get("string", "unknown")))
	lines.append("template: " + ("debug" if OS.is_debug_build() else "release"))
	lines.append("os: %s %s" % [OS.get_name(), OS.get_version()])
	lines.append("cpu: " + OS.get_processor_name())
	var memory := OS.get_memory_info()
	lines.append("memory MB physical/free: %d / %d" % [int(memory.get("physical", 0) / 1048576.0), int(memory.get("free", 0) / 1048576.0)])
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
