extends "res://rooms/production-ten/construction_drone_bay_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("construction-fabrication-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	var retained: Array=[]
	if q==3:
		for prop in props:
			if prop.id in ["construction_rov","construction_hatch","construction_bench"]: retained.append(prop.duplicate(true))
	full_wall.apply(self)
	# Saved standalone furnishing supersedes the old bank restoration.
	var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
	if authored.get("full_wall_"+full_wall.asset_id,0)==null: return
	if q==3 and not retained.is_empty():
		var bank: Array=[]
		for prop in props:
			if full_wall.owns(prop): bank.append(prop)
		var stations={"construction_rov":Vector2(67,-90),"construction_hatch":Vector2(-157,-90),"construction_bench":Vector2(-45,-115)}
		for prop in retained:
			prop.rect.position=stations[prop.id]
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

