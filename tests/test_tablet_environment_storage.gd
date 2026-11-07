extends SceneTree
const CASES=[
 [preload("res://assets/environment/ocean-floor-expansion-v1/ocean_floor_view.gd"),"ocean"],
 [preload("res://assets/environment/alien-fungi-biomes-v1/fungi_biome_view.gd"),"fungi"],
 [preload("res://assets/environment/biome-floor-variants-v1/biome_floor_view.gd"),"ground"],
 [preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd"),"replacement"],
 [preload("res://assets/environment/rock-features-v1/rock_feature_view.gd"),"rock"]]
class Canvas extends Node2D:
 var provider
 var kind:String
 var identity:String
 func _draw():
  if kind=="ocean":provider.draw_asset(self,identity,Vector2(64,64),100.0)
  elif kind=="fungi":provider.draw_prop(self,identity,Vector2(64,64),100.0)
  elif kind=="ground":
   var habitats={"brine-ripples":"brine","coral-shell-sand":"coral","iron-clay":"iron"}
   var region={"biome":habitats[identity],"center":Vector2(1,0)}
   var texture:Texture2D=provider.texture_for(region,null)
   if texture!=null:draw_texture_rect(texture,Rect2(12,12,100,100),false)
  else:provider.draw_asset(self,identity,Vector2(64,64),100.0,Color.WHITE)
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func picture(provider,kind:String,identity:String)->PackedByteArray:
 var viewport:=SubViewport.new();viewport.size=Vector2i(128,128);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport)
 var canvas:=Canvas.new();canvas.provider=provider;canvas.kind=kind;canvas.identity=identity;viewport.add_child(canvas)
 await process_frame;await RenderingServer.frame_post_draw
 var image:=viewport.get_texture().get_image()
 check(image.get_used_rect().has_area(),"Visible original environment pixels: "+kind+"/"+identity)
 var pixels:=image.get_data();viewport.queue_free();await process_frame
 return pixels
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 for entry in CASES:
  var script=entry[0];var kind:String=entry[1]
  root.set_meta("tablet_controls",true)
  var tablet=script.new();tablet.prepare()
  check(tablet.textures.is_empty(),"Tablet preparation must not retain unrequested "+kind+" sheets")
  var identity:String=script.SOURCES.keys()[0]
  var pixels:PackedByteArray=await picture(tablet,kind,identity)
  check(tablet.textures.size()==1,"One actual draw retains only the requested "+kind+" sheet")
  var original_texture:Texture2D=tablet.textures.get(identity)
  await picture(tablet,kind,identity)
  check(is_same(tablet.textures.get(identity),original_texture),"Repeated draw reuses the same "+kind+" texture")
  root.set_meta("tablet_controls",false)
  var desktop=script.new();desktop.prepare()
  check(desktop.textures.size()==script.SOURCES.size(),"Desktop preparation remains eager: "+kind)
  check(await picture(desktop,kind,identity)==pixels,"First-use native pixels match eager source: "+kind)
  root.set_meta("tablet_controls",true)
  for key in script.SOURCES:
   var requested:PackedByteArray=await picture(tablet,kind,key)
   check(tablet.textures.has(key),"Every original sheet remains reachable: "+kind+"/"+key)
   var image:=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(script.SOURCES[key]))
   check(tablet.textures[key].get_image().get_data()==image.get_data(),"Full source pixels preserved: "+kind+"/"+key)
   root.set_meta("tablet_controls",false)
   check(await picture(desktop,kind,key)==requested,"All native draw pixels identical: "+kind+"/"+key)
   root.set_meta("tablet_controls",true)
 check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No missing source artwork")
 print("TABLET ENVIRONMENT STORAGE failures=",failures);quit(1 if failures else 0)
