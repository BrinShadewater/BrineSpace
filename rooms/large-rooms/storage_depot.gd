extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(248, 244, 272, 280)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#e6c84f")
	Common.begin(canvas, room, rect, Color("#30383a"), yellow)
	Common.panel(canvas, Rect2(-136, -140, 272, 280), Color("#253039"), Color("#65757b"))
	for x in [-101, 0, 101]:
		for y in [-91, 0, 91]:
			Common.panel(canvas, Rect2(x - 34, y - 29, 68, 58), Color("#77745c"), Color("#b2a77a"))
			canvas.draw_rect(Rect2(x - 24, y - 18, 48, 12), Color("#c5ba86"))
	for x in [-149, 149]:
		canvas.draw_rect(Rect2(x - 7, -167, 14, 334), Color("#b5a85e"))
	canvas.draw_rect(Rect2(-160, -174, 320, 18), Color("#d0ba58"))
	canvas.draw_rect(Rect2(-30, -190, 60, 25), Color("#2f444b"))
	for x in [-284, 284]:
		for y in [-278, 278]:
			canvas.draw_rect(Rect2(x - 18, y - 13, 36, 26), Color("#48555b"))
	Common.finish(canvas)
