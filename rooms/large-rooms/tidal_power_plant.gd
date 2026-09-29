extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"tidal_condenser", "art":"res://rooms/large-rooms/art/tidal_wall_bank.png", "axis":230.0, "shade":0.3}
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-1.png", "rect":Rect2(-197,-305,92,93)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-4.png", "rect":Rect2(100,-295,100,67)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-2.png", "rect":Rect2(244,0,68,84)},
	{"path":"res://assets/station-props-v2/sp-tidal_condenser-5.png", "rect":Rect2(-37,214,73,98)},
]

static func fixed_bounds() -> Array[Rect2]:
	var result: Array[Rect2] = [Rect2(180, 180, 408, 408)]
	result.append_array(Common.feature_bounds(FEATURES))
	return result

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#b9aa70")
	Common.begin(canvas, room, rect, Color("#303841"), yellow, WALL_STYLE, "res://assets/department-floors-v1/engineering-tread.png", 0.36)
	# Recessed service grates flank the turbine's heavy mounting frame.
	for x in [-270.0, 270.0]:
		canvas.draw_rect(Rect2(x - 9, -207, 18, 414), Color("#1b282e"))
		for y in range(-200, 201, 20):
			canvas.draw_line(Vector2(x - 7, y), Vector2(x + 7, y), Color("#75817d", 0.65), 2)
	Common.draw_features(canvas, FEATURES)
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
