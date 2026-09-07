extends RefCounted
## Call from the floor pass, before props and crew. This helper creates no blockers.
static var manifest: Dictionary={}
static var textures: Dictionary={}
static func catalog() -> Dictionary:
	if manifest.is_empty(): manifest=JSON.parse_string(FileAccess.get_file_as_string("res://assets/floor-utilities-v1/manifest.json"))
	return manifest.sprites
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
static func port(id: String,name: String,center: Vector2,scale:=1.0) -> Vector2:
	var spec: Dictionary=catalog()[id]
	var point: Array=spec.ports[name]
	return center+(Vector2(point[0],point[1])-Vector2(spec.pivot[0],spec.pivot[1]))*float(spec.units_per_pixel)*scale
static func center_for_port(id: String,name: String,target: Vector2,scale:=1.0) -> Vector2:
	return target-port(id,name,Vector2.ZERO,scale)
