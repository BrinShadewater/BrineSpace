extends "res://rooms/whole-room/nursery_south_facing.gd"
## Shared painted prop-room shell. Each leaf owns a stable room id and Studio layout.
var room_id := "aquarium"
var survey_clock := 0.0
var survey_status := "yellow"
const Library = preload("res://scripts/room_asset_library.gd")
const Store = preload("res://scripts/room_layout_store.gd")
func rebuild() -> void:
 layout=[{"cell":Vector2i.ZERO,"rotation":quarter,"kind":3}]
 edges=Geometry.edges(layout)
 for edge in edges:edge.open=edge.port
 props=[]
 actor=Vector2.ZERO
 queue_redraw()
func configure_embedded(q:int,open_sides:Array,running:bool,time_seconds:float,omitted_sides:Array=[]) -> void:
 super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
 Store.apply(self,"room-"+room_id)
 after_layout_apply()
func after_layout_apply() -> void:
 if room_id!="survey_probe_bay":return
 props=props.filter(func(p):return p.id!="survey_hatch")
 props.append(preload("res://scripts/survey_probe_art.gd").launcher(quarter))
func draw_room_floor(center:Vector2) -> void:
 var category=preload("res://scripts/room_database.gd").get_room(room_id).get("category","Operations")
 var tint={"Recreation":Color("44413b"),"Life Support":Color("35413b"),"Robotics":Color("303d43"),"Anomaly":Color("3d3844")}.get(category,Color("3e3a3a"))
 RoomFloor.draw_profile_floor(self,painter,center,tint)
func draw_floor_overlays(_center:Vector2) -> void:pass
func draw_registered_prop(prop:Dictionary) -> void:
 if prop.id=="survey_hatch":preload("res://scripts/survey_probe_art.gd").interior(self,prop)
 elif prop.get("library_asset",false):Library.draw(self,prop)
func is_animated_prop(prop:Dictionary) -> bool:
 return prop.id=="survey_hatch" or prop.get("registration",{}).has("aquarium")


func prop_visual_bounds(prop:Dictionary) -> Rect2:
 if prop.id=="survey_hatch" and quarter==0:return prop.rect.merge(Rect2(-28,-178,48,68))
 if prop.id=="survey_hatch":return prop.rect
 return super.prop_visual_bounds(prop)
