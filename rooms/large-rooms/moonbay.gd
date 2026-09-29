extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(151, 267, 466, 234)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var cyan := Color("#46d3e6")
	Common.begin(canvas, room, rect, Color("#263842"), cyan)
	# Floor rail points west to the sealed launch chamber; the hangar stays dry.
	for y in [-89, 89]:
		canvas.draw_rect(Rect2(-360, y - 7, 720, 14), Color("#597683"))
		for x in range(-340, 341, 68): canvas.draw_rect(Rect2(x - 4, y - 12, 8, 24), Color("#a2b7b9"))
	Common.panel(canvas, Rect2(-233, -117, 466, 234), Color("#1b303b"), Color("#537887"))
	# Broad pressure hull, observation glass and twin compact thrusters.
	canvas.draw_colored_polygon(PackedVector2Array([Vector2(-210,0),Vector2(-130,-73),Vector2(137,-73),Vector2(215,-35),Vector2(225,0),Vector2(215,35),Vector2(137,73),Vector2(-130,73)]), Color("#b4c5c6"))
	canvas.draw_colored_polygon(PackedVector2Array([Vector2(-173,0),Vector2(-114,-54),Vector2(120,-54),Vector2(180,-22),Vector2(185,0),Vector2(180,22),Vector2(120,54),Vector2(-114,54)]), Color("#4e707d"))
	canvas.draw_rect(Rect2(-80, -48, 105, 96), Color("#123a4e"))
	canvas.draw_rect(Rect2(-68, -37, 81, 74), Color("#2d7384"))
	for y in [-48, 48]:
		canvas.draw_rect(Rect2(130, y - 16, 94, 32), Color("#899ca2"))
		canvas.draw_circle(Vector2(218, y), 16, Color("#223c49"))
	canvas.draw_line(Vector2(-203, 0), Vector2(-340, 0), cyan.darkened(0.4), 6)
	for x in [-280, -150, 150, 280]: canvas.draw_circle(Vector2(x, 172), 9, cyan.darkened(0.3))
	Common.finish(canvas)
