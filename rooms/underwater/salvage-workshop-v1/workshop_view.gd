extends "res://rooms/whole-room/nursery_south_facing.gd"
var textures: Dictionary={}
var regions: Dictionary={}
var carriers: Array=[]
var north_bench_art: Dictionary={}
var overhead_textures: Dictionary={}
func overhead_texture(id: String) -> ImageTexture:
	var key:=id+"-q"+str(quarter)
	if not overhead_textures.has(key):overhead_textures[key]=load_source_texture("res://assets/rooms/salvage-workshop/pack/"+key+".png")
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
	for id in ["bench","tote"]:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/underwater/salvage-workshop-v1/"+id+".png")
		textures[id]=ImageTexture.create_from_image(image)
		regions[id]=Rect2(image.get_used_rect())
	north_bench_art=DirectionalLibrary.template("library/salvage-bench-north").duplicate(true)
	rebuild()
func rebuild() -> void:
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	props.clear()
	for id in ["bench","tote"]:
		var rect:=Rect2(-160,-180,320,115) if id=="bench" else Rect2(-148,84,64,28)
		if id=="tote":
			var prop: Dictionary=DirectionalLibrary.template("library/side-salvage-tote-south").duplicate(true)
			var height: float=102.4*prop.registration.height/prop.registration.width
			prop.id=id
			prop.rect=Rect2(-166.0,184.0-height,102.4,height)
			prop.sort_y=184.0
			props.append(prop)
			continue
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{}})
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
	for prop in props:
		if prop.id=="bench":
			prop.custom_library_draw=true
func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("overhead_furnishing",false):return overhead_bounds(prop)
	if prop.get("library_asset",false): return DirectionalLibrary.bounds(prop)
	var region: Rect2=regions[prop.id]
	var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
	return Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size)
func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("overhead_furnishing",false):
		painter.draw_texture_rect(overhead_texture(prop.id),overhead_bounds(prop),false)
		if prop.id=="bench" and operating:
			var points:=PackedVector2Array()
			for p in [Vector2(.645,.155),Vector2(.755,.155),Vector2(.755,.175),Vector2(.645,.175)]:points.append(overhead_point(prop,p))
			painter.draw_colored_polygon(points,Color(1,.78,.42,.35))
		return
	var bounds:=prop_visual_bounds(prop)
	if prop.get("library_asset",false):
		DirectionalLibrary.draw(self,prop)
		if prop.id=="bench" and operating:
			var indicator:=bounds.position+bounds.size*Vector2(.86,.87)
			painter.draw_circle(indicator,1.4,Color(1,.60,.20,.6+.2*sin(machine_clock*3)))
		return
	if prop.id=="bench" and not north_bench_art.is_empty():
		var artwork:=north_bench_art.duplicate()
		artwork.rect=bounds
		DirectionalLibrary.draw(self,artwork)
		if operating:
			var reg: Dictionary=artwork.registration
			var anchor:=Vector2(bounds.get_center().x,bounds.end.y)
			var scale_value: float=bounds.size.x/reg.width
			var light:=Rect2(anchor+(Vector2(1004,146)-reg.pivot)*scale_value,Vector2(173,10)*scale_value)
			painter.draw_rect(light,Color(.88,.65,.30,.45+.05*sin(machine_clock*2)))
	else:
		painter.draw_texture_rect_region(textures[prop.id],bounds,regions[prop.id],Color.WHITE if operating else Color(.65,.65,.65))
	if prop.id=="bench" and operating:
		var at:=bounds.position+bounds.size*Vector2(.89,.68)
		painter.draw_circle(at,1.4,Color(1,.60,.20,.6+.2*sin(machine_clock*3)))
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="bench"
func draw_actor() -> void:
	super.draw_actor()
	for point in carriers:
		if actor.distance_to(point)<1:
			var region: Rect2=regions.tote
			var size:=Vector2(21,21*region.size.y/region.size.x)
			painter.draw_texture_rect_region(textures.tote,Rect2(actor+Vector2(-10,-32),size),region)
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("373a3b"),Color(.1,.1,.1,.35),2,"steel")
func draw_wall(rect: Rect2, horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"engineering")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"engineering")

func layout_caption() -> String: return "SALVAGE WORKSHOP / one entrance"
