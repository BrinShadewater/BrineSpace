extends "res://rooms/whole-room/nursery_south_facing.gd"
## North-facing three-wall reading installation; shared south doorway and crew depth.
var installation: ImageTexture
var source_registration := {}
const ART_ORIGIN := Vector2(-180,-180)
var art_scale:=1.0
var source_origin:=Vector2.ZERO
var office_textures: Dictionary={}
var office_regions: Dictionary={}

func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library=ActorLibrary.new()
	set_process(false)
	set_process_unhandled_key_input(false)
	show_actor=false
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/underwater/observation-room-v1/source-v3.png")
	installation=ImageTexture.create_from_image(image)
	source_registration=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/underwater/observation-room-v1/registration.json"))
	var region: Array=source_registration.region
	art_scale=360.0/float(region[2])
	source_origin=Vector2(region[0],region[1])
	for id in ["wooden-desk","chair-rear","reading-set"]:
		var item:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(item, "res://assets/observation-office-v1/"+id+".png")
		office_textures[id]=ImageTexture.create_from_image(item)
		office_regions[id]=Rect2(item.get_used_rect())
	rebuild()

func rebuild() -> void:
	pair_mode=0
	layout=[{"cell":Vector2i.ZERO,"rotation":0,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	props.clear()
	for part in source_registration.get("parts",[]):
		var r: Array=part.footprint
		var rect:=Rect2(r[0],r[1],r[2],r[3])
		props.append({"id":part.id,"rect":rect,"sort_y":rect.end.y,"center":Vector2.ZERO,"registration":part})
	for id in ["wooden-desk","chair-rear"]:
		if not office_textures.has(id): continue
		var rect:=Rect2(-72,36,144,42) if id=="wooden-desk" else Rect2(-23,130,46,18)
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{"office":true}})
	actor=Vector2.ZERO
	queue_redraw()

func configure_embedded(_q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(0,open_sides,running,time_seconds,omitted_sides)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.registration.get("office",false):
		var region: Rect2=office_regions[prop.id]
		var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
		var bounds:=Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size)
		if prop.id=="wooden-desk": bounds=bounds.merge(reading_bounds(prop))
		return bounds
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	var r: Array=prop.registration.bounds
	return Rect2(ART_ORIGIN+(Vector2(r[0],r[1])-source_origin)*art_scale,Vector2(r[2],r[3])*art_scale)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.registration.get("office",false):
		var region: Rect2=office_regions[prop.id]
		var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
		painter.draw_texture_rect_region(office_textures[prop.id],Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size),region)
		if prop.id=="wooden-desk":
			painter.draw_texture_rect_region(office_textures["reading-set"],reading_bounds(prop),office_regions["reading-set"],Color.WHITE if operating else Color(.72,.72,.72))
		return
	for piece in prop.registration.pieces:
		var vertices:=PackedVector2Array()
		var uv:=PackedVector2Array()
		for point in piece:
			var source:=Vector2(point[0],point[1])
			vertices.append(ART_ORIGIN+(source-source_origin)*art_scale)
			uv.append(source/installation.get_size())
		draw_cached_polygon(vertices,uv,installation)

func is_animated_prop(_prop: Dictionary) -> bool: return false

func reading_bounds(prop: Dictionary) -> Rect2:
	var region: Rect2=office_regions["reading-set"]
	var size:=Vector2(64,64*region.size.y/region.size.x)
	# The blotter rests on the desktop, never on the walking floor.
	return Rect2(Vector2(prop.rect.get_center().x-size.x*.5,prop.rect.end.y-58-size.y),size)

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("413b32"),Color(0.12,0.1,0.08,0.35),2,"wood")

func draw_wall(rect: Rect2, horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"habitation")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"habitation")

func layout_caption() -> String: return "OBSERVATION ROOM / north window / south entrance"
