extends "res://rooms/production-ten/ore_refinery_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("ore-refinery-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	# Without a rebuild the bank is already installed; re-arranging the retained
	# props from their moved positions would drift them on every configure.
	if props.any(func(prop): return full_wall.owns(prop)):
		full_wall.apply(self)
		return
	var retained: Array=[]
	if q==3:
		for prop in props:
			var spec: Dictionary=prop.get("registration",{}).get("spec",{})
			if prop.id in ["refinery_crusher","refinery_hopper"] or spec.get("centerpiece",false) or spec.get("authored_anchor",false): retained.append(prop.duplicate(true))
	full_wall.apply(self)
	if q==3 and not retained.is_empty():
		var bank: Array=[]
		for prop in props:
			if full_wall.owns(prop): bank.append(prop)
		for prop in retained:
			if prop.id=="refinery_crusher": prop.rect.position=Vector2(-148,-100)
			elif prop.id=="refinery_hopper": prop.rect.position=Vector2(16,-94)
			prop.sort_y=prop.rect.end.y
			bank.append(prop)
		props=bank
		preload("res://scripts/room_layout_store.gd").apply(self,"ore-refinery-wall")

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

