extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
class Reference extends GridCanvas:
	func _find_content_region(image: Image) -> Rect2:
		var width := image.get_width()
		var height := image.get_height()
		var min_x := width
		var min_y := height
		var max_x := -1
		var max_y := -1
		for y in range(0, height, 2):
			for x in range(0, width, 2):
				var pixel := image.get_pixel(x, y)
				var is_visible_pixel := pixel.a > 0.04 and maxf(maxf(pixel.r, pixel.g), pixel.b) > 0.018
				if is_visible_pixel:
					min_x = mini(min_x, x)
					min_y = mini(min_y, y)
					max_x = maxi(max_x, x)
					max_y = maxi(max_y, y)
		if max_x < min_x or max_y < min_y:
			return Rect2(Vector2.ZERO, Vector2(width, height))
		min_x = maxi(min_x - ROOM_SOURCE_MARGIN, 0)
		min_y = maxi(min_y - ROOM_SOURCE_MARGIN, 0)
		max_x = mini(max_x + ROOM_SOURCE_MARGIN, width - 1)
		max_y = mini(max_y + ROOM_SOURCE_MARGIN, height - 1)
		return Rect2(Vector2(min_x, min_y), Vector2(max_x - min_x + 1, max_y - min_y + 1))
	

var checks:=0
var failures:=0
var old_usec:=0
var new_usec:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func compare(candidate,reference,image:Image,label:String):
	var before:=image.get_data()
	var stamp:=Time.get_ticks_usec()
	var expected:Rect2=reference._find_content_region(image)
	old_usec+=Time.get_ticks_usec()-stamp
	stamp=Time.get_ticks_usec()
	var actual:Rect2=candidate._find_content_region(image)
	new_usec+=Time.get_ticks_usec()-stamp
	check(actual==expected,"Exact region: "+label)
	check(image.get_data()==before,"Input unchanged: "+label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):
		push_error("Isolation mismatch");quit(2);return
	var candidate=Grid.new();var reference=Reference.new()
	var rng:=RandomNumberGenerator.new();rng.seed=71006
	for format in [Image.FORMAT_RGBA8,Image.FORMAT_RGB8,Image.FORMAT_RGBAF]:
		for size in [Vector2i(1,1),Vector2i(2,3),Vector2i(31,33),Vector2i(64,64)]:
			for mode in range(7):
				var image:=Image.create(size.x,size.y,false,format)
				image.fill(Color.TRANSPARENT)
				for y in size.y:
					for x in size.x:
						var color:=Color.TRANSPARENT
						match mode:
							0:color=Color(0.018,0,0,0.04)
							1:color=Color(0.01801,0,0,0.04001)
							2:color=Color.WHITE
							3:color=Color.WHITE if x%2==1 or y%2==1 else Color.TRANSPARENT
							4:color=Color.WHITE if x==size.x-1 and y==size.y-1 else Color.TRANSPARENT
							5:color=Color(0,0,0,1)
							6:color=Color(rng.randf(),rng.randf(),rng.randf(),rng.randf()) if rng.randf()<0.03 else Color.TRANSPARENT
						image.set_pixel(x,y,color)
				compare(candidate,reference,image,"%s/%s/%s"%[format,size,mode])
	var paths:Dictionary={}
	for path in candidate.room_texture_paths.values():paths[path]=true
	for group in candidate.room_texture_variant_paths.values():
		for path in group:paths[path]=true
	for path in paths:
		var image:Image=preload("res://scripts/safe_image.gd").raw_image(path)
		check(image!=null,"Runtime room image available: "+path)
		if image!=null:compare(candidate,reference,image,path)
	check(preload("res://scripts/safe_image.gd").failures.is_empty(),"No diagnostic artwork failures")
	candidate.free();reference.free()
	print("CARD_REGIONS ",checks," checks; ",failures," failures; reference_ms ",old_usec/1000.0," candidate_ms ",new_usec/1000.0)
	quit(1 if failures else 0)
