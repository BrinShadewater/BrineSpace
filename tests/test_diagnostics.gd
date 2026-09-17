extends SceneTree
## Diagnostics added Sept 17 (owner request): automatic capture of stalls, the error counter,
## the event timeline and the per-session stats line. Everything here uses its own paths.
const Monitor = preload("res://scripts/performance_monitor.gd")
const Watch = preload("res://scripts/error_watch.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

class Reporter extends Node:
	var notes: Array = []
	var performance_monitor
	func save_report(note: String, _after_crash: bool = false) -> String:
		notes.append(note)
		return "user://fixture-report-%d.zip" % notes.size()

class FakeScene extends Node:
	var cycle := 7
	var crew_count := 2
	var run_victory := false

func run() -> void:
	var prefix := "user://diagnostics_%d" % OS.get_process_id()

	# The error watch groups repeated errors and keeps the first backtrace of each.
	var log_path := prefix + ".log"
	var file := FileAccess.open(log_path, FileAccess.WRITE)
	file.store_string("normal line\nERROR: Parameter \"mesh\" is null.\n   at: mesh_get_aabb (drivers/x.cpp:1)\nERROR: Parameter \"mesh\" is null.\nSCRIPT ERROR: Cannot call method 'x' on a null value.\n   at: _unhandled_input (res://scripts/main.gd:1)\n")
	file.close()
	var watch := Watch.new()
	watch.path = log_path
	watch.poll(1000.0)
	check(watch.total == 3 and watch.groups.size() == 2, "Errors are counted and grouped: %d in %d" % [watch.total, watch.groups.size()])
	var mesh_key := "ERROR: Parameter \"mesh\" is null."
	check(watch.groups.has(mesh_key) and watch.groups[mesh_key].count == 2, "Repeated errors count once per occurrence")
	check(str(watch.groups[mesh_key].context[0]).contains("mesh_get_aabb"), "The first backtrace of each error is kept")
	var append := FileAccess.open(log_path, FileAccess.READ_WRITE)
	append.seek_end()
	append.store_string("ERROR: Parameter \"mesh\" is null.\n")
	append.close()
	watch.poll(2000.0)
	check(watch.total == 4 and watch.groups[mesh_key].count == 3, "Only new log lines are read")
	check(watch.report_lines()[0].contains("4 in 2 kinds"), "Reports summarise the error counts")
	var replaced := FileAccess.open(log_path, FileAccess.WRITE)
	replaced.store_string("ERROR: fresh session.\n")
	replaced.close()
	watch.poll(3000.0)
	check(watch.total == 5, "A rotated log is read from the start again")

	# A stall saves one report by itself, and the gap keeps a slow patch from filling the folder.
	var reporter := Reporter.new()
	root.add_child(reporter)
	var monitor = Monitor.new()
	reporter.performance_monitor = monitor
	reporter.add_child(monitor)
	monitor.auto_capture = true # Scripts (including this test) start with it off.
	monitor.breadcrumb_path = prefix + "-breadcrumbs.json" # Never the player's file.
	monitor.errors.path = log_path
	monitor.stats_path = prefix + ".csv"
	monitor._watch_for_stalls(500.0, false, false, 100000.0)
	check(reporter.notes.size() == 1 and str(reporter.notes[0]).contains("one frame took 500 ms"), "A long frame saves a report by itself")
	monitor._watch_for_stalls(500.0, false, false, 101000.0)
	check(reporter.notes.size() == 1, "A second stall within the gap does not add a report")
	monitor._watch_for_stalls(500.0, true, false, 400000.0)
	check(reporter.notes.size() == 1, "A paused station never triggers a capture")
	for step in range(45):
		monitor._watch_for_stalls(60.0, false, false, 400000.0 + step * 60.0)
	check(reporter.notes.size() == 2 and str(reporter.notes[1]).contains("under 20 FPS"), "A slow stretch saves a report too: %s" % str(reporter.notes))
	monitor.auto_reports = monitor.AUTO_LIMIT
	monitor._watch_for_stalls(900.0, false, false, 900000.0)
	check(reporter.notes.size() == 2, "The session limit stops further automatic reports")

	# The timeline records station events and stays bounded.
	for index in range(monitor.MAX_TIMELINE + 20):
		monitor.note("log", "event %d" % index)
	check(monitor.timeline.size() == monitor.MAX_TIMELINE and str(monitor.timeline.back().text) == "event %d" % (monitor.MAX_TIMELINE + 19), "The timeline keeps the most recent events")
	# Breadcrumbs: the recent timeline lands in a small file a crash cannot erase.
	monitor.write_breadcrumbs()
	var crumbs: Dictionary = JSON.parse_string(FileAccess.open(prefix + "-breadcrumbs.json", FileAccess.READ).get_as_text())
	check(crumbs.has("timeline") and crumbs.timeline.size() > 0 and crumbs.has("memory"), "Breadcrumbs carry the recent timeline and memory stats")
	check(int(crumbs.memory.nodes) > 0 and crumbs.memory.has("floor_meshes_retired"), "Breadcrumbs record node counts and retained mesh caches")
	monitor.errors.poll(5000.0) # The monitor keeps its own watcher; the log now holds one error.
	var snapshot: Dictionary = monitor.snapshot()
	check(snapshot.has("timeline") and snapshot.has("errors") and snapshot.has("automatic_reports"), "Reports include the timeline, errors and automatic captures")
	check(int(snapshot.errors.total) == 1, "The report carries the error count")

	# One line per finished loop, with a header the first time.
	var scene := FakeScene.new()
	root.add_child(scene)
	monitor.observe(20.0, false, false, 1000.0)
	monitor.finish_bucket({"rooms": 3}, 2000.0)
	monitor.record_session(monitor.session_row(scene))
	monitor.record_session(monitor.session_row(scene))
	var csv := FileAccess.open(prefix + ".csv", FileAccess.READ).get_as_text().strip_edges().split("\n")
	check(csv.size() == 3 and csv[0].begins_with("when,build,cycles"), "The stats file has one header and one line per loop")
	check(csv[1].split(",").size() == csv[0].split(",").size() and csv[1].contains(",7,"), "Each line records the loop's cycles")
	monitor.stats_path = ""
	monitor.record_session(monitor.session_row(scene))
	check(FileAccess.open(prefix + ".csv", FileAccess.READ).get_as_text().strip_edges().split("\n").size() == 3, "An empty stats path writes nothing")
	scene.queue_free()
	reporter.queue_free()
	await process_frame
	for suffix in [".log", ".csv", "-breadcrumbs.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(prefix + suffix))
	print("DIAGNOSTICS %s: error grouping, automatic stall capture, timeline, session stats" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
