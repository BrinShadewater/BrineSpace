extends RefCounted
## Opt-in session store. Main-thread ownership; no global frame or Image references.
## A private open file owns cold bytes independently of the evictable prepared cache.
var path:=""
var file:FileAccess
var cache_limit:=16*1024*1024
var cache_bytes:=0
var cache:Dictionary={}
var records:Dictionary={}
var reads:=0
var recoveries:=0
var read_usec:=0
var write_usec:=0
static func digest(bytes:PackedByteArray)->PackedByteArray:
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(bytes)
 return hash.finish()
func open(destination:String)->bool:
 if file!=null or FileAccess.file_exists(destination):return false
 file=FileAccess.open(destination,FileAccess.WRITE_READ)
 if file==null:return false
 path=destination
 return true
func append(bytes:PackedByteArray,source_path:String)->int:
 if file==null or bytes.is_empty() or not FileAccess.file_exists(source_path):return -1
 var started:=Time.get_ticks_usec()
 var expected:=digest(bytes)
 file.seek_end();var offset:=file.get_position()
 file.store_buffer(bytes);file.flush()
 if file.get_error()!=OK:return -1
 file.seek(offset)
 var verified:=file.get_buffer(bytes.size())
 if verified.size()!=bytes.size() or digest(verified)!=expected:return -1
 records[offset]={"size":bytes.size(),"digest":expected,"source":source_path}
 write_usec+=Time.get_ticks_usec()-started
 return offset
func clear_cache():
 cache.clear();cache_bytes=0
func _remember(key:int,bytes:PackedByteArray):
 if cache.has(key):cache_bytes-=cache[key].size();cache.erase(key)
 if bytes.size()>cache_limit:return
 while not cache.is_empty() and cache_bytes+bytes.size()>cache_limit:
  var oldest:int=cache.keys()[0];cache_bytes-=cache[oldest].size();cache.erase(oldest)
 cache[key]=bytes;cache_bytes+=bytes.size()
func read(key:int)->PackedByteArray:
 if not records.has(key):return PackedByteArray()
 if cache.has(key):
  var hot:PackedByteArray=cache[key];cache.erase(key);cache[key]=hot
  return hot
 var started:=Time.get_ticks_usec()
 var record:Dictionary=records[key]
 var bytes:=PackedByteArray()
 if file!=null:
  file.seek(key);bytes=file.get_buffer(record.size);reads+=1
 if bytes.size()!=record.size or digest(bytes)!=record.digest:
  # Never display changed/replaced art as a successful recovery. Source pixels
  # must reproduce the exact compressed record from this engine/build.
  var image:=Image.new()
  if image.load(record.source)!=OK:return PackedByteArray()
  bytes=image.get_data().compress(FileAccess.COMPRESSION_ZSTD)
  if bytes.size()!=record.size or digest(bytes)!=record.digest:return PackedByteArray()
  recoveries+=1
 _remember(key,bytes)
 read_usec+=Time.get_ticks_usec()-started
 return bytes
func _notification(what:int):
 if what==NOTIFICATION_PREDELETE:
  if file!=null:file.close();file=null
  if not path.is_empty():DirAccess.remove_absolute(path)
