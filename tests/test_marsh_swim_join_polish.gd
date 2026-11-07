extends SceneTree
## Native source/hold review of the installed Marsh swim joins, not world routing.
const Player = preload("res://scripts/crew_sprite_player.gd")
const OUT = "res://output/marsh-swim-polish-2026-10-14/native"

func review_output() -> String: return OUT
func scratch_token() -> String: return "marsh-swim-polish-2026-10-14"
func manifest_paths() -> Array:
	return ["res://character/marsh-swim-joins-v1/manifest.json"]

class ReviewCanvas extends Node2D:
	var textures: Array = []
	var marker = Color.BLACK
	func _draw():
		draw_rect(Rect2(0, 0, 1320, 600), Color("26333c"))
		draw_rect(Rect2(0, 0, 8, 8), marker)
		for i in textures.size():
			var texture: Texture2D = textures[i]
			var pivot: Vector2 = texture.get_meta("crew_pivot")
			var column = i % 5
			var row = floori(i / 5.0)
			draw_string(ThemeDB.fallback_font, Vector2(15 + column * 260, 45 + row * 260), "hold " + str(i), HORIZONTAL_ALIGNMENT_LEFT, -1, 16)
			draw_texture(texture, Vector2(110 + column * 260, 200 + row * 260) - pivot)
			draw_set_transform(Vector2(110 + column * 260, 280 + row * 260), 0, Vector2(0.5, 0.5))
			draw_texture(texture, -pivot)
			draw_set_transform(Vector2.ZERO)

func _init(): call_deferred("run")

func run():
	if DisplayServer.get_name() == "headless":
		print("SKIP-NATIVE: source review needs rendered frames")
		quit(2)
		return
	if not OS.get_environment("APPDATA").contains(scratch_token()):
		push_error("Explicit scratch APPDATA required")
		quit(1)
		return
	root.size = Vector2i(1320, 600)
	root.content_scale_size = Vector2i(1320, 600)
	var player = Player.new()
	var catalog_path = "res://character/marsh-v2/catalog.json"
	var catalog = JSON.parse_string(FileAccess.get_file_as_string(catalog_path))
	for path in catalog.body: player.load_manifest(catalog_path.get_base_dir().path_join(str(path)), true)
	var states = {}
	for manifest_path in manifest_paths():
		var manifest = JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
		for state in manifest.states: states[state.id] = state
	var canvas = ReviewCanvas.new()
	root.add_child(canvas)
	DirAccess.make_dir_recursive_absolute(review_output())
	var checks = 0
	var failures = 0
	var capture_index = 0
	for state in states.values():
		var key: String = state.id
		var elapsed = 0.0
		canvas.textures = []
		for i in player.frames[key].size():
			var duration: float = player.timing[key].durations[i] / 1000.0
			var texture = player.frame_at_elapsed(key, elapsed + duration / 2)
			checks += 1
			if texture != player.frames[key][i]: failures += 1
			canvas.textures.append(texture)
			elapsed += duration
		if key.begins_with("swim-turn-"):
			canvas.textures.append(player.frames["swim-" + key.get_slice("-", 3)][0])
		capture_index += 1
		canvas.marker = Color8(capture_index * 15, 60, 120)
		canvas.queue_redraw()
		# Observe the actually rendered marker: a valid source array can still
		# accompany the preceding viewport image at the first post-draw signal.
		var captured: Image
		for attempt in 20:
			await process_frame
			await RenderingServer.frame_post_draw
			captured = root.get_texture().get_image()
			if captured.get_pixel(2, 2).is_equal_approx(canvas.marker): break
		checks += 1
		if not captured.get_pixel(2, 2).is_equal_approx(canvas.marker): failures += 1
		var error = captured.save_png(review_output() + "/" + key + ".png")
		checks += 1
		if error != OK: failures += 1
	canvas.queue_free()
	await process_frame
	print("MARSH SWIM JOIN REVIEW: ", checks, " checks, failures=", failures, "; ", states.size(), " native chronology boards at 1x and 0.5x")
	quit(0 if failures == 0 else 1)
