extends SceneTree
const Scope=preload("res://scripts/session_art_cache.gd")
const Shell=preload("res://rooms/whole-room/painted_shell.gd")
const Windows=preload("res://rooms/whole-room/ocean_windows.gd")
const Risers=preload("res://rooms/whole-room/riser_catalog.gd")
const Walls=preload("res://rooms/whole-room/department_wall_material.gd")
const Grain=preload("res://rooms/whole-room/room_floor.gd")
var checks:=0
var failures:=0
class Surface extends Node2D:
	var images:Array=[]
	func _draw():
		for index in images.size():draw_texture_rect(images[index],Rect2((index%2)*256,(index/2)*256,256,256),false)
func _init():call_deferred("run")
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func populate(surface):
	var shell_path:String=Shell.catalog().reactor.base.source
	var riser_group:String=Risers.catalog().keys()[0]
	surface.images=[Shell.png(shell_path),Windows.texture("porthole"),Risers.texture(riser_group),Walls.texture("engineering")]
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace("\\","/"):
		push_error("Material cache test requires isolated user directory");quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	var capture:=SubViewport.new();capture.size=Vector2i(512,512);capture.transparent_bg=true
	capture.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(capture)
	for filter_value in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
		var first:=Surface.new();first.texture_filter=filter_value;capture.add_child(first);Scope.retain(first);populate(first)
		var second:=Node.new();root.add_child(second);Scope.retain(second)
		var refs:Array=[]
		for image in first.images:refs.append(weakref(image))
		await frame();var pixels:Image=capture.get_texture().get_image()
		check(not pixels.is_invisible(),"Material art visible")
		second.queue_free();await frame()
		check(not Shell.textures.is_empty() and not Windows.textures.is_empty(),"Live owner protects material images")
		check(pixels.get_data()==capture.get_texture().get_image().get_data(),"Closing overlapping owner preserves material pixels")
		first.queue_free();first=null;await frame()
		check(Shell.textures.is_empty() and Windows.textures.is_empty() and Risers.textures.is_empty() and Walls.textures.is_empty(),"All four material factories cleared")
		for ref in refs:check(ref.get_ref()==null,"Material images released")
		first=Surface.new();first.texture_filter=filter_value;capture.add_child(first);Scope.retain(first);populate(first);await frame()
		check(pixels.get_data()==capture.get_texture().get_image().get_data(),"Reloaded material pixels exact")
		first.queue_free();first=null;await frame()
	capture.queue_free();await frame()
	print("SESSION MATERIAL CACHE: %d checks; %d failures"%[checks,failures]);quit(1 if failures else 0)
