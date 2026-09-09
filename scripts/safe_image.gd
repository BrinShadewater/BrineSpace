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

static func placeholder() -> Image:
	var result := Image.create(64,64,false,Image.FORMAT_RGBA8)
	result.fill(Color(0.24,0.10,0.22,1))
	for y in range(0,64,16):
		for x in range(0,64,16):
			if (x+y)%32 == 0: result.fill_rect(Rect2i(x,y,16,16),Color(0.68,0.32,0.58,1))
	return result
