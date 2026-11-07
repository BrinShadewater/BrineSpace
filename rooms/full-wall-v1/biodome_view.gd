extends "res://rooms/underwater/batch-two/biodome_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("biodome-habitat-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	var retained: Array=[]
	if q==3:
		for prop in props:
			var spec: Dictionary=prop.registration.get("spec",{})
			if prop.id in ["biodome_tree","biodome_aquatic"] or spec.get("centerpiece",false) or spec.get("authored_anchor",false):
				retained.append(prop.duplicate(true))
	full_wall.apply(self)
	# Saved standalone furnishing supersedes the old bank restoration.
	var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
	if authored.get("full_wall_"+full_wall.asset_id,0)==null: return
	if q==3 and not retained.is_empty():
		var bank: Array=[]
		for prop in props:
			if full_wall.owns(prop): bank.append(prop)
		for prop in retained:
			if prop.id in ["biodome_tree","biodome_aquatic"]:
				prop.rect.position=Vector2(-156.959182739258,-90) if prop.id=="biodome_tree" else Vector2(57,-90)
			prop.sort_y=prop.rect.end.y
			bank.append(prop)
		props=bank

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

