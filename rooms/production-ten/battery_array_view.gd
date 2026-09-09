extends "res://rooms/whole-room/life_support_view.gd"
## Immutable source silhouettes, shared hull, south-facing assemblies.
const FLOOR_CUTOUTS = {
	"battery_bank_west":[[Vector2(521,239),Vector2(508,181),Vector2(500,161),Vector2(479,156),Vector2(479,141),Vector2(457,141),Vector2(457,155),Vector2(401,155),Vector2(401,141),Vector2(383,141),Vector2(382,154),Vector2(324,154),Vector2(324,140),Vector2(305,140),Vector2(305,152),Vector2(248,152),Vector2(247,140),Vector2(229,140),Vector2(228,151),Vector2(209,151),Vector2(195,168),Vector2(194,208),Vector2(173,221),Vector2(173,265),Vector2(149,280),Vector2(145.966,288),Vector2(176,288),Vector2(521.373,288)],[Vector2(521.373,288),Vector2(176,288),Vector2(176.138,297),Vector2(521.441,297)],[Vector2(142.552,297),Vector2(156,297),Vector2(176,288),Vector2(145.966,288)],[Vector2(521.441,297),Vector2(176.138,297),Vector2(176.2,301),Vector2(521.471,301)],[Vector2(141.034,301),Vector2(156,301),Vector2(156,297),Vector2(142.552,297)],[Vector2(521.471,301),Vector2(176.2,301),Vector2(176.323,309),Vector2(521.532,309)],[Vector2(138,309),Vector2(156,309),Vector2(156,301),Vector2(141.034,301)],[Vector2(521.532,309),Vector2(176.323,309),Vector2(177,353),Vector2(521.867,353)],[Vector2(137.762,353),Vector2(156,353),Vector2(156,309),Vector2(138,309)],[Vector2(521.867,353),Vector2(177,353),Vector2(156,358),Vector2(521.905,358)],[Vector2(137.735,358),Vector2(156,358),Vector2(156,353),Vector2(137.762,353)],[Vector2(521.905,358),Vector2(156,358),Vector2(137.735,358),Vector2(137.632,377),Vector2(158,377),Vector2(522.049,377)],[Vector2(522.049,377),Vector2(158,377),Vector2(159.12,384),Vector2(522.103,384)],[Vector2(137.595,384),Vector2(158,384),Vector2(158,377),Vector2(137.632,377)],[Vector2(522.103,384),Vector2(159.12,384),Vector2(159.76,388),Vector2(522.133,388)],[Vector2(137.573,388),Vector2(158,388),Vector2(158,384),Vector2(137.595,384)],[Vector2(522.133,388),Vector2(159.76,388),Vector2(162,402),Vector2(522.24,402)],[Vector2(137.497,402),Vector2(158,402),Vector2(158,388),Vector2(137.573,388)],[Vector2(522.24,402),Vector2(162,402),Vector2(161.893,406),Vector2(522.27,406)],[Vector2(137.476,406),Vector2(158,406),Vector2(158,402),Vector2(137.497,402)],[Vector2(522.27,406),Vector2(161.893,406),Vector2(161.467,422),Vector2(522.392,422)],[Vector2(137.389,422),Vector2(158,422),Vector2(158,406),Vector2(137.476,406)],[Vector2(522.392,422),Vector2(161.467,422),Vector2(160.053,475),Vector2(522.795,475)],[Vector2(137.103,475),Vector2(158,475),Vector2(158,422),Vector2(137.389,422)],[Vector2(522.795,475),Vector2(160.053,475),Vector2(160,477),Vector2(522.81,477)],[Vector2(137.092,477),Vector2(158,477),Vector2(158,475),Vector2(137.103,475)],[Vector2(522.81,477),Vector2(160,477),Vector2(166.346,488),Vector2(522.894,488)],[Vector2(137.032,488),Vector2(158,488),Vector2(158,477),Vector2(137.092,477)],[Vector2(522.894,488),Vector2(166.346,488),Vector2(166.923,489),Vector2(522.901,489)],[Vector2(137.027,489),Vector2(158,489),Vector2(158,488),Vector2(137.032,488)],[Vector2(137.318,495),Vector2(158,495),Vector2(158,489),Vector2(137.027,489),Vector2(137,494)],[Vector2(522.901,489),Vector2(166.923,489),Vector2(170.385,495),Vector2(522.947,495)],[Vector2(138.591,499),Vector2(158,499),Vector2(158,495),Vector2(137.318,495)],[Vector2(522.947,495),Vector2(170.385,495),Vector2(172.692,499),Vector2(522.977,499)],[Vector2(139.545,502),Vector2(162.312,502),Vector2(158,499),Vector2(138.591,499)],[Vector2(522.977,499),Vector2(172.692,499),Vector2(174.423,502),Vector2(523,502)],[Vector2(139.864,503),Vector2(163.75,503),Vector2(162.312,502),Vector2(139.545,502)],[Vector2(523,502),Vector2(174.423,502),Vector2(175,503),Vector2(520.846,503)],[Vector2(140.818,506),Vector2(168.062,506),Vector2(163.75,503),Vector2(139.864,503)],[Vector2(520.846,503),Vector2(175,503),Vector2(216,506),Vector2(514.385,506)],[Vector2(142.409,511),Vector2(175.25,511),Vector2(168.062,506),Vector2(140.818,506)],[Vector2(514.385,506),Vector2(216,506),Vector2(229,511),Vector2(503.615,511)],[Vector2(143.682,515),Vector2(181,515),Vector2(175.25,511),Vector2(142.409,511)],[Vector2(495,515),Vector2(503.615,511),Vector2(229,511),Vector2(181,515),Vector2(268,515)],[Vector2(144,516),Vector2(167,531),Vector2(250,527),Vector2(268,515),Vector2(181,515),Vector2(143.682,515)]],
	"battery_bank_east":[[Vector2(1080,225),Vector2(1071,204),Vector2(1047,196),Vector2(1045,145),Vector2(785,145),Vector2(781,196),Vector2(764,215),Vector2(756,267),Vector2(735,273),Vector2(717.188,288),Vector2(1082.72,288)],[Vector2(1082.72,288),Vector2(717.188,288),Vector2(716,289),Vector2(712.308,297),Vector2(1083.11,297)],[Vector2(1083.11,297),Vector2(712.308,297),Vector2(710.462,301),Vector2(734,301),Vector2(1083.28,301)],[Vector2(1083.28,301),Vector2(734,301),Vector2(734,309),Vector2(1083.63,309)],[Vector2(706.769,309),Vector2(722,309),Vector2(734,301),Vector2(710.462,301)],[Vector2(1083.63,309),Vector2(734,309),Vector2(734,353),Vector2(1085.53,353)],[Vector2(704,315),Vector2(704.481,353),Vector2(721.443,353),Vector2(722,309),Vector2(706.769,309)],[Vector2(1085.53,353),Vector2(734,353),Vector2(734,358),Vector2(1085.75,358)],[Vector2(704.544,358),Vector2(721.38,358),Vector2(721.443,353),Vector2(704.481,353)],[Vector2(1085.75,358),Vector2(734,358),Vector2(734,377),Vector2(1086.57,377)],[Vector2(704.785,377),Vector2(721.139,377),Vector2(721.38,358),Vector2(704.544,358)],[Vector2(1086.57,377),Vector2(734,377),Vector2(734,384),Vector2(1086.87,384)],[Vector2(704.873,384),Vector2(721.051,384),Vector2(721.139,377),Vector2(704.785,377)],[Vector2(1087,387),Vector2(1086.87,384),Vector2(734,384),Vector2(721,388),Vector2(1087.06,388)],[Vector2(704.924,388),Vector2(721,388),Vector2(721.051,384),Vector2(704.873,384)],[Vector2(1087.06,388),Vector2(721,388),Vector2(704.924,388),Vector2(705.101,402),Vector2(1087.83,402)],[Vector2(1087.83,402),Vector2(705.101,402),Vector2(705.152,406),Vector2(724,406),Vector2(1088.06,406)],[Vector2(1088.06,406),Vector2(724,406),Vector2(732,422),Vector2(1088.94,422)],[Vector2(705.354,422),Vector2(725.561,422),Vector2(724,406),Vector2(705.152,406)],[Vector2(707,475),Vector2(730.732,475),Vector2(725.561,422),Vector2(705.354,422),Vector2(706,473)],[Vector2(1090,441),Vector2(1088.94,422),Vector2(732,422),Vector2(733,475),Vector2(1074,475)],[Vector2(708,477),Vector2(730.927,477),Vector2(730.732,475),Vector2(707,475)],[Vector2(1074,475),Vector2(733,475),Vector2(735,477),Vector2(1073.06,477)],[Vector2(713.5,488),Vector2(732,488),Vector2(730.927,477),Vector2(708,477)],[Vector2(1073.06,477),Vector2(735,477),Vector2(746,488),Vector2(1067.88,488)],[Vector2(714,489),Vector2(733.571,489),Vector2(732,488),Vector2(713.5,488)],[Vector2(1067.88,488),Vector2(746,488),Vector2(747,489),Vector2(1067.41,489)],[Vector2(717,495),Vector2(743,495),Vector2(733.571,489),Vector2(714,489)],[Vector2(1066,492),Vector2(1067.41,489),Vector2(747,489),Vector2(786,495),Vector2(892.75,495)],[Vector2(718,497),Vector2(721.857,499),Vector2(749.286,499),Vector2(743,495),Vector2(717,495)],[Vector2(835,496),Vector2(892.75,495),Vector2(786,495),Vector2(791.5,499),Vector2(831.4,499)],[Vector2(727.643,502),Vector2(754,502),Vector2(749.286,499),Vector2(721.857,499)],[Vector2(831.4,499),Vector2(791.5,499),Vector2(795.625,502),Vector2(827.8,502)],[Vector2(729.571,503),Vector2(797,503),Vector2(754,502),Vector2(727.643,502)],[Vector2(827.8,502),Vector2(795.625,502),Vector2(797,503),Vector2(826.6,503)],[Vector2(735.357,506),Vector2(823,506),Vector2(826.6,503),Vector2(797,503),Vector2(729.571,503)],[Vector2(745,511),Vector2(817,511),Vector2(823,506),Vector2(735.357,506)]],
	"battery_distribution":[[Vector2(1075,807),Vector2(1047,798),Vector2(1022,765),Vector2(980,765),Vector2(951,752),Vector2(847,754),Vector2(833,764),Vector2(785,764),Vector2(768,783),Vector2(751,809),Vector2(751.067,824),Vector2(1063,824),Vector2(1085.46,824)],[Vector2(1091,833),Vector2(1085.46,824),Vector2(1063,824),Vector2(1077,838),Vector2(1091,838)],[Vector2(751.129,838),Vector2(1063.27,838),Vector2(1063,824),Vector2(751.067,824)],[Vector2(1091,838),Vector2(1077,838),Vector2(1077,963),Vector2(1091,963)],[Vector2(751.688,963),Vector2(1065.71,963),Vector2(1063.27,838),Vector2(751.129,838)],[Vector2(1091,963),Vector2(1077,963),Vector2(1066,978),Vector2(1091,978)],[Vector2(751.754,978),Vector2(1066,978),Vector2(1065.71,963),Vector2(751.688,963)],[Vector2(849,1033),Vector2(863,1048),Vector2(1045,1038),Vector2(1056,1021),Vector2(1077,1010),Vector2(1091,981),Vector2(1091,978),Vector2(1066,978),Vector2(751.754,978),Vector2(752,1033)]]
}
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/production-ten/battery_array-source-v1.png")) != OK: push_error("Failed to load image (rooms/production-ten/battery_array_view.gd:13)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"battery_bank_west","rect":Rect2(-165,-119,114,64),"pivot":Vector2(331,531),"width":390.0,"outline":[Vector2(138,309),Vector2(149,280),Vector2(173,265),Vector2(173,221),Vector2(194,208),Vector2(195,168),Vector2(209,151),Vector2(228,151),Vector2(229,140),Vector2(247,140),Vector2(248,152),Vector2(305,152),Vector2(305,140),Vector2(324,140),Vector2(324,154),Vector2(382,154),Vector2(383,141),Vector2(401,141),Vector2(401,155),Vector2(457,155),Vector2(457,141),Vector2(479,141),Vector2(479,156),Vector2(500,161),Vector2(508,181),Vector2(521,239),Vector2(523,502),Vector2(495,515),Vector2(268,515),Vector2(250,527),Vector2(167,531),Vector2(144,516),Vector2(137,494)]},
		{"id":"battery_bank_east","rect":Rect2(51,45,114,64),"pivot":Vector2(897,511),"width":391.0,"outline":[Vector2(704,315),Vector2(716,289),Vector2(735,273),Vector2(756,267),Vector2(764,215),Vector2(781,196),Vector2(785,145),Vector2(1045,145),Vector2(1047,196),Vector2(1071,204),Vector2(1080,225),Vector2(1087,387),Vector2(1090,441),Vector2(1066,492),Vector2(835,496),Vector2(817,511),Vector2(745,511),Vector2(718,497),Vector2(706,473)]},
		{"id":"battery_breaker","rect":Rect2(-168,62,72,44),"pivot":Vector2(352,1046),"width":429.0,"outline":[Vector2(172,713),Vector2(465,713),Vector2(466,703),Vector2(499,703),Vector2(511,720),Vector2(516,848),Vector2(543,848),Vector2(549,884),Vector2(565,896),Vector2(567,915),Vector2(550,932),Vector2(551,978),Vector2(564,990),Vector2(560,1016),Vector2(542,1024),Vector2(518,1044),Vector2(170,1046),Vector2(161,1028),Vector2(146,983),Vector2(138,955),Vector2(147,927),Vector2(145,810),Vector2(153,779),Vector2(169,773)]},
		{"id":"battery_distribution","rect":Rect2(-90,110,58,36),"pivot":Vector2(920,1048),"width":341.0,"outline":[Vector2(751,809),Vector2(768,783),Vector2(785,764),Vector2(833,764),Vector2(847,754),Vector2(951,752),Vector2(980,765),Vector2(1022,765),Vector2(1047,798),Vector2(1075,807),Vector2(1091,833),Vector2(1091,981),Vector2(1077,1010),Vector2(1056,1021),Vector2(1045,1038),Vector2(863,1048),Vector2(849,1033),Vector2(752,1033)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/battery-composition-v4.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("424546"),Color(0.12,0.14,0.15,0.4),2)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
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

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="battery_bank_west":
		for column in range(4):
			for row in range(5):
				if row>int(fposmod(time*2+column,6)): continue
				var p := Vector2(232+column*76,428-row*13)
				marks.append([p,p+Vector2(9,0)])
	elif prop.id=="battery_bank_east":
		for column in range(3):
			var p := Vector2(830+column*76,331+8*sin(time*2+column))
			marks.append([p,p+Vector2(10,0)])
	elif prop.id=="battery_breaker":
		for row in range(3):
			marks.append([Vector2(355,779+row*15),Vector2(381+19*sin(time*2+row),779+row*15)])
	return marks

func is_animated_prop(prop: Dictionary) -> bool:
	return prop.id in ["battery_bank_west","battery_bank_east","battery_breaker"]

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in FLOOR_CUTOUTS.get(prop.id,[prop.registration.outline]):
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)
	if dressing!=null: dressing.draw_supported(prop)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("d9b36c"),1.15,true)
