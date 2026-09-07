extends "res://rooms/whole-room/life_support_view.gd"
## Chilled coils and water recovery; source assemblies with canonical tee routes.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/tidal-condenser/tidal_condenser-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"tidal_coils","rect":Rect2(-165,-143,108,64),"pivot":Vector2(348,510),"width":419.0,"outline":[Vector2(140,174),Vector2(163,172),Vector2(164,180),Vector2(191,179),Vector2(204,160),Vector2(222,155),Vector2(247,157),Vector2(260,171),Vector2(431,171),Vector2(445,156),Vector2(477,158),Vector2(492,174),Vector2(511,174),Vector2(514,185),Vector2(538,189),Vector2(550,204),Vector2(558,475),Vector2(543,505),Vector2(490,510),Vector2(477,497),Vector2(215,497),Vector2(201,510),Vector2(157,510),Vector2(140,491)]},
		{"id":"tidal_tanks","rect":Rect2(57,-143,108,64),"pivot":Vector2(934,502),"width":379.0,"outline":[Vector2(744,478),Vector2(747,220),Vector2(757,211),Vector2(757,160),Vector2(774,152),Vector2(789,159),Vector2(792,176),Vector2(850,175),Vector2(863,165),Vector2(972,165),Vector2(998,177),Vector2(1072,177),Vector2(1073,158),Vector2(1091,153),Vector2(1106,164),Vector2(1106,210),Vector2(1119,222),Vector2(1122,481),Vector2(1109,501),Vector2(1072,500),Vector2(1061,488),Vector2(799,488),Vector2(788,502),Vector2(757,502)]},
		{"id":"tidal_pump","rect":Rect2(-165,93,84,52),"pivot":Vector2(326,1054),"width":372.0,"outline":[Vector2(140,1024),Vector2(143,829),Vector2(156,817),Vector2(174,817),Vector2(176,829),Vector2(189,827),Vector2(194,812),Vector2(214,799),Vector2(242,798),Vector2(264,811),Vector2(277,831),Vector2(304,824),Vector2(457,824),Vector2(469,813),Vector2(489,815),Vector2(495,830),Vector2(508,845),Vector2(512,1036),Vector2(494,1053),Vector2(466,1053),Vector2(456,1040),Vector2(194,1040),Vector2(183,1054),Vector2(154,1053)]},
		{"id":"tidal_monitor","rect":Rect2(81,94,84,52),"pivot":Vector2(932,1055),"width":373.0,"outline":[Vector2(746,1028),Vector2(746,853),Vector2(759,837),Vector2(769,819),Vector2(790,820),Vector2(801,812),Vector2(1068,812),Vector2(1080,823),Vector2(1080,837),Vector2(1097,842),Vector2(1112,860),Vector2(1118,1018),Vector2(1110,1048),Vector2(1074,1054),Vector2(1063,1042),Vector2(799,1042),Vector2(788,1055),Vector2(760,1054)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/tidal-condenser/tidal-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=0
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("41474a"),Color(0.17,0.19,0.20,0.35),2,"wet")
	RoomFloor.draw_dressing(painter,center,edges,"wet")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(310,42,130,38) if horizontal else Rect2(32,269,30,95))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(38,33,48,48))

const SCREEN := Rect2(813,842,69,40)
func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="tidal_coils":
		for x in [260,330,400]:
			var y := 416+fposmod(time*8+x,9)
			marks.append([Vector2(x,y),Vector2(x,y+3)])
	elif prop.id=="tidal_tanks":
		for x in [826,980]:
			var y := 337+sin(time*2)*10
			marks.append([Vector2(x,y),Vector2(x+15,y)])
	elif prop.id=="tidal_pump":
		var angle := -1.2+sin(time*2)*0.4
		marks.append([Vector2(428,914),Vector2(428,914)+Vector2(cos(angle),sin(angle))*15])
	elif prop.id=="tidal_monitor":
		for row in range(3): marks.append([Vector2(819,849+row*10),Vector2(848+15*sin(time*2+row),849+row*10)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)

	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("88bdc5"),1.0,true)
