extends "res://rooms/underwater/acoustic-comms/radio_lab_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("radio-signal-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	# Without a rebuild the bank is already installed; re-anchoring the equipment
	# from its moved bounds accumulates float drift on every configure.
	if props.any(func(prop): return full_wall.owns(prop)):
		full_wall.apply(self)
		return
	var radio_equipment := {}
	if posmod(q,4)==2:
		for prop in props:
			var spec: Dictionary=prop.get("registration",{}).get("spec",{})
			if prop.id in ["acoustic_listener","acoustic_transducers","acoustic_receiver"] or spec.get("centerpiece",false) or spec.get("authored_anchor",false):
				radio_equipment[prop.id]=prop.duplicate(true)
	full_wall.apply(self)
	if posmod(q,4)==2:
		# Keep the live signal equipment separate from the static south workbench.
		var retained: Array=[]
		for prop in props:
			if prop.get("full_wall",false): retained.append(prop)
		var positions := {"acoustic_listener":Vector2(-168,-164),"acoustic_transducers":Vector2(60,-164),"acoustic_receiver":Vector2(-36,24)}
		for id in positions:
			if not radio_equipment.has(id): continue
			var prop: Dictionary=radio_equipment[id]
			prop.rect.position+=positions[id]-prop_visual_bounds(prop).position
			prop.sort_y=prop.rect.end.y
			retained.append(prop)
		for id in radio_equipment:
			if id not in positions: retained.append(radio_equipment[id])
		props=retained
		# Register the retained equipment like the bank's props, so a later configure
		# without rebuild sees identical prop data.
		preload("res://scripts/room_layout_store.gd").apply(self,"radio-signal-wall")

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

