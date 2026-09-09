extends SceneTree
const New=preload("res://assets/wall-dressing-style-v1/wall_sprites.gd")
const Old1=preload("res://assets/wall-dressing-v1/wall_sprites.gd")
const Old2=preload("res://assets/wall-dressing-v2/wall_sprites.gd")
const IDS=["digital_clock","com_panel","poster_diver","poster_marine","oxygen_masks","pressure_gauge"]
func _init() -> void: call_deferred("run")
class Canvas extends Node2D:
	var reference_textures: Array[Texture2D]=[]
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,900),Color("172930"))
		draw_string(ThemeDB.fallback_font,Vector2(24,32),"BRINESPACE / STYLE CORRECTIONS / ORIGINAL LEFT, REVISED RIGHT",HORIZONTAL_ALIGNMENT_LEFT,-1,20,Color("c8d1c3"))
		var i:=0
		for id in IDS:
			var origin:=Vector2(24+(i%3)*418,70+(i/3)*260)
			draw_rect(Rect2(origin,Vector2(400,240)),Color("344a53"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(12,28),id,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("c8d1c3"))
			if Old1.catalog().has(id): Old1.draw(self,id,origin+Vector2(105,135),3)
			else: Old2.draw(self,id,origin+Vector2(105,135),3)
			New.draw(self,id,origin+Vector2(295,135),3)
			i+=1
		draw_string(ThemeDB.fallback_font,Vector2(24,630),"ROOM REFERENCES / materials and visual hierarchy, not wall-mounting approval",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("c8d1c3"))
		var x:=24
		for path in ["res://rooms/whole-room/crew-hab-card-activity-v1.png","res://rooms/underwater/corner-card-dressing-v2-0.png"]:
			var im:=Image.new()
			if im.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK: push_error("Failed to load image (assets/wall-dressing-style-v1/compare.gd:25)")
			var tex:=ImageTexture.create_from_image(im)
			reference_textures.append(tex)
			draw_texture_rect(tex,Rect2(x,648,230,230),false)
			x+=250
func run() -> void:
	root.size=Vector2i(1280,900)
	root.content_scale_size=Vector2i.ZERO
	var canvas:=Canvas.new()
	canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(canvas)
	for frame in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://assets/wall-dressing-style-v1/comparison.png")
	print("STYLE COMPARISON: six same-height before/after pairs and two room references")
	quit()
