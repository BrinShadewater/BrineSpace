extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load("res://character/james-floor-case-west-v1/midpoint-body-generated-v1.png")!=OK or raw.get_size()!=Vector2i(1254,1254):quit(2);return
	raw.convert(Image.FORMAT_RGBA8);raw.resize(251,251,Image.INTERPOLATE_LANCZOS)
	var edit:=Rect2i(0,192,120,33);var checks:=0
	for gear in ["bare","helmet"]:
		var original:=Image.new()
		var path:String="res://character/james-floor-case-west-v1/rise-v4/bare/000.png" if gear=="bare" else "res://character/james-floor-case-west-v1/rise-v4/helmet/000.png"
		if original.load(path)!=OK:quit(2);return
		original.convert(Image.FORMAT_RGBA8)
		var frame:Image=original.duplicate();frame.blit_rect(raw,edit,edit.position)
		for y in range(256):
			for x in range(256):
				if edit.has_point(Vector2i(x,y)):continue
				if frame.get_pixel(x,y)!=original.get_pixel(x,y):quit(2);return
				checks+=1
		DirAccess.make_dir_recursive_absolute(ROOT+"midpoint-body-v1/"+gear)
		if frame.save_png(ROOT+"midpoint-body-v1/"+gear+"/000.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"midpoint-body-v1-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"raw":"midpoint-body-generated-v1.png","scale":251.0/1254.0,"editRect":[0,192,120,33],"outsideEditOriginalPixelChecks":checks,"canvas":[256,256],"pivot":[128,224],"standingHeight":148,"scope":"Built-in case-removal edit contributes only floor/case and tiny leftmost toe region. Both original V4 heads/helmets/body and most boots preserved byte-exact outside stated rectangle; no grade, pose normalization or translation. Native case/body contact review pending."},"  "))
	if not FileAccess.file_exists(ROOT+"package_midpoint_body_v1.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_midpoint_body_v1.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES MIDPOINT BODY: ",checks,"protected original pixel checks; paired/unselected")
	quit(0)
