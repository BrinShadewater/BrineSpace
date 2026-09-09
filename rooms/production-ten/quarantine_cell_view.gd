extends "res://rooms/whole-room/life_support_view.gd"
## Isolated berth, dedicated filtration, observation console and protective gear.
const FLOOR_CUTOUTS = {
	"quarantine_berth":[[Vector2(532,147),Vector2(524,130),Vector2(507,125),Vector2(493,100),Vector2(217,100),Vector2(199,105),Vector2(180,144),Vector2(177,175),Vector2(145,177),Vector2(135,191),Vector2(135,201),Vector2(163,201),Vector2(531.349,201)],[Vector2(531.349,201),Vector2(163,201),Vector2(163,204),Vector2(531.313,204)],[Vector2(135,204),Vector2(149,204),Vector2(163,201),Vector2(135,201)],[Vector2(531.313,204),Vector2(163,204),Vector2(163,229),Vector2(531.012,229)],[Vector2(135,229),Vector2(150.163,229),Vector2(149,204),Vector2(135,204)],[Vector2(548,238),Vector2(531,230),Vector2(531.012,229),Vector2(163,229),Vector2(151,247),Vector2(550.812,247)],[Vector2(135,233),Vector2(128,247),Vector2(151,247),Vector2(150.163,229),Vector2(135,229)],[Vector2(550.812,247),Vector2(151,247),Vector2(128,247),Vector2(128.008,249),Vector2(163,249),Vector2(551.438,249)],[Vector2(551.438,249),Vector2(163,249),Vector2(163,266),Vector2(556.75,266)],[Vector2(128.075,266),Vector2(151,266),Vector2(163,249),Vector2(128.008,249)],[Vector2(558,270),Vector2(556.75,266),Vector2(163,266),Vector2(163,374),Vector2(558,374)],[Vector2(128.504,374),Vector2(150,374),Vector2(151,266),Vector2(128.075,266)],[Vector2(558,374),Vector2(163,374),Vector2(150,374),Vector2(128.504,374),Vector2(128.603,399),Vector2(149,399),Vector2(163,399),Vector2(558,399)],[Vector2(542,440),Vector2(558,421),Vector2(558,399),Vector2(163,399),Vector2(163,475),Vector2(535,475)],[Vector2(128.905,475),Vector2(149,475),Vector2(149,399),Vector2(128.603,399)],[Vector2(535,475),Vector2(163,475),Vector2(163,479),Vector2(534.2,479)],[Vector2(128.921,479),Vector2(151,479),Vector2(149,475),Vector2(128.905,475)],[Vector2(534.2,479),Vector2(163,479),Vector2(154,485),Vector2(533,485)],[Vector2(128.944,485),Vector2(154,485),Vector2(151,479),Vector2(128.921,479)],[Vector2(148,513),Vector2(190,511),Vector2(202,498),Vector2(521,499),Vector2(533,485),Vector2(154,485),Vector2(128.944,485),Vector2(129,499)]],
	"quarantine_monitor":[[Vector2(515,802),Vector2(504,788),Vector2(448,788),Vector2(448,770),Vector2(430,751),Vector2(251,751),Vector2(245,736),Vector2(216,734),Vector2(203,740),Vector2(202,786),Vector2(192,796),Vector2(179,822),Vector2(137,830),Vector2(125,846),Vector2(125.031,852),Vector2(166,852),Vector2(515,852)],[Vector2(515,852),Vector2(166,852),Vector2(166,855),Vector2(515,855)],[Vector2(125.046,855),Vector2(150,855),Vector2(166,852),Vector2(125.031,852)],[Vector2(515,861),Vector2(515,855),Vector2(166,855),Vector2(166,862),Vector2(515.389,862)],[Vector2(125.082,862),Vector2(150,862),Vector2(150,855),Vector2(125.046,855)],[Vector2(515.389,862),Vector2(166,862),Vector2(166,879),Vector2(522,879)],[Vector2(125.168,879),Vector2(150,879),Vector2(150,862),Vector2(125.082,862)],[Vector2(522,879),Vector2(166,879),Vector2(166,894),Vector2(522.097,894)],[Vector2(125.245,894),Vector2(150,894),Vector2(150,879),Vector2(125.168,879)],[Vector2(522.097,894),Vector2(166,894),Vector2(150,894),Vector2(125.245,894),Vector2(125.347,914),Vector2(522.226,914)],[Vector2(522.226,914),Vector2(125.347,914),Vector2(125.367,918),Vector2(150,918),Vector2(165,918),Vector2(522.252,918)],[Vector2(522.252,918),Vector2(165,918),Vector2(165,986),Vector2(522.69,986)],[Vector2(125.714,986),Vector2(151.925,986),Vector2(150,918),Vector2(125.367,918)],[Vector2(522.69,986),Vector2(165,986),Vector2(165,999),Vector2(522.774,999)],[Vector2(125.781,999),Vector2(152.292,999),Vector2(151.925,986),Vector2(125.714,986)],[Vector2(522.774,999),Vector2(165,999),Vector2(165,1000),Vector2(522.781,1000)],[Vector2(125.786,1000),Vector2(152.321,1000),Vector2(152.292,999),Vector2(125.781,999)],[Vector2(522.781,1000),Vector2(165,1000),Vector2(174.6,1024),Vector2(522.935,1024)],[Vector2(125.908,1024),Vector2(153,1024),Vector2(152.321,1000),Vector2(125.786,1000)],[Vector2(522.935,1024),Vector2(174.6,1024),Vector2(175,1025),Vector2(522.942,1025)],[Vector2(125.913,1025),Vector2(155,1025),Vector2(153,1024),Vector2(125.908,1024)],[Vector2(523,1034),Vector2(522.942,1025),Vector2(175,1025),Vector2(175,1035),Vector2(522.278,1035)],[Vector2(125.964,1035),Vector2(175,1035),Vector2(155,1025),Vector2(125.913,1025)],[Vector2(141,1057),Vector2(182,1064),Vector2(274,1062),Vector2(285,1077),Vector2(428,1076),Vector2(437,1055),Vector2(510,1052),Vector2(522.278,1035),Vector2(175,1035),Vector2(125.964,1035),Vector2(126,1042)]],
	"quarantine_cabinet":[[Vector2(1118,832),Vector2(1103,816),Vector2(1073,814),Vector2(1069,745),Vector2(1050,725),Vector2(753,726),Vector2(737,751),Vector2(737,852),Vector2(1121.39,852)],[Vector2(1121.39,852),Vector2(737,852),Vector2(737,855),Vector2(1082,855),Vector2(1121.9,855)],[Vector2(1121.9,855),Vector2(1082,855),Vector2(1098,862),Vector2(1123.08,862)],[Vector2(737,862),Vector2(1082.29,862),Vector2(1082,855),Vector2(737,855)],[Vector2(1123.08,862),Vector2(1098,862),Vector2(1100,879),Vector2(1125.97,879)],[Vector2(737,879),Vector2(1083,879),Vector2(1082.29,862),Vector2(737,862)],[Vector2(1128,891),Vector2(1125.97,879),Vector2(1100,879),Vector2(1083,879),Vector2(737,879),Vector2(737,888),Vector2(735.32,894),Vector2(1127.89,894)],[Vector2(1127.89,894),Vector2(735.32,894),Vector2(730,913),Vector2(730,914),Vector2(1081,914),Vector2(1100,914),Vector2(1127.17,914)],[Vector2(1127.17,914),Vector2(1100,914),Vector2(1100,918),Vector2(1127.03,918)],[Vector2(730,918),Vector2(1080.95,918),Vector2(1081,914),Vector2(730,914)],[Vector2(1127.03,918),Vector2(1100,918),Vector2(1100,986),Vector2(1124.58,986)],[Vector2(730,986),Vector2(1080.15,986),Vector2(1080.95,918),Vector2(730,918)],[Vector2(1124.58,986),Vector2(1100,986),Vector2(1092,999),Vector2(1124.11,999)],[Vector2(730,999),Vector2(1080,999),Vector2(1080.15,986),Vector2(730,986)],[Vector2(1124.11,999),Vector2(1092,999),Vector2(1080,999),Vector2(730,999),Vector2(730,1000),Vector2(1124.07,1000)],[Vector2(1114,1018),Vector2(1124,1002),Vector2(1124.07,1000),Vector2(730,1000),Vector2(730,1024),Vector2(1093.6,1024)],[Vector2(1093.6,1024),Vector2(730,1024),Vector2(730,1025),Vector2(1090.2,1025)],[Vector2(1080,1028),Vector2(1090.2,1025),Vector2(730,1025),Vector2(730,1035),Vector2(1080,1035)],[Vector2(749,1091),Vector2(1062,1089),Vector2(1080,1067),Vector2(1080,1035),Vector2(730,1035),Vector2(730,1072)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/quarantine_cell-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"quarantine_berth","rect":Rect2(-165,-128,120,72),"pivot":Vector2(344,513),"width":435.0,"outline":[Vector2(128,247),Vector2(135,233),Vector2(135,191),Vector2(145,177),Vector2(177,175),Vector2(180,144),Vector2(199,105),Vector2(217,100),Vector2(493,100),Vector2(507,125),Vector2(524,130),Vector2(532,147),Vector2(531,230),Vector2(548,238),Vector2(558,270),Vector2(558,421),Vector2(542,440),Vector2(533,485),Vector2(521,499),Vector2(202,498),Vector2(190,511),Vector2(148,513),Vector2(129,499)]},
		{"id":"quarantine_filter","rect":Rect2(92,-133,70,52),"pivot":Vector2(915,508),"width":404.0,"outline":[Vector2(717,248),Vector2(726,230),Vector2(727,173),Vector2(741,153),Vector2(763,148),Vector2(773,125),Vector2(793,115),Vector2(822,116),Vector2(843,137),Vector2(849,151),Vector2(868,149),Vector2(882,126),Vector2(905,115),Vector2(930,120),Vector2(949,140),Vector2(954,152),Vector2(978,151),Vector2(993,123),Vector2(1015,115),Vector2(1044,124),Vector2(1060,148),Vector2(1079,159),Vector2(1081,176),Vector2(1101,178),Vector2(1112,192),Vector2(1116,472),Vector2(1102,489),Vector2(1008,489),Vector2(1000,505),Vector2(847,507),Vector2(833,491),Vector2(731,488),Vector2(717,475)]},
		{"id":"quarantine_monitor","rect":Rect2(-28,-105,72,44),"pivot":Vector2(324,1077),"width":404.0,"outline":[Vector2(125,846),Vector2(137,830),Vector2(179,822),Vector2(192,796),Vector2(202,786),Vector2(203,740),Vector2(216,734),Vector2(245,736),Vector2(251,751),Vector2(430,751),Vector2(448,770),Vector2(448,788),Vector2(504,788),Vector2(515,802),Vector2(515,861),Vector2(522,879),Vector2(523,1034),Vector2(510,1052),Vector2(437,1055),Vector2(428,1076),Vector2(285,1077),Vector2(274,1062),Vector2(182,1064),Vector2(141,1057),Vector2(126,1042)]},
		{"id":"quarantine_cabinet","rect":Rect2(-166,106,74,46),"pivot":Vector2(927,1091),"width":407.0,"outline":[Vector2(730,913),Vector2(737,888),Vector2(737,751),Vector2(753,726),Vector2(1050,725),Vector2(1069,745),Vector2(1073,814),Vector2(1103,816),Vector2(1118,832),Vector2(1128,891),Vector2(1124,1002),Vector2(1114,1018),Vector2(1080,1028),Vector2(1080,1067),Vector2(1062,1089),Vector2(749,1091),Vector2(730,1072)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/quarantine-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1
	layout[0].rotation=(quarter+1)%4 # Canonical east/west straight; props retain quarter.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("525c60"),Color(0.17,0.19,0.20,0.35),2)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(270,20,118,56) if horizontal else Rect2(19,252,42,124))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(14,15,48,48))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="quarantine_filter":
		var center := Vector2(805,360)
		var angle := -1.1+0.35*sin(time*2)
		marks.append([center,center+Vector2(cos(angle),sin(angle))*14])
	elif prop.id=="quarantine_monitor":
		for row in range(3):
			var start := Vector2(304,790+row*18)
			marks.append([start,start+Vector2(35+20*sin(time*2+row),0)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["quarantine_filter","quarantine_monitor"]

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
