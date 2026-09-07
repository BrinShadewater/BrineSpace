extends SceneTree
const Art = preload("res://rooms/underwater/corridor_surfaces.gd")
const Geometry = preload("res://rooms/underwater/corridor_geometry.gd")
class Card extends Node2D:
	var textures: Array
	var corner := false
	func _draw() -> void:
		draw_rect(Rect2(0,0,512,512),Color("09222d"))
		draw_set_transform(Vector2(256,256),0,Vector2.ONE*1.16)
		var q := 0 if corner else 1
		Art.draw_hull(self,Geometry.hull_for(corner),Geometry.floor_for(corner),Vector2.ZERO,q,textures,corner,true)
		for p in ([Vector2(-192,0),Vector2(0,192)] if corner else [Vector2(0,-192),Vector2(0,192)]):
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
	for corner in [false,true]:
		card.corner = corner
		card.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var path := "res://rooms/underwater/%s-card-%s.png"%[("corner" if corner else "corridor"),suffix]
		assert(not FileAccess.file_exists(path),"Preserve earlier card exports")
		assert(root.get_texture().get_image().save_png(path)==OK)
	print("UNDERWATER CARDS: two 512px sealed-end cards using production geometry and surfaces")
	quit()
