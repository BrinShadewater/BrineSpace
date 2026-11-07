extends "res://rooms/production-ten/quarantine_cell_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("quarantine-specimen-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	var retained: Array=[]
	if quarter==2:
		for prop in props:
			var spec: Dictionary=prop.get("registration",{}).get("spec",{})
			if prop.id in ["quarantine_berth","quarantine_filter","quarantine_monitor"] or spec.get("centerpiece",false) or spec.get("authored_anchor",false): retained.append(prop.duplicate(true))
	full_wall.apply(self)
	# Standalone saved furniture must survive the legacy q2 bank restoration.
	var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
	if authored.get("full_wall_"+full_wall.asset_id,0)==null: return
	if quarter==2:
		props=props.filter(func(prop): return full_wall.owns(prop))
		for prop in retained:
			var stations={"quarantine_berth":Vector2(47,-100),"quarantine_filter":Vector2(-157,-105),"quarantine_monitor":Vector2(-49,-100)}
			if stations.has(prop.id): prop.rect.position=stations[prop.id]
			prop.sort_y=prop.rect.end.y
			props.append(prop)

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

