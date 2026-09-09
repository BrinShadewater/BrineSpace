extends SceneTree
class Sprite extends Node2D:
	var tex: ImageTexture
	var parts: Array=[]
	func _draw() -> void:
		for part in parts:
			var points:=PackedVector2Array()
			var uv:=PackedVector2Array()
			for p in part:
				points.append(Vector2(p[0],p[1]))
				uv.append(Vector2(p[0],p[1])/tex.get_size())
			draw_polygon(points,PackedColorArray([Color.WHITE]),uv,tex)
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1254,1254)
	root.content_scale_size=root.size
	root.transparent_bg=true
	for id in ["fridge-v2","rack-v2"]:
		var base: String="res://rooms/underwater/cold-store-v1/"+id
		var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(base+".json"))
		var im:=Image.new()
		preload("res://scripts/safe_image.gd").load_png(im, data.source)
		root.size=im.get_size()
		root.content_scale_size=root.size
		var sprite:=Sprite.new()
		sprite.tex=ImageTexture.create_from_image(im)
		sprite.parts=data.pieces
		root.add_child(sprite)
		await process_frame
		await RenderingServer.frame_post_draw
		assert(root.get_texture().get_image().save_png(base+".png")==OK)
		sprite.queue_free()
		await process_frame
	print("COLD STORE CUTOUTS PASS: two native transparent renders")
	quit()
