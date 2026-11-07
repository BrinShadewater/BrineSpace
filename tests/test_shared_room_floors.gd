extends SceneTree
const Floors=preload("res://rooms/whole-room/modular_floor.gd")
const Common=preload("res://rooms/large-rooms/common.gd")
const PATHS=["res://assets/department-floors-v1/wet-drainage.png","res://assets/department-floors-v1/engineering-tread.png","res://assets/department-floors-v2/storage-load-deck.png"]
var failures:=0
class FloorCanvas extends Node2D:
 var path:String
 func _draw():
  Common.floor_tiles(self,path,Rect2(8,8,203,167),96.0,Color(.6,.7,.8,.43))
func _init():call_deferred("run")
func check(value:bool,message:String):
 if not value:failures+=1;print("FAIL ",message)
func settle():
 for i in 3:await process_frame
 await RenderingServer.frame_post_draw
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
 root.set_disable_input(true)
 for path in PATHS:
  for ordinary_first in [true,false]:
   Common.art_textures.erase(path);Floors.textures.erase(path)
   var ordinary:Texture2D
   if ordinary_first:ordinary=Floors.texture(path)
   var canvas=FloorCanvas.new();canvas.path=path;root.add_child(canvas);await settle()
   var large:Texture2D=Common.art_textures[path]
   if not ordinary_first:ordinary=Floors.texture(path)
   check(ordinary.get_rid()==large.get_rid(),"One shared floor upload, load order "+str(ordinary_first)+" "+path)
   var source=Image.new();check(source.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,"Original floor available")
   check(large.get_image().get_data()==source.get_data(),"Original ungraded floor bytes unchanged")
   canvas.queue_free();await settle()
 # Large-room callers still request the exact original raster. Ordinary floors
 # apply their accepted revision map; those two distinct sources must not alias.
 var old="res://assets/corridor-risers-v2/floor-sage.png"
 var revised=Floors.texture(old)
 var canvas=FloorCanvas.new();canvas.path=old;root.add_child(canvas);await settle()
 var raw:Texture2D=Common.art_textures[old];var source=Image.new();source.load_png_from_buffer(FileAccess.get_file_as_bytes(old))
 check(raw.get_rid()!=revised.get_rid(),"Distinct revised and original floor sources do not alias")
 check(raw.get_image().get_data()==source.get_data(),"Large-room original source policy preserved")
 canvas.queue_free();await settle()
 # The last scene owner releases both aliases. Keeping either alias alive
 # would allocate a second upload when gameplay starts again.
 var session=preload("res://scripts/session_art_cache.gd")
 for ordinary_first in [true,false]:
  var path=PATHS[0]
  var owner_a=Node.new();var owner_b=Node.new();root.add_child(owner_a);root.add_child(owner_b)
  session.retain(owner_a);session.retain(owner_b)
  var session_canvas=FloorCanvas.new();session_canvas.path=path;owner_b.add_child(session_canvas);await settle()
  owner_a.queue_free();await settle()
  check(Floors.textures.has(path) and Common.art_textures.has(path),"Live second owner preserves shared floor")
  owner_b.queue_free();await settle()
  check(not Floors.textures.has(path) and not Common.art_textures.has(path),"Last owner releases both floor aliases")
  var session_ordinary:Texture2D
  if ordinary_first:session_ordinary=Floors.texture(path)
  session_canvas=FloorCanvas.new();session_canvas.path=path;root.add_child(session_canvas);await settle()
  if not ordinary_first:session_ordinary=Floors.texture(path)
  check(session_ordinary.get_rid()==Common.art_textures[path].get_rid(),"Reentered session shares floor, order "+str(ordinary_first))
  session_canvas.queue_free();await settle()
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing art")
 print("SHARED ROOM FLOORS failures=",failures);quit(1 if failures else 0)
