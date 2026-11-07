extends SceneTree
## Bounded Crew notice rail strip-fit diagnostic, not runtime attachment.
const Geometry = preload("res://tools/modular_room_geometry.gd")
class Board extends Node2D:
	var texture: Texture2D
	var region: Rect2
	var fitted_width: float
	func _draw() -> void:
		draw_rect(Rect2(0,0,1000,500),Color("203238"))
		draw_string(ThemeDB.fallback_font,Vector2(24,32),"Notice rail: measured low-strip fit (not installed)",HORIZONTAL_ALIGNMENT_LEFT,-1,22)
		draw_string(ThemeDB.fallback_font,Vector2(24,67),"Native 1 px/world unit: 16-unit host strip, 14-unit accessory",HORIZONTAL_ALIGNMENT_LEFT,-1,16)
		for i in range(2):
			var factor := 1.0 if i==0 else 3.0
			var at := Vector2(30,100+i*150)
			draw_rect(Rect2(at,Vector2(250,16)*factor),Color("b0a99b"))
			draw_texture_rect_region(texture,Rect2(at+Vector2(5,1)*factor,Vector2(fitted_width,14)*factor),region)
		draw_string(ThemeDB.fallback_font,Vector2(24,228),"3x diagnostic: uniform scale, host margins visible",HORIZONTAL_ALIGNMENT_LEFT,-1,16)
		draw_string(ThemeDB.fallback_font,Vector2(24,420),"Host material shown schematically. Door gaps, mounting plane and depth ordering remain unverified.",HORIZONTAL_ALIGNMENT_LEFT,-1,16)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	assert(Geometry.WALL==16.0)
	var data=JSON.parse_string(FileAccess.get_file_as_string("res://assets/crew-notice-rail-v1/low-strip-fit.json"))
	var review=JSON.parse_string(FileAccess.get_file_as_string("res://assets/crew-notice-rail-v1/material-scale-review.json"))
	assert(FileAccess.get_sha256(data.asset)==review.export_sha256)
	var raw:=Image.new()
	assert(raw.load_png_from_buffer(FileAccess.get_file_as_bytes(data.asset))==OK)
	var board:=Board.new()
	board.texture=ImageTexture.create_from_image(raw)
	board.region=Rect2(data.region[0],data.region[1],data.region[2],data.region[3])
	board.fitted_width=data.width
	assert(is_equal_approx(board.fitted_width*board.region.size.y/board.region.size.x,14.0))
	root.size=Vector2i(1000,500)
	root.content_scale_size=root.size
	root.canvas_item_default_texture_filter=Viewport.DEFAULT_CANVAS_ITEM_TEXTURE_FILTER_NEAREST
	root.add_child(board)
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png("res://output/crew-notice-rail-v1/low-strip-fit.png")==OK)
	var script_path: String=get_script().resource_path
	if not FileAccess.file_exists(script_path+".uid"):
		var f:=FileAccess.open(script_path+".uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("NOTICE FIT PASS: 16-unit geometry, export hash, uniform 14-unit fitting; not runtime placement")
	quit()
