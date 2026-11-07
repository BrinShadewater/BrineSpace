extends "res://character/bill-floor-case-north-v1/workshop_preview.gd"
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
var bound_room:Dictionary={}
func bind_room(room:Dictionary)->void:
 bound_room=room;sync_case()
func sync_case()->void:
 var data:Dictionary=FLOOR.payload(bound_room)
 case_enabled=not data.is_empty()
 case_anchor=Vector2(data.anchor) if case_enabled else Vector2.ZERO
func configure_embedded(q:int,open_sides:Array,running:bool,time_seconds:float,omitted_sides:Array=[])->void:
 super.configure_embedded(q,open_sides,running,time_seconds,omitted_sides)
 sync_case()
