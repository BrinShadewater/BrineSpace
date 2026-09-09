extends "res://rooms/whole-room/nursery_south_facing.gd"
var textures: Dictionary={}
var regions: Dictionary={}
func _ready() -> void:
	texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	actor_library=ActorLibrary.new()
	set_process(false)
	show_actor=false
	for id in ["kitchen","serving"]:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image, "res://rooms/underwater/galley-v1/"+id+".png")
		textures[id]=ImageTexture.create_from_image(image)
		regions[id]=Rect2(image.get_used_rect())
	rebuild()
func rebuild() -> void:
	layout=[{"cell":Vector2i.ZERO,"rotation":0,"kind":3}]
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	props.clear()
	for id in ["kitchen","serving"]:
		var rect:=Rect2(-160,-80,320,64) if id=="kitchen" else Rect2(20,74,132,42)
		props.append({"id":id,"rect":rect,"center":Vector2.ZERO,"sort_y":rect.end.y,"registration":{}})
	queue_redraw()
func configure_embedded(_q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array=[]) -> void:
	super.configure_embedded(0,open_sides,running,time_seconds,omitted_sides)
func prop_visual_bounds(prop: Dictionary) -> Rect2:
	var region: Rect2=regions[prop.id]
	var size:=Vector2(prop.rect.size.x,prop.rect.size.x*region.size.y/region.size.x)
	return Rect2(Vector2(prop.rect.position.x,prop.rect.end.y-size.y),size)
func draw_registered_prop(prop: Dictionary) -> void:
	var bounds:=prop_visual_bounds(prop)
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

func layout_caption() -> String: return "GALLEY / south entrance"
