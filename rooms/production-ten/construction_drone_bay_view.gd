extends "res://rooms/production-ten/mining_drone_bay_view.gd"
## Engineering fabrication bay. The dock is the only built-in prop: the old bench, panels
## and separate hatch retired with the Sept 27 drone art (station props furnish the room).

func _ready() -> void:
	super._ready()
	dressing = null
	life_items = [{"id":"construction_rov","rect":Rect2(-156,-143,90,64),"pivot":Vector2.ZERO,"width":90.0,
		"outline":[Vector2(-45,-64),Vector2(45,-64),Vector2(45,0),Vector2(-45,0)]}]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/construction-composition-v2.json")
	rebuild()

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id == "construction_rov":
		var Dock=preload("res://scripts/drone_dock.gd")
		Dock.draw(painter,Dock.legacy_rect(prop,"construction"),"construction",drone_visual,operating,machine_clock)
		return
	if dressing!=null: dressing.draw(prop)

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
# The docked drone bobs, so its dock redraws live like the mining and salvage docks.
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="construction_rov"

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.id=="construction_rov":return preload("res://scripts/drone_dock.gd").visual_bounds(preload("res://scripts/drone_dock.gd").legacy_rect(prop,"construction"))
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	return super.prop_visual_bounds(prop)
