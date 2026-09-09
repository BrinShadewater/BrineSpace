extends SceneTree
const View = preload("res://rooms/whole-room/nursery_whole_view.gd")
func _init() -> void:
	var paths := [View.SOURCE,"res://rooms/whole-room/life-support-candidate.png"]
	for path in paths:
		var first := View.load_source_texture(path)
		for i in range(50):
			assert(View.load_source_texture(path) == first, "Repeated views share immutable source textures")
		var source := Image.new()
		assert(source.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) == OK)
		assert(first.get_size() == Vector2(source.get_size()), "Shared source keeps native dimensions")
		if DisplayServer.get_name() != "headless":
			var pixels := first.get_image()
			source.convert(pixels.get_format())
			assert(pixels.get_data() == source.get_data(), "Shared GPU texture preserves every source pixel")
		# Invalidate the timestamp without modifying source art or deleting cache files.
		View.shared_source_textures[path].modified = -1
		var refreshed := View.load_source_texture(path)
		assert(refreshed != first, "Changed source stamp reloads artwork")
		assert(refreshed.get_size() == first.get_size(), "Reload keeps source dimensions")
	assert(View.shared_source_textures.size() == 2, "Reload replaces cache entries instead of accumulating versions")
	print("SHARED ROOM SOURCES PASS: reuse, native size, refresh, bounded cache")
	quit()
