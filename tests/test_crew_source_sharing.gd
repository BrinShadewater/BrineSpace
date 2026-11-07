extends SceneTree
var checks:=0
var failures:=0
class Bank extends RefCounted:
 func source_image(frame:Texture2D)->Image:return frame.diffuse_texture.source
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures+=1;push_error(label)
func _initialize():call_deferred("run")
func run():
 check(OS.get_environment("BRINESPACE_TEST_USER_DIR")==OS.get_user_data_dir(),"Scratch profile required")
 check(DisplayServer.get_name()!="headless","Native renderer required")
 if failures:quit(2);return
 var image:=Image.create(8,8,false,Image.FORMAT_RGBA8);image.fill(Color.RED)
 var source=load("res://scripts/crew_storage/frame.gd").new();source.source=image
 var a:=CanvasTexture.new();a.diffuse_texture=source;a.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;a.set_meta("crew_pivot",Vector2(4,7))
 var b:=CanvasTexture.new();b.diffuse_texture=source;b.texture_filter=a.texture_filter;b.set_meta("crew_pivot",Vector2(1,2))
 var presenter=load("res://scripts/crew_storage/slots.gd").new();presenter.bank=Bank.new()
 var one:=Node2D.new();root.add_child(one);var two:=Node2D.new();root.add_child(two)
 presenter.begin_draw(one);presenter.begin_draw(two)
 var shown_a:CanvasTexture=presenter.acquire(one,a);var shown_b:CanvasTexture=presenter.acquire(two,b)
 check(shown_a.diffuse_texture==shown_b.diffuse_texture,"Distinct frame wrappers share one immutable source upload")
 check(presenter.uploads==1 and presenter.cache_bytes==256,"Pixel budget counts the unique upload once")
 check(shown_a.get_meta("crew_pivot")==a.get_meta("crew_pivot") and shown_b.get_meta("crew_pivot")==b.get_meta("crew_pivot"),"Shared image preserves each wrapper's metadata")
 check(shown_a.get_image().get_data()==image.get_data() and shown_b.get_image().get_data()==image.get_data(),"Full logical source pixels remain unchanged")
 var nearest:CanvasTexture=a.duplicate();nearest.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
 var shown_nearest:CanvasTexture=presenter.acquire(one,nearest)
 check(shown_nearest.texture_filter==CanvasItem.TEXTURE_FILTER_NEAREST and shown_nearest.diffuse_texture!=shown_a.diffuse_texture,"Different sampler policies keep independent storage")
 presenter.display_alias_limit=2
 var extra:CanvasTexture=a.duplicate();extra.set_meta("crew_pivot",Vector2(6,5))
 var overflow:CanvasTexture=presenter.acquire(one,extra)
 check(presenter.spill_allocations==1 and overflow.get_meta("crew_pivot")==Vector2(6,5),"Alias cap uses an independent immutable spill")
 check(overflow.get_image().get_data()==image.get_data(),"Alias overflow preserves full logical pixels")
 presenter.release_owner(one.get_instance_id());presenter.finish_frame()
 check(presenter.cache_bytes==512 and presenter.owners.size()==1,"Retained peer pins shared upload")
 check(shown_b.get_image().get_data()==image.get_data(),"Peer pixels survive original owner removal")
 presenter.release_owner(two.get_instance_id())
 check(presenter.cache_bytes==0 and presenter.slots.is_empty(),"Final owner releases shared storage and aliases")
 one.queue_free();two.queue_free()
 print("CREW SOURCE SHARING: %d checks, %d failures"%[checks,failures])
 quit(1 if failures else 0)
