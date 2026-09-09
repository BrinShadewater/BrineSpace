extends "res://rooms/whole-room/life_support_view.gd"
## Science host with localized containment instrumentation, not purple architecture.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func _ready() -> void:
	super._ready()
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://assets/material-polish-xeno-v1/xeno-equipment.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"xeno_vessel","rect":Rect2(-39,-141,78,72),"pivot":Vector2(314,499),"width":260.0,"outline":[Vector2(184,341),Vector2(192,326),Vector2(206,319),Vector2(209,305),Vector2(222,293),Vector2(222,174),Vector2(231,151),Vector2(246,137),Vector2(267,128),Vector2(291,119),Vector2(331,118),Vector2(358,128),Vector2(379,139),Vector2(395,158),Vector2(403,178),Vector2(403,292),Vector2(416,302),Vector2(424,320),Vector2(437,330),Vector2(442,344),Vector2(443,486),Vector2(432,498),Vector2(196,499),Vector2(184,487)]},
		{"id":"xeno_scanner","rect":Rect2(60,-24,106,70),"pivot":Vector2(926,450),"width":342.0,"outline":[Vector2(757,232),Vector2(766,218),Vector2(774,218),Vector2(776,209),Vector2(800,184),Vector2(1028,184),Vector2(1036,175),Vector2(1071,175),Vector2(1082,186),Vector2(1095,195),Vector2(1099,431),Vector2(1086,449),Vector2(765,450),Vector2(756,438)]},
		{"id":"xeno_samples","rect":Rect2(-160,67,94,68),"pivot":Vector2(316,1014),"width":290.0,"outline":[Vector2(187,742),Vector2(439,742),Vector2(445,754),Vector2(445,877),Vector2(456,887),Vector2(460,1004),Vector2(449,1014),Vector2(183,1014),Vector2(172,1003),Vector2(171,889),Vector2(182,878),Vector2(185,752)]},
		{"id":"xeno_workbench","rect":Rect2(66,84,94,70),"pivot":Vector2(909,1010),"width":258.0,"outline":[Vector2(781,826),Vector2(790,809),Vector2(800,796),Vector2(813,796),Vector2(814,774),Vector2(905,774),Vector2(910,783),Vector2(910,799),Vector2(926,799),Vector2(930,787),Vector2(947,780),Vector2(974,758),Vector2(977,749),Vector2(990,741),Vector2(1004,747),Vector2(1012,759),Vector2(1011,780),Vector2(1006,790),Vector2(1006,804),Vector2(1025,814),Vector2(1037,831),Vector2(1037,992),Vector2(1024,1010),Vector2(797,1010),Vector2(781,995)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/xeno-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=3 # One south socket. Generated tee shell is rejected.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("a4b0ba"),Color(0.22,0.30,0.39,0.15),2,"sealed")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"sealed")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("2a3a51"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(257,45,120,31) if horizontal else Rect2(74,88,31,120))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("d5dce1"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("2a3a51"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(75,45,34,32))

func display_regions(prop: Dictionary) -> Array:
	if prop.id!="xeno_vessel": return []
	return [Rect2(294,205,40,41),Rect2(224,201,14,24),Rect2(386,200,15,24),Rect2(288,431,49,12),Rect2(211,447,16,16),Rect2(400,446,16,17),Rect2(290,198,7,7),Rect2(225,303,7,16),Rect2(394,308,7,13),Rect2(212,423,8,8)]

func display_polygon(rect: Rect2,index: int) -> PackedVector2Array:
	if index!=0: return PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
	var points:=PackedVector2Array()
	for i in range(32): points.append(rect.get_center()+Vector2(cos(i*TAU/32)*rect.size.x/2,sin(i*TAU/32)*rect.size.y/2))
	return points

func effect_region(prop: Dictionary) -> Rect2:
	match prop.id:
		"xeno_vessel": return Rect2(272,286,74,104)
		"xeno_scanner": return Rect2(943,277,79,64)
		"xeno_samples": return Rect2(206,846,211,104)
		"xeno_workbench": return Rect2(850,855,72,45)
	return Rect2()

func lamp_aperture(index: int) -> PackedVector2Array:
	# Lens faces only; preserve the surrounding curved/angled source housings.
	match index:
		1: return PackedVector2Array([Vector2(228,202),Vector2(235,202),Vector2(237,206),Vector2(237,218),Vector2(234,222),Vector2(228,222),Vector2(225,218),Vector2(225,207)])
		2: return PackedVector2Array([Vector2(390,201),Vector2(397,201),Vector2(400,206),Vector2(400,218),Vector2(397,222),Vector2(390,222),Vector2(387,218),Vector2(387,206)])
		3: return PackedVector2Array([Vector2(289,433),Vector2(335,433),Vector2(335,438),Vector2(331,441),Vector2(294,441),Vector2(289,438)])
		4: return PackedVector2Array([Vector2(213,449),Vector2(224,453),Vector2(224,462),Vector2(213,457)])
		5: return PackedVector2Array([Vector2(402,452),Vector2(414,448),Vector2(414,456),Vector2(402,462)])
	return PackedVector2Array()

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"xeno_vessel":
			var y:=332+sin(time*1.3)*24
			marks.append([Vector2(277,y),Vector2(338,y)])
		"xeno_scanner":
			for row in range(3): marks.append([Vector2(948,286+row*17),Vector2(986+sin(time*1.9+row)*22,286+row*17)])
		"xeno_samples":
			for row in range(2):
				for column in range(3):
					var x:=217+column*85
					var y:=860+row*66+sin(time*1.2+column)*7
					marks.append([Vector2(x,y),Vector2(x+17,y)])
		"xeno_workbench":
			var x:=882+sin(time*1.8)*20
			marks.append([Vector2(x,863),Vector2(x,891)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	if prop.id=="xeno_workbench":
		# Only the nearly-white lens; keep the surrounding source bezel intact.
		var lens_vertices:=PackedVector2Array()
		var lens_uv:=PackedVector2Array()
		for point in [Vector2(951,929),Vector2(999,929),Vector2(999,935),Vector2(951,935)]:
			lens_vertices.append(life_point(prop,point))
			lens_uv.append(point/Vector2(life_texture.get_size()))
		var value:=0.85 if operating else 0.24
		painter.draw_polygon(lens_vertices,PackedColorArray([Color(value,value,value)]),lens_uv,life_texture)
	var regions:=display_regions(prop)
	for i in range(regions.size()):
		var points:=PackedVector2Array()
		var surface_uv:=PackedVector2Array()
		for p in display_polygon(regions[i],i):
			points.append(life_point(prop,p))
			surface_uv.append(p/Vector2(life_texture.get_size()))
		if i==0:
			# Optical depth is static material; the source's bright points are not.
			painter.draw_colored_polygon(points,Color("161b25"))
			for inset in [3.0,6.0]:
				var glass:=PackedVector2Array()
				for p in display_polygon(regions[i].grow(-inset),0): glass.append(life_point(prop,p))
				painter.draw_colored_polygon(glass,Color("222935") if inset==3.0 else Color("1b212d"))
		else:
			# Retain inset housing and bevel texture while neutralizing violet lamps.
			# This is local material modulation, not a complete emissive extraction.
			painter.draw_polygon(points,PackedColorArray([Color(0.62,0.70,0.48)]),surface_uv,life_texture)
			var aperture:=lamp_aperture(i)
			if not aperture.is_empty():
				var lens:=PackedVector2Array()
				for p in aperture: lens.append(life_point(prop,p))
				painter.draw_colored_polygon(lens,Color("121b25"))
				for depth in [1.3,2.6]:
					for inset in Geometry2D.offset_polygon(aperture,-depth):
						var inner:=PackedVector2Array()
						for p in inset: inner.append(life_point(prop,p))
						painter.draw_colored_polygon(inner,Color("273442") if depth==1.3 else Color("1b2632"))
	if not operating: return
	if prop.id=="xeno_vessel":
		painter.draw_circle(life_point(prop,Vector2(314,225)),1.35,Color("aa8bcc"))
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("aa91c4") if prop.id=="xeno_vessel" else Color("a1bfc9"),0.95,true)

func layout_caption() -> String:
	return "XENO LAB / south-facing instrumentation / %d degrees"%(quarter*90)
