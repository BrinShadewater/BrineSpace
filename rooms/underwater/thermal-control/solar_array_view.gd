extends "res://rooms/whole-room/life_support_view.gd"
## Immutable source silhouettes, shared hull, south-facing assemblies.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/thermal-control/solar_array-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"thermal_exchangers","rect":Rect2(-165,-143,108,64),"pivot":Vector2(312,553),"width":402.0,"outline":[Vector2(112,551),Vector2(111,394),Vector2(121,379),Vector2(121,254),Vector2(132,221),Vector2(158,213),Vector2(159,180),Vector2(179,154),Vector2(195,149),Vector2(195,132),Vector2(210,114),Vector2(399,114),Vector2(416,128),Vector2(422,151),Vector2(443,161),Vector2(462,186),Vector2(468,213),Vector2(494,223),Vector2(506,249),Vector2(509,379),Vector2(514,396),Vector2(513,551)]},
		{"id":"thermal_converter","rect":Rect2(-31,-143,108,64),"pivot":Vector2(903,532),"width":354.0,"outline":[Vector2(724,531),Vector2(724,456),Vector2(732,446),Vector2(731,330),Vector2(722,324),Vector2(724,307),Vector2(750,305),Vector2(751,237),Vector2(765,225),Vector2(764,158),Vector2(778,156),Vector2(778,148),Vector2(796,148),Vector2(799,157),Vector2(827,157),Vector2(832,150),Vector2(844,150),Vector2(846,156),Vector2(891,156),Vector2(893,149),Vector2(905,149),Vector2(909,156),Vector2(951,156),Vector2(956,148),Vector2(969,149),Vector2(970,156),Vector2(1008,156),Vector2(1010,222),Vector2(1016,222),Vector2(1017,199),Vector2(1051,199),Vector2(1061,215),Vector2(1062,306),Vector2(1073,316),Vector2(1077,527),Vector2(1031,531)]},
		{"id":"thermal_monitor","rect":Rect2(-165,79,108,64),"pivot":Vector2(321,1064),"width":370.0,"outline":[Vector2(134,931),Vector2(133,823),Vector2(143,800),Vector2(173,794),Vector2(176,750),Vector2(190,733),Vector2(465,731),Vector2(482,746),Vector2(484,815),Vector2(497,817),Vector2(505,833),Vector2(505,1048),Vector2(491,1064),Vector2(167,1064),Vector2(153,1049),Vector2(152,950)]},
		{"id":"thermal_pumps","rect":Rect2(57,79,108,64),"pivot":Vector2(889,1068),"width":422.0,"outline":[Vector2(676,1037),Vector2(678,1002),Vector2(683,815),Vector2(701,808),Vector2(707,776),Vector2(728,757),Vector2(749,750),Vector2(1028,750),Vector2(1053,767),Vector2(1066,792),Vector2(1068,815),Vector2(1088,815),Vector2(1095,841),Vector2(1098,1049),Vector2(1076,1067),Vector2(1027,1067),Vector2(1019,1057),Vector2(771,1057),Vector2(763,1068),Vector2(701,1068)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/thermal-control/thermal-composition-v2.json")
	rebuild()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("424546"),Color(0.12,0.14,0.15,0.4),2)
	RoomFloor.draw_dressing(painter,center,edges,"steel")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("282a29"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(240,34,142,58) if horizontal else Rect2(29,106,46,148))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(28,32,50,52))

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=4 # Canonical west/south corner, rotated by quarter.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func layout_caption() -> String:
	return "THERMAL POWER CONTROL / registered pilot / %d degrees"%(quarter*90)

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="thermal_monitor":
		for row in range(3):
			marks.append([Vector2(239,791+row*18),Vector2(283+24*sin(time*2+row),791+row*18)])
	elif prop.id=="thermal_converter":
		var y := 391+7*sin(time*2)
		marks.append([Vector2(1036,y),Vector2(1045,y)])
	return marks

func is_animated_prop(prop: Dictionary) -> bool:
	return prop.id in ["thermal_monitor","thermal_converter"]

func draw_piece(prop: Dictionary, outline: Array) -> void:
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,life_texture)
func rendered_pieces(prop: Dictionary) -> Array:
	if prop.id!="thermal_exchangers": return [prop.registration.outline]
	# Separate the overhead manifold, vessels and shared skid. The central
	# floor aperture is omitted without modifying the immutable source PNG.
	return [
		[Vector2(195,151),Vector2(195,132),Vector2(210,114),Vector2(399,114),Vector2(416,128),Vector2(422,151),Vector2(406,173),Vector2(393,169),Vector2(391,142),Vector2(228,142),Vector2(226,170),Vector2(205,174)],
		[Vector2(112,394),Vector2(121,379),Vector2(121,254),Vector2(132,221),Vector2(158,213),Vector2(159,180),Vector2(179,154),Vector2(195,149),Vector2(225,157),Vector2(249,155),Vector2(270,170),Vector2(272,141),Vector2(292,141),Vector2(292,351),Vector2(285,382),Vector2(278,440),Vector2(113,440)],
		[Vector2(330,141),Vector2(347,141),Vector2(347,174),Vector2(368,158),Vector2(393,152),Vector2(422,151),Vector2(443,161),Vector2(462,186),Vector2(468,213),Vector2(494,223),Vector2(506,249),Vector2(509,379),Vector2(514,396),Vector2(513,440),Vector2(346,440),Vector2(336,382),Vector2(330,351)],
		[Vector2(112,440),Vector2(275,440),Vector2(276,395),Vector2(294,387),Vector2(294,359),Vector2(327,359),Vector2(329,388),Vector2(345,400),Vector2(346,440),Vector2(513,440),Vector2(513,551),Vector2(112,551)]
	]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in rendered_pieces(prop): draw_piece(prop,outline)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("d9b36c"),1.15,true)
