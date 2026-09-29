extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"storage_bay", "art":"res://rooms/large-rooms/art/cargo_wall_bank.png", "axis":192.0, "shade":0.31}
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-storage_bay-1.png", "rect":Rect2(-312,-40,100,73)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-3.png", "rect":Rect2(-310,-155,86,101)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-5.png", "rect":Rect2(220,0,91,115)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-6.png", "rect":Rect2(80,-305,42,77)},
]

static func fixed_bounds() -> Array[Rect2]:
	var result: Array[Rect2] = [Rect2(180, 180, 408, 408)]
	result.append_array(Common.feature_bounds(FEATURES))
	return result

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#a49b7a")
	Common.begin(canvas, room, rect, Color("#30383a"), yellow, WALL_STYLE)
	Common.draw_features(canvas, FEATURES)
	Common.sprite(canvas, "res://rooms/large-rooms/art/cargo_gantry.png", Rect2(-204, -204, 408, 408))
	for x in [-284, 284]:
		for y in [-278, 278]:
			canvas.draw_rect(Rect2(x - 18, y - 13, 36, 26), Color("#48555b"))
	Common.finish(canvas)
