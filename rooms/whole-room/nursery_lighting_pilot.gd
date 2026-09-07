extends "res://rooms/whole-room/nursery_south_facing.gd"
## Isolated prototype: no simulation/save changes and no source-art edits.
var electrical_power := true
var machine_enabled := true
var light_level := 1.0
const LIGHT_FADE_SECONDS := 0.65

func set_power_state(power: bool, enabled: bool, instant := false) -> void:
	electrical_power = power
	machine_enabled = enabled
	operating = power and enabled
	if instant: light_level = 1.0 if power else 0.0
	queue_redraw()

func advance(delta: float, direction := Vector2.ZERO) -> void:
	if paused: return
	super.advance(delta,direction)
	light_level = move_toward(light_level,1.0 if electrical_power else 0.0,delta/LIGHT_FADE_SECONDS)

func sconce_center() -> Vector2:
	# Away from the centered socket; fixture follows its wall, not machinery yaw.
	return Geometry.turn(Vector2(80,-190),quarter)

func fan_center(prop: Dictionary) -> Vector2:
	return pixel_to_world(Vector2(945,937))+prop.art_offset

func draw_registered_prop(prop: Dictionary) -> void:
	super.draw_registered_prop(prop)
	if prop.id != "filter": return
	var at := fan_center(prop)
	# Independent motor assembly on the existing vent face, with fixed housing.
	painter.draw_circle(at,7.0,Color("141e23"))
	painter.draw_arc(at,7,0,TAU,24,Color("8b9c97"),0.8)
	for blade in range(4):
		var angle := machine_clock*2.8+blade*TAU/4.0
		painter.draw_line(at+Vector2.from_angle(angle)*1.5,at+Vector2.from_angle(angle+0.28)*5.5,Color("a3b5af"),1.8)
	painter.draw_circle(at,1.5,Color("46595b"))
	# Machine status lens is a separate, state-driven element on this assembly.
	painter.draw_rect(Rect2(at+Vector2(9,-1),Vector2(3,2)),Color("82cfaa") if operating else Color("293d38"))

func draw_room_floor(center: Vector2) -> void:
	super.draw_room_floor(center)
	if light_level<=0: return
	var inward := -Vector2(Geometry.DIRS[quarter])
	var tangent := Vector2(-inward.y,inward.x)
	var start := sconce_center()+inward*8
	# Shallow, room-bounded pool. Not a dynamic shadow/normal-map implementation.
	for band in range(14):
		var distance := float(band)*4
		var width := 9.0+distance*0.38
		var a := start+inward*distance
		var b := start+inward*(distance+4)
		var poly := PackedVector2Array([a-tangent*width,a+tangent*width,b+tangent*(width+1.52),b-tangent*(width+1.52)])
		var clip := PackedVector2Array([Vector2(-184,-184),Vector2(184,-184),Vector2(184,184),Vector2(-184,184)])
		for clipped in Geometry2D.intersect_polygons(poly,clip):
			painter.draw_colored_polygon(clipped,Color(0.68,0.87,0.76,0.13*(1-float(band)/14)*light_level))

func draw_room_world(include_floor := true) -> void:
	super.draw_room_world(include_floor)
	# Dim machinery, crew and architecture together; retain readable ambient.
	painter.draw_rect(Rect2(-200,-203,400,407),Color(0.025,0.045,0.07,lerpf(0.72,0.12,light_level)))
	var at := sconce_center()
	var horizontal := quarter%2==0
	var size := Vector2(19,6) if horizontal else Vector2(6,19)
	painter.draw_rect(Rect2(at-size*0.5+Vector2(0,1),size),Color("111a20"))
	painter.draw_rect(Rect2(at-size*0.5,size).grow(-0.5),Color("a3b1a8").lerp(Color("364249"),1-light_level))
	var lens := Vector2(13,2) if horizontal else Vector2(2,13)
	painter.draw_rect(Rect2(at-lens*0.5,lens),Color("34484b").lerp(Color("d5f5dc"),light_level))

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.physical_keycode==KEY_P:
			set_power_state(not electrical_power,machine_enabled)
			return
		if event.physical_keycode==KEY_O:
			set_power_state(electrical_power,not machine_enabled)
			return
		if event.physical_keycode==KEY_C: return
	super._unhandled_key_input(event)

func _draw() -> void:
	if embedded: return
	super._draw()
	painter.draw_rect(Rect2(20,38,1100,56),Color("161d27"))
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,58),"LIGHTING STUDY / P: power / O: machine / R: rotate / Space: pause / WASD: crew",HORIZONTAL_ALIGNMENT_LEFT,-1,17,Color("c1d5ca"))
	painter.draw_string(ThemeDB.fallback_font,Vector2(28,82),"%s / %d degrees / procedural fixture art; no dynamic shadows"%[("OPERATING" if operating else "POWERED IDLE") if electrical_power else "UNPOWERED",quarter*90],HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("91ada4"))
