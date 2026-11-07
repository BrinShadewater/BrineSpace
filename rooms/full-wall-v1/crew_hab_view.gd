extends "res://rooms/whole-room/crew_hab_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("crew-hab-berth-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	full_wall.apply(self)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		draw_berth_lamp(prop)
		return
	super.draw_registered_prop(prop)

func draw_prop_base(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	super.draw_prop_base(prop)

func draw_prop_animation(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		draw_berth_lamp(prop)
		return
	super.draw_prop_animation(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if full_wall.owns(prop): return prop.registration.has("reading_lamp")
	return super.is_animated_prop(prop)

func draw_berth_lamp(prop: Dictionary) -> void:
	var reg: Dictionary=prop.registration
	if not operating or not reg.has("reading_lamp"): return
	var scale_value: float=prop.rect.size.x/reg.width
	var anchor:=Vector2(prop.rect.get_center().x,prop.rect.end.y+float(prop.get("visual_y_offset",0.0)))
	var points:=PackedVector2Array()
	for value in reg.reading_lamp:
		var point:=preload("res://scripts/room_asset_library.gd").source_uv(reg,Vector2(value[0],value[1]))
		points.append(anchor+(point-reg.pivot)*scale_value)
	# A reading light is steady; machine activity must not make it flicker.
	painter.draw_colored_polygon(points,Color(.93,.75,.44,.65))

