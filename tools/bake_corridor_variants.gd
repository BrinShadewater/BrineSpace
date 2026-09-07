extends SceneTree
const Art = preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry = preload("res://rooms/underwater/corridor_geometry.gd")
class Card extends Node2D:
	var textures: Array
	var corner := false
	var tee := false
	var variant := 0
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("09222d"))
		draw_set_transform(Vector2(256,275),0,Vector2.ONE*1.05)
		var q := 0 if corner or tee else 1
		Art.draw_hull(self,Geometry.hull_for(corner,tee),Geometry.floor_for(corner,tee),Vector2.ZERO,q,textures,corner,true,-1.0,tee,variant)
		preload("res://rooms/underwater/corridor_dressing.gd").draw_risers(self,Geometry.hull_for(corner,tee),q,variant,1.0)
		preload("res://rooms/underwater/corridor_dressing.gd").draw_props(self,q,variant,1.0)
		for p in ([Vector2(-192,0),Vector2(192,0),Vector2(0,192)] if tee else [Vector2(-192,0),Vector2(0,192)] if corner else [Vector2(0,-192),Vector2(0,192)]):
			var size := Vector2(16,104) if p.x!=0 else Vector2(104,16)
			draw_rect(Rect2(p-size/2,size),Color("7f9290"))
			draw_rect(Rect2(p-size/2,size).grow(-2),Color("536967"))
var suffix := "v3"
func _init() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--suffix="): suffix=argument.trim_prefix("--suffix=")
	assert(suffix.is_valid_filename(),"Card suffix must be a filename component")
	call_deferred("run")
func run() -> void:
	root.size = Vector2i(512,512)
	root.content_scale_size = root.size
	var card := Card.new()
	card.textures = Art.load_sources()
	card.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	root.add_child(card)
	for id in ["corridor","corner","tee_corridor"]:
		for variant in range(3):
			card.corner=id=="corner"
			card.tee=id=="tee_corridor"
			card.variant=variant
			card.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var path := "res://rooms/underwater/%s-card-joins-v1-%d.png"%[id,variant]
			assert(not FileAccess.file_exists(path))
			assert(root.get_texture().get_image().save_png(path)==OK)
	print("CORRIDOR CARDS PASS: three shapes, three variants")
	quit()
