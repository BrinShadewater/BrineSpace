extends SceneTree
const Sea=preload("res://assets/environment/seabed-v1/seabed_background.gd")
class Canvas extends Node2D:
 var sea
 var layout:Dictionary={}
 func _draw():sea.render_into(self,12.0,40,0.0,layout)
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func picture(sea,layout:Dictionary)->PackedByteArray:
 var view:=SubViewport.new();view.size=Vector2i(480,480);view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view)
 var canvas:=Canvas.new();canvas.sea=sea;canvas.layout=layout;view.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var image:=view.get_texture().get_image();check(image.get_used_rect().has_area(),"Pixel fixture contains visible seabed")
 var pixels:=image.get_data();view.queue_free();await process_frame
 return pixels
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 for seed in [101,1928894317]:
  var layout:Dictionary=preload("res://scripts/site_generator.gd").generate(seed);var original:=layout.duplicate(true)
  root.set_meta("tablet_controls",true)
  var tablet:=Sea.new();tablet.still_key(12.0,40,layout)
  check(tablet.textures.keys()==["silt-plain"],"Generated tablet sites do not load unused legacy scenery textures")
  var scenery:=tablet.scenery.duplicate(true)
  var pixels:PackedByteArray=await picture(tablet,layout)
  check(tablet.textures.keys()==["silt-plain"],"Generated rendering keeps unused legacy scenery unloaded")
  root.set_meta("tablet_controls",false)
  var desktop:=Sea.new();desktop.still_key(12.0,40,layout)
  check(desktop.textures.size()==6,"Desktop keeps existing eager seabed policy")
  check(await picture(desktop,layout)==pixels,"Generated tablet and desktop pixels match exactly")
  check(layout==original,"Texture preparation does not change generated site state")
  root.set_meta("tablet_controls",true)
  var legacy_pixels:PackedByteArray=await picture(tablet,{})
  check(tablet.textures.size()==6 and tablet.scenery==scenery,"Switching to legacy loads original scenery without duplicating geography")
  root.set_meta("tablet_controls",false)
  check(await picture(Sea.new(),{})==legacy_pixels,"Legacy scene pixels survive generated-to-legacy transition")
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"All original art remains available")
 print("TABLET SEABED STORAGE failures=",failures);quit(1 if failures else 0)
