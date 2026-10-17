extends SceneTree
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var original:=Image.new();var raw:=Image.new()
	if original.load("res://character/james-cargo-return-bridges-v1/frames-v9/bare/002.png")!=OK or raw.load("res://character/james-cargo-return-bridges-v1/collar-repair-v10-raw.png")!=OK:quit(2);return
	original.convert(Image.FORMAT_RGBA8);raw.convert(Image.FORMAT_RGBA8)
	if raw.get_size()!=Vector2i(1254,1254):push_error("Unexpected raw composition; inspect before packaging");quit(2);return
	raw.resize(256,256,Image.INTERPOLATE_LANCZOS)
	var frame:Image=original.duplicate()
	var region:=Rect2i(104,72,49,48)
	frame.blit_rect(raw,region,region.position)
	var checks:=0
	for y in range(256):
		for x in range(256):
			if not region.has_point(Vector2i(x,y)):
				checks+=1
				if frame.get_pixel(x,y)!=original.get_pixel(x,y):push_error("Protected original changed");quit(2);return
	if frame.save_png("res://character/james-cargo-return-bridges-v1/collar-v10-bare.png")!=OK:quit(2);return
	var report:=FileAccess.open("res://character/james-cargo-return-bridges-v1/collar-v10-package.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"selected":false,"protectedOriginalPixels":checks,"editRect":[104,72,49,48],"rawScale":256.0/1254.0,"translation":[0,0],"grade":"none","scope":"One bare bridge interior head/collar candidate. Original case, gloves, lower body and feet exact. Not paired, installed or full transition accepted."},"  "))
	if not FileAccess.file_exists("res://character/james-cargo-return-bridges-v1/package-collar-v10.gd.uid"):
		var uid:=FileAccess.open("res://character/james-cargo-return-bridges-v1/package-collar-v10.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES COLLAR V10: ",checks," original pixels protected; unselected")
	quit(0)
