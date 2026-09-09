extends "res://rooms/whole-room/nursery_south_facing.gd"
const Corridor=preload("res://rooms/underwater/corridor_geometry.gd")
const Surface=preload("res://rooms/underwater/corridor_surfaces.gd")
var room_id:="corridor"
var sources: Array=[]
func _ready() -> void:
	sources=Surface.load_sources()
	rebuild()
func rebuild() -> void:
	props=[]
	layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":1 if room_id=="corridor" else 2 if room_id=="corner" else 4}]
	edges=Geometry.edges(layout)
func draw_room_world(include_floor:=true) -> void:
	if include_floor: draw_room_floor(Vector2.ZERO)
	for prop in props:
		if preload("res://scripts/room_layout_store.gd").surface_positions(self).get("hidden/"+str(prop.id),false): continue
		preload("res://scripts/room_layout_store.gd").draw_flip(self,painter,prop,view_origin,view_scale)
		preload("res://scripts/room_asset_library.gd").draw(self,prop)
	painter.draw_set_transform(view_origin,0,Vector2.ONE*view_scale)
func draw_room_floor(_center: Vector2) -> void:
	var corner:=room_id=="corner"
	var tee:=room_id=="tee_corridor"
	Surface.draw_hull(painter,Corridor.hull_for(corner,tee),Corridor.floor_for(corner,tee),Vector2.ZERO,Corridor.rotation({"id":room_id,"rotation":quarter}),sources,corner,operating,-1,tee,0,preload("res://scripts/room_layout_store.gd").surface_positions(self))
func draw_floor_overlays(_center: Vector2) -> void: pass
func prop_visual_bounds(prop: Dictionary) -> Rect2: return prop.rect
