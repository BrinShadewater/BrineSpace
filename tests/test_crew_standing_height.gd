extends SceneTree
## A pack declares how many source pixels span 65.28 world units. Packs that say
## nothing keep the legacy 74, so every existing sprite renders exactly as before.
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void: call_deferred("run")

func fixture(name: String, standing) -> String:
	var dir := "user://standing_height_fixture_" + name
	DirAccess.make_dir_recursive_absolute(dir + "/frames")
	var image := Image.create(92, 92, false, Image.FORMAT_RGBA8)
	image.fill(Color(0, 0, 0, 0)); image.set_pixel(30, 40, Color(1, 0, 0, 1))
	image.save_png(dir + "/frames/f.png")
	var manifest := {"frameWidth": 92, "frameHeight": 92, "pivot": [46, 86],
		"mirrorDirections": {"west": "east"},
		"states": [{"id": "walk-east", "frameFiles": ["frames/f.png"], "frameDurationsMs": [100], "loop": true}]}
	if standing != null: manifest["standingHeight"] = standing
	var file := FileAccess.open(dir + "/manifest.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest)); file.close()
	return dir + "/manifest.json"

func run() -> void:
	var legacy := Player.new(); legacy.load_manifest(fixture("legacy", null))
	check(legacy.frames["walk-east"][0].get_meta("crew_standing_height") == 74.0, "Undeclared packs keep the legacy 74")
	var dense := Player.new(); dense.load_manifest(fixture("dense", 148))
	check(dense.frames["walk-east"][0].get_meta("crew_standing_height") == 148.0, "Declared standing height is stamped on frames")
	check(dense.frames["walk-west"][0].get_meta("crew_standing_height") == 148.0, "Mirrored frames carry the standing height")
	# The scale a draw site derives: a 148px pack lands at exactly the legacy world size.
	var cell := 384.0
	var legacy_scale: float = cell * 0.17 / float(legacy.frames["walk-east"][0].get_meta("crew_standing_height", 74.0))
	var dense_scale: float = cell * 0.17 / float(dense.frames["walk-east"][0].get_meta("crew_standing_height", 74.0))
	check(is_equal_approx(74.0 * legacy_scale, 148.0 * dense_scale), "74px at legacy scale and 148px at dense scale span the same world height")
	check(is_equal_approx(74.0 * legacy_scale, 65.28), "Legacy figure still spans 65.28 world units")
	var bill: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/major-bill-v3/catalog.json"))
	check(float(bill.standingHeight) == 148.0, "Selected Bill uses twice the source density")
	if failures == 0: print("CREW STANDING HEIGHT PASS: legacy default, declared density, mirror carries it, world size preserved")
	else: print("CREW STANDING HEIGHT: %d failures" % failures)
	quit(1 if failures else 0)
