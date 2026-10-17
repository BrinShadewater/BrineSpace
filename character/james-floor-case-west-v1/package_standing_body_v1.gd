extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load("res://character/james-floor-case-west-v1/standing-body-only-generated-v1.png")!=OK or raw.get_size()!=Vector2i(1254,1254):quit(2);return
	raw.convert(Image.FORMAT_RGBA8);raw.resize(251,251,Image.INTERPOLATE_LANCZOS)
	var lower:=Image.create(256,256,false,Image.FORMAT_RGBA8);lower.fill(Color.TRANSPARENT);lower.blit_rect(raw,Rect2i(0,194,251,57),Vector2i(0,194))
	var protected_checks:=0
	for gear in ["bare","helmet"]:
		var original:=Image.new()
		var path:String="res://character/james-cargo-material-joined-v1/frames/bare/unload-west/005.png" if gear=="bare" else "res://character/james-cargo-material-joined-v1/frames/helmet/unload-west/005.png"
		if original.load(path)!=OK:quit(2);return
		original.convert(Image.FORMAT_RGBA8)
		var frame:Image=lower.duplicate();frame.blit_rect(original,Rect2i(0,0,256,194),Vector2i.ZERO)
		for y in range(194):
			for x in range(256):
				if frame.get_pixel(x,y)!=original.get_pixel(x,y):quit(2);return
				protected_checks+=1
		DirAccess.make_dir_recursive_absolute(ROOT+"standing-body-v1/"+gear)
		if frame.save_png(ROOT+"standing-body-v1/"+gear+"/000.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"standing-body-v1-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"protectedUpperPixelsChecked":protected_checks,"protectedRect":[0,0,256,194],"sharedGeneratedLowerRect":[0,194,256,62],"rawCanvas":[1254,1254],"scale":251.0/1254.0,"canvas":[256,256],"pivot":[128,224],"standingHeight":148,"scope":"Built-in authored body-only standing feet, uniform full-canvas resize/no translation/grade. Original upper194rows preserved exactly per gear; one shared generated lower region. Original paired lower region byte-identical before editing. Boot/case/master source comparison pending; no runtime/normal selection acceptance."},"  "))
	if not FileAccess.file_exists(ROOT+"package_standing_body_v1.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_standing_body_v1.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES BODY ONLY PACKAGE: paired; ",protected_checks,"original upper pixel checks; unselected")
	quit(0)
