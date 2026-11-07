extends "res://rooms/underwater/acoustic-comms/radio_lab_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("radio-signal-wall")
const SIGNAL_SCREENS=[Rect2(144,322,237,163),Rect2(874,322,237,163)]

func is_signal_console(prop: Dictionary) -> bool:
	return str(prop.get("copy_source",prop.id))=="radio_signal_routing_console"

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
	# Standalone layouts must keep the complete prop set after removing the bank.
	var authored: Dictionary=preload("res://scripts/room_layout_store.gd").shared_positions(full_wall.layout_key(self),quarter)
	if authored.get("full_wall_"+full_wall.asset_id,0)==null: return
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
		preload("res://scripts/room_layout_store.gd").apply(self,full_wall.layout_key(self))

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if full_wall.owns(prop):
		full_wall.draw(self,prop)
		return
	super.draw_registered_prop(prop)
	if is_signal_console(prop): draw_signal_displays(prop)

func is_animated_prop(prop: Dictionary) -> bool:
	if is_signal_console(prop): return operating
	if full_wall.owns(prop): return false
	return super.is_animated_prop(prop)

func draw_signal_displays(prop: Dictionary) -> void:
	# Cover only the source apertures, leaving knobs, cables and bezels intact.
	for index in range(SIGNAL_SCREENS.size()):
		var source: Rect2=SIGNAL_SCREENS[index]
		var start:=life_point(prop,source.position)
		var end:=life_point(prop,source.end)
		var screen:=Rect2(start,end-start)
		painter.draw_rect(screen,Color("101b18"))
		if not operating: continue
		for row in range(1,4):
			var y:=start.y+screen.size.y*float(row)/4.0
			painter.draw_line(Vector2(start.x,y),Vector2(end.x,y),Color(0.20,0.34,0.26,0.45),0.6)
		var points:=PackedVector2Array()
		for i in range(49):
			var x:=float(i)/48.0
			var envelope: float=0.10+0.25*pow(sin(PI*x),2.0)
			if index==1: envelope=0.06+0.30*exp(-pow((x-0.42-0.09*sin(machine_clock*0.6))*5.0,2.0))
			var y:=0.52+sin(x*72.0+machine_clock*2.0+float(index))*envelope
			points.append(start+screen.size*Vector2(x,clampf(y,0.06,0.94)))
		painter.draw_polyline(points,Color("83b78d"),0.8,true)

