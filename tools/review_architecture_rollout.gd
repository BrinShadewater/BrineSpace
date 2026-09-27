extends SceneTree
const OUT="res://assets/architecture-rollout-2026-09-26/review"
const Store=preload("res://scripts/room_layout_store.gd")
class Preview extends Node2D:
	var room
	var id:String
	var q:=0
	var corridor_textures:Array=preload("res://rooms/underwater/corridor_surfaces.gd").load_sources()
	func _draw() -> void:
		var anchor:=Vector2(256,290)
		var zoom:=1.06
		room.configure_embedded(q,[],false,0)
		room.set_meta("raised_north_visible",true)
		if id not in ["corridor","corner","tee_corridor"]:room.render_into(self,anchor,zoom,true)
		draw_set_transform(anchor,0,Vector2.ONE*zoom)
		if id in ["corridor","corner","tee_corridor"]:
			var g=preload("res://rooms/underwater/corridor_geometry.gd")
			preload("res://rooms/underwater/corridor_surfaces.gd").draw_hull(self,g.hull_for(id=="corner",id=="tee_corridor"),g.floor_for(id=="corner",id=="tee_corridor"),Vector2.ZERO,g.rotation({"id":id,"rotation":q}),corridor_textures,id=="corner",true,1,id=="tee_corridor",0)
			preload("res://rooms/underwater/corridor_dressing.gd").draw_risers(self,g.hull_for(id=="corner",id=="tee_corridor"),g.rotation({"id":id,"rotation":q}),0,1)
		else:
			# Floor, complete shell, raised face, then room contents.
			room.shell_pass=1
			room.render_into(self,anchor,zoom,false,false)
			draw_set_transform(anchor,0,Vector2.ONE*zoom)
			preload("res://rooms/whole-room/north_wall.gd").draw_into(self,id,Vector2i.ZERO,false,false,room)
			room.shell_pass=2
			room.render_into(self,anchor,zoom,false,false)
			room.shell_pass=0
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":quit(2);return
	Store.ensure_loaded()
	root.size=Vector2i(512,512);root.content_scale_size=root.size;root.transparent_bg=true
	DirAccess.make_dir_recursive_absolute(OUT)
	var preview:=Preview.new();preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST;root.add_child(preview)
	var entries:Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/full-wall-v1/editor-catalog.json"))
	var cards=preload("res://scripts/room_card_art.gd")
	var count:=0
	var selected:PackedStringArray=[]
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--rooms="):selected=arg.trim_prefix("--rooms=").split(",")
	for entry in entries:
		if not selected.is_empty() and entry.room not in selected:continue
		var room=load(entry.view).new();room.embedded=true;room.hide();root.add_child(room)
		preview.id=entry.room;preview.room=room
		for q in range(4):
			preview.q=q;preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var im:=root.get_texture().get_image()
			var error:=im.save_png(OUT+"/%s-q%d.png"%[entry.room,q]);assert(error==OK)
			if q==0 and cards.PATHS.has(entry.room):
				error=im.save_png(cards.PATHS[entry.room]);assert(error==OK)
			count+=1
		room.queue_free();await process_frame
	print("ARCHITECTURE: ",count," native views; registered cards refreshed; owner layouts read-only")
	quit()
