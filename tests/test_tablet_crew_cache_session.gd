extends SceneTree
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func prepare(path:String)->Dictionary:
 var batch=Batch.new()
 var texture:=ImageTexture.new();texture.set_meta("crew_pivot",Vector2.ZERO);texture.set_meta("crew_standing_height",148.0)
 var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=texture
 batch.add(texture,wrapper,path)
 return {"stats":batch.finish(),"frame":wrapper,"cache":batch.prepared_cache}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var image:=Image.create(64,64,false,Image.FORMAT_RGBA8);image.fill(Color.AQUA)
 image.save_png("user://session.png")
 var cold:=prepare("user://session.png")
 var warm:=prepare("user://session.png")
 check(is_same(cold.cache,warm.cache),"Consecutive tablet batches reuse one metadata index instead of reopening every cache entry")
 check(int(warm.stats.private_disk_cache_hits)==1 and int(warm.stats.private_disk_cache_writes)==0,"Cache counters describe this batch only")
 var again:=prepare("user://session.png")
 check(int(again.stats.private_disk_cache_hits)==1,"Later batches do not accumulate earlier hit counts")
 var idle=Batch.new()
 var active:=prepare("user://session.png")
 var idle_stats:Dictionary=idle.finish()
 check(int(active.stats.private_disk_cache_hits)==1,"Active overlapping batch records its hit")
 check(int(idle_stats.private_disk_cache_hits)==0 and int(idle_stats.private_disk_cache_writes)==0 and int(idle_stats.private_disk_cache_rejected)==0,"Idle overlapping batch does not count another batch's cache operations")
 var path:String=cold.cache.directory.path_join(FileAccess.get_sha256("user://session.png")+".bin")
 DirAccess.remove_absolute(path)
 var repaired:=prepare("user://session.png")
 check(int(repaired.stats.private_disk_cache_hits)==0 and int(repaired.stats.private_disk_cache_writes)==1,"Purged cache entries are rebuilt safely")
 check(repaired.frame.get_image().get_data()==image.get_data(),"Rebuilt source preserves exact pixels")
 var final:=prepare("user://session.png")
 check(int(final.stats.private_disk_cache_hits)==1,"Repaired entry is reusable without a rescan")
 print("TABLET CREW CACHE SESSION failures=",failures)
 quit(1 if failures else 0)
