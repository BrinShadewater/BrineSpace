extends "res://rooms/whole-room/nursery_south_facing.gd"
var textures: Dictionary={}
var regions: Dictionary={}
var overhead_textures: Dictionary={}
const DirectionalLibrary=preload("res://scripts/room_asset_library.gd")
func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library=ActorLibrary.new()
	set_process(false)
	show_actor=false
	for id in ["fridge","rack"]:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/underwater/cold-store-v1/"+id+"-v2.png")
		textures[id]=ImageTexture.create_from_image(image)
		regions[id]=Rect2(image.get_used_rect())
	rebuild()
func overhead_texture(id: String) -> ImageTexture:
	var source: String="cooler" if id.begins_with("cooler") else id
	var key:=source+"-q"+str(quarter)
	if not overhead_textures.has(key):overhead_textures[key]=load_source_texture("res://assets/rooms/cold-store/pack/"+key+".png")
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
func draw_cooler_frost(prop: Dictionary) -> void:
	# Deterministic lid vapor: cold activity stays local to the chest and follows
	# the same quarter transform as its authored handles and hinges.
	for i in range(6):
		var phase:=fposmod(machine_clock*.24+float(i)*.173,1.0)
		var x:=.22+float(i)*.115+sin(machine_clock*.8+float(i)*1.7)*.018
		var y:=.60-phase*.31
		var alpha:=sin(phase*PI)*.22
		painter.draw_circle(overhead_point(prop,Vector2(x,y)),.55+phase*.55,Color(.58,.90,1.0,alpha))
func rebuild() -> void:
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":1}]
	edges=Geometry.edges(layout)
	for edge in edges:edge.open=edge.port
	props.clear()
	for id in ["fridge","rack","cooler-0","cooler-1"]:
		var rect:=Rect2(-184,-126,70,252) if id=="fridge" else Rect2(104,-126,80,252)
		if id.begins_with("cooler"):rect=Rect2(-44,-82 if id=="cooler-0" else 30,88,50)
		var size: Vector2=rect.size if quarter%2==0 else Vector2(rect.size.y,rect.size.x)
		rect=Rect2(Geometry.turn(rect.get_center(),quarter)-size*.5,size)
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{},"overhead_furnishing":true})
	queue_redraw()
func configure_embedded(_q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array=[]) -> void:
	super.configure_embedded(_q,open_sides,running,time_seconds,omitted_sides)
func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("overhead_furnishing",false):return overhead_bounds(prop)
	if prop.get("library_asset",false): return DirectionalLibrary.bounds(prop)
	var region: Rect2=regions[prop.id]
	var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
	return Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size)
func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("overhead_furnishing",false):
		painter.draw_texture_rect(overhead_texture(prop.id),overhead_bounds(prop),false)
		if operating and prop.id.begins_with("cooler"):
			painter.draw_circle(overhead_point(prop,Vector2(.88,.82)),1.2,Color(.3,.8,.88,.6+.15*sin(machine_clock*3)))
			draw_cooler_frost(prop)
		return
	var bounds:=prop_visual_bounds(prop)
	if prop.get("library_asset",false):
		DirectionalLibrary.draw(self,prop)
		if prop.id=="fridge" and operating:
			var indicator:=bounds.position+bounds.size*Vector2(.93,.5)
			if prop.registration.has("status_point"):
				var reg: Dictionary=prop.registration
				var point:=Vector2(reg.status_point[0],reg.status_point[1])
				indicator=Vector2(prop.rect.get_center().x,prop.rect.end.y)+(DirectionalLibrary.source_uv(reg,point)-reg.pivot)*prop.rect.size.x/reg.width
			painter.draw_circle(indicator,1.4,Color(.30,.80,.88,.6+.2*sin(machine_clock*3)))
		return
	painter.draw_texture_rect_region(textures[prop.id],bounds,regions[prop.id],Color.WHITE if operating else Color(.65,.65,.65))
	if prop.id=="fridge" and operating:
		var at:=bounds.position+bounds.size*Vector2(.82,.84)
		painter.draw_circle(at,1.4,Color(.30,.80,.88,.6+.2*sin(machine_clock*3)))
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="fridge" or prop.id.begins_with("cooler")
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("414648"),Color(.1,.1,.1,.35),2,"steel")
func draw_wall(rect: Rect2, horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"medical")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"medical")

func layout_caption() -> String: return "COLD STORE / north-south aisle"
