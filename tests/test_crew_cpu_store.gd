extends SceneTree
var failures:=0
var checks:=0
class Target extends RefCounted:
 var frames:Dictionary={}
 var equipment_frames:Dictionary={}
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _initialize():call_deferred("run")
func run():
 if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir():quit(2);return
 var Frame=load("res://scripts/crew_storage/frame.gd")
 var frame=Frame.new()
 check(frame.has_method("offload"),"CPU frames support bounded backing storage")
 if failures:quit(1);return
 var Store=load("res://scripts/crew_storage/cpu_store.gd")
 var store=Store.new();store.cache_limit=80
 check(store.open("user://cpu-store.bin"),"Create session-owned backing file")
 var originals:Array=[];var frames:Array=[];var hashes:Array=[]
 for i in range(12):
  var image:=Image.create(32,32,false,Image.FORMAT_RGBA8)
  image.fill(Color(float(i)/12.0,0.3,0.8,1));image.set_pixel(i,2,Color.RED)
  var path:="user://cpu-frame-%d.png"%i;image.save_png(path)
  var item=Frame.new();item.source=image
  var digest:String=item.checkpoint_rgba_sha256()
  check(item.offload(store,path),"Offload frame %d"%i)
  check(item.packed.is_empty(),"Inactive compressed bytes released %d"%i)
  originals.append(image.get_data());frames.append(item);hashes.append(digest)
 for index in range(2):
  for i in range(frames.size()-1,-1,-1):
   check(frames[i].get_image().get_data()==originals[i],"Eviction/reentry preserves full pixels")
   check(frames[i].checkpoint_rgba_sha256()==hashes[i],"Checkpoint signature remains exact")
   check(store.cache_bytes<=store.cache_limit,"Hot compressed payload stays bounded")
 check(store.reads>0,"Evicted payloads read on demand")
 # Caller mutation cannot alter the canonical record or another returned Image.
 var returned:Image=frames[0].get_image();returned.fill(Color.GREEN)
 check(frames[0].get_image().get_data()==originals[0],"Independent decoded Images")
 var broken=Store.new()
 check(not broken.open("user://missing-parent/store.bin"),"Creation failure is recoverable")
 var kept=Frame.new();kept.source=Image.create(4,4,false,Image.FORMAT_RGBA8)
 check(not kept.offload(broken,"user://missing.png") and not kept.packed.is_empty(),"Failed offload keeps original bytes")
 store.clear_cache()
 # Corrupt backing bytes; immutable source PNG must recover the original pixels.
 var corrupt:=FileAccess.open("user://cpu-store.bin",FileAccess.READ_WRITE)
 corrupt.seek(frames[0].backing_key);corrupt.store_8(0);corrupt.flush();corrupt.close()
 check(frames[0].get_image().get_data()==originals[0],"Corrupt record recovers exact source pixels")
 check(store.recoveries==1,"Recovery is recorded")
 root.set_meta("tablet_controls",true)
 var target:=Target.new();var wrapper:=CanvasTexture.new()
 var bank_source=Frame.new();bank_source.source=Image.create_from_data(32,32,false,Image.FORMAT_RGBA8,originals[1])
 bank_source.set_meta("private_source_png","user://cpu-frame-1.png")
 wrapper.diffuse_texture=bank_source;target.frames={"idle":[wrapper]}
 var bank=load("res://scripts/crew_storage/bank.gd").new();bank.adopt(target)
 check(bank_source.packed.is_empty()==OS.get_cmdline_user_args().has("--bounded-crew-cpu-store"),"Tablet bank offloading is explicitly opt-in")
 check(bank.source_image(wrapper).get_data()==originals[1],"Bank adoption still resolves exact pixels")
 var bank_path:String=bank_source.backing.path if bank_source.backing!=null else ""
 bank=null;target=null;wrapper=null;bank_source=null
 check(not FileAccess.file_exists(bank_path),"Bank teardown releases backing file")
 root.set_meta("tablet_controls",false)
 var file_path:String=store.path
 frames.clear();frame=null;store=null
 check(not FileAccess.file_exists(file_path),"Last owner removes session file")
 print("CREW CPU STORE: %d checks, %d failures"%[checks,failures])
 quit(1 if failures else 0)
