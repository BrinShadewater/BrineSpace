extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"hydroponics_bay", "art":"res://rooms/large-rooms/art/grow_wall_bank.png", "axis":192.0, "shade":0.45}

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(180, 180, 408, 408)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var green := Color("#7ba889")
	Common.begin(canvas, room, rect, Color("#263b36"), green, WALL_STYLE)
	# Fixed painted grow beds stay inside the recorded equipment footprint.
	Common.sprite(canvas, "res://rooms/large-rooms/art/grow_beds.png", Rect2(-204, -204, 408, 408))
	for x in [-258, 258]:
		for y in [-236, 0, 236]: canvas.draw_circle(Vector2(x, y), 11, green.darkened(0.4))
	Common.finish(canvas)
