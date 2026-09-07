extends SceneTree
const OUT := "res://output/ripple-sand-v1/"

class Sheet extends Control:
	var ground: Texture2D
	var debris: Texture2D
	var stone: Texture2D
	var porous: Texture2D
	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("102a32"))
		for panel in range(4):
			var origin := Vector2(25+(panel%2)*790,65+(panel/2)*430)
			var mirrored := panel%2==1
			var tinted := panel>=2
			var title := ("Mirrored" if mirrored else "Ordinary")+ (" / habitat tint" if tinted else " / source colors")
			draw_string(ThemeDB.fallback_font,origin-Vector2(0,20),title,HORIZONTAL_ALIGNMENT_LEFT,-1,22)
			for y in range(2):
				for x in range(4):
					var rect := Rect2(origin+Vector2(x,y)*180,Vector2(180,180))
					if mirrored:
						if x%2==1: rect.size.x=-180
						if y%2==1: rect.size.y=-180
					draw_texture_rect(ground,rect,false,Color(.49,.58,.57) if tinted else Color.WHITE)
			# 45 screen pixels per cell; show companion props at their authored scale.
			draw_texture_rect(debris,Rect2(origin+Vector2(220,150),Vector2.ONE*30.6),false,Color(.43,.57,.60,.88) if tinted else Color.WHITE)
			draw_texture_rect(stone,Rect2(origin+Vector2(470,200),Vector2.ONE*18),false,Color(.59,.68,.66,.85) if tinted else Color.WHITE)
			draw_texture_rect(porous,Rect2(origin+Vector2(350,120),Vector2.ONE*22.5),false,Color(.59,.68,.66,.85) if tinted else Color.WHITE)

func _init() -> void:
	call_deferred("run")

func run() -> void:
	preload("res://scripts/title_settings.gd").initialized = true
	root.mode = Window.MODE_WINDOWED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1600,900)
	var sheet := Sheet.new()
	sheet.size=root.size
	var paths := ["res://assets/environment/ripple-sand-v1/ripple-sand-v1.png","res://assets/environment/service-wreckage-v1/collapsed-support-v1.png","res://assets/environment/shell-shoal-v1/limestone-cobbles-v1.png"]
	var textures: Array[Texture2D] = []
	for path in paths:
		var source := Image.new()
		assert(source.load(path)==OK)
		textures.append(ImageTexture.create_from_image(source))
	sheet.ground=textures[0]
	sheet.debris=textures[1]
	sheet.stone=textures[2]
	var porous_image := Image.new()
	assert(porous_image.load("res://assets/environment/volcanic-ash-v1/porous-rocks-v1.png")==OK)
	assert(porous_image.detect_alpha()!=Image.ALPHA_NONE)
	sheet.porous=ImageTexture.create_from_image(porous_image)
	root.add_child(sheet)
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw
	var frame := root.get_texture().get_image()
	assert(frame.get_size()==Vector2i(1600,900))
	DirAccess.make_dir_recursive_absolute(OUT)
	assert(frame.save_png(OUT+"ground-repetition.png")==OK)
	print("RIPPLE SAND STUDY PASS: four comparison panels; four sources loaded; 1600x900 capture")
	quit()
