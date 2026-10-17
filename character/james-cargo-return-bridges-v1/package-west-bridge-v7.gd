extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
const ORIGINALS={
	"bare":["res://character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png","res://character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png"],
	"helmet":["res://character/james-east-cargo-heads-v3/frames/helmet/carry-turn-east-west/010.png","res://character/james-cargo-material-joined-v1/frames/helmet/unload-west/000.png"]}
const EDGES=[0,443,887,1330,1774]
const SCALE=148.0/408.0
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"west-bridge-generated-v7.png")!=OK or raw.get_size()!=Vector2i(1774,887):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	var records:Array=[]
	var protected_checks:=0
	var prior:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"package-v6-evidence.json"))
	for row in range(2):
		var mode:String="bare" if row==0 else "helmet"
		var y0:int=0 if row==0 else 452
		var height:int=452 if row==0 else 435
		DirAccess.make_dir_recursive_absolute(OUT+"frames-v7/"+mode)
		var files:Array=[ORIGINALS[mode][0]]
		for col in range(4):
			var cell:=Rect2i(EDGES[col],y0,EDGES[col+1]-EDGES[col],height)
			var source:Image=raw.get_region(cell)
			var sole:=0;var top:=height
			for y in range(height):
				for x in range(cell.size.x):
					if source.get_pixel(x,y).a>=128.0/255.0:sole=maxi(sole,y+1);top=mini(top,y)
			if sole<=top:quit(2);return
			var left:=cell.size.x;var right:=0
			for y in range(maxi(top,sole-12),sole):
				for x in range(cell.size.x):
					if source.get_pixel(x,y).a>=128.0/255.0:left=mini(left,x);right=maxi(right,x+1)
			var foot_x:float=(left+right)*.5
			for y in range(height):
				for x in range(cell.size.x):
					if source.get_pixel(x,y).a<32.0/255.0:source.set_pixel(x,y,Color.TRANSPARENT)
			var resized:=Vector2i(roundi(cell.size.x*SCALE),roundi(height*SCALE))
			source.resize(resized.x,resized.y,Image.INTERPOLATE_LANCZOS)
			var old_anchor:Array=prior["sources"][row*4+col]["anchor"]
			var anchor:=Vector2i(old_anchor[0],old_anchor[1])
			var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
			frame.blit_rect(source,Rect2i(Vector2i.ZERO,resized),anchor)
			var prior_frame:=Image.new()
			if prior_frame.load(OUT+"frames-v6/"+mode+"/%03d.png"%col)!=OK:quit(2);return
			prior_frame.convert(Image.FORMAT_RGBA8)
			if mode=="bare":frame=prior_frame.duplicate()
			else:
				var head:Image=frame.get_region(Rect2i(0,0,256,110))
				frame=prior_frame.duplicate();frame.blit_rect(head,Rect2i(0,0,256,110),Vector2i.ZERO)
			for yy in range(256):
				for xx in range(256):
					if mode=="helmet" and yy<110:continue
					protected_checks+=1
					if frame.get_pixel(xx,yy)!=prior_frame.get_pixel(xx,yy):push_error("V6 body protection failed");quit(2);return
			var file:String="frames-v7/"+mode+"/%03d.png"%col
			if frame.save_png(OUT+file)!=OK:quit(2);return
			files.append(file)
			records.append({"mode":mode,"column":col,"cell":[cell.position.x,cell.position.y,cell.size.x,cell.size.y],"rawTop":top,"rawSole":sole,"rawFootX":foot_x,"anchor":[anchor.x,anchor.y],"resized":[resized.x,resized.y]})
		files.append(ORIGINALS[mode][1])
		var pack:Dictionary={"name":"James coherent whole-body West bridge v7 "+mode,"frameWidth":256,"frameHeight":256,"pivot":[128,224],"standingHeight":148,"precomposed":true,"status":"unselected_fullbody_source_review_pending","states":[{"id":"carry-settle-west","frameCount":6,"frameFiles":files,"frameDurationsMs":[80,80,80,80,80,80],"loop":false,"facings":["west","west","west","west","west","west"]}]}
		var output:=FileAccess.open(OUT+mode+"-joined-manifest-v7.json",FileAccess.WRITE);output.store_string(JSON.stringify(pack,"  "))
	var evidence:=FileAccess.open(OUT+"package-v7-evidence.json",FileAccess.WRITE)
	evidence.store_string(JSON.stringify({"rawSize":[1774,887],"rawBareRuler":408,"nominalRuler":148,"scale":SCALE,"alphaDustCutoff":32,"sources":records,"selected":false,"protectedCandidateRgbaChecks":protected_checks,"helmetHeadWindow":[0,0,256,110],"scope":"V6 bare interiors retained RGBA exact. V7 generated helmet/head window on V6 exact lower body, using V6 recorded registration and same shared scale. Protection is against candidate body, not original master. Original endpoints referenced exactly; no per-frame grade/height normalization. Full visual/native join admission pending."},"  "))
	if not FileAccess.file_exists(OUT+"package-west-bridge-v7.gd.uid"):
		var uid:=FileAccess.open(OUT+"package-west-bridge-v7.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST BRIDGE V7: 8fullbody frames; shared148/408scale; original endpoints retained; unselected")
	quit(0)
