extends RefCounted
const G = preload("res://tools/modular_room_geometry.gd")

static func draw_props(canvas: CanvasItem, q: int, variant: int, light: float) -> void:
	# Small supplies are strapped to the hull ledge, outside the walkable deck.
	var tint:=Color(light,light,light)
	for index in range(2):
		var at:=G.turn(Vector2(-122+index*32,-56),q)
		canvas.draw_rect(Rect2(at+Vector2(-9,-1),Vector2(20,5)),Color(0,0,0,.3))
		canvas.draw_rect(Rect2(at+Vector2(-8,-19),Vector2(16,22)),Color("24373b")*tint)
		if (variant+index)%2==0:
			canvas.draw_rect(Rect2(at+Vector2(-7,-17),Vector2(14,19)),Color("766c50")*tint)
			canvas.draw_style_box(_box(Color("a29873")*tint),Rect2(at+Vector2(-7,-20),Vector2(14,6)))
			canvas.draw_rect(Rect2(at+Vector2(4,-16),Vector2(3,17)),Color("514d3d")*tint)
			canvas.draw_circle(at+Vector2(2,-18),1.2,Color("4a5148")*tint)
			for y in [-14,-3]:canvas.draw_line(at+Vector2(-7,y),at+Vector2(7,y),Color("b1b7a0")*tint,2)
			canvas.draw_line(at+Vector2(-4,-12),at+Vector2(-4,-5),Color("998c65")*tint,1)
		else:
			canvas.draw_rect(Rect2(at+Vector2(-9,-15),Vector2(18,17)),Color("596c68")*tint)
			canvas.draw_rect(Rect2(at+Vector2(-7,-13),Vector2(14,13)),Color("93a095")*tint,false,1)
			canvas.draw_colored_polygon(PackedVector2Array([at+Vector2(-9,-15),at+Vector2(-6,-19),at+Vector2(9,-19),at+Vector2(9,-15)]),Color("8d9c90")*tint)
			canvas.draw_rect(Rect2(at+Vector2(6,-14),Vector2(3,15)),Color("32474b")*tint)
			canvas.draw_line(at+Vector2(-6,-12),at+Vector2(6,-1),Color("334a4e")*tint,2)
			canvas.draw_rect(Rect2(at+Vector2(-2,-9),Vector2(5,4)),Color("c4b787")*tint)
	var mount:=G.turn(Vector2(-54,-56),q)
	if variant==1:
		# Wall-mounted extinguisher and a service cable reel.
		canvas.draw_rect(Rect2(mount+Vector2(-5,-21),Vector2(10,22)),Color("384b4d")*tint)
		canvas.draw_style_box(_box(Color("a36148")*tint),Rect2(mount+Vector2(-4,-18),Vector2(8,17)))
		canvas.draw_rect(Rect2(mount+Vector2(-4,-11),Vector2(8,4)),Color("d0c39d")*tint)
		canvas.draw_line(mount+Vector2(-2,-20),mount+Vector2(5,-20),Color("a6b4a8")*tint,2)
		var reel:=G.turn(Vector2(-150,-56),q)+Vector2(0,-6)
		canvas.draw_circle(reel,7,Color("84958a")*tint)
		for radius in [3,5]:canvas.draw_arc(reel,radius,0,TAU,18,Color("263e46")*tint,1.5)
		canvas.draw_circle(reel,1.5,Color("c5b17e")*tint)
	elif variant==2:
		# Compact emergency intercom, kept upright at every rotation.
		canvas.draw_rect(Rect2(mount+Vector2(-6,-20),Vector2(12,21)),Color("374e56")*tint)
		canvas.draw_rect(Rect2(mount+Vector2(-4,-18),Vector2(8,6)),Color("89b7aa")*tint)
		for y in [-9,-6,-3]:canvas.draw_line(mount+Vector2(-3,y),mount+Vector2(3,y),Color("859990")*tint,1)
	else:
		# Shallow strapped case with reinforced corners and a carrying handle.
		canvas.draw_rect(Rect2(mount+Vector2(-10,-12),Vector2(20,13)),Color("64766b")*tint)
		for x in [-8,6]:canvas.draw_rect(Rect2(mount+Vector2(x,-12),Vector2(2,13)),Color("b4ab87")*tint)
		canvas.draw_line(mount+Vector2(-3,-14),mount+Vector2(3,-14),Color("aeb8a6")*tint,2)
	# Bundled power cables run along the north-side wall band in local space.
	for offset in [0,3]:
		var points:=PackedVector2Array()
		for p in [Vector2(-151,-61+offset),Vector2(-76,-61+offset),Vector2(-66,-57+offset)]:points.append(G.turn(p,q))
		canvas.draw_polyline(points,Color("1b3038")*tint,2)
	for x in [-146,-82]:
		var at:=G.turn(Vector2(x,-59),q)
		canvas.draw_circle(at,2,Color("9aa89e")*tint)

static func draw_risers(canvas: CanvasItem, hull: PackedVector2Array, q: int, variant: int, light: float, neighbors: Array = []) -> void:
	var tint:=Color(light,light,light)
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
			canvas.draw_colored_polygon(taper_face(a,b),Color("536a70")*tint)
			canvas.draw_colored_polygon(PackedVector2Array([a+lift,b+lift,b+lift+Vector2(0,3),a+lift+Vector2(0,3)]),Color("a0afa5")*tint)
			canvas.draw_line(a,b,Color("293f45")*tint,2)
			canvas.draw_line(a+Vector2(0,-2),a+lift+Vector2(0,4),Color("3a5159")*tint,1)
			continue
		if absf(a.x-b.x)<.1 and absf(a.y-b.y)>60:
			# Narrow side returns keep the central aisle visible in the fixed camera.
			var outside:=6.0 if b.y>a.y else -6.0
			var top:=minf(a.y,b.y)-35.0
			var bottom:=maxf(a.y,b.y)
			var face:=Rect2(minf(a.x,a.x+outside),top,absf(outside),bottom-top)
			canvas.draw_rect(face,Color("425960")*tint)
			canvas.draw_line(Vector2(face.position.x,top),Vector2(face.end.x,top),Color("a0afa5")*tint,2)
			canvas.draw_line(Vector2(a.x+outside,top),Vector2(a.x+outside,bottom),Color("a0afa5")*tint,2)
			for y in range(int(top)+12,int(bottom),40):
				canvas.draw_line(Vector2(face.position.x,y),Vector2(face.end.x,y),Color("253e45")*tint,1)
			continue
		# Clockwise hull: left-to-right horizontal edges face screen north.
		if absf(a.y-b.y)>.1 or b.x-a.x<60:continue
		var width:=b.x-a.x
		var wall:=Rect2(a-Vector2(0,35),Vector2(width,35))
		canvas.draw_rect(wall,Color("647a7c")*tint)
		for y in range(5,33):
			canvas.draw_line(wall.position+Vector2(0,y),wall.position+Vector2(width,y),Color(0,0,0,float(y)/200.0),1)
		for x in range(4,int(width)-34,40):
			var panel:=Rect2(wall.position+Vector2(x,6),Vector2(32,25))
			canvas.draw_rect(panel,Color("40585f")*tint,false,1)
			canvas.draw_line(panel.position+Vector2(1,1),panel.position+Vector2(30,1),Color("849894")*tint,1)
			for dx in [3,29]:canvas.draw_circle(panel.position+Vector2(dx,3),.65,Color("b6bbae")*tint)

		canvas.draw_rect(Rect2(wall.position,Vector2(width,4)),Color("a1b1a8")*tint)
		canvas.draw_line(a,b,Color("293f45")*tint,3)
		for x in range(12,int(width),40):
			canvas.draw_line(wall.position+Vector2(x,5),a+Vector2(x,-2),Color("455d64")*tint,1)
		var middle:=(a+b)*.5
		if width>120 and variant!=1:
			var window:=Rect2(middle+Vector2(-32,-29),Vector2(64,23))
			canvas.draw_style_box(_box(Color("233f49")*tint),window.grow(3))
			canvas.draw_rect(window.grow(1),Color("102b34")*tint)
			canvas.draw_rect(window,Color("174754")*tint)
			canvas.draw_line(window.position+Vector2(0,24),window.position+Vector2(64,24),Color("a2b0a7")*tint,2)
			canvas.draw_line(window.position+Vector2(3,3),window.position+Vector2(58,3),Color("527f87")*tint,2)
			for x in [-18,13,20]:
				canvas.draw_line(middle+Vector2(x,-17),middle+Vector2(x+4,-16),Color("83a8a4")*tint,1)
			canvas.draw_line(window.position+Vector2(9,2),window.position+Vector2(5,14),Color(.7,.9,.9,.25),2)
			canvas.draw_line(middle+Vector2(0,-29),middle+Vector2(0,-6),Color("879c96")*tint,2)
		else:
			canvas.draw_rect(Rect2(middle+Vector2(-22,-27),Vector2(44,19)),Color("304950")*tint)
			for x in range(-18,20,5):canvas.draw_line(middle+Vector2(x,-24),middle+Vector2(x,-11),Color("9caeaa")*tint,2)
		if width>230:
			var sign_at:=b+Vector2(-56,-26)
			canvas.draw_rect(Rect2(sign_at,Vector2(39,15)),Color("29464e")*tint)
			canvas.draw_line(sign_at+Vector2(5,7),sign_at+Vector2(17,7),Color("cad0a9")*tint,2)
			canvas.draw_polyline(PackedVector2Array([sign_at+Vector2(12,3),sign_at+Vector2(17,7),sign_at+Vector2(12,11)]),Color("cad0a9")*tint,1.5)
			for x in [24,28,32]:canvas.draw_line(sign_at+Vector2(x,4),sign_at+Vector2(x,10),Color("93aaa1")*tint,1)
		# A short conduit and strapped elbow sit beside the window/vent bay.
		if width>180:
			canvas.draw_polyline(PackedVector2Array([a+Vector2(12,-9),a+Vector2(12,-23),a+Vector2(47,-23)]),Color("273e43")*tint,6)
			canvas.draw_polyline(PackedVector2Array([a+Vector2(12,-9),a+Vector2(12,-23),a+Vector2(47,-23)]),Color("a79872")*tint,3)
			for x in [22,40]:canvas.draw_line(a+Vector2(x,-27),a+Vector2(x,-19),Color("bac0a8")*tint,2)

static func _box(color: Color) -> StyleBoxFlat:
	var box:=StyleBoxFlat.new()
	box.bg_color=color
	box.set_corner_radius_all(3)
	return box

static func taper_face(a: Vector2, b: Vector2) -> PackedVector2Array:
	if absf(a.x-b.x)<=.1 or absf(a.y-b.y)<=.1:return PackedVector2Array()
	var lift:=Vector2(0,-35.0 if b.x>a.x else -18.0)
	return PackedVector2Array([a,b,b+lift,a+lift])
