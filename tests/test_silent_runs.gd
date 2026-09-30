extends SceneTree
## Test, probe and fixture runs must not be heard (owner playtest, Sept 29: native runs on screen 2 played the
## game's music over the owner's own game, so it seemed to cut in and out). They mute the master bus, keep
## every sound counted, and the F8 report says what the music is doing.
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	expect(TitleSettings.silent_run(), "A --script run counts as a silent run")
	TitleSettings.save_path = "user://silent_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://silent_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://silent_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	for i in 30: await process_frame
	expect(AudioServer.is_bus_mute(0), "The master bus is muted in a test run")
	var music = root.get_meta("station_music").get_ref() if root.has_meta("station_music") else null
	expect(music != null, "The music still starts (its logic is unchanged)")
	if music != null:
		var line: String = music.status_line()
		expect(line.contains("MUTED") and line.contains("track"), "The music status line reports the mute and the track: " + line)
	# A sound still plays and is counted while muted.
	game.play_station_sound("placement")
	expect(game.station_sound.voices.has("placement"), "Sound effects still run, silently")
	# The F8 report carries the music line.
	var report = load("res://scripts/bug_report.gd").new()
	root.add_child(report)
	var lines: Array = report._input_state()
	var found := false
	for entry in lines:
		if str(entry).begins_with("music: "): found = true
	expect(found, "The bug report includes a music line")
	print("SILENT RUNS: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
