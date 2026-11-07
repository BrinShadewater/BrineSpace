extends SceneTree
const Frame=preload("res://scripts/crew_storage/frame.gd")
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
 if not ok:failures+=1;push_error(label)
func run():
 if OS.get_user_data_dir()!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
 var image:=Image.create(64,64,false,Image.FORMAT_RGBA8)
 for y in 64:
  for x in 64:image.set_pixel(x,y,Color(float(x)/64.0,float(y)/64.0,float((x*y)%64)/64.0,1))
 var frame=Frame.new();frame.source=image
 var expected:=image.get_data().hex_encode().sha256_text()
 check(frame.checkpoint_rgba_sha256()==expected,"Checkpoint keeps existing RGBA binding")
 check(frame.checkpoint_rgba_sha256()==expected,"Repeated binding is stable")
 var retained:=0
 for property in frame.get_property_list():
  if property.name=="packed":continue
  var value=frame.get(property.name)
  if value is PackedByteArray:retained+=value.size()
 check(retained<=32,"Checkpoint validity cache must not retain another compressed frame payload")
 image.fill(Color.RED)
 var replacement:=image.get_data().compress(FileAccess.COMPRESSION_ZSTD)
 # Mutate the same PackedByteArray, preserving size and alias identity.
 frame.packed.resize(replacement.size())
 for i in replacement.size():frame.packed[i]=replacement[i]
 check(frame.checkpoint_rgba_sha256()==image.get_data().hex_encode().sha256_text(),"In-place compressed edits invalidate cached RGBA binding")
 print("CREW CHECKPOINT STORAGE failures=",failures)
 quit(1 if failures else 0)
