extends RefCounted
## Static decoration library. No collision, resource production or power logic.
static var manifest: Dictionary={}
static var textures: Dictionary={}

static func catalog() -> Dictionary:
	if manifest.is_empty():
		manifest=JSON.parse_string(FileAccess.get_file_as_string("res://assets/utility-kit-style-v2/manifest.json"))
	return manifest.sprites

static func texture(id: String) -> Texture2D:
	if not textures.has(id):
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://"+catalog()[id].path)
		textures[id]=ImageTexture.create_from_image(image)
	return textures[id]

static func rect(id: String,center: Vector2,scale:=1.0) -> Rect2:
	var spec: Dictionary=catalog()[id]
	var size:=Vector2(spec.size[0],spec.size[1])*float(spec.units_per_pixel)*scale
	return Rect2(center-size*0.5,size)

static func draw(canvas: CanvasItem,id: String,center: Vector2,scale:=1.0) -> void:
	canvas.draw_texture_rect(texture(id),rect(id,center,scale),false)

static func port(id: String,name: String,center: Vector2,scale:=1.0) -> Vector2:
	var spec: Dictionary=catalog()[id]
	var point: Array=spec.ports[name]
	return center+(Vector2(point[0],point[1])-Vector2(spec.pivot[0],spec.pivot[1]))*float(spec.units_per_pixel)*scale

static func center_for_port(id: String,name: String,target: Vector2,scale:=1.0) -> Vector2:
	return target-port(id,name,Vector2.ZERO,scale)
