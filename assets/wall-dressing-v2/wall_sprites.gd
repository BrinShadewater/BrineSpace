extends RefCounted
## Wall-space decoration; draw after the hull face, before foreground occluders.
static var manifest: Dictionary={}
static var textures: Dictionary={}
static func data() -> Dictionary:
	if manifest.is_empty(): manifest=JSON.parse_string(FileAccess.get_file_as_string("res://assets/wall-dressing-v2/manifest.json"))
	return manifest
static func catalog() -> Dictionary: return data().sprites
static func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+catalog()[id].path))==OK)
		textures[id]=ImageTexture.create_from_image(image)
	return textures[id]
static func size(id: String,scale:=1.0) -> Vector2:
	var spec: Dictionary=catalog()[id]
	return Vector2(spec.size[0],spec.size[1])*float(spec.units_per_pixel)*scale
static func draw(canvas: CanvasItem,id: String,center: Vector2,scale:=1.0) -> void:
	var dimensions:=size(id,scale)
	canvas.draw_texture_rect(texture(id),Rect2(center-dimensions*0.5,dimensions),false)
static func draw_layout(canvas: CanvasItem,name: String) -> void:
	for item in data().layouts[name]: draw(canvas,item[0],Vector2(item[1],item[2]))
