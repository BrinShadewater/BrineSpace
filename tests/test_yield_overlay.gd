extends SceneTree
## The resource overlay (owner playtest, Sept 30): a hotkey shows what each room gives and takes over the rooms.
const Overlay = preload("res://scripts/yield_overlay.gd")
const Preferences = preload("res://scripts/title_settings.gd")
const Database = preload("res://scripts/room_database.gd")
var failures := 0

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func _init() -> void: call_deferred("run")

func run() -> void:
	# What a room shows: gains first, then costs, nothing for structure.
	var reactor: Array = Overlay.lines_for({"id": "x", "production": {"power": 3}, "consumption": {"water": 1}})
	check(reactor.size() == 2 and reactor[0] == ["power", 3, true] and reactor[1] == ["water", 1, false], "Gains come before costs")
	check(Overlay.lines_for(Database.get_room("corridor")).is_empty(), "A corridor shows nothing")
	check(Overlay.lines_for({"id": "heat_recovery", "production": {}}) == [["power", 4, true]], "Heat recovery shows its usual power")
	check(not Overlay.lines_for(Database.get_room("reactor")).is_empty(), "A working room shows something")
	# The hotkey is bound, rebindable, and does not collide with another action.
	check(Preferences.DEFAULT_KEYS.has("Resource overlay"), "The overlay has a hotkey")
	var used := {}
	for action in Preferences.DEFAULT_KEYS:
		check(not used.has(Preferences.DEFAULT_KEYS[action]), "Default keys are unique: " + str(action))
		used[Preferences.DEFAULT_KEYS[action]] = true
	# Settings offers it as a switch, and the Accessibility reset turns it off. The switch saves settings,
	# so point them at a scratch file first.
	var saved_settings: String = Preferences.save_path
	Preferences.save_path = "user://test_yield_overlay_panel_%d.cfg" % OS.get_process_id()
	var saved_flag: bool = Preferences.resource_overlay
	var panel = preload("res://scripts/settings_panel.gd").new()
	root.add_child(panel)
	var toggle = panel.find_child("ResourceOverlay", true, false)
	check(toggle is CheckButton, "Settings has a Resource overlay switch")
	if toggle is CheckButton:
		toggle.button_pressed = true
		check(Preferences.resource_overlay, "The switch turns the overlay on")
	panel._defaults("ACCESSIBILITY")
	check(not Preferences.resource_overlay, "Accessibility reset turns the overlay off")
	panel.queue_free()
	Preferences.resource_overlay = saved_flag
	if FileAccess.file_exists(Preferences.save_path): DirAccess.remove_absolute(Preferences.save_path)
	Preferences.save_path = saved_settings
	# The choice is remembered.
	var saved_path: String = Preferences.save_path
	Preferences.save_path = "user://test_yield_overlay.cfg"
	Preferences.resource_overlay = true
	var config := ConfigFile.new()
	config.set_value("display", "resource_overlay", Preferences.resource_overlay)
	check(bool(config.get_value("display", "resource_overlay", false)), "The setting round-trips through the config")
	Preferences.resource_overlay = false
	Preferences.save_path = saved_path
	print("yield overlay: %d failure(s)" % failures)
	quit(1 if failures > 0 else 0)
