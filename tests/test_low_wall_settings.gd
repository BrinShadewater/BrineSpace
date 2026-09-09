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
	expect(Preferences.raised_walls, "Fresh sessions use raised walls")
	Preferences.save_path = "user://low_wall_regression_%d.cfg" % OS.get_process_id()
	var legacy := ConfigFile.new()
	legacy.set_value("display", "raised_walls", false)
	expect(legacy.save(Preferences.save_path) == OK, "Isolated legacy settings saved")
	Preferences.initialize(root)
	expect(Preferences.raised_walls, "Legacy forced-low preference migrates to raised walls")
	var panel = preload("res://scripts/settings_panel.gd").new()
	root.add_child(panel)
	expect(panel.find_child("RaisedWalls", true, false) != null, "Raised wall toggle is available")
	Preferences.raised_walls = false
	Preferences.save(root)
	Preferences.initialized=false
	Preferences.initialize(root)
	expect(not Preferences.raised_walls, "New explicit low-wall choice persists")
	panel._defaults("ACCESSIBILITY")
	expect(Preferences.raised_walls, "Accessibility reset restores raised walls")
	await process_frame
	var saved := ConfigFile.new()
	expect(saved.load(Preferences.save_path) == OK, "Reset settings load")
	expect(saved.get_value("display", "riser_walls_enabled", false) == true, "Reset persists raised walls")
	panel.queue_free()
	await process_frame
	DirAccess.remove_absolute(Preferences.save_path)
	print("RISER WALL SETTINGS: %d failures" % failures)
	quit(1 if failures else 0)
