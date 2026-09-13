extends SceneTree
func _init():
	var source := Image.load_from_file("res://assets/hull-damage-v1/source-v1.png")
	source.convert(Image.FORMAT_RGBA8)
	for y in range(source.get_height()):
		for x in range(source.get_width()):
			var c := source.get_pixel(x,y)
			if minf(c.r,c.b)-c.g>0.12:
				source.set_pixel(x,y,Color(0,0,0,0))
	var atlas := Image.create(288,192,false,Image.FORMAT_RGBA8)
	for i in range(6):
		var cell := source.get_region(Rect2i((i%3)*512,(i/3)*512,512,512))
		cell.resize(96,96,Image.INTERPOLATE_NEAREST)
		atlas.blit_rect(cell,Rect2i(0,0,96,96),Vector2i((i%3)*96,(i/3)*96))
	atlas.save_png("res://assets/hull-damage-v1/hull-96.png")
	source.save_png("res://assets/hull-damage-v1/hull-full.png")
	print("HULL ATLAS BAKED 288x192 RGBA")
	quit()
