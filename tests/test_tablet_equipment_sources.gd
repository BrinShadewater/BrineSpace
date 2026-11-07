extends SceneTree
const VIEWS=[preload("res://rooms/production-ten/storage_bay_view.gd"),preload("res://rooms/production-ten/mining_drone_bay_view.gd"),preload("res://rooms/underwater/thermal-control/solar_array_view.gd")]
var failures:=0
class PropCanvas extends Node2D:
 var renderer
 var prop:Dictionary
 func _draw():
  renderer.painter=self;renderer.draw_registered_prop(prop);renderer.painter=renderer
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func view(script,tablet:bool,preview:=false):
 root.set_meta("tablet_controls",tablet)
 var item=script.new();item.hide()
 if preview:item.set_meta("layout_editor_preview",true)
 root.add_child(item);item.set_process(false);item.machine_clock=.5;return item
func picture(item,prop:Dictionary)->PackedByteArray:
 var vp:=SubViewport.new();vp.size=Vector2i(384,384);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas:=PropCanvas.new();canvas.position=Vector2(192,192);canvas.renderer=item;canvas.prop=prop;vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 canvas.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 var image=vp.get_texture().get_image();check(image.get_used_rect().has_area(),"Fallback still draws visible pixels")
 var pixels=image.get_data();vp.queue_free();await process_frame;return pixels
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 for script in VIEWS:
  var tablet=view(script,true)
  check(tablet._life_texture==null,"Tablet must defer retired equipment sheet: "+script.resource_path)
  var reference=view(script,false);check(reference._life_texture!=null,"Desktop preserves eager equipment")
  var preview=view(script,true,true);check(preview._life_texture!=null,"Editor preview preserves eager equipment")
  for quarter in 4:
   tablet.quarter=quarter;tablet.rebuild();reference.quarter=quarter;reference.rebuild()
   check(tablet.props==reference.props,"Equipment geometry/registration unchanged")
   for i in tablet.props.size():
    check(await picture(tablet,tablet.props[i])==await picture(reference,reference.props[i]),"Fallback native pixels exact q"+str(quarter)+" "+str(tablet.props[i].id))
  var expected=reference.life_texture.get_image()
  var actual=tablet.life_texture.get_image()
  check(actual.get_data()==expected.get_data() and actual.get_size()==expected.get_size(),"Demanded source pixels/bounds exact")
  check(tablet.life_texture==tablet.life_texture,"Repeated requests reuse the upload")
  tablet.queue_free();reference.queue_free();preview.queue_free();await process_frame
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Original equipment sources available")
 print("TABLET EQUIPMENT SOURCES failures=",failures);quit(1 if failures else 0)
