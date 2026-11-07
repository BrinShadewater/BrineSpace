extends SceneTree
const View=preload("res://rooms/underwater/batch-two/cryo_chamber_view.gd")
var failures:=0
class PodCanvas extends Node2D:
 var view
 var prop:Dictionary
 func _draw():
  view.painter=self;view.draw_registered_prop(prop);view.painter=view
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func make_view(preview:=false):
 var v=View.new();v.embedded=true;v.hide()
 if preview:v.set_meta("layout_editor_preview",true)
 root.add_child(v);v.set_process(false);return v
func picture(view,prop:Dictionary)->PackedByteArray:
 var viewport=SubViewport.new();viewport.size=Vector2i(384,384);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var canvas=PodCanvas.new();canvas.position=Vector2(192,192);canvas.view=view;canvas.prop=prop;viewport.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var image=viewport.get_texture().get_image();check(image.get_used_rect().has_area(),"Fallback pixels visible")
 var data=image.get_data();viewport.queue_free();await process_frame;return data
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.set_meta("tablet_controls",false);var reference=make_view()
 check(reference.wake_frames.size()==6 and reference.wake_frames.all(func(t):return t!=null),"Desktop keeps six wake frames eager")
 root.set_meta("tablet_controls",true);var tablet=make_view()
 check(tablet.wake_frames.all(func(t):return t==null),"Tablet constructor must not decode unused generic-pod wake frames")
 check(tablet.get("_life_texture")==null,"Tablet constructor must defer original cryo equipment sheet")
 var item=reference.life_items[0];var prop={"id":item.id,"rect":item.rect,"registration":item}
 for index in 6:
  var pod={"id":"generic_fixture","name":"Fixture","wake":float(index)*7.0/6.0+0.01,"recovered":false}
  reference.recovery={"pods":[pod],"cleared":true};tablet.recovery=reference.recovery.duplicate(true)
  check(await picture(tablet,prop)==await picture(reference,prop),"Generic wake pixels exact "+str(index))
  check(tablet.wake_frames[index]!=null,"Displayed frame cached "+str(index))
  check(tablet.wake_frames.filter(func(t):return t!=null).size()==index+1,"Only displayed frames loaded "+str(index))
 check(tablet.life_texture.get_image().get_data()==reference.life_texture.get_image().get_data(),"Original equipment fallback pixels exact")
 var first=tablet.life_texture;check(tablet.life_texture==first,"Equipment source uploaded once")
 var preview=make_view(true);check(preview.wake_frames.all(func(t):return t!=null) and preview.get("_life_texture")!=null,"Tablet layout preview remains eager")
 preview.free();tablet.free();reference.free()
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing cryo art")
 print("TABLET CRYO FALLBACK failures=",failures);quit(1 if failures else 0)
