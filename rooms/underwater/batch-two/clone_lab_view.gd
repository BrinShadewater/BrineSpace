extends "res://rooms/whole-room/life_support_view.gd"
## Medical host with localized biological vessels and scientific instruments.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func _ready() -> void:
	super._ready()
	var image:=Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://assets/material-polish-v2/clone-equipment.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"clone_vessel","rect":Rect2(-148,-118,64,65),"pivot":Vector2(338,550),"width":214.0,"outline":[Vector2(316,101),Vector2(361,101),Vector2(393,114),Vector2(416,137),Vector2(430,167),Vector2(430,196),Vector2(421,213),Vector2(421,365),Vector2(437,383),Vector2(445,412),Vector2(445,519),Vector2(428,539),Vector2(402,550),Vector2(272,550),Vector2(246,539),Vector2(233,520),Vector2(233,412),Vector2(241,384),Vector2(253,365),Vector2(254,213),Vector2(246,197),Vector2(249,157),Vector2(266,130),Vector2(289,113)]},
		{"id":"clone_incubator","rect":Rect2(63,-125,98,75),"pivot":Vector2(889,540),"width":308.0,"outline":[Vector2(878,142),Vector2(900,142),Vector2(915,149),Vector2(921,154),Vector2(936,154),Vector2(952,161),Vector2(976,174),Vector2(977,177),Vector2(1006,177),Vector2(1017,185),Vector2(1017,283),Vector2(1037,302),Vector2(1040,510),Vector2(1032,518),Vector2(978,519),Vector2(978,529),Vector2(968,539),Vector2(808,539),Vector2(797,529),Vector2(797,518),Vector2(747,518),Vector2(738,510),Vector2(738,258),Vector2(746,251),Vector2(756,251),Vector2(756,184),Vector2(763,177),Vector2(790,177),Vector2(797,184),Vector2(797,174),Vector2(818,162),Vector2(837,154),Vector2(858,154),Vector2(865,148)]},
		{"id":"clone_nutrients","rect":Rect2(-151,96,78,59),"pivot":Vector2(328,1032),"width":228.0,"outline":[Vector2(227,779),Vector2(429,779),Vector2(441,795),Vector2(442,1019),Vector2(433,1032),Vector2(222,1032),Vector2(215,1018),Vector2(215,802)]},
		{"id":"clone_console","rect":Rect2(67,99,94,56),"pivot":Vector2(886,1013),"width":254.0,"outline":[Vector2(771,814),Vector2(1001,814),Vector2(1011,829),Vector2(1011,1002),Vector2(1003,1013),Vector2(768,1013),Vector2(758,1002),Vector2(758,830)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/clone-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=0 # Canonical west/east/south tee.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("a9b4b2"),Color(0.20,0.32,0.32,0.13),2,"sealed")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"sealed")
	if dressing!=null: dressing.floor()

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	match prop.id:
		"clone_vessel":
			for i in range(4):
				var p:=Vector2(283+i*33,406-fposmod(time*24+i*19,133))
				marks.append([p,p+Vector2(0,4)])
		"clone_incubator":
			var hub:=Vector2(888,329)
			var axis:=Vector2.from_angle(time*1.8)
			marks.append([hub+axis*8,hub+axis*27])
		"clone_nutrients":
			for i in range(3):
				var p:=Vector2(267+i*50,886-fposmod(time*14+i*9,29))
				marks.append([p,p+Vector2(0,5)])
		"clone_console":
			for row in range(3): marks.append([Vector2(910,844+row*13),Vector2(942+sin(time*1.7+row)*20,844+row*13)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("a6cbbd"),1.0,true)

func layout_caption() -> String:
	return "CLONE LAB / south-facing equipment / %d degrees"%(quarter*90)

# Use this room's repainted structural material, with the existing low hull geometry.
func draw_wall(rect: Rect2, horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("202d32"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(94,49,123,39) if horizontal else Rect2(40,98,36,114))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(39,45,43,43))
