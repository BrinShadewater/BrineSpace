extends SceneTree
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func prepare()->Dictionary:
 var b=Batch.new();var wrappers:Array=[]
 for i in 9:
  var t:=ImageTexture.new();t.set_meta("crew_pivot",Vector2.ZERO);t.set_meta("crew_standing_height",148.0)
  var w:=CanvasTexture.new();w.diffuse_texture=t;wrappers.append(w)
  b.add(t,w,"user://frame%d.png"%i)
 return {"stats":b.finish(),"frames":wrappers}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 for i in 9:
  var image:=Image.create(64,64,false,Image.FORMAT_RGBA8);image.fill(Color(float(i)/9,0.3,0.6,1));image.save_png("user://frame%d.png"%i)
 var cold:=prepare();var warm:=prepare()
 check(int(warm.stats.get("private_cache_read_jobs",0))==9,"Warm cache validation must run in independent CPU worker jobs")
 check(int(warm.stats.private_compress_peak_jobs)<=4,"Prepared cache workers obey the tablet window")
 check(int(warm.stats.private_disk_cache_hits)==9 and int(warm.stats.private_compress_jobs)==0,"Warm workers avoid PNG decode/compression")
 check(int(warm.stats.private_peak_pending_image_bytes)==0 and int(warm.stats.private_compress_jobs_left)==0,"Warm queue retains no decoded images or unfinished jobs")
 for i in 9:check(cold.frames[i].get_image().get_data()==warm.frames[i].get_image().get_data(),"Worker cache pixels remain exact")
 # Reject a corrupt cached digest shared by different PNG paths, then rebuild once.
 var key:=FileAccess.get_sha256("user://frame0.png")
 var cache=preload("res://scripts/crew_storage/prepared_cache.gd").shared()
 var file:=FileAccess.open(cache.directory.path_join(key+".bin"),FileAccess.WRITE);file.store_string("broken");file.close()
 DirAccess.copy_absolute("user://frame0.png","user://alias.png")
 var aliases=Batch.new();var held:Array=[]
 for path in ["user://frame0.png","user://alias.png"]:
  var t:=ImageTexture.new();t.set_meta("crew_pivot",Vector2.ZERO);t.set_meta("crew_standing_height",148.0)
  var w:=CanvasTexture.new();w.diffuse_texture=t;held.append(w);aliases.add(t,w,path)
 aliases.prepare_path("user://frame0.png");aliases.prepare_path("user://alias.png")
 var alias_stats:Dictionary=aliases.finish()
 check(int(alias_stats.private_disk_cache_rejected)==1 and int(alias_stats.private_compress_jobs)==1,"Corrupt aliases rebuild one shared source")
 check(held[0].diffuse_texture==held[1].diffuse_texture and held[0].get_image().get_data()==cold.frames[0].get_image().get_data(),"Alias fallback preserves shared source and pixels")
 # Purging one file leaves stale session metadata: worker miss must repair it.
 DirAccess.remove_absolute(cache.directory.path_join(key+".bin"))
 var purged:=prepare()
 check(int(purged.stats.private_disk_cache_hits)==8 and int(purged.stats.private_disk_cache_writes)==1,"OS-purged entry falls back and repairs without a rescan")
 var unused=Batch.new();unused.prepare_path("user://frame0.png")
 var unused_stats:Dictionary=unused.finish()
 check(int(unused_stats.private_compress_unused_jobs)==1 and int(unused_stats.private_compress_jobs_left)==0,"Discarded cache task is joined and released")
 var dir:=DirAccess.open("user://crew-frame-cache-v1")
 for name in dir.get_files():
  var f:=FileAccess.open("user://crew-frame-cache-v1/"+name,FileAccess.WRITE);f.store_string("broken");f.close()
 var repaired:=prepare()
 check(int(repaired.stats.private_disk_cache_rejected)==9 and int(repaired.stats.private_disk_cache_writes)==9,"Corrupt worker reads rebuild each cache on main-owned PNG path")
 for i in 9:check(cold.frames[i].get_image().get_data()==repaired.frames[i].get_image().get_data(),"Corruption fallback preserves pixels")
 var again:=prepare()
 check(int(again.stats.private_disk_cache_hits)==9,"Repaired entries remain reusable")
 print("TABLET CREW CACHE WORKERS failures=",failures," warm=",warm.stats)
 quit(1 if failures else 0)
