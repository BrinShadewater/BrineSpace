extends SceneTree
const Keys=preload("res://scripts/crew_storage/source_keys.gd")
const Batch=preload("res://scripts/crew_storage/worker_batch.gd")
const SOURCE:="res://character/major-bill-v3/rotations/south.png"
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func prepare()->Dictionary:
 var b=Batch.new();var texture:=ImageTexture.new();texture.set_meta("crew_pivot",Vector2(92,172));texture.set_meta("crew_standing_height",148.0)
 var wrapper:=CanvasTexture.new();wrapper.diffuse_texture=texture;b.add(texture,wrapper,SOURCE)
 return {"stats":b.finish(),"frame":wrapper}
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 root.set_meta("tablet_controls",true)
 Keys.immutable_sources=false
 var baseline:=prepare()
 Keys.immutable_sources=true
 var table=Keys.new()
 var data:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(Keys.PATH))
 check(table.lookup(SOURCE)==FileAccess.get_sha256(SOURCE),"Installed immutable source identity matches original PNG")
 check(table.keys.size()+table.digests.size()==int(data.count)*64,"Retain only two compact32-byte key arrays")
 Keys.session=table
 var warm:=prepare()
 check(int(warm.stats.get("private_source_key_hits",0))==1 and int(warm.stats.get("private_source_png_reads",-1))==0,"Warm immutable package source skips original PNG reads")
 check(warm.frame.get_image().get_data()==baseline.frame.get_image().get_data(),"Indexed cache returns original pixels")
 check(warm.frame.get_meta("crew_alpha_extent")==baseline.frame.get_meta("crew_alpha_extent"),"Indexed cache preserves pivot/density/alpha geometry")
 check(table.lookup("user://changed.png").is_empty() and table.lookup("res://character/missing.png").is_empty(),"Mutable or absent sources retain ordinary validation")
 var bad:Dictionary=data.duplicate();bad.checksum="00".repeat(32)
 check(not table.load_data(bad) and table.lookup(SOURCE).is_empty(),"Bad checksum clears stale identity data")
 check(not table.load_data({"schema":1,"count":Keys.MAX_KEYS+1}),"Oversized identity table rejected")
 check(table.load_path(Keys.PATH),"Valid packaged table reloads")
 check(not table.load_path("user://missing-index.json") and table.keys.is_empty(),"Missing table clears retained data")
 Keys.session=table
 var ordinary:=prepare()
 check(int(ordinary.stats.private_source_key_hits)==0 and int(ordinary.stats.private_source_png_reads)==1 and ordinary.frame.get_image().get_data()==baseline.frame.get_image().get_data(),"Missing index uses original PNG fingerprinting and exact cached pixels")
 table.load_path(Keys.PATH);Keys.session=table
 var cache=preload("res://scripts/crew_storage/prepared_cache.gd").shared()
 var key:=FileAccess.get_sha256(SOURCE)
 var file:=FileAccess.open(cache.directory.path_join(key+".bin"),FileAccess.WRITE);file.store_string("broken");file.close()
 var repaired:=prepare()
 check(int(repaired.stats.private_disk_cache_rejected)==1 and int(repaired.stats.private_worker_png_jobs)==1,"Corrupt prepared data still falls back to bounded original PNG decode")
 check(repaired.frame.get_image().get_data()==baseline.frame.get_image().get_data(),"Repair preserves original pixels")
 root.set_meta("tablet_controls",false)
 var desktop:=prepare()
 check(int(desktop.stats.get("private_source_key_hits",0))==0,"Desktop preparation stays unchanged")
 Keys.immutable_sources=false
 check(table.lookup(SOURCE).is_empty(),"Editor/default mutable source policy never trusts package table")
 print("TABLET CREW SOURCE KEYS failures=",failures," warm=",warm.stats)
 quit(1 if failures else 0)
