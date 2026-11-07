extends SceneTree
var checks:int=0
var failures:int=0
class Bank extends RefCounted:
	func source_image(frame:Texture2D)->Image:return frame.diffuse_texture.source
func expect(condition:bool,message:String):
	checks+=1
	if not condition:failures+=1;push_error(message)
func _initialize():call_deferred("run")
func pixels(texture:Texture2D)->PackedByteArray:return texture.diffuse_texture.get_image().get_data()
func make_frame(color:Color,size:int=8)->CanvasTexture:
	var cpu=load("res://scripts/crew_storage/frame.gd").new()
	var image:=Image.create(size,size,false,Image.FORMAT_RGBA8);image.fill(color);cpu.source=image
	var frame:=CanvasTexture.new();frame.diffuse_texture=cpu;frame.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	frame.set_meta("pivot",Vector2(4,7));return frame
func run():
	expect(DisplayServer.get_name()!="headless","Native renderer required")
	var script=load("res://scripts/crew_storage/slots.gd")
	if script==null or not script.can_instantiate():quit(2);return
	var presenter=script.new();presenter.bank=Bank.new();presenter.capacity=2;presenter.cache_byte_limit=512
	var one:=Node2D.new();var two:=Node2D.new();root.add_child(one);root.add_child(two)
	var a:=make_frame(Color.RED);var b:=make_frame(Color.GREEN);var c:=make_frame(Color.BLUE);var big:=make_frame(Color.WHITE,16)
	presenter.begin_draw(one);presenter.begin_draw(two)
	var shown_a:Texture2D=presenter.acquire(one,a);var shown_b:Texture2D=presenter.acquire(two,b)
	await RenderingServer.frame_post_draw
	expect(presenter.cache_bytes==512 and presenter.slots.size()==2,"Initial cache budget")
	expect(pixels(shown_a)==a.diffuse_texture.source.get_data(),"Initial A pixels")
	expect(pixels(shown_b)==b.diffuse_texture.source.get_data(),"Initial B pixels")
	expect(shown_a.texture_filter==a.texture_filter and shown_a.get_meta("pivot")==a.get_meta("pivot"),"Frame metadata/filter")
	presenter.begin_draw(one)
	var shown_c:Texture2D=presenter.acquire(one,c)
	expect(presenter.evictions==1 and presenter.cache_bytes==512,"Free-only byte eviction")
	expect(pixels(shown_a)==a.diffuse_texture.source.get_data(),"Evicted texture pixels never overwritten")
	expect(pixels(shown_b)==b.diffuse_texture.source.get_data(),"Other retained owner B pixels preserved")
	var uploads:int=presenter.uploads
	presenter.begin_draw(one)
	expect(presenter.acquire(one,c)==shown_c and presenter.uploads==uploads,"Repeated pose cache hit without upload")
	var overflow:Texture2D=presenter.acquire(one,a)
	expect(presenter.spills.size()==1 and presenter.cache_bytes==512,"All-held overflow preserves cache budget")
	expect(pixels(overflow)==a.diffuse_texture.source.get_data(),"Overflow pose pixels")
	expect(pixels(shown_b)==b.diffuse_texture.source.get_data() and pixels(shown_c)==c.diffuse_texture.source.get_data(),"Overflow preserves held poses")
	presenter.begin_draw(one);presenter.finish_frame()
	expect(presenter.spills.is_empty(),"Unused spill released after frame")
	var oversized:Texture2D=presenter.acquire(one,big)
	expect(presenter.cache_bytes==512 and presenter.spills.size()==1,"Oversized pose uses independent spill")
	expect(pixels(oversized)==big.diffuse_texture.source.get_data(),"Oversized pixels unchanged")
	presenter.begin_draw(one);presenter.begin_draw(two);presenter.finish_frame()
	presenter.cache_byte_limit=1024
	presenter.acquire(one,a)
	expect(presenter.slots.size()==2 and presenter.cache_bytes==512,"Entry-count bound with spare byte budget")
	uploads=presenter.uploads
	expect(presenter.acquire(two,c)==shown_c and presenter.uploads==uploads,"Least recently used free pose evicted")
	presenter.release_owner(one.get_instance_id());presenter.release_owner(two.get_instance_id())
	expect(presenter.cache_bytes==0 and presenter.slots.is_empty() and presenter.spills.is_empty() and presenter.owners.is_empty(),"Final owner releases all cache resources")
	FileAccess.open("user://lease-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"debug":OS.is_debug_build(),"scope":"Native GPU texture byte equality and manual two-owner lease/cache branches; not actual canvas routing, room motion or FPS acceptance"}))
	print("test_crew_pose_cache: ",checks," checks, ",failures," failures");quit(0 if failures==0 else 3)
