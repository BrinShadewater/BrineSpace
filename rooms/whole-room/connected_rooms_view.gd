extends "res://rooms/whole-room/nursery_south_facing.gd"
## Isolated distinct-room seam test; not enabled in normal station or cards.
var life_texture: ImageTexture
var vertical_pair := false
var life_items := [
	{"id":"life_fan_north","rect":Rect2(-165,-113,108,54),"pivot":Vector2(355,442),"width":326.0,"outline":[Vector2(194,168),Vector2(510,168),Vector2(519,440),Vector2(193,440)]},
	{"id":"life_fan_south","rect":Rect2(-165,97,108,54),"pivot":Vector2(355,1008),"width":326.0,"outline":[Vector2(194,735),Vector2(510,735),Vector2(519,1007),Vector2(193,1007)]},
	{"id":"life_pressure","rect":Rect2(57,-151,108,78),"pivot":Vector2(921,444),"width":330.0,"outline":[Vector2(765,190),Vector2(786,190),Vector2(806,173),Vector2(850,165),Vector2(879,189),Vector2(923,189),Vector2(943,170),Vector2(982,165),Vector2(1017,188),Vector2(1026,177),Vector2(1044,177),Vector2(1044,190),Vector2(1074,190),Vector2(1087,442),Vector2(756,442)]},
	{"id":"life_console","rect":Rect2(58,87,104,64),"pivot":Vector2(925,1017),"width":274.0,"outline":[Vector2(800,780),Vector2(1045,780),Vector2(1062,802),Vector2(1062,1016),Vector2(788,1016),Vector2(788,807)]}
]
func _ready() -> void:
	var img := Image.new()
	if img.load("res://rooms/whole-room/life-support-candidate.png") != OK: push_error("Failed to load image (rooms/whole-room/connected_rooms_view.gd:13)")
	life_texture = ImageTexture.create_from_image(img)
	pair_mode = 1
	super._ready()
func rebuild() -> void:
	pair_mode = 2 if vertical_pair else 1
	super.rebuild()
	layout[1].kind = 2
	edges = Geometry.edges(layout)
	for edge in edges:
		if not edge.shared: edge.open = edge.port
	props = props.filter(func(p: Dictionary)->bool: return p.center==Vector2.ZERO)
	for item in life_items:
		var rect: Rect2 = item.rect
		var center := Vector2(0,384) if vertical_pair else Vector2(384,0)
		rect.position += center
		props.append({"id":item.id,"rect":rect,"center":center,"sort_y":rect.end.y,"registration":item})
func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode==KEY_V:
		vertical_pair = not vertical_pair
		rebuild()
		return
	super._unhandled_key_input(event)
func draw_room_floor(center: Vector2) -> void:
	if center==Vector2.ZERO:
		super.draw_room_floor(center)
		return
	draw_life_floor(center)

func draw_life_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center)
	RoomFloor.draw_dressing(painter,center,edges,"steel")
func life_point(prop: Dictionary, p: Vector2) -> Vector2:
	var r: Dictionary = prop.registration
	return Vector2(prop.rect.get_center().x,prop.rect.end.y)+(p-r.pivot)*(prop.rect.size.x/r.width)
func draw_registered_prop(prop: Dictionary) -> void:
	if not str(prop.id).begins_with("life_"):
		super.draw_registered_prop(prop)
		return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(1254,1254))
	draw_cached_polygon(vertices,uv,life_texture)
	if not operating: return
	if str(prop.id).begins_with("life_fan"):
		var y := 250.0 if prop.id=="life_fan_north" else 818.0
		for x in [282.0,399.0]:
			var hub := life_point(prop,Vector2(x,y))
			var angle := machine_clock*4.0
			# A subpixel orbiting dot vanished at small station zoom. Keep the
			# operating cue inside the fan face, with antialiased radial marks.
			for blade in range(3):
				var direction := Vector2.from_angle(angle+blade*TAU/3.0)
				painter.draw_line(hub+direction*1.5,hub+direction*7.0,Color("aac6c3"),1.5,true)
	if prop.id=="life_console":
		for line in range(3):
			var a := life_point(prop,Vector2(853,816+line*13))
			var b := life_point(prop,Vector2(853+35+22*sin(machine_clock*2+line),816+line*13))
			painter.draw_line(a,b,Color("69aaa1"),1.0,true)
func layout_caption() -> String:
	return "NURSERY + LIFE SUPPORT / V: horizontal or vertical seam"
