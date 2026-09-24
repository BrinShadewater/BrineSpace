extends "res://rooms/underwater/batch-two/holographic_core_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/split_wall_prop.gd").new("holo-wall","room-holographic_core")
const LAYERED_PROJECTOR="library/holo-projector-v1"
const LAYERED_CHART="library/holo-chart-v1"

func is_layered_projector(prop: Dictionary) -> bool:
	return preload("res://scripts/room_asset_library.gd").base_id(str(prop.get("copy_source",prop.id)))==LAYERED_PROJECTOR

func is_layered_chart(prop: Dictionary) -> bool:
	return preload("res://scripts/room_asset_library.gd").base_id(str(prop.get("copy_source",prop.id)))==LAYERED_CHART

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	full_wall.apply(self)
	for prop in props:
		if is_layered_projector(prop) or is_layered_chart(prop): prop.custom_library_draw=true
	# Keep the legacy fallback only when no authored calibrator placement exists.
	var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions("room-holographic_core",quarter)
	if q==0 and not authored.has("holo_calibrator"):
		for prop in props:
			if prop.id=="holo_calibrator":
				prop.rect.position=Vector2(47.7307739257813,51.4230804443359)
				prop.sort_y=prop.rect.end.y

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if is_layered_chart(prop):
		draw_analysis_chart(prop)
		return
	if is_layered_projector(prop):
		preload("res://scripts/room_asset_library.gd").draw(self,prop)
		if operating: draw_projection(prop)
		return
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	super.draw_registered_prop(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if is_layered_projector(prop) or is_layered_chart(prop): return operating
	if full_wall.owns(prop): return false
	return super.is_animated_prop(prop)

func draw_analysis_chart(prop: Dictionary) -> void:
	# Registration samples only the original physical stand. The luminous source
	# panel is omitted, so an offline chart cannot retain its baked cyan glow.
	preload("res://scripts/room_asset_library.gd").draw(self,prop)
	var bounds: Rect2=prop_visual_bounds(prop)
	var panel:=Rect2(bounds.position+bounds.size*Vector2(0.04,0.01),bounds.size*Vector2(0.90,0.57))
	painter.draw_rect(panel,Color("14252c"))
	painter.draw_rect(panel,Color("40565d"),false,0.8)
	if not operating: return
	var chart:=Rect2(panel.position+panel.size*Vector2(0.09,0.13),panel.size*Vector2(0.81,0.74))
	for i in range(1,4):
		var y:=chart.position.y+chart.size.y*float(i)/4.0
		painter.draw_line(Vector2(chart.position.x,y),Vector2(chart.end.x,y),Color(0.22,0.43,0.47,0.30),0.6)
	var points:=PackedVector2Array()
	for i in range(13):
		var x:=float(i)/12.0
		var y:=0.74-x*0.43+sin(float(i)*1.8+machine_clock*0.65)*0.09
		points.append(chart.position+chart.size*Vector2(x,y))
	painter.draw_polyline(points,Color("72bcb6"),0.9,true)

func draw_projection(prop: Dictionary) -> void:
	# Source-independent light layer; physical housing and collision remain fixed.
	var bounds: Rect2=prop_visual_bounds(prop)
	var base: Vector2=bounds.position+bounds.size*Vector2(0.5,0.60)
	var radius: float=bounds.size.x*0.23
	var height: float=bounds.size.y*0.30
	var color:=Color(0.30,0.72,0.78,0.70)
	for level in range(2):
		var center:=base-Vector2(0,height*float(level))
		var ring_radius: float=radius*(0.35 if level==0 else 1.0)
		var points:=PackedVector2Array()
		for i in range(33):
			var angle:=TAU*float(i)/32.0+machine_clock*0.35
			points.append(center+Vector2(cos(angle)*ring_radius,sin(angle)*ring_radius*0.30))
		painter.draw_polyline(points,color,0.8,true)
	for i in range(6):
		var angle:=TAU*float(i)/6.0+machine_clock*0.35
		var radial:=Vector2(cos(angle)*radius,sin(angle)*radius*0.30)
		painter.draw_line(base+radial*0.35,base+radial-Vector2(0,height),Color(color,0.24),0.8,true)
	# Stable spatial points rotate with the visual clock, never random per draw.
	for i in range(24):
		var angle: float=float(i)*2.39996+machine_clock*0.18
		var distance: float=radius*sqrt(float(i+1)/25.0)*0.88
		var point:=base-Vector2(0,height)+Vector2(cos(angle)*distance,sin(angle)*distance*0.30)
		painter.draw_circle(point,0.65,Color(0.55,0.84,0.87,0.72))
	var screen:=Rect2(bounds.position+bounds.size*Vector2(0.43,0.785),bounds.size*Vector2(0.14,0.065))
	painter.draw_line(screen.position+Vector2(1,screen.size.y*0.5),screen.position+Vector2(screen.size.x*(0.6+0.2*sin(machine_clock)),screen.size.y*0.5),color,0.8,true)

