extends SceneTree
const ROOT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var source:=Image.new();var paired:=Image.new()
	if source.load("res://character/james-cargo-material-joined-v1/frames/bare/unload-west/004.png")!=OK or paired.load("res://character/james-cargo-material-joined-v1/frames/helmet/unload-west/004.png")!=OK:quit(2);return
	source.convert(Image.FORMAT_RGBA8);paired.convert(Image.FORMAT_RGBA8)
	# Explicit extraction boundary excludes adjacent toe atx117+; retain original
	# case pixels without resampling/grade. Rightmost low-alpha outline is cropped.
	var crop:=Rect2i(74,192,43,32);var checks:=0
	var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color(0,0,0,0));frame.blit_rect(source,crop,crop.position)
	for y in range(crop.position.y,crop.end.y):
		for x in range(crop.position.x,crop.end.x):
			if source.get_pixel(x,y)!=paired.get_pixel(x,y) or frame.get_pixel(x,y)!=source.get_pixel(x,y):quit(2);return
			checks+=1
	if frame.save_png("res://character/james-floor-case-west-v1/floor-case-west-v7.png")!=OK:quit(2);return
	var f:=FileAccess.open(ROOT+"case-v7-package-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"selected":false,"method":"Native deterministic extraction of original cue4 case pixels; no provider, repaint, resampling or grade.","crop":[74,192,43,32],"placement":[74,192],"canvas":[256,256],"pivot":[128,224],"standingHeight":148,"pairedOriginalAndExtractedPixelChecks":checks,"limitation":"Explicit right boundary excludes adjacent boot toe, and trims rightmost low-alpha case outline; no complete unoccluded-source/exactwholecase claim. Visual case/feet contact review pending."},"  "))
	if not FileAccess.file_exists(ROOT+"package_case_v7.gd.uid"):
		var uid:=FileAccess.open(ROOT+"package_case_v7.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CASE V7: ",checks,"paired original/extracted pixel checks; no rescale; unselected")
	quit(0)
