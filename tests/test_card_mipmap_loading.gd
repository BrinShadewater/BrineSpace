extends SceneTree
const Main=preload("res://scripts/main.gd")
const Art=preload("res://scripts/room_card_art.gd")
const Safe=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
var before_usec:=0
var after_usec:=0
func original(path:String)->Texture2D:
	var texture:=Safe.raw_texture(path)
	if texture==null:return null
	var image:=texture.get_image()
	if image!=null and not image.has_mipmaps():
		if image.generate_mipmaps()==OK:return ImageTexture.create_from_image(image)
	return texture
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func capture(view:SubViewport,sprite:Sprite2D,texture:Texture2D)->PackedByteArray:
	sprite.texture=texture
	await process_frame
	await RenderingServer.frame_post_draw
	return view.get_texture().get_image().get_data()
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):
		push_error("Isolation mismatch");quit(2);return
	if DisplayServer.get_name()=="headless":push_error("Native mipmap/filter verification required");quit(2);return
	var main=Main.new()
	var view:=SubViewport.new();view.size=Vector2i(192,192);view.transparent_bg=true;view.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	root.add_child(view)
	var sprite:=Sprite2D.new();sprite.position=Vector2(96,96);view.add_child(sprite)
	var paths:Array=Art.PATHS.values()
	var imported:=Image.create(17,19,false,Image.FORMAT_RGBA8);imported.fill(Color(0.3,0.6,0.1,0.7));imported.generate_mipmaps()
	check(ResourceSaver.save(ImageTexture.create_from_image(imported),"user://mipmap-texture.tres")==OK,"Imported mipmap fixture saved")
	paths.append("user://mipmap-texture.tres")
	for index in paths.size():
		var path:String=paths[index]
		var stamp:=Time.get_ticks_usec();var expected:Texture2D=original(path);before_usec+=Time.get_ticks_usec()-stamp
		stamp=Time.get_ticks_usec();var actual:Texture2D=main._load_card_thumbnail(path);after_usec+=Time.get_ticks_usec()-stamp
		check(expected!=null and actual!=null,"Card available: "+path)
		if expected==null or actual==null:continue
		var a:=expected.get_image();var b:=actual.get_image()
		check(a.get_size()==b.get_size() and a.get_format()==b.get_format(),"Card headers: "+path)
		check(a.has_mipmaps()==b.has_mipmaps() and a.get_mipmap_count()==b.get_mipmap_count(),"Mipmap count: "+path)
		check(a.get_data()==b.get_data(),"All GPU mipmap bytes: "+path)
		# Different alpha/art families at actual fan reduction and rotation.
		if index<6:
			for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS]:
				for angle in [-17.0,0.0,17.0]:
					sprite.texture_filter=filter;sprite.rotation=deg_to_rad(angle);sprite.scale=Vector2.ONE*0.19
					var old_pixels:PackedByteArray=await capture(view,sprite,expected)
					var new_pixels:PackedByteArray=await capture(view,sprite,actual)
					check(old_pixels==new_pixels,"Exact fan raster: %s/%s/%s"%[path,filter,angle])
	check(main._load_card_thumbnail("user://missing.png")==null,"Missing card fallback remains null")
	main.free();view.queue_free()
	await process_frame
	print("CARD_MIPMAPS ",checks," checks; ",failures," failures; original_ms ",before_usec/1000.0," candidate_ms ",after_usec/1000.0)
	quit(1 if failures else 0)
