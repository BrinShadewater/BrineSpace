extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load("res://character/james-floor-case-west-v1/rise-generated-v4-helmet.png")!=OK or raw.get_size()!=Vector2i(1254,1254):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	raw.resize(251,251,Image.INTERPOLATE_LANCZOS)
	var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
	frame.blit_rect(raw,Rect2i(0,0,251,251),Vector2i.ZERO)
	DirAccess.make_dir_recursive_absolute(ROOT+"rise-v4/helmet")
	if frame.save_png("res://character/james-floor-case-west-v1/rise-v4/helmet/000.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"rise-v4-helmet-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"gear":"helmet","canvas":[256,256],"pivot":[128,224],"standingHeight":148,"rawCanvas":[1254,1254],"scaledCanvas":[251,251],"sharedScale":251.0/1254.0,"translation":[0,0],"scope":"Original case/feet landmarks match5:1 ruler. Full raw canvas uniformly resized then transparent right/bottom padding. No per-pose height, crop, floor translation, grade or alpha retouch. Original endpoint comparison pending."},"  "))
	if not FileAccess.file_exists(ROOT+"package_rise_v4_helmet.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_rise_v4_helmet.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES RISE V4 PACKAGE: helmet midpoint; full canvas5:1; no translation; unselected")
	quit(0)
