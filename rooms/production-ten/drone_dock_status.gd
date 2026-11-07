extends RefCounted
## Cradle diagnostics, independent of a parked vehicle or exterior tool animation.
static func draw(painter: CanvasItem,center: Vector2,time: float,operating: bool) -> void:
	# Two physical panel lenses on the 90-unit cradle's front rail posts.
	for side in [-1,1]:
		var lens:=Rect2(center+Vector2(side*35.0-2.0,11.0),Vector2(4.0,3.0))
		painter.draw_rect(lens,Color("172125"))
		if operating:
			var level:=0.55+0.2*sin(time*2.0+side*0.7)
			painter.draw_rect(lens.grow(-0.6),Color(level,level*0.98,level*0.93,1.0))
