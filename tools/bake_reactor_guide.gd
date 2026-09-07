extends "res://tools/bake_life_support_guide.gd"
class ReactorGuide extends Guide:
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,1280),Color("161d27"))
		draw_set_transform(Vector2(640,640),0,Vector2(2.75,2.75))
		draw_rect(Rect2(-192,-192,384,384),Color("303640"))
		for side in range(4):
			var edge := {"center":Vector2(Geometry.DIRS[side])*192,"horizontal":side%2==0,"open":true}
			for rect in Geometry.wall_rects(edge): draw_rect(rect,Color("dfd5c0"))
		cabinet(Rect2(-52,-40,104,80),28)
		draw_circle(Vector2(0,-28),40,Color("d9d0b9"))
		draw_circle(Vector2(0,-28),34,Color("70563b"))
		draw_circle(Vector2(0,-28),20,Color("b28a51"))
		cabinet(Rect2(-164,-150,70,48),14)
		draw_rect(Rect2(-152,-153,46,29),Color("35434b"))
		cabinet(Rect2(94,107,70,46),14)
		draw_rect(Rect2(104,103,50,22),Color("35434b"))
func run() -> void:
	root.size = Vector2i(1280,1280)
	root.content_scale_size = Vector2i(1280,1280)
	root.add_child(ReactorGuide.new())
	await process_frame
	await RenderingServer.frame_post_draw
	var out := "res://output/whole-room-pilot-01/reactor-guide-v2.png"
	assert(not FileAccess.file_exists(out))
	assert(root.get_texture().get_image().save_png(out)==OK)
	print("REACTOR GUIDE: central chamber, perimeter circulation, four canonical doors; guide only")
	quit()
