extends SceneTree
const Router=preload("res://scripts/crew_storage/router.gd")
var checks:=0
var failures:=0
class Pose extends Node2D:
 var texture:Texture2D
 var mode:=0
 func _draw():
  if mode==0:texture.draw(get_canvas_item(),Vector2.ZERO)
  elif mode==1:texture.draw_rect(get_canvas_item(),Rect2(0,0,220,290),false,Color(.6,.8,1,.7),false)
  elif mode==2:texture.draw_rect_region(get_canvas_item(),Rect2(10,20,220,260),Rect2(40,45,180,190),Color(.6,.8,1,.7),false,true)
  else:texture.draw_rect(get_canvas_item(),Rect2(0,0,220,290),false,Color(.6,.8,1,.7),true)
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _initialize():call_deferred("run")
func capture(pose:Pose,viewport:SubViewport)->PackedByteArray:
 pose.queue_redraw();await pose.draw;await RenderingServer.frame_post_draw
 return viewport.get_texture().get_image().get_data()
func run():
 check(OS.get_environment("BRINESPACE_TEST_USER_DIR")==OS.get_user_data_dir(),"Scratch profile required")
 check(DisplayServer.get_name()!="headless","Native renderer required")
 if failures:quit(1);return
 var player=load("res://scripts/crew_storage/player.gd").new()
 player.begin_texture_batch();player.load_manifest("res://character/bill-run-south-coherent-v1/manifest.json");player.finish_texture_batch()
 var alias_row:Array=[]
 for frame in player.frames["run-south"]:
  var alias:CanvasTexture=frame.duplicate();alias.set_meta("crew_pivot",Vector2(1,2));alias_row.append(alias)
 player.frames["fixture-alias"]=alias_row
 var bank=load("res://scripts/crew_storage/bank.gd").new();bank.cpu_store_enabled=false;bank.adopt(player)
 var session:=Node.new();root.add_child(session)
 var viewport:=SubViewport.new();viewport.size=Vector2i(460,460);viewport.transparent_bg=true;viewport.world_2d=World2D.new();viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;session.add_child(viewport)
 var pose:=Pose.new();viewport.add_child(pose)
 Router.start(self,session,bank)
 var presenter=Router.active.presenter
 var row:Array=player.frames["run-south"]
 presenter.share_sources=false
 var expected:Array=[]
 for zoom in [.5,1.0,1.5,.137,.29672727,.73]:
  pose.scale=Vector2.ONE*zoom;pose.position=Vector2(8.25,8.75)
  for frame in row:
   pose.texture=frame;expected.append(await capture(pose,viewport))
 presenter.clear_leases(pose.get_instance_id())
 for index in presenter.slots.size():presenter.drop_slot(index)
 # Freeze the original in-memory oracle before reading cold records on demand.
 var backing_store:RefCounted
 if OS.get_cmdline_user_args().has("--bounded-crew-cpu-store"):
  backing_store=load("res://scripts/crew_storage/cpu_store.gd").new();backing_store.cache_limit=1
  check(backing_store.open("user://crew-pixel-store.bin"),"Open pixel comparison store")
  var seen:Dictionary={}
  for frame in row:
   var source:Texture2D=frame.diffuse_texture
   if seen.has(source.get_instance_id()):continue
   seen[source.get_instance_id()]=true
   check(source.offload(backing_store,str(source.get_meta("private_source_png"))),"Real animation source becomes disk-backed")
 # Capture the reference first, then compare the same presenter with shared sources.
 presenter.share_sources=true
 var uploads_before:int=presenter.uploads
 var cursor:=0
 for zoom in [.5,1.0,1.5,.137,.29672727,.73]:
  pose.scale=Vector2.ONE*zoom
  for frame in row:
   pose.texture=frame
   check(await capture(pose,viewport)==expected[cursor],"Routed full frames preserve fractional scaled pixels")
   cursor+=1
 check(presenter.uploads-uploads_before==6,"Six unique pixel sources each upload once")
 var unique_bytes:int=presenter.cache_bytes
 for i in alias_row.size():
  pose.texture=alias_row[i];pose.scale=Vector2.ONE*.5
  check(await capture(pose,viewport)==expected[i],"Independent metadata wrappers preserve source pixels")
 check(presenter.uploads-uploads_before==6 and presenter.cache_bytes==6*256*256*4,"Twelve wrappers retain six unique full-frame uploads")
 for mode in [1,2,3]:
  pose.mode=mode
  for frame in row:
   pose.texture=frame
   presenter.share_sources=false
   var reference:PackedByteArray=await capture(pose,viewport)
   presenter.share_sources=true
   check(await capture(pose,viewport)==reference,"Rect/region/tinted shared image pixels match mode %d frame %d"%[mode,row.find(frame)])
 pose.mode=0
 # A retained visible peer must keep its immutable shared image while another owner redraws.
 var peer:=Pose.new();peer.texture=row[2];peer.position=Vector2(220,0);viewport.add_child(peer)
 await capture(peer,viewport)
 var peer_id:int=peer.get_instance_id()
 var held:Array=presenter.owner_slots[peer_id].duplicate()
 var material:=ShaderMaterial.new();material.shader=Shader.new()
 material.shader.code="shader_type canvas_item; void fragment(){COLOR=texture(TEXTURE,UV)*vec4(UV.x,UV.y,1.0,1.0);}"
 pose.material=material
 presenter.share_sources=false
 var shaded_reference:PackedByteArray=await capture(pose,viewport)
 presenter.share_sources=true
 check(await capture(pose,viewport)==shaded_reference,"UV-dependent material retains full-frame sampling")
 pose.material=null
 var id:int=pose.get_instance_id()
 pose.hide()
 check(presenter.owner_slots[id].is_empty(),"Hidden canvas releases compact shared image lease")
 for index in presenter.slots.size():
  if presenter.slots[index].holders.is_empty():presenter.drop_slot(index)
 for index in held:check(not presenter.slots[index].holders.is_empty(),"Visible peer pins its compact shared image")
 peer.hide()
 for index in presenter.slots.size():
  if presenter.slots[index].holders.is_empty():presenter.drop_slot(index)
 check(presenter.cache_bytes==0,"Unleased compact shared image can be completely evicted")
 pose.show();pose.texture=row[0];pose.scale=Vector2.ONE*.5
 check(await capture(pose,viewport)==expected[0],"Evicted shared image rebuild preserves reveal pixels")
 # Exhausting the shared image budget must spill a full logical frame, never the atlas image.
 presenter.clear_leases(id)
 for index in presenter.slots.size():
  if presenter.slots[index].holders.is_empty():presenter.drop_slot(index)
 presenter.cache_byte_limit=1
 pose.texture=row[1]
 check(await capture(pose,viewport)==expected[1],"Over-budget shared image fallback preserves requested frame pixels")
 check(presenter.spill_allocations>0 and presenter.cache_bytes==0,"Shared image cannot exceed its immutable slot budget")
 session.free()
 check(presenter.slots.is_empty() and presenter.cache_bytes==0,"Final scene releases shared image storage")
 FileAccess.open("user://source-sharing-pixels.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"unique_bytes":unique_bytes,"original_bytes":6*256*256*4,"diagnostics":presenter.diagnostics_snapshot(),"pid":OS.get_process_id(),"tree_paused":paused},"  "))
 print("CREW SOURCE SHARING PIXELS: %d checks, %d failures"%[checks,failures])
 quit(1 if failures else 0)
