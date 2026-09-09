extends "res://rooms/whole-room/underwater_life_support_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/split_wall_prop.gd").new("life-support-wall")

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
		if operating and prop.id.ends_with("_fan"):
			var locations: Array={"north":[Vector2(0.39,0.45),Vector2(0.71,0.45)],"south":[Vector2(0.40,0.49),Vector2(0.71,0.49)],"east":[Vector2(0.43,0.31),Vector2(0.43,0.72)],"west":[Vector2(0.55,0.31),Vector2(0.55,0.72)]}[prop.side_view]
			for location in locations:
				var center: Vector2=prop.rect.position+location*prop.rect.size
				for blade in range(3):
					var direction := Vector2.from_angle(machine_clock*1.6+blade*TAU/3)
					painter.draw_line(center+direction*2,center+direction*8,Color(0.40,0.51,0.52,0.22),0.6)
		return
	super.draw_registered_prop(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if full_wall.owns(prop): return prop.id.ends_with("_fan")
	return super.is_animated_prop(prop)

