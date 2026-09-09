extends "res://rooms/whole-room/life_support_view.gd"
## Cultivated ecology: dry planters and a separately contained aquatic system.
var processor_render_pieces: Array=[]
var tree_render_pieces: Array=[]
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func _ready() -> void:
	super._ready()
	var image:=Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/batch-two/biodome-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"biodome_tree","rect":Rect2(-159,-149,94,74),"pivot":Vector2(322,536),"width":294.0,"outline":[Vector2(179,274),Vector2(191,255),Vector2(207,246),Vector2(214,235),Vector2(212,226),Vector2(230,226),Vector2(211,215),Vector2(218,204),Vector2(232,200),Vector2(225,184),Vector2(244,182),Vector2(255,191),Vector2(259,180),Vector2(274,175),Vector2(280,191),Vector2(287,171),Vector2(302,160),Vector2(306,178),Vector2(329,173),Vector2(340,181),Vector2(331,195),Vector2(329,196),Vector2(331,198),Vector2(334,200),Vector2(339,202),Vector2(344,204),Vector2(343,198),Vector2(343,190),Vector2(344,185),Vector2(347,182),Vector2(352,184),Vector2(365,188),Vector2(369,201),Vector2(377,191),Vector2(395,190),Vector2(394,208),Vector2(410,208),Vector2(422,217),Vector2(409,228),Vector2(417,243),Vector2(442,242),Vector2(457,252),Vector2(468,269),Vector2(468,510),Vector2(456,526),Vector2(438,536),Vector2(199,536),Vector2(178,517)]},
		{"id":"biodome_ferns","rect":Rect2(51,-121,106,76),"pivot":Vector2(908,541),"width":336.0,"outline":[Vector2(744,274),Vector2(755,258),Vector2(778,250),Vector2(811,252),Vector2(814,248),Vector2(814,243),Vector2(817,239),Vector2(817,236),Vector2(820,232),Vector2(823,228),Vector2(826,224),Vector2(830,220),Vector2(834,218),Vector2(846,216),Vector2(848,225),Vector2(841,249),Vector2(858,237),Vector2(882,232),Vector2(888,239),Vector2(873,249),Vector2(916,249),Vector2(918,242),Vector2(934,248),Vector2(957,249),Vector2(955,234),Vector2(960,214),Vector2(972,218),Vector2(989,246),Vector2(1008,245),Vector2(1019,236),Vector2(1032,239),Vector2(1038,247),Vector2(1030,255),Vector2(1057,261),Vector2(1068,273),Vector2(1073,292),Vector2(1073,331),Vector2(1080,346),Vector2(1074,351),Vector2(1075,513),Vector2(1061,531),Vector2(1045,541),Vector2(770,541),Vector2(745,523)]},
		{"id":"biodome_aquatic","rect":Rect2(-158,72,96,66),"pivot":Vector2(316,1039),"width":296.0,"outline":[Vector2(170,781),Vector2(182,759),Vector2(201,746),Vector2(282,746),Vector2(282,735),Vector2(296,724),Vector2(320,724),Vector2(337,735),Vector2(337,746),Vector2(422,746),Vector2(446,757),Vector2(461,779),Vector2(463,1018),Vector2(448,1034),Vector2(429,1039),Vector2(190,1039),Vector2(170,1020)]},
		{"id":"biodome_processor","rect":Rect2(58,74,108,80),"pivot":Vector2(905,1039),"width":372.0,"outline":[Vector2(722,779),Vector2(730,762),Vector2(738,758),Vector2(738,725),Vector2(750,705),Vector2(772,691),Vector2(795,686),Vector2(818,687),Vector2(844,698),Vector2(860,716),Vector2(870,740),Vector2(870,752),Vector2(881,761),Vector2(888,779),Vector2(889,841),Vector2(895,841),Vector2(895,720),Vector2(905,705),Vector2(922,702),Vector2(1074,702),Vector2(1089,714),Vector2(1092,1014),Vector2(1080,1031),Vector2(1063,1039),Vector2(746,1039),Vector2(722,1021)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/biodome-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1 # Canonical north/south straight, not source-image topology.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("a9b2a8"),Color(0.23,0.32,0.25,0.14),2,"wet")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"wet")
	if dressing!=null: dressing.floor()
	_draw_care_chart(center)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("243a2c"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(245,49,135,42) if horizontal else Rect2(50,130,39,90))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("e0e3d7"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("243a2c"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(51,47,41,42))

func effect_region(prop: Dictionary) -> Rect2:
	# Source-space operating envelopes: irrigation belongs to beds; circulation
	# belongs to contained water, never to the room floor or unrelated machinery.
	match prop.id:
		"biodome_tree": return Rect2(235,350,170,55)
		"biodome_ferns": return Rect2(777,366,244,70)
		"biodome_aquatic": return Rect2(206,810,218,90)
		"biodome_processor": return Rect2(756,799,94,94)
	return Rect2()

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"biodome_tree":
			for i in range(4):
				var p:=Vector2(246+i*49,355+fposmod(time*18+i*7,27))
				marks.append([p,p+Vector2(0,4)])
		"biodome_ferns":
			for i in range(5):
				var p:=Vector2(786+i*55,376+fposmod(time*18+i*7,37))
				marks.append([p,p+Vector2(0,4)])
		"biodome_aquatic":
			for i in range(4):
				var p:=Vector2(219+i*57,885-fposmod(time*20+i*11,60))
				marks.append([p,p+Vector2(0,4)])
		"biodome_processor":
			for i in range(3):
				var p:=Vector2(772+i*31,879-fposmod(time*22+i*17,75))
				marks.append([p,p+Vector2(0,4)])
	return marks

func render_polygons(prop: Dictionary) -> Array:
	var outline:=PackedVector2Array(prop.registration.outline)
	if prop.id=="biodome_tree":
		if tree_render_pieces.is_empty():
			# Two source-floor windows between leaves, not the brown branches below.
			# Split through both windows before subtraction: draw_polygon cannot
			# represent an enclosed inner ring in one polygon.
			var size:=Vector2(life_texture.get_size())
			for region in [Rect2(0,0,size.x,230),Rect2(0,230,size.x,size.y-230)]:
				var rect: Rect2=region
				var clip:=PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
				tree_render_pieces.append_array(Geometry2D.intersect_polygons(outline,clip))
			for gap in tree_canopy_gaps():
				var remaining: Array=[]
				for piece in tree_render_pieces: remaining.append_array(Geometry2D.clip_polygons(piece,gap))
				tree_render_pieces=remaining
		return tree_render_pieces
	if prop.id!="biodome_processor": return [outline]
	if processor_render_pieces.is_empty():
		# Source floor visible between the tank and its right return pipe.
		# Partition around the opening: no background-colored cover or fake hole.
		var gap:=Rect2(866,780,7,38)
		var size:=Vector2(life_texture.get_size())
		for region in [Rect2(0,0,size.x,gap.position.y),Rect2(0,gap.end.y,size.x,size.y-gap.end.y),Rect2(0,gap.position.y,gap.position.x,gap.size.y),Rect2(gap.end.x,gap.position.y,size.x-gap.end.x,gap.size.y)]:
			var rect: Rect2=region
			var clip:=PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
			processor_render_pieces.append_array(Geometry2D.intersect_polygons(outline,clip))
	return processor_render_pieces

func tree_canopy_gaps() -> Array:
	return [
		PackedVector2Array([Vector2(320,221),Vector2(323,224),Vector2(327,225),Vector2(329,227),Vector2(328,230),Vector2(324,232),Vector2(319,234),Vector2(320,230)]),
		PackedVector2Array([Vector2(332,227),Vector2(335,228),Vector2(338,228),Vector2(339,229),Vector2(338,231),Vector2(337,232),Vector2(337,235),Vector2(333,235),Vector2(333,232)])
	]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in render_polygons(prop):
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("b9d5c4"),0.85,true)

func layout_caption() -> String:
	return "BIODOME / south-facing ecology / %d degrees"%(quarter*90)

func _draw_care_chart(center: Vector2) -> void:
	# Attached to the north hull, including when the station owns a shared wall.
	# Mount spans x=-66..-38, outside the canonical 72-unit door bay.
	var at:=center+Vector2(-52,-182)
	painter.draw_line(at+Vector2(-8,-5),at+Vector2(-8,2),Color("56665e"),2)
	painter.draw_line(at+Vector2(8,-5),at+Vector2(8,2),Color("56665e"),2)
	painter.draw_rect(Rect2(at-Vector2(14,0),Vector2(28,22)),Color("53675c"))
	painter.draw_rect(Rect2(at-Vector2(12,-2),Vector2(24,18)),Color("d5d8be"))
	painter.draw_rect(Rect2(at+Vector2(-8,3),Vector2(16,3)),Color("54705b"))
	for row in range(3):
		painter.draw_rect(Rect2(at+Vector2(-8,8+row*3),Vector2(2,2)),Color("73816a"))
		painter.draw_line(at+Vector2(-3,9+row*3),at+Vector2(8,9+row*3),Color("89917c"),1)
