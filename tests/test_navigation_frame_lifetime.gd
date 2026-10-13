extends SceneTree
const Badge=preload("res://scripts/navigation_badge.gd")
var checks:=0
var failures:=0
func _init():call_deferred("run")
func check(value:bool,label:String):
	checks+=1
	if not value:failures+=1;push_error(label)
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	# A strong cache of processed results must fail the final-owner assertion.
	for with_mips in [false,true]:
		var image:=Image.create(4,12,false,Image.FORMAT_RGBA8)
		image.fill(Color.RED);image.fill_rect(Rect2i(0,7,4,1),Color.BLUE);image.fill_rect(Rect2i(0,8,4,1),Color.GREEN)
		if with_mips:image.generate_mipmaps()
		var source:Texture2D=ImageTexture.create_from_image(image)
		var result:Texture2D=Badge.plain_frame(source)
		var pixels:=result.get_image()
		check(pixels.get_size()==Vector2i(4,12) and pixels.has_mipmaps()==with_mips,"Dimensions and mipmap state retained")
		check(source.get_image().get_pixel(0,8)==Color.GREEN,"Source pixels remain immutable")
		for row in range(12):
			check(pixels.get_pixel(0,row)==(Color.BLUE if row in [7,8] else Color.RED),"Only highlight row is replaced: "+str(row))
		check(Badge.plain_frame(source)==result,"Live callers reuse the processed frame")
		var weak:WeakRef=weakref(result)
		result=null
		check(weak.get_ref()==null,"Processed frame released when its final caller releases it")
		source=null
	# Tiny sources return themselves; the lookup must not keep them alive either.
	var tiny:Texture2D=ImageTexture.create_from_image(Image.create(2,2,false,Image.FORMAT_RGBA8))
	check(Badge.plain_frame(tiny)==tiny,"Tiny frame stays unchanged")
	var tiny_weak:WeakRef=weakref(tiny);tiny=null
	check(tiny_weak.get_ref()==null,"Unchanged tiny source released with final caller")
	check(Badge.plain_frame(null)==null,"Null remains null")
	FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures}))
	print("NAVIGATION_FRAME_LIFETIME ",checks," checks ",failures," failures");quit(1 if failures else 0)
