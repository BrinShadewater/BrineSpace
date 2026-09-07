extends SceneTree
class Sheet extends Control:
	var textures: Array[Texture2D] = []
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		var names := ["Red algae","Seagrass","Ribbon kelp"]
		for i in range(textures.size()):
			var at := Vector2(40+i*510,90)
			draw_string(ThemeDB.fallback_font,at-Vector2(0,30),names[i],HORIZONTAL_ALIGNMENT_LEFT,-1,24)
			draw_texture_rect(textures[i],Rect2(at,Vector2.ONE*360),false)
			for row in range(2):
				var origin := at+Vector2(0,430+row*140)
				draw_rect(Rect2(origin,Vector2(440,110)),Color("172b2d"))
				draw_string(ThemeDB.fallback_font,origin+Vector2(10,25),"Source" if row==0 else "Runtime tint",HORIZONTAL_ALIGNMENT_LEFT,-1,18)
				for j in range(3):
					var side: float = [30.0,39.6,60.0][j]
					draw_texture_rect(textures[i],Rect2(origin+Vector2(150+j*90,40),Vector2.ONE*side),false,Color.WHITE if row==0 else Color(.57,.66,.63,.86))
		draw_string(ThemeDB.fallback_font,Vector2(40,875),"Scale comparison: 120 pixels per room cell; 0.25 / 0.33 / 0.50 cell widths. No live integration implied.",HORIZONTAL_ALIGNMENT_LEFT,-1,20)

func _init() -> void:
	call_deferred("run")
func run() -> void:
	preload("res://scripts/title_settings.gd").initialized=true
	root.mode=Window.MODE_WINDOWED
	root.content_scale_size=Vector2i.ZERO
	root.size=Vector2i(1600,900)
	var sheet := Sheet.new()
	sheet.size=root.size
	for path in ["res://assets/environment/red-algae-v1/red-algae-tuft-v1.png","res://assets/environment/low-growth-v1/seagrass-rosette-v2.png","res://assets/environment/sub-biomes-v1/kelp-ribbon-kelp-v1.png"]:
		var source := Image.new()
		assert(source.load(path)==OK)
		assert(source.detect_alpha()!=Image.ALPHA_NONE)
		sheet.textures.append(ImageTexture.create_from_image(source))
	root.add_child(sheet)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var frame:=root.get_texture().get_image()
	assert(frame.get_size()==Vector2i(1600,900))
	DirAccess.make_dir_recursive_absolute("res://output/red-algae-v1")
	assert(frame.save_png("res://output/red-algae-v1/plant-scale.png")==OK)
	print("RED ALGAE STUDY PASS: three alpha sources; three cell widths; source and runtime tint; 1600x900")
	quit()
