extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("anomaly-containment-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	var platform := {}
	if posmod(q,4)==2:
		for prop in props:
			if prop.id=="anomaly_platform": platform=prop.duplicate(true)
	full_wall.apply(self)
	# The overhead bank must not discard the separate functioning specimen platform.
	if not platform.is_empty():
		var present := false
		for prop in props:
			if prop.id=="anomaly_platform": present=true
		if not present:
			platform.rect.position=Vector2(48,-25.7391357421875)
			platform.sort_y=platform.rect.end.y
			props.append(platform)

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	super.draw_registered_prop(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if full_wall.owns(prop): return false
	return super.is_animated_prop(prop)

