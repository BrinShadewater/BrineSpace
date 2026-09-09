extends SceneTree
## Native catalog, using the same view lookup as the station; isolated from saves.
const Grid = preload("res://scripts/grid_canvas.gd")
const DB = preload("res://scripts/room_database.gd")
const Baker = preload("res://tools/bake_current_architecture_cards.gd")
const Corridors = preload("res://tools/bake_corridor_variants.gd")
var OUT = "res://output/room-catalog-2026-09-08/"
func _init() -> void: call_deferred("run")
func run() -> void:
	var layouts_path:=""
	var selected_rooms: PackedStringArray=[]
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--out="): OUT=argument.trim_prefix("--out=").trim_suffix("/")+"/"
		if argument.begins_with("--layouts="): layouts_path=argument.trim_prefix("--layouts=")
		if argument.begins_with("--rooms="): selected_rooms=argument.trim_prefix("--rooms=").split(",")
	preload("res://scripts/room_layout_store.gd").loaded=true
	preload("res://scripts/room_layout_store.gd").data={}
	if not layouts_path.is_empty():
		preload("res://scripts/room_layout_store.gd").data=JSON.parse_string(FileAccess.get_file_as_string(layouts_path)).layouts
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	DirAccess.make_dir_recursive_absolute(OUT+"images")
	var grid=Grid.new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var records: Array=[]
	for id in DB.all_rooms():
		if not selected_rooms.is_empty() and id not in selected_rooms: continue
		var data: Dictionary=DB.get_room(id)
		var row: Dictionary={"id":id,"name":data.display_name,"category":data.category,"layout":data.layout,"card_before":preload("res://scripts/room_card_art.gd").PATHS.get(id,""),"images":[],"views":[]}
		var preview
		var corridor: bool=grid._is_narrow_corridor(data)
		if corridor:
			preview=Corridors.Card.new()
			preview.textures=Corridors.Art.load_sources()
			preview.corner=id=="corner"
			preview.tee=id=="tee_corridor"
			row.view="res://rooms/underwater/corridor_surfaces.gd"
		else:
			preview=Baker.Preview.new()
			preview.compact=true
			preview.id=id
			preview.room=grid._bill_room_view(data)
			assert(preview.room!=null)
			row.view=preview.room.get_script().resource_path
		preview.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(preview)
		for q in range(1 if corridor or data.has("fixed_rotation") else 4):
			if not corridor: preview.q=q
			preview.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path: String=OUT+"images/%s-q%d.png"%[id,q]
			assert(root.get_texture().get_image().save_png(path)==OK)
			row.images.append(path)
			if not corridor:
				var props: Array=[]
				for prop in preview.room.props:
					props.append({"id":str(prop.id),"full_wall":prop.get("full_wall",false),"side_view":prop.get("side_view","")})
				row.views.append({"quarter":q,"props":props})
		preview.queue_free()
		await process_frame
		records.append(row)
	var file=FileAccess.open(OUT+"runtime.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"\t"))
	file.close()
	grid.queue_free()
	await process_frame
	print("ROOM CATALOG PASS: ",records.size()," live identities captured")
	quit()
