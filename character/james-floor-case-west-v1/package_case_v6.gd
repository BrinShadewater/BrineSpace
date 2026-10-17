extends SceneTree
const OUT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"floor-case-generated-v6.png")!=OK or raw.get_size()!=Vector2i(1630,965):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	var crop:=Rect2i(498,314,634,357)
	var case:Image=raw.get_region(crop)
	for y in range(case.get_height()):
		for x in range(case.get_width()):
			if case.get_pixel(x,y).a<32.0/255.0:case.set_pixel(x,y,Color.TRANSPARENT)
	# Shared scale fits width without changing source aspect or case grade.
	var scale:=43.0/626.0
	var size:=Vector2i(roundi(crop.size.x*scale),roundi(crop.size.y*scale))
	case.resize(size.x,size.y,Image.INTERPOLATE_LANCZOS)
	var bounds:=Rect2i();var first:=true
	for y in range(case.get_height()):
		for x in range(case.get_width()):
			if case.get_pixel(x,y).a<.5:continue
			var pixel:=Rect2i(x,y,1,1);bounds=pixel if first else bounds.merge(pixel);first=false
	if first:quit(2);return
	var anchor:=Vector2i(75-bounds.position.x,222-bounds.end.y)
	var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
	frame.blit_rect(case,Rect2i(Vector2i.ZERO,size),anchor)
	if frame.save_png(OUT+"floor-case-west-v6.png")!=OK:quit(2);return
	var file:=FileAccess.open(OUT+"package-v6-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"selected":false,"raw":"floor-case-generated-v6.png","rawSize":[1630,965],"rawAlpha128Bounds":[502,318,626,349],"crop":[498,314,634,357],"sharedScale":scale,"cell":[size.x,size.y],"cellAlpha128Bounds":[bounds.position.x,bounds.position.y,bounds.size.x,bounds.size.y],"placement":[anchor.x,anchor.y],"frameSize":[256,256],"crewPivot":[128,224],"crewStandingHeight":148,"caseFloorBaseline":222,"alphaDustCutoff":32,"scope":"Native aspect-preserving packaging of built-in authored v6. Alpha128 left75/floor222 registration; no separate-axis warp or grade edit. Original crew/case reference unchanged. Hidden right edge inferred; continuous/world acceptance pending."},"  "))
	if not FileAccess.file_exists(OUT+"package_case_v6.gd.uid"):
		var uid:=FileAccess.open(OUT+"package_case_v6.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CASE V6 PACKAGE cell=",size," alpha128=",bounds," floor222")
	quit(0)
