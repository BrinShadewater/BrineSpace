extends SceneTree
const OUT="res://character/brine-slim-v14-2026-10-03/production-frames"
class Preview extends Node2D:
	var room
	var time:=0.0
	func _draw() -> void:
		room.configure_embedded(0,[],true,time)
		room.set_meta("raised_north_visible",true)
		room.render_into(self,Vector2(256,290),1.06,true)
		room.shell_pass=1;room.render_into(self,Vector2(256,290),1.06,false,false)
		draw_set_transform(Vector2(256,290),0,Vector2.ONE*1.06)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,"brine_core",Vector2i.ZERO,false,false,room)
		room.shell_pass=2;room.render_into(self,Vector2(256,290),1.06,false,false);room.shell_pass=0
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512);root.content_scale_size=root.size;root.transparent_bg=true
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	DirAccess.make_dir_recursive_absolute(OUT)
	var room=preload("res://rooms/underwater/brine-core/brine_core_view.gd").new();room.embedded=true;room.hide();root.add_child(room)
	var preview:=Preview.new();preview.room=room;preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	var motion=preload("res://rooms/underwater/brine-core/brine_float.gd")
	for i in range(201):
		var t:=i/25.0
		assert(motion.drift(Vector2(.3,.1),t).is_equal_approx(motion.drift(Vector2(.7,.1),t)),"Rigid face")
		assert(motion.drift(Vector2(.5,.35),t).is_equal_approx(motion.drift(Vector2(.5,.5),t)),"Rigid central torso")
	for uv in motion.uvs():
		assert(motion.drift(uv,0).is_equal_approx(motion.drift(uv,8)),"Loop position closes")
		var before:Vector2=(motion.drift(uv,8)-motion.drift(uv,7.999))/.001
		var after:Vector2=(motion.drift(uv,.001)-motion.drift(uv,0))/.001
		assert(before.distance_to(after)<.02,"Loop velocity closes")
	for i in range(200):
		preview.time=i/25.0;preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var error:=root.get_texture().get_image().save_png(OUT+"/frame-%03d.png"%i);assert(error==OK)
	for path in ["res://rooms/underwater/brine-core/brine_float.gd","res://character/brine-slim-v14-2026-10-03/production_preview.gd"]:
		if FileAccess.file_exists(path+".uid"):continue
		var f:=FileAccess.open(path+".uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));f.close()
	print("BRINE FLOAT: 200 native frames at 25 fps; production renderer and selected v14 body")
	quit()
