extends SceneTree
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var original:=Image.new();var raw:=Image.new()
	if original.load("res://character/james-cargo-return-bridges-v1/frames-v9/bare/002.png")!=OK or raw.load("res://character/james-cargo-return-bridges-v1/collar-repair-v11-raw.png")!=OK:quit(2);return
	original.convert(Image.FORMAT_RGBA8);raw.convert(Image.FORMAT_RGBA8)
	if raw.get_size()!=Vector2i(1254,1254):push_error("Unexpected inspected raw dimensions");quit(2);return
	raw.resize(256,256,Image.INTERPOLATE_LANCZOS)
	var frame:Image=original.duplicate()
	var region:=Rect2i(108,100,29,15)
	var badge:=Rect2i(134,110,23,25)
	var checks:=0;var edited:=0
	for y in range(256):
		for x in range(256):
			var point:=Vector2i(x,y)
			if region.has_point(point) and not badge.has_point(point):
				frame.set_pixel(x,y,raw.get_pixel(x,y));edited+=1
			else:
				checks+=1
				if frame.get_pixel(x,y)!=original.get_pixel(x,y):push_error("Protected original changed");quit(2);return
	if frame.save_png("res://character/james-cargo-return-bridges-v1/collar-v11-bare.png")!=OK:quit(2);return
	var report:=FileAccess.open("res://character/james-cargo-return-bridges-v1/collar-v11-package.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"selected":false,"protectedOriginalPixels":checks,"editedPixels":edited,"editRect":[108,100,29,15],"badgeExclusion":[134,110,23,25],"rawScale":256.0/1254.0,"translation":[0,0],"grade":"none","scope":"One bare bridge interior collar-only candidate. Original face/head above100, badge exclusion, case/gloves/feet exact. Not paired or motion accepted."},"  "))
	if not FileAccess.file_exists("res://character/james-cargo-return-bridges-v1/package-collar-v11.gd.uid"):
		var uid:=FileAccess.open("res://character/james-cargo-return-bridges-v1/package-collar-v11.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES COLLAR V11: ",checks," original pixels protected; ",edited," collar pixels edited; unselected")
	quit(0)
