extends SceneTree
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func prepare(path:String)->Dictionary:
 var b=Batch.new();var tex:=ImageTexture.new();tex.set_meta("crew_pivot",Vector2(80,140));tex.set_meta("crew_standing_height",148.0)
 var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=tex;b.add(tex,wrapper,path)
 return {"stats":b.finish(),"frame":wrapper}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var prior:=DirAccess.open("user://crew-frame-cache-v1")
 if prior!=null:
  for name in prior.get_files():DirAccess.remove_absolute("user://crew-frame-cache-v1/"+name)
 root.set_meta("tablet_controls",true)
 var image:=Image.create(160,160,false,Image.FORMAT_RGBA8);image.fill(Color.TRANSPARENT);image.fill_rect(Rect2i(20,30,80,100),Color(0.2,0.4,0.7,1));image.save_png("user://cached.png")
 var cold:=prepare("user://cached.png");var warm:=prepare("user://cached.png")
 check(int(warm.stats.get("private_disk_cache_hits",0))==1,"Warm tablet load must reuse prepared immutable source")
 check(int(warm.stats.get("private_compress_jobs",-1))==0 and int(warm.stats.get("private_peak_pending_image_bytes",-1))==0,"Warm cache must avoid PNG/compression jobs and retained decoded images")
 check(warm.frame.get_image().get_data()==image.get_data(),"Warm cache preserves every original pixel")
 check(warm.frame.get_meta("crew_alpha_extent")==cold.frame.get_meta("crew_alpha_extent"),"Warm cache preserves alpha bounds and wrapper geometry")
 image.set_pixel(30,40,Color.RED);image.save_png("user://cached.png");var changed:=prepare("user://cached.png")
 check(int(changed.stats.get("private_disk_cache_hits",0))==0 and changed.frame.get_image().get_data()==image.get_data(),"Changed PNG content invalidates old prepared data")
 # Corrupt every cache entry; fallback must reconstruct the source without accepting bad data.
 var dir:=DirAccess.open("user://crew-frame-cache-v1")
 if dir!=null:
  for name in dir.get_files():
   var f:=FileAccess.open("user://crew-frame-cache-v1/"+name,FileAccess.WRITE);f.store_string("broken");f.close()
 var repaired:=prepare("user://cached.png")
 check(int(repaired.stats.get("private_disk_cache_hits",0))==0 and repaired.frame.get_image().get_data()==image.get_data(),"Corrupt cache falls back safely")
 var prefetch=preload("res://scripts/image_prefetch.gd")
 prefetch.begin("user://fixture-startup.txt");prefetch.last_pump=0
 var pumped_before:int=prefetch.pumps
 var rebuilt:=prepare("user://cached.png")
 check(prefetch.pumps>pumped_before,"Warm prepared path keeps the native loading window responsive")
 prefetch.end()
 check(int(rebuilt.stats.get("private_disk_cache_hits",0))==1,"Fallback repairs a corrupt entry")
 var cache=preload("res://scripts/crew_storage/prepared_cache.gd").new()
 var digest:=FileAccess.get_sha256("user://cached.png");var cached:Dictionary=cache.load_prepared(digest)
 check(not cached.is_empty(),"Valid prepared entry can be reopened independently")
 cached.raw_bytes=4
 check(not cache._valid(cached,digest),"Layout-inconsistent cached bytes are rejected before Image creation")
 # Budget eviction must remove only disposable cache files; progress is independent.
 var progress:=FileAccess.open("user://progress-sentinel",FileAccess.WRITE);progress.store_string("keep");progress.close()
 cache.entries={"fixture.bin":cache.MAX_BYTES};cache.bytes=cache.MAX_BYTES;cache._trim(1)
 check(cache.entries.is_empty() and cache.bytes==0 and FileAccess.get_file_as_string("user://progress-sentinel")=="keep","Cache budget eviction preserves saved progress")
 root.set_meta("tablet_controls",false);var desktop:=prepare("user://cached.png")
 check(int(desktop.stats.get("private_disk_cache_hits",0))==0 and int(desktop.stats.private_compress_jobs)==1,"Desktop keeps existing preparation policy")
 print("TABLET CREW CACHE failures=",failures," cold=",cold.stats," warm=",warm.stats)
 quit(1 if failures else 0)
