extends RefCounted
## Generated surface samples on authoritative hull polygons; no whole-bitmap rotation.
static var current_floor: ImageTexture
const G = preload("res://tools/modular_room_geometry.gd")
static func load_sources() -> Array:
	var textures: Array = []
	for path in ["res://rooms/underwater/straight-source-v1.png","res://rooms/underwater/corner-source-v1.png"]:
		var image := Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK)
		textures.append(ImageTexture.create_from_image(image))
	return textures
static func patch(canvas: CanvasItem, points: PackedVector2Array, uv: PackedVector2Array, texture: Texture2D, center: Vector2, q: int, light: float) -> void:
	var vertices := PackedVector2Array()
	for p in points: vertices.append(G.turn(p+center,q))
	canvas.draw_polygon(vertices,PackedColorArray([Color(light,light,light)]),uv,texture)
static func detail_parts(_corner: bool) -> Array:
	return []

static func draw_details(_canvas: CanvasItem, _center: Vector2, _q: int, _light: float, _corner: bool) -> void:
	pass

static func draw_hull(canvas: CanvasItem, hull: PackedVector2Array, floor_poly: PackedVector2Array, center: Vector2, q: int, textures: Array, corner: bool, powered: bool, power_level := -1.0, tee := false, variant := 0, floor_edits: Dictionary={}) -> void:
	var level := clampf(power_level,0,1) if power_level>=0 else (1.0 if powered else 0.0)
	var light := lerpf(0.35,1.0,level)
	var vertices := PackedVector2Array()
	for p in hull: vertices.append(G.turn(p+center,q))
	canvas.draw_colored_polygon(vertices,Color("617471")*Color(light,light,light))
	# Map individual low-relief wall plates along the hull perimeter. Entrance
	# end segments are intentionally omitted: shared doors/infill own the seam.
	for index in range(hull.size()):
		var a := hull[index]
		var b := hull[(index+1)%hull.size()]
		if (absf(a.x)==192 and a.x==b.x) or (absf(a.y)==192 and a.y==b.y): continue
		var tangent := (b-a).normalized()
		var normal := Vector2(-tangent.y,tangent.x)*16
		var count := ceili(a.distance_to(b)/48)
		for tile in range(count):
			var start := a+tangent*tile*48
			var end := a+tangent*minf((tile+1)*48,a.distance_to(b))
			var wall_art=preload("res://rooms/underwater/corridor_wall_art.gd")
			var points:=PackedVector2Array()
			for point in [start,end,end+normal,start+normal]:points.append(G.turn(point+center,q))
			wall_art.polygon(canvas,wall_art.key(corner or tee,variant),points,"low",light)
	# Current department deck uses the authoritative footprint and existing transform.
	if current_floor==null:
		var image:=Image.new()
		assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/floors-and-details-v5/corridor-deck.png"))==OK)
		current_floor=ImageTexture.create_from_image(image)
	var floor_texture:=current_floor
	var floor_uv:=PackedVector2Array()
	for p in floor_poly: floor_uv.append((p+Vector2.ONE*192)/384)
	if preload("res://rooms/whole-room/modular_floor.gd").enabled:
		preload("res://rooms/whole-room/modular_floor.gd").draw(canvas,floor_edits,true,q,1.0,G.turn(center,q),light,"", "tee_corridor" if tee else "corner" if corner else "corridor",variant)
	else:
		patch(canvas,floor_poly,floor_uv,floor_texture,center,q,light)


static func draw_variant(_canvas: CanvasItem, _floor_poly: PackedVector2Array, _center: Vector2, _q: int, _light: float, _variant: int) -> void:
	# Legacy variant IDs remain save-compatible; the authored deck supplies its art.
	pass
