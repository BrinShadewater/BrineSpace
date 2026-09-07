extends SceneTree
const PACK := "res://assets/environment/shell-shoal-v1/"

class Sheet extends Control:
	var ground: Texture2D
	var rocks: Texture2D
	var shells: Texture2D
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		var font := ThemeDB.fallback_font
		for panel in range(2):
			var origin := Vector2(30+panel*790,90)
			draw_string(font,origin-Vector2(0,30),["Ordinary repeat / source colors","Mirrored repeat / habitat tint"][panel],HORIZONTAL_ALIGNMENT_LEFT,-1,23)
			for y in range(3):
				for x in range(3):
					var rect := Rect2(origin+Vector2(x,y)*240,Vector2(240,240))
					if panel == 1:
						if x%2 == 1: rect.size.x = -240
						if y%2 == 1: rect.size.y = -240
					draw_texture_rect(ground,rect,false,Color.WHITE if panel==0 else Color(.49,.58,.57))
			# A material repeat represents four cells; each prop is 0.4 cell wide.
			for at in [Vector2(200,220),Vector2(490,420),Vector2(360,560)]:
				draw_texture_rect(rocks,Rect2(origin+at,Vector2(24,24)),false,Color.WHITE if panel==0 else Color(.59,.68,.66,.85))
			for at in [Vector2(230,240),Vector2(450,460)]:
				draw_texture_rect(shells,Rect2(origin+at,Vector2(20,20)),false,Color.WHITE if panel==0 else Color(.59,.68,.66,.85))
		draw_string(font,Vector2(30,855),"Scale study: each ground repeat spans four room cells; cobbles span 0.4 cell. No station integration implied.",HORIZONTAL_ALIGNMENT_LEFT,-1,20)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	var sheet := Sheet.new()
	sheet.size = root.size
	var ground := Image.load_from_file(PACK+"shell-hash-ground-v2.png")
	var rocks := Image.load_from_file(PACK+"limestone-cobbles-v1.png")
	var shells := Image.load_from_file(PACK+"shell-bed-v1.png")
	assert(not shells.is_empty() and shells.detect_alpha()!=Image.ALPHA_NONE)
	assert(not ground.is_empty() and not rocks.is_empty())
	assert(rocks.detect_alpha()!=Image.ALPHA_NONE)
	sheet.ground = ImageTexture.create_from_image(ground)
	sheet.rocks = ImageTexture.create_from_image(rocks)
	sheet.shells = ImageTexture.create_from_image(shells)
	root.add_child(sheet)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==Vector2i(1600,900))
	DirAccess.make_dir_recursive_absolute("res://output/shell-shoal-v1")
	assert(frame.save_png("res://output/shell-shoal-v1/repetition-v3.png")==OK)
	print("SHELL SHOAL STUDY PASS: three sources loaded; 1600x900 repetition and scale capture")
	quit()
