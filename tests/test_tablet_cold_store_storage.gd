extends SceneTree
const Cold=preload("res://rooms/underwater/cold-store-v1/cold_store_view.gd")
var failures:=0
class PropCanvas extends Node2D:
 var renderer
 var prop:Dictionary
 func _draw():
  renderer.painter=self;renderer.draw_registered_prop(prop);renderer.painter=renderer
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func view(tablet:bool,preview:=false):
 root.set_meta("tablet_controls",tablet)
 var item=Cold.new();item.hide()
 if preview:item.set_meta("layout_editor_preview",true)
 root.add_child(item);item.set_process(false);item.machine_clock=.5;return item
func picture(item,prop:Dictionary)->PackedByteArray:
 var vp:=SubViewport.new();vp.size=Vector2i(384,384);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas:=PropCanvas.new();canvas.position=Vector2(192,192);canvas.renderer=item;canvas.prop=prop;vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var image=vp.get_texture().get_image();check(image.get_used_rect().has_area(),"Cold Store fallback draws visible pixels")
 var pixels=image.get_data();vp.queue_free();await process_frame;return pixels
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 var tablet=view(true)
 check(tablet.textures.is_empty() and tablet.regions.is_empty(),"Tablet Cold Store must not upload unused retired furniture sheets")
 var reference=view(false);check(reference.textures.size()==2,"Desktop keeps eager original furniture")
 var preview=view(true,true);check(preview.textures.size()==2,"Editor preview keeps original furniture")
 for quarter in 4:
  tablet.quarter=quarter;tablet.rebuild();reference.quarter=quarter;reference.rebuild()
  check(tablet.props==reference.props,"Cold Store geometry/registration unchanged")
  for i in tablet.props.size():
   check(await picture(tablet,tablet.props[i])==await picture(reference,reference.props[i]),"Native overhead fallback pixels identical q"+str(quarter)+" prop"+str(i))
 check(tablet.textures.is_empty(),"Overhead fallback does not load unrelated retired sheets")
 for id in ["fridge","rack"]:
  var prop={"id":id,"rect":Rect2(-80,-80,160,160),"registration":{}}
  check(await picture(tablet,prop)==await picture(reference,prop.duplicate(true)),"Explicit retired-sheet pixels identical: "+id)
  check(tablet.textures.has(id) and tablet.regions[id]==reference.regions[id],"Requested legacy sheet and bounds available: "+id)
  check(tablet.textures[id].get_image().get_data()==reference.textures[id].get_image().get_data(),"Legacy source pixels unchanged: "+id)
  if id=="fridge":check(tablet.textures.size()==1,"Only requested sheet uploaded")
 tablet.queue_free();reference.queue_free();preview.queue_free();await process_frame
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Original Cold Store art available")
 print("TABLET COLD STORE STORAGE failures=",failures);quit(1 if failures else 0)
