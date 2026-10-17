extends SceneTree
## Standing/first-gait drawings must agree at the repaired controller boundaries.
const Player = preload("res://scripts/crew_sprite_player.gd")
var checks := 0
var failures := 0

func registered(texture: Texture2D) -> PackedByteArray:
	var canvas = Image.create(640, 640, false, Image.FORMAT_RGBA8)
	var source = texture.get_image()
	canvas.blend_rect(source, Rect2i(Vector2i.ZERO, source.get_size()), Vector2i(Vector2(320, 320) - texture.get_meta("crew_pivot")))
	return canvas.get_data()

func _init(): call_deferred("run")
func run():
	var player = Player.new()
	var path = "res://character/marsh-v2/catalog.json"
	var catalog = JSON.parse_string(FileAccess.get_file_as_string(path))
	for relative in catalog.body: player.load_manifest(path.get_base_dir().path_join(str(relative)), true)
	for direction in ["east", "west"]:
		for boundary in [["walk-start-", 0], ["walk-stop-", -1], ["walk-step-", 0], ["walk-step-", -1]]:
			var key: String = boundary[0] + direction
			checks += 1
			if registered(player.frames[key][boundary[1]]) != registered(player.frames["idle-" + direction][0]):
				failures += 1
				push_error("Standing endpoint differs: " + key + " / " + str(boundary[1]))
	checks += 1
	# The north controller resumes at .23 seconds: inside gait slot 1 (.15-.30).
	if registered(player.frames["walk-start-north"][-1]) != registered(player.frames["walk-north"][1]):
		failures += 1
		push_error("North start does not share its selected gait-slot-1 handoff")
	print("MARSH LOCOMOTION JOINS: ", checks, " checks, failures=", failures)
	quit(0 if failures == 0 else 1)
