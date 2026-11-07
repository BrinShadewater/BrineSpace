extends RefCounted
## Disposable, app-local tablet CPU preparation. Source PNG digest is the key;
## saves never depend on this cache. No textures or decoded Images are retained.
const MAX_BYTES:=192*1024*1024
const MAX_ENTRY:=4*1024*1024
const MAX_RAW:=16*1024*1024
# Four current crew banks need 8262 distinct prepared files. The old 8192
# ceiling caused cyclic LRU misses despite spare byte budget; decoded memory
# and worker bounds are independent and unchanged. The index stays capped below.
const MAX_FILES:=16384
const INDEX_NAME:=".index-v1"
const MAX_INDEX_BYTES:=2*1024*1024
static var shared_session:RefCounted
static func cache_directory()->String:
 return OS.get_cache_dir().path_join("BrineSpace/crew-frame-v1") if OS.has_feature("ios") else "user://crew-frame-cache-v1"
static func shared()->RefCounted:
 # Reuse metadata, not pixels: each batch still validates the bytes it opens.
 # Profile changes and OS removal of the whole disposable directory reset it.
 var path:=cache_directory()
 if shared_session==null or shared_session.directory!=path or not DirAccess.dir_exists_absolute(path):
  shared_session=load("res://scripts/crew_storage/prepared_cache.gd").new()
 return shared_session
var directory:String
var entries:Dictionary={}
var bytes:=0
var writes:=0
var hits:=0
var rejected:=0
var index_loaded:=false
var index_file_opens:=0
var index_dirty:=false
var pending_write:Dictionary={}
static func _valid_name(name:String)->bool:
 return name.length()==68 and name.ends_with(".bin") and name[0] not in ["-","+"] and name.substr(0,64).is_valid_hex_number(false)
static func _valid_index(value:Variant)->bool:
 if not value is Dictionary or value.size()>MAX_FILES:return false
 var total:=0
 for name in value:
  if not name is String or not _valid_name(name) or not value[name] is int or value[name]<=32 or value[name]>MAX_ENTRY:return false
  total+=int(value[name])
  if total>MAX_BYTES:return false
 return true
func _read_index()->Dictionary:
 var file:=FileAccess.open(directory.path_join(INDEX_NAME),FileAccess.READ)
 if file==null:return {}
 var size:=file.get_length()
 if size<=32 or size>MAX_INDEX_BYTES:file.close();return {}
 var checksum:=file.get_buffer(32);var payload:=file.get_buffer(size-32);file.close()
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 if hash.finish()!=checksum:return {}
 var value:Variant=bytes_to_var(payload)
 if not _valid_index(value):return {}
 index_loaded=true
 return value
func _init():
 directory=cache_directory()
 if DirAccess.make_dir_recursive_absolute(directory)!=OK:return
 var dir:=DirAccess.open(directory)
 if dir==null:return
 var known:=_read_index()
 var present:Dictionary={}
 var unknown:Array=[]
 for name in dir.get_files():
  if not _valid_name(name):continue
  if known.has(name):present[name]=true;continue
  var path:=directory.path_join(name);var file:=FileAccess.open(path,FileAccess.READ)
  index_file_opens+=1
  if file==null:continue
  var size:=file.get_length();file.close()
  if size<=32 or size>MAX_ENTRY:
   DirAccess.remove_absolute(path);continue
  unknown.append({"name":name,"size":size,"time":FileAccess.get_modified_time(path)})
 # Keep persisted LRU order; missing files vanish and unindexed files are recovered.
 for name in known:
  if present.has(name):entries[name]=known[name];bytes+=int(known[name])
 unknown.sort_custom(func(a,b):return a.time<b.time)
 for entry in unknown:entries[entry.name]=entry.size;bytes+=int(entry.size)
 index_dirty=not index_loaded or not unknown.is_empty() or present.size()!=known.size()
 _trim(0)
func flush_index():
 finish_store(pending_write)
 if not index_dirty or not _valid_index(entries):return
 var payload:=var_to_bytes(entries)
 if payload.size()+32>MAX_INDEX_BYTES:return
 var temporary:=directory.path_join(INDEX_NAME+".tmp")
 var file:=FileAccess.open(temporary,FileAccess.WRITE)
 if file==null:return
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 file.store_buffer(hash.finish());file.store_buffer(payload);file.close()
 if DirAccess.rename_absolute(temporary,directory.path_join(INDEX_NAME))==OK:index_dirty=false
func _erase(name:String):
 if entries.has(name):bytes-=int(entries[name]);entries.erase(name);index_dirty=true
 DirAccess.remove_absolute(directory.path_join(name))
func _trim(incoming:int):
 while not entries.is_empty() and (bytes+incoming>MAX_BYTES or entries.size()>=MAX_FILES):_erase(str(entries.keys()[0]))
func begin_read(key:String)->Dictionary:
 var name:=key+".bin"
 if not entries.has(name):return {}
 # Capture only immutable strings; workers never touch this index or SceneTree.
 var path:=directory.path_join(name)
 var result:Dictionary={}
 var task:=WorkerThreadPool.add_task(func():result.merge(_read_file(path,key)),true)
 return {"key":key,"name":name,"task":task,"result":result}
func finish_read(ticket:Dictionary)->Dictionary:
 WorkerThreadPool.wait_for_task_completion(ticket.task)
 return _accept_read(ticket.key,ticket.result)
func load_prepared(key:String)->Dictionary:
 var name:=key+".bin"
 if not entries.has(name):return {}
 return _accept_read(key,_read_file(directory.path_join(name),key))
func _accept_read(key:String,result:Dictionary)->Dictionary:
 var name:=key+".bin"
 if result.value.is_empty():
  _erase(name)
  if result.rejected:rejected+=1
  return {}
 # Only the main-thread owner mutates eviction metadata/counters.
 if entries.has(name):
  var size:int=int(result.get("file_bytes",entries[name]))
  bytes+=size-int(entries[name]);entries.erase(name);entries[name]=size;index_dirty=true
  _trim(0)
 hits+=1;return result.value
static func _read_file(path:String,key:String)->Dictionary:
 var bad:Dictionary={"value":{},"rejected":true}
 var file:=FileAccess.open(path,FileAccess.READ)
 if file==null:return {"value":{},"rejected":false}
 var length:=file.get_length()
 if length<=32 or length>MAX_ENTRY:file.close();return bad
 var checksum:=file.get_buffer(32);var payload:=file.get_buffer(length-32);file.close()
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 if hash.finish()!=checksum:return bad
 var value:Variant=bytes_to_var(payload)
 if not _valid(value,key):return bad
 # Validate compressed integrity before immutable frame adoption; retain no Image.
 if value.packed.decompress(value.raw_bytes,FileAccess.COMPRESSION_ZSTD).size()!=value.raw_bytes:return bad
 return {"value":value,"rejected":false,"file_bytes":length}
static func _valid(value:Variant,key:String)->bool:
 if not value is Dictionary or value.size()!=9 or value.get("key")!=key or value.get("revision")!=1:return false
 if not value.get("dimensions") is Vector2i or value.dimensions.x<=0 or value.dimensions.y<=0 or value.dimensions.x>2048 or value.dimensions.y>2048:return false
 if not value.get("format") is int or value.format<0 or value.format>=Image.FORMAT_MAX:return false
 if not value.get("mipmaps") is bool or not value.get("mipmap_count") is int or value.mipmap_count<0 or value.mipmap_count>12:return false
 if not value.get("raw_bytes") is int or value.raw_bytes<=0 or value.raw_bytes>MAX_RAW:return false
 var channels:int={Image.FORMAT_L8:1,Image.FORMAT_LA8:2,Image.FORMAT_RGB8:3,Image.FORMAT_RGBA8:4}.get(value.format,0)
 if channels==0:return false # Other source formats keep the ordinary loader.
 var expected:=0;var width:int=value.dimensions.x;var height:int=value.dimensions.y;var count:=0
 while true:
  expected+=width*height*channels
  if not value.mipmaps or (width==1 and height==1):break
  width=maxi(width/2,1);height=maxi(height/2,1);count+=1
 if value.raw_bytes!=expected or value.mipmap_count!=count:return false
 if not value.get("packed") is PackedByteArray or value.packed.is_empty() or value.packed.size()>MAX_ENTRY:return false
 if not value.get("used") is Rect2 or not value.used.position.is_finite() or not value.used.size.is_finite():return false
 return value.used.position.x>=0 and value.used.position.y>=0 and value.used.size.x>=0 and value.used.size.y>=0 and value.used.end.x<=value.dimensions.x and value.used.end.y<=value.dimensions.y
# At most one immutable serialized payload is pending. Only this owner changes
# LRU/index metadata; the worker hashes and writes bytes, never Images or nodes.
func begin_store_prepared(value:Dictionary)->Dictionary:
 finish_store(pending_write)
 var body:Dictionary={}
 for key in ["key","dimensions","format","mipmaps","mipmap_count","raw_bytes","packed","used"]:body[key]=value[key]
 body["revision"]=1
 var payload:=var_to_bytes(body)
 if payload.size()+32>MAX_ENTRY:return {}
 var name:String=str(body.key)+".bin"
 if entries.has(name):return {}
 _trim(payload.size()+32)
 var path:=directory.path_join(name)
 var result:Dictionary={}
 var task:=WorkerThreadPool.add_task(func():result.merge(_write_file(path,payload)),true)
 pending_write={"task":task,"name":name,"size":payload.size()+32,"result":result,"finished":false,"written":false}
 return pending_write
static func _write_file(path:String,payload:PackedByteArray)->Dictionary:
 var file:=FileAccess.open(path,FileAccess.WRITE)
 if file==null:return {"written":false}
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 file.store_buffer(hash.finish());file.store_buffer(payload)
 var ok:=file.get_error()==OK and file.get_position()==payload.size()+32
 file.close();return {"written":ok}
func finish_store(ticket:Dictionary)->int:
 if ticket.is_empty():return 0
 if not ticket.finished:
  WorkerThreadPool.wait_for_task_completion(ticket.task)
  ticket.written=bool(ticket.result.get("written",false));ticket.finished=true
  if ticket.written:
   entries[ticket.name]=ticket.size;bytes+=int(ticket.size);writes+=1;index_dirty=true
  else:DirAccess.remove_absolute(directory.path_join(ticket.name))
 if is_same(pending_write,ticket):pending_write={}
 return 1 if ticket.written else 0
func store_prepared(value:Dictionary):
 # Existing direct callers still observe a complete write on return.
 finish_store(begin_store_prepared(value))
