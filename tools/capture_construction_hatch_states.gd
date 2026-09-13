extends SceneTree
const View=preload("res://rooms/production-ten/construction_drone_bay_view.gd")
class Preview extends Node2D:
	var room
	func _draw() -> void:
		draw_rect(Rect2(0,0,600,450),Color("34474b"))
		var centers=[Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]
		for col in range(4):
			var prop={"id":"construction_hatch","rect":Rect2(centers[col]-Vector2(45,32),Vector2(90,64))}
			var b: Rect2=room._hatch_bounds(prop)
			assert(b.size.x<=90.01 and b.size.y<=78.47)
			for row in range(3):
				draw_set_transform(Vector2(75+150*col,75+150*row)-b.get_center(),0,Vector2.ONE)
				room._draw_overhead_hatch(self,prop,row*0.5)
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(600,450); root.content_scale_size=root.size
	var room=View.new(); var preview=Preview.new(); preview.room=room; root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/construction-owner-repair-2026-09-12/hatch-states"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/states.png")==OK)
	room.free(); quit()
