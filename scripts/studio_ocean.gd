extends Control
## The ocean behind a room in the Room Layout Studio (owner playtest, Sept 29: a background that looks like
## the ocean in game). The seabed is the game's own ground: the same silt tiles, tint and mirrored repeat,
## three cells to a tile, lined up with the room at the Studio's zoom (owner, October 14, 2026). Over it,
## slow light shafts and drifting marine snow, with a dark edge. It is a node of its own behind the editor
## canvas, so its slow drift never makes the room redraw. Low quality and Reduced Motion hold it still.

const TitleSettings = preload("res://scripts/title_settings.gd")
const SNOW := 70
const Seabed = preload("res://assets/environment/seabed-v1/seabed_background.gd")
## The room stands on this cell of the game's grid, so the tiles fall where they would in the station.
const ROOM_CELL := Vector2(20, 20)
var clock := 0.0
var since_draw := 0.0
var drawn_view := []
static var _vignette: GradientTexture2D
static var _ground: Texture2D

func _init() -> void:
	name = "OceanBackdrop"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	show_behind_parent = true
	# Whole tiles and leaning shafts reach past the canvas; keep them off the toolbars.
	clip_contents = true
	set_anchors_preset(Control.PRESET_FULL_RECT)

func animated() -> bool:
	return visible and not TitleSettings.reduced_motion and TitleSettings.effects_quality > 0

# Where the canvas puts the room: [origin, room units to pixels]. The tiles follow pan and zoom.
func view() -> Array:
	var canvas := get_parent()
	if canvas == null or not canvas.has_method("origin") or not canvas.has_method("factor") or canvas.editor == null: return [size * 0.5, 1.0]
	return [canvas.origin(), canvas.factor()]

# The silt tile the game's seabed picks (`prepare` in seabed_background.gd), without loading its scenery.
static func ground() -> Texture2D:
	if _ground == null:
		_ground = preload("res://scripts/environment_art.gd").texture("silt-plain")
		if _ground == null:
			var image := Image.new()
			if preload("res://scripts/safe_image.gd").load_png(image, Seabed.SOURCES["silt-plain"]) == OK: _ground = ImageTexture.create_from_image(image)
	return _ground

func _process(delta: float) -> void:
	if view() != drawn_view: queue_redraw()
	if not animated(): return
	clock += delta
	since_draw += delta
	if since_draw >= 0.05:
		since_draw = 0.0
		queue_redraw()

static func _h(i: int) -> Vector2:
	return Vector2(fposmod(sin(float(i) * 127.1) * 43758.5453, 1.0), fposmod(sin(float(i) * 311.7) * 43758.5453, 1.0))

static func vignette() -> GradientTexture2D:
	if _vignette != null: return _vignette
	var gradient := Gradient.new()
	gradient.offsets = PackedFloat32Array([0.0, 0.6, 1.0])
	gradient.colors = PackedColorArray([Color(0, 0, 0, 0), Color(0, 0, 0, 0.08), Color(0.0, 0.02, 0.03, 0.62)])
	_vignette = GradientTexture2D.new()
	_vignette.gradient = gradient
	_vignette.fill = GradientTexture2D.FILL_RADIAL
	_vignette.fill_from = Vector2(0.5, 0.5)
	_vignette.fill_to = Vector2(1.0, 0.5)
	_vignette.width = 256
	_vignette.height = 256
	return _vignette

func _draw() -> void:
	var area := Rect2(Vector2.ZERO, size)
	drawn_view = view()
	_draw_seabed(area, drawn_view[0], float(drawn_view[1]))
	# Slow light shafts from the surface.
	for i in range(5):
		var base := size.x * (0.08 + 0.2 * float(i)) + sin(clock * 0.15 + float(i) * 1.7) * size.x * 0.03
		var lean := size.x * 0.10
		var width := size.x * (0.05 + 0.02 * _h(i + 70).x)
		var quad := PackedVector2Array([Vector2(base, 0), Vector2(base + width, 0), Vector2(base + width - lean, size.y), Vector2(base - lean, size.y)])
		draw_colored_polygon(quad, Color(0.35, 0.75, 0.85, 0.035))
	# Marine snow drifting down and across.
	for i in range(SNOW):
		var h := _h(i + 100)
		var x := fposmod(h.x * size.x + sin(clock * 0.4 + float(i)) * 10.0 + clock * 4.0, size.x)
		var y := fposmod(h.y * size.y + clock * (6.0 + h.x * 8.0), size.y)
		draw_circle(Vector2(x, y), 1.0 + h.y * 1.2, Color(0.75, 0.9, 0.95, 0.18 * (0.4 + h.x * 0.6)))
	draw_texture_rect(vignette(), area, false)

# The game's still seabed (`render_still` in seabed_background.gd): its base colour, then the silt tile
# mirrored on alternate tiles so edges join, tinted the same.
func _draw_seabed(area: Rect2, origin: Vector2, factor: float) -> void:
	draw_rect(area, Color("09222d"))
	var tile_texture := ground()
	if tile_texture == null: return
	var cell := 384.0 * factor
	var tile := cell * 3.0
	# Screen position of the game grid's top-left corner.
	var grid_origin := origin - Vector2.ONE * 192.0 * factor - ROOM_CELL * cell
	var first := Vector2i(((area.position - grid_origin) / tile).floor())
	var last := Vector2i(((area.end - grid_origin) / tile).ceil())
	var tint := Color(.49, .60, .64)
	for y in range(first.y, last.y):
		for x in range(first.x, last.x):
			var at := grid_origin + Vector2(x, y) * tile
			var uv := PackedVector2Array([Vector2.ZERO, Vector2.RIGHT, Vector2.ONE, Vector2.DOWN])
			for i in range(uv.size()):
				if x % 2 != 0: uv[i].x = 1.0 - uv[i].x
				if y % 2 != 0: uv[i].y = 1.0 - uv[i].y
			draw_polygon(PackedVector2Array([at, at + Vector2(tile, 0), at + Vector2(tile, tile), at + Vector2(0, tile)]), PackedColorArray([tint]), uv, tile_texture)
