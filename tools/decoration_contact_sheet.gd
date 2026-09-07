extends SceneTree
class Sheet extends Node2D:
	var entries: Array=[]
	var textures: Array=[]
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,570),Color("15232b"))
		for i in entries.size():
			var at:=Vector2((i%5)*256,(i/5)*282)
			draw_texture_rect(textures[i],Rect2(at,Vector2(256,256)),false)
			draw_string(ThemeDB.fallback_font,at+Vector2(8,274),entries[i].id,HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("cfddd5"))
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1280,570)
	root.content_scale_size=root.size
	var rows: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/decoration-integration/rooms.json"))
	var sheet:=Sheet.new()
	sheet.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(sheet)
	for page in range(4):
		sheet.entries=rows.slice(page*10,page*10+10)
		sheet.textures.clear()
		for entry in sheet.entries:
			var image:=Image.new()
			assert(image.load_png_from_buffer(FileAccess.get_file_as_bytes(entry.card))==OK)
			sheet.textures.append(ImageTexture.create_from_image(image))
		sheet.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png("res://output/decoration-integration/overview-%d.png"%page)==OK)
	quit()
