extends "res://rooms/whole-room/life_support_view.gd"
var drone_deployed := false
var hatch_open := 0.0
## Underwater ROV service equipment; deployment hatch remains closed.
const FLOOR_CUTOUTS = {
	"salvage_hatch":[[Vector2(1048,669),Vector2(1038,656),Vector2(1002,655),Vector2(999,658),Vector2(818,659),Vector2(805,672),Vector2(805,699),Vector2(846,699),Vector2(947,699),Vector2(1048,699)],[Vector2(1048,699),Vector2(947,699),Vector2(977,729),Vector2(1048,729)],[Vector2(805,710),Vector2(809,718),Vector2(808.267,729),Vector2(843,729),Vector2(846,699),Vector2(805,699)],[Vector2(1081,737),Vector2(1048,737),Vector2(1048,729),Vector2(977,729),Vector2(843,729),Vector2(808.267,729),Vector2(808,733),Vector2(785,736),Vector2(769.25,750),Vector2(1053,750),Vector2(1075,750),Vector2(1091,750)],[Vector2(1091,750),Vector2(1075,750),Vector2(1075,769),Vector2(1091.22,769)],[Vector2(767,752),Vector2(764.385,769),Vector2(1053,769),Vector2(1053,750),Vector2(769.25,750)],[Vector2(1091.22,769),Vector2(1075,769),Vector2(1075,786),Vector2(1091.42,786)],[Vector2(763,778),Vector2(739,778),Vector2(731,786),Vector2(1064,786),Vector2(1064,769),Vector2(1053,769),Vector2(764.385,769)],[Vector2(1091.42,786),Vector2(1075,786),Vector2(1075,788),Vector2(1091.45,788)],[Vector2(729,788),Vector2(1075,788),Vector2(1064,786),Vector2(731,786)],[Vector2(741,1083),Vector2(765,1083),Vector2(773,1091),Vector2(807,1091),Vector2(815,1082),Vector2(1025,1082),Vector2(1033,1090),Vector2(1080,1091),Vector2(1094,1074),Vector2(1098,1006),Vector2(1098,858),Vector2(1092,835),Vector2(1091.45,788),Vector2(1075,788),Vector2(729,788),Vector2(727,790),Vector2(727,1070)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/salvage_drone_bay-source-v1.png")) != OK: push_error("Failed to load image (rooms/production-ten/salvage_drone_bay_view.gd:13)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"salvage_rov","rect":Rect2(-156,-143,90,64),"pivot":Vector2(347,585),"width":344.0,"outline":[Vector2(179,256),Vector2(191,253),Vector2(191,224),Vector2(209,216),Vector2(225,220),Vector2(225,174),Vector2(237,163),Vector2(282,163),Vector2(286,141),Vector2(302,133),Vector2(389,133),Vector2(410,145),Vector2(410,162),Vector2(452,163),Vector2(467,177),Vector2(467,216),Vector2(498,217),Vector2(506,239),Vector2(516,275),Vector2(514,319),Vector2(506,332),Vector2(516,346),Vector2(516,528),Vector2(503,552),Vector2(473,554),Vector2(453,579),Vector2(429,585),Vector2(400,562),Vector2(389,550),Vector2(306,550),Vector2(286,575),Vector2(267,584),Vector2(238,568),Vector2(227,550),Vector2(177,552)]},
		{"id":"salvage_winch","rect":Rect2(66,-143,90,64),"pivot":Vector2(896,562),"width":409.0,"outline":[Vector2(695,293),Vector2(708,235),Vector2(726,229),Vector2(726,199),Vector2(745,188),Vector2(769,172),Vector2(790,172),Vector2(793,151),Vector2(811,151),Vector2(820,146),Vector2(841,148),Vector2(851,158),Vector2(964,157),Vector2(967,151),Vector2(989,151),Vector2(991,188),Vector2(1013,190),Vector2(1030,201),Vector2(1032,222),Vector2(1042,233),Vector2(1045,250),Vector2(1057,243),Vector2(1090,242),Vector2(1101,259),Vector2(1099,340),Vector2(1090,361),Vector2(1093,477),Vector2(1083,497),Vector2(1089,544),Vector2(1077,558),Vector2(1035,557),Vector2(1029,563),Vector2(1002,562),Vector2(996,552),Vector2(800,553),Vector2(793,562),Vector2(750,562),Vector2(743,552),Vector2(705,551),Vector2(697,533)]},
		{"id":"salvage_sorter","rect":Rect2(-156,79,90,64),"pivot":Vector2(333,1090),"width":393.0,"outline":[Vector2(143,776),Vector2(153,760),Vector2(172,760),Vector2(178,738),Vector2(180,711),Vector2(195,689),Vector2(230,681),Vector2(257,657),Vector2(281,650),Vector2(299,655),Vector2(313,669),Vector2(316,681),Vector2(360,710),Vector2(375,715),Vector2(390,713),Vector2(398,732),Vector2(487,732),Vector2(499,745),Vector2(500,776),Vector2(515,778),Vector2(527,792),Vector2(527,1069),Vector2(513,1087),Vector2(469,1089),Vector2(460,1082),Vector2(241,1083),Vector2(233,1090),Vector2(201,1089),Vector2(193,1083),Vector2(150,1083),Vector2(141,1068)]},
		{"id":"salvage_hatch","rect":Rect2(66,79,90,64),"pivot":Vector2(912,1092),"width":373.0,"outline":[Vector2(727,790),Vector2(739,778),Vector2(763,778),Vector2(767,752),Vector2(785,736),Vector2(808,733),Vector2(809,718),Vector2(805,710),Vector2(805,672),Vector2(818,659),Vector2(999,658),Vector2(1002,655),Vector2(1038,656),Vector2(1048,669),Vector2(1048,737),Vector2(1081,737),Vector2(1091,750),Vector2(1092,835),Vector2(1098,858),Vector2(1098,1006),Vector2(1094,1074),Vector2(1080,1091),Vector2(1033,1090),Vector2(1025,1082),Vector2(815,1082),Vector2(807,1091),Vector2(773,1091),Vector2(765,1083),Vector2(741,1083),Vector2(727,1070)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/salvage-composition-v2.json")
	# Offset the intake bench toward circulation and reserve a quiet lower-right
	# staging area; recovery hatch/winch and inspection/sorter read as two zones.
	var activity_centers := {"salvage_hatch":Vector2(111,55),"salvage_intake_bench":Vector2(-96,12),"salvage_sorter":Vector2(-117,130)}
	for item in life_items:
		if activity_centers.has(item.id): item.rect.position=activity_centers[item.id]-item.rect.size*0.5
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1 # Canonical north/south straight.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("525c60"),Color(0.17,0.19,0.20,0.35),2)
	RoomFloor.draw_dressing(painter,center,edges,"steel")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(223,39,122,58) if horizontal else Rect2(50,118,39,169))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(52,37,48,44))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="salvage_rov":
		var x := 329+sin(time*2)*8
		marks.append([Vector2(x,303),Vector2(x+7,303)])
	elif prop.id=="salvage_winch":
		# Control-panel diagnostics; an unloaded winch does not spool itself.
		var x := 1020+sin(time*2)*5
		marks.append([Vector2(x,444),Vector2(x+6,444)])
	elif prop.id=="salvage_sorter":
		var x := 410+fposmod(time*17,28)
		marks.append([Vector2(x,879),Vector2(x+7,879)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["salvage_rov","salvage_winch","salvage_sorter"]

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.id in ["salvage_rov","salvage_hatch"]:
		return preload("res://rooms/production-ten/drone_prop_bounds.gd").bounds(prop,"salvage")
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id == "salvage_hatch":
		preload("res://scripts/drone_art.gd").draw_hatch(painter,Vector2(prop.rect.get_center().x,prop.rect.end.y-35),90,hatch_open)
		return
	if prop.id == "salvage_rov":
		var center := Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
		preload("res://scripts/drone_art.gd").draw_asset(painter,"cradle",center,90)
		if not drone_deployed: preload("res://scripts/drone_art.gd").draw_drone(painter,"salvage",center-Vector2(0,15),70,machine_clock,false,false)
		preload("res://rooms/production-ten/drone_dock_status.gd").draw(painter,center,machine_clock,operating)
		return
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
