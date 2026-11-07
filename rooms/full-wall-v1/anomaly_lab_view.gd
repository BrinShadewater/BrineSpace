extends "res://rooms/underwater/batch-two/anomaly_lab_view.gd"
## Balanced full-wall installation; original view is the reversible baseline.
var full_wall = preload("res://rooms/full-wall-v1/full_wall_prop.gd").new("anomaly-containment-wall")

func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
	# Without a rebuild the bank is already installed; keep the arranged props.
	if props.any(func(prop): return full_wall.owns(prop)):
		full_wall.apply(self)
		configure_bought_effects()
		return
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
			# Register the re-added platform the same way the bank's props were, so a
			# later configure without rebuild sees identical prop data.
			preload("res://scripts/room_layout_store.gd").apply(self,full_wall.layout_key(self))

	configure_bought_effects()

const SCREEN_STUDY=Rect2(250,614,31,22)
const TANK_SCREEN=Rect2(375,64,18,10)
const EFFECT_PROPS=["library/tileset-hss-53","library/tileset-mb-45b","library/tileset-cyb-123"]
func configure_bought_effects()->void:
	for prop in props:
		if prop.id in EFFECT_PROPS:prop.custom_library_draw=true

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	if full_wall.owns(prop): return full_wall.bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop:Dictionary)->void:
	if prop.id=="library/tileset-cyb-123":
		draw_orb_study(prop)
		return
	if full_wall.owns(prop) and prop.id not in EFFECT_PROPS:
		full_wall.draw(self,prop)
		return
	if prop.get("library_asset",false):
		preload("res://scripts/room_asset_library.gd").draw(self,prop)
	else:
		super.draw_registered_prop(prop)
	if prop.id not in ["library/tileset-hss-53","library/tileset-mb-45b"]:return
	var aperture=SCREEN_STUDY if prop.id=="library/tileset-hss-53" else TANK_SCREEN
	var reg=prop.registration
	var factor=prop.rect.size.x/reg.width
	var anchor=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	var origin=anchor+(aperture.position-reg.pivot)*factor
	painter.draw_rect(Rect2(origin,aperture.size*factor),Color("10191c"))
	if not operating:return
	if prop.id=="library/tileset-mb-45b":
		for bar in range(3):
			var height=3+2*sin(machine_clock*2+bar)
			painter.draw_rect(Rect2(origin+Vector2(3+bar*5,8-height)*factor,Vector2(2,height)*factor),Color("75a8ba"))
		return
	var points=PackedVector2Array()
	for step in range(9):
		points.append(origin+Vector2(3+25.0*step/8.0,11+3*sin(step*1.7+machine_clock*3))*factor)
	painter.draw_polyline(points,Color("87baa8"),maxf(.55,factor))

func is_animated_prop(prop: Dictionary) -> bool:
	if prop.id in EFFECT_PROPS:return operating
	if full_wall.owns(prop): return false
	return super.is_animated_prop(prop)


func draw_orb_study(prop:Dictionary)->void:
	var reg=prop.registration
	var factor=prop.rect.size.x/reg.width
	var anchor=Vector2(prop.rect.get_center().x,prop.rect.end.y)
	var origin=anchor+(Vector2(386,586)-reg.pivot)*factor
	# Retain the lower source stand; the projection is a separately drawn layer.
	painter.draw_texture_rect_region(prop.library_texture,Rect2(origin+Vector2(0,42)*factor,Vector2(45,44)*factor),Rect2(386,628,45,44))
	var emitter=origin+Vector2(22,42)*factor
	var rim=PackedVector2Array()
	for i in range(25):
		var angle=TAU*i/24.0
		rim.append(emitter+Vector2(cos(angle)*12,sin(angle)*3.84)*factor)
	painter.draw_colored_polygon(rim,Color("17252b"))
	painter.draw_polyline(rim,Color("48565a"),maxf(.5,factor))
	if operating:
		var lift=.8+.7*sin(machine_clock*2)
		painter.draw_texture_rect_region(prop.library_texture,Rect2(origin+Vector2(0,-lift)*factor,Vector2(45,42)*factor),Rect2(386,586,45,42),Color(.85,.95,1,.88))
