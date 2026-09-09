extends RefCounted
## Flush, non-emissive floor pieces. Coordinates are native room units.
const GEO = preload("res://rooms/underwater/corridor_geometry.gd")
const SHAPES = ["straight","corner","tee","cross","dead_end"]
const JOINS = ["straight","corner","tee","cross"]
const UTILITIES = ["straight","bend","tee","cross","end_cap","equipment_entry"]
const DETAILS = ["tie_down","pipe_cap","inspection_plug","repair","damp","corrosion","access_hatch","standing_mat","teal_marking","service_marking","threshold"]
static var deck: Texture2D
static func polygon(shape: String) -> PackedVector2Array:
	if shape=="straight": return GEO.straight
	if shape=="corner": return GEO.elbow
	if shape=="tee": return GEO.junction
	if shape=="dead_end": return PackedVector2Array([Vector2(-192,-36),Vector2(-160,-48),Vector2(36,-48),Vector2(48,-36),Vector2(48,36),Vector2(36,48),Vector2(-160,48),Vector2(-192,36)])
	var result := GEO.junction
	var upper := PackedVector2Array([Vector2(-48,-48),Vector2(-48,-160),Vector2(-36,-192),Vector2(36,-192),Vector2(48,-160),Vector2(48,-48)])
	return Geometry2D.merge_polygons(result,upper)[0]
static func corridor(c: CanvasItem, shape: String, light := 1.0) -> void:
	if deck==null:
		var im:=Image.new()
		assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/floors-and-details-v5/corridor-deck.png"))==OK)
		deck=ImageTexture.create_from_image(im)
	var poly:=polygon(shape)
	var uv:=PackedVector2Array()
	for v in poly: uv.append((v+Vector2.ONE*192)/384)
	c.draw_polygon(poly,PackedColorArray([Color(light*.65,light*.65,light*.65)]),uv,deck)
	var outline:=poly.duplicate()
	outline.append(poly[0])
	c.draw_polyline(outline,Color(.12,.17,.17),1.0)
static func branches(shape: String, length: float) -> Array:
	var ends: Array=[Vector2(-length,0)]
	if shape not in ["end_cap","equipment_entry","dead_end"]: ends.append(Vector2(0,length) if shape in ["bend","corner"] else Vector2(length,0))
	if shape in ["tee","cross"]: ends.append(Vector2(0,length))
	if shape=="cross": ends.append(Vector2(0,-length))
	return ends
static func join(c: CanvasItem, shape: String) -> void:
	for end in branches(shape,48):
		c.draw_line(Vector2.ZERO,end,Color("202a2a"),4)
		c.draw_line(Vector2.ZERO,end,Color("626966"),1)
static func utility(c: CanvasItem, family: String, shape: String) -> void:
	for end in branches(shape,36):
		c.draw_line(Vector2.ZERO,end,Color("202929"),10)
		c.draw_line(Vector2.ZERO,end,Color("515b58"),7)
		var direction: Vector2=end.normalized()
		var side:=Vector2(-direction.y,direction.x)
		for n in range(4,35,6):
			var at:=direction*n
			c.draw_line(at-side*2.5,at+side*2.5,Color("293534"),1 if family=="drain" else .6)
	if shape=="equipment_entry": c.draw_rect(Rect2(-5,-8,10,16),Color("626a62"))
	if shape=="end_cap": c.draw_line(Vector2(0,-4),Vector2(0,4),Color("8a8467"),2)
static func detail(c: CanvasItem, kind: String) -> void:
	var metal:=Color("606a66")
	var dark:=Color("293533")
	if kind in ["tie_down","pipe_cap","inspection_plug"]:
		var radius:=5.0 if kind=="tie_down" else 8.0
		c.draw_circle(Vector2.ZERO,radius+1,dark)
		c.draw_circle(Vector2.ZERO,radius,metal)
		c.draw_arc(Vector2.ZERO,radius-2,0,TAU,20,dark,1)
		c.draw_line(Vector2(-3,0),Vector2(3,0),dark,2)
	elif kind in ["repair","access_hatch","standing_mat"]:
		var r:=Rect2(-30,-18,60,36)
		c.draw_rect(r,dark)
		c.draw_rect(r.grow(-2),Color("495651") if kind!="standing_mat" else Color("303b38"))
		if kind=="standing_mat":
			for y in range(-13,15,4): c.draw_line(Vector2(-26,y),Vector2(26,y),metal*.7,1)
		else:
			for v in [Vector2(-25,-13),Vector2(25,-13),Vector2(25,13),Vector2(-25,13)]: c.draw_circle(v,1,metal)
			if kind=="access_hatch": c.draw_rect(Rect2(-6,-2,12,4),dark)
	elif kind in ["teal_marking","service_marking"]:
		var ink:=Color("476b62") if kind=="teal_marking" else Color("88784f")
		for x in [-1,1]:
			for y in [-1,1]:
				var v:=Vector2(x*32,y*20)
				c.draw_line(v,v-Vector2(x*10,0),ink,2)
				c.draw_line(v,v-Vector2(0,y*8),ink,2)
	elif kind=="threshold":
		c.draw_rect(Rect2(-36,-4.5,72,9),dark)
		c.draw_rect(Rect2(-34,-3,68,6),metal)
		for x in range(-28,29,7): c.draw_line(Vector2(x,-2),Vector2(x,2),dark,1)
	elif kind=="damp":
		c.draw_colored_polygon(PackedVector2Array([Vector2(-30,-8),Vector2(-13,-15),Vector2(16,-9),Vector2(30,3),Vector2(11,12),Vector2(-21,9)]),Color(.12,.23,.21,.28))
	elif kind=="corrosion":
		for i in range(14): c.draw_circle(Vector2(-30+i*4,-12+sin(i*2.1)*2),.8+float(i%3)*.4,Color(.32,.24,.16,.38))
