extends SceneTree
const Motion=preload("res://scripts/drone_animation.gd")
const Storage=preload("res://scripts/drone_cargo_storage.gd")
var failures:=0
class Painter extends Node2D:
 var texture:Texture2D
 var record:Dictionary
 var cell:Vector2
 var index:=0
 var reference:=false
 var scale_value:=1.0
 var shift:=Vector2.ZERO
 func _draw():
  if reference:draw_texture_rect_region(texture,Rect2(Vector2(12,14),cell*scale_value),Rect2(Vector2(index%int(record.columns),index/int(record.columns))*cell+shift,cell))
  else:Motion.begin(self);Motion.atlas(self,record,index,Rect2(Vector2(12,14),cell*scale_value),cell,Color.WHITE)
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 check(DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("user://tablet-evidence")) == OK, "Isolated tablet evidence directory exists")
 # Simulate Apple policy without disabling the shipped Windows LA8 path.
 var desktop_effect_policy:bool=Motion.native_effect_storage
 Motion.native_effect_storage=false
 root.set_meta("tablet_controls",true)
 var mode="hull"
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--compact-case="):mode=arg.trim_prefix("--compact-case=")
 var manifest=Motion.catalog("construction" if mode=="construction" else "mining")
 var clip=manifest.states["job-weld-south" if mode=="construction" else "mine-south"]
 var record:Dictionary=clip.effectAtlas if mode=="effect" else clip.atlas
 var path:String=record.path
 var source_spec=Motion.compact_storage_spec(path)
 var full_size=Vector2i(source_spec.width,source_spec.height)
 var full_bytes:int=full_size.x*full_size.y*4
 var cell=Vector2(manifest.frameWidth,manifest.frameHeight)
 var compact:Texture2D=Motion.texture(path)
 check(compact is Storage,"iPad uses compact storage for large hull sheets")
 print("COMPACT_BYTES ",Motion.texture_bytes[path]," ORIGINAL_BYTES ",full_bytes)
 check(Motion.texture_bytes[path]<full_bytes*.66,"iPad keeps less than two thirds the original decoded sheet bytes")
 if compact is Storage:
  check(compact.cropped==null,"iPad releases decoded compact atlas after worker packing")
  check(compact.base_bytes<int(source_spec.box[2])*int(source_spec.box[3])*int(source_spec.columns)*(int(source_spec.height)/int(source_spec.cell[1]))*4*.8,"Lossless packing reduces retained compact atlas bytes by at least 20 percent")
  var decoded:=Image.new()
  check(decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(source_spec.path))==OK,"Compact reference decodes")
  var crop_size:=Vector2i(source_spec.box[2],source_spec.box[3])
  for i in range(int(record.frameCount) if record.has("frameCount") else int(clip.frameCount)):
   var at:=Vector2i(i%int(source_spec.columns),i/int(source_spec.columns))*crop_size
   var expected:Image=decoded.get_region(Rect2i(at,crop_size))
   var actual:Texture2D=compact.frame(i)
   check(actual!=null and actual.get_image().get_data()==expected.get_data(),"Lossless frame pixels match compact source %d"%i)
  decoded=null
  for i in range(20):compact.frame(i)
  check(compact.frames.size()<=6,"iPad frame texture cache stays bounded to six frames")
 if DisplayServer.get_name()!="headless" and compact is Storage:
  var image=Image.new();image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
  var original=ImageTexture.create_from_image(image);image=null
  var painters=[];var captures=[]
  for lane in range(2):
   var view=SubViewport.new();view.size=Vector2i(cell)+Vector2i(32,32);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(view);captures.append(view)
   var p=Painter.new();p.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;p.texture_repeat=CanvasItem.TEXTURE_REPEAT_DISABLED;p.texture=original;p.cell=cell;p.record=record;p.reference=lane==0;view.add_child(p);painters.append(p)
  var lease_tested:=false
  for frame in [0,int(clip.frameCount)/2,int(clip.frameCount)-1]:
   for p in painters:p.index=frame;p.queue_redraw()
   for i in range(3):await process_frame
   await RenderingServer.frame_post_draw
   check(captures[0].get_texture().get_image().get_data()==captures[1].get_texture().get_image().get_data(),"Compact hull renders exact visible pixels frame%d"%frame)
   # Empty effect cells deliberately issue no draw command or frame lease.
   if not lease_tested and compact.frames.has(int(frame)):
    lease_tested=true
    var held=weakref(compact.frames[int(frame)])
    var before=captures[1].get_texture().get_image().get_data()
    for offset in range(1,13):compact.frame((int(frame)+offset)%int(clip.frameCount))
    check(not compact.frames.has(int(frame)),"Another consumer evicts old frame from LRU")
    check(held.get_ref()!=null,"Retained canvas leases survive frame cache eviction")
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    check(before==captures[1].get_texture().get_image().get_data(),"Retained pixels stay visible after frame cache eviction")
    painters[1].index=(int(frame)+1)%int(clip.frameCount);painters[1].queue_redraw()
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    check(held.get_ref()==null,"Redrawing canvas releases retired frame lease")

  check(lease_tested,"A visible sampled frame exercises retained canvas leases")
  var flood=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader")
  for p in painters:p.material=flood;p.index=int(clip.frameCount)/2;p.queue_redraw()
  for i in range(3):await process_frame
  await RenderingServer.frame_post_draw
  check(captures[0].get_texture().get_image().get_data()==captures[1].get_texture().get_image().get_data(),"Flood material preserves unscaled visible pixels")
  for p in painters:p.material=null;p.queue_redraw()
  for scale_value in [0.1,0.3,0.5,0.73]:
   for p in painters:p.index=int(clip.frameCount)/2;p.scale_value=scale_value;p.queue_redraw()
   for i in range(3):await process_frame
   await RenderingServer.frame_post_draw
   var drawn=captures[1].get_texture().get_image()
   var references:Array=[]
   for shift in [Vector2.ZERO,Vector2(-.5,-.5),Vector2(0,-.5),Vector2(.5,-.5),Vector2(-.5,0),Vector2(.5,0),Vector2(-.5,.5),Vector2(0,.5),Vector2(.5,.5)]:
    painters[0].shift=shift;painters[0].queue_redraw()
    for i in range(2):await process_frame
    await RenderingServer.frame_post_draw
    references.append(captures[0].get_texture().get_image().get_data())
   var data=drawn.get_data();var changed:=0;var unexplained:=0
   for k in range(0,data.size(),4):
    if data.slice(k,k+4)==references[0].slice(k,k+4):continue
    changed+=1
    if not references.any(func(other):return data.slice(k,k+4)==other.slice(k,k+4)):unexplained+=1
   print("SCALED_COMPACT scale=",scale_value," changed=",changed," unexplained=",unexplained)
   check(unexplained==0,"Fractional zoom samples only original neighboring pixels")
   if scale_value==0.5:
    drawn.save_png("user://tablet-evidence/half-"+mode+".png")
    Image.create_from_data(drawn.get_width(),drawn.get_height(),false,Image.FORMAT_RGBA8,references[0]).save_png("user://tablet-evidence/half-reference-"+mode+".png")
   if scale_value==0.3:drawn.save_png("user://tablet-evidence/scaled-"+mode+".png")
   painters[0].shift=Vector2.ZERO
  for view in captures:view.queue_free()
 # Edited or unavailable derived data must retain the original artwork fallback.
 var spec=Motion.compact_storage_spec(path).duplicate(true)
 spec.sha256="invalid-fixture-hash"
 var rejected:Image=Motion.load_cargo_storage(path,spec,FileAccess.get_file_as_bytes(path))
 check(rejected==null,"Invalid compact hash rejects derived data for original fallback")
 root.remove_meta("tablet_controls")
 Motion.native_effect_storage=desktop_effect_policy
 check(Motion.compact_storage_spec(path).is_empty(),"Desktop does not select tablet hull storage")
 print("TABLET COMPACT STORAGE ","PASS" if failures==0 else "FAIL",": ",failures," failures")
 quit(1 if failures else 0)
