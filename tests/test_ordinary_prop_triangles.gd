extends SceneTree
const Original=preload("res://scripts/room_content_canvas.gd")
const Candidate=preload("res://scripts/room_content_canvas.gd")
const Library=preload("res://scripts/room_asset_library.gd")
class Context extends RefCounted:
 var painter:CanvasItem
 var operating:=false
 var machine_clock:=0.0
 var actor:=Vector2.ZERO
 var external_actor_texture:Texture2D
 func props_rebuilt_each_configure()->bool:return true
 func prop_visual_bounds(prop:Dictionary)->Rect2:return Library.bounds(prop)
func _init():call_deferred("run")
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
 root.size=Vector2i(400,400);root.mode=Window.MODE_WINDOWED;root.always_on_top=true
 var views:Array=[];var contents:Array=[];var contexts:Array=[]
 for i in range(2):
  var view:=SubViewport.new();view.size=Vector2i(400,400);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);views.append(view)
  var content=Original.new() if i==0 else Candidate.new();content.combine_ordinary_bases=i==1;content.cull_props=false;content.draw_origin=Vector2(180.375,270.125);view.add_child(content);contents.append(content);contexts.append(Context.new())
 var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",190.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
 var selected:Array=[];var sources:Dictionary={};var pairs:=0;var failures:=0
 for id in Library.entries():
  if not str(id).begins_with("library/sp-"):continue
  var prop:Dictionary=Library.template(id).duplicate(true)
  if prop.is_empty():continue
  var reg:Dictionary=prop.registration
  if reg.has("drone_dock") or reg.has("aquarium") or not reg.get("effects",[]).is_empty() or not reg.get("operating_screens",[]).is_empty():continue
  var source:String=Library.entries()[id].data.source
  if sources.has(source):continue
  sources[source]=true;selected.append(id)
  var scale_value:float=160.0/prop.rect.size.y;prop.rect.size*=scale_value;prop.rect.position=-prop.rect.size*.5;prop.layout_flip=Vector2.ONE
  for mirrored in [false,true]:
   var artwork:Dictionary=prop.duplicate(true)
   if mirrored:artwork.registration=Library.mirror_registration(reg)
   for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
    for wet in [false,true]:
     for i in range(2):
      contents[i].texture_filter=filter;contents[i].material=flood if wet else null;contexts[i].machine_clock=2.5;contents[i].submit(contexts[i],[{"kind":"prop","prop":artwork}])
     await process_frame;await process_frame;await RenderingServer.frame_post_draw
     pairs+=1
     var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
     if not a.get_used_rect().has_area() or a.get_data()!=b.get_data():
      failures+=1;print("MISMATCH ",id," ",mirrored," ",filter," ",wet)
     if pairs==1:a.save_png("user://original.png");b.save_png("user://candidate.png")
  if selected.size()>=12:break
 assert(contents[1].ordinary_draws>0)
 FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"failures":failures,"selected":selected,"draws":contents[1].ordinary_draws}))
 for view in views:view.queue_free()
 await process_frame
 print("ORDINARY_PROP ",pairs," exact comparisons ",failures," failures");quit(1 if failures else 0)
