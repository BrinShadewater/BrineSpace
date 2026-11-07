extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const DB=preload("res://scripts/room_database.gd")
const Kit=preload("res://assets/floor-kit-v6/installed_floor.gd")
const Baker=preload("res://tools/bake_whole_room_card.gd")
const CorridorBaker=preload("res://tools/bake_corridor_variants.gd")
var OUT="res://assets/floor-kit-v6/cards/"
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output-dir="): OUT=arg.trim_prefix("--output-dir=").trim_suffix("/")+"/"
	assert(OUT.begins_with("res://assets/"),"Card output must stay in the asset tree")
	call_deferred("run")
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	root.transparent_bg=true
	var grid:=Grid.new()
	grid.hide()
	grid.process_mode=Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	var records: Array=[]
	for id in DB.all_rooms():
		var entry: Dictionary=DB.get_room(id)
		var card
		var before:=Kit.draws
		if grid._is_narrow_corridor(entry):
			card=CorridorBaker.Card.new()
			card.textures=CorridorBaker.Art.load_sources()
			card.corner=id=="corner"
			card.tee=id=="tee_corridor"
		else:
			card=Baker.Card.new()
			card.room=grid._bill_room_view(entry)
			assert(card.room!=null)
		card.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(card)
		await process_frame
		await RenderingServer.frame_post_draw
		if grid._is_narrow_corridor(entry) or Kit.draws>before or not preload("res://rooms/whole-room/room_floor.gd").profile_for(card.room).is_empty():
			var path: String=OUT+id+".png"
			assert(not FileAccess.file_exists(path),"Preserve previous cards")
			assert(root.get_texture().get_image().save_png(path)==OK)
			records.append({"id":id,"path":path,"sha256":FileAccess.get_sha256(path)})
		card.queue_free()
		await process_frame
	var file:=FileAccess.open(OUT+"manifest.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"	"))
	print("FLOOR CARD PASS: ",records.size()," affected live room views, sealed offline cards")
	quit()

