extends "res://rooms/whole-room/life_support_view.gd"
## Central reactor: south-facing assemblies, perimeter circulation, canonical shell.
var cooler_render_pieces: Array=[]
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func rebuild() -> void:
	super.rebuild()
	if dressing!=null: dressing.place()
func _ready() -> void:
	super._ready()
	var img := Image.new()
	if img.load("res://rooms/underwater/reactor/source-v1.png") != OK: push_error("Failed to load image (rooms/whole-room/reactor_view.gd:12)")
	life_texture = ImageTexture.create_from_image(img)
	life_items = [
		{"id":"reactor_chamber","rect":Rect2(-52,-40,104,80),"pivot":Vector2(619,806),"width":292.0,"outline":[Vector2(474,550),Vector2(483,523),Vector2(505,523),Vector2(505,461),Vector2(519,428),Vector2(548,400),Vector2(591,383),Vector2(643,383),Vector2(687,399),Vector2(716,426),Vector2(734,461),Vector2(734,523),Vector2(753,534),Vector2(766,553),Vector2(766,793),Vector2(753,806),Vector2(487,806),Vector2(474,793)]},
		{"id":"reactor_cooler","rect":Rect2(-164,-150,70,54),"pivot":Vector2(262,358),"width":244.0,"outline":[Vector2(151,115),Vector2(324,115),Vector2(332,124),Vector2(332,144),Vector2(356,144),Vector2(367,151),Vector2(373,166),Vector2(373,197),Vector2(384,208),Vector2(384,334),Vector2(337,346),Vector2(334,358),Vector2(143,358),Vector2(140,342),Vector2(149,126)]},
		{"id":"reactor_console","rect":Rect2(94,119,70,34),"pivot":Vector2(973,1078),"width":281.0,"outline":[Vector2(860,870),Vector2(1084,870),Vector2(1098,879),Vector2(1098,911),Vector2(1112,919),Vector2(1112,1067),Vector2(1100,1078),Vector2(1072,1078),Vector2(1072,1064),Vector2(871,1064),Vector2(871,1078),Vector2(842,1078),Vector2(831,1066),Vector2(831,921),Vector2(847,911),Vector2(847,882)]}
	]
	dressing=Dressing.new(self,"res://rooms/whole-room/reactor-composition-v2.json")
	rebuild()
	actor = Vector2(0,120)

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	if dressing!=null: dressing.floor()
	preload("res://rooms/whole-room/room_services.gd").render(painter,props,"reactor",operating)

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	# Department finish only: retain canonical wall faces and low cutaway depth.
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("242625"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(125,45,220,38) if horizontal else Rect2(55,110,31,220))
		cursor+=length
	var trim:=Rect2(top.position+Vector2(0,top.size.y-2),Vector2(top.size.x,1)) if horizontal else Rect2(top.position+Vector2(top.size.x-2,0),Vector2(1,top.size.y))
	painter.draw_rect(trim,Color("98602e"))

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("242625"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(56,46,29,33))

func render_polygons(prop: Dictionary) -> Array:
	var outline:=PackedVector2Array(prop.registration.outline)
	if prop.id!="reactor_cooler": return [outline]
	if cooler_render_pieces.is_empty():
		# Only verified source floor inside the return loop; retain its base plate.
		var gap:=Rect2(335,182,7,98)
		var size:=Vector2(life_texture.get_size())
		for region in [Rect2(0,0,size.x,gap.position.y),Rect2(0,gap.end.y,size.x,size.y-gap.end.y),Rect2(0,gap.position.y,gap.position.x,gap.size.y),Rect2(gap.end.x,gap.position.y,size.x-gap.end.x,gap.size.y)]:
			var rect: Rect2=region
			var clip:=PackedVector2Array([rect.position,Vector2(rect.end.x,rect.position.y),rect.end,Vector2(rect.position.x,rect.end.y)])
			cooler_render_pieces.append_array(Geometry2D.intersect_polygons(outline,clip))
	return cooler_render_pieces

func draw_registered_prop(prop: Dictionary) -> void:
	draw_prop_base(prop)
	draw_prop_animation(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	for outline in render_polygons(prop):
		var vertices := PackedVector2Array()
		var uv := PackedVector2Array()
		for p in outline:
			vertices.append(life_point(prop,p))
			uv.append(p/Vector2(life_texture.get_size()))
		draw_cached_polygon(vertices,uv,life_texture)

func draw_prop_animation(prop: Dictionary) -> void:
	if prop.registration.get("dressing",false): return
	if not operating: return
	if prop.id=="reactor_chamber":
		for i in range(3):
			var y := 632.0+i*14
			var a := life_point(prop,Vector2(592,y))
			var b := life_point(prop,Vector2(648,y))
			painter.draw_line(a,b,Color(0.85,0.53,0.17,0.25+0.18*sin(machine_clock*2-i)),1.5,true)
	elif prop.id=="reactor_console":
		var a := life_point(prop,Vector2(895,940))
		painter.draw_line(a,a+Vector2(9+3*sin(machine_clock*2),0),Color("6aa896"),1.0,true)

func layout_caption() -> String:
	return "REACTOR / perimeter circulation / south-facing / %d degrees"%(quarter*90)
