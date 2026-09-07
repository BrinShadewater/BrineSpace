extends "res://tools/bake_life_support_guide.gd"
class HydroGuide extends Guide:
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,1280),Color("161d27"))
		draw_set_transform(Vector2(640,640),0,Vector2(2.75,2.75))
		draw_rect(Rect2(-192,-192,384,384),Color("303640"))
		for side in range(4):
			var edge := {"center":Vector2(Geometry.DIRS[side])*192,"horizontal":side%2==0,"open":true}
			for rect in Geometry.wall_rects(edge): draw_rect(rect,Color("dfd5c0"))
		for x in [-163.0,57.0]:
			cabinet(Rect2(x,-145,106,78),16)
			for row in range(3):
				for column in range(4):
					draw_circle(Vector2(x+16+column*24,-148+row*23),8,Color("638754"))
		cabinet(Rect2(-160,75,98,78),18)
		draw_circle(Vector2(-135,96),17,Color("6d9da3"))
		draw_circle(Vector2(-88,96),17,Color("6d9da3"))
		cabinet(Rect2(60,88,104,64),19)
		draw_rect(Rect2(72,78,44,30),Color("66804c"))
		draw_rect(Rect2(125,79,24,22),Color("253e43"))
func run() -> void:
	root.size = Vector2i(1280,1280)
	root.content_scale_size = Vector2i(1280,1280)
	root.add_child(HydroGuide.new())
	await process_frame
	await RenderingServer.frame_post_draw
	var out := "res://output/whole-room-pilot-01/hydroponics-guide.png"
	assert(not FileAccess.file_exists(out))
	assert(root.get_texture().get_image().save_png(out)==OK)
	print("HYDROPONICS GUIDE: four south-facing assemblies, canonical cross shell; composition guide only")
	quit()
