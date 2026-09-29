extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(210, 207, 348, 350)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#e6c84f")
	Common.begin(canvas, room, rect, Color("#303841"), yellow)
	for x in [-227, 227]:
		canvas.draw_rect(Rect2(x - 16, -319, 32, 638), Color("#6f7b7c"))
		for y in range(-277, 278, 92): canvas.draw_rect(Rect2(x - 24, y - 5, 48, 10), Color("#b4ab70"))
	Common.panel(canvas, Rect2(-174, -177, 348, 350), Color("#27343c"), Color("#92926b"))
	canvas.draw_circle(Vector2.ZERO, 151, Color("#74888c"))
	canvas.draw_circle(Vector2.ZERO, 125, Color("#253f4a"))
	for i in range(12):
		var angle := TAU * float(i) / 12.0
		var inner := Vector2.RIGHT.rotated(angle) * 46.0
		var outer := Vector2.RIGHT.rotated(angle + 0.22) * 119.0
		canvas.draw_line(inner, outer, Color("#b0bdaf"), 23)
		canvas.draw_line(inner, outer, Color("#567c7b"), 10)
	canvas.draw_circle(Vector2.ZERO, 43, Color("#d1bb65"))
	canvas.draw_circle(Vector2.ZERO, 25, Color("#26333b"))
	for x in [-305, 305]:
		for y in [-165, 165]:
			canvas.draw_rect(Rect2(x - 18, y - 28, 36, 56), Color("#5f6e70"))
			canvas.draw_rect(Rect2(x - 12, y - 16, 24, 9), yellow.darkened(0.35))
	Common.finish(canvas)
