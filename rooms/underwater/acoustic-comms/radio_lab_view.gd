extends "res://rooms/whole-room/life_support_view.gd"
## Underwater acoustic communications with engine-owned signal displays.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/acoustic-comms/radio_lab-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"acoustic_listener","rect":Rect2(-165,-143,108,64),"pivot":Vector2(324,472),"width":400.0,"outline":[Vector2(125,258),Vector2(129,237),Vector2(140,210),Vector2(162,197),Vector2(197,190),Vector2(224,197),Vector2(248,211),Vector2(257,211),Vector2(263,193),Vector2(399,192),Vector2(416,211),Vector2(467,211),Vector2(492,236),Vector2(493,276),Vector2(508,292),Vector2(519,326),Vector2(519,412),Vector2(502,438),Vector2(486,451),Vector2(462,471),Vector2(161,470),Vector2(143,451),Vector2(139,377),Vector2(132,355)]},
		{"id":"acoustic_transducers","rect":Rect2(57,-143,108,64),"pivot":Vector2(916,469),"width":390.0,"outline":[Vector2(722,327),Vector2(725,308),Vector2(733,305),Vector2(737,246),Vector2(755,226),Vector2(758,197),Vector2(778,174),Vector2(810,157),Vector2(831,157),Vector2(844,166),Vector2(869,170),Vector2(889,196),Vector2(895,211),Vector2(934,211),Vector2(945,186),Vector2(974,164),Vector2(996,157),Vector2(1015,160),Vector2(1048,179),Vector2(1071,207),Vector2(1074,228),Vector2(1094,243),Vector2(1102,272),Vector2(1103,311),Vector2(1112,320),Vector2(1105,420),Vector2(1086,443),Vector2(988,449),Vector2(982,468),Vector2(851,469),Vector2(844,450),Vector2(755,448),Vector2(734,434)]},
		{"id":"acoustic_receiver","rect":Rect2(-165,63,80,54),"pivot":Vector2(312,1052),"width":380.0,"outline":[Vector2(126,815),Vector2(138,787),Vector2(159,784),Vector2(160,777),Vector2(193,777),Vector2(193,733),Vector2(204,718),Vector2(461,716),Vector2(477,733),Vector2(479,783),Vector2(493,792),Vector2(503,813),Vector2(503,1013),Vector2(481,1042),Vector2(465,1052),Vector2(193,1051),Vector2(176,1036),Vector2(176,995),Vector2(142,995),Vector2(130,982),Vector2(121,895)]},
		{"id":"acoustic_bench","rect":Rect2(83,48,82,54),"pivot":Vector2(926,1065),"width":417.0,"outline":[Vector2(720,1010),Vector2(721,830),Vector2(734,798),Vector2(751,783),Vector2(852,783),Vector2(862,768),Vector2(879,755),Vector2(901,758),Vector2(921,773),Vector2(940,784),Vector2(1078,784),Vector2(1096,801),Vector2(1100,832),Vector2(1117,840),Vector2(1135,864),Vector2(1137,928),Vector2(1124,950),Vector2(1108,960),Vector2(1105,1038),Vector2(1086,1063),Vector2(753,1065),Vector2(733,1044)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/acoustic-comms/radio-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1
	layout[0].rotation=(quarter+1)%4 # Canonical east/west straight; props retain quarter.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("41474a"),Color(0.17,0.19,0.20,0.35),2,"technical")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"technical")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(280,37,116,48) if horizontal else Rect2(36,340,44,98))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(35,39,48,48))

const SCREEN := Rect2(287,220,101,48)
func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="acoustic_listener":
		for x in range(294,378,7):
			var y := 245+8*sin(x*0.19+time*3)
			marks.append([Vector2(x,y),Vector2(x+6,245+8*sin((x+6)*0.19+time*3))])
	elif prop.id=="acoustic_receiver":
		for row in range(3):
			marks.append([Vector2(269,832+row*58),Vector2(279+7*sin(time*2+row),832+row*58)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["acoustic_listener","acoustic_receiver"]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)

	if prop.id=="acoustic_listener":
		# Offline screen surface replaces the faint generated signal trace.
		painter.draw_rect(Rect2(life_point(prop,SCREEN.position),SCREEN.size*(prop.rect.size.x/prop.registration.width)),Color("080e11"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("90bec6"),1.0,true)
