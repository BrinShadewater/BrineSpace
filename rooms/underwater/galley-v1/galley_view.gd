extends "res://rooms/whole-room/nursery_south_facing.gd"
var textures: Dictionary={}
var regions: Dictionary={}
var north_kitchen_art: Dictionary={}
var overhead_textures: Dictionary={}
func overhead_texture(id: String) -> ImageTexture:
	var turn:=quarter
	var source:=id
	if id.begins_with("mess-table"):
		source="table"
		turn=posmod(quarter+1,4)
	var key:=source+"-q"+str(turn)
	if not overhead_textures.has(key):overhead_textures[key]=load_source_texture("res://legacy/retired/assets/rooms/galley/pack/"+key+".png")
	return overhead_textures[key]
func overhead_bounds(prop: Dictionary) -> Rect2:
	var size:=Vector2(overhead_texture(prop.id).get_size())
	size*=minf(prop.rect.size.x/size.x,prop.rect.size.y/size.y)
	return Rect2(prop.rect.get_center()-size*.5,size)
func overhead_point(prop: Dictionary, point: Vector2) -> Vector2:
	var p:=point
	match quarter:
		1:p=Vector2(1-point.y,point.x)
		2:p=Vector2(1-point.x,1-point.y)
		3:p=Vector2(point.y,1-point.x)
	var bounds:=overhead_bounds(prop)
	return bounds.position+p*bounds.size
const DirectionalLibrary=preload("res://scripts/room_asset_library.gd")
func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library=ActorLibrary.new()
	set_process(false)
	show_actor=false
	for id in ["kitchen","serving"]:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://legacy/retired/rooms/underwater/galley-v1/"+id+".png")
		textures[id]=ImageTexture.create_from_image(image)
		regions[id]=Rect2(image.get_used_rect())
	north_kitchen_art=DirectionalLibrary.template("library/galley-kitchen-north").duplicate(true)
	rebuild()
func rebuild() -> void:
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	props.clear()
	for id in ["kitchen","serving"]:
		var rect:=Rect2(-160,-180,320,64) if id=="kitchen" else Rect2(20,74,132,42)
		if id=="serving":
			var prop: Dictionary=DirectionalLibrary.template("library/side-galley-serving-south").duplicate(true)
			var height: float=152.0*prop.registration.height/prop.registration.width
			prop.id=id
			prop.rect=Rect2(32.0,184.0-height,152.0,height)
			prop.sort_y=184.0
			props.append(prop)
			continue
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{},"custom_library_draw":true})
	for index in range(2):
		var rect:=Rect2(-140 if index==0 else 64,-55,76,160)
		props.append({"id":"mess-table-"+str(index),"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{}})
	for prop in props:
		prop.overhead_furnishing=true
		prop.library_asset=false
		var original: Rect2=prop.rect
		var size: Vector2=original.size if quarter%2==0 else Vector2(original.size.y,original.size.x)
		prop.rect=Rect2(Geometry.turn(original.get_center(),quarter)-size*.5,size)
		prop.sort_y=prop.rect.end.y
		prop.center=Vector2.ZERO
	queue_redraw()
func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array=[]) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("overhead_furnishing",false):return overhead_bounds(prop)
	if prop.get("library_asset",false): return DirectionalLibrary.bounds(prop)
	var region: Rect2=regions[prop.id]
	var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
	return Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size)
func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("overhead_furnishing",false):
		painter.draw_texture_rect(overhead_texture(prop.id),overhead_bounds(prop),false)
		if prop.id=="kitchen" and operating:
			var ring:=PackedVector2Array()
			for i in range(33):
				var angle:=TAU*i/32.0
				ring.append(overhead_point(prop,Vector2(.541+cos(angle)*.039,.508+sin(angle)*.196)))
			painter.draw_polyline(ring,Color(.75,.32,.10,.28+.10*sin(machine_clock*2)),.65)
		return
	if prop.get("library_asset",false):
		DirectionalLibrary.draw(self,prop)
		if operating and prop.registration.has("cooktop_ring"):
			var reg: Dictionary=prop.registration
			var ring: Array=reg.cooktop_ring
			var points:=PackedVector2Array()
			var anchor:=Vector2(prop.rect.get_center().x,prop.rect.end.y)
			for i in range(33):
				var angle:=TAU*i/32.0
				var point:=Vector2(ring[0]+cos(angle)*ring[2],ring[1]+sin(angle)*ring[3])
				points.append(anchor+(DirectionalLibrary.source_uv(reg,point)-reg.pivot)*prop.rect.size.x/reg.width)
			painter.draw_polyline(points,Color(.75,.32,.10,.28+.10*sin(machine_clock*2)),.65)
		return
	var bounds:=prop_visual_bounds(prop)
	if prop.id=="kitchen" and not north_kitchen_art.is_empty():
		var artwork:=north_kitchen_art.duplicate()
		artwork.rect=bounds
		DirectionalLibrary.draw(self,artwork)
	else:
		painter.draw_texture_rect_region(textures[prop.id],bounds,regions[prop.id],Color.WHITE if operating else Color(.65,.65,.65))
	if prop.id=="kitchen" and operating:
		var at:=bounds.position+bounds.size*Vector2(.46,.72)
		painter.draw_circle(at,1.4,Color(1,.60,.20,.6+.2*sin(machine_clock*3)))
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="kitchen"
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("48463d"),Color(.1,.1,.1,.35),2,"wood")
func draw_wall(rect: Rect2, horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"habitation")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"habitation")

func layout_caption() -> String: return "GALLEY / one entrance"
