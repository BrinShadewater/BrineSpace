extends "res://rooms/whole-room/nursery_south_facing.gd"
## North-facing three-wall reading installation; shared south doorway and crew depth.
var installation: ImageTexture
var overhead_shelves: ImageTexture
var rotated_textures: Dictionary={}
func furnishing_texture(id: String) -> ImageTexture:
	var key:=id+"-q"+str(quarter)
	if not rotated_textures.has(key):
		var path: String="res://assets/rooms/observation-room/pack/"+key+".png"
		if id=="observation_north":path="res://assets/rooms/observation-room/pack/shelves-"+["down","left","up","right"][quarter]+".png"
		rotated_textures[key]=load_source_texture(path)
	return rotated_textures[key]

func furnishing_bounds(prop: Dictionary) -> Rect2:
	var size:=Vector2(furnishing_texture(prop.id).get_size())
	size*=minf(prop.rect.size.x/size.x,prop.rect.size.y/size.y)
	return Rect2(prop.rect.get_center()-size*0.5,size)

func furnishing_point(prop: Dictionary, point: Vector2) -> Vector2:
	var p:=point
	match quarter:
		1:p=Vector2(1.0-point.y,point.x)
		2:p=Vector2(1.0-point.x,1.0-point.y)
		3:p=Vector2(point.y,1.0-point.x)
	var bounds:=furnishing_bounds(prop)
	return bounds.position+p*bounds.size

func draw_reading_light(prop: Dictionary) -> void:
	# A reading lamp is steady while powered, with no machine-clock pulsing.
	if not operating:return
	var points:=PackedVector2Array()
	for p in [Vector2(.31,.39),Vector2(.70,.39),Vector2(.70,.88),Vector2(.31,.88)]:
		points.append(furnishing_point(prop,p))
	painter.draw_colored_polygon(points,Color(1.0,.79,.40,.10))
var source_registration := {}
const ART_ORIGIN := Vector2(-180,-258)
var art_scale:=1.0
var source_origin:=Vector2.ZERO
var office_textures: Dictionary={}
var office_regions: Dictionary={}
const DirectionalLibrary=preload("res://scripts/room_asset_library.gd")

func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library=ActorLibrary.new()
	set_process(false)
	set_process_unhandled_key_input(false)
	show_actor=false
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://legacy/default/assets/rooms/observation-room/source/overhead.png")
	installation=ImageTexture.create_from_image(image)
	overhead_shelves=load_source_texture("res://legacy/default/assets/rooms/observation-room/pack/shelves-down.png")
	source_registration=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/underwater/observation-room-v1/registration.json"))
	var region: Array=source_registration.region
	art_scale=360.0/float(region[2])
	source_origin=Vector2(region[0],region[1])
	for id in ["wooden-desk","chair-rear","reading-set"]:
		var item:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(item, "res://assets/rooms/observation-room/office/"+id+".png")
		office_textures[id]=ImageTexture.create_from_image(item)
		office_regions[id]=Rect2(item.get_used_rect())
	rebuild()

func rebuild() -> void:
	pair_mode=0
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	props.clear()
	for part in source_registration.get("parts",[]):
		if part.id=="observation_north":
			var shelf_rect:=Rect2(-180,-180,360,48)
			props.append({"id":part.id,"rect":shelf_rect,"sort_y":shelf_rect.end.y,"center":Vector2.ZERO,"registration":{"overhead_shelf":true}})
			continue
		if part.id in ["observation_west","observation_east"]:
			var west: bool=part.id=="observation_west"
			var asset: String="library/side-observation-shelves-"+("west" if west else "east")
			var prop: Dictionary=DirectionalLibrary.template(asset).duplicate(true)
			var width: float=274.0*prop.registration.width/prop.registration.height
			prop.id=part.id
			prop.rect=Rect2(-180.0 if west else 180.0-width,-104.0,width,274.0)
			prop.sort_y=170.0
			props.append(prop)
			continue
		var r: Array=part.footprint
		var rect:=Rect2(r[0],r[1],r[2],r[3])
		rect.position.y-=78.0
		props.append({"id":part.id,"rect":rect,"sort_y":rect.end.y,"center":Vector2.ZERO,"registration":part})
	for id in ["wooden-desk","chair-rear"]:
		if not office_textures.has(id): continue
		var rect:=Rect2(-72,-8,144,75) if id=="wooden-desk" else Rect2(-23,87,46,44)
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{"office":true}})
	for prop in props:
		prop["overhead_furnishing"]=true
		prop["library_asset"]=false
		var original: Rect2=prop.rect
		var size: Vector2=original.size if quarter%2==0 else Vector2(original.size.y,original.size.x)
		prop.rect=Rect2(Geometry.turn(original.get_center(),quarter)-size*0.5,size)
		prop.sort_y=prop.rect.end.y
		prop["center"]=Vector2.ZERO
	actor=Vector2.ZERO
	queue_redraw()

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("overhead_furnishing",false):return furnishing_bounds(prop)
	if prop.registration.get("overhead_shelf",false): return prop.rect
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
	if prop.get("overhead_furnishing",false):
		painter.draw_texture_rect(furnishing_texture(prop.id),furnishing_bounds(prop),false)
		if prop.id=="wooden-desk":draw_reading_light(prop)
		return
	if prop.registration.get("overhead_shelf",false):
		painter.draw_texture_rect(overhead_shelves,prop.rect,false)
		return
	if prop.get("library_asset",false):
		DirectionalLibrary.draw(self,prop)
		return
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

func layout_caption() -> String: return "OBSERVATION ROOM / window opposite the entrance"
