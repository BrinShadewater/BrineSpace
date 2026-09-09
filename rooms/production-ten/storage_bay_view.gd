extends "res://rooms/whole-room/life_support_view.gd"
## Passive logistics: secured cargo and manual handling platform remain stationary.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/storage_bay-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"storage_crates","rect":Rect2(-170,105,62,42),"pivot":Vector2(317,530),"width":379.0,"outline":[Vector2(129,158),Vector2(141,125),Vector2(153,112),Vector2(184,112),Vector2(188,108),Vector2(202,109),Vector2(204,112),Vector2(304,112),Vector2(307,108),Vector2(321,110),Vector2(355,112),Vector2(368,125),Vector2(379,152),Vector2(392,146),Vector2(480,147),Vector2(484,206),Vector2(498,211),Vector2(505,232),Vector2(505,512),Vector2(491,530),Vector2(142,530),Vector2(128,516)]},
		{"id":"storage_shelves","rect":Rect2(84,-156,88,56),"pivot":Vector2(927,514),"width":374.0,"outline":[Vector2(750,116),Vector2(766,116),Vector2(768,134),Vector2(1086,135),Vector2(1086,116),Vector2(1103,116),Vector2(1107,256),Vector2(1112,275),Vector2(1113,506),Vector2(1081,514),Vector2(1080,495),Vector2(776,495),Vector2(773,513),Vector2(740,513),Vector2(741,471),Vector2(747,464),Vector2(746,258),Vector2(751,236)]},
		{"id":"storage_lift","rect":Rect2(-100,94,66,50),"pivot":Vector2(315,1106),"width":327.0,"outline":[Vector2(173,741),Vector2(201,741),Vector2(202,769),Vector2(217,773),Vector2(219,805),Vector2(398,805),Vector2(400,772),Vector2(414,769),Vector2(416,741),Vector2(440,741),Vector2(442,776),Vector2(455,783),Vector2(461,830),Vector2(470,839),Vector2(471,903),Vector2(479,911),Vector2(478,1059),Vector2(458,1074),Vector2(454,1105),Vector2(415,1106),Vector2(409,1094),Vector2(205,1093),Vector2(202,1106),Vector2(167,1105),Vector2(152,1085),Vector2(152,834),Vector2(161,821),Vector2(162,784),Vector2(173,782)]},
		{"id":"storage_secured_rack","rect":Rect2(116,-66,52,36),"pivot":Vector2(931,1074),"width":292.0,"outline":[Vector2(796,776),Vector2(813,776),Vector2(815,790),Vector2(1051,790),Vector2(1052,776),Vector2(1070,776),Vector2(1075,834),Vector2(1078,848),Vector2(1075,1058),Vector2(1064,1074),Vector2(1038,1074),Vector2(1036,1059),Vector2(825,1059),Vector2(823,1073),Vector2(786,1072),Vector2(785,1050),Vector2(790,840)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/storage-composition-v4.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	for prop in props:
		if prop.id=="storage_secured_rack" and quarter==0:
			prop.rect.position.y=-48
			prop.sort_y=prop.rect.end.y
		if prop.id=="storage_secured_rack" and quarter==2:
			prop.rect.position=Vector2(-142,40)-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
		if prop.id=="storage_lift" and quarter in [1,3]:
			var at:=Vector2(-119,-52) if quarter==1 else Vector2(119,55)
			prop.rect.position=at-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("505659"),Color(0.17,0.19,0.20,0.35),2)
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
		painter.draw_texture_rect_region(life_texture,target,Rect2(241,9,132,45) if horizontal else Rect2(9,96,40,123))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(12,10,42,43))

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
func is_animated_prop(_prop: Dictionary) -> bool: return false

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	if dressing!=null: dressing.draw_supported(prop)

