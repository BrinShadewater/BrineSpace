extends "res://rooms/whole-room/life_support_view.gd"
## Two compact berths; static furniture, localized desk activity only.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/whole-room/crew-hab-source-v1.png")) != OK: push_error("Failed to load image (rooms/whole-room/crew_hab_view.gd:8)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"hab_berth_west","rect":Rect2(-163,-154,62,92),"pivot":Vector2(272,460),"width":198.0,"outline":[Vector2(175,128),Vector2(187,114),Vector2(349,114),Vector2(365,128),Vector2(369,443),Vector2(357,460),Vector2(182,460),Vector2(172,444)]},
		{"id":"hab_berth_east","rect":Rect2(-82,-154,84,92),"pivot":Vector2(995,458),"width":258.0,"outline":[Vector2(870,125),Vector2(884,113),Vector2(1108,117),Vector2(1125,128),Vector2(1125,302),Vector2(1053,311),Vector2(1053,441),Vector2(1043,458),Vector2(875,458),Vector2(867,441)]},
		{"id":"hab_desk","rect":Rect2(-132,100,96,54),"pivot":Vector2(292,1039),"width":277.0,"outline":[Vector2(171,797),Vector2(413,797),Vector2(430,813),Vector2(430,1037),Vector2(338,1037),Vector2(336,948),Vector2(321,948),Vector2(321,1039),Vector2(253,1039),Vector2(253,948),Vector2(177,948),Vector2(176,1039),Vector2(156,1039),Vector2(156,814)]},
		{"id":"hab_chair","rect":Rect2(82,-76,76,50),"pivot":Vector2(966,1064),"width":275.0,"outline":[Vector2(860,800),Vector2(1003,800),Vector2(1020,818),Vector2(1028,858),Vector2(1082,868),Vector2(1102,889),Vector2(1102,1051),Vector2(1088,1064),Vector2(839,1064),Vector2(828,1049),Vector2(829,870),Vector2(846,849),Vector2(846,818)]}
	]
	dressing=Dressing.new(self,"res://rooms/whole-room/crew-hab-composition-v3.json")
	rebuild()
func rebuild() -> void:
	super.rebuild()
	for prop in props:
		if quarter==1 and prop.id in ["hab_berth_west","hab_berth_east"]:
			var at:=Vector2(116,-113) if prop.id=="hab_berth_west" else Vector2(116,8)
			prop.rect.position=at-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
		if quarter==3 and prop.id in ["hab_berth_west","hab_berth_east"]:
			var at:=Vector2(-124,101) if prop.id=="hab_berth_west" else Vector2(-132,-20)
			prop.rect.position=at-prop.rect.size*0.5
			prop.sort_y=prop.rect.end.y
		if quarter==3 and prop.id in ["hab_chair","hab_reading_lamp"]:
			# Keep the rear reading pose inside the low north-hull silhouette.
			# Host-linked mat follows the chair; book storage stays against the wall.
			prop.rect.position.y+=32.0
			prop.sort_y=prop.rect.end.y
	layout[0].kind=0 # Canonical west/east/south tee, not Life Support's four ports.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("454442"),Color(0.13,0.13,0.12,0.4),2,"warm")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"hab_rug")
	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").render(painter,props,"crew",operating)
func effect_marks(prop: Dictionary,time: float) -> Array:
	if prop.id!="hab_desk": return []
	var marks: Array=[]
	for line in range(3): marks.append([Vector2(249,829+line*12),Vector2(275+12*sin(time*1.5+line),829+line*12)])
	return marks
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="hab_desk"
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
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("c5b495"),1.0,true)
