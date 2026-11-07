extends SceneTree
const Storage=preload("res://scripts/drone_cargo_storage.gd")
const Motion=preload("res://scripts/drone_animation.gd")
const Dock=preload("res://scripts/drone_dock.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 # Simulate Apple policy without disabling the shipped Windows LA8 path.
 var desktop_effect_policy:bool=Motion.native_effect_storage
 Motion.native_effect_storage=false
 root.set_meta("tablet_controls",true)
 if OS.get_cmdline_user_args().has("--atlas-bench"):
  var clip=Motion.catalog("mining").states["mine-south"]
  var paths=[clip.atlas.path,clip.effectAtlas.path]
  var ready:=false;var deadline=Time.get_ticks_msec()+30000
  while not ready and Time.get_ticks_msec()<deadline:
   ready=Dock.prepare_paths(paths,true)
   await process_frame
  check(ready,"Large sheet benchmark loads both layers")
  for path in paths:
   var texture=Motion.textures[path]
   if not OS.get_cmdline_user_args().has("--reference-tablet-storage"):check(texture is Storage,"Worker decodes compact tablet data")
   if texture is Storage:
    for i in range(20):texture.frame(i)
  for i in range(4):await process_frame
  print("ATLAS_BENCH cache_payload_bytes=",Motion.cached_bytes," ready=",ready)
  quit(1 if failures else 0);return
 var paths=Dock.record("construction").components.values()
 paths.append_array(Dock.record("mining").components.values())
 Dock.prepare_paths(paths,true)
 check(Motion.image_jobs.size()<=1,"iPad has at most one pending decoded drone layer")
 var deadline=Time.get_ticks_msec()+15000
 while not Dock.prepare_paths(paths,true) and Time.get_ticks_msec()<deadline:await process_frame
 check(paths.all(func(path):return Motion.textures.has(path)),"Serialized requests eventually prepare all requested layers")
 # A changed visible set must not strand a finished request and block the queue.
 var stale=Dock.record("salvage").components.values()[0]
 Motion.request_texture(stale)
 while Motion.image_jobs.has(stale) and not WorkerThreadPool.is_task_completed(Motion.image_jobs[stale].task):await process_frame
 var replacement=Dock.record("salvage").components.values()[1]
 deadline=Time.get_ticks_msec()+15000
 while not Dock.prepare_paths([replacement],true) and Time.get_ticks_msec()<deadline:await process_frame
 check(Motion.textures.has(replacement),"Changed visible paths drain completed requests without starving")
 var direct_paths=Dock.record("salvage").components.values()
 Motion.request_texture(direct_paths[2])
 Motion.texture(direct_paths[3])
 check(Motion.image_jobs.is_empty(),"Synchronous drawing consumes pending decode before starting another image")
 check(int(Motion.cache_diagnostics().budget_bytes)<=64*1024*1024,"iPad drone cache budget is at most 64 MiB")
 for i in range(6):
  for path in Motion.last_used:Motion.last_used[path]=-1000
  var image=Image.create(2048,2048,false,Image.FORMAT_RGBA8)
  image.fill(Color(0.2,0.4,0.5,1))
  Motion.cache_image("memory-fixture-%d"%i,image)
 check(Motion.cached_bytes<=64*1024*1024,"Stale decoded layer cache stays within iPad budget")
 # Exercise the actual large sheets that made parallel decoding dangerous.
 for i in range(4):await process_frame
 var clip=Motion.catalog("mining").states["mine-south"]
 var large_paths=[clip.atlas.path,clip.effectAtlas.path]
 var max_pending:=0
 deadline=Time.get_ticks_msec()+30000
 var ready:=false
 while not ready and Time.get_ticks_msec()<deadline:
  ready=Dock.prepare_paths(large_paths,true)
  max_pending=maxi(max_pending,Motion.image_jobs.size())
  await process_frame
 check(ready and max_pending<=1,"Two actual 138 MiB mining layers prepare with one pending decode")
 for path in large_paths:
  if not OS.get_cmdline_user_args().has("--reference-tablet-storage"):check(Motion.textures[path] is Storage,"Large asynchronous requests use compact tablet storage")
  check(Motion.textures.has(path) and Motion.textures[path].get_size()==Vector2(2688,13440),"Large atlas keeps original dimensions")
 print("TABLET LARGE ATLAS peak_pending=",max_pending," ready=",ready)
 Motion.finish_pending_jobs()
 root.remove_meta("tablet_controls")
 Motion.native_effect_storage=desktop_effect_policy
 check(int(Motion.cache_diagnostics().budget_bytes)==256*1024*1024,"Desktop cache budget is retained")
 print("TABLET DRONE MEMORY ","PASS" if failures==0 else "FAIL",": ",failures," failures")
 quit(1 if failures else 0)
