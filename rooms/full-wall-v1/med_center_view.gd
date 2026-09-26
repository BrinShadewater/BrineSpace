extends "res://rooms/underwater/batch-two/med_center_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("medical-diagnostic-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	var retained: Array=[]
	if q==3:
		for prop in props:
			var spec: Dictionary=prop.get("registration",{}).get("spec",{})
			if prop.id in ["medical_treatment","medical_imaging","medical_supplies"] or spec.get("centerpiece",false) or spec.get("authored_anchor",false): retained.append(prop.duplicate(true))
	full_wall.apply(self)
	# Standalone layouts already contain their complete, explicitly placed props.
	# The old bank-specific q3 restoration would discard the diagnostic console.
	var authored_layout: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
	if authored_layout.get("full_wall_"+full_wall.asset_id,0)==null: return
	if q==3 and not retained.is_empty():
		var bank: Array=[]
		for prop in props:
			if full_wall.owns(prop): bank.append(prop)
		# Keep the three stations against the closed north wall so the two side
		# doors retain one continuous crew route through the room.
		var stations={"medical_treatment":Vector2(-158,-150),"medical_imaging":Vector2(-53,-150),"medical_supplies":Vector2(54,-145)}
		for prop in retained:
			var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
			if authored.has(str(prop.id)) and authored[str(prop.id)]==null: continue
			preload("res://scripts/room_layout_store.gd").resize_prop(prop,authored.get("size/"+str(prop.id),[1.0,1.0]))
			var saved=authored.get(str(prop.id))
			if saved is Array and saved.size()==2:
				prop.rect.position=Vector2(saved[0],saved[1])
			elif stations.has(prop.id):
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
	if full_wall.owns(prop): return prop.registration.has("operating_screens")
	return super.is_animated_prop(prop)

