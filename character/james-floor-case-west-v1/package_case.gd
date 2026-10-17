extends SceneTree
const OUT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"floor-case-generated-v3.png")!=OK or raw.get_size()!=Vector2i(1632,963):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	var crop:=Rect2i(509,275,614,391)
	var case:Image=raw.get_region(crop)
	for y in range(case.get_height()):
		for x in range(case.get_width()):
			if case.get_pixel(x,y).a<32.0/255.0:case.set_pixel(x,y,Color.TRANSPARENT)
	var scale:=44.0/606.0
	var size:=Vector2i(roundi(614*scale),roundi(391*scale))
	case.resize(size.x,size.y,Image.INTERPOLATE_LANCZOS)
	var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
	frame.blit_rect(case,Rect2i(Vector2i.ZERO,size),Vector2i(75,194))
	if frame.save_png(OUT+"floor-case-west.png")!=OK:quit(2);return
	var file:=FileAccess.open(OUT+"package-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"selected":false,"raw":"floor-case-generated-v3.png","rawSize":[1632,963],"crop":[509,275,614,391],"scale":scale,"resized":[size.x,size.y],"frameSize":[256,256],"anchor":[75,194],"crewPivot":[128,224],"crewStandingHeight":148,"caseFloorBaseline":222,"alphaDustCutoff":32,"scope":"Native aspect-preserving generated case extraction. Reference right edge partly occluded by original boot; full case artwork inferred, not original-pixel exact. Original crew sources unchanged; contact/grade/world lifetime/save acceptance pending."},"  "))
	if not FileAccess.file_exists(OUT+"package_case.gd.uid"):
		var uid:=FileAccess.open(OUT+"package_case.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST FLOOR CASE PACKAGE: 45x28cell; 256canvas/p128224/H148; baseline222; unselected")
	quit(0)
