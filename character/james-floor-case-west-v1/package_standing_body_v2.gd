extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var pixel_checks:=0
	var source_bare:=Image.new()
	if source_bare.load("res://character/crew-runtime-matte-v1/branforth/frames/idle-west-breathing-v1/000.png")!=OK:quit(2);return
	source_bare.convert(Image.FORMAT_RGBA8)
	var original_bare:=Image.new()
	if original_bare.load("res://character/james-cargo-material-joined-v1/frames/bare/unload-west/005.png")!=OK:quit(2);return
	original_bare.convert(Image.FORMAT_RGBA8)
	var body_bare:=Image.create(256,256,false,Image.FORMAT_RGBA8)
	body_bare.fill(Color(0,0,0,0));body_bare.blit_rect(source_bare,Rect2i(0,0,184,184),Vector2i(36,52))
	for y in range(193):
		for x in range(256):
			if body_bare.get_pixel(x,y)!=original_bare.get_pixel(x,y):quit(2);return
			pixel_checks+=1
	DirAccess.make_dir_recursive_absolute(ROOT+"standing-body-v2/bare")
	if body_bare.save_png(ROOT+"standing-body-v2/bare/000.png")!=OK:quit(2);return
	var source_helmet:=Image.new()
	if source_helmet.load("res://character/james-shared-helmet-runtime-v1/frames/idle-west/000.png")!=OK:quit(2);return
	source_helmet.convert(Image.FORMAT_RGBA8)
	var original_helmet:=Image.new()
	if original_helmet.load("res://character/james-cargo-material-joined-v1/frames/helmet/unload-west/005.png")!=OK:quit(2);return
	original_helmet.convert(Image.FORMAT_RGBA8)
	var body_helmet:=Image.create(256,256,false,Image.FORMAT_RGBA8)
	body_helmet.fill(Color(0,0,0,0));body_helmet.blit_rect(source_helmet,Rect2i(0,0,184,184),Vector2i(36,52))
	for y in range(193):
		for x in range(256):
			if body_helmet.get_pixel(x,y)!=original_helmet.get_pixel(x,y):quit(2);return
			pixel_checks+=1
	DirAccess.make_dir_recursive_absolute(ROOT+"standing-body-v2/helmet")
	if body_helmet.save_png(ROOT+"standing-body-v2/helmet/000.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"standing-body-v2-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"upperOriginalPixelChecks":pixel_checks,"method":"Exact original selected West idle184canvas translated36/52 into256canvas. No resampling, grade or invented pixels. Source binding file records original visible-right-body agreement."},"  "))
	if not FileAccess.file_exists(ROOT+"package_standing_body_v2.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_standing_body_v2.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CANONICAL BODY PACKAGE: paired; ",pixel_checks,"original upper pixel checks; exact idle body")
	quit(0)
