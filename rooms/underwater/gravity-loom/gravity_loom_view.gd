extends "res://rooms/whole-room/life_support_view.gd"
## Gravity Loom: a complete low apparatus with clear perimeter circulation.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="loom_apparatus"
func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/gravity-loom/source-v2.png")) != OK: push_error("Failed to load image (rooms/underwater/gravity-loom/gravity_loom_view.gd:12)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[{"id":"loom_apparatus","rect":Rect2(-90,-60,180,120),"pivot":Vector2(626,946),"width":660.0,"outline":[Vector2(297,595),Vector2(309,580),Vector2(334,568),Vector2(349,509),Vector2(378,457),Vector2(416,414),Vector2(459,378),Vector2(512,353),Vector2(567,337),Vector2(568,319),Vector2(585,299),Vector2(657,297),Vector2(681,315),Vector2(687,337),Vector2(741,354),Vector2(795,382),Vector2(840,420),Vector2(875,468),Vector2(902,520),Vector2(918,568),Vector2(941,581),Vector2(957,600),Vector2(957,650),Vector2(943,672),Vector2(918,683),Vector2(901,740),Vector2(872,792),Vector2(833,836),Vector2(787,871),Vector2(736,897),Vector2(687,914),Vector2(680,934),Vector2(660,947),Vector2(591,947),Vector2(572,933),Vector2(566,913),Vector2(510,897),Vector2(456,870),Vector2(412,834),Vector2(374,789),Vector2(347,738),Vector2(333,684),Vector2(310,674),Vector2(297,655)]}]
	dressing=Dressing.new(self,"res://rooms/underwater/gravity-loom/loom-composition-v2.json")
	rebuild()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("303238"),Color(0.13,0.14,0.17,0.25),2,"technical")
	RoomFloor.draw_dressing(painter,center,edges,"technical")
	if dressing!=null: dressing.floor()

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for point in prop.registration.outline:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("b59acd"),1.0,true)
	for index in range(3):
		var angle := machine_clock*0.7+index*TAU/3
		var point := Vector2(626,624)+Vector2(cos(angle),sin(angle))*64
		var fragment := PackedVector2Array()
		for corner in [Vector2(-4,-2),Vector2(2,-4),Vector2(5,2),Vector2(-2,4)]:
			fragment.append(life_point(prop,point+corner))
		painter.draw_colored_polygon(fragment,Color("b7b0c2"))

func effect_marks(prop: Dictionary,time: float) -> Array:
	if not is_animated_prop(prop): return []
	var marks: Array=[]
	for index in range(8):
		var angle := index*TAU/8+time*0.25
		marks.append([Vector2(626,624)+Vector2(cos(angle),sin(angle))*197,Vector2(626,624)+Vector2(cos(angle+0.07),sin(angle+0.07))*197])
	return marks

func layout_caption() -> String:
	return "GRAVITY LOOM / perimeter circulation / %d degrees"%(quarter*90)
