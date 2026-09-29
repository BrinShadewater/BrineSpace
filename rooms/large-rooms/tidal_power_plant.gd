extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"tidal_condenser", "art":"res://rooms/large-rooms/art/tidal_wall_bank.png", "axis":230.0, "shade":0.3}

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(180, 180, 408, 408)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#e6c84f")
	Common.begin(canvas, room, rect, Color("#303841"), yellow, WALL_STYLE)
	for x in [-227, 227]:
		canvas.draw_rect(Rect2(x - 16, -319, 32, 638), Color("#6f7b7c"))
		for y in range(-277, 278, 92): canvas.draw_rect(Rect2(x - 24, y - 5, 48, 10), Color("#b4ab70"))
	Common.panel(canvas, Rect2(-204, -204, 408, 408), Color("#27343c"), Color("#92926b"))
	Common.sprite(canvas, "res://rooms/large-rooms/art/tidal_turbine.png", Rect2(-204, -204, 408, 408))
	for x in [-305, 305]:
		for y in [-165, 165]:
			canvas.draw_rect(Rect2(x - 18, y - 28, 36, 56), Color("#5f6e70"))
			canvas.draw_rect(Rect2(x - 12, y - 16, 24, 9), yellow.darkened(0.35))
	Common.finish(canvas)
