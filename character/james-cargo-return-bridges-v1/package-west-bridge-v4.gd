extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
const WINDOW=Rect2i(80,110,84,69)
const ORIGINALS={"bare":"res://character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png","helmet":"res://character/james-east-cargo-heads-v3/frames/helmet/carry-turn-east-west/010.png"}
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"west-bridge-generated-v4.png")!=OK:quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	if raw.get_size()!=Vector2i(1536,1024):quit(2);return
	var sources:Array=[];var evidence:Array=[];var protected_checks:=0
	# Only generated bare torso is used. The original paired gear pixels stay
	# outside a documented torso/hip rectangle, not a claimed semantic mask.
	for col in range(3):
		var source:Image=raw.get_region(Rect2i(col*512,0,512,512))
		var left:=512;var right:=0
		for y in range(463,498):
			for x in range(512):
				if source.get_pixel(x,y).a>=128.0/255.0:left=mini(left,x);right=maxi(right,x+1)
		if right<=left:quit(2);return
		var foot_x:float=(left+right)*.5
		for y in range(512):
			for x in range(512):
				if source.get_pixel(x,y).a<32.0/255.0:source.set_pixel(x,y,Color.TRANSPARENT)
		source.resize(215,215,Image.INTERPOLATE_LANCZOS)
		var transformed:=Image.create(256,256,false,Image.FORMAT_RGBA8);transformed.fill(Color.TRANSPARENT)
		var anchor:=Vector2i(roundi(128-foot_x*215.0/512.0),roundi(224-498*215.0/512.0))
		transformed.blit_rect(source,Rect2i(0,0,215,215),anchor);sources.append(transformed)
		evidence.append({"index":col,"cell":[col*512,0,512,512],"rawFootX":foot_x,"rawSole":498,"anchor":[anchor.x,anchor.y]})
	for mode in ["bare","helmet"]:
		var original:=Image.new()
		if original.load(ORIGINALS[mode])!=OK:quit(2);return
		original.convert(Image.FORMAT_RGBA8)
		DirAccess.make_dir_recursive_absolute(OUT+"frames-v4/"+mode)
		var files:Array=[]
		for i in range(3):
			var frame:Image=original.duplicate()
			if i<2:
				if frame.load(OUT+"frames-v3/"+mode+"/%03d.png"%i)!=OK:quit(2);return
				frame.convert(Image.FORMAT_RGBA8)
			else:frame.blit_rect(sources[i],WINDOW,WINDOW.position)
			for y in range(256):
				for x in range(256):
					if WINDOW.has_point(Vector2i(x,y)):continue
					protected_checks+=1
					if frame.get_pixel(x,y)!=original.get_pixel(x,y):push_error("Protected original changed");quit(2);return
			var file:String="frames-v4/"+mode+"/%03d.png"%i
			if frame.save_png(OUT+file)!=OK:quit(2);return
			if i<2 and FileAccess.get_file_as_bytes(OUT+file)!=FileAccess.get_file_as_bytes(OUT+"frames-v3/"+mode+"/%03d.png"%i):push_error("Retained first pose bytes changed");quit(2);return
			files.append(file)
		var pack:Dictionary={"name":"James original-registered West grip bridge v4 "+mode,"frameWidth":256,"frameHeight":256,"pivot":[128,224],"standingHeight":148,"precomposed":true,"status":"unselected_rectangular_torso_bridge_join_review_pending","states":[{"id":"carry-settle-west","frameCount":3,"frameFiles":files,"frameDurationsMs":[80,80,80],"loop":false,"facings":["west","west","west"]}]}
		var manifest:=FileAccess.open(OUT+mode+"-manifest-v4.json",FileAccess.WRITE);manifest.store_string(JSON.stringify(pack,"  "))
	var report:=FileAccess.open(OUT+"package-v4-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"rawBareRuler":353,"nominalRuler":148,"actualFullCellResize":[215,215],"alphaDustCutoff":32,"window":[80,110,84,69],"sources":evidence,"outsideWindowExactChecks":protected_checks,"originals":ORIGINALS,"selected":false,"scope":"Native deterministic generated coherent torso/hip rectangle on retained original paired sources. Outside rectangle RGBA exact, not semantic head-only or full anatomy acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"package-west-bridge-v4.gd.uid"):
		var uid:=FileAccess.open(OUT+"package-west-bridge-v4.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST BRIDGE V4: 6frames; ",protected_checks,"protected RGBA checks; unselected")
	quit(0)
