extends SceneTree
const View=preload("res://rooms/underwater/airlock-v1/airlock_view.gd")
const Geometry=preload("res://tools/modular_room_geometry.gd")
const OUT="res://output/bill-airlock-release-20260912/visibility/"
class Preview extends Node2D:
 var room
 func _draw():
  draw_rect(Rect2(0,0,512,512),Color("20333b"))
  room.render_into(self,Vector2(256,280),1.0)
func _init():call_deferred("run")
func capture(preview):
 preview.queue_redraw()
 await process_frame
 await RenderingServer.frame_post_draw
 return root.get_texture().get_image()
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 DirAccess.make_dir_recursive_absolute(OUT)
 root.size=Vector2i(512,512);root.content_scale_size=root.size
 var grid=load("res://scripts/grid_canvas.gd").new();grid._load_major_bill_animations()
 var room=View.new();room.embedded=true;root.add_child(room);room.hide()
 var preview=Preview.new();preview.room=room;root.add_child(preview)
 var failures:=0
 for q in range(4):
  for wet in [false,true]:
   room.configure_embedded(q,[],false,0)
   room.cycle_pose=preload("res://scripts/airlock_cycle.gd").pose({"airlock_cycle":{"phase":"exterior" if wet else "dry","elapsed":0.0}})
   room.actor=Geometry.turn(Vector2(0,-70),q)
   room.external_actor_texture=grid.human_water_player.equipment_frames["diving-helmet"]["tread-east" if wet else "idle-east"][0]
   room.show_actor=false
   await capture(preview)
   var before: Image=await capture(preview)
   room.show_actor=true
   var after: Image=await capture(preview)
   var changed:=0
   for y in range(512):
    for x in range(512):
     if before.get_pixel(x,y)!=after.get_pixel(x,y):changed+=1
   if changed<30:failures+=1;push_error("Airlock hides crew q%d wet=%s pixels=%d"%[q,wet,changed])
   if room.flood_water!=0:failures+=1;push_error("Chamber water leaked into room state")
   after.save_png(OUT+"q%d-%s.png"%[q,"wet" if wet else "dry"])
   print("VISIBILITY q%d wet=%s changed=%d"%[q,wet,changed])
 grid.free();room.queue_free();preview.queue_free()
 print("AIRLOCK ACTOR VISIBILITY: %d failures"%failures)
 quit(1 if failures else 0)
