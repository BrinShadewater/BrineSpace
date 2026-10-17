extends SceneTree
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	OS.set_environment("BRINE_SILENT","1")
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"),true)
	var primary:int=DisplayServer.get_primary_screen()
	for screen in DisplayServer.get_screen_count():
		var extent:Vector2i=DisplayServer.screen_get_size(screen)
		if screen!=primary and extent.x>=1920 and extent.y>=1080:
			root.current_screen=screen;root.position=DisplayServer.screen_get_position(screen)+Vector2i(100,100)
			break
	root.set_disable_input(true)
	var motion=load("res://scripts/drone_animation.gd")
	var session=load("res://scripts/session_art_cache.gd")
	var owner:=Node.new();root.add_child(owner);session.retain(owner)
	var path:="res://assets/mining-rover-v1-2026-09-26/completion/atlases/empty-120.png"
	var original:Texture2D=motion.texture(path)
	check(original.get_meta("drone_invisible",false) and original.get_size()==Vector2.ONE,"Verified blank atlas collapses to one transparent pixel")
	var pixels:PackedByteArray=original.get_image().get_data()
	var held:WeakRef=weakref(original);original=null
	var uploads:int=motion.texture_uploads
	var pressure:=Image.create(1024,1024,false,Image.FORMAT_RGBA8);pressure.fill(Color(.2,.3,.4,1))
	motion.last_used[path]=-100
	for i in range(65):
		var key:String="fixture-pressure-%d"%i
		motion.cache_image(key,pressure,false);motion.last_used[key]=-100
	check(not motion.textures.has(path),"Real cache pressure evicts regular lookup ownership")
	check(held.get_ref()!=null,"Bounded transparent ownership survives eviction")
	var prior:int=motion.texture_uploads
	check(motion.ready(path),"Blank layer is ready without another decode job")
	check(not motion.image_jobs.has(path),"No repeated PNG decode")
	var restored:Texture2D=motion.texture(path)
	check(motion.texture_uploads==prior,"No repeated transparent upload")
	check(is_same(restored,held.get_ref()),"Retain original immutable texture identity")
	check(restored.get_image().get_data()==pixels,"Restored pixels exact")
	restored=null
	var blank:=Image.create(1,1,false,Image.FORMAT_RGBA8)
	for i in range(70):motion.cache_image("fixture-blank-%d"%i,blank,true)
	var tiny=motion.get("invisible_images")
	check(tiny is Dictionary and tiny.size()<=64,"Transparent ownership is bounded")
	tiny=null
	owner.queue_free();await process_frame;await RenderingServer.frame_post_draw
	check(motion.textures.is_empty() and motion.image_jobs.is_empty() and motion.cached_bytes==0,"Scene release clears ordinary cache and workers")
	check(held.get_ref()==null,"Scene release frees retained transparent image")
	var remaining=motion.get("invisible_images")
	check(remaining is Dictionary and remaining.is_empty(),"Scene release clears bounded transparent ownership")
	FileAccess.open("user://invisible-cache.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("INVISIBLE_CACHE ",checks," checks; ",failures," failures");quit(1 if failures else 0)
