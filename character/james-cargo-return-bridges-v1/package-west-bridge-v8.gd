extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
const ORIGINALS={
	"bare":["res://character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png","res://character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png"],
	"helmet":["res://character/james-east-cargo-heads-v3/frames/helmet/carry-turn-east-west/010.png","res://character/james-cargo-material-joined-v1/frames/helmet/unload-west/000.png"]}
const EDGES=[0,443,887,1330,1774]
const SCALE=148.0/414.0
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"west-bridge-generated-v8.png")!=OK or raw.get_size()!=Vector2i(1774,887):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	var records:Array=[]
	var protected_checks:=0
	for row in range(2):
		var mode:String="bare" if row==0 else "helmet"
		var y0:int=0 if row==0 else 448
		var height:int=448 if row==0 else 439
		DirAccess.make_dir_recursive_absolute(OUT+"frames-v8/"+mode)
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
			var anchor:=Vector2i(roundi(128-foot_x*SCALE),roundi(224-sole*SCALE))
			var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
			frame.blit_rect(source,Rect2i(Vector2i.ZERO,resized),anchor)
			if col<2:
				var prior:=Image.new()
				if prior.load(OUT+"frames-v7/"+mode+"/%03d.png"%col)!=OK:quit(2);return
				prior.convert(Image.FORMAT_RGBA8)
				if mode=="bare":frame=prior.duplicate()
				else:
					var head:Image=frame.get_region(Rect2i(0,0,256,110))
					frame=prior.duplicate();frame.blit_rect(head,Rect2i(0,0,256,110),Vector2i.ZERO)
				for yy in range(256):
					for xx in range(256):
						if mode=="helmet" and yy<110:continue
						protected_checks+=1
						if frame.get_pixel(xx,yy)!=prior.get_pixel(xx,yy):push_error("Early candidate protection failed");quit(2);return
			var file:String="frames-v8/"+mode+"/%03d.png"%col
			if frame.save_png(OUT+file)!=OK:quit(2);return
			files.append(file)
			records.append({"mode":mode,"column":col,"cell":[cell.position.x,cell.position.y,cell.size.x,cell.size.y],"rawTop":top,"rawSole":sole,"rawFootX":foot_x,"anchor":[anchor.x,anchor.y],"resized":[resized.x,resized.y]})
		files.append(ORIGINALS[mode][1])
		var pack:Dictionary={"name":"James coherent whole-body West bridge v8 "+mode,"frameWidth":256,"frameHeight":256,"pivot":[128,224],"standingHeight":148,"precomposed":true,"status":"unselected_fullbody_source_review_pending","states":[{"id":"carry-settle-west","frameCount":6,"frameFiles":files,"frameDurationsMs":[80,80,80,80,80,80],"loop":false,"facings":["west","west","west","west","west","west"]}]}
		var output:=FileAccess.open(OUT+mode+"-joined-manifest-v8.json",FileAccess.WRITE);output.store_string(JSON.stringify(pack,"  "))
	var evidence:=FileAccess.open(OUT+"package-v8-evidence.json",FileAccess.WRITE)
	evidence.store_string(JSON.stringify({"rawSize":[1774,887],"rawBareRuler":414,"nominalRuler":148,"scale":SCALE,"alphaDustCutoff":32,"sources":records,"selected":false,"protectedCandidateRgbaChecks":protected_checks,"retainedV7Columns":[0,1],"helmetHeadWindow":[0,0,256,110],"scope":"V8 last two coherent body interiors at shared148/414 scale. First two bare interiors retained V7 RGBA exact; first two helmet lower bodies retained V7 exact, generated V8 heads above110. Original endpoints exact refs. Protection is against candidate, not original masters. New row boundary448 prevents neighboring row contamination. No per-frame grading/height normalization."},"  "))
	if not FileAccess.file_exists(OUT+"package-west-bridge-v8.gd.uid"):
		var uid:=FileAccess.open(OUT+"package-west-bridge-v8.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST BRIDGE V8: 8fullbody frames; shared148/414scale; original endpoints retained; unselected")
	quit(0)
