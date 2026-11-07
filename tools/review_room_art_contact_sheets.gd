extends SceneTree
class Sheet extends Node2D:
	var frames: Array=[]
	func _draw() -> void:
		draw_rect(Rect2(0,0,2400,1800),Color("0b1d25"))
		for i in range(frames.size()):
			draw_texture_rect(frames[i].texture,Rect2((i%8)*300,(i/8)*360,300,335),false)
			draw_string(ThemeDB.fallback_font,Vector2((i%8)*300+8,(i/8)*360+351),frames[i].label,HORIZONTAL_ALIGNMENT_LEFT,290,17,Color.WHITE)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(2400,1800); root.content_scale_size=root.size
	var sheet:=Sheet.new(); root.add_child(sheet)
	for q in range(4):
		sheet.frames.clear()
		for file in DirAccess.get_files_at("res://output/room-art-audit"):
			if not file.ends_with("-q"+str(q)+".png"): continue
			var im:=Image.new(); im.load_png_from_buffer(FileAccess.get_file_as_bytes("res://output/room-art-audit/"+file))
			sheet.frames.append({"texture":ImageTexture.create_from_image(im),"label":file.trim_suffix("-q"+str(q)+".png")})
		sheet.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/room-art-audit/contact-q"+str(q)+".png")
	print("CONTACT SHEETS PASS")
	quit()
