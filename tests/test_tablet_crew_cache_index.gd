extends SceneTree
const Cache=preload("res://scripts/crew_storage/prepared_cache.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func value(key:String)->Dictionary:
 var image:=Image.create(32,32,false,Image.FORMAT_RGBA8);image.fill(Color.AQUA)
 return {"key":key,"dimensions":Vector2i(32,32),"format":Image.FORMAT_RGBA8,"mipmaps":false,"mipmap_count":0,"raw_bytes":4096,"packed":image.get_data().compress(FileAccess.COMPRESSION_ZSTD),"used":Rect2(0,0,32,32)}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var cache=Cache.new()
 check(cache.has_method("flush_index"),"Prepared cache persists a compact restart index instead of reopening every frame")
 if failures:quit(1);return
 var key:="original".sha256_text();cache.store_prepared(value(key));cache.flush_index()
 var reopened=Cache.new()
 check(reopened.index_loaded and reopened.index_file_opens==0,"Restart reuses validated index without opening every known entry")
 check(not reopened.load_prepared(key).is_empty(),"Index reuse preserves full per-entry checksum/decompression validation")
 # Unknown entry after an interrupted index write is recovered, while removed files disappear.
 var other:="new".sha256_text();reopened.store_prepared(value(other))
 var interrupted=Cache.new()
 check(interrupted.entries.has(other+".bin") and interrupted.index_file_opens==1,"Unindexed entry is reconciled once")
 interrupted.load_prepared(key);interrupted.flush_index()
 var lru=Cache.new()
 check(lru.entries.keys()==[other+".bin",key+".bin"],"Restart preserves recent-read eviction order")
 DirAccess.remove_absolute(interrupted.directory.path_join(key+".bin"));interrupted.flush_index()
 var purged=Cache.new()
 check(not purged.entries.has(key+".bin") and not purged.load_prepared(other).is_empty(),"OS partial purge cannot resurrect absent cache entries")
 # Index corruption triggers an ordinary rebuild; source data stays independently verified.
 var index_path:String=purged.directory.path_join(".index-v1")
 var encoded:=FileAccess.get_file_as_bytes(index_path);encoded[0]=encoded[0]^1
 var broken:=FileAccess.open(index_path,FileAccess.WRITE);broken.store_buffer(encoded);broken.close()
 var recovered=Cache.new()
 check(not recovered.index_loaded and not recovered.load_prepared(other).is_empty(),"Corrupt index safely rebuilds from disposable files")
 recovered.flush_index()
 # A changed cached file cannot bypass checksum validation or inflate allocations unchecked.
 var file:=FileAccess.open(recovered.directory.path_join(other+".bin"),FileAccess.WRITE);file.store_string("bad");file.close()
 var changed=Cache.new()
 check(changed.load_prepared(other).is_empty() and changed.rejected==1,"Known-name replacement is still validated and rejected")
 var invalid:Dictionary={"../outside.bin":33}
 check(not changed._valid_index({other+".bin":Cache.MAX_ENTRY+1}),"Index rejects oversized frame metadata")
 check(not changed._valid_index(invalid),"Index rejects paths outside the disposable cache")
 print("TABLET CREW CACHE INDEX failures=",failures)
 quit(1 if failures else 0)
