extends "res://rooms/whole-room/life_support_view.gd"
## Underwater Life Support: registered south-facing equipment; original art kept.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
func _ready() -> void:
	super._ready()
	var image := Image.new()
	assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/whole-room/life-support-underwater-source-v1.png"))==OK)
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"life_fan","rect":Rect2(-165,-113,108,54),"pivot":Vector2(355,448),"width":326.0,"outline":[Vector2(194,170),Vector2(510,170),Vector2(519,439),Vector2(509,448),Vector2(193,448)]},
		{"id":"life_filter","rect":Rect2(57,-151,108,78),"pivot":Vector2(921,455),"width":358.0,"outline":[Vector2(745,203),Vector2(762,203),Vector2(767,181),Vector2(789,160),Vector2(829,157),Vector2(850,179),Vector2(865,194),Vector2(878,171),Vector2(899,156),Vector2(933,157),Vector2(955,176),Vector2(970,192),Vector2(985,172),Vector2(1008,156),Vector2(1040,161),Vector2(1064,183),Vector2(1071,205),Vector2(1092,205),Vector2(1101,439),Vector2(1086,455),Vector2(744,455)]},
		{"id":"life_tank","rect":Rect2(-165,107,74,42),"pivot":Vector2(330,1015),"width":370.0,"outline":[Vector2(244,742),Vector2(405,742),Vector2(405,734),Vector2(453,734),Vector2(454,742),Vector2(474,742),Vector2(486,761),Vector2(486,780),Vector2(511,787),Vector2(513,1003),Vector2(500,1015),Vector2(195,1015),Vector2(195,958),Vector2(146,958),Vector2(146,882),Vector2(238,880),Vector2(238,755)]},
		{"id":"life_console","rect":Rect2(-80,111,60,38),"pivot":Vector2(925,1020),"width":274.0,"outline":[Vector2(808,773),Vector2(1034,773),Vector2(1045,785),Vector2(1045,807),Vector2(1062,817),Vector2(1062,1010),Vector2(1050,1020),Vector2(788,1020),Vector2(788,811),Vector2(803,807)]}
	]
	dressing=Dressing.new(self,"res://rooms/whole-room/life-support-composition-v3.json")
	rebuild()

func draw_wall(rect: Rect2, horizontal: bool) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("20292b"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(270,72,124,25) if horizontal else Rect2(88,235,29,120))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("bdc7c8"),0.6)

func draw_cap(rect: Rect2) -> void:
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("20292b"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(90,72,30,24))

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("424c4c"),Color(0.1,0.15,0.16,0.45),2,"wet")
	RoomFloor.draw_dressing(painter,center,edges,"wet")
	if dressing!=null: dressing.floor()
	for prop in props:
		if prop.id not in ["life_filter","life_tank"]: continue
		var at := Vector2(prop.rect.get_center().x,prop.rect.end.y+10)
		preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"linear_drain",Rect2(at-Vector2(27,4),Vector2(54,8)))

func effect_marks(prop: Dictionary, time: float) -> Array:
	var marks: Array=[]
	if prop.id=="life_fan":
		for x in [282.0,399.0]:
			for blade in range(3):
				var d := Vector2.from_angle(time*4+blade*TAU/3)
				marks.append([Vector2(x,250)+d*5,Vector2(x,250)+d*21])
	elif prop.id=="life_filter":
		for i in range(3):
			var y := 302-fposmod(time*20+i*11,35)
			marks.append([Vector2(810+i*107,y),Vector2(810+i*107,y+5)])
	elif prop.id=="life_tank":
		for i in range(5):
			var p := Vector2(260+i*45,932-fposmod(time*25+i*17,80))
			marks.append([p,p+Vector2(0,3)])
	elif prop.id=="life_console":
		for line in range(3):
			marks.append([Vector2(853,816+line*13),Vector2(900+22*sin(time*2+line),816+line*13)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	draw_prop_base(prop)
	draw_prop_animation(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.registration.get("dressing",false): return
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("a0c6c4"),1.0,true)
