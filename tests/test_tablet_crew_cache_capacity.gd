extends SceneTree
const Cache=preload("res://scripts/crew_storage/prepared_cache.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var cache=Cache.new()
 var image:=Image.create(16,16,false,Image.FORMAT_RGBA8);image.fill(Color.CORAL)
 var packed:=image.get_data().compress(FileAccess.COMPRESSION_ZSTD)
 # The multi-crew cache reached its file ceiling below its byte budget on iPad.
 # Exercise real admission/restart/reads, not the numeric file-limit constant.
 for i in 9000:
  var key:=("capacity-fixture-%d"%i).sha256_text()
  cache.store_prepared({"key":key,"dimensions":Vector2i(16,16),"format":Image.FORMAT_RGBA8,"mipmaps":false,"mipmap_count":0,"raw_bytes":1024,"packed":packed,"used":Rect2(0,0,16,16)})
 cache.flush_index()
 check(cache.entries.size()==9000,"A multi-crew working set below the disk byte budget must not churn prepared frames")
 check(cache.bytes<192*1024*1024,"Fixture remains below the unchanged 192 MiB byte budget")
 var reopened=Cache.new()
 check(reopened.index_loaded and reopened.index_file_opens==0,"Large working set reopens through the validated compact index")
 for i in [0,4500,8999]:
  var loaded:Dictionary=reopened.load_prepared(("capacity-fixture-%d"%i).sha256_text())
  check(not loaded.is_empty() and loaded.packed.decompress(loaded.raw_bytes,FileAccess.COMPRESSION_ZSTD)==image.get_data(),"Old and new prepared frames survive restart with exact pixels")
 var huge:Dictionary={}
 for i in 20000:huge[("too-many-%d"%i).sha256_text()+".bin"]=100
 check(not reopened._valid_index(huge),"Index still rejects an unbounded file count")
 reopened._trim(192*1024*1024)
 check(reopened.entries.is_empty() and reopened.bytes==0,"Byte pressure still evicts prepared entries independently of file-count headroom")
 print("TABLET CREW CACHE CAPACITY failures=",failures)
 quit(1 if failures else 0)
