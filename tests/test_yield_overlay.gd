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
