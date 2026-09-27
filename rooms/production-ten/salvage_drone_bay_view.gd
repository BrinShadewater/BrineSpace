extends "res://rooms/whole-room/life_support_view.gd"
## Salvage bay. The dock is the only built-in prop: the old winch, sorter and separate
## hatch retired with the Sept 27 drone art (station props furnish the room).
var drone_deployed := false
var hatch_open := 0.0
const Dressing = preload("res://rooms/whole-room/room_dressing.gd")
var dressing: RefCounted
func _ready() -> void:
	super._ready()
	var image := Image.new()
	# The walls still sample this atlas (draw_wall, draw_cap).
	preload("res://scripts/safe_image.gd").load_png(image, "res://legacy/default/assets/rooms/salvage-drone-bay/source/overhead.png")
	life_texture=ImageTexture.create_from_image(image)
	life_items=[
		{"id":"salvage_rov","rect":Rect2(-156,-143,90,64),"pivot":Vector2(347,585),"width":344.0,"outline":[Vector2(179,256),Vector2(191,253),Vector2(191,224),Vector2(209,216),Vector2(225,220),Vector2(225,174),Vector2(237,163),Vector2(282,163),Vector2(286,141),Vector2(302,133),Vector2(389,133),Vector2(410,145),Vector2(410,162),Vector2(452,163),Vector2(467,177),Vector2(467,216),Vector2(498,217),Vector2(506,239),Vector2(516,275),Vector2(514,319),Vector2(506,332),Vector2(516,346),Vector2(516,528),Vector2(503,552),Vector2(473,554),Vector2(453,579),Vector2(429,585),Vector2(400,562),Vector2(389,550),Vector2(306,550),Vector2(286,575),Vector2(267,584),Vector2(238,568),Vector2(227,550),Vector2(177,552)]}
	]
	dressing=Dressing.new(self,"res://rooms/production-ten/decor/salvage-composition-v2.json")
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
	var top := Rect2(rect.position-Vector2(0,3),rect.size)
	painter.draw_rect(Rect2(top.position+Vector2(0,4),top.size),Color("292d2e"))
	var span := rect.size.x if horizontal else rect.size.y
	var cursor := 0.0
	while cursor<span:
		var length := minf(48,span-cursor)
		var target := Rect2(top.position+Vector2(cursor,0),Vector2(length,top.size.y)) if horizontal else Rect2(top.position+Vector2(0,cursor),Vector2(top.size.x,length))
		painter.draw_texture_rect_region(life_texture,target,Rect2(223,39,122,58) if horizontal else Rect2(50,118,39,169))
		cursor+=length

func draw_cap(rect: Rect2) -> void:
	painter.draw_texture_rect_region(life_texture,Rect2(rect.position-Vector2(0,3),rect.size),Rect2(52,37,48,44))

func effect_marks(_prop: Dictionary,_time: float) -> Array: return []
func is_animated_prop(prop: Dictionary) -> bool: return prop.id=="salvage_rov"

func prop_visual_bounds(prop: Dictionary) -> Rect2:
	if prop.id=="salvage_rov":return preload("res://scripts/drone_dock.gd").visual_bounds(preload("res://scripts/drone_dock.gd").legacy_rect(prop,"salvage"))
	if prop.get("library_asset",false): return preload("res://scripts/room_asset_library.gd").bounds(prop)
	return super.prop_visual_bounds(prop)

func draw_registered_prop(prop: Dictionary) -> void:
	if prop.id == "salvage_rov":
		var Dock=preload("res://scripts/drone_dock.gd")
		Dock.draw(painter,Dock.legacy_rect(prop,"salvage"),"salvage",drone_visual,operating,machine_clock)
		return
	if dressing!=null: dressing.draw(prop)
