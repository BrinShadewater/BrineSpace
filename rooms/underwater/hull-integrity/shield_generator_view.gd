extends "res://rooms/whole-room/life_support_view.gd"
## Pressure-hull monitoring and repair machinery; canonical north/south routes.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/hull-integrity/shield_generator-source-v1.png")) != OK: push_error("Failed to load image (rooms/underwater/hull-integrity/shield_generator_view.gd:8)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"hull_monitor","rect":Rect2(-165,-143,108,64),"pivot":Vector2(315,503),"width":405.0,"outline":[Vector2(112,183),Vector2(117,166),Vector2(137,151),Vector2(138,140),Vector2(151,128),Vector2(477,128),Vector2(489,144),Vector2(489,157),Vector2(510,170),Vector2(516,188),Vector2(516,470),Vector2(495,499),Vector2(144,503),Vector2(112,474)]},
		{"id":"hull_test_rig","rect":Rect2(57,-143,108,64),"pivot":Vector2(934,505),"width":394.0,"outline":[Vector2(739,181),Vector2(751,163),Vector2(767,153),Vector2(766,144),Vector2(779,130),Vector2(829,130),Vector2(841,144),Vector2(841,156),Vector2(1028,156),Vector2(1028,142),Vector2(1040,130),Vector2(1091,130),Vector2(1102,144),Vector2(1102,154),Vector2(1123,170),Vector2(1131,187),Vector2(1131,470),Vector2(1101,502),Vector2(768,505),Vector2(739,476)]},
		{"id":"hull_injector","rect":Rect2(-165,92,84,54),"pivot":Vector2(314,1110),"width":387.0,"outline":[Vector2(121,809),Vector2(134,788),Vector2(142,781),Vector2(145,767),Vector2(155,764),Vector2(157,754),Vector2(171,740),Vector2(359,740),Vector2(375,750),Vector2(399,750),Vector2(410,760),Vector2(463,760),Vector2(480,776),Vector2(483,788),Vector2(502,807),Vector2(507,1081),Vector2(481,1108),Vector2(150,1110),Vector2(120,1083)]},
		{"id":"hull_patch_rack","rect":Rect2(80,100,84,54),"pivot":Vector2(935,1110),"width":351.0,"outline":[Vector2(762,804),Vector2(775,782),Vector2(779,754),Vector2(794,744),Vector2(794,734),Vector2(813,734),Vector2(814,741),Vector2(1050,741),Vector2(1050,734),Vector2(1070,734),Vector2(1074,748),Vector2(1088,753),Vector2(1090,772),Vector2(1107,786),Vector2(1110,1082),Vector2(1083,1109),Vector2(786,1110),Vector2(760,1081)]}
	]
	dressing=Dressing.new(self,"res://rooms/underwater/hull-integrity/hull-composition-v3.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("41474a"),Color(0.17,0.19,0.20,0.35),2)
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
		painter.draw_texture_rect_region(life_texture,target,Rect2(240,19,112,46) if horizontal else Rect2(18,280,32,102))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(18,18,40,40))

const SCREEN := Rect2(165,158,245,108)
func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if prop.id=="hull_monitor":
		# Closed pressure-compartment schematic remains within the actual display.
		var corners := [Vector2(195,183),Vector2(374,183),Vector2(374,240),Vector2(195,240)]
		for i in range(4): marks.append([corners[i],corners[(i+1)%4]])
		for x in [240,285,330]: marks.append([Vector2(x,183),Vector2(x,240)])
		var x := 205+fposmod(time*45,158)
		marks.append([Vector2(x,199),Vector2(x,223)])
	elif prop.id=="hull_injector":
		var angle := -1.2+sin(time*2)*0.4
		marks.append([Vector2(422,870),Vector2(422,870)+Vector2(cos(angle),sin(angle))*17])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["hull_monitor","hull_injector"]

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
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("d6b778"),1.0,true)
