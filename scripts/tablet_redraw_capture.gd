extends RefCounted
## Five render-signal intervals after the loading cover leaves. Not GPU timings.
const FRAME_LIMIT:=5
static func capture(tree:SceneTree,owner:WeakRef,initial:Dictionary)->void:
 var data:Dictionary=initial.duplicate(true)
 var rows:Array=[]
 var previous_post:=Time.get_ticks_usec()
 for index in range(FRAME_LIMIT):
  await tree.process_frame
  var process_started:=Time.get_ticks_usec()
  var scene:Node=owner.get_ref()
  if scene==null or tree.current_scene!=scene:return
  await RenderingServer.frame_post_draw
  var now:=Time.get_ticks_usec()
  if not is_instance_valid(scene) or tree.current_scene!=scene:return
  var row:={"frame":index,"frame_ms":(now-previous_post)/1000.0,"process_to_post_draw_ms":(now-process_started)/1000.0,"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),"texture_mib":Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)/1048576.0}
  var grid=scene.get("grid_view")
  if is_instance_valid(grid):
   row["grid_draw_usec"]=grid.draw_usec_since_read
   row["grid_redraws"]=grid.draws_since_read
  rows.append(row);previous_post=now
 var scene:Node=owner.get_ref()
 if scene==null or tree.current_scene!=scene:return
 data.timings["initial_redraw"]={"frames":rows,"scope":"Five frame_post_draw intervals after cover retirement; signal/CPU boundaries, not GPU execution. Excludes player reading time and earlier station setup."}
 var path:String=scene.get_meta("tablet_startup_profile_path","user://ipad_startup_profile.json")
 var file:=FileAccess.open(path,FileAccess.WRITE)
 if file!=null:file.store_string(JSON.stringify(data,"  "))
 scene.set_meta("tablet_initial_redraw_profile",data.timings.initial_redraw)
