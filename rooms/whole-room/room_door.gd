extends RefCounted
## Two leaves retract into code-owned jambs; no second bitmap frame.
const OPENING := 72.0
static func leaf_rects(open_amount: float) -> Array:
	var width := OPENING*0.5*(1.0-clampf(open_amount,0,1))
	if width<=0: return []
	return [Rect2(-36,-6,width,12),Rect2(36-width,-6,width,12)]
static func draw_door(canvas: CanvasItem, open_amount: float) -> void:
	for panel in leaf_rects(open_amount):
		canvas.draw_rect(panel,Color("18262e"))
		if panel.size.x>2:
			canvas.draw_rect(panel.grow(-0.7),Color("879791"))
			canvas.draw_line(panel.position+Vector2(0.7,2),panel.position+Vector2(panel.size.x-0.7,2),Color("c8d0bc"),0.8)
			canvas.draw_line(panel.position+Vector2(0.7,9),panel.position+Vector2(panel.size.x-0.7,9),Color("4d6260"),0.8)
	for side in [-1,1]:
		canvas.draw_rect(Rect2(side*39-2,-4,4,8),Color("263c3b"))
		canvas.draw_rect(Rect2(side*39-1,-2,2,4),Color("91d4b0"))
