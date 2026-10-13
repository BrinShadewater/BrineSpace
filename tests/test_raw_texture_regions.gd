extends SceneTree
const Grid=preload("res://scripts/grid_canvas.gd")
const Safe=preload("res://scripts/safe_image.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):
		push_error("Isolation mismatch");quit(2);return
	if DisplayServer.get_name()=="headless":push_error("Native GPU readback required");quit(2);return
	var grid=Grid.new()
	var paths:Array=["res://legacy/retired/space texture.jpg","res://legacy/default/dooranimated.png",grid.DepartmentDoor.SOURCE,"res://assets/sea-life-v1/lighting/caustics-tile-512.png"]
	for path in grid.room_texture_paths.values():paths.append(path)
	var image:=Image.create(17,19,false,Image.FORMAT_RGBA8)
	image.fill(Color(0.2,0.4,0.8,0.5))
	check(ResourceSaver.save(ImageTexture.create_from_image(image),"user://imported-texture.tres")==OK,"Scratch imported texture saved")
	paths.append("user://imported-texture.tres")
	for path in paths:
		var expected:Texture2D=Safe.raw_texture(path)
		var actual:Texture2D=grid._load_png_texture(path)
		check(expected!=null and actual!=null,"Texture available: "+path)
		if expected==null or actual==null:continue
		var old_image:=expected.get_image()
		var new_image:=actual.get_image()
		check(old_image.get_data()==new_image.get_data(),"Exact GPU pixels: "+path)
		check(old_image.get_size()==new_image.get_size() and old_image.get_format()==new_image.get_format() and old_image.has_mipmaps()==new_image.has_mipmaps(),"Image headers preserved: "+path)
		check(grid.texture_source_regions[actual.get_instance_id()]==grid._find_content_region(old_image),"Source region preserved: "+path)
	check(grid._load_png_texture("user://missing.png")==null,"Missing source retains null fallback")
	check(Safe.failures.is_empty(),"No unexpected art failures")
	grid.free()
	print("RAW_TEXTURE_REGIONS ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
