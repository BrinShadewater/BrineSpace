extends "res://rooms/whole-room/life_support_view.gd"
const Dressing=preload("res://rooms/whole-room/room_dressing.gd")
var dressing
var shelf_helmet_visible := true
var shelf_helmet: Texture2D
var cycle_pose: Dictionary=preload("res://scripts/airlock_cycle.gd").pose({})
const CHAMBER=Rect2(-60,-184,120,220)
const Fittings=preload("res://rooms/underwater/airlock-v4/fittings.gd")

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	for segment in exterior_wall_segments(rect):
		draw_steel_wall(segment,horizontal)

func exterior_wall_segments(rect: Rect2) -> Array:
	# Only the outer hull edge is split. Inner chamber rails keep their own geometry.
	var canonical_center:=Geometry.turn(rect.get_center(),posmod(4-quarter,4))
	if absf(canonical_center.y+192)>1: return [rect]
	var gap:=turned_rect(Rect2(-36,-208,72,40))
	if not rect.intersects(gap): return [rect]
	var result: Array=[]
	if quarter%2==0:
		if rect.position.x<gap.position.x: result.append(Rect2(rect.position,Vector2(gap.position.x-rect.position.x,rect.size.y)))
		if rect.end.x>gap.end.x: result.append(Rect2(Vector2(gap.end.x,rect.position.y),Vector2(rect.end.x-gap.end.x,rect.size.y)))
	else:
		if rect.position.y<gap.position.y: result.append(Rect2(rect.position,Vector2(rect.size.x,gap.position.y-rect.position.y)))
		if rect.end.y>gap.end.y: result.append(Rect2(Vector2(rect.position.x,gap.end.y),Vector2(rect.size.x,rect.end.y-gap.end.y)))
	return result

func draw_steel_wall(rect: Rect2,horizontal: bool) -> void:
	# Engineering cladding over the same authoritative hull dimensions.
	var top:=Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("182d35"))
	painter.draw_rect(top,Color("536767"))
	painter.draw_rect(top.grow(-1),Color("657873"))
	painter.draw_line(top.position,top.position+Vector2(top.size.x,0),Color("9ba898"),1)
	if not horizontal:
		painter.draw_line(top.position+Vector2(1,0),top.position+Vector2(1,top.size.y),Color("a2aea1"),1)
		painter.draw_line(top.position+Vector2(top.size.x-1,0),top.end,Color("243b43"),2)
	var span:=rect.size.x if horizontal else rect.size.y
	for offset in range(12,int(span),32):
		var point:=top.position+(Vector2(offset,0) if horizontal else Vector2(0,offset))
		painter.draw_line(point,point+(Vector2(0,top.size.y) if horizontal else Vector2(top.size.x,0)),Color("293f46"),1)

func draw_cap(rect: Rect2) -> void:
	painter.draw_rect(rect,Color("2b4148"))
	painter.draw_rect(rect.grow(-2),Color("76867c"))

func chamber_rect() -> Rect2:
	return CHAMBER

func keep_props_inside_walls() -> void:
	# The code-owned cutaway hatch is registered after floor furniture placement.
	var all_props:=props.duplicate()
	props=props.filter(func(prop): return prop.id!="outer_hatch")
	super.keep_props_inside_walls()
	props=all_props

func turned_rect(rect: Rect2) -> Rect2:
	var size:=rect.size if quarter%2==0 else Vector2(rect.size.y,rect.size.x)
	return Rect2(Geometry.turn(rect.get_center(),quarter)-size*0.5,size)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.id=="pressure_chamber": return prop.rect.grow(5)
	if prop.id=="outer_hatch": return turned_rect(Rect2(-44,-200,88,24))
	return super.prop_visual_bounds(prop)
func _ready() -> void:
	super._ready()
	var helmet_image := Image.new()
	if helmet_image.load_png_from_buffer(FileAccess.get_file_as_bytes("res://character/crew-underwater-v1/equipment/east/overlay.png")) == OK:
		shelf_helmet = ImageTexture.create_from_image(helmet_image)
	life_items=[]
	dressing=Dressing.new(self,"res://rooms/underwater/airlock-v1/composition.json")
	rebuild()
func rebuild() -> void:
	super.rebuild()
	layout[0].kind=3 # One station connection; pressure chamber has its own interlock.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()
	# Keep the compressor's working group above the east-facing chamber.
	if quarter==1:
		for prop in props:
			if prop.id=="air_compressor":
				prop.rect.position.y=-122
				prop.sort_y=prop.rect.end.y
		keep_props_inside_walls()
	for prop in props:
		if prop.id=="outer_hatch":
			prop.rect=turned_rect(Rect2(-36,outer_threshold()-6,72,12))
			prop.sort_y=prop.rect.end.y
	# Roaming crew stay in the dry preparation area. Exterior dispatch is separate.
	var chamber:=turned_rect(chamber_rect())
	props.append({"id":"pressure_chamber","rect":chamber,"center":Vector2.ZERO,"sort_y":chamber.end.y,"registration":{}})
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_floor(painter,center,Color("465356"),Color(0.19,0.29,0.29,0.16),2,"steel")
	RoomFloor.draw_dressing(painter,center,edges,"steel")
	for prop in props:
		if prop.id=="changing_bench":
			preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"boot_scrub_tray",Rect2(prop.rect.position-Vector2(4,4),prop.rect.size+Vector2(8,22)))
		if prop.id=="air_compressor":
			var start:=Vector2(prop.rect.get_center().x,prop.rect.end.y+3)
			var end:=Geometry.turn(Vector2(-66,-70),quarter)
			var elbow:=Vector2(end.x,start.y)
			for points in [[start,elbow],[elbow,end]]:
				painter.draw_line(points[0],points[1],Color("172e36"),5)
				painter.draw_line(points[0],points[1],Color("6c817e"),2)
			for point in [start,elbow,end]:
				painter.draw_rect(Rect2(point-Vector2(3,3),Vector2(6,6)),Color("9b885b"))
func draw_registered_prop(prop: Dictionary) -> void:
	# Draw with the chamber so its wet-deck pass cannot cover the hatch leaves.
	if prop.id=="outer_hatch": return
	if prop.id=="pressure_chamber":
		draw_chamber()
		return
	if dressing==null or not dressing.draw(prop): return
	if prop.id=="suit_lockers":
		# Screen-facing attachment follows the fitting point in every room rotation.
		var at := Vector2(prop.rect.position.x-7, prop.rect.end.y-25)
		# A shallow side ledge supports the handoff rather than a floating sprite.
		painter.draw_rect(Rect2(at+Vector2(-12,2),Vector2(22,3)),Color("536767"))
		painter.draw_line(at+Vector2(-12,2),at+Vector2(10,2),Color("9ba898"),1)
		painter.draw_line(at+Vector2(-7,5),at+Vector2(10,14),Color("293f46"),2)
		if shelf_helmet_visible and shelf_helmet != null:
			painter.draw_texture_rect(shelf_helmet, Rect2(at-Vector2(10,24),Vector2(20,25)),false)
	if prop.id=="air_compressor" and operating:
		var center: Vector2=life_point(prop,Vector2(269,762))
		painter.draw_line(center,center+Vector2(2,-3),Color("a4c7bc"),0.8)
func draw_chamber() -> void:
	var floor_rect:=turned_rect(chamber_rect().grow(-6))
	painter.draw_rect(floor_rect,Color("283c40"))
	for y in range(-168,20,32):
		painter.draw_line(Geometry.turn(Vector2(-51,y),quarter),Geometry.turn(Vector2(51,y),quarter),Color("40565a"),1)
	for y in [-152,-8]:
		Fittings.sprite(painter,"drain",turned_rect(Rect2(-13,y-13,26,26)))
	var water: float=cycle_pose.water
	if water>0:
		var depth:=208.0
		var wet:=Rect2(-54,30-depth*water,108,depth*water)
		painter.draw_rect(turned_rect(wet),Color(0.08,0.42,0.49,0.48))
		painter.draw_line(Geometry.turn(wet.position,quarter),Geometry.turn(wet.position+Vector2(wet.size.x,0),quarter),Color("79c5c9"),1.5)
	var rear: float=-190
	var walls: Array=[Rect2(-64,rear,8,40-rear),Rect2(56,rear,8,40-rear),Rect2(-60,30,24,10),Rect2(36,30,24,10)]
	walls.append_array([Rect2(-60,-190,24,8),Rect2(36,-190,24,8)])
	for wall in walls:
		var rect:=turned_rect(wall)
		draw_wall(rect,rect.size.x>rect.size.y)
	# The same two-leaf mechanism as the shared doors, registered in room space.
	for leaf in preload("res://rooms/whole-room/room_door.gd").leaf_rects(cycle_pose.inner):
		var rect:=turned_rect(Rect2(leaf.position+Vector2(0,35),leaf.size))
		painter.draw_rect(rect,Color("9ca89b"))
		painter.draw_rect(rect.grow(-2),Color("475d5b"))
	for x in [-39,39]:
		var point:=Geometry.turn(Vector2(x,35),quarter)
		painter.draw_circle(point,2,Color("95cfad") if cycle_pose.inner>=1 else Color("df9860"))
	for x in [-52,46]:
		painter.draw_rect(turned_rect(Rect2(x,31,6,5)),Color("b89a5b"))
	# Supported local controller, kept on the chamber post rather than floor scatter.
	var panel_at:=Geometry.turn(Vector2(-67,22),quarter)
	painter.draw_line(panel_at,Geometry.turn(Vector2(-58,22),quarter),Color("182d35"),4)
	Fittings.sprite(painter,"controller",Rect2(panel_at-Vector2(11,21),Vector2(22,20)))
	var gauge:=turned_rect(Rect2(-45,14,90,4))
	painter.draw_rect(gauge,Color("15272d"))
	painter.draw_rect(turned_rect(Rect2(-45,14,90*float(cycle_pose.pressure),4)),Color("d5af68"))
	draw_outer_cutaway()

func outer_threshold() -> float:
	return -184.0

func draw_outer_cutaway() -> void:
	var at:=Vector2(0,outer_threshold())
	# Low pressure sill and two leaves use the shared 72-unit aperture.
	# Rotate hull geometry, never the upright source sprite.
	painter.draw_rect(turned_rect(Rect2(-36,-200,72,22)),Color("172f37"))
	painter.draw_line(Geometry.turn(at+Vector2(-36,5),quarter),Geometry.turn(at+Vector2(36,5),quarter),Color("758780"),1)
	for leaf in preload("res://rooms/whole-room/room_door.gd").leaf_rects(cycle_pose.outer):
		var panel:=turned_rect(Rect2(leaf.position+at,leaf.size))
		painter.draw_rect(panel,Color("9ca89b"))
		if minf(panel.size.x,panel.size.y)>2:
			painter.draw_rect(panel.grow(-1),Color("475d5b"))
	for x in [-40,40]:
		var jamb:=turned_rect(Rect2(at+Vector2(x-4,-8),Vector2(8,16)))
		draw_cap(jamb)
		var lamp:=Geometry.turn(at+Vector2(x,0),quarter)
		painter.draw_circle(lamp,1.5,Color("e3e3cc") if operating else Color("52605b"))

func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["pressure_chamber","outer_hatch","suit_lockers"]
func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
