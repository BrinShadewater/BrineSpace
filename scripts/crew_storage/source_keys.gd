extends RefCounted
## Immutable installed iOS package identities; editor/user files keep ordinary hashing.
const PATH:="res://assets/tablet-crew-source-keys.json"
const MAX_KEYS:=60000
const MAX_FILE_BYTES:=9*1024*1024
static var immutable_sources:=OS.has_feature("ios") and not OS.has_feature("editor")
static var session:RefCounted
var keys:=PackedByteArray()
var digests:=PackedByteArray()
static func shared()->RefCounted:
 if session==null:session=load("res://scripts/crew_storage/source_keys.gd").new()
 return session
func _init():
 if immutable_sources:load_path(PATH)
func load_path(path:String)->bool:
 keys=PackedByteArray();digests=PackedByteArray()
 var file:=FileAccess.open(path,FileAccess.READ)
 if file==null:return false
 var size:=file.get_length()
 if size<=0 or size>MAX_FILE_BYTES:file.close();return false
 var text:=file.get_as_text();file.close()
 var parser:=JSON.new()
 if parser.parse(text)!=OK:return false
 return load_data(parser.data)
func load_data(value:Variant)->bool:
 keys=PackedByteArray();digests=PackedByteArray()
 if not value is Dictionary or value.size()!=5 or value.get("schema")!=1:return false
 var count:Variant=value.get("count")
 if not (count is int or count is float) or not is_finite(float(count)) or float(count)!=floorf(float(count)) or count<0 or count>MAX_KEYS:return false
 var n:=int(count)
 for field in ["path_keys","source_keys","checksum"]:
  var text:Variant=value.get(field)
  var length:int=64 if field=="checksum" else n*64
  if not text is String or text.length()!=length:return false
  if length>0 and (text[0] in ["+","-"] or not text.is_valid_hex_number(false)):return false
 var new_keys:PackedByteArray=value.path_keys.hex_decode()
 var new_digests:PackedByteArray=value.source_keys.hex_decode()
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256)
 hash.update(new_keys);hash.update(new_digests)
 if hash.finish().hex_encode()!=value.checksum:return false
 for i in range(1,n):
  if _compare(new_keys,(i-1)*32,new_keys,i*32)>=0:return false
 keys=new_keys;digests=new_digests;return true
static func _compare(left:PackedByteArray,a:int,right:PackedByteArray,b:int)->int:
 for i in 32:
  if left[a+i]!=right[b+i]:return -1 if left[a+i]<right[b+i] else 1
 return 0
func lookup(path:String)->String:
 if not immutable_sources or keys.is_empty() or not path.begins_with("res://") or not path.ends_with(".png"):return ""
 var key:=path.sha256_text().hex_decode()
 var low:=0;var high:=keys.size()/32
 while low<high:
  var mid:int=(low+high)/2
  if _compare(keys,mid*32,key,0)<0:low=mid+1
  else:high=mid
 if low>=keys.size()/32 or _compare(keys,low*32,key,0)!=0:return ""
 return digests.slice(low*32,(low+1)*32).hex_encode()
