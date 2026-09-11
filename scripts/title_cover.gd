extends Control

const Preferences = preload("res://scripts/title_settings.gd")
const DESIGN := Vector2(1584, 672)
var elapsed := 0.0
var stage: Control
var character: Control
var rear: AmbientLayer
var front: AmbientLayer

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = true
	stage = Control.new()
	stage.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(stage)
	var background := _picture("res://brineui/title/consistency-v1/background.png")
	stage.add_child(background)
	rear = AmbientLayer.new()
	stage.add_child(rear)
	character = _character_layer()
	character.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	stage.add_child(character)
	front = AmbientLayer.new()
	front.foreground = true
	stage.add_child(front)
	resized.connect(_layout)
	_layout()

func _character_layer() -> Control:
	var layer := Control.new()
	layer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var body := Polygon2D.new()
	var source := Image.new()
	var error := preload("res://scripts/safe_image.gd").load_png(source, "res://brineui/title/likeness-v2/cover.png")
	if error != OK:
		var fallback := TextureRect.new()
		fallback.texture = ImageTexture.create_from_image(source)
		fallback.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		fallback.size = DESIGN
		fallback.mouse_filter = Control.MOUSE_FILTER_IGNORE
		layer.add_child(fallback)
		body.free()
		return layer
	body.texture = ImageTexture.create_from_image(source)
	var outline: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://brineui/title/consistency-v1/character-outline.json"))
	assert(source.get_size()==Vector2i(outline.sourceSize[0],outline.sourceSize[1]),"Title silhouette must match its registered source")
	var points := PackedVector2Array()
	for point in outline.points: points.append(Vector2(point[0],point[1]))
	body.polygon = points
	body.uv = points
	body.antialiased = true
	body.scale = DESIGN / Vector2(source.get_size())
	layer.add_child(body)
	return layer

func _picture(path: String) -> TextureRect:
	var picture := TextureRect.new()
	var source := Image.new()
	preload("res://scripts/safe_image.gd").load_png(source, path)
	picture.texture = ImageTexture.create_from_image(source)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.size = DESIGN
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	return picture

func _layout() -> void:
	stage.scale = size / DESIGN

func _process(delta: float) -> void:
	if Preferences.reduced_motion:
		return
	elapsed = fposmod(elapsed + delta, 120.0)
	character.position.y = 3.0 * sin(TAU * elapsed / 8.0)
	rear.elapsed = elapsed
	front.elapsed = elapsed
	rear.queue_redraw()
	front.queue_redraw()

class AmbientLayer extends Node2D:
	var foreground := false
	var elapsed := 0.0
	const SCREENS := [
		[Vector2(119,191),Vector2(204,204),Vector2(195,276),Vector2(108,264)],
		[Vector2(113,326),Vector2(197,330),Vector2(191,392),Vector2(112,390)],
		[Vector2(512,311),Vector2(551,313),Vector2(553,346),Vector2(510,344)],
		[Vector2(537,374),Vector2(558,373),Vector2(563,416),Vector2(543,417)],
		[Vector2(1089,391),Vector2(1140,389),Vector2(1132,422),Vector2(1080,420)],
		[Vector2(1320,327),Vector2(1375,322),Vector2(1382,368),Vector2(1321,372)],
		[Vector2(1514,321),Vector2(1536,320),Vector2(1536,351),Vector2(1514,352)]
	]

	func _draw() -> void:
		# Stable deterministic seeds; depth changes size, speed and opacity.
		for i in range(9 if foreground else 38):
			var phase := fposmod(i * 0.6180339 + (0.23 if foreground else 0.0) - elapsed / (10.0 if foreground else 15.0), 1.0)
			var center := Vector2(626 + fposmod(i * 113.73, 350.0) + 3.0 * sin(elapsed * TAU / 8.0 + i), 214 + phase * 468)
			var fade := smoothstep(0.0, 0.13, phase) * smoothstep(0.0, 0.08, 1.0 - phase)
			var radius := (2.2 if foreground else 1.0) + (i % 3) * 0.55
			draw_arc(center, radius, 0, TAU, 8, Color(0.58,0.89,0.96,fade * (0.24 if foreground else 0.40)), 1.0, true)
		if not foreground:
			for i in range(SCREENS.size()):
				_monitor(SCREENS[i], i)

	func _point(quad: Array, uv: Vector2) -> Vector2:
		return quad[0].lerp(quad[1], uv.x).lerp(quad[3].lerp(quad[2], uv.x), uv.y)

	func _line(quad: Array, a: Vector2, b: Vector2, color: Color) -> void:
		draw_line(_point(quad,a), _point(quad,b), color, 1.0)

	func _monitor(quad: Array, index: int) -> void:
		draw_colored_polygon(PackedVector2Array(quad), Color("051627"))
		_line(quad,Vector2(0.04,0.07),Vector2(0.94,0.07),Color("328aab"))
		if index % 3 == 1:
			var points := PackedVector2Array()
			for x in range(49):
				var u := float(x) / 48.0
				var phase := fposmod(u + elapsed / 4.0, 1.0)
				var v := 0.5 + 0.04 * sin(phase * TAU * 5) - 0.28 * exp(-pow((phase - 0.47) / 0.028, 2))
				points.append(_point(quad, Vector2(0.04 + u * 0.9,v)))
			draw_polyline(points, Color("68d6de"), 1.0, true)
		else:
			for row in range(7):
				var y := 0.16 + fposmod(row / 7.0 - elapsed / 8.0, 1.0) * 0.72
				for column in range(4):
					var x := 0.06 + column * 0.23
					var width := 0.05 + ((row * 7 + column * 3 + index) % 9) * 0.012
					_line(quad,Vector2(x,y),Vector2(x + width,y),Color("489aaf"))
		var pulse := 0.55 + 0.25 * sin(elapsed * TAU / 4 + index)
		_line(quad,Vector2(0.78,0.94),Vector2(0.95,0.94),Color(0.4,0.85,0.88,pulse))
