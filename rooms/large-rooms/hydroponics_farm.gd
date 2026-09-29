extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"hydroponics_bay", "art":"res://rooms/large-rooms/art/grow_wall_bank.png", "axis":192.0, "shade":0.45}
const CENTER_BOUNDS := Rect2(180, 180, 408, 408)
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-1.png", "rect":Rect2(-150,228,125,84)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-4.png", "rect":Rect2(65,-305,126,67)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-2.png", "rect":Rect2(-58,-305,116,83)},
	{"path":"res://assets/station-props-v2/sp-hydroponics_bay-5.png", "rect":Rect2(209,30,103,66)},
]

static func fixed_bounds() -> Array[Rect2]:
	var result: Array[Rect2] = [CENTER_BOUNDS]
	result.append_array(Common.feature_bounds(FEATURES))
	return result

static func fixed_bounds_for_rotation(rotation: int) -> Array[Rect2]:
	return Common.fixed_bounds_for_rotation(CENTER_BOUNDS, FEATURES, rotation)

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	Common.begin(canvas, room, rect, Color("#343b3b"), WALL_STYLE, "res://assets/department-floors-v1/wet-drainage.png", 0.36)
	Common.draw_features(canvas, FEATURES, room, rect)
	# Fixed painted grow beds stay inside the recorded equipment footprint.
	Common.sprite(canvas, "res://rooms/large-rooms/art/grow_beds.png", Rect2(-204, -204, 408, 408))
	Common.finish(canvas)
