extends RefCounted
## Disposable, app-local tablet CPU preparation. Source PNG digest is the key;
## saves never depend on this cache. No textures or decoded Images are retained.
const MAX_BYTES:=192*1024*1024
const MAX_ENTRY:=4*1024*1024
const MAX_RAW:=16*1024*1024
const MAX_FILES:=8192
var directory:String
var entries:Dictionary={}
var bytes:=0
var writes:=0
var hits:=0
var rejected:=0
func _init():
 directory=OS.get_cache_dir().path_join("BrineSpace/crew-frame-v1") if OS.has_feature("ios") else "user://crew-frame-cache-v1"
 if DirAccess.make_dir_recursive_absolute(directory)!=OK:return
 var dir:=DirAccess.open(directory)
 if dir==null:return
 var ordered:Array=[]
 for name in dir.get_files():
  if name.length()!=68 or not name.ends_with(".bin"):continue
  var path:=directory.path_join(name);var file:=FileAccess.open(path,FileAccess.READ)
  if file==null:continue
  var size:=file.get_length();file.close()
  entries[name]=size;bytes+=size
  ordered.append({"name":name,"time":FileAccess.get_modified_time(path)})
 ordered.sort_custom(func(a,b):return a.time<b.time)
 # Dictionary order is the eviction order; don't rescan thousands of files per write.
 var sorted:Dictionary={}
 for entry in ordered:sorted[entry.name]=entries[entry.name]
 entries=sorted
 _trim(0)
func _erase(name:String):
 if entries.has(name):bytes-=int(entries[name]);entries.erase(name)
 DirAccess.remove_absolute(directory.path_join(name))
func _trim(incoming:int):
 while not entries.is_empty() and (bytes+incoming>MAX_BYTES or entries.size()>=MAX_FILES):_erase(str(entries.keys()[0]))
func load_prepared(key:String)->Dictionary:
 var name:=key+".bin"
 if not entries.has(name):return {}
 var file:=FileAccess.open(directory.path_join(name),FileAccess.READ)
 if file==null:return {}
 var length:=file.get_length()
 if length<=32 or length>MAX_ENTRY:file.close();_erase(name);rejected+=1;return {}
 var checksum:=file.get_buffer(32);var payload:=file.get_buffer(length-32);file.close()
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 if hash.finish()!=checksum:_erase(name);rejected+=1;return {}
 var value:Variant=bytes_to_var(payload)
 if not _valid(value,key):_erase(name);rejected+=1;return {}
 # Check compressed integrity before handing bytes to the immutable frame API.
 if value.packed.decompress(value.raw_bytes,FileAccess.COMPRESSION_ZSTD).size()!=value.raw_bytes:
  _erase(name);rejected+=1;return {}
 var size:int=entries[name];entries.erase(name);entries[name]=size
 hits+=1;return value
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
func store_prepared(value:Dictionary):
 var body:Dictionary={}
 for key in ["key","dimensions","format","mipmaps","mipmap_count","raw_bytes","packed","used"]:body[key]=value[key]
 # Version is part of the directory; fixed shape prevents stale extra fields.
 body["revision"]=1
 var payload:=var_to_bytes(body)
 if payload.size()+32>MAX_ENTRY:return
 var name:String=str(body.key)+".bin"
 if entries.has(name):return
 _trim(payload.size()+32)
 var file:=FileAccess.open(directory.path_join(name),FileAccess.WRITE)
 if file==null:return
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(payload)
 file.store_buffer(hash.finish());file.store_buffer(payload);file.close()
 entries[name]=payload.size()+32;bytes+=payload.size()+32;writes+=1
