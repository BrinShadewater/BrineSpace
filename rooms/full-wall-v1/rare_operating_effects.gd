extends RefCounted
## Small instrument-local cues; source art and room lighting remain unchanged.
static func owns(prop: Dictionary) -> bool:
	return prop.get("full_wall",false) or prop.id=="flush_back"

static func marks(room, prop: Dictionary, listening: bool) -> Array:
	if not room.operating or not owns(prop): return []
	var box: Rect2=room.prop_visual_bounds(prop)
	var side: String=prop.get("side_view","")
	var vertical: bool=side in ["west","east"]
	var center: Vector2
	var radius: Vector2
	if listening:
		center=Vector2(0.5,0.33 if prop.id=="flush_back" else 0.43)
		radius=Vector2(box.size.x*0.095,box.size.y*(0.22 if prop.id=="flush_back" else 0.23))
		if vertical:
			center=Vector2(0.76 if side=="west" else 0.24,0.29)
			radius=Vector2(box.size.x*0.065,box.size.y*0.035)
	else:
		center=Vector2(0.5,0.59 if prop.id=="flush_back" else 0.44)
		radius=Vector2.ONE*box.size.x*0.042
		if vertical:
			center=Vector2(0.72 if side=="west" else 0.28,0.49)
			radius=Vector2(box.size.x*0.09,box.size.y*0.029)
	center=box.position+center*box.size
	var angle: float=room.machine_clock*0.55 if listening else -1.0+0.10*sin(room.machine_clock*0.7)
	var direction:=Vector2(cos(angle),sin(angle))*radius
	var color:=Color(0.23,0.61,0.54,0.48) if listening else Color(0.45,0.32,0.16,0.65)
	return [[center,center+direction,color]]

static func draw(room, prop: Dictionary, listening: bool) -> void:
	for mark in marks(room,prop,listening):
		room.painter.draw_line(mark[0],mark[1],mark[2],0.75,true)
