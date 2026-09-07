extends SceneTree
const Kit=preload("res://assets/floor-dressing-v1/floor_dressing.gd")
func _init() -> void: call_deferred("run")
class Canvas extends Node2D:
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,960),Color("18292f"))
		draw_string(ThemeDB.fallback_font,Vector2(24,34),"BRINESPACE / REUSABLE ROOM FLOOR DRESSING",HORIZONTAL_ALIGNMENT_LEFT,-1,23,Color("ced3c5"))
		var i:=0
		for id in Kit.catalog():
			var origin:=Vector2(12+(i%4)*317,62+(i/4)*218)
			draw_rect(Rect2(origin,Vector2(305,204)),Color("34464c"))
			draw_line(origin+Vector2(10,90),origin+Vector2(295,90),Color("293d44"),1)
			draw_line(origin+Vector2(155,43),origin+Vector2(155,174),Color("293d44"),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(10,22),id,HORIZONTAL_ALIGNMENT_LEFT,-1,13,Color("d0d3c3"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(10,40),Kit.catalog()[id].department.to_upper(),HORIZONTAL_ALIGNMENT_LEFT,-1,11,Color("94aaa3"))
			Kit.draw(self,id,origin+Vector2(85,116),2)
			Kit.draw(self,id,origin+Vector2(233,116),1)
			draw_string(ThemeDB.fallback_font,origin+Vector2(74,190),"2x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("9aaea5"))
			draw_string(ThemeDB.fallback_font,origin+Vector2(221,190),"1x",HORIZONTAL_ALIGNMENT_LEFT,-1,12,Color("9aaea5"))
			i+=1
func run() -> void:
	assert(Kit.catalog().size()==16)
	for id in Kit.catalog():
		var spec: Dictionary=Kit.catalog()[id]
		assert(spec.layer=="floor_under_actors" and not spec.collision)
		assert(Kit.texture(id).get_size()==Vector2(spec.size[0],spec.size[1]))
		assert(Kit.size(id).x>=30 and Kit.size(id).x<=70)
	if DisplayServer.get_name()!="headless":
		root.size=Vector2i(1280,960)
		root.content_scale_size=Vector2i.ZERO
		var canvas:=Canvas.new()
		canvas.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		root.add_child(canvas)
		for frame in range(4): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://assets/floor-dressing-v1/preview.png")
	print("FLOOR DRESSING PASS: 16 textures, floor metadata, suggested scale bounds, native 1x/2x review")
	quit()
