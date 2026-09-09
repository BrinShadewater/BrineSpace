extends "res://rooms/production-ten/mining_drone_bay_view.gd"
## Engineering fabrication cradle, panel bench and pressure launch trunk.
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
			DroneArt.draw_asset(painter,"cradle",center,90)
			if not drone_deployed: DroneArt.draw_drone(painter,"construction",center-Vector2(0,15),70,machine_clock,false,false)
		"construction_bench": DroneArt.draw_asset(painter,"bench",center,100)
		"construction_hatch": DroneArt.draw_hatch(painter,center,90,hatch_open)
		"construction_panels":
			DroneArt.draw_asset(painter,"panels",Vector2(center.x,prop.rect.end.y-90.0*730.0/820.0*0.5),90)

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	# Match the fleet renderer's actual draw sizes, not the placeholder outline.
	var bounds_helper=preload("res://rooms/production-ten/drone_prop_bounds.gd")
	var center:=Vector2(prop.rect.get_center().x,prop.rect.end.y-35)
	if prop.id in ["construction_rov","construction_hatch"]:
		return bounds_helper.bounds(prop,"construction")
	if prop.id=="construction_bench": return bounds_helper.asset_rect("bench",center,100)
	if prop.id=="construction_panels":
		var size:=Vector2(90,90.0*730.0/820.0)
		return Rect2(Vector2(center.x-size.x*0.5,prop.rect.end.y-size.y),size)
	return super.prop_visual_bounds(prop)
