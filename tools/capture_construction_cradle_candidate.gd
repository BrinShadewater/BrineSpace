extends SceneTree
const Art=preload("res://scripts/drone_art.gd")
class Preview extends Node2D:
	var textures: Array=[]
	func _draw() -> void:
		draw_rect(Rect2(0,0,600,300),Color("34474b"))
		for col in range(4):
			var size=Vector2(textures[col].get_size())
			size*=minf(90.0/size.x,(90.0*320.0/370.0)/size.y)
			for row in range(2):
				var center=Vector2(75+150*col,85+150*row)
				draw_texture_rect(textures[col],Rect2(center-size*0.5,size),false)
				if row==1: Art.draw_drone(self,"construction",center-Vector2(0,15),70,0,false,false)
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(600,300); root.content_scale_size=root.size
	var preview=Preview.new()
	for facing in ["down","left","up","right"]:
		preview.textures.append(Art._decode_matte("res://assets/rooms/construction-drone-bay/material/cradle-square-%s.png"%facing))
	root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/construction-owner-repair-2026-09-12/cradle-square"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/empty-docked.png")==OK)
	quit()
