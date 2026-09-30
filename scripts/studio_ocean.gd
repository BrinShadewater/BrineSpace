extends Control
## The ocean behind a room in the Room Layout Studio (owner playtest, Sept 29: a background that looks like
## the ocean in game). Deep teal water that darkens with depth, soft patches of seabed, slow light shafts
## and drifting marine snow, with a dark edge. It is a node of its own behind the editor canvas, so its slow
## drift never makes the room redraw. Low quality and Reduced Motion hold it still.

const TitleSettings = preload("res://scripts/title_settings.gd")
const DraftCard = preload("res://scripts/draft_card.gd")
const SNOW := 70
var clock := 0.0
var since_draw := 0.0
static var _vignette: GradientTexture2D

func _init() -> void:
	name = "OceanBackdrop"
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	show_behind_parent = true
	set_anchors_preset(Control.PRESET_FULL_RECT)

func animated() -> bool:
	return visible and not TitleSettings.reduced_motion and TitleSettings.effects_quality > 0

func _process(delta: float) -> void:
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
	draw_texture_rect(DraftCard.ocean_texture(), area, false)
	# Patches of dark seabed, each with a paler rim.
	for i in range(14):
		var h := _h(i)
		var centre := Vector2(h.x * size.x, h.y * size.y)
		var radius := size.y * (0.09 + 0.15 * _h(i + 40).x)
		draw_circle(centre, radius, Color(0.02, 0.07, 0.09, 0.24))
		draw_circle(centre + Vector2(radius * 0.15, -radius * 0.1), radius * 0.6, Color(0.05, 0.15, 0.18, 0.10))
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
