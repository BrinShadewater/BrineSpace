extends SceneTree
const Kit=preload("res://assets/wall-dressing-v2/wall_sprites.gd")
func _init() -> void: call_deferred("run")
class Canvas extends Node2D:
	var layouts:=false
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,960),Color("172930"))
		draw_string(ThemeDB.fallback_font,Vector2(24,34),"BRINESPACE / WALL DECORATIONS / SECOND COLLECTION",HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color("c8d1c3"))
		if layouts:
			var row:=0
			for name in Kit.data().layouts:
				draw_string(ThemeDB.fallback_font,Vector2(80,92+row*250),name.to_upper()+" / 48-unit riser / central door bay reserved",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color("b5c4bc"))
				draw_set_transform(Vector2(640,175+row*250+216*2.4),0,Vector2.ONE*2.4)
				draw_rect(Rect2(-192,-240,384,48),Color("3e535b"))
				for x in range(-192,192,48): draw_rect(Rect2(x+2,-238,44,44),Color("475e65"),false,1)
				draw_rect(Rect2(-192,-244,384,4),Color("7b8c85"))
				draw_rect(Rect2(-192,-192,384,4),Color("1e343d"))
				draw_rect(Rect2(-34,-240,68,48),Color("233840"))
				Kit.draw_layout(self,name)
				draw_set_transform(Vector2.ZERO)
				row+=1
			return
		var i:=0
		for id in Kit.catalog():
			var origin:=Vector2(14+(i%3)*421,64+(i/3)*219)
			draw_rect(Rect2(origin,Vector2(402,205)),Color("344a53"))
			draw_line(origin+Vector2(221,46),origin+Vector2(221,172),Color("263b44"),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(10,25),id,HORIZONTAL_ALIGNMENT_LEFT,-1,15,Color("d0d5c8"))
			Kit.draw(self,id,origin+Vector2(111,114),2)
			Kit.draw(self,id,origin+Vector2(312,114),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(97,189),"2x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("99afa7"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(299,189),"1x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("99afa7"))
			i+=1
func run() -> void:
	assert(Kit.catalog().size()==12)
	for id in Kit.catalog():
		var spec: Dictionary=Kit.catalog()[id]
		assert(Kit.texture(id).get_size()==Vector2(spec.size[0],spec.size[1]))
		assert(Kit.size(id).y<=40 and spec.layer=="wall_attachment")
	for name in Kit.data().layouts:
		for item in Kit.data().layouts[name]:
			var dimensions:=Kit.size(item[0])
			var bounds:=Rect2(Vector2(item[1],item[2])-dimensions*0.5,dimensions)
			assert(Rect2(-192,-240,384,48).encloses(bounds))
			assert(not Rect2(-34,-246,68,58).intersects(bounds))
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1280,960)
		root.content_scale_size=Vector2i.ZERO
		var canvas:=Canvas.new()
		canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(canvas)
		for layout_mode in [false,true]:
			canvas.layouts=layout_mode
			canvas.queue_redraw()
			for frame in range(4): await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://assets/wall-dressing-v2/"+("wall-layouts.png" if layout_mode else "preview.png"))
	print("WALL DRESSING PASS: 12 textures, native 1x/2x preview, 3 wall layouts, riser and hatch-bay bounds")
	quit()
