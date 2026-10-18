extends SceneTree
const Queue=preload("res://scripts/hand_image_preparation.gd")
const Floors=preload("res://rooms/whole-room/modular_floor.gd")
const Walls=preload("res://rooms/whole-room/painted_shell.gd")
class Hand extends RefCounted:
 var hand:Array=["solar_array","galley"]
 var selected_card_id:="solar_array"
 var selected_rotation:=0
 func _default_card_rotation(_id):return 0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var grid=preload("res://scripts/grid_canvas.gd").new()
 var hand=Hand.new()
 hand.selected_card_id=""
 grid.prepare_hand_images(hand)
 hand.selected_card_id="galley"
 var records:Array=grid._surface_image_records("galley",0)
 check(not records.is_empty(),"Selected blueprint has actual surface images")
 var deadline:=Time.get_ticks_msec()+3000
 while Time.get_ticks_msec()<deadline:
  var before:=Floors.textures.size()+Walls.textures.size()
  grid.prepare_hand_images(hand)
  grid.prepare_hand_images(hand)
  check(Floors.textures.size()+Walls.textures.size()-before<=1,"At most one prepared surface uploads per frame")
  if records.all(func(r):return Floors.textures.has(r.key) if r.kind=="floor" else Walls.textures.has(r.key)):break
  await process_frame
 check(records.all(func(r):return Floors.textures.has(r.key) if r.kind=="floor" else Walls.textures.has(r.key)),"Selected room surfaces upload before placement")
 var textures:=Floors.textures.size()+Walls.textures.size()
 hand.selected_card_id=""
 for i in range(10):grid.prepare_hand_images(hand);await process_frame
 check(Floors.textures.size()+Walls.textures.size()==textures,"Unselected hand does not preupload more GPU surfaces")
 Queue.clear();grid.free()
 print("TABLET PLACEMENT PREPARATION ",failures," failures")
 quit(0 if failures==0 else 1)
