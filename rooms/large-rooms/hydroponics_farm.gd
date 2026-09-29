extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(238, 218, 292, 332)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var green := Color("#57c879")
	Common.begin(canvas, room, rect, Color("#263b36"), green)
	# A single anchored growing installation spans all four grid cells.
	Common.panel(canvas, Rect2(-146, -166, 292, 332), Color("#1b3029"), Color("#557b67"))
	for x in [-104, -34, 36, 106]:
		Common.panel(canvas, Rect2(x - 25, -145, 50, 290), Color("#243b2e"), Color("#77937b"))
		for y in range(-118, 128, 49):
			canvas.draw_circle(Vector2(x - 9, y), 13, Color("#244e32"))
			canvas.draw_circle(Vector2(x + 8, y + 7), 11, Color("#3d8951"))
			canvas.draw_circle(Vector2(x, y - 6), 7, Color("#77c96e"))
	canvas.draw_rect(Rect2(-9, -172, 18, 344), Color("#98c8a6"))
	for y in [-126, -42, 42, 126]:
		canvas.draw_line(Vector2(-144, y), Vector2(144, y), Color("#65b8ad"), 5)
	for x in [-258, 258]:
		for y in [-236, 0, 236]: canvas.draw_circle(Vector2(x, y), 11, green.darkened(0.4))
	Common.finish(canvas)
