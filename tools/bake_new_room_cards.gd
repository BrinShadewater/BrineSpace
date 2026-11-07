extends SceneTree
const Preview=preload("res://tools/bake_room_cards_v2.gd").Preview
const Views=preload("res://rooms/new-room-expansion/views.gd")
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(512,512);root.content_scale_size=root.size;root.transparent_bg=true
	var preview:=Preview.new();preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	DirAccess.make_dir_recursive_absolute("res://assets/new-room-cards")
	var selected:PackedStringArray=[]
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--rooms="):selected=arg.trim_prefix("--rooms=").split(",")
	var count:=0
	for id in Views.PATHS:
		if not selected.is_empty() and id not in selected:continue
		count+=1
		var room=load(Views.PATHS[id]).new();room.embedded=true;room.hide();root.add_child(room)
		preview.id=id;preview.room=room;preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var error:=root.get_texture().get_image().save_png("res://assets/new-room-cards/%s.png"%id)
		if error!=OK:push_error("Card save failed: "+id);quit(1);return
		room.queue_free()
	print("NEW ROOM CARDS: %d baked"%count)
	quit()
