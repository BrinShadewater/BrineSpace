extends "res://rooms/whole-room/life_support_view.gd"
## Crew-style BRINE floats behind the chamber's water, reflections and front rim.
var body_texture: Texture2D
const BODY_RECT := Rect2(521,575,210,210)
const NAMEPLATE := Rect2(555,535,142,34)
var architect_pod: Dictionary = {}:
	set(value):
		var changed := architect_pod.is_empty()!=value.is_empty()
		architect_pod=value
		if changed: layout.clear() # Invalidate the shared geometry cache only when furniture changes.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="brine_chamber"
func prop_visual_bounds(prop: Dictionary) -> Rect2:
	var bounds: Rect2=super.prop_visual_bounds(prop)
	if prop.id=="brine_chamber":
		bounds=bounds.merge(Rect2(life_point(prop,NAMEPLATE.position),NAMEPLATE.size*prop.rect.size.x/prop.registration.width))
	return bounds
func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
	if not architect_pod.is_empty():
		var source: Rect2=preload("res://scripts/architects.gd").CORE_POD_RECT
		var center:=Geometry.turn(source.get_center(),quarter)
		var rect:=Rect2(center-source.size/2,source.size)
		props.append({"id":"architect_pod","rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{"rect":source,"pivot":Vector2(210,560),"width":290.0,"outline":[Vector2(30,70),Vector2(365,70),Vector2(365,610),Vector2(30,610)]}})
func _ready() -> void:
	super._ready()
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/brine-core/source-v1.png")) != OK: push_error("Failed to load image (rooms/underwater/brine-core/brine_core_view.gd:30)")
	life_texture=ImageTexture.create_from_image(image)
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/brine-core/renewal-v2/brine-float-v4.png")) != OK: push_error("Failed to load image (rooms/underwater/brine-core/brine_core_view.gd:32)")
	body_texture=ImageTexture.create_from_image(image)
	life_items=[{"id":"brine_chamber","rect":Rect2(-52,-40,104,80),"pivot":Vector2(626,879),"width":286.0,"outline":[Vector2(512,459),Vector2(517,429),Vector2(538,404),Vector2(570,384),Vector2(603,375),Vector2(649,375),Vector2(686,386),Vector2(718,407),Vector2(737,434),Vector2(743,460),Vector2(743,670),Vector2(760,695),Vector2(770,722),Vector2(770,808),Vector2(757,836),Vector2(730,858),Vector2(690,873),Vector2(648,880),Vector2(603,879),Vector2(562,870),Vector2(525,853),Vector2(500,830),Vector2(484,797),Vector2(484,719),Vector2(493,696),Vector2(511,674)]}]
	dressing=Dressing.new(self,"res://rooms/underwater/brine-core/renewal-v2/composition.json")
	rebuild()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("303b40"),Color(0.10,0.17,0.19,0.22),2,"sealed")
	RoomFloor.draw_dressing(painter,center,edges,"sealed")
	if dressing!=null: dressing.floor()
	for prop in props:
		if prop.id=="brine_chamber":
			preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"specimen_alignment_ring",prop.rect.grow(10))
	# Flush workstation mats and tank contact shadow add grounding without blockers.
	for prop in props:
		if prop.id in ["brine_dual_workstation","brine_diagnostics"]:
			var pad: Rect2=prop.rect.grow(5)
			pad.size.y+=12
			painter.draw_rect(pad,Color(0.07,0.13,0.15,0.5))
			painter.draw_rect(pad.grow(-2),Color(0.35,0.48,0.48,0.25),false,0.75)
		elif prop.id=="brine_chamber":
			var shadow:=PackedVector2Array()
			for i in range(40):
				var a:=i*TAU/40.0
				shadow.append(Vector2(prop.rect.get_center().x,prop.rect.end.y-3)+Vector2(cos(a)*53,sin(a)*12))
			painter.draw_colored_polygon(shadow,Color(0.025,0.065,0.075,0.20))

var retain_brine_parts := not OS.get_cmdline_user_args().has("--redraw-brine-parts")

func retained_prop_passes(prop: Dictionary) -> Array:
	if not retain_brine_parts:
		return [{"method":"draw_registered_prop","live":is_animated_prop(prop) or prop.registration.get("dressing",false)}]
	if prop.id=="architect_pod": return [{"method":"draw_prop_occupant","live":true}]
	if prop.registration.get("dressing",false):
		return [{"method":"draw_prop_base","live":false},{"method":"draw_prop_occupant","live":true}]
	return [{"method":"draw_prop_base","live":false},{"method":"draw_prop_occupant","live":true},
		{"method":"draw_prop_glass","live":false},{"method":"draw_prop_bubbles","live":true},
		{"method":"draw_prop_front","live":false}]

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id=="architect_pod":
		draw_prop_occupant(prop)
		return
	draw_prop_base(prop)
	draw_prop_occupant(prop)
	if prop.registration.get("dressing",false): return
	draw_prop_glass(prop)
	draw_prop_bubbles(prop)
	draw_prop_front(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for point in prop.registration.outline:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)

func draw_prop_occupant(prop: Dictionary) -> void:
	if prop.id=="architect_pod":
		preload("res://scripts/architect_cryo_art.gd").draw(painter,prop.rect,architect_pod)
		return
	if prop.registration.get("dressing",false):
		if operating: draw_computer_display(prop)
		return
	var scale: float=prop.rect.size.x/prop.registration.width
	var drift := float_offset(machine_clock) if operating else Vector2.ZERO
	painter.draw_texture_rect(body_texture,Rect2(life_point(prop,BODY_RECT.position+drift),BODY_RECT.size*scale),false,Color(0.79,0.88,0.91))

func draw_prop_glass(prop: Dictionary) -> void:
	# Foreground water and reflections cross the body, rather than sitting behind it.
	glass_polygon(prop,[Vector2(555,576),Vector2(695,576),Vector2(697,738),Vector2(680,762),Vector2(652,775),Vector2(601,775),Vector2(571,761),Vector2(553,739)],Color(0.15,0.53,0.58,0.14))
	glass_polygon(prop,[Vector2(582,577),Vector2(602,579),Vector2(626,768),Vector2(612,773)],Color(0.70,0.90,0.91,0.12))
	glass_polygon(prop,[Vector2(665,578),Vector2(671,577),Vector2(692,738),Vector2(686,749)],Color(0.77,0.93,0.94,0.17))

func draw_prop_bubbles(prop: Dictionary) -> void:
	if operating:
		for mark in effect_marks(prop,machine_clock):
			painter.draw_circle(life_point(prop,mark[0]),0.6,Color(0.67,0.87,0.89,0.65),false,0.5,true)

func draw_prop_front(prop: Dictionary) -> void:
	# Repaint the real ceramic front lip after the occupant. It is an occluder.
	var rim := [Vector2(515,754),Vector2(540,778),Vector2(576,794),Vector2(624,801),Vector2(671,795),Vector2(711,779),Vector2(738,753),Vector2(738,800),Vector2(715,832),Vector2(681,850),Vector2(628,857),Vector2(576,850),Vector2(540,832),Vector2(516,803)]
	var vertices := PackedVector2Array()
	var uv := PackedVector2Array()
	for point in rim:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	# The cap also belongs in front of the occupant, never behind her hair.
	var cap := [Vector2(512,459),Vector2(517,429),Vector2(538,404),Vector2(570,384),Vector2(603,375),Vector2(649,375),Vector2(686,386),Vector2(718,407),Vector2(737,434),Vector2(743,460),Vector2(743,526),Vector2(728,552),Vector2(685,574),Vector2(640,583),Vector2(602,582),Vector2(559,568),Vector2(528,547),Vector2(512,521)]
	vertices.clear()
	uv.clear()
	for point in cap:
		vertices.append(life_point(prop,point))
		uv.append(point/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	for x in [553.0,701.0]:
		painter.draw_line(life_point(prop,Vector2(x,577)),life_point(prop,Vector2(x,735)),Color(0.55,0.83,0.85,0.32),0.8,true)
	draw_nameplate(prop)

func draw_nameplate(prop: Dictionary) -> void:
	var scale: float=prop.rect.size.x/prop.registration.width
	var rect:=Rect2(life_point(prop,NAMEPLATE.position),NAMEPLATE.size*scale)
	# A flush enamel marking covers the old collar seam beneath the lettering.
	painter.draw_rect(rect,Color("c9cec5"))
	var font:=ThemeDB.fallback_font
	var size:=11
	var text_size:=font.get_string_size("BRINE",HORIZONTAL_ALIGNMENT_LEFT,-1,size)
	var at:=Vector2(rect.get_center().x-text_size.x*0.5,rect.get_center().y+(font.get_ascent(size)-font.get_descent(size))*0.5)
	# Printed directly on the pearl upper collar; no separate sign or supports.
	painter.draw_string(font,at,"BRINE",HORIZONTAL_ALIGNMENT_LEFT,-1,size,Color("29484a"))

func glass_polygon(prop: Dictionary, source: Array, color: Color) -> void:
	var points:=PackedVector2Array()
	for point in source: points.append(life_point(prop,point))
	painter.draw_colored_polygon(points,color)

func float_offset(time: float) -> Vector2:
	return Vector2(sin(time*TAU/11.0)*1.2,sin(time*TAU/8.0)*5.0)

func draw_computer_display(prop: Dictionary) -> void:
	if prop.id=="brine_server":
		for i in range(4):
			painter.draw_rect(Rect2(life_point(prop,Vector2(1242,466+i*44)),Vector2(1.5,0.65)),Color("79aba8") if i!=2 else Color("baad79"))
	var screens: Array[Rect2]=[]
	if prop.id=="brine_dual_workstation": screens=[Rect2(198,346,148,66),Rect2(441,346,142,66)]
	elif prop.id=="brine_diagnostics": screens=[Rect2(877,366,112,59)]
	for screen_index in range(screens.size()):
		var screen: Rect2=screens[screen_index]
		if screen_index==1:
			for column in range(5):
				var start:=screen.position+Vector2(column*27+8,screen.size.y)
				var height:=18.0+float((column*17)%41)
				painter.draw_line(life_point(prop,start),life_point(prop,start-Vector2(0,height)),Color(0.40,0.65,0.62,0.8),1.3)
			continue
		var points:=PackedVector2Array()
		for i in range(12):
			var p: Vector2 = screen.position+Vector2(screen.size.x*i/11.0,screen.size.y*(0.5+0.18*sin(i*1.8)))
			points.append(life_point(prop,p))
		painter.draw_polyline(points,Color(0.30,0.62,0.64,0.78),0.65,true)
		for line in range(3):
			var a: Vector2 = screen.position+Vector2(0,line*7)
			painter.draw_line(life_point(prop,a),life_point(prop,a+Vector2(screen.size.x*(0.65-line*0.12),0)),Color(0.33,0.53,0.54,0.6),0.5)

func effect_marks(prop: Dictionary,time: float) -> Array:
	if not is_animated_prop(prop): return []
	var phase:=fposmod(time,9.0)
	if phase>1.8: return []
	var point:=Vector2(668+sin(phase*3.0)*2.0,743-phase/1.8*150)
	return [[point,point]] # One brief bubble, followed by more than seven quiet seconds.

func layout_caption() -> String:
	return "BRINE CORE / registered chamber and body / %d degrees"%(quarter*90)

