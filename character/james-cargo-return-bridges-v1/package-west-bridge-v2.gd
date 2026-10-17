extends SceneTree
const OUT="res://character/james-cargo-return-bridges-v1/"
func _init()->void:
	call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load(OUT+"west-bridge-generated-v2.png")!=OK:quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	if raw.get_size()!=Vector2i(1536,1024):quit(2);return
	var scale:float=148.0/450.0
	var evidence:Array=[]
	for row in range(2):
		var mode:String="bare" if row==0 else "helmet"
		DirAccess.make_dir_recursive_absolute(OUT+"frames/"+mode)
		var paths:Array=[]
		for col in range(3):
			var source:Image=raw.get_region(Rect2i(col*512,row*512,512,512))
			var sole:int=489 if row==0 else 477
			var left:=512;var right:=0
			for y in range(sole-35,sole):
				for x in range(512):
					if source.get_pixel(x,y).a>=128.0/255.0:left=mini(left,x);right=maxi(right,x+1)
			if right<=left:quit(2);return
			var foot_x:float=(left+right)*.5
			# Deterministic extraction only: remove low-alpha provider dust, then use
			# one pooled ruler for all six figures. No material or anatomy repainting.
			for y in range(512):
				for x in range(512):
					if source.get_pixel(x,y).a<32.0/255.0:source.set_pixel(x,y,Color.TRANSPARENT)
			source.resize(168,168,Image.INTERPOLATE_LANCZOS)
			var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
			var anchor:=Vector2i(roundi(128-foot_x*scale),roundi(224-sole*scale))
			frame.blit_rect(source,Rect2i(0,0,168,168),anchor)
			var file:String="frames/"+mode+"/%03d.png"%col
			if frame.save_png(OUT+file)!=OK:quit(2);return
			paths.append(file)
			evidence.append({"mode":mode,"index":col,"cell":[col*512,row*512,512,512],"rawFootX":foot_x,"rawSole":sole,"anchor":[anchor.x,anchor.y],"usedRect":str(frame.get_used_rect()),"file":file})
		var pack:Dictionary={"name":"James West held-cargo bridge v2 study "+mode,"frameWidth":256,"frameHeight":256,"pivot":[128,224],"standingHeight":148,"precomposed":true,"status":"unselected_source_study_paired_head_and_join_review_pending","states":[{"id":"carry-settle-west","frameCount":3,"frameFiles":paths,"frameDurationsMs":[80,80,80],"loop":false,"facings":["west","west","west"]}]}
		var manifest:=FileAccess.open(OUT+mode+"-manifest.json",FileAccess.WRITE);manifest.store_string(JSON.stringify(pack,"  "))
	var report:=FileAccess.open(OUT+"package-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"scale":scale,"rawBareRuler":450,"outputRuler":148,"alphaDustCutoff":32,"frames":evidence,"selected":false,"scope":"Six native deterministic extracted study frames; no controller, shared-head fidelity, paired-body equivalence or motion acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"package-west-bridge-v2.gd.uid"):
		var uid:=FileAccess.open(OUT+"package-west-bridge-v2.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WEST BRIDGE STUDY: 6frames exported; unselected")
	quit(0)
