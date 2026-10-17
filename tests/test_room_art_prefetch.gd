extends SceneTree
const Dressing=preload("res://rooms/whole-room/room_dressing.gd")
const Prefetch=preload("res://scripts/image_prefetch.gd")
const SOURCES=["res://legacy/default/rooms/whole-room/nursery-master.png","res://legacy/default/rooms/whole-room/life-support-candidate.png"]
class Pool extends RefCounted:
	var announced:Array=[]
	func acquire(path:String)->Dictionary:
		announced.append(Prefetch.index_of.has(path))
		return {"texture":RefCounted.new()}
class Host extends RefCounted:
	var life_items:Array=[]
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func exercise(path:String)->Pool:
	var host:=Host.new();var pool:=Pool.new();host.set_meta("room_texture_pool",pool)
	var dressing=Dressing.new(host,path)
	check(dressing.textures.size()==2 and host.life_items.is_empty(),"Texture keys and empty authored furniture preserved")
	return pool
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR").is_empty() or OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):
		push_error("Scratch profile required");quit(2);return
	var path:="user://room-art-prefetch-profile.json"
	var file:=FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify({"textures":{"first":SOURCES[0],"second":SOURCES[1]},"furniture":[]}));file.close()
	var manifest:="user://room-art-prefetch-order.txt"
	if FileAccess.file_exists(manifest):DirAccess.remove_absolute(ProjectSettings.globalize_path(manifest))
	Prefetch.begin(manifest)
	var pool:=exercise(path)
	check(pool.announced==[true,true],"Fresh profile announces all room textures before the first acquisition")
	check(Prefetch.paths==PackedStringArray(SOURCES) and Prefetch.tasks.is_empty(),"Announcement preserves order and performs no eager decoding")
	Prefetch.end()
	file=FileAccess.open(manifest,FileAccess.WRITE);file.store_string(SOURCES[1]+"\n");file.close()
	Prefetch.begin(manifest);pool=exercise(path)
	check(pool.announced==[false,true] and Prefetch.paths==PackedStringArray([SOURCES[1]]),"Learned repeat order stays authoritative")
	Prefetch.end();pool=exercise(path)
	check(pool.announced==[false,false] and Prefetch.paths.is_empty(),"Ordinary room construction leaves prefetch inactive")
	check(Prefetch.tasks.is_empty() and Prefetch.results.is_empty() and Prefetch.cached_bytes==0,"No decoded jobs/images retained")
	print("ROOM ART PREFETCH ","PASS" if failures==0 else "FAIL", " failures=",failures)
	quit(1 if failures else 0)
