extends "res://rooms/underwater/batch-two/cryo_chamber_view.gd"
## Empty treatment equipment: diagnostic readiness, not imaginary patient vitals.
var center_dressing: RefCounted
func rebuild() -> void:
	super.rebuild()
	if center_dressing!=null: center_dressing.place()
func draw_room_floor(center: Vector2) -> void:
	super.draw_room_floor(center)
	if center_dressing!=null: center_dressing.floor()
func _ready() -> void:
	super._ready()
	cryo_dressing=null # This room replaces the inherited Cryo equipment list.
	var source:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(source, "res://assets/material-polish-medical-v3/center-equipment.png")
	life_texture=ImageTexture.create_from_image(source)
	life_items=[
		{"id":"medical_treatment","rect":Rect2(-153,-147,82,82),"pivot":Vector2(340,539),"width":274.0,"outline":[Vector2(215,229),Vector2(231,219),Vector2(247,219),Vector2(248,213),Vector2(290,213),Vector2(301,222),Vector2(320,224),Vector2(327,236),Vector2(335,226),Vector2(326,215),Vector2(326,202),Vector2(339,188),Vector2(406,204),Vector2(421,210),Vector2(423,195),Vector2(437,193),Vector2(474,213),Vector2(475,250),Vector2(464,261),Vector2(451,257),Vector2(450,333),Vector2(459,342),Vector2(459,526),Vector2(447,539),Vector2(219,539),Vector2(205,525),Vector2(206,290),Vector2(213,283)]},
		{"id":"medical_imaging","rect":Rect2(68,-148,88,84),"pivot":Vector2(886,558),"width":290.0,"outline":[Vector2(749,230),Vector2(760,198),Vector2(783,172),Vector2(817,151),Vector2(842,146),Vector2(929,146),Vector2(960,155),Vector2(989,177),Vector2(1010,204),Vector2(1021,240),Vector2(1021,252),Vector2(1029,259),Vector2(1029,339),Vector2(1021,348),Vector2(1021,429),Vector2(1008,444),Vector2(1007,545),Vector2(994,558),Vector2(780,558),Vector2(766,545),Vector2(766,444),Vector2(749,431),Vector2(741,342),Vector2(741,275),Vector2(747,267)]},
		{"id":"medical_supplies","rect":Rect2(-158,94,96,64),"pivot":Vector2(339,972),"width":292.0,"outline":[Vector2(204,769),Vector2(248,769),Vector2(259,788),Vector2(279,783),Vector2(293,805),Vector2(302,805),Vector2(302,723),Vector2(316,710),Vector2(470,710),Vector2(484,724),Vector2(484,958),Vector2(471,972),Vector2(313,972),Vector2(298,957),Vector2(203,957),Vector2(192,943),Vector2(193,812),Vector2(202,806)],"pieces":[[Vector2(204,769),Vector2(248,769),Vector2(259,788),Vector2(279,783),Vector2(293,805),Vector2(295,943),Vector2(282,957),Vector2(204,957),Vector2(192,944),Vector2(193,812),Vector2(202,806)],[Vector2(302,723),Vector2(316,710),Vector2(470,710),Vector2(484,724),Vector2(484,958),Vector2(471,972),Vector2(313,972),Vector2(300,957)]]},
		{"id":"medical_station","rect":Rect2(64,86,98,74),"pivot":Vector2(890,991),"width":300.0,"outline":[Vector2(742,806),Vector2(755,781),Vector2(771,779),Vector2(773,752),Vector2(828,737),Vector2(841,746),Vector2(845,737),Vector2(929,737),Vector2(937,745),Vector2(1005,751),Vector2(1008,779),Vector2(1024,784),Vector2(1037,802),Vector2(1039,941),Vector2(1026,957),Vector2(934,957),Vector2(919,946),Vector2(917,967),Vector2(924,980),Vector2(919,990),Vector2(910,989),Vector2(889,975),Vector2(869,990),Vector2(858,987),Vector2(858,980),Vector2(868,967),Vector2(865,948),Vector2(843,957),Vector2(755,957),Vector2(742,944)]}
	]
	center_dressing=CryoDressing.new(self,"res://rooms/underwater/batch-two/med-center-composition-v3.json")
	rebuild()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("30413f"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(250,45,110,28) if horizontal else Rect2(57,130,26,76))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("e4e8df"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("30413f"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(58,44,26,24))

func is_animated_prop(prop: Dictionary) -> bool: return prop.id!="medical_supplies" and not prop.registration.get("dressing",false)

func effect_region(prop: Dictionary) -> Rect2:
	match prop.id:
		"medical_treatment": return Rect2(435,217,23,23)
		"medical_imaging": return Rect2(868,231,29,7)
		"medical_station": return Rect2(851,754,74,33)
	return Rect2()

func effect_marks(prop: Dictionary,time: float) -> Array:
	match prop.id:
		"medical_treatment": return [[Vector2(438,224),Vector2(448+sin(time*1.5)*6,224)]]
		"medical_imaging": return [[Vector2(871,234),Vector2(881+sin(time*1.2)*8,234)]]
		"medical_station":
			var marks: Array=[]
			for row in range(3): marks.append([Vector2(855,760+row*9),Vector2(891+sin(time*1.4+row)*24,760+row*9)])
			return marks
	return []

func draw_registered_prop(prop: Dictionary) -> void:
	if center_dressing!=null and center_dressing.draw(prop): return
	for piece in prop.registration.get("pieces",[prop.registration.outline]):
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in piece:
			vertices.append(life_point(prop,point))
			uv.append(point/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)
	if prop.id=="medical_station":
		var region:=effect_region(prop)
		painter.draw_rect(Rect2(life_point(prop,region.position),region.size*prop.rect.size.x/prop.registration.width),Color("182e2d"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("a3c7c0"),0.85,true)

func layout_caption() -> String:
	return "MEDICAL CENTER / empty treatment equipment / %d degrees"%(quarter*90)
