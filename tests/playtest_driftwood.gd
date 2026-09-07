extends SceneTree
class Sheet extends Control:
	var grounds: Array[Texture2D]=[]
	var prop: Texture2D
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		for panel in range(2):
			var origin:=Vector2(30+panel*790,90)
			draw_string(ThemeDB.fallback_font,origin-Vector2(0,30),["Clay silt / runtime tint","Volcanic ash / runtime tint"][panel],HORIZONTAL_ALIGNMENT_LEFT,-1,24)
			draw_texture_rect(grounds[panel],Rect2(origin,Vector2.ONE*720),false,Color(.49,.58,.57))
			for i in range(3):
				var side: float=[72.0,90.0,117.0][i]
				var at:=origin+Vector2(80+i*210,250)
				draw_texture_rect(prop,Rect2(at,Vector2.ONE*side),false,Color(.49,.58,.57,.9))
				draw_string(ThemeDB.fallback_font,at+Vector2(0,160),["0.40 cell","0.50 cell","0.65 cell"][i],HORIZONTAL_ALIGNMENT_LEFT,-1,20)
		draw_string(ThemeDB.fallback_font,Vector2(30,860),"One ground source spans four cells. Original prop pixels; no live placement implied.",HORIZONTAL_ALIGNMENT_LEFT,-1,20)
func _init() -> void:
	call_deferred("run")
func run() -> void:
	preload("res://scripts/title_settings.gd").initialized=true
	root.mode=Window.MODE_WINDOWED
	root.content_scale_size=Vector2i.ZERO
	root.size=Vector2i(1600,900)
	var sheet:=Sheet.new()
	sheet.size=root.size
	for path in ["res://assets/environment/clay-silt-v1/clay-silt-ground-v1.png","res://assets/environment/volcanic-ash-v1/ash-ground-v1.png"]:
		var source:=Image.new()
		assert(source.load(path)==OK)
		sheet.grounds.append(ImageTexture.create_from_image(source))
	var prop:=Image.new()
	assert(prop.load("res://assets/environment/driftwood-v1/waterlogged-timber-v1.png")==OK)
	assert(prop.detect_alpha()!=Image.ALPHA_NONE)
	sheet.prop=ImageTexture.create_from_image(prop)
	root.add_child(sheet)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var frame:=root.get_texture().get_image()
	assert(frame.get_size()==Vector2i(1600,900))
	DirAccess.make_dir_recursive_absolute("res://output/driftwood-v1")
	assert(frame.save_png("res://output/driftwood-v1/terrain-scale.png")==OK)
	print("DRIFTWOOD STUDY PASS: two grounds, three cell widths, alpha source, 1600x900 capture")
	quit()
