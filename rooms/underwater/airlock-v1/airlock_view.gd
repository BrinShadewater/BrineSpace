extends "res://rooms/whole-room/life_support_view.gd"
const Dressing=preload("res://rooms/whole-room/room_dressing.gd")
var dressing
var shelf_helmet_visible := true
var shelf_helmet_scale := 1.0
var shelf_helmet: Texture2D
var cycle_pose: Dictionary=preload("res://scripts/airlock_cycle.gd").pose({})
const CHAMBER=Rect2(-60,-184,120,220)
const Fittings=preload("res://rooms/underwater/airlock-v4/fittings.gd")
static var wet_deck: Texture2D
var embedded_omitted_sides: Array = []

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	embedded_omitted_sides=omitted_sides.duplicate()
	var library=preload("res://scripts/room_asset_library.gd")
	if quarter==0:
		for i in range(props.size()):
			if props[i].id!="suit_lockers": continue
			var prop: Dictionary=library.template("library/side-airlock-suit-storage-south-empty-tray").duplicate(true)
			prop.id="suit_lockers"
			prop.custom_library_draw=true
			prop.rect.position=Vector2(58,180-prop.rect.size.y)
			prop.helmet_anchor_uv=Vector2(0.051,-0.80)
			prop.sort_y=prop.rect.end.y
			props[i]=prop
		return
	if quarter==2:
		for i in range(props.size()):
			var id: String=props[i].id
			if id=="suit_lockers":
				var locker: Dictionary=library.template("library/side-airlock-suit-storage-north").duplicate(true)
				locker.id=id
				locker.custom_library_draw=true
				locker.rect.position=Vector2(-158,-180)
				locker.helmet_anchor_uv=Vector2(0.051,1.3)
				# The wall-art rect depends on the omitted/raised north wall, which is a
				# per-host drawing state; resolve it at draw time (locker_wall_art_rect)
				# so embedded geometry stays identical across running/omitted configs.
				locker.sort_y=locker.rect.end.y
				props[i]=locker
				continue
			if id not in ["reserve_air_bank","equipment_check_bench"]: continue
			var asset: String="reserve-air" if id=="reserve_air_bank" else "check-bench"
			var prop: Dictionary=library.template("library/side-airlock-"+asset+"-south").duplicate(true)
			prop.id=id
			prop.rect.position=Vector2(76.0 if id=="reserve_air_bank" else -178.0,180.0-prop.rect.size.y)
			prop.sort_y=prop.rect.end.y
			props[i]=prop
		return
	if quarter not in [1,3]: return
	for i in range(props.size()):
		if props[i].id!="suit_lockers": continue
		var locker: Dictionary=library.template("library/side-airlock-suit-storage-side").duplicate(true)
		locker.id="suit_lockers"
		locker.custom_library_draw=true
		if quarter==1: locker.registration=library.mirror_registration(locker.registration)
		locker.rect.position=Vector2(-180,40) if quarter==1 else Vector2(180-locker.rect.size.x,-176)
		locker.helmet_anchor_uv=Vector2(2.0,0.8) if quarter==1 else Vector2(-0.25,0.8)
		locker.helmet_tray_uv=Vector2(0.75,0.94) if quarter==1 else Vector2(0.25,0.94)
		locker.sort_y=locker.rect.end.y
		props[i]=locker
	for i in range(props.size()):
		if props[i].id!="equipment_check_bench": continue
		var prop: Dictionary=library.template("library/side-airlock-check-bench-side").duplicate(true)
		prop.id="equipment_check_bench"
		if quarter==3: prop.registration=library.mirror_registration(prop.registration)
		prop.rect.position=Vector2(180.0-prop.rect.size.x,76.0) if quarter==1 else Vector2(-180.0,-176.0)
		prop.sort_y=prop.rect.end.y
		props[i]=prop
	if quarter==3:
		for i in range(props.size()):
			if props[i].id!="reserve_air_bank": continue
			var prop: Dictionary=library.template("library/side-airlock-reserve-air-side").duplicate(true)
			prop.id="reserve_air_bank"
			prop.registration=library.mirror_registration(prop.registration)
			prop.rect.position=Vector2(-180.0,76.0)
			prop.sort_y=prop.rect.end.y
			props[i]=prop

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
	# Keep exterior hatch exclusions; use registered steel instead of flat bands.
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"engineering")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"engineering")

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
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
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
	# The composition owns per-facing service bays, including compressor clearance.
	for prop in props:
		if prop.id=="outer_hatch":
			prop.rect=turned_rect(Rect2(-36,outer_threshold()-6,72,12))
			prop.sort_y=prop.rect.end.y
	# Roaming crew stay in the dry preparation area. Exterior dispatch is separate.
	var chamber:=turned_rect(chamber_rect())
	props.append({"id":"pressure_chamber","rect":chamber,"center":Vector2.ZERO,"sort_y":chamber.end.y,"registration":{}})
func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("465356"),Color(0.19,0.29,0.29,0.16),2,"steel")
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	draw_chamber_floor()
	for prop in props:
		if prop.id=="changing_bench":
			preload("res://rooms/whole-room/decoration_props.gd").floor_patch(painter,"boot_scrub_tray",Rect2(prop.rect.position-Vector2(4,4),prop.rect.size+Vector2(8,22)))
		if prop.id=="air_compressor":
			var start:=Vector2(prop.rect.get_center().x,prop.rect.end.y+3)
			var end:=Geometry.turn(Vector2(-66,-70),quarter)
			var elbow:=Vector2(end.x,start.y)
			preload("res://rooms/whole-room/decoration_props.gd").service_run(painter,PackedVector2Array([start,elbow,end]),5.0,"pipe_straight")
func has_wall_art(prop: Dictionary) -> bool:
	return quarter==2 and prop.id=="suit_lockers" and prop.get("custom_library_draw",false)

func locker_wall_art_rect(prop: Dictionary) -> Rect2:
	if not has_wall_art(prop): return prop.rect
	var riser=preload("res://rooms/whole-room/riser_geometry.gd")
	var raised: bool=get_meta("raised_north_visible",preload("res://scripts/title_settings.gd").raised_walls)
	var wall_top: float=riser.TOP if raised and not embedded_omitted_sides.has(0) else riser.BASE_Y
	return Rect2(Vector2(-158,wall_top),prop.rect.size)

func wall_art_rects() -> Array:
	var result: Array=[]
	for prop in props:
		if has_wall_art(prop): result.append(locker_wall_art_rect(prop))
	return result

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("library_asset",false):
		var artwork: Dictionary=prop
		if has_wall_art(prop):
			artwork=prop.duplicate()
			artwork.rect=locker_wall_art_rect(prop)
		preload("res://scripts/room_asset_library.gd").draw(self,artwork)
		if prop.id!="suit_lockers": return
	# Draw with the chamber so its wet-deck pass cannot cover the hatch leaves.
	if prop.id=="outer_hatch": return
	if prop.id=="pressure_chamber":
		draw_chamber()
		return
	if not prop.get("library_asset",false) and (dressing==null or not dressing.draw(prop)): return
	if prop.id=="suit_lockers":
		# Screen-facing attachment follows the fitting point in every room rotation.
		var at: Vector2=preload("res://scripts/airlock_service.gd").helmet_anchor(prop)
		if prop.has("helmet_anchor_uv"):
			var support: Rect2=locker_wall_art_rect(prop)
			var tray: Vector2=support.position+support.size*prop.get("helmet_tray_uv",Vector2(0.051,0.52))
			painter.draw_line(tray,at+Vector2(0,4),Color("293f46"),3)
		# A shallow side ledge supports the handoff rather than a floating sprite.
		painter.draw_rect(Rect2(at+Vector2(-12,2),Vector2(22,3)),Color("536767"))
		painter.draw_line(at+Vector2(-12,2),at+Vector2(10,2),Color("9ba898"),1)
		painter.draw_line(at+Vector2(-7,5),at+Vector2(10,14),Color("293f46"),2)
		if shelf_helmet_visible and shelf_helmet != null:
			var helmet_size:=Vector2(20,25)*shelf_helmet_scale
			painter.draw_texture_rect(shelf_helmet, Rect2(at+Vector2(-helmet_size.x*0.5,1-helmet_size.y),helmet_size),false)
	if prop.id=="air_compressor" and operating:
		var center: Vector2=life_point(prop,Vector2(269,762))
		painter.draw_line(center,center+Vector2(2,-3),Color("a4c7bc"),0.8)
func draw_actor() -> void:
	var room_water:=flood_water
	if turned_rect(chamber_rect()).has_point(actor):
		flood_water=maxf(flood_water,float(cycle_pose.water))
	super.draw_actor()
	flood_water=room_water

func draw_chamber_floor() -> void:
	if wet_deck==null:
		var image:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(image,"res://assets/airlock-deck-v1/wet-deck-source.png")
		wet_deck=ImageTexture.create_from_image(image)
	var floor_rect:=chamber_rect().grow(-6)
	var corners:=PackedVector2Array([floor_rect.position,Vector2(floor_rect.end.x,floor_rect.position.y),floor_rect.end,Vector2(floor_rect.position.x,floor_rect.end.y)])
	for i in range(corners.size()): corners[i]=Geometry.turn(corners[i],quarter)
	painter.draw_polygon(corners,PackedColorArray([Color.WHITE]),PackedVector2Array([Vector2.ZERO,Vector2.RIGHT,Vector2.ONE,Vector2.DOWN]),wet_deck)
	var water: float=cycle_pose.water
	if water>0:
		var depth:=208.0
		var wet:=Rect2(-54,30-depth*water,108,depth*water)
		painter.draw_rect(turned_rect(wet),Color(0.08,0.42,0.49,0.48))
		painter.draw_line(Geometry.turn(wet.position,quarter),Geometry.turn(wet.position+Vector2(wet.size.x,0),quarter),Color("79c5c9"),1.5)

func draw_chamber() -> void:
	var water: float=cycle_pose.water
	var rear: float=-190
	var walls: Array=[Rect2(-64,rear,8,40-rear),Rect2(56,rear,8,40-rear),Rect2(-60,30,24,10),Rect2(36,30,24,10)]
	walls.append_array([Rect2(-60,-190,24,8),Rect2(36,-190,24,8)])
	for wall in walls:
		var rect:=turned_rect(wall)
		draw_wall(rect,rect.size.x>rect.size.y)
	# The same two-leaf mechanism as the shared doors, registered in room space.
	for leaf in preload("res://rooms/whole-room/room_door.gd").leaf_rects(cycle_pose.inner):
		var rect:=turned_rect(Rect2(leaf.position+Vector2(0,35),leaf.size))
		var vertical:=quarter%2==1
		var delta:=rect.get_center()-Geometry.turn(Vector2(0,35),quarter)
		preload("res://rooms/doors/door_finish.gd").low_leaf(painter,rect,(delta.y if vertical else delta.x)<0,vertical,"life-support")
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
	draw_wet_gate("inner",Vector2(0,35),Vector2.DOWN,cycle_pose.inner,water-flood_water,maxf(water,flood_water))
	draw_wet_gate("outer",Vector2(0,outer_threshold()),Vector2.UP,cycle_pose.outer,water-1.0,water)

var wet_gate_history: Dictionary={}
func draw_wet_gate(id: String, at: Vector2, direction: Vector2, amount: float, difference: float, water: float) -> void:
	var fx=preload("res://rooms/doors/door_water.gd")
	var state: Dictionary=fx.advance(wet_gate_history.get(id,{}),roundi(amount*9),machine_clock)
	wet_gate_history[id]=state
	fx.draw(painter,Geometry.turn(at,quarter),Geometry.turn(direction,quarter),amount,difference,water,float(state.closing_until)>machine_clock,machine_clock,1.0)

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
		var vertical:=quarter%2==1
		var delta:=panel.get_center()-Geometry.turn(at,quarter)
		preload("res://rooms/doors/door_finish.gd").low_leaf(painter,panel,(delta.y if vertical else delta.x)<0,vertical,"life-support")
	for x in [-40,40]:
		var jamb:=turned_rect(Rect2(at+Vector2(x-4,-8),Vector2(8,16)))
		draw_cap(jamb)
		var lamp:=Geometry.turn(at+Vector2(x,0),quarter)
		painter.draw_circle(lamp,1.5,Color("e3e3cc") if operating else Color("52605b"))

func is_animated_prop(prop: Dictionary) -> bool: return prop.id in ["pressure_chamber","outer_hatch","suit_lockers"]
func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
