extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"hydroponics_bay", "art":"res://rooms/large-rooms/art/grow_wall_bank.png", "axis":192.0, "shade":0.45}
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-1.png", "rect":Rect2(-150,228,125,84)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-4.png", "rect":Rect2(65,-305,126,67)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-2.png", "rect":Rect2(-58,-305,116,83)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-5.png", "rect":Rect2(209,30,103,66)},
]

static func fixed_bounds() -> Array[Rect2]:
	var result: Array[Rect2] = [Rect2(180, 180, 408, 408)]
	result.append_array(Common.feature_bounds(FEATURES))
	return result

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var green := Color("#7ba889")
	Common.begin(canvas, room, rect, Color("#263b36"), green, WALL_STYLE)
	Common.draw_features(canvas, FEATURES)
	# Fixed painted grow beds stay inside the recorded equipment footprint.
	Common.sprite(canvas, "res://rooms/large-rooms/art/grow_beds.png", Rect2(-204, -204, 408, 408))
	for x in [-258, 258]:
		for y in [-236, 0, 236]: canvas.draw_circle(Vector2(x, y), 11, green.darkened(0.4))
	Common.finish(canvas)
