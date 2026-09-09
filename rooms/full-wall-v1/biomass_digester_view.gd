extends "res://rooms/power-expansion-v1/biomass_digester_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("biomass-processing-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	# The wall skid replaces the original digestion skid, including its fixed service run.
	props=props.filter(func(prop): return prop.id!="power_machine")
	full_wall.apply(self)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		if operating:
			var point: Vector2={"":Vector2(1570,319),"south":Vector2(675,157),"west":Vector2(542,596),"east":Vector2(1023,596)}.get(prop.side_view,Vector2.ZERO)
			var scale: float=prop.rect.size.x/prop.registration.width
			var anchor := Vector2(prop.rect.get_center().x,prop.rect.end.y+float(prop.get("visual_y_offset",0.0)))
			painter.draw_circle(anchor+(point-prop.registration.pivot)*scale,1.2,Color(0.65,0.52,0.20,0.3+0.2*sin(machine_clock*2)))
		return
	super.draw_registered_prop(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if full_wall.owns(prop): return true
	return super.is_animated_prop(prop)

