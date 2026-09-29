extends RefCounted

const FLOOR_SIZE := 768.0
const HALF := FLOOR_SIZE * 0.5
const RiserCatalog = preload("res://rooms/whole-room/riser_catalog.gd")
static var art_textures: Dictionary = {}

static func sprite(canvas: CanvasItem, path: String, bounds: Rect2, tint: Color = Color.WHITE) -> void:
	if not art_textures.has(path):
		var image := Image.new()
		var error := image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
		if error != OK:
			push_error("Large room art could not load: %s (%d)" % [path, error])
			return
		art_textures[path] = ImageTexture.create_from_image(image)
	var texture: Texture2D = art_textures[path]
	var natural: Vector2 = texture.get_size()
	var scale: float = minf(bounds.size.x / natural.x, bounds.size.y / natural.y)
	var size: Vector2 = natural * scale
	canvas.draw_texture_rect(texture, Rect2(bounds.get_center() - size * 0.5, size), false, tint)

static func begin(canvas: CanvasItem, room: Dictionary, rect: Rect2, floor_color: Color, accent: Color, wall_style: Dictionary) -> void:
	canvas.draw_set_transform(rect.get_center(), deg_to_rad(float(int(room.get("rotation", 0)) * 90)), Vector2.ONE * (rect.size.x / FLOOR_SIZE))
	canvas.draw_rect(Rect2(-HALF, -HALF, FLOOR_SIZE, FLOOR_SIZE), Color("#081119"))
	canvas.draw_rect(Rect2(-370, -370, 740, 740), floor_color)
	for line in range(-320, 321, 64):
		canvas.draw_line(Vector2(-360, line), Vector2(360, line), Color(1, 1, 1, 0.035), 2)
		canvas.draw_line(Vector2(line, -360), Vector2(line, 360), Color(1, 1, 1, 0.035), 2)
	for p in [Vector2(-334,-334),Vector2(334,-334),Vector2(-334,334),Vector2(334,334)]:
		canvas.draw_circle(p, 7, accent.darkened(0.6))
		canvas.draw_circle(p, 3, accent)
	for y in [-360, 360]:
		canvas.draw_rect(Rect2(-384, y-12, 768, 24), Color("#1e313c"))
		canvas.draw_line(Vector2(-356, y), Vector2(356, y), accent.darkened(0.68), 3)
	for x in [-360, 360]:
		canvas.draw_rect(Rect2(x-12, -384, 24, 768), Color("#1e313c"))
		canvas.draw_line(Vector2(x, -356), Vector2(x, 356), accent.darkened(0.68), 3)
	var raised: bool = bool(room.get("raised_walls", true))
	if raised:
		_draw_risers(canvas, room, rect, wall_style)
	for port in room.get("ports", []):
		_draw_station_port(canvas, port, accent, floor_color, raised)
	if room.has("ocean_side"):
		_draw_ocean_face(canvas, str(room.ocean_side), accent, bool(room.get("moonbay_mission",{}).get("ocean_open",false)), raised)

static func _draw_risers(canvas: CanvasItem, room: Dictionary, rect: Rect2, wall_style: Dictionary) -> void:
	var material: String = str(wall_style.get("material",""))
	var art: String = str(wall_style.get("art",""))
	var shade: float = float(wall_style.get("shade",0.25))
	var names := ["north","east","south","west"]
	var base_rotation := deg_to_rad(float(int(room.get("rotation",0))*90))
	var scale := Vector2.ONE * (rect.size.x / FLOOR_SIZE)
	for side in range(4):
		canvas.draw_set_transform(rect.get_center(),base_rotation+float(side)*PI*0.5,scale)
		canvas.draw_rect(Rect2(-384,-388,768,76),Color("#0b151b"))
		for half in range(2):
			var left: float = -384.0+float(half)*384.0
			RiserCatalog.face(canvas,material,Rect2(left,-380,384,60))
			RiserCatalog.cap(canvas,material,Rect2(left,-388,384,8))
			RiserCatalog.skirt(canvas,material,Rect2(left,-320,384,8))
		canvas.draw_rect(Rect2(-384,-388,768,76),Color(0.04,0.08,0.09,shade))
		if art!="" and names[side]==str(wall_style.get("side","")):
			var axis: float = float(wall_style.get("axis",0.0))
			sprite(canvas,art,Rect2(axis-102,-381,204,62))
	canvas.draw_set_transform(rect.get_center(),base_rotation,scale)

static func finish(canvas: CanvasItem) -> void:
	canvas.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

static func panel(canvas: CanvasItem, rect: Rect2, body: Color, rim: Color) -> void:
	canvas.draw_rect(rect.grow(7), Color("#061016"))
	canvas.draw_rect(rect.grow(3), rim)
	canvas.draw_rect(rect, body)
	canvas.draw_line(rect.position + Vector2(7, 7), Vector2(rect.end.x - 7, rect.position.y + 7), Color(1, 1, 1, 0.25), 3)
	canvas.draw_line(Vector2(rect.position.x + 7, rect.end.y - 7), rect.end - Vector2(7, 7), Color(0, 0, 0, 0.45), 4)

static func _draw_station_port(canvas: CanvasItem, port: Dictionary, accent: Color, floor_color: Color, raised: bool) -> void:
	var local: Vector2i = port.get("cell", Vector2i.ZERO)
	var side := str(port.get("side", ""))
	var center := Vector2(-192 + local.x * 384, -192 + local.y * 384)
	if side == "north": center.y = -370
	elif side == "south": center.y = 370
	elif side == "west": center.x = -370
	elif side == "east": center.x = 370
	else: return
	var vertical := side == "west" or side == "east"
	if raised:
		var passage := Rect2(center - (Vector2(76, 92) if vertical else Vector2(92, 76)) * 0.5, Vector2(76, 92) if vertical else Vector2(92, 76))
		canvas.draw_rect(passage, floor_color)
	var opening := Rect2(center - (Vector2(20, 92) if vertical else Vector2(92, 20)) * 0.5, Vector2(20, 92) if vertical else Vector2(92, 20))
	canvas.draw_rect(opening.grow(5), accent.darkened(0.58))
	canvas.draw_rect(opening, Color("#050d14"))
	if vertical:
		for y in [-38, 38]: canvas.draw_rect(Rect2(center + Vector2(-13, y-4), Vector2(26, 8)), accent.lightened(0.26))
	else:
		for x in [-38, 38]: canvas.draw_rect(Rect2(center + Vector2(x-4, -13), Vector2(8, 26)), accent.lightened(0.26))

static func _draw_ocean_face(canvas: CanvasItem, side: String, accent: Color, open: bool, raised: bool) -> void:
	var center := Vector2.ZERO
	if side == "north": center.y = -370
	elif side == "south": center.y = 370
	elif side == "west": center.x = -370
	elif side == "east": center.x = 370
	else: return
	var vertical := side == "west" or side == "east"
	var size := (Vector2(76, 192) if vertical else Vector2(192, 76)) if raised else (Vector2(28, 192) if vertical else Vector2(192, 28))
	canvas.draw_rect(Rect2(center - size * 0.5, size).grow(9), Color("#0a2838"))
	canvas.draw_rect(Rect2(center - size * 0.5, size), Color("#07161e") if open else Color("#113b4b"))
	for i in range(-2, 3):
		var mark := center + (Vector2(0, i * 31) if vertical else Vector2(i * 31, 0))
		canvas.draw_circle(mark, 4, accent.lightened(0.32))
