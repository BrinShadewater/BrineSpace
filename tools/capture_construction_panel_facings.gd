extends SceneTree
## Native component fixture: four actual placement centers, one draw/bounds path.
const View = preload("res://rooms/production-ten/construction_drone_bay_view.gd")
class Preview extends Node2D:
	var room
	var placements: Array
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("34474b"))
		draw_set_transform(Vector2(256,256),0,Vector2.ONE)
		draw_line(Vector2(-180,0),Vector2(180,0),Color("71817e"))
		draw_line(Vector2(0,-180),Vector2(0,180),Color("71817e"))
		for prop in placements:
			var bounds: Rect2=room._panel_bounds(prop)
			draw_texture_rect(room._panel_texture(prop),bounds,false)
			draw_rect(bounds,Color("81968c"),false,1)
		draw_circle(Vector2.ZERO,4,Color("b9c8bf"))
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(512,512)
	root.content_scale_size=root.size
	var room=View.new()
	var preview=Preview.new()
	preview.room=room
	var report: Array=[]
	for center in [Vector2(0,-140),Vector2(140,0),Vector2(0,140),Vector2(-140,0)]:
		var prop={"id":"construction_panels","rect":Rect2(center-Vector2(45,32),Vector2(90,64))}
		preview.placements.append(prop)
		var bounds: Rect2=room._panel_bounds(prop)
		assert(bounds.size.x<=90.01 and bounds.size.y<=80.13)
		report.append({"center":[center.x,center.y],"facing":room._panel_facing(prop),"bounds":[bounds.position.x,bounds.position.y,bounds.size.x,bounds.size.y]})
	root.add_child(preview)
	await process_frame
	await RenderingServer.frame_post_draw
	var folder="res://output/construction-owner-repair-2026-09-12/panel-facings"
	DirAccess.make_dir_recursive_absolute(folder)
	assert(root.get_texture().get_image().save_png(folder+"/facings.png")==OK)
	var file=FileAccess.open(folder+"/review.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t")); file.close()
	room.free()
	quit()
