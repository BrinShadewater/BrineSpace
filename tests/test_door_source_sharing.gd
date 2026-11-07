extends SceneTree
const Doors=preload("res://rooms/doors/painted_door.gd")
const Scope=preload("res://scripts/session_art_cache.gd")
var checks:=0
var failures:=0
class Surface extends Node2D:
 var skin
 var amount:=0.0
 func _draw():
  skin.raised_at(self,amount,128,24,110)
  skin.progress=amount
  skin.low_closed(self,Vector2(340,75),false,skin.family)
  skin.low_closed(self,Vector2(340,150),true,skin.family)
func frame():
 await process_frame
 await RenderingServer.frame_post_draw
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func clear():
 for skin in Doors.skins.values():skin.textures.clear()
func _init():call_deferred("run")
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 clear()
 var hallway=Doors.for_variant("hallway");var normal=Doors.for_variant("default")
 check(hallway!=normal,"Independent style objects")
 hallway.progress=.25;normal.progress=.75
 for kind in ["raised","low"]:check(hallway.texture(kind)==normal.texture(kind),"Shared identical source "+kind)
 check(hallway.progress==.25 and normal.progress==.75,"Independent animation progress")
 var first:=Node.new();var second:=Node.new();root.add_child(first);root.add_child(second);Scope.retain(first);Scope.retain(second)
 var ref:WeakRef=weakref(hallway.texture("raised"))
 first.queue_free();await frame();check(ref.get_ref()!=null,"Surviving owner retains upload")
 second.queue_free();await frame();check(ref.get_ref()==null,"Last owner releases all aliases")
 check(Doors.for_variant("hallway")==hallway and hallway.progress==.25,"Style state survives release")
 check(normal.texture("low")==hallway.texture("low"),"Reverse order shares after reentry")
 clear()
 var viewport:=SubViewport.new();viewport.size=Vector2i(512,240);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var surface:=Surface.new();viewport.add_child(surface)
 for family in Doors.catalog.styles.keys()+["hallway"]:
  var skin=Doors.for_variant(family);surface.skin=skin
  for kind in ["raised","low"]:
   var path:String=Doors.catalog.styles["default" if family=="hallway" else family][kind]
   var original:=Image.new();original.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
   check(skin.texture(kind).get_image().get_data()==original.get_data(),"Exact source pixels "+family+kind)
  for filter_value in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
   surface.texture_filter=filter_value
   for amount in [0.0,0.45,1.0]:
    surface.amount=amount;Doors.share_sources=false;clear();surface.queue_redraw();await frame()
    var reference:Image=viewport.get_texture().get_image()
    Doors.share_sources=true;clear();surface.queue_redraw();await frame()
    check(reference.get_data()==viewport.get_texture().get_image().get_data(),"Exact composed pixels "+family+str(amount))
 viewport.queue_free();await frame();clear()
 print("DOOR SOURCE SHARING ",checks," checks ",failures," failures");quit(1 if failures else 0)
