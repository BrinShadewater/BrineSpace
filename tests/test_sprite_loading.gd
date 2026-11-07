extends SceneTree
const Player = preload("res://scripts/crew_sprite_player.gd")
const SafeImage = preload("res://scripts/safe_image.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var folder := "user://sprite-loading-%d" % OS.get_process_id()
	DirAccess.make_dir_recursive_absolute(folder)
	var original := Image.create(4, 4, false, Image.FORMAT_RGBA8)
	original.fill(Color.GREEN)
	original.save_png(folder + "/good.png")
	var file := FileAccess.open(folder + "/bad.png", FileAccess.WRITE)
	file.store_string("invalid PNG"); file.close()
	var manifest := {"states": [{"id": "idle-south", "frameFiles": ["missing.png", "bad.png", "good.png"], "frameDurationsMs": [100, 200, 300], "facings": ["north", "west", "south"], "depthOffsets": [1, 2, 3], "loop": true}]}
	file = FileAccess.open(folder + "/manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest)); file.close()
	var player = Player.new()
	player.load_manifest(folder + "/manifest.json")
	check(player.frames["idle-south"].size() == 3, "Missing/corrupt frames retain their timeline slots")
	check(SafeImage.failures.has(folder + "/missing.png") and SafeImage.failures.has(folder + "/bad.png"), "Both failures reach F8 diagnostics")
	var last: Texture2D = player.frame_at_elapsed("idle-south", 0.35)
	check(last.get_image().get_data() == original.get_data(), "Later valid frame retains pixels and original start time")
	check(last.get_meta("crew_water_facing") == "south" and last.get_meta("crew_depth_offset") == 3.0, "Later frame retains its own metadata")
	check(player.frame_at_elapsed("idle-south", 0.15) != null, "Corrupt slot stays drawable")
	check(is_equal_approx(player.cycle_seconds("idle-south"), 0.6), "Cached authored duration preserves timing")
	player.timing["generated"] = {"durations": [100, 350], "loop": false}
	check(is_equal_approx(player.cycle_seconds("generated"), 0.45), "Generated clips retain duration fallback")
	# Reload must replace durations instead of retaining a stale total.
	manifest.states[0].frameDurationsMs = [300, 300, 300]
	file = FileAccess.open(folder + "/manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest)); file.close()
	player.load_manifest(folder + "/manifest.json")
	check(is_equal_approx(player.cycle_seconds("idle-south"), 0.9), "Reload refreshes authored duration")
	for name in ["good.png", "bad.png", "manifest.json"]: DirAccess.remove_absolute(folder + "/" + name)
	DirAccess.remove_absolute(folder)
	print("SPRITE LOADING: %d failures" % failures)
	quit(1 if failures else 0)
