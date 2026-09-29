extends RefCounted

const Common = preload("res://rooms/large-rooms/common.gd")
const WALL_STYLE := {"material":"storage_bay", "art":"res://rooms/large-rooms/art/cargo_wall_bank.png", "axis":192.0, "shade":0.25}

static func fixed_bounds() -> Array[Rect2]:
	return [Rect2(180, 180, 408, 408)]

static func draw(canvas: CanvasItem, room: Dictionary, rect: Rect2) -> void:
	var yellow := Color("#e6c84f")
	Common.begin(canvas, room, rect, Color("#30383a"), yellow, WALL_STYLE)
	Common.sprite(canvas, "res://rooms/large-rooms/art/cargo_gantry.png", Rect2(-204, -204, 408, 408))
	for x in [-284, 284]:
		for y in [-278, 278]:
			canvas.draw_rect(Rect2(x - 18, y - 13, 36, 26), Color("#48555b"))
	Common.finish(canvas)
