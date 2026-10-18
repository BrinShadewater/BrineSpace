extends SceneTree
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 var image:=Image.create(256,256,false,Image.FORMAT_RGBA8)
 image.fill(Color.TRANSPARENT);image.fill_rect(Rect2i(40,30,120,160),Color(0.3,0.6,0.8,1))
 var png:=image.save_png_to_buffer()
 for name in ["one","two","four"]:
  var f:=FileAccess.open("user://"+name+".png",FileAccess.WRITE);f.store_buffer(png);f.close()
 var batch=Batch.new()
 batch.prepare_path("user://one.png");batch.prepare_path("user://two.png")
 check(batch.dedup_hits==1,"Identical encoded PNGs share pending work")
 var wrappers:Array=[]
 for name in ["one","two"]:
  var texture:=ImageTexture.new();texture.set_meta("crew_pivot",Vector2(128,240));texture.set_meta("crew_standing_height",200.0)
  var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=texture
  batch.add(texture,wrapper,"user://"+name+".png");wrappers.append(wrapper)
 var stats:Dictionary=batch.finish()
 check(int(stats.get("private_skipped_png_decodes",0))==1,"Tablet skips duplicate PNG decoding before worker sharing")
 check(int(stats.get("private_work_window",8))==4,"Tablet retains at most four pending compression images")
 check(wrappers[0].diffuse_texture==wrappers[1].diffuse_texture,"Distinct paths share immutable source")
 check(wrappers[0].diffuse_texture.get_image().get_data()==image.get_data(),"Original decoded pixels are unchanged")
 var used:=Rect2(image.get_used_rect());var expected:=Rect2((used.position-Vector2(128,240))*(65.28/200.0),used.size*(65.28/200.0))
 check(wrappers[0].get_meta("crew_alpha_extent")==expected,"Alpha bounds and pivot density are unchanged")
 # Completed content lookup must skip decoding too, and must not merge changed art.
 batch.prepare_path("user://four.png")
 var changed:=image.duplicate();changed.set_pixel(40,30,Color.RED)
 changed.save_png("user://three.png");batch.prepare_path("user://three.png")
 check(batch.jobs.size()==1,"Changed PNG bytes receive independent compression work")
 var texture4:=ImageTexture.new();texture4.set_meta("crew_pivot",Vector2(90,180));texture4.set_meta("crew_standing_height",100.0)
 var wrapper4:=CanvasTexture.new();wrapper4.diffuse_texture=texture4;batch.add(texture4,wrapper4,"user://four.png")
 var last:Dictionary=batch.finish()
 check(wrapper4.diffuse_texture==wrappers[0].diffuse_texture,"Completed-content alias adopts the same source")
 check(wrapper4.get_meta("crew_alpha_extent")==Rect2((used.position-Vector2(90,180))*(65.28/100.0),used.size*(65.28/100.0)),"Shared source preserves each wrapper's own pivot and density")
 # Exercise the actual queue bound with more than eight distinct live images.
 var bounded=Batch.new();var held:Array=[]
 for i in range(10):
  var pixels:=image.duplicate();pixels.set_pixel(40,30,Color(float(i)/10.0,0.1,0.9,1));var path:="user://window-"+str(i)+".png";pixels.save_png(path)
  var tex:=ImageTexture.new();tex.set_meta("crew_pivot",Vector2.ZERO);tex.set_meta("crew_standing_height",100.0)
  var display:=CanvasTexture.new();display.diffuse_texture=tex;held.append(display);bounded.add(tex,display,path)
 var bounded_stats:Dictionary=bounded.finish()
 check(bounded_stats.private_compress_peak_jobs==4 and bounded_stats.private_peak_pending_image_bytes==4*image.get_data_size(),"Actual tablet work queue bounds ten unique images to four retained payloads")
 check(int(last.get("private_skipped_png_decodes",0))==2,"Completed content under a new path stays shared without new decode work")
 root.set_meta("tablet_controls",false)
 var desktop=Batch.new()
 desktop.prepare_path("user://one.png");desktop.prepare_path("user://two.png")
 var desktop_stats:Dictionary=desktop.finish()
 check(desktop_stats.private_skipped_png_decodes==0 and desktop.dedup_hits==1,"Desktop keeps original post-decode content sharing")
 check(int(desktop_stats.get("private_work_window",8))==8,"Desktop compression window remains eight")
 print("TABLET CREW DECODE failures=",failures," stats=",stats)
 quit(1 if failures else 0)
