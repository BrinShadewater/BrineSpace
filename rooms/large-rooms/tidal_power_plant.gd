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
	Common.begin(canvas, room, rect, Color("#303841"), WALL_STYLE, "res://assets/department-floors-v1/engineering-tread.png", 0.36)
	Common.draw_features(canvas, FEATURES)
	Common.panel(canvas, Rect2(-204, -204, 408, 408), Color("#27343c"), Color("#92926b"))
	Common.sprite(canvas, "res://rooms/large-rooms/art/tidal_turbine.png", Rect2(-204, -204, 408, 408))
	Common.finish(canvas)
