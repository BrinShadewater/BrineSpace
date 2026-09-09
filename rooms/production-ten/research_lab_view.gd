extends "res://rooms/whole-room/life_support_view.gd"
## Science equipment; aperture pieces omit source floor rather than painting it out.
const FLOOR_CUTOUTS = {
	"research_specimens":[[Vector2(168,253),Vector2(168.046,264),Vector2(499,264),Vector2(522.065,264),Vector2(522,261),Vector2(504,243),Vector2(479,236),Vector2(478,168),Vector2(462,152),Vector2(193,152),Vector2(182,163),Vector2(180,234)],[Vector2(168.092,275),Vector2(499.272,275),Vector2(499,264),Vector2(168.046,264)],[Vector2(522.065,264),Vector2(499,264),Vector2(508,275),Vector2(522.301,275)],[Vector2(168.239,310),Vector2(500.136,310),Vector2(499.272,275),Vector2(168.092,275)],[Vector2(522.301,275),Vector2(508,275),Vector2(508,310),Vector2(523.054,310)],[Vector2(168.286,321),Vector2(500.407,321),Vector2(500.136,310),Vector2(168.239,310)],[Vector2(523.054,310),Vector2(508,310),Vector2(508,321),Vector2(523.29,321)],[Vector2(168.336,333),Vector2(500.704,333),Vector2(500.407,321),Vector2(168.286,321)],[Vector2(523.29,321),Vector2(508,321),Vector2(508,333),Vector2(523.548,333)],[Vector2(168.387,345),Vector2(501,345),Vector2(500.704,333),Vector2(168.336,333)],[Vector2(523.548,333),Vector2(508,333),Vector2(501,345),Vector2(523.806,345)],[Vector2(168.555,385),Vector2(498,385),Vector2(498,369),Vector2(510,367),Vector2(524,354),Vector2(523.806,345),Vector2(501,345),Vector2(168.387,345)],[Vector2(168.588,393),Vector2(498,393),Vector2(498,385),Vector2(168.555,385)],[Vector2(169,491),Vector2(184,508),Vector2(484,508),Vector2(498,491),Vector2(498,393),Vector2(168.588,393)]],
	"research_analyzer":[[Vector2(718,262),Vector2(718,264),Vector2(1070.46,264),Vector2(1067,162),Vector2(1052,139),Vector2(983,138),Vector2(974,145),Vector2(743,145),Vector2(731,158),Vector2(729,244)],[Vector2(718,275),Vector2(1070.83,275),Vector2(1070.46,264),Vector2(718,264)],[Vector2(718,310),Vector2(1080,310),Vector2(1107.3,310),Vector2(1092,293),Vector2(1071,280),Vector2(1070.83,275),Vector2(718,275)],[Vector2(718,321),Vector2(1080.27,321),Vector2(1080,310),Vector2(718,310)],[Vector2(1110,313),Vector2(1107.3,310),Vector2(1080,310),Vector2(1094,321),Vector2(1110,321)],[Vector2(718,333),Vector2(1080.55,333),Vector2(1080.27,321),Vector2(718,321)],[Vector2(1110,321),Vector2(1094,321),Vector2(1094,333),Vector2(1110,333)],[Vector2(718,345),Vector2(1080.84,345),Vector2(1080.55,333),Vector2(718,333)],[Vector2(1110,333),Vector2(1094,333),Vector2(1094,345),Vector2(1110,345)],[Vector2(718,385),Vector2(1081.81,385),Vector2(1080.84,345),Vector2(718,345)],[Vector2(1110,345),Vector2(1094,345),Vector2(1094,385),Vector2(1110,385)],[Vector2(718,393),Vector2(1082,393),Vector2(1081.81,385),Vector2(718,385)],[Vector2(1110,385),Vector2(1094,385),Vector2(1082,393),Vector2(1110,393)],[Vector2(718,502),Vector2(734,520),Vector2(1061,520),Vector2(1074,503),Vector2(1076,412),Vector2(1091,411),Vector2(1110,393),Vector2(1082,393),Vector2(718,393)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/material-polish-v2/research-equipment.png")) != OK: push_error("Failed to load image (rooms/production-ten/research_lab_view.gd)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"research_specimens","rect":Rect2(-166,-124,98,58),"pivot":Vector2(346,508),"width":358.0,"outline":[Vector2(182,163),Vector2(193,152),Vector2(462,152),Vector2(478,168),Vector2(479,236),Vector2(504,243),Vector2(522,261),Vector2(524,354),Vector2(510,367),Vector2(498,369),Vector2(498,491),Vector2(484,508),Vector2(184,508),Vector2(169,491),Vector2(168,253),Vector2(180,234)]},
		{"id":"research_analyzer","rect":Rect2(-54,-124,108,64),"pivot":Vector2(913,520),"width":394.0,"outline":[Vector2(731,158),Vector2(743,145),Vector2(974,145),Vector2(983,138),Vector2(1052,139),Vector2(1067,162),Vector2(1071,280),Vector2(1092,293),Vector2(1110,313),Vector2(1110,393),Vector2(1091,411),Vector2(1076,412),Vector2(1074,503),Vector2(1061,520),Vector2(734,520),Vector2(718,502),Vector2(718,262),Vector2(729,244)]},
		{"id":"research_scanner","rect":Rect2(-162,22,106,68),"pivot":Vector2(343,1050),"width":352.0,"outline":[Vector2(169,824),Vector2(181,808),Vector2(190,808),Vector2(192,749),Vector2(211,711),Vector2(244,683),Vector2(286,670),Vector2(347,669),Vector2(390,686),Vector2(422,713),Vector2(445,755),Vector2(448,787),Vector2(487,787),Vector2(488,805),Vector2(510,814),Vector2(522,839),Vector2(516,866),Vector2(499,880),Vector2(499,1034),Vector2(485,1050),Vector2(185,1050),Vector2(169,1034)]},
		{"id":"research_cabinet","rect":Rect2(100,-117,64,42),"pivot":Vector2(915,1035),"width":308.0,"outline":[Vector2(764,690),Vector2(776,675),Vector2(1053,675),Vector2(1069,691),Vector2(1069,1020),Vector2(1057,1035),Vector2(778,1035),Vector2(763,1021)]}
	]
	# The sealed rear wall holds paired instruments; the larger prep station sits beside the entry aisle.
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/research-composition-v3.json")

	rebuild()

func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
	layout[0].kind=3 # Canonical south-only dead end.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("909a9e"),Color(0.25,0.32,0.38,0.2),2,"sealed")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"sealed")

	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").identity_details(painter,props,"research",operating)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("263747"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(254,54,112,50) if horizontal else Rect2(61,379,44,117))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(59,51,48,54))

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="research_specimens":
		var x := 315+fposmod(time*22,20)
		marks.append([Vector2(x,373),Vector2(x+4,373)])
	elif prop.id=="research_analyzer":
		for row in range(3):
			marks.append([Vector2(780,221+row*22),Vector2(835+24*sin(time*2+row),221+row*22)])
	elif prop.id=="research_scanner":
		var y := 833+sin(time*2)*8
		marks.append([Vector2(298,y),Vector2(338,y)])
	return marks

func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["research_specimens","research_analyzer","research_scanner"]

func draw_piece(prop: Dictionary,outline: Array) -> void:
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	painter.draw_polygon(vertices,PackedColorArray([Color.WHITE]),uv,life_texture)

func draw_registered_prop(prop: Dictionary) -> void:
	draw_prop_base(prop)
	draw_prop_animation(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	if prop.id=="research_scanner":
		# Open arch: split into the U-shaped frame, central scanner head and base.
		# No sampled floor is drawn through the two gaps beside the head.
		draw_piece(prop,[Vector2(190,810),Vector2(192,749),Vector2(211,711),Vector2(244,683),Vector2(286,670),Vector2(347,669),Vector2(390,686),Vector2(422,713),Vector2(445,755),Vector2(448,810),Vector2(385,810),Vector2(378,782),Vector2(364,765),Vector2(350,754),Vector2(286,754),Vector2(269,766),Vector2(257,786),Vector2(252,810)])
		draw_piece(prop,[Vector2(289,743),Vector2(337,743),Vector2(351,754),Vector2(350,789),Vector2(335,803),Vector2(334,821),Vector2(300,821),Vector2(299,803),Vector2(288,788)])
		draw_piece(prop,[Vector2(169,824),Vector2(181,808),Vector2(190,808),Vector2(194,841),Vector2(217,867),Vector2(250,886),Vector2(264,886),Vector2(264,824),Vector2(279,812),Vector2(355,812),Vector2(373,825),Vector2(373,886),Vector2(400,875),Vector2(422,851),Vector2(439,822),Vector2(448,787),Vector2(487,787),Vector2(488,805),Vector2(510,814),Vector2(522,839),Vector2(516,866),Vector2(499,880),Vector2(499,1034),Vector2(485,1050),Vector2(185,1050),Vector2(169,1034)])
	else:
		for outline in FLOOR_CUTOUTS.get(prop.id,[prop.registration.outline]): draw_piece(prop,outline)
	if dressing!=null: dressing.draw_supported(prop)

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.registration.get("dressing",false): return
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("8cd2e8"),1.15,true)

