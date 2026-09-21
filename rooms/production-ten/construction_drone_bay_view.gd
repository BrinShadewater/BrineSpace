extends "res://rooms/production-ten/mining_drone_bay_view.gd"
## Engineering fabrication cradle, panel bench and pressure launch trunk.
var panel_textures: Dictionary = {}
var bench_textures: Dictionary = {}
var hatch_textures: Dictionary = {}
var cradle_textures: Dictionary = {}

func _cradle_texture(prop: Dictionary) -> ImageTexture:
	var facing := _panel_facing(prop)
	if not cradle_textures.has(facing):
		cradle_textures[facing] = DroneArt._decode_matte("res://legacy/retired/assets/rooms/construction-drone-bay/material/cradle-square-%s.png" % facing)
	return cradle_textures[facing]

func _cradle_bounds(prop: Dictionary) -> Rect2:
	var size := Vector2(_cradle_texture(prop).get_size())
	size *= minf(90.0/size.x,(90.0*320.0/370.0)/size.y)
	return Rect2(Vector2(prop.rect.get_center().x,prop.rect.end.y-35.0)-size*0.5,size)

func _hatch_texture(prop: Dictionary) -> ImageTexture:
	var facing := _panel_facing(prop)
	if not hatch_textures.has(facing):
		hatch_textures[facing] = DroneArt._decode_matte("res://legacy/retired/assets/rooms/construction-drone-bay/material/hatch-overhead-%s.png" % facing)
	return hatch_textures[facing]

func _hatch_bounds(prop: Dictionary) -> Rect2:
	var size := Vector2(_hatch_texture(prop).get_size())
	size *= minf(90.0/size.x,(90.0*340.0/390.0)/size.y)
	return Rect2(Vector2(prop.rect.get_center().x,prop.rect.end.y-35.0)-size*0.5,size)

func _draw_overhead_hatch(target: CanvasItem, prop: Dictionary, opened: float) -> void:
	var texture := _hatch_texture(prop)
	var bounds := _hatch_bounds(prop)
	target.draw_texture_rect(texture,bounds,false)
	if opened<=0.0: return
	var centers := {"down":Vector2(479,478),"right":Vector2(478,480),"up":Vector2(480,515),"left":Vector2(515,479)}
	var scale := bounds.size.x / float(texture.get_width())
	var center: Vector2 = bounds.position + centers[_panel_facing(prop)]*scale
	var radius := 320.0*scale*clampf(opened,0.0,1.0)
	target.draw_circle(center,radius,Color("091c23"))
	target.draw_arc(center,radius,0,TAU,48,Color("80908c"),1.2,true)

func _bench_texture(prop: Dictionary) -> ImageTexture:
	var facing := _panel_facing(prop)
	if not bench_textures.has(facing):
		bench_textures[facing] = DroneArt._decode_matte("res://legacy/retired/assets/rooms/construction-drone-bay/material/bench-overhead-%s.png" % facing)
	return bench_textures[facing]

func _bench_bounds(prop: Dictionary) -> Rect2:
	var size := Vector2(_bench_texture(prop).get_size())
	size *= minf(100.0/size.x,(100.0*350.0/450.0)/size.y)
	return Rect2(Vector2(prop.rect.get_center().x-size.x*0.5,prop.rect.end.y-35.0-size.y*0.5),size)

func _panel_facing(prop: Dictionary) -> String:
	var center: Vector2 = prop.rect.get_center()
	if absf(center.x) > absf(center.y): return "right" if center.x < 0 else "left"
	return "down" if center.y < 0 else "up"

func _panel_texture(prop: Dictionary) -> ImageTexture:
	var facing := _panel_facing(prop)
	if not panel_textures.has(facing):
		panel_textures[facing] = DroneArt._decode_matte("res://legacy/retired/assets/rooms/construction-drone-bay/material/panel-pallet-%s.png" % facing)
	return panel_textures[facing]

func _panel_bounds(prop: Dictionary) -> Rect2:
	var tex := _panel_texture(prop)
	var size := Vector2(tex.get_size())
	size *= minf(90.0 / size.x, (90.0 * 730.0 / 820.0) / size.y)
	return Rect2(Vector2(prop.rect.get_center().x-size.x*0.5,prop.rect.end.y-size.y),size)

func _ready() -> void:
	super._ready()
	dressing = null
	life_items = [
		{"id":"construction_rov","rect":Rect2(-156,-143,90,64)},
		{"id":"construction_bench","rect":Rect2(66,-143,90,64)},
		{"id":"construction_hatch","rect":Rect2(-156,-12,90,64)},
		{"id":"construction_panels","rect":Rect2(66,79,90,64)}
	]
	for item in life_items:
		item["pivot"] = Vector2.ZERO
		item["width"] = 90.0
		item["outline"] = [Vector2(-45,-64),Vector2(45,-64),Vector2(45,0),Vector2(-45,0)]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/construction-composition-v2.json")
	rebuild()

func draw_registered_prop(prop: Dictionary) -> void:
	if dressing!=null and dressing.draw(prop): return
	var center := Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	match prop.id:
		"construction_rov":
			painter.draw_texture_rect(_cradle_texture(prop),_cradle_bounds(prop),false)
			if not drone_deployed: DroneArt.draw_drone(painter,"construction",center-Vector2(0,15),70,machine_clock,false,false)
		"construction_bench": painter.draw_texture_rect(_bench_texture(prop),_bench_bounds(prop),false)
		"construction_hatch": _draw_overhead_hatch(painter,prop,hatch_open)
		"construction_panels":
			painter.draw_texture_rect(_panel_texture(prop),_panel_bounds(prop),false)

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	# Match the fleet renderer's actual draw sizes, not the placeholder outline.
	var bounds_helper=preload("res://rooms/production-ten/drone_prop_bounds.gd")
	var center:=Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	if prop.id=="construction_hatch": return _hatch_bounds(prop)
	if prop.id=="construction_rov":
		return _cradle_bounds(prop).merge(bounds_helper.asset_rect("construction",center-Vector2(0,15),70))
	if prop.id=="construction_bench": return _bench_bounds(prop)
	if prop.id=="construction_panels":
		return _panel_bounds(prop)
	return super.prop_visual_bounds(prop)
