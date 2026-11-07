extends SceneTree
const View=preload("res://assets/environment/wrecked-rooms-v1/wreck_view.gd")
const Field=preload("res://scripts/wreck_field.gd")
class Canvas extends Node2D:
 var provider
 var progress:=0.0
 var kind:="engineering"
 func _draw():
  var wrecks={Vector2i.ZERO:{"kind":kind,"progress":progress*18.0,"active":false,"cleared":false}}
  provider.draw_into(self,wrecks,128.0,0.0,Vector2i(-1,-1),false)
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func picture(provider,kind:String,progress:float)->PackedByteArray:
 var vp:=SubViewport.new();vp.size=Vector2i(128,128);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp)
 var canvas:=Canvas.new();canvas.provider=provider;canvas.kind=kind;canvas.progress=progress;vp.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var pixels:=vp.get_texture().get_image().get_data()
 vp.queue_free();await process_frame
 return pixels
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 for kind in Field.TYPES:
  root.set_meta("tablet_controls",false)
  var reference=View.new()
  var expected:PackedByteArray=await picture(reference,kind,0.0)
  check(reference.textures.has(kind+"-stripped"),"Desktop retains original stage loading")
  root.set_meta("tablet_controls",true)
  var tablet=View.new()
  check(await picture(tablet,kind,0.0)==expected,"Initial native pixels match: "+kind)
  check(not tablet.textures.has(kind+"-stripped"),"Invisible tablet stripped layer must not upload: "+kind)
  for stage in [0.25,0.38,0.39,0.44,0.50,0.84,0.9,0.98,1.0]:
   root.set_meta("tablet_controls",false)
   expected=await picture(reference,kind,stage)
   root.set_meta("tablet_controls",true)
   check(await picture(tablet,kind,stage)==expected,"Salvage native pixels match: "+kind+"/"+str(stage))
   if stage>0.38:check(tablet.textures.has(kind+"-stripped"),"First visible stage remains reachable: "+kind)
  var original=tablet.textures.get(kind+"-stripped")
  await picture(tablet,kind,0.44)
  check(is_same(original,tablet.textures.get(kind+"-stripped")),"Repeated visible stage reuses texture")
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"Original artwork all present")
 print("TABLET WRECK STORAGE failures=",failures)
 quit(1 if failures else 0)
