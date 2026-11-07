extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
class Room extends Node:
 const Geometry=preload("res://tools/modular_room_geometry.gd")
 var quarter=0
 var layout=[{"kind":2,"rotation":0,"cell":Vector2i.ZERO}]
 var props=[{"id":"bank","rect":Rect2(80,-170,70,150),"sort_y":-20,"validate_directional_layout":true}]
 func prop_visual_bounds(p):return p.rect
func _init():call_deferred("run")
func run():
 Store.loaded=true;Store.data={};Store.defaults_path="user://missing-layout-defaults.json"
 for mode in ["implicit","free","constrained","detached"]:
  var view=Room.new()
  var values={"bank":[90,-210],"size/bank":[1.15,1.15]}
  if mode=="free":values.__free_placement=true
  if mode=="constrained":values.__free_placement=false
  if mode=="detached":values.bank=[900,900]
  Store.data={"fixture/0":values};Store.apply(view,"fixture")
  var wanted=Rect2(90,-210,80.5,172.5) if mode in ["implicit","free"] else Rect2(80,-170,70,150)
  assert(view.props[0].rect.is_equal_approx(wanted),"Free-placement parity and constrained/stale guards: "+mode)
  assert(Store.data["fixture/0"]==values,"Validation never rewrites author data")
  view.free()
 var prop={"rect":Rect2(10,20,100,100),"collision_boxes":[[0,0,1,.29],[0,.29,.25,.71]]}
 var boxes=Geometry.prop_collision_rects(prop)
 assert(boxes.size()==2 and boxes[0].has_point(Vector2(60,30)) and boxes[1].has_point(Vector2(20,90)))
 assert(not boxes[0].has_point(Vector2(80,90)) and not boxes[1].has_point(Vector2(80,90)),"Corner's empty notch stays traversable")
 prop.layout_flip=Vector2(-1,1);boxes=Geometry.prop_collision_rects(prop)
 assert(boxes[1].has_point(Vector2(100,90)) and not boxes[1].has_point(Vector2(20,90)),"Collision follows mirrored furniture")
 assert(Store.navigation_stamp({"a/0":{"flip/bank":[true,false]}})!=Store.navigation_stamp({"a/0":{"flip/bank":[false,false]}}))
 assert(Store.navigation_stamp({"a/0":{"__free_placement":true}})!=Store.navigation_stamp({"a/0":{"__free_placement":false}}),"Placement-mode changes invalidate crew routes")
 print("FREE PLACEMENT PASS: implicit/explicit free authoring, constrained/stale fallback, unchanged saves, notched and mirrored collision")
 quit()
