extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var protected_original:=0;var protected_body:=0;var sources:Array=[]
	for mode in ["bare","helmet"]:
		var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+mode+"-joined-manifest-v8.json"))
		var row:Dictionary=manifest.states[0];var endpoints:Array=row.frameFiles
		var files:Array=[endpoints[0]]
		DirAccess.make_dir_recursive_absolute(OUT+"frames-v9/"+mode)
		for col in range(4):
			var body:=Image.new();var original:=Image.new()
			var authority:String=endpoints[0] if col<2 else endpoints[-1]
			if body.load(OUT+"frames-v8/"+mode+"/%03d.png"%col)!=OK or original.load(authority)!=OK:quit(2);return
			body.convert(Image.FORMAT_RGBA8);original.convert(Image.FORMAT_RGBA8)
			var frame:Image=body.duplicate();frame.blit_rect(original,Rect2i(0,0,256,110),Vector2i.ZERO)
			for y in range(256):
				for x in range(256):
					if y<110:
						protected_original+=1
						if frame.get_pixel(x,y)!=original.get_pixel(x,y):push_error("Original upper region changed");quit(2);return
					else:
						protected_body+=1
						if frame.get_pixel(x,y)!=body.get_pixel(x,y):push_error("Candidate body changed");quit(2);return
			var file:String="frames-v9/"+mode+"/%03d.png"%col
			if frame.save_png(OUT+file)!=OK:quit(2);return
			files.append(file);sources.append({"mode":mode,"column":col,"upperAuthority":authority,"body":"frames-v8/"+mode+"/%03d.png"%col})
		files.append(endpoints[-1]);row.frameFiles=files
		manifest.name="James original-headed coherent West bridge v9 "+mode
		manifest.status="unselected_original_upper_region_native_join_review_pending"
		var output:=FileAccess.open(OUT+mode+"-joined-manifest-v9.json",FileAccess.WRITE);output.store_string(JSON.stringify(manifest,"  "))
	var report:=FileAccess.open(OUT+"package-v9-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"selected":false,"upperWindow":[0,0,256,110],"protectedOriginalRgbaChecks":protected_original,"protectedCandidateBodyRgbaChecks":protected_body,"sources":sources,"scope":"V8 coherent body exact below110; original endpoint upper rectangles exact above110, first two carry and last two unload. Not semantic head masks. No generated head resize or new grading. Head orientation switch/collar seam and full native motion/master match remain review requirements."},"  "))
	if not FileAccess.file_exists(OUT+"package-west-bridge-v9.gd.uid"):
		var uid:=FileAccess.open(OUT+"package-west-bridge-v9.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST BRIDGE V9: ",protected_original,"original upper and ",protected_body,"candidate body RGBA checks; unselected")
	quit(0)
