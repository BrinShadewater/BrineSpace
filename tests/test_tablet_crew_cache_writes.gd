extends SceneTree
const Cache=preload("res://scripts/crew_storage/prepared_cache.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func value_for(image:Image,key:String)->Dictionary:
 return {"key":key,"dimensions":image.get_size(),"format":image.get_format(),"mipmaps":false,"mipmap_count":0,"raw_bytes":image.get_data_size(),"packed":image.get_data().compress(FileAccess.COMPRESSION_ZSTD),"used":Rect2(image.get_used_rect())}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var cache=Cache.new()
 check(cache.has_method("begin_store_prepared"),"Disposable crew cache writes must run in one bounded CPU worker instead of blocking adoption")
 if failures:quit(1);return
 var image:=Image.create(64,64,false,Image.FORMAT_RGBA8);image.fill(Color.CORAL)
 var first:=value_for(image,"a".repeat(64));var second:=value_for(image,"b".repeat(64))
 var a:Dictionary=cache.begin_store_prepared(first)
 check(not a.is_empty() and int(a.task)>=0,"Prepared write starts a CPU job")
 var b:Dictionary=cache.begin_store_prepared(second)
 check(bool(a.finished),"Starting another write joins the previous job; queue cannot grow")
 check(cache.finish_store(a)==1 and cache.finish_store(a)==1,"A completed ticket remains readable without double-counting shared cache counters")
 check(cache.finish_store(b)==1 and cache.writes==2,"Each owner's ticket reports its own successful write")
 check(cache.pending_write.is_empty(),"All pending payload/job references release after join")
 cache.flush_index()
 var loaded:Dictionary=cache.load_prepared(first.key)
 check(not loaded.is_empty() and loaded.packed.decompress(loaded.raw_bytes,FileAccess.COMPRESSION_ZSTD)==image.get_data(),"Worker-written cache preserves all source pixels")
 check(cache.begin_store_prepared(first).is_empty(),"Existing cache entry is not queued again")
 var third:=value_for(image,"c".repeat(64));cache.store_prepared(third)
 check(cache.pending_write.is_empty() and cache.writes==3,"Existing synchronous API joins its worker before returning")
 var fourth:=value_for(image,"d".repeat(64));var d:Dictionary=cache.begin_store_prepared(fourth);cache.flush_index()
 check(d.finished and cache.pending_write.is_empty() and cache.writes==4,"Index flush joins its final write before persisting metadata")
 var reopened=Cache.new();check(not reopened.load_prepared(fourth.key).is_empty(),"Persisted index exposes the final worker-written entry")
 var bad=Cache.new();var previous_entries:int=bad.entries.size();bad.directory="user://missing-parent/not-created";var failure:Dictionary=bad.begin_store_prepared(value_for(image,"e".repeat(64)))
 check(bad.finish_store(failure)==0 and bad.pending_write.is_empty() and bad.writes==0 and bad.entries.size()==previous_entries,"Optional write failure leaves no admitted entry or pending work")
 print("TABLET CREW CACHE WRITES failures=",failures);quit(1 if failures else 0)
