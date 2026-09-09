extends "res://rooms/whole-room/life_support_view.gd"
## Underwater ROV service equipment; deployment hatch remains closed.
const FLOOR_CUTOUTS = {
	"mining_rov":[[Vector2(405,149),Vector2(391,137),Vector2(297,138),Vector2(284,149),Vector2(283.76,155),Vector2(302,155),Vector2(384,155),Vector2(405,155)],[Vector2(405,155),Vector2(384,155),Vector2(384,171),Vector2(405,171)],[Vector2(283.12,171),Vector2(302,171),Vector2(302,155),Vector2(283.76,155)],[Vector2(405,171),Vector2(384,171),Vector2(384,185),Vector2(405,185)],[Vector2(283,174),Vector2(253,173),Vector2(231,181),Vector2(229.143,185),Vector2(302,185),Vector2(302,171),Vector2(283.12,171)],[Vector2(368,171),Vector2(312,171),Vector2(312,185),Vector2(368,185)],[Vector2(405,185),Vector2(384,185),Vector2(368,185),Vector2(312,185),Vector2(312,188),Vector2(405,188)],[Vector2(227.75,188),Vector2(302,188),Vector2(302,185),Vector2(229.143,185)],[Vector2(465,206),Vector2(435,205),Vector2(405,190),Vector2(405,188),Vector2(312,188),Vector2(302,188),Vector2(227.75,188),Vector2(218,209),Vector2(217.234,221),Vector2(469.5,221)],[Vector2(471,226),Vector2(469.5,221),Vector2(217.234,221),Vector2(216.532,232),Vector2(471.157,232)],[Vector2(471.157,232),Vector2(216.532,232),Vector2(215.638,246),Vector2(471.522,246)],[Vector2(471.522,246),Vector2(215.638,246),Vector2(215,256),Vector2(212.5,260),Vector2(471.888,260)],[Vector2(471.888,260),Vector2(212.5,260),Vector2(205,272),Vector2(472.201,272)],[Vector2(472.201,272),Vector2(205,272),Vector2(200.625,279),Vector2(472.384,279)],[Vector2(472.384,279),Vector2(200.625,279),Vector2(200,280),Vector2(199.922,290),Vector2(472.672,290)],[Vector2(219,555),Vector2(466,556),Vector2(487,542),Vector2(488,508),Vector2(478,494),Vector2(472.672,290),Vector2(199.922,290),Vector2(198,535)]],
	"mining_service":[[Vector2(987,151),Vector2(978.429,155),Vector2(993.133,155)],[Vector2(1010,166),Vector2(993.133,155),Vector2(978.429,155),Vector2(972,158),Vector2(963.333,171),Vector2(1020.74,171)],[Vector2(1020.74,171),Vector2(963.333,171),Vector2(956,182),Vector2(954.429,185),Vector2(1050.81,185)],[Vector2(1050.81,185),Vector2(954.429,185),Vector2(952.857,188),Vector2(1057.26,188)],[Vector2(1084,211),Vector2(1068,193),Vector2(1057.26,188),Vector2(952.857,188),Vector2(945,203),Vector2(932,190),Vector2(791,192),Vector2(778,202),Vector2(777.269,221),Vector2(1003,221),Vector2(1081.74,221)],[Vector2(1081.74,221),Vector2(1003,221),Vector2(1039,232),Vector2(1079.26,232)],[Vector2(777,228),Vector2(765.667,232),Vector2(1005.37,232),Vector2(1003,221),Vector2(777.269,221)],[Vector2(1079.26,232),Vector2(1039,232),Vector2(1031.5,246),Vector2(1063,246),Vector2(1075.69,246),Vector2(1077,242)],[Vector2(760,234),Vector2(757.391,246),Vector2(1008.39,246),Vector2(1005.37,232),Vector2(765.667,232)],[Vector2(755,257),Vector2(753.125,260),Vector2(1011.41,260),Vector2(1008.39,246),Vector2(757.391,246)],[Vector2(1063,246),Vector2(1031.5,246),Vector2(1024,260),Vector2(1059.82,260)],[Vector2(1070,260),Vector2(1071.12,260),Vector2(1075.69,246),Vector2(1063,246)],[Vector2(745.625,272),Vector2(1014,272),Vector2(1011.41,260),Vector2(753.125,260)],[Vector2(1059.82,260),Vector2(1024,260),Vector2(1014,272),Vector2(1057.09,272)],[Vector2(1069.79,264.066),Vector2(1067.67,270.552),Vector2(1071.12,260),Vector2(1070,260)],[Vector2(741.25,279),Vector2(1055.5,279),Vector2(1057.09,272),Vector2(1014,272),Vector2(745.625,272)],[Vector2(740,281),Vector2(739.929,290),Vector2(1053,290),Vector2(1055.5,279),Vector2(741.25,279)],[Vector2(1063.72,282.633),Vector2(1053,290),Vector2(1061.31,290)],[Vector2(738,535),Vector2(751,550),Vector2(1034,551),Vector2(1048,534),Vector2(1047,375),Vector2(1056,366),Vector2(1080,358),Vector2(1081,338),Vector2(1068,328),Vector2(1060,294),Vector2(1061.31,290),Vector2(1053,290),Vector2(739.929,290)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
const DroneArt = preload("res://scripts/drone_art.gd")
var drone_deployed := false
var hatch_open := 0.0
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/production-ten/mining_drone_bay-source-v1.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"mining_rov","rect":Rect2(-156,-143,90,64),"pivot":Vector2(343,556),"width":290.0,"outline":[Vector2(200,280),Vector2(215,256),Vector2(218,209),Vector2(231,181),Vector2(253,173),Vector2(283,174),Vector2(284,149),Vector2(297,138),Vector2(391,137),Vector2(405,149),Vector2(405,190),Vector2(435,205),Vector2(465,206),Vector2(471,226),Vector2(478,494),Vector2(488,508),Vector2(487,542),Vector2(466,556),Vector2(219,555),Vector2(198,535)]},
		{"id":"mining_service","rect":Rect2(66,-143,90,64),"pivot":Vector2(912,551),"width":350.0,"outline":[Vector2(740,281),Vector2(755,257),Vector2(760,234),Vector2(777,228),Vector2(778,202),Vector2(791,192),Vector2(932,190),Vector2(945,203),Vector2(956,182),Vector2(972,158),Vector2(987,151),Vector2(1010,166),Vector2(1068,193),Vector2(1084,211),Vector2(1077,242),Vector2(1060,294),Vector2(1068,328),Vector2(1081,338),Vector2(1080,358),Vector2(1056,366),Vector2(1047,375),Vector2(1048,534),Vector2(1034,551),Vector2(751,550),Vector2(738,535)]},
		{"id":"mining_hatch","rect":Rect2(-156,79,90,64),"pivot":Vector2(332,1062),"width":353.0,"outline":[Vector2(159,818),Vector2(168,772),Vector2(203,699),Vector2(308,698),Vector2(310,668),Vector2(324,650),Vector2(341,650),Vector2(356,666),Vector2(361,697),Vector2(453,698),Vector2(490,779),Vector2(497,846),Vector2(510,877),Vector2(511,950),Vector2(502,990),Vector2(503,1043),Vector2(487,1062),Vector2(172,1061),Vector2(156,1044)]},
		{"id":"mining_tether","rect":Rect2(66,79,90,64),"pivot":Vector2(903,1065),"width":387.0,"outline":[Vector2(726,780),Vector2(752,769),Vector2(757,733),Vector2(776,732),Vector2(783,745),Vector2(928,744),Vector2(934,738),Vector2(949,741),Vector2(954,771),Vector2(977,771),Vector2(982,740),Vector2(1070,743),Vector2(1078,758),Vector2(1087,803),Vector2(1094,1019),Vector2(1095,1050),Vector2(1080,1065),Vector2(741,1065),Vector2(726,1051),Vector2(721,999),Vector2(711,986),Vector2(709,902),Vector2(718,874)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/mining-composition-v2.json")
	# One western deployment/service zone rather than four equally spaced displays.
	# Centers rotate with topology; every assembly's artwork remains south-facing.
	var activity_centers := {"mining_hatch":Vector2(-111,20),"mining_tool_trolley":Vector2(-120,112),"mining_inspection_lamp":Vector2(-168,98)}
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
		painter.draw_texture_rect_region(life_texture,target,Rect2(223,39,122,58) if horizontal else Rect2(50,118,39,169))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(52,37,48,44))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="mining_rov":
		# Dock-side diagnostic lens; no spinning thruster or drilling while cradled.
		var x := 325+sin(time*2)*6
		marks.append([Vector2(x,370),Vector2(x+5,370)])
	elif prop.id=="mining_service":
		var x := 850+fposmod(time*18,25)
		marks.append([Vector2(x,207),Vector2(x+8,207)])
	elif prop.id=="mining_tether":
		for row in range(3):
			marks.append([Vector2(1010,773+row*12),Vector2(1032+11*sin(time*2+row),773+row*12)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["mining_rov","mining_service","mining_tether"]

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if prop.id in ["mining_rov","mining_hatch"]:
		return preload("res://rooms/production-ten/drone_prop_bounds.gd").bounds(prop,"mining")
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id == "mining_hatch":
		DroneArt.draw_hatch(painter,Vector2(prop.rect.get_center().x,prop.rect.end.y-35),90,hatch_open)
		return
	if prop.id == "mining_rov":
		var center := Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
		DroneArt.draw_asset(painter,"cradle",center,90)
		if not drone_deployed: DroneArt.draw_drone(painter,"mining",center-Vector2(0,15),70,machine_clock,false,false)
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
