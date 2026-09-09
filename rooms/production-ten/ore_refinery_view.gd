extends "res://rooms/whole-room/life_support_view.gd"
## Mineral processing: local belt/flow cues remain inside complete machinery bases.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/ore_refinery-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"refinery_crusher","rect":Rect2(-164,-115,104,64),"pivot":Vector2(321,576),"width":360.0,"outline":[Vector2(143,245),Vector2(173,213),Vector2(177,198),Vector2(193,191),Vector2(194,180),Vector2(224,174),Vector2(224,139),Vector2(248,112),Vector2(369,112),Vector2(396,137),Vector2(398,174),Vector2(422,175),Vector2(427,190),Vector2(458,190),Vector2(478,207),Vector2(480,225),Vector2(500,244),Vector2(501,489),Vector2(482,507),Vector2(398,507),Vector2(398,559),Vector2(380,576),Vector2(242,576),Vector2(222,559),Vector2(222,507),Vector2(162,507),Vector2(143,489)]},
		{"id":"refinery_vessels","rect":Rect2(67,-119,98,60),"pivot":Vector2(935,507),"width":393.0,"outline":[Vector2(740,268),Vector2(759,245),Vector2(776,240),Vector2(776,182),Vector2(790,164),Vector2(816,151),Vector2(828,146),Vector2(840,153),Vector2(858,162),Vector2(879,190),Vector2(889,181),Vector2(909,157),Vector2(931,150),Vector2(939,145),Vector2(949,154),Vector2(968,163),Vector2(989,185),Vector2(1000,171),Vector2(1026,153),Vector2(1044,145),Vector2(1055,153),Vector2(1078,169),Vector2(1097,188),Vector2(1099,242),Vector2(1119,257),Vector2(1130,278),Vector2(1131,486),Vector2(1114,507),Vector2(758,507),Vector2(739,488)]},
		{"id":"refinery_sorter","rect":Rect2(84,37,80,50),"pivot":Vector2(320,1095),"width":366.0,"outline":[Vector2(174,733),Vector2(299,733),Vector2(306,719),Vector2(353,719),Vector2(360,728),Vector2(421,728),Vector2(434,742),Vector2(456,744),Vector2(458,766),Vector2(485,771),Vector2(499,791),Vector2(502,1074),Vector2(482,1095),Vector2(157,1095),Vector2(137,1078),Vector2(137,790),Vector2(152,771),Vector2(171,766)]},
		{"id":"refinery_hopper","rect":Rect2(-154,-4,80,52),"pivot":Vector2(938,1095),"width":338.0,"outline":[Vector2(772,791),Vector2(791,768),Vector2(808,766),Vector2(809,746),Vector2(823,733),Vector2(1053,733),Vector2(1069,747),Vector2(1070,765),Vector2(1090,772),Vector2(1105,791),Vector2(1107,1074),Vector2(1088,1095),Vector2(790,1095),Vector2(769,1075)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/refinery-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	for prop in props:
		if prop.id=="refinery_crusher" and quarter==2:
			prop.rect.position=Vector2(112,111)-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
	if dressing!=null: dressing.place()
	layout[0].kind=1 # Canonical north/south straight.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("3c4346"),Color(0.17,0.19,0.20,0.35),2)
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
		painter.draw_texture_rect_region(life_texture,target,Rect2(202,45,108,48) if horizontal else Rect2(48,97,36,99))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(47,46,39,43))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="refinery_crusher":
		for i in range(4):
			var y := 386+fposmod(time*35+i*29,116)
			marks.append([Vector2(270,y),Vector2(341,y)])
	elif prop.id=="refinery_vessels":
		for i in range(3):
			var y := 259+fposmod(time*20+i*7,29)
			marks.append([Vector2(827+i*108,y),Vector2(827+i*108,y+5)])
	elif prop.id=="refinery_sorter":
		for x in [211.0,357.0]:
			for i in range(4):
				var y := 909+fposmod(time*32+i*29,116)
				marks.append([Vector2(x,y),Vector2(x+42,y)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["refinery_crusher","refinery_vessels","refinery_sorter"]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)

	if dressing!=null: dressing.draw_supported(prop)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color(0.70,0.66,0.51,0.65),1.0,true)
