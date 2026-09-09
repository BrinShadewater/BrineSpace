extends RefCounted
## Decorative floor layer. Placement does not add physics or gameplay effects.
static var manifest: Dictionary={}
static var textures: Dictionary={}
static func catalog() -> Dictionary:
	if manifest.is_empty(): manifest=JSON.parse_string(FileAccess.get_file_as_string("res://assets/floor-dressing-v1/manifest.json"))
	return manifest.sprites
static func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+catalog()[id].path)) != OK: push_error("Failed to load image (assets/floor-dressing-v1/floor_dressing.gd:11)")
		textures[id]=ImageTexture.create_from_image(image)
	return textures[id]
static func size(id: String,scale:=1.0) -> Vector2:
	var spec: Dictionary=catalog()[id]
	return Vector2(spec.size[0],spec.size[1])*float(spec.units_per_pixel)*scale
static func draw(canvas: CanvasItem,id: String,center: Vector2,scale:=1.0) -> void:
	var dimensions:=size(id,scale)
	canvas.draw_texture_rect(texture(id),Rect2(center-dimensions*0.5,dimensions),false)
