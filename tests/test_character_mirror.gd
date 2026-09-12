extends SceneTree
## One authored profile, mirrored onto the opposite side at load.
## Fixture art is written to an isolated user:// directory, never into a pack.
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void: call_deferred("run")

func fixture(mirror: bool) -> String:
	var dir := "user://character_mirror_fixture"
	DirAccess.make_dir_recursive_absolute(dir)
	DirAccess.make_dir_recursive_absolute(dir + "/frames")
	# An asymmetric frame: a mirror must actually move the marked pixel.
	var image := Image.create(92, 92, false, Image.FORMAT_RGBA8)
	image.fill(Color(0, 0, 0, 0))
	image.set_pixel(20, 40, Color(1, 0, 0, 1))
	image.set_pixel(21, 40, Color(1, 0, 0, 1))
	image.save_png(dir + "/frames/east_000.png")
	var manifest := {
		"frameWidth": 92, "frameHeight": 92, "pivot": [46, 86],
		"states": [{"id": "walk-east", "frameFiles": ["frames/east_000.png"],
			"frameDurationsMs": [120], "loop": true}],
	}
	if mirror: manifest["mirrorDirections"] = {"west": "east"}
	var path := dir + "/manifest.json"
	var file := FileAccess.open(path, FileAccess.WRITE)
	file.store_string(JSON.stringify(manifest))
	file.close()
	return path

func run() -> void:
	var plain := Player.new()
	plain.load_manifest(fixture(false))
	check(plain.frames.has("walk-east"), "Authored state loads")
	check(not plain.frames.has("walk-west"), "Without the opt-in, no mirror is invented")

	var player := Player.new()
	player.load_manifest(fixture(true))
	check(player.frames.has("walk-west"), "Declared direction is mirrored at load")
	check(player.timing["walk-west"] == player.timing["walk-east"], "Mirror keeps the source timing")

	var source: Texture2D = player.frames["walk-east"][0]
	var mirrored: Texture2D = player.frames["walk-west"][0]
	var a := source.get_image()
	var b := mirrored.get_image()
	check(a.get_size() == b.get_size(), "Mirror keeps the frame size")
	check(b.get_pixel(92 - 1 - 20, 40).a > 0.5, "Marked pixel lands on the opposite side")
	check(a.get_pixel(20, 40).a > 0.5, "Source frame is left untouched")
	var seat: Vector2 = mirrored.get_meta("crew_pivot")
	check(seat == Vector2(92 - 1 - 46, 86), "Pivot reflects with the art: got " + str(seat))
	check(str(mirrored.get_meta("crew_mirrored_from", "")) == "walk-east", "Mirrored frames record their source")

	# An authored opposite profile must win over the mirror.
	var authored := Player.new()
	authored.load_manifest(fixture(true))
	authored.frames["walk-west"] = ["sentinel"]
	authored.load_manifest(fixture(true), true)
	check(authored.frames["walk-west"] == ["sentinel"], "Authored art is never replaced by a mirror")

	# Vertical flips are refused: north and south are separately authored.
	var vertical := Player.new()
	vertical.load_manifest(fixture(true))
	vertical.mirror_declared_directions({"mirrorDirections": {"north": "south"}, "pivot": [46, 86]})
	check(not vertical.frames.has("walk-north"), "Only east and west may mirror")

	if failures == 0: print("CHARACTER MIRROR PASS: opt-in, pivot reflected, authored art wins, vertical refused")
	else: print("CHARACTER MIRROR: %d failures" % failures)
	quit(1 if failures else 0)
