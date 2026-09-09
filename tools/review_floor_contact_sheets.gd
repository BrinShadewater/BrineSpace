extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1200,1680)
	root.content_scale_size=root.size
	var rows: Array=JSON.parse_string(FileAccess.get_file_as_string("res://assets/floor-details-v3/cards/manifest.json"))
	for page in range(ceili(rows.size()/12.0)):
		var group:=Node2D.new()
		root.add_child(group)
		for offset in range(12):
			var index:=page*12+offset
			if index>=rows.size(): break
			var item: Dictionary=rows[index]
			var im:=Image.new()
			assert(im.load_png_from_buffer(FileAccess.get_file_as_bytes(item.path))==OK)
			var sprite:=Sprite2D.new()
			sprite.texture=ImageTexture.create_from_image(im)
			sprite.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
			sprite.scale=Vector2.ONE*.75
			sprite.position=Vector2(200+(offset%3)*400,198+(offset/3)*420)
			group.add_child(sprite)
			var label:=Label.new()
			label.text=item.id
			label.position=sprite.position+Vector2(-180,188)
			group.add_child(label)
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png("res://output/floor-details-v3/contact-%d.png"%page)==OK)
		group.queue_free()
		await process_frame
	print("FLOOR CONTACT SHEETS: ",rows.size()," current selected cards at 384-pixel width")
	quit()
