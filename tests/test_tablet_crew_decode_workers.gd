extends SceneTree
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var original:bool=Batch.prepared_cache_enabled;Batch.prepared_cache_enabled=false
 var batch=Batch.new();var wrappers:Array=[];var expected:Array=[]
 for i in range(16):
  var image:=Image.create(96,96,false,Image.FORMAT_RGBA8);image.fill(Color.TRANSPARENT)
  image.fill_rect(Rect2i(12,18,32,40),Color(float(i%4)/4.0,0.4,0.8,1))
  var path:="user://decode-worker-%d.png"%i;image.save_png(path);expected.append(image.get_data())
  var texture:=ImageTexture.new();texture.set_meta("crew_pivot",Vector2(20,70));texture.set_meta("crew_standing_height",148.0)
  var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=texture;wrappers.append(wrapper);batch.add(texture,wrapper,path)
 var stats:Dictionary=batch.finish()
 check(int(stats.get("private_worker_png_jobs",0))>0,"Uncached tablet PNG decoding uses CPU workers")
 check(int(stats.private_png_usec)==0,"Successful tablet worker decodes do not repeat on the main thread")
 check(int(stats.private_compress_peak_jobs)<=4 and int(stats.private_compress_jobs_left)==0,"CPU preparation stays within four jobs and drains")
 for i in wrappers.size():
  check(wrappers[i].get_image().get_data()==expected[i],"Worker output preserves exact pixels %d"%i)
  check(wrappers[i].get_meta("crew_alpha_extent")==Rect2((Vector2(12,18)-Vector2(20,70))*(65.28/148.0),Vector2(32,40)*(65.28/148.0)),"Worker bounds preserve wrapper geometry")
 check(wrappers[0].diffuse_texture==wrappers[4].diffuse_texture,"Different paths for identical encoded art share immutable sources")
 Batch.prepared_cache_enabled=original
 root.set_meta("tablet_controls",false)
 var desktop=Batch.new();var texture:=ImageTexture.new();texture.set_meta("crew_pivot",Vector2.ZERO);texture.set_meta("crew_standing_height",148.0)
 var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=texture;desktop.add(texture,wrapper,"user://decode-worker-0.png")
 var desktop_stats:Dictionary=desktop.finish()
 check(int(desktop_stats.get("private_worker_png_jobs",0))==0,"Desktop decoding policy remains unchanged")
 print("TABLET CREW DECODE WORKERS failures=",failures," stats=",stats)
 quit(1 if failures else 0)
