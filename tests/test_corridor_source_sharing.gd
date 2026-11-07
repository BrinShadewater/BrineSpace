extends SceneTree
const Walls=preload("res://rooms/underwater/corridor_wall_art.gd")
const Scope=preload("res://scripts/session_art_cache.gd")
var checks:=0
var failures:=0
class Surface extends Node2D:
 var identity:="straight-transit"
 func _draw():
  Walls.face(self,identity,Rect2(16,48,480,100),0.8)
  Walls.cap(self,identity,Rect2(16,24,480,24),0.8)
func frame():
 await process_frame
 await RenderingServer.frame_post_draw
func _init():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 Walls.textures.clear()
 var sources:Dictionary={}
 for id in Walls.catalog():
  var source:String=Walls.catalog()[id].source
  var texture:Texture2D=Walls.texture(id)
  if sources.has(source):check(texture==sources[source],"Variants share canonical upload: "+id)
  else:sources[source]=texture
 check(Walls.textures.size()==sources.size(),"One cache entry per canonical source")
 for source in sources:
  var original:=Image.new();original.load_png_from_buffer(FileAccess.get_file_as_bytes(source))
  check(sources[source].get_image().get_data()==original.get_data(),"Exact original source pixels: "+source)
 sources.clear()
 var first:=Node.new();var second:=Node.new();root.add_child(first);root.add_child(second);Scope.retain(first);Scope.retain(second)
 var ref:WeakRef=weakref(Walls.texture("straight-transit"))
 first.queue_free();await process_frame;await RenderingServer.frame_post_draw
 check(ref.get_ref()!=null and not Walls.textures.is_empty(),"Surviving owner retains shared upload")
 second.queue_free();await process_frame;await RenderingServer.frame_post_draw
 check(Walls.textures.is_empty() and ref.get_ref()==null,"Final owner releases source lookup without hidden alias")
 var a=Walls.texture("tee-transit");var b=Walls.texture("corner-transit")
 check(a==b,"Reverse load order shares after scene reentry")
 a=null;b=null;Walls.textures.clear()
 var viewport:=SubViewport.new();viewport.size=Vector2i(512,192);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var surface:=Surface.new();viewport.add_child(surface)
 for filter_value in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
  surface.texture_filter=filter_value
  for id in Walls.catalog():
   surface.identity=id;Walls.share_sources=false;Walls.textures.clear();surface.queue_redraw();await frame()
   var reference:Image=viewport.get_texture().get_image()
   Walls.share_sources=true;Walls.textures.clear();surface.queue_redraw();await frame()
   check(reference.get_data()==viewport.get_texture().get_image().get_data(),"Exact composed wall pixels: "+id)
 viewport.queue_free();await frame();Walls.textures.clear()
 print("CORRIDOR SOURCE SHARING ",checks," checks ",failures," failures");quit(1 if failures else 0)
