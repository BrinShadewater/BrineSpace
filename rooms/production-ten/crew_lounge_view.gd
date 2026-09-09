extends "res://rooms/whole-room/life_support_view.gd"
## Habitation lounge; furnishings remain still, galley display indicates operation.
var support_texture: ImageTexture
var decor_texture: ImageTexture
var table_tray: Dictionary={}
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/crew_lounge-source-v2.png")) != OK: push_error("Failed to load image (rooms/production-ten/crew_lounge_view.gd:9)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"lounge_sofa","rect":Rect2(-165,-135,108,64),"pivot":Vector2(318,540),"width":386.0,"outline":[Vector2(125,149),Vector2(510,149),Vector2(510,540),Vector2(125,540)],"pieces":[[Vector2(125,179),Vector2(137,155),Vector2(419,156),Vector2(436,157),Vector2(433,180),Vector2(433,153),Vector2(461,149),Vector2(485,161),Vector2(482,189),Vector2(505,190),Vector2(510,206),Vector2(510,305),Vector2(497,324),Vector2(240,324),Vector2(239,515),Vector2(228,534),Vector2(136,534),Vector2(125,521)],[Vector2(253,337),Vector2(490,337),Vector2(490,540),Vector2(253,540)]]},
		{"id":"lounge_table","rect":Rect2(57,-135,108,64),"pivot":Vector2(921,565),"width":342.0,"outline":[Vector2(752,174),Vector2(1093,174),Vector2(1093,565),Vector2(752,565)],"pieces":[[Vector2(825,196),Vector2(844,178),Vector2(998,174),Vector2(1016,193),Vector2(1018,443),Vector2(1004,463),Vector2(1003,496),Vector2(957,504),Vector2(957,550),Vector2(946,565),Vector2(887,565),Vector2(882,550),Vector2(882,505),Vector2(840,499),Vector2(834,467),Vector2(824,450)],[Vector2(755,244),Vector2(766,235),Vector2(805,235),Vector2(817,244),Vector2(817,478),Vector2(805,488),Vector2(764,487),Vector2(752,476)],[Vector2(1030,244),Vector2(1040,236),Vector2(1078,235),Vector2(1090,245),Vector2(1093,478),Vector2(1080,488),Vector2(1039,486),Vector2(1027,476)]]},
		{"id":"lounge_galley","rect":Rect2(-165,79,108,64),"pivot":Vector2(296,1020),"width":348.0,"outline":[Vector2(125,719),Vector2(469,719),Vector2(469,1020),Vector2(125,1020)],"pieces":[[Vector2(125,788),Vector2(141,769),Vector2(145,769),Vector2(146,732),Vector2(157,719),Vector2(213,719),Vector2(225,732),Vector2(225,763),Vector2(378,763),Vector2(390,746),Vector2(409,735),Vector2(427,738),Vector2(447,752),Vector2(444,768),Vector2(458,773),Vector2(467,787),Vector2(469,1004),Vector2(454,1020),Vector2(140,1020),Vector2(126,1005)]]},
		{"id":"lounge_games","rect":Rect2(57,79,108,64),"pivot":Vector2(900,1050),"width":373.0,"outline":[Vector2(718,858),Vector2(1086,858),Vector2(1086,1049),Vector2(718,1049)],"pieces":[[Vector2(718,884),Vector2(729,873),Vector2(729,860),Vector2(815,858),Vector2(820,872),Vector2(831,883),Vector2(831,1035),Vector2(819,1049),Vector2(730,1048),Vector2(718,1034)],[Vector2(853,942),Vector2(863,930),Vector2(938,930),Vector2(949,941),Vector2(949,1015),Vector2(940,1024),Vector2(939,1042),Vector2(926,1048),Vector2(868,1047),Vector2(858,1038),Vector2(858,1022),Vector2(853,1015)],[Vector2(970,884),Vector2(979,873),Vector2(980,860),Vector2(1067,858),Vector2(1074,873),Vector2(1086,885),Vector2(1086,1035),Vector2(1074,1049),Vector2(983,1048),Vector2(970,1034)]]}
	]
	# Authored activity areas: reading nook, dining, refreshments and games.
	life_items[0].rect=Rect2(-165,-126,104,60)
	life_items[1].rect=Rect2(78,-112,84,56)
	life_items[2].rect=Rect2(-164,99,82,52)
	life_items[3].rect=Rect2(80,47,82,50)
	var decor_image := Image.new()
	if decor_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/decor/lounge-v1.png")) != OK: push_error("Failed to load image (rooms/production-ten/crew_lounge_view.gd:23)")
	decor_texture=ImageTexture.create_from_image(decor_image)
	life_items.append({"id":"decor_lounge_0","rect":Rect2(-132.5,32,25,6),"pivot":Vector2(361.0,499),"width":472.0,"outline":[Vector2(125,172),Vector2(597,172),Vector2(597,499),Vector2(125,499)],"pieces":[[Vector2(125,172),Vector2(597,172),Vector2(597,499),Vector2(125,499)]],"decor":true})
	life_items.append({"id":"decor_lounge_1","rect":Rect2(-79.0,32,22,6),"pivot":Vector2(934.5,512),"width":431.0,"outline":[Vector2(719,79),Vector2(1150,79),Vector2(1150,512),Vector2(719,512)],"pieces":[[Vector2(719,79),Vector2(1150,79),Vector2(1150,512),Vector2(719,512)]],"decor":true})
	life_items.append({"id":"decor_lounge_2","rect":Rect2(58.0,-38,24,6),"pivot":Vector2(319.0,1099),"width":434.0,"outline":[Vector2(102,676),Vector2(536,676),Vector2(536,1099),Vector2(102,1099)],"pieces":[[Vector2(102,676),Vector2(536,676),Vector2(536,1099),Vector2(102,1099)]],"decor":true})
	life_items.append({"id":"decor_lounge_3","rect":Rect2(110.0,-38,28,6),"pivot":Vector2(930.0,1110),"width":564.0,"outline":[Vector2(648,608),Vector2(1212,608),Vector2(1212,1110),Vector2(648,1110)],"pieces":[[Vector2(648,608),Vector2(1212,608),Vector2(1212,1110),Vector2(648,1110)]],"decor":true})

	# The tray belongs to the tabletop; it is drawn with the host, never collided.
	table_tray=life_items[6].duplicate(true)
	life_items.remove_at(6)
	life_items[4].rect=Rect2(-165,-41,24,8) # Basket beside reading nook.
	life_items[5].rect=Rect2(141,-48,25,9) # Plant at the dining area's edge.
	life_items.remove_at(6) # The coat stand now provides the bag's physical home.
	var support_image := Image.new()
	if support_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/decor/lounge-support-v2.png")) != OK: push_error("Failed to load image (rooms/production-ten/crew_lounge_view.gd:37)")
	support_texture=ImageTexture.create_from_image(support_image)
	append_support("reading_lamp",Rect2(-78,-57,23,8),Rect2(191,69,209,480))
	append_support("book_console",Rect2(-31,-145,62,23),Rect2(659,155,411,395))
	append_support("tea_trolley",Rect2(-83,61,38,16),Rect2(182,701,341,417))
	append_support("coat_stand",Rect2(149,66,18,9),Rect2(764,618,189,515))

	rebuild()

func append_support(id: String, rect: Rect2, source: Rect2) -> void:
	var outline := [source.position,Vector2(source.end.x,source.position.y),source.end,Vector2(source.position.x,source.end.y)]
	life_items.append({"id":id,"rect":rect,"pivot":Vector2(source.get_center().x,source.end.y),"width":source.size.x,"outline":outline,"pieces":[outline],"support":true})

func rebuild() -> void:
	super.rebuild()
	# Floor companions follow their activity area when furniture is wall-clamped.
	for index in range(4,mini(6,props.size())):
		var host: Dictionary=props[[0,1][index-4]]
		var prop: Dictionary=props[index]
		var offset: Vector2=[Vector2(22 if quarter==1 else -33,15),Vector2(33,20)][index-4]
		prop.rect.position=Vector2(host.rect.get_center().x,host.rect.end.y)+offset-prop.rect.size*0.5
		prop.sort_y=prop.rect.end.y
	# Supporting furniture has authored clearances for the fixed-facing sprites.
	# Rotation moves activity areas; these small adjustments preserve access after clamping.
	for prop in props:
		if prop.id=="reading_lamp" and quarter in [2,3]:
			prop.rect.position.x=(45.0 if quarter==2 else -166.0)-prop.rect.size.x*0.5
		if prop.id=="tea_trolley":
			var at: Vector2=[Vector2(-53,129),Vector2(-129,-42),Vector2(53,-110),Vector2(129,53)][quarter]
			prop.rect=Rect2(at-Vector2(22,9),Vector2(44,18))
		if prop.id=="coat_stand":
			var at: Vector2=[Vector2(170,146),Vector2(-137,142),Vector2(-171,-68),Vector2(170,-69)][quarter]
			prop.rect=Rect2(at-Vector2(9,4.5),Vector2(18,9))
		prop.sort_y=prop.rect.end.y
	layout[0].kind=0 # Canonical east/south/west tee.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("66665f"),Color(0.17,0.19,0.20,0.35),2,"warm")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"warm",false) # Rugs are anchored to seating below.

	# The lamp lead follows the furniture edge to an outlet on the sealed wall.
	for prop in props:
		if prop.id!="reading_lamp": continue
		var outlet := Geometry.turn(Vector2(-160,-176),quarter)
		var cable := PackedVector2Array([life_point(prop,Vector2(194,526)),Geometry.turn(Vector2(-169,-50),quarter),Geometry.turn(Vector2(-169,-168),quarter),outlet])
		if prop.get("relocated",false):
			var start := life_point(prop,Vector2(194,526))
			outlet=Vector2(start.x,-176 if not Geometry.has_port(layout[0],0) else 176)
			cable=PackedVector2Array([start,outlet])
		preload("res://rooms/whole-room/decoration_props.gd").service_run(painter,cable,2.0)
	# A localized pool of light belongs to the reading lamp, below all furniture.
	for prop in props:
		if prop.id=="reading_lamp" and operating:
			for radius in [29.0,23.0,17.0]:
				painter.draw_circle(prop.rect.get_center(),radius,Color(0.95,0.69,0.32,0.025))
	# A second textile groups the games seating without carpeting the aisle.
	for prop in props:
		if prop.id!="lounge_games": continue
		var pad := Rect2(prop.rect.position+Vector2(-5,8),prop.rect.size+Vector2(10,15))
		preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"oval_braided_rug",pad)
	# The reading nook retains its own warmer rug.
	for prop in props:
		if prop.id!="lounge_sofa": continue
		var rug := Rect2(prop.rect.position+Vector2(-3,12),prop.rect.size+Vector2(6,15))
		preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"woven_bedside_rug",rug)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(246,41,130,66) if horizontal else Rect2(43,220,43,137))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(45,43,45,44))

func effect_marks(prop: Dictionary,time: float) -> Array:
	if prop.id!="lounge_galley": return []
	var x := 177+sin(time*2)*4
	return [[Vector2(x,789),Vector2(x+5,789)]]
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="lounge_galley"

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.registration.get("support",false):
		var points := PackedVector2Array()
		var coords := PackedVector2Array()
		for point in prop.registration.outline:
			points.append(life_point(prop,point))
			coords.append(point/Vector2(support_texture.get_size()))
		painter.draw_polygon(points,PackedColorArray([Color.WHITE]),coords,support_texture)
		if operating and prop.id=="reading_lamp":
			painter.draw_circle(life_point(prop,Vector2(338,99)),1.7,Color("ffd698"))
		return
	if prop.registration.get("decor",false):
		var points := PackedVector2Array()
		var coords := PackedVector2Array()
		for p in prop.registration.outline:
			points.append(life_point(prop,p))
			coords.append(p/Vector2(decor_texture.get_size()))
		painter.draw_polygon(points,PackedColorArray([Color.WHITE]),coords,decor_texture)
		return
	for piece in prop.registration.pieces:
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in piece:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)
	if prop.id=="lounge_table" and not table_tray.is_empty():
		# Anchor in the source tabletop plane, inheriting its exact clamp and scale.
		var anchor := life_point(prop,Vector2(920,310))
		var tray := {"rect":Rect2(anchor-Vector2(9,4),Vector2(18,4)),"registration":table_tray}
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for point in table_tray.outline:
			vertices.append(life_point(tray,point))
			uv.append(point/Vector2(decor_texture.get_size()))
		painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,decor_texture)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("c6c397"),1.0,true)

