extends "res://rooms/whole-room/life_support_view.gd"
const HARVEST_SCREEN := Rect2(974,803,62,40)
## Isolated Hydroponics candidate using the proven south-facing cross-room adapter.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
func _ready() -> void:
	super._ready()
	var img := Image.new()
	preload("res://scripts/safe_image.gd").load_png(img, "res://rooms/whole-room/hydroponics-candidate.png")
	life_texture = ImageTexture.create_from_image(img)
	life_items = [
		{"id":"hydro_bed_west","rect":Rect2(-163,-147,106,80),"pivot":Vector2(330,499),"width":348.0,"outline":[Vector2(176,169),Vector2(484,169),Vector2(501,183),Vector2(501,492),Vector2(485,499),Vector2(169,499),Vector2(155,486),Vector2(155,187)]},
		{"id":"hydro_bed_east","rect":Rect2(57,-147,106,80),"pivot":Vector2(924,499),"width":348.0,"outline":[Vector2(770,169),Vector2(1078,169),Vector2(1095,183),Vector2(1095,492),Vector2(1079,499),Vector2(763,499),Vector2(749,486),Vector2(749,187)]},
		{"id":"hydro_nutrients","rect":Rect2(-160,55,66,44),"pivot":Vector2(306,1010),"width":275.0,"outline":[Vector2(173,805),Vector2(198,805),Vector2(198,761),Vector2(208,744),Vector2(232,730),Vector2(255,730),Vector2(281,749),Vector2(285,787),Vector2(311,787),Vector2(312,757),Vector2(329,737),Vector2(354,730),Vector2(378,738),Vector2(398,757),Vector2(400,790),Vector2(428,790),Vector2(440,806),Vector2(440,1003),Vector2(427,1010),Vector2(173,1010)]},
		{"id":"hydro_harvest","rect":Rect2(77,104,88,48),"pivot":Vector2(931,1014),"width":288.0,"outline":[Vector2(804,778),Vector2(1058,778),Vector2(1070,790),Vector2(1077,1001),Vector2(1062,1014),Vector2(797,1014),Vector2(785,1000),Vector2(791,792)]}
	]
	dressing=Dressing.new(self,"res://rooms/whole-room/hydro-composition-v3.json")
	rebuild()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("a4b1a7"),Color(0.18,0.29,0.22,0.16),2,"wet")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"wet")
	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").render(painter,props,"hydro",operating)
	_draw_care_chart(center)

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
	if prop.id=="hydro_harvest":
		# The donor includes a live readout. Own the screen surface in every state.
		painter.draw_rect(Rect2(life_point(prop,HARVEST_SCREEN.position),HARVEST_SCREEN.size*(prop.rect.size.x/prop.registration.width)),Color("0b1314"))
	for lens in status_lenses(prop):
		var surface := Rect2(life_point(prop,lens.position),lens.size*(prop.rect.size.x/prop.registration.width))
		painter.draw_rect(surface,Color("70b781") if operating else Color("344039"))

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.registration.get("dressing",false): return
	if not operating: return
	for mark in effect_marks(prop,machine_clock):
		if prop.id=="hydro_nutrients":
			painter.draw_circle(life_point(prop,mark[0]),0.8,Color("9fced3"),true,-1,true)
		else:
			painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("79b697") if prop.id=="hydro_harvest" else Color("75acb0"),0.8 if prop.id=="hydro_harvest" else 1.1,true)

func status_lenses(prop: Dictionary) -> Array:
	match str(prop.id):
		"hydro_bed_west": return [Rect2(460,430,12,8)]
		"hydro_bed_east": return [Rect2(1054,430,12,8)]
		"hydro_nutrients": return [Rect2(390,924,14,8)]
		"hydro_harvest": return [Rect2(1033,908,13,9)]
	return []

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	if str(prop.id).begins_with("hydro_bed"):
		var offset := 594.0 if prop.id=="hydro_bed_east" else 0.0
		var x := 197.0+fposmod(time*85.0,255.0)
		for y in [273.0,339.0]:
			marks.append([Vector2(x+offset,y),Vector2(x+offset+12,y)])
	elif prop.id=="hydro_nutrients":
		for x in [234.0,350.0]:
			for i in range(3):
				var point := Vector2(x+i*4,858.0-fposmod(time*24+i*19,52.0))
				marks.append([point,point])
	elif prop.id=="hydro_harvest":
		for row in range(3):
			var start := Vector2(981,812+row*9)
			marks.append([start,start+Vector2(24+10*sin(time*2+row),0)])
	return marks

func layout_caption() -> String:
	return "HYDROPONICS / south-facing equipment / %d degrees"%(quarter*90)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	super.draw_wall(rect,horizontal)

func _draw_care_chart(center: Vector2) -> void:
	# Attached to the north hull, including when the station owns a shared wall.
	# Mount spans x=-66..-38, outside the canonical 72-unit door bay.
	var at:=center+Vector2(-52,-182)
	painter.draw_line(at+Vector2(-8,-5),at+Vector2(-8,2),Color("56665e"),2)
	painter.draw_line(at+Vector2(8,-5),at+Vector2(8,2),Color("56665e"),2)
	painter.draw_rect(Rect2(at-Vector2(14,0),Vector2(28,22)),Color("53675c"))
	painter.draw_rect(Rect2(at-Vector2(12,-2),Vector2(24,18)),Color("d5d8be"))
	painter.draw_rect(Rect2(at+Vector2(-8,3),Vector2(16,3)),Color("54705b"))
	for row in range(3):
		painter.draw_rect(Rect2(at+Vector2(-8,8+row*3),Vector2(2,2)),Color("73816a"))
		painter.draw_line(at+Vector2(-3,9+row*3),at+Vector2(8,9+row*3),Color("89917c"),1)
