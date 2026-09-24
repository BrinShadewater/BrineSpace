extends "res://rooms/whole-room/life_support_view.gd"
## Registered machinery; Current Turbine follows the intake arrow wall.
var room_id := "current_turbine"
# Explicit bindings keep the release closure limited to the three live machines.
const MACHINE_PATHS = {
	"current_turbine": "res://legacy/default/assets/rooms/current-turbine/source/machine.png",
	"biomass_digester": "res://legacy/default/assets/rooms/biomass-digester/source/machine.png",
	"heat_recovery": "res://legacy/default/assets/rooms/heat-recovery/source/machine.png",
}
var machine_texture: ImageTexture
var machine_region := Rect2()
var intake_clear := true
var dressing: RefCounted
const DirectionalLibrary=preload("res://scripts/room_asset_library.gd")

func _ready() -> void:
	super._ready()
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, MACHINE_PATHS[room_id])
	machine_texture = ImageTexture.create_from_image(image)
	machine_region = Rect2(image.get_used_rect())
	# Register the visible turbine, excluding near-transparent source padding.
	if room_id=="current_turbine": machine_region=Rect2(18,260,1218,652)
	life_items = [
		{"id":"power_machine", "rect":Rect2(-172,-143,144,62), "pivot":Vector2.ZERO,"width":1.0,"outline":[]},
		{"id":"life_console", "rect":Rect2(63,70,88,58), "pivot":Vector2(925,1017),"width":274.0,"outline":[Vector2(800,780),Vector2(1045,780),Vector2(1062,802),Vector2(1062,1016),Vector2(788,1016),Vector2(788,807)]}
	]
	var profile_path := "res://rooms/power-expansion-v1/"+room_id+"-composition-v2.json"
	dressing = preload("res://rooms/whole-room/room_dressing.gd").new(self,profile_path)
	rebuild()

func rebuild() -> void:
	super.rebuild()
	if layout.is_empty(): return
	layout[0].kind = 1 if room_id=="current_turbine" else (0 if room_id=="biomass_digester" else 2)
	layout[0].rotation = posmod(quarter+1,4) if room_id=="current_turbine" else quarter
	edges = Geometry.edges(layout)
	for edge in edges: edge.open = edge.port
	# Large south-facing skids occupy the lower work area in every orientation.
	# Crew can pass around either side; rotated doors retain the shared hull.
	for prop in props:
		if prop.id=="power_machine":
			var width := 250.0 if room_id=="current_turbine" else (220.0 if room_id=="biomass_digester" else 270.0)
			prop.rect=Rect2(-width*0.5,24,width,88)
			# Use the sealed south wall when the turbine's doors run east/west.
			# North/south rotations retain clearance behind the skid for the door.
			if room_id=="current_turbine" and posmod(quarter,2)==0:
				prop.rect.position.y=84
		elif prop.id=="life_console":
			prop.rect=Rect2(61,-128,88,58)
		prop.sort_y=prop.rect.end.y
	if room_id=="current_turbine":
		for i in range(props.size()):
			if props[i].id!="power_machine": continue
			var side: String=["north","east","south","west"][quarter]
			var replacement: Dictionary=DirectionalLibrary.template("library/side-current-turbine-"+side).duplicate(true)
			var ratio: float=replacement.registration.width/replacement.registration.height
			replacement.id="power_machine"
			replacement.custom_library_draw=true
			if quarter==0:
				replacement.rect=Rect2(-135,-148,270,270/ratio)
			elif quarter==2:
				replacement.rect=Rect2(-135,184-270/ratio,270,270/ratio)
			else:
				var width: float=270*ratio
				replacement.rect=Rect2(184-width if quarter==1 else -184,-135,width,270)
			replacement.sort_y=replacement.rect.end.y
			props[i]=replacement
	if room_id=="heat_recovery":
		for i in range(props.size()):
			if props[i].id!="power_machine": continue
			var replacement: Dictionary=DirectionalLibrary.template("library/side-heat-recovery-south").duplicate(true)
			var height: float=270.0*replacement.registration.height/replacement.registration.width
			replacement.id="power_machine"
			replacement.custom_library_draw=true
			replacement.rect=Rect2(-135,24,270,height)
			replacement.sort_y=replacement.rect.end.y
			props[i]=replacement
	if dressing!=null: dressing.place()

func machine_bounds(prop: Dictionary) -> Rect2:
	var size := Vector2(prop.rect.size.x, prop.rect.size.x * machine_region.size.y / maxf(machine_region.size.x,1.0))
	return Rect2(Vector2(prop.rect.get_center().x-size.x*0.5,prop.rect.end.y-size.y),size)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if prop.id=="power_machine": return machine_bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.get("library_asset",false):
		DirectionalLibrary.draw(self,prop)
		if operating and prop.id=="power_machine" and room_id=="heat_recovery":
			var bounds:=DirectionalLibrary.bounds(prop)
			painter.draw_circle(bounds.position+bounds.size*Vector2(.81,.19),1.5,Color(.52,.64,.53,.55+.2*sin(machine_clock*2)))
		if operating and prop.id=="power_machine" and room_id=="current_turbine":
			if prop.registration.has("turbine_effects"):
				draw_source_turbine_effects(prop)
				return
			var bounds:=DirectionalLibrary.bounds(prop)
			var lamp_uv:=Vector2(.80,.145) if quarter==2 else Vector2(.15 if quarter==1 else .85,.757)
			var lamp: Vector2=bounds.position+bounds.size*lamp_uv
			painter.draw_circle(lamp,1.5,Color(.52,.64,.53,.55+.2*sin(machine_clock*2)))
			var hub_uv:=Vector2(.235,.12) if quarter==2 else Vector2(.09 if quarter==1 else .91,.215)
			var hub: Vector2=bounds.position+bounds.size*hub_uv
			for blade in range(3):
				var angle: float=machine_clock*1.6+blade*TAU/3
				var tip:=Vector2(cos(angle)*bounds.size.x*.075,sin(angle)*bounds.size.y*.026) if quarter==2 else Vector2(cos(angle)*bounds.size.x*.022,sin(angle)*bounds.size.y*.09)
				painter.draw_line(hub,hub+tip,Color(.32,.44,.43,.28),1)
		return
	if dressing!=null and dressing.draw(prop): return
	if prop.id!="power_machine":
		var points := PackedVector2Array()
		var uv := PackedVector2Array()
		for point in prop.registration.outline:
			points.append(life_point(prop,point))
			uv.append(point/Vector2(life_texture.get_size()))
		var console_tint:=Color(0.68,0.72,0.68) if room_id=="biomass_digester" else Color(0.47,0.51,0.49)
		painter.draw_polygon(points,PackedColorArray([console_tint]),uv,life_texture)
		if operating:
			var a := life_point(prop,Vector2(840,838))
			painter.draw_line(a,a+Vector2(12+4*sin(machine_clock*2),0),Color("7e9a8c"),1)
		return
	var machine_tint := Color(0.81,0.81,0.81) if room_id=="current_turbine" else Color(0.82,0.82,0.82)
	painter.draw_texture_rect_region(machine_texture,machine_bounds(prop),machine_region,machine_tint)
	if operating:
		var bounds := machine_bounds(prop)
		var lamp := bounds.position + bounds.size * Vector2(0.79,0.52)
		painter.draw_circle(lamp,1.5,Color(0.52,0.64,0.53,0.55+0.2*sin(machine_clock*2)))
		if room_id=="current_turbine":
			var hub := bounds.position+bounds.size*Vector2(0.235,0.48)
			for blade in range(3):
				var direction := Vector2.from_angle(machine_clock*1.6+blade*TAU/3)
				painter.draw_line(hub+direction*7,hub+direction*(bounds.size.x*23.0/144.0),Color(0.32,0.44,0.43,0.28),1)

func turbine_source_point(prop: Dictionary, point: Vector2) -> Vector2:
	var reg: Dictionary=prop.registration
	var anchor:=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	return anchor+(DirectionalLibrary.source_uv(reg,point)-reg.pivot)*prop.rect.size.x/reg.width

func draw_source_turbine_effects(prop: Dictionary) -> void:
	var effect: Dictionary=prop.registration.turbine_effects
	var lamp:=Vector2(effect.lamp[0],effect.lamp[1])
	var hub:=Vector2(effect.hub[0],effect.hub[1])
	var radius:=Vector2(effect.radius[0],effect.radius[1])
	painter.draw_circle(turbine_source_point(prop,lamp),1.1,Color(.52,.64,.53,.55+.2*sin(machine_clock*2)))
	for blade in range(3):
		var angle: float=machine_clock*1.6+blade*TAU/3
		var tip:=hub+Vector2(cos(angle),sin(angle))*radius
		painter.draw_line(turbine_source_point(prop,hub),turbine_source_point(prop,tip),Color(.32,.44,.43,.28),1)

func is_animated_prop(prop: Dictionary) -> bool:
	return prop.id in ["power_machine","life_console"]

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("343937" if room_id=="biomass_digester" else "333638"),Color(0.1,0.12,0.12,0.4),2)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	if dressing!=null: dressing.floor()
	# Recessed service runs connect machinery and controls beneath the walking deck.
	for prop in props:
		if prop.id!="power_machine": continue
		var service_y: float=prop.rect.end.y-22
		var run := PackedVector2Array([Vector2(prop.rect.end.x,service_y),Vector2(160,service_y),Vector2(160,-72),Vector2(105,-72)])
		preload("res://rooms/whole-room/decoration_props.gd").service_run(painter,run,5.0)
	if room_id=="current_turbine":
		var distance: float=44.0 if quarter==0 else 100.0
		var tip := Geometry.turn(Vector2(0,-distance),quarter)
		var tail := Geometry.turn(Vector2(0,-distance+26),quarter)
		var tint := Color("728e89") if intake_clear else Color("ac7156")
		painter.draw_line(tail,tip,tint,3)
		for x in [-7,7]: painter.draw_line(tip,Geometry.turn(Vector2(x,-distance+9),quarter),tint,2)

func draw_wall(rect: Rect2, horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"engineering")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"engineering")

func layout_caption() -> String:
	return room_id.replace("_"," ").to_upper()
