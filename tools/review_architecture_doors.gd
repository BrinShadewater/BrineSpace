extends SceneTree
const Door=preload("res://rooms/doors/painted_door.gd")
const OUT="res://assets/architecture-rollout-2026-09-26/motion"
class Preview extends Node2D:
	var phase:=0.0
	func _draw() -> void:
		draw_rect(Rect2(0,0,900,560),Color("203039"))
		var families=["default","operations","recreation","life_support","airlock","robotics","anomaly","science","engineering"]
		for i in range(families.size()):
			var skin=Door.for_variant(families[i])
			var at:=Vector2(100+(i%3)*300,70+(i/3)*175)
			skin.raised_at(self,phase,at.x,at.y,79)
			draw_string(ThemeDB.fallback_font,at+Vector2(-45,-20),families[i],HORIZONTAL_ALIGNMENT_LEFT,-1,15)
			for left in [true,false]:
				var width:=36.0*(1-phase)
				skin.low_leaf(self,Rect2(at+Vector2(-36 if left else 36-width,112),Vector2(width,12)),left,false,families[i])
func _init() -> void:call_deferred("run")
func run() -> void:
	root.size=Vector2i(900,560);root.content_scale_size=root.size
	DirAccess.make_dir_recursive_absolute(OUT)
	var preview:=Preview.new();root.add_child(preview)
	for i in range(19):
		preview.phase=float(i)/18;preview.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var error:=root.get_texture().get_image().save_png(OUT+"/doors-%02d.png"%i);assert(error==OK)
	for path in ["res://rooms/doors/painted_door.gd","res://rooms/doors/ocean_hatch.gd","res://rooms/whole-room/painted_shell.gd","res://tools/review_architecture_rollout.gd","res://tools/review_architecture_live.gd","res://tools/review_architecture_doors.gd"]:
		if FileAccess.file_exists(path+".uid"):continue
		var file:=FileAccess.open(path+".uid",FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close()
	print("DOOR MOTION: nine families, 19 native raised/low poses; UID pairs present")
	quit()
