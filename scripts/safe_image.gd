extends RefCounted
## Raw PNGs remain independent of editor imports. Failure always leaves a drawable image.
static var failures: Dictionary = {}

static func load_png(image: Image, path: String) -> Error:
	var file := FileAccess.open(path, FileAccess.READ)
	var error := FileAccess.get_open_error() if file == null else OK
	if file != null:
		var bytes := file.get_buffer(file.get_length())
		if bytes.size() < 33 or bytes.slice(0,8) != PackedByteArray([137,80,78,71,13,10,26,10]):
			error = ERR_FILE_CORRUPT
		else:
			error = image.load_png_from_buffer(bytes)
	if error == OK and not image.is_empty():
		return OK
	if error == OK: error = ERR_FILE_CORRUPT
	if not failures.has(path):
		failures[path] = {"error": error, "message": error_string(error)}
		push_warning("Artwork unavailable: %s (%s). Diagnostic placeholder substituted; include an F8 report." % [path,error_string(error)])
	image.copy_from(placeholder())
	return error

static func raw_texture(path: String) -> Texture2D:
	# Raw bytes first: most rasters use importer="keep"/"skip"
	# (tools/set_raw_png_import_keep.py) and cannot load through ResourceLoader.
	# The loader is only the fallback for normal-imported textures whose raw
	# source is absent. Returns null on failure so callers can choose a fallback.
	var image := raw_image(path)
	if image != null:
		return ImageTexture.create_from_image(image)
	if ResourceLoader.exists(path):
		var resource = ResourceLoader.load(path)
		if resource is Texture2D:
			return resource
	return null

static func raw_image(path: String) -> Image:
	if not FileAccess.file_exists(path):
		return null
	var bytes := FileAccess.get_file_as_bytes(path)
	var image := Image.new()
	var error := ERR_FILE_UNRECOGNIZED
	match path.get_extension().to_lower():
		"png": error = image.load_png_from_buffer(bytes)
		"jpg", "jpeg": error = image.load_jpg_from_buffer(bytes)
		"webp": error = image.load_webp_from_buffer(bytes)
	return image if error == OK and not image.is_empty() else null

static func placeholder() -> Image:
	var result := Image.create(64,64,false,Image.FORMAT_RGBA8)
	result.fill(Color(0.24,0.10,0.22,1))
	for y in range(0,64,16):
		for x in range(0,64,16):
			if (x+y)%32 == 0: result.fill_rect(Rect2i(x,y,16,16),Color(0.68,0.32,0.58,1))
	return result
