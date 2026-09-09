extends "res://rooms/whole-room/life_support_view.gd"
## Dark archive equipment with separately controlled indicator apertures.
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func is_animated_prop(prop: Dictionary) -> bool: return not prop.registration.get("dressing",false)
func rebuild() -> void:
	super.rebuild()
	# Upright cutouts need local clearance, not bitmap rotation. Preserve q1.
	for prop in props:
		if prop.id=="archive_service_cart" and quarter==0:
			prop.rect.position.y+=4.0
		elif prop.id=="archive_task_lamp" and quarter==2:
			prop.rect.position.x+=24.0
		elif prop.id=="archive_task_lamp" and quarter==3:
			prop.rect.position.y+=12.0
	if dressing!=null: dressing.place()
func _ready() -> void:
	super._ready()
	var image:=Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/underwater/batch-two/data_archive-source-v1.png")) != OK: push_error("Failed to load image (rooms/underwater/batch-two/data_archive_view.gd:20)")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[]
	for i in range(2):
		var dx:=650.0*i
		var outline: Array=[]
		for p in [Vector2(216,121),Vector2(379,121),Vector2(384,132),Vector2(393,143),Vector2(393,568),Vector2(381,580),Vector2(214,580),Vector2(203,568),Vector2(203,143),Vector2(210,134),Vector2(213,134)]: outline.append(p+Vector2(dx,0))
		life_items.append({"id":"archive_rack_"+str(i),"rect":Rect2(-143 if i==0 else 85,-135,58,60),"pivot":Vector2(298+dx,580),"width":190.0,"outline":outline,"source_dx":dx})
	life_items.append({"id":"archive_library","rect":Rect2(-154,101,84,55),"pivot":Vector2(307,1071),"width":208.0,"outline":[Vector2(218,810),Vector2(397,810),Vector2(411,824),Vector2(411,1058),Vector2(400,1071),Vector2(215,1071),Vector2(203,1058),Vector2(203,827)]})
	life_items.append({"id":"archive_terminal","rect":Rect2(84,46,80,50),"pivot":Vector2(919,1073),"width":252.0,"outline":[Vector2(812,851),Vector2(1030,851),Vector2(1044,865),Vector2(1044,1062),Vector2(1033,1073),Vector2(805,1073),Vector2(793,1061),Vector2(793,869)]})
	dressing=Dressing.new(self,"res://rooms/underwater/batch-two/archive-composition-v2.json")
	rebuild()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("3b4650"),Color(0.08,0.13,0.17,0.24),2,"technical")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"technical")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("151c25"))
	var span:=rect.size.x if horizontal else rect.size.y
	var cursor:=0.0
	while cursor<span:
		var length:=minf(48,span-cursor)
		var target:=Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(128,44,116,26) if horizontal else Rect2(76,135,25,180))
		cursor+=length
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("a8b1bb"),0.7)

func draw_cap(rect: Rect2) -> void:
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("151c25"))
	painter.draw_texture_rect_region(life_texture,top,Rect2(77,45,27,27))
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("a8b1bb"),0.7)

func display_regions(prop: Dictionary) -> Array:
	var regions: Array=[]
	if str(prop.id).begins_with("archive_rack"):
		var dx: float=prop.registration.source_dx
		for y in [249,286,322,358,394,431,467,504]: regions.append(Rect2(334+dx,y-6,26,12))
		for x in [219,375]: regions.append(Rect2(x+dx-5,565,10,12))
	elif prop.id=="archive_library":
		for x in [242,270,297,324,352,378]: regions.append(Rect2(x-6,1004,12,12))
		for x in [217,399]: regions.append(Rect2(x-5,1049,10,12))
	elif prop.id=="archive_terminal":
		for x in [866,892,917,944,970]: regions.append(Rect2(x-5,912,10,13))
		regions.append(Rect2(970,960,46,20))
		regions.append(Rect2(975,1028,34,11))
		regions.append(Rect2(991,1045,30,11))
		regions.append(Rect2(1000,1007,20,9))
		regions.append(Rect2(820,1041,16,18))
	return regions

func effect_marks(prop: Dictionary,time: float) -> Array:
	var marks: Array=[]
	var regions:=display_regions(prop)
	for i in range(regions.size()):
		var rect: Rect2=regions[i]
		var start:=Vector2(rect.position.x+2,rect.get_center().y)
		var length: float=(rect.size.x-4)*(0.45+0.30*sin(time*2.1+i*0.7))
		marks.append([start,start+Vector2(length,0)])
	return marks

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var vertices:=PackedVector2Array()
	var uv:=PackedVector2Array()
	for p in prop.registration.outline:
		vertices.append(life_point(prop,p))
		uv.append(p/Vector2(life_texture.get_size()))
	draw_cached_polygon(vertices,uv,life_texture)
	# Engine-owned dark apertures cover the source's baked indicator pixels.
	# Source texture is unchanged; power/operation controls the replacement lens.
	for rect in display_regions(prop):
		var a:=life_point(prop,rect.position)
		var b:=life_point(prop,rect.end)
		painter.draw_rect(Rect2(a,b-a),Color("111b23"))
	if not operating: return
	for mark in effect_marks(prop,machine_clock): painter.draw_line(life_point(prop,mark[0]),life_point(prop,mark[1]),Color("6cbbc4"),0.9,true)

func layout_caption() -> String:
	return "DATA ARCHIVE / south-facing racks / %d degrees"%(quarter*90)
