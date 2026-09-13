extends SceneTree
const Effects=preload("res://scripts/fire_effects.gd")
var failures := 0
var checks := 0
func check(ok: bool,message: String):
	checks+=1
	if not ok: failures+=1;push_error(message)
func _init():
	for kind in Effects.PATHS:
		var image := Image.new()
		check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(Effects.PATHS[kind]))==OK,"Raw atlas loads: "+kind)
		check(image.get_size()==Vector2i(384,256) and image.get_format()==Image.FORMAT_RGBA8,"RGBA atlas dimensions: "+kind)
		var signatures := {}
		for index in range(8):
			var region := image.get_region(Rect2i(Vector2i(index%4,index/4)*Vector2i(96,128),Vector2i(96,128)))
			var bounds := region.get_used_rect()
			check(bounds.has_area() and bounds.position.x>0 and bounds.position.y>0 and bounds.end.x<96 and bounds.end.y<128,"Frame stays within its cell: %s/%d" % [kind,index])
			signatures[hash(region.get_data())]=true
		check(signatures.size()==8,"Eight distinct authored frames: "+kind)
		var has_transparent := false
		var has_solid := false
		var matte_spill := false
		for y in range(image.get_height()):
			for x in range(image.get_width()):
				var color := image.get_pixel(x,y)
				if color.a==0: has_transparent=true
				elif color.a==1:
					has_solid=true
					if color.r-color.g>.09 and color.b-color.g>.09: matte_spill=true
		check(has_transparent and has_solid and not matte_spill,"Real transparent background without magenta fringe: "+kind)
	check(Effects.frame(0,8,0)==0 and Effects.frame(.875,8,0)==7 and Effects.frame(1,8,0)==0,"Atlas loops across all eight frames")
	check(Effects.spark_time(0,0)<8.0/12.0 and Effects.spark_time(1,0)>8.0/12.0,"Spark burst has a quiet interval")
	check(is_equal_approx(Effects.spark_time(2.8,0),0.0),"Spark burst restarts after quiet interval")
	print("Fire assets: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
