extends "res://rooms/whole-room/connected_rooms_view.gd"
## Single Life Support room using the shared embedded interface and south-facing art.
func rebuild() -> void:
	pair_mode = 0
	layout = [{"cell":Vector2i.ZERO,"rotation":quarter,"kind":2}]
	edges = Geometry.edges(layout)
	for edge in edges: edge.open = edge.port
	props.clear()
	for item in life_items:
		var source: Rect2 = item.rect
		var center := Geometry.turn(source.get_center(),quarter)
		var rect := Rect2(center-source.size*0.5,source.size)
		props.append({"id":item.id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":item})
	keep_props_inside_walls()
	actor = Vector2.ZERO
	queue_redraw()
func draw_room_floor(center: Vector2) -> void:
	draw_life_floor(center)
func layout_caption() -> String:
	return "LIFE SUPPORT / south-facing equipment / %d degrees"%(quarter*90)
