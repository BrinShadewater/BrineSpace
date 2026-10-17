extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load("res://character/james-floor-case-west-v1/rise-generated-v4-bare.png")!=OK or raw.get_size()!=Vector2i(1280,1280):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	raw.resize(256,256,Image.INTERPOLATE_LANCZOS)
	DirAccess.make_dir_recursive_absolute(ROOT+"rise-v4/bare")
	if raw.save_png("res://character/james-floor-case-west-v1/rise-v4/bare/000.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"rise-v4-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"gear":"bare","canvas":[256,256],"pivot":[128,224],"standingHeight":148,"rawCanvas":[1280,1280],"sharedScale":0.2,"translation":[0,0],"scope":"Full original canvas composition uniformly resized5:1. No per-pose height, crop, floor translation, grade or alpha retouch. Original endpoint comparison pending."},"  "))
	if not FileAccess.file_exists(ROOT+"package_rise_v4.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_rise_v4.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES RISE V4 PACKAGE: bare midpoint; full canvas5:1; no translation; unselected")
	quit(0)
