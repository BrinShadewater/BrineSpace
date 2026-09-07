extends SceneTree

const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0

func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	expect(not Preferences.raised_walls, "Fresh sessions use low walls")
	Preferences.save_path = "user://low_wall_regression_%d.cfg" % OS.get_process_id()
	var legacy := ConfigFile.new()
	legacy.set_value("display", "raised_walls", true)
	expect(legacy.save(Preferences.save_path) == OK, "Isolated legacy settings saved")
	Preferences.initialize(root)
	expect(not Preferences.raised_walls, "Legacy study preference cannot restore raised walls")
	var panel = preload("res://scripts/settings_panel.gd").new()
	root.add_child(panel)
	expect(panel.find_child("RaisedWalls", true, false) == null, "Retired study toggle is absent")
	Preferences.raised_walls = true
	panel._defaults("ACCESSIBILITY")
	expect(not Preferences.raised_walls, "Accessibility reset retains low walls")
	await process_frame
	var saved := ConfigFile.new()
	expect(saved.load(Preferences.save_path) == OK, "Reset settings load")
	expect(saved.get_value("display", "raised_walls", true) == false, "Reset persists low walls")
	panel.queue_free()
	await process_frame
	print("LOW WALL SETTINGS: %d failures" % failures)
	quit(1 if failures else 0)
