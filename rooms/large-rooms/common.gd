extends RefCounted

const FLOOR_SIZE := 768.0
const HALF := FLOOR_SIZE * 0.5
const RiserCatalog = preload("res://rooms/whole-room/riser_catalog.gd")
const WallMaterial = preload("res://rooms/whole-room/department_wall_material.gd")
const ART_SATURATION := 0.58
static var art_textures: Dictionary = {}

static func sprite(canvas: CanvasItem, path: String, bounds: Rect2, tint: Color = Color.WHITE) -> void:
	if not art_textures.has(path):
		var image := Image.new()
		var error := image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
		if error != OK:
			push_error("Large room art could not load: %s (%d)" % [path, error])
			return
		# Grade only these new room sprites; neutral steel keeps its value and detail.
		image.adjust_bcs(1.0, 1.0, ART_SATURATION)
		if path.ends_with("_wall_bank.png"):
			var target := wall_bank_raster_size(image.get_size())
			image.resize(target.x, target.y, Image.INTERPOLATE_LANCZOS)
		art_textures[path] = ImageTexture.create_from_image(image)
	var texture: Texture2D = art_textures[path]
	var natural: Vector2 = texture.get_size()
	var scale: float = minf(bounds.size.x / natural.x, bounds.size.y / natural.y)
	var size: Vector2 = natural * scale
	canvas.draw_texture_rect(texture, Rect2(bounds.get_center() - size * 0.5, size), false, tint)

static func wall_bank_raster_size(native: Vector2i) -> Vector2i:
	var factor: float = minf(1020.0 / float(native.x), 310.0 / float(native.y))
	return Vector2i(maxi(1, roundi(float(native.x) * factor)), maxi(1, roundi(float(native.y) * factor)))

static func begin(canvas: CanvasItem, room: Dictionary, rect: Rect2, floor_color: Color, accent: Color, wall_style: Dictionary) -> void:
	var rotation: int = posmod(int(room.get("rotation", 0)), 4)
	var scale := Vector2.ONE * (rect.size.x / FLOOR_SIZE)
	canvas.draw_set_transform(rect.get_center(), 0.0, scale)
	canvas.draw_rect(Rect2(-HALF, -HALF, FLOOR_SIZE, FLOOR_SIZE), Color("#081119"))
	canvas.draw_rect(Rect2(-370, -370, 740, 740), floor_color)
	for line in range(-320, 321, 64):
		canvas.draw_line(Vector2(-360, line), Vector2(360, line), Color(1, 1, 1, 0.035), 2)
		canvas.draw_line(Vector2(line, -360), Vector2(line, 360), Color(1, 1, 1, 0.035), 2)
	for p in [Vector2(-334,-334),Vector2(334,-334),Vector2(-334,334),Vector2(334,334)]:
		canvas.draw_circle(p, 7, accent.darkened(0.6))
		canvas.draw_circle(p, 3, accent)
	var raised: bool = bool(room.get("raised_walls", true))
	_draw_perimeter(canvas, room, wall_style, raised, rotation)
	for port in room.get("ports", []):
		var facing := rotated_side(str(port.get("side", "")), rotation)
		var center: Vector2 = port_center(port).rotated(float(rotation) * PI * 0.5)
		_draw_station_port(canvas, center, facing, accent, floor_color, raised and facing == "north")
	if room.has("ocean_side"):
		_draw_ocean_face(canvas, rotated_side(str(room.ocean_side), rotation), accent, bool(room.get("moonbay_mission",{}).get("ocean_open",false)), raised)
	canvas.draw_set_transform(rect.get_center(), float(rotation) * PI * 0.5, scale)

static func rotated_side(side: String, rotation: int) -> String:
	var names := ["north", "east", "south", "west"]
	var index := names.find(side)
	return names[posmod(index + rotation, 4)] if index >= 0 else ""

static func port_center(port: Dictionary) -> Vector2:
	var cell: Vector2i = port.get("cell", Vector2i.ZERO)
	var center := Vector2(-192 + cell.x * 384, -192 + cell.y * 384)
	match str(port.get("side", "")):
		"north": center.y = -370
		"south": center.y = 370
		"west": center.x = -370
		"east": center.x = 370
	return center

static func _draw_perimeter(canvas: CanvasItem, room: Dictionary, wall_style: Dictionary, raised: bool, rotation: int) -> void:
	for side in ["north", "east", "south", "west"]:
		if side == "north" and raised: continue
		var horizontal: bool = side in ["north", "south"]
		var wall := Rect2(-384, -380 if side == "north" else 356, 768, 28) if horizontal else Rect2(-380 if side == "west" else 356, -384, 28, 768)
		WallMaterial.wall(canvas, wall, horizontal, "engineering")
	if raised: _draw_north_riser(canvas, room, wall_style, rotation)

static func _draw_north_riser(canvas: CanvasItem, room: Dictionary, wall_style: Dictionary, rotation: int) -> void:
	var material: String = str(wall_style.get("material",""))
	var art: String = str(wall_style.get("art",""))
	var shade: float = float(wall_style.get("shade",0.25))
	canvas.draw_rect(Rect2(-384,-388,768,76),Color("#0b151b"))
	for half in range(2):
		var left: float = -384.0+float(half)*384.0
		RiserCatalog.face(canvas,material,Rect2(left,-380,384,60))
		RiserCatalog.cap(canvas,material,Rect2(left,-388,384,8))
		RiserCatalog.skirt(canvas,material,Rect2(left,-320,384,8))
	canvas.draw_rect(Rect2(-384,-388,768,76),Color(0.04,0.08,0.09,shade))
	if art != "":
		var axis: float = north_art_axis(room, wall_style, rotation)
		sprite(canvas,art,Rect2(axis-102,-381,204,62))

static func north_art_axis(room: Dictionary, wall_style: Dictionary, rotation: int) -> float:
	var occupied: Array[float] = []
	for port in room.get("ports", []):
		if rotated_side(str(port.get("side", "")), rotation) == "north":
			occupied.append(port_center(port).rotated(float(rotation) * PI * 0.5).x)
	if room.has("ocean_side") and rotated_side(str(room.ocean_side), rotation) == "north":
		occupied.append(0.0)
	for candidate in [float(wall_style.get("axis",0.0)), 0.0, -230.0, 230.0]:
		var clear := true
		for blocked in occupied:
			var gap := 198.0 if room.has("ocean_side") and rotated_side(str(room.ocean_side), rotation) == "north" else 148.0
			if absf(candidate - blocked) < gap: clear = false
		if clear: return candidate
	return 0.0

static func finish(canvas: CanvasItem) -> void:
	canvas.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

static func panel(canvas: CanvasItem, rect: Rect2, body: Color, rim: Color) -> void:
	canvas.draw_rect(rect.grow(7), Color("#061016"))
	canvas.draw_rect(rect.grow(3), rim)
	canvas.draw_rect(rect, body)
	canvas.draw_line(rect.position + Vector2(7, 7), Vector2(rect.end.x - 7, rect.position.y + 7), Color(1, 1, 1, 0.25), 3)
	canvas.draw_line(Vector2(rect.position.x + 7, rect.end.y - 7), rect.end - Vector2(7, 7), Color(0, 0, 0, 0.45), 4)

static func _draw_station_port(canvas: CanvasItem, center: Vector2, side: String, accent: Color, floor_color: Color, raised: bool) -> void:
	if side.is_empty(): return
	var vertical := side == "west" or side == "east"
	var passage_size := Vector2(40 if vertical else 92, 92 if vertical else (76 if raised else 40))
	canvas.draw_rect(Rect2(center - passage_size * 0.5, passage_size), floor_color)
	var opening := Rect2(center - (Vector2(20, 92) if vertical else Vector2(92, 20)) * 0.5, Vector2(20, 92) if vertical else Vector2(92, 20))
	canvas.draw_rect(opening.grow(5), accent.darkened(0.58))
	canvas.draw_rect(opening, Color("#050d14"))
	if vertical:
		for y in [-38, 38]: canvas.draw_rect(Rect2(center + Vector2(-13, y-4), Vector2(26, 8)), accent.lightened(0.12))
	else:
		for x in [-38, 38]: canvas.draw_rect(Rect2(center + Vector2(x-4, -13), Vector2(8, 26)), accent.lightened(0.12))

static func _draw_ocean_face(canvas: CanvasItem, side: String, accent: Color, open: bool, raised: bool) -> void:
	var center := Vector2.ZERO
	if side == "north": center.y = -370
	elif side == "south": center.y = 370
	elif side == "west": center.x = -370
	elif side == "east": center.x = 370
	else: return
	var vertical := side == "west" or side == "east"
	var size := Vector2(28 if vertical else 192, 192 if vertical else (76 if raised and side == "north" else 28))
	canvas.draw_rect(Rect2(center - size * 0.5, size).grow(9), Color("#0a2838"))
	canvas.draw_rect(Rect2(center - size * 0.5, size), Color("#07161e") if open else Color("#113b4b"))
	for i in range(-2, 3):
		var mark := center + (Vector2(0, i * 31) if vertical else Vector2(i * 31, 0))
		canvas.draw_circle(mark, 4, accent.lightened(0.14))
