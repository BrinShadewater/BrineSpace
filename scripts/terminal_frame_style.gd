@tool
extends StyleBox
## Clean HUD panel frame (owner playtest, Sept 17: the pixel-art frames looked low quality and
## pixelated when stretched to the window). Drawn as vector shapes at any size: a dark rounded
## panel with an anti-aliased border, a faint inner highlight along the top and the small
## corner marker the pixel frames carried. Settings > Accessibility > Pixel panel frames brings
## the textured frames back.

var bg_color := Color("071018")
var border_color := Color("1e3844")
var accent_color := Color("3f8f86")
var border_width := 2
var radius := 7
var _fill := StyleBoxFlat.new()

func _init() -> void:
	content_margin_left = 24
	content_margin_right = 24
	content_margin_top = 20
	content_margin_bottom = 20

func _draw(to_canvas_item: RID, rect: Rect2) -> void:
	_fill.bg_color = bg_color
	_fill.border_color = border_color
	_fill.set_border_width_all(border_width)
	_fill.set_corner_radius_all(radius)
	_fill.anti_aliasing = true
	_fill.corner_detail = 6
	_fill.draw(to_canvas_item, rect)
	var inner := rect.grow(-float(border_width) - 2.0)
	if inner.size.x <= 12.0 or inner.size.y <= 12.0: return
	RenderingServer.canvas_item_add_line(to_canvas_item, inner.position + Vector2(radius, 0), Vector2(inner.end.x - radius, inner.position.y), Color(border_color.lightened(0.25), 0.35), 1.0, true)
	RenderingServer.canvas_item_add_rect(to_canvas_item, Rect2(rect.position + Vector2(radius + 3, border_width + 4), Vector2(5, 5)), accent_color)

func _get_draw_rect(rect: Rect2) -> Rect2:
	return rect
