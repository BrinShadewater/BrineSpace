extends SceneTree

# Read-only art review: no main scene, save system, or live texture mappings.
# Run without --headless. Output is a viewport capture, not modified room art.
const INDEX := "res://output/room-art-pilot/pack-index.json"
var destination := ""

func _init() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture="):
			destination = argument.trim_prefix("--capture=")
	call_deferred("_run")

func _run() -> void:
	if destination.is_empty() or FileAccess.file_exists(destination):
		push_error("Pass --capture=<new absolute PNG path>; existing captures are preserved.")
		quit(1)
		return
	var data = JSON.parse_string(FileAccess.get_file_as_string(INDEX))
	if not data is Dictionary or not data.get("rooms") is Array:
		push_error("Missing or invalid room pack index")
		quit(1)
		return
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600, 1280)
	var background := ColorRect.new()
	background.color = Color("#10171d")
	background.size = Vector2(1600, 1280)
	root.add_child(background)
	var heading := Label.new()
	heading.text = "BRINESPACE / CANDIDATE PACK — art comparison only; geometry and runtime acceptance pending"
	heading.position = Vector2(24, 10)
	heading.add_theme_font_size_override("font_size", 18)
	root.add_child(heading)
	var seen := {}
	var index := 0
	for record in data.rooms:
		var id := str(record.id)
		if seen.has(id):
			push_error("Duplicate room identity: " + id)
			quit(1)
			return
		seen[id] = true
		var source := Image.new()
		var error := source.load("res://" + str(record.path))
		if error != OK:
			push_error("Cannot decode candidate: " + str(record.path))
			quit(1)
			return
		var tile := Vector2(24 + (index % 7) * 223, 48 + (index / 7) * 242)
		var art := TextureRect.new()
		art.position = tile
		art.size = Vector2(208, 208)
		art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		art.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		art.texture = ImageTexture.create_from_image(source)
		root.add_child(art)
		var caption := Label.new()
		caption.text = id
		caption.position = tile + Vector2(0, 212)
		caption.add_theme_font_size_override("font_size", 15)
		root.add_child(caption)
		index += 1
	if index != int(data.counts.expected):
		push_error("Candidate count differs from declared scope")
		quit(1)
		return
	await process_frame
	await RenderingServer.frame_post_draw
	var error := root.get_texture().get_image().save_png(destination)
	if error != OK:
		push_error("Could not save contact sheet: " + error_string(error))
		quit(1)
		return
	print("Captured %d unique room candidates: %s" % [index, destination])
	quit(0)
