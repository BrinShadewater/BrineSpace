extends SceneTree
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var original:=Image.new();var raw:=Image.new()
	if original.load("res://character/james-cargo-return-bridges-v1/frames-v9/bare/002.png")!=OK or raw.load("res://character/james-cargo-return-bridges-v1/collar-repair-v11-raw.png")!=OK:quit(2);return
	original.convert(Image.FORMAT_RGBA8);raw.convert(Image.FORMAT_RGBA8)
	if raw.get_size()!=Vector2i(1254,1254):quit(2);return
	raw.resize(256,256,Image.INTERPOLATE_LANCZOS)
	var frame:Image=original.duplicate()
	var region:=Rect2i(108,100,26,10)
	var checks:=0;var edited:=0;var ochre_checks:=0
	for y in range(256):
		for x in range(256):
			var point:=Vector2i(x,y);var old:Color=original.get_pixel(x,y)
			var ochre:bool=old.a>.5 and old.r>old.g*1.05 and old.g>old.b*1.3
			if region.has_point(point) and not ochre:
				frame.set_pixel(x,y,raw.get_pixel(x,y));edited+=1
			else:
				checks+=1
				if region.has_point(point) and ochre:ochre_checks+=1
				if frame.get_pixel(x,y)!=old:quit(2);return
	if frame.save_png("res://character/james-cargo-return-bridges-v1/collar-v12-bare.png")!=OK:quit(2);return
	var report:=FileAccess.open("res://character/james-cargo-return-bridges-v1/collar-v12-package.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"selected":false,"protectedOriginalPixels":checks,"editedPixels":edited,"protectedOchreInWindow":ochre_checks,"editRect":[108,100,26,10],"rawScale":256.0/1254.0,"translation":[0,0],"grade":"none","scope":"Collar-only alternative packaging of same V11 raw. All original pixels below110 and above100 exact, ochre cap and badge preserved. Source review required."},"  "))
	if not FileAccess.file_exists("res://character/james-cargo-return-bridges-v1/package-collar-v12.gd.uid"):
		var uid:=FileAccess.open("res://character/james-cargo-return-bridges-v1/package-collar-v12.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES COLLAR V12: ",checks," protected; ",edited," admitted collar; ",ochre_checks," protected ochre pixels")
	quit(0)
