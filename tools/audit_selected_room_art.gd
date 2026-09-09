extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const DB=preload("res://scripts/room_database.gd")
class Preview extends Node2D:
	var room
	var id: String
	var foundation: Texture2D
	var q:=0
	func _draw() -> void:
		draw_rect(Rect2(0,0,760,900),Color("12282e"))
		draw_set_transform(Vector2(380,410),0,Vector2.ONE*1.5)
		draw_texture_rect_region(foundation,Rect2(-192,181.632,384,384.0*596/1934),Rect2(25,138,1934,596),Color(.72,.78,.80))
		room.configure_embedded(q,[],false,0.0)
		room.render_into(self,Vector2(380,410),1.5,true)
		draw_set_transform(Vector2(380,410),0,Vector2.ONE*1.5)
		preload("res://rooms/whole-room/north_wall.gd").draw_into(self,id,Vector2i.ZERO,false,false,room)
		room.render_into(self,Vector2(380,410),1.5,false,false)
		draw_string(ThemeDB.fallback_font,Vector2(50,875),id.replace("_"," ").capitalize(),HORIZONTAL_ALIGNMENT_LEFT,-1,26,Color("c1cec7"))
func wall_owner(view) -> String:
	var source: Script=view.get_script()
	while source!=null:
		if source.source_code.contains("\nfunc draw_wall("): return source.resource_path
		source=source.get_base_script()
	return "MISSING"
func _init() -> void: call_deferred("run")
func run() -> void:
	var output_dir: String="res://output/room-art-audit"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): output_dir=arg.trim_prefix("--output=")
	preload("res://scripts/room_layout_store.gd").path=output_dir+"/no-owner-overrides.json"
	preload("res://scripts/room_layout_store.gd").loaded=true
	preload("res://scripts/room_layout_store.gd").data={}
	root.size=Vector2i(760,900)
	root.content_scale_size=root.size
	var grid:=Grid.new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var preview:=Preview.new()
	var im:=Image.new()
	assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://rooms/foundation-v1/foundation-silt-v1.png"))==OK)
	preview.foundation=ImageTexture.create_from_image(im)
	root.add_child(preview)
	DirAccess.make_dir_recursive_absolute(output_dir)
	var manifest: Array=[]
	for id in DB.all_rooms():
		if id not in ["corridor","corner","tee_corridor"]: manifest.append({"room":id})
	var report: Array=[]
	for entry in manifest:
		preview.id=entry.room
		preview.room=grid._bill_room_view(DB.get_room(entry.room))
		var row: Dictionary={"room":entry.room,"view":preview.room.get_script().resource_path,"wall_renderer":wall_owner(preview.room),"layered":grid._uses_layered_art(DB.get_room(entry.room)),"floor_profile":preload("res://rooms/whole-room/room_floor.gd").profile_for(preview.room),"rotations":[]}
		for q in range(4):
			preview.q=q
			preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			assert(root.get_texture().get_image().save_png(output_dir+"/%s-q%d.png"%[entry.room,q])==OK)
			var props: Array=[]
			for prop in preview.room.props: props.append({"id":str(prop.id),"registered":prop.has("registration"),"full_wall":prop.get("full_wall",false),"side_view":prop.get("side_view","")})
			row.rotations.append({"quarter":q,"props":props})
		report.append(row)
	var audit_file:=FileAccess.open(output_dir+"/runtime.json",FileAccess.WRITE)
	audit_file.store_string(JSON.stringify(report,"\t")); audit_file.close()
	print("ARCHITECTURE REVIEW: %d rooms, four rotations, native risers and foundation"%manifest.size()+"")
	quit()

