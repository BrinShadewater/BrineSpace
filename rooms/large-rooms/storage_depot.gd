extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"storage_bay", "art":"res://rooms/large-rooms/art/cargo_wall_bank.png", "axis":192.0, "shade":0.31}
const CENTER_BOUNDS := Rect2(180, 180, 408, 408)
# Default placements of the supporting equipment: ordinary movable props seeded by StudioView.feature_seed. Only the centerpiece is fixed.
const FEATURES := [
	{"path":"res://assets/station-props-v2/sp-storage_bay-1.png", "rect":Rect2(-312,-40,100,73)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-3.png", "rect":Rect2(-310,-155,86,101)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-5.png", "rect":Rect2(220,0,91,115)},
	{"path":"res://assets/station-props-v2/sp-storage_bay-6.png", "rect":Rect2(80,-305,42,77)},
]

static func fixed_bounds() -> Array[Rect2]:
	return [CENTER_BOUNDS]

static func fixed_bounds_for_rotation(rotation: int) -> Array[Rect2]:
	return Common.fixed_bounds_for_rotation(CENTER_BOUNDS, [], rotation)

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	Common.begin(canvas, room, rect, Color("#30383a"), WALL_STYLE, "res://assets/department-floors-v2/storage-load-deck.png", 0.43)
	Common.south_transform(canvas, rect)
	Common.sprite(canvas, "res://rooms/large-rooms/art/cargo_gantry.png", Rect2(-204, -204, 408, 408))
	Common.finish(canvas)
