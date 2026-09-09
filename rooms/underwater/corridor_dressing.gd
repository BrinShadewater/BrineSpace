extends RefCounted
const WallArt = preload("res://rooms/underwater/corridor_wall_art.gd")
const G = preload("res://tools/modular_room_geometry.gd")

static func draw_props(_canvas: CanvasItem, _q: int, _variant: int, _light: float) -> void:
	# Retained call contract; owner removed legacy corridor fittings and clutter.
	pass

static func draw_risers(canvas: CanvasItem, hull: PackedVector2Array, q: int, variant: int, light: float, neighbors: Array = []) -> void:
	var tint:=Color(light,light,light)
	var wall_id:=WallArt.key(hull.size()!=8,variant)
	for i in range(hull.size()):
		var a:=G.turn(hull[i],q)
		var b:=G.turn(hull[(i+1)%hull.size()],q)
		var middle_edge:=(a+b)*.5
		# Only a boundary touching the neighboring cell loses its raised face.
		if middle_edge.y<=-191 and neighbors.has(Vector2i.UP):continue
		if middle_edge.y>=191 and neighbors.has(Vector2i.DOWN):continue
		if middle_edge.x<=-191 and neighbors.has(Vector2i.LEFT):continue
		if middle_edge.x>=191 and neighbors.has(Vector2i.RIGHT):continue
		if absf(a.x-b.x)>.1 and absf(a.y-b.y)>.1:
			# Chamfer faces use the actual sloped hull edge, not a rectangular patch.
			var rise:=35.0 if b.x>a.x else 18.0
			var lift:=Vector2(0,-rise)
			WallArt.polygon(canvas,wall_id,PackedVector2Array([a+lift,b+lift,b,a]),"return",light)
			canvas.draw_colored_polygon(PackedVector2Array([a+lift,b+lift,b+lift+Vector2(0,3),a+lift+Vector2(0,3)]),Color("a0afa5")*tint)
			canvas.draw_line(a,b,Color("293f45")*tint,2)
			canvas.draw_line(a+Vector2(0,-2),a+lift+Vector2(0,4),Color("3a5159")*tint,1)
			continue
		if absf(a.x-b.x)<.1 and absf(a.y-b.y)>60:
			# Narrow side returns keep the central aisle visible in the fixed camera.
			var outside:=6.0 if b.y>a.y else -6.0
			var top:=side_return_top(hull,q,i)
			var bottom:=maxf(a.y,b.y)
			var face:=Rect2(minf(a.x,a.x+outside),top,absf(outside),bottom-top)
			WallArt.polygon(canvas,wall_id,PackedVector2Array([face.position,Vector2(face.position.x,face.end.y),face.end,Vector2(face.end.x,face.position.y)]),"cap",light)
			canvas.draw_line(Vector2(face.position.x,top),Vector2(face.end.x,top),Color("a0afa5")*tint,2)
			canvas.draw_line(Vector2(a.x+outside,top),Vector2(a.x+outside,bottom),Color("a0afa5")*tint,2)
			for y in range(int(top)+12,int(bottom),40):
				canvas.draw_line(Vector2(face.position.x,y),Vector2(face.end.x,y),Color("253e45")*tint,1)
			continue
		# Clockwise hull: left-to-right horizontal edges face screen north.
		if absf(a.y-b.y)>.1 or b.x-a.x<60:continue
		var width:=b.x-a.x
		var wall:=Rect2(a-Vector2(0,35),Vector2(width,35))
		var entry:=is_north_entry(a,b)
		if entry: WallArt.solid(canvas,wall_id,wall,light)
		else: WallArt.face(canvas,wall_id,wall,light)
		WallArt.cap(canvas,wall_id,Rect2(wall.position,Vector2(width,4)),light)
		canvas.draw_line(a,b,Color("293f45")*tint,3)
		if entry: WallArt.closed_entry(canvas,wall,light)

	draw_entries(canvas,hull,q,true,neighbors)

static func draw_entries(canvas: CanvasItem, hull: PackedVector2Array, q: int, raised: bool, neighbors: Array=[]) -> void:
	for i in range(hull.size()):
		var a:=G.turn(hull[i],q)
		var b:=G.turn(hull[(i+1)%hull.size()],q)
		var middle: Vector2=(a+b)*.5
		var side:=Vector2i.ZERO
		if absf(middle.x)>=191.99: side=Vector2i(int(signf(middle.x)),0)
		elif absf(middle.y)>=191.99: side=Vector2i(0,int(signf(middle.y)))
		if side==Vector2i.ZERO or side in neighbors or (raised and side==Vector2i.UP): continue
		preload("res://rooms/doors/door_finish.gd").low_closed(canvas,middle,side.x!=0,"metal")

static func side_return_top(hull: PackedVector2Array, q: int, edge: int) -> float:
	var a:=G.turn(hull[edge],q)
	var b:=G.turn(hull[(edge+1)%hull.size()],q)
	var vertex:=edge if a.y<b.y else (edge+1)%hull.size()
	var p:=G.turn(hull[vertex],q)
	var before:=G.turn(hull[posmod(vertex-1,hull.size())],q)
	var after:=G.turn(hull[(vertex+1)%hull.size()],q)
	var concave: bool=(p-before).cross(after-p)<0
	return p.y if concave else p.y-35.0

static func is_north_entry(a: Vector2, b: Vector2) -> bool:
	return absf(a.y+192)<.01 and absf(b.y+192)<.01 and a.x<0 and b.x>0

static func taper_face(a: Vector2, b: Vector2) -> PackedVector2Array:
	if absf(a.x-b.x)<=.1 or absf(a.y-b.y)<=.1:return PackedVector2Array()
	var lift:=Vector2(0,-35.0 if b.x>a.x else -18.0)
	return PackedVector2Array([a,b,b+lift,a+lift])
