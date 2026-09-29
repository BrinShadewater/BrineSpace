extends SceneTree
## Visual effects quality (spec 2026-09-29-lighting-atmosphere-design.md): Low switches the water
## atmosphere off, Medium is the default, High is stronger, the setting round-trips through the
## settings file, and out-of-range saved values fall back safely.
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	Preferences.save_path = "user://effects_quality_%d.cfg" % OS.get_process_id()
	expect(Preferences.effects_quality == 1, "Medium is the default")
	Preferences.effects_quality = 0
	var low: Dictionary = Preferences.atmosphere()
	expect(float(low.shafts) == 0.0 and float(low.caustics) == 0.0 and float(low.tint) == 0.0, "Low turns the water atmosphere off")
	Preferences.effects_quality = 1
	var medium: Dictionary = Preferences.atmosphere()
	expect(float(medium.shafts) > 0.0 and float(medium.caustics) > 0.0 and float(medium.tint) > 0.0, "Medium turns it on")
	Preferences.effects_quality = 2
	var high: Dictionary = Preferences.atmosphere()
	expect(float(high.shafts) >= float(medium.shafts) and float(high.snow) > float(medium.snow), "High is stronger than Medium")
	# round trip
	Preferences.effects_quality = 2
	var window := root
	Preferences.save(window)
	Preferences.effects_quality = 1
	var config := ConfigFile.new()
	expect(config.load(Preferences.save_path) == OK, "Settings file was written")
	expect(int(config.get_value("display", "effects_quality", -1)) == 2, "Quality is saved under display/effects_quality")
	# out-of-range saved values are clamped when loaded
	config.set_value("display", "effects_quality", 9)
	config.save(Preferences.save_path)
	Preferences.initialized = false
	Preferences.initialize(window)
	expect(Preferences.effects_quality == 2, "A saved value of 9 loads as High (clamped)")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Preferences.save_path))
	print("EFFECTS QUALITY: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
