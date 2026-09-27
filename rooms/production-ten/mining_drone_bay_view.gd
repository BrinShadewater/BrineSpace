extends "res://rooms/whole-room/life_support_view.gd"
## Mining bay. The dock is the only built-in prop: the old service rig, tether and separate
## hatch retired with the Sept 27 drone art (station props furnish the room).
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var drone_deployed := false
var hatch_open := 0.0
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	preload("res://scripts/safe_image.gd").load_png(image, "res://legacy/default/assets/rooms/mining-drone-bay/source/overhead.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"mining_rov","rect":Rect2(-156,-143,90,64),"pivot":Vector2(343,556),"width":290.0,"outline":[Vector2(200,280),Vector2(215,256),Vector2(218,209),Vector2(231,181),Vector2(253,173),Vector2(283,174),Vector2(284,149),Vector2(297,138),Vector2(391,137),Vector2(405,149),Vector2(405,190),Vector2(435,205),Vector2(465,206),Vector2(471,226),Vector2(478,494),Vector2(488,508),Vector2(487,542),Vector2(466,556),Vector2(219,555),Vector2(198,535)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/mining-composition-v2.json")
	rebuild()

func rebuild() -> void:
	super.rebuild()
	layout[0].kind=1 # Canonical north/south straight.
	edges=Geometry.edges(layout)
	for edge in edges: edge.open=edge.port
	if dressing!=null: dressing.place()

func draw_room_floor(center: Vector2) -> void:
	RoomFloor.draw_profile_floor(self,painter,center,Color("525c60"),Color(0.17,0.19,0.20,0.35),2)
	RoomFloor.draw_profile_dressing(self,painter,center,edges,"steel")
	if dressing!=null: dressing.floor()

func draw_wall(rect: Rect2,horizontal: bool) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").wall(painter,rect,horizontal,"engineering")

func draw_cap(rect: Rect2) -> void:
	preload("res://rooms/whole-room/department_wall_material.gd").cap(painter,rect,"engineering")

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="mining_rov"

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.id=="mining_rov":return preload("res://scripts/drone_dock.gd").visual_bounds(preload("res://scripts/drone_dock.gd").legacy_rect(prop,"mining"))
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id == "mining_rov":
		var Dock=preload("res://scripts/drone_dock.gd")
		Dock.draw(painter,Dock.legacy_rect(prop,"mining"),"mining",drone_visual,operating,machine_clock)
		return
	if dressing!=null: dressing.draw(prop)
