extends SceneTree
const Geometry = preload("res://tools/modular_room_geometry.gd")
class Guide extends Node2D:
	func cabinet(rect: Rect2, height: float) -> void:
		draw_rect(rect,Color("515761"))
		draw_rect(Rect2(rect.position-Vector2(0,height),rect.size),Color("dfd5c0"))
	func _draw() -> void:
		draw_rect(Rect2(0,0,1280,1280),Color("161d27"))
		draw_set_transform(Vector2(640,640),0,Vector2(2.75,2.75))
		draw_rect(Rect2(-192,-192,384,384),Color("303640"))
		for side in range(4):
			var edge := {"center":Vector2(Geometry.DIRS[side])*192,"horizontal":side%2==0,"open":true}
			for rect in Geometry.wall_rects(edge): draw_rect(rect,Color("dfd5c0"))
		for y in [-105.0,105.0]:
			cabinet(Rect2(-165,y-46,108,92),18)
			for x in [-140.0,-83.0]:
				draw_circle(Vector2(x,y-18),21,Color("252d34"))
				draw_circle(Vector2(x,y-18),7,Color("71969a"))
		cabinet(Rect2(57,-151,108,78),12)
		for x in [82.0,137.0]:
			draw_circle(Vector2(x,-124),20,Color("6b929c"))
		cabinet(Rect2(58,67,104,84),18)
		draw_rect(Rect2(72,60,72,31),Color("28383f"))
		draw_rect(Rect2(72,105,72,16),Color("7e9591"))
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size = Vector2i(1280,1280)
	root.content_scale_size = Vector2i(1280,1280)
	var guide := Guide.new()
	root.add_child(guide)
	await process_frame
	await RenderingServer.frame_post_draw
	var out := "res://output/whole-room-pilot-01/life-support-guide.png"
	assert(not FileAccess.file_exists(out),"Preserve existing guide")
	assert(root.get_texture().get_image().save_png(out)==OK)
	print("LIFE SUPPORT GUIDE: 384 cell, 16 wall, four 96-unit openings; art guide only")
	quit()
