extends SceneTree
## A key binding added in an update must not wipe the player's saved bindings when its default key is
## already one of theirs (Sept 30: the resource overlay's Y).
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func _init() -> void: call_deferred("run")

func run() -> void:
	var saved_path: String = Preferences.save_path
	Preferences.save_path = "user://test_key_migration_%d.cfg" % OS.get_process_id()
	var config := ConfigFile.new()
	var old_keys: Dictionary = Preferences.DEFAULT_KEYS.duplicate()
	old_keys.erase("Resource overlay")
	old_keys["Pan left"] = KEY_Y
	config.set_value("controls", "keys", old_keys)
	config.save(Preferences.save_path)
	Preferences.initialized = false
	Preferences.initialize(root)
	check(int(Preferences.keys["Pan left"]) == KEY_Y, "The player's own binding survives: Pan left is still Y")
	check(int(Preferences.keys["Resource overlay"]) != KEY_Y, "The new action moves off the taken key")
	var used := {}
	for action in Preferences.keys:
		check(not used.has(Preferences.keys[action]), "Bindings stay unique: " + str(action))
		used[Preferences.keys[action]] = true
	DirAccess.remove_absolute(Preferences.save_path)
	Preferences.save_path = saved_path
	Preferences.keys = Preferences.DEFAULT_KEYS.duplicate()
	print("KEY MIGRATION: %s failures=%d" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(1 if failures > 0 else 0)
