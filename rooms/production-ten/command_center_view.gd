extends "res://rooms/whole-room/life_support_view.gd"
## Underwater operations consoles with host-local sonar and system displays.
const FLOOR_CUTOUTS = {
	"command_ops":[[Vector2(565,150),Vector2(553,146),Vector2(538,130),Vector2(194,130),Vector2(192,140),Vector2(154,146),Vector2(138,159),Vector2(137.818,160),Vector2(183,160),Vector2(567,160)],[Vector2(567,160),Vector2(183,160),Vector2(183.75,166),Vector2(568.2,166)],[Vector2(136.727,166),Vector2(165,166),Vector2(183,160),Vector2(137.818,160)],[Vector2(570,175),Vector2(568.2,166),Vector2(183.75,166),Vector2(185,176),Vector2(570.895,176)],[Vector2(134.909,176),Vector2(158.684,176),Vector2(165,166),Vector2(136.727,166)],[Vector2(570.895,176),Vector2(185,176),Vector2(172,185),Vector2(578.947,185)],[Vector2(133.273,185),Vector2(153,185),Vector2(158.684,176),Vector2(134.909,176)],[Vector2(587,194),Vector2(578.947,185),Vector2(172,185),Vector2(170,248),Vector2(589.455,248)],[Vector2(132,192),Vector2(127,222),Vector2(128.106,248),Vector2(151.031,248),Vector2(153,185),Vector2(133.273,185)],[Vector2(589.455,248),Vector2(170,248),Vector2(170.517,249),Vector2(589.5,249)],[Vector2(128.149,249),Vector2(151,249),Vector2(151.031,248),Vector2(128.106,248)],[Vector2(590,260),Vector2(589.5,249),Vector2(170.517,249),Vector2(181.897,271),Vector2(589.2,271)],[Vector2(129,269),Vector2(129.158,271),Vector2(160,271),Vector2(151,249),Vector2(128.149,249)],[Vector2(589.2,271),Vector2(181.897,271),Vector2(185,277),Vector2(588.764,277)],[Vector2(129.632,277),Vector2(166.3,277),Vector2(160,271),Vector2(129.158,271)],[Vector2(588.764,277),Vector2(185,277),Vector2(181,291),Vector2(587.745,291)],[Vector2(130.737,291),Vector2(181,291),Vector2(166.3,277),Vector2(129.632,277)],[Vector2(146,487),Vector2(176,497),Vector2(208,489),Vector2(226,475),Vector2(239,478),Vector2(239,513),Vector2(251,525),Vector2(499,524),Vector2(513,500),Vector2(577,498),Vector2(590,482),Vector2(590,333),Vector2(586,315),Vector2(587.745,291),Vector2(181,291),Vector2(130.737,291),Vector2(132,307),Vector2(124,321),Vector2(129,467)]],
	"command_table":[[Vector2(474,746),Vector2(432,745),Vector2(422.714,750),Vector2(478,750)],[Vector2(409,742),Vector2(392,741),Vector2(387.091,750),Vector2(417,750)],[Vector2(370,740),Vector2(303,739),Vector2(299,746),Vector2(270,745),Vector2(257.5,750),Vector2(376.667,750)],[Vector2(232,733),Vector2(208,724),Vector2(183,730),Vector2(154,746),Vector2(151.714,750),Vector2(183,750),Vector2(240.13,750)],[Vector2(478,750),Vector2(422.714,750),Vector2(420.857,751),Vector2(479,751)],[Vector2(417,750),Vector2(387.091,750),Vector2(386.545,751),Vector2(418,751)],[Vector2(376.667,750),Vector2(257.5,750),Vector2(255,751),Vector2(377.333,751)],[Vector2(240.13,750),Vector2(183,750),Vector2(216,751),Vector2(240.609,751)],[Vector2(151.143,751),Vector2(181.722,751),Vector2(183,750),Vector2(151.714,750)],[Vector2(487,759),Vector2(479,751),Vector2(420.857,751),Vector2(419,752),Vector2(418,751),Vector2(386.545,751),Vector2(386,752),Vector2(378,752),Vector2(377.333,751),Vector2(255,751),Vector2(243,756),Vector2(240.609,751),Vector2(216,751),Vector2(225,761),Vector2(487.095,761)],[Vector2(145.429,761),Vector2(168.944,761),Vector2(181.722,751),Vector2(151.143,751)],[Vector2(487.095,761),Vector2(225,761),Vector2(192,765),Vector2(487.286,765)],[Vector2(143.143,765),Vector2(163.833,765),Vector2(168.944,761),Vector2(145.429,761)],[Vector2(487.286,765),Vector2(192,765),Vector2(188.357,768),Vector2(487.429,768)],[Vector2(141.429,768),Vector2(160,768),Vector2(163.833,765),Vector2(143.143,765)],[Vector2(487.429,768),Vector2(188.357,768),Vector2(175,779),Vector2(487.952,779)],[Vector2(138,774),Vector2(137.196,779),Vector2(154.5,779),Vector2(160,768),Vector2(141.429,768)],[Vector2(516,780),Vector2(488,780),Vector2(487.952,779),Vector2(175,779),Vector2(173.632,792),Vector2(528,792)],[Vector2(135.107,792),Vector2(148,792),Vector2(154.5,779),Vector2(137.196,779)],[Vector2(536,800),Vector2(528,792),Vector2(173.632,792),Vector2(171,817),Vector2(536.39,817)],[Vector2(131.089,817),Vector2(150.885,817),Vector2(148,792),Vector2(135.107,792)],[Vector2(536.39,817),Vector2(171,817),Vector2(151,818),Vector2(536.413,818)],[Vector2(130.929,818),Vector2(151,818),Vector2(150.885,817),Vector2(131.089,817)],[Vector2(133,979),Vector2(137.576,1006),Vector2(154,1006),Vector2(540.725,1006),Vector2(536.413,818),Vector2(151,818),Vector2(130.929,818),Vector2(129,830),Vector2(124,913),Vector2(123,974)],[Vector2(139.61,1018),Vector2(158.125,1018),Vector2(154,1006),Vector2(137.576,1006)],[Vector2(540.725,1006),Vector2(154,1006),Vector2(162.571,1018),Vector2(205,1018),Vector2(541,1018)],[Vector2(139.78,1019),Vector2(158.469,1019),Vector2(158.125,1018),Vector2(139.61,1018)],[Vector2(541,1018),Vector2(205,1018),Vector2(216,1019),Vector2(540.591,1019)],[Vector2(163.286,1019),Vector2(204.417,1019),Vector2(205,1018),Vector2(162.571,1018)],[Vector2(141.136,1027),Vector2(161.219,1027),Vector2(158.469,1019),Vector2(139.78,1019)],[Vector2(540.591,1019),Vector2(216,1019),Vector2(213.2,1027),Vector2(537.318,1027)],[Vector2(169,1027),Vector2(199.75,1027),Vector2(204.417,1019),Vector2(163.286,1019)],[Vector2(141.644,1030),Vector2(162.25,1030),Vector2(161.219,1027),Vector2(141.136,1027)],[Vector2(537.318,1027),Vector2(213.2,1027),Vector2(212.15,1030),Vector2(536.091,1030)],[Vector2(198,1030),Vector2(199.75,1027),Vector2(169,1027)],[Vector2(143,1038),Vector2(165,1038),Vector2(162.25,1030),Vector2(141.644,1030)],[Vector2(536.091,1030),Vector2(212.15,1030),Vector2(209.35,1038),Vector2(532.818,1038)],[Vector2(143.556,1039),Vector2(168.714,1039),Vector2(165,1038),Vector2(143,1038)],[Vector2(532.818,1038),Vector2(209.35,1038),Vector2(209,1039),Vector2(532.409,1039)],[Vector2(146.889,1045),Vector2(191,1045),Vector2(168.714,1039),Vector2(143.556,1039)],[Vector2(532,1040),Vector2(532.409,1039),Vector2(209,1039),Vector2(191,1045),Vector2(527.37,1045)],[Vector2(153,1056),Vector2(173,1064),Vector2(203,1064),Vector2(220,1058),Vector2(238,1069),Vector2(507,1067),Vector2(527.37,1045),Vector2(191,1045),Vector2(146.889,1045)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/command_center-source-v2.png")) != OK: push_error("Failed to load image (rooms/production-ten/command_center_view.gd:12)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"command_ops","rect":Rect2(-160,-78,72,42),"pivot":Vector2(355,525),"width":469.0,"outline":[Vector2(124,321),Vector2(132,307),Vector2(129,269),Vector2(127,222),Vector2(132,192),Vector2(138,159),Vector2(154,146),Vector2(192,140),Vector2(194,130),Vector2(538,130),Vector2(553,146),Vector2(565,150),Vector2(570,175),Vector2(587,194),Vector2(590,260),Vector2(586,315),Vector2(590,333),Vector2(590,482),Vector2(577,498),Vector2(513,500),Vector2(499,524),Vector2(251,525),Vector2(239,513),Vector2(239,478),Vector2(226,475),Vector2(208,489),Vector2(176,497),Vector2(146,487),Vector2(129,467)]},
		{"id":"command_systems","rect":Rect2(-158,-145,80,40),"pivot":Vector2(933,491),"width":387.0,"outline":[Vector2(741,277),Vector2(746,266),Vector2(746,222),Vector2(758,209),Vector2(768,204),Vector2(771,191),Vector2(800,190),Vector2(810,165),Vector2(810,128),Vector2(820,125),Vector2(824,181),Vector2(1043,181),Vector2(1055,192),Vector2(1066,211),Vector2(1079,197),Vector2(1086,181),Vector2(1087,158),Vector2(1095,155),Vector2(1098,197),Vector2(1111,209),Vector2(1121,231),Vector2(1124,270),Vector2(1120,406),Vector2(1111,433),Vector2(1094,457),Vector2(1064,465),Vector2(1054,485),Vector2(1043,491),Vector2(847,489),Vector2(837,478),Vector2(792,478),Vector2(767,465),Vector2(749,442),Vector2(738,418)]},
		{"id":"command_table","rect":Rect2(-145,80,114,66),"pivot":Vector2(333,1069),"width":421.0,"outline":[Vector2(124,913),Vector2(129,830),Vector2(138,774),Vector2(154,746),Vector2(183,730),Vector2(208,724),Vector2(232,733),Vector2(243,756),Vector2(255,751),Vector2(270,745),Vector2(299,746),Vector2(303,739),Vector2(370,740),Vector2(378,752),Vector2(386,752),Vector2(392,741),Vector2(409,742),Vector2(419,752),Vector2(432,745),Vector2(474,746),Vector2(487,759),Vector2(488,780),Vector2(516,780),Vector2(536,800),Vector2(541,1018),Vector2(532,1040),Vector2(507,1067),Vector2(238,1069),Vector2(220,1058),Vector2(203,1064),Vector2(173,1064),Vector2(153,1056),Vector2(143,1038),Vector2(133,979),Vector2(123,974)]},
		{"id":"command_comms","rect":Rect2(64,-120,96,58),"pivot":Vector2(933,1040),"width":408.0,"outline":[Vector2(731,862),Vector2(741,846),Vector2(751,845),Vector2(753,809),Vector2(765,800),Vector2(777,785),Vector2(800,784),Vector2(803,768),Vector2(815,762),Vector2(971,762),Vector2(978,766),Vector2(1007,762),Vector2(1017,741),Vector2(1074,737),Vector2(1078,680),Vector2(1085,677),Vector2(1090,737),Vector2(1100,746),Vector2(1108,786),Vector2(1122,813),Vector2(1138,841),Vector2(1138,884),Vector2(1126,903),Vector2(1122,970),Vector2(1109,996),Vector2(1087,1008),Vector2(1077,1027),Vector2(1063,1039),Vector2(762,1038),Vector2(732,1008)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/command-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=2 # Canonical cross.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	for prop in props:
		if prop.id=="command_systems":
			var centers := [Vector2(-118,-125),Vector2(138,-124),Vector2(118,140),Vector2(-138,124)]
			prop.rect.position=centers[quarter]-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("525c60"),Color(0.17,0.19,0.20,0.35),2,"technical")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"technical")
	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").identity_details(painter,props,"command",operating)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(263,54,101,45) if horizontal else Rect2(70,236,35,103))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(70,57,38,38))

func screen_rect(prop: Dictionary) -> Rect2:
	match prop.id:
		"command_ops": return Rect2(218,171,297,105)
		"command_systems": return Rect2(872,218,145, 70)
		"command_table": return Rect2(248,823,231,119)
	return Rect2(824,795,121,69)

func effect_marks(prop: Dictionary,time: float) -> Array:
	if prop.registration.get("dressing",false): return []
	var screen := screen_rect(prop)
	var marks: Array=[]
	if prop.id in ["command_ops","command_table"]:
		# Sonar sweep remains entirely on the physical display.
		var center := screen.get_center()
		var radius := screen.size.y*0.40
		marks.append([center,center+Vector2(cos(time*1.4),sin(time*1.4))*radius])
		for segment in range(24):
			var a := TAU*segment/24.0
			var b := TAU*(segment+1)/24.0
			marks.append([center+Vector2(cos(a),sin(a))*radius,center+Vector2(cos(b),sin(b))*radius])
	else:
		for row in range(3):
			var start := screen.position+Vector2(9,12+row*15)
			marks.append([start,start+Vector2(25+18*sin(time*2+row),0)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in FLOOR_CUTOUTS.get(prop.id,[prop.registration.outline]):
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)

	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("90bec6"),1.0,true)
