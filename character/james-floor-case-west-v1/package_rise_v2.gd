extends SceneTree
const OUT="res://character/james-floor-case-west-v1/"
func _init()->void:call_deferred("run")
func run()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	var raw:=Image.new()
	if raw.load("res://character/james-floor-case-west-v1/rise-generated-v2.png")!=OK or raw.get_size()!=Vector2i(1254,1254):quit(2);return
	raw.convert(Image.FORMAT_RGBA8)
	var scale:=44.0/148.0
	var cells:Array=[]
	for mode in ["bare","helmet"]:
		var row:int=0 if mode=="bare" else 1
		DirAccess.make_dir_recursive_absolute(OUT+"rise-v2/"+mode)
		for col in range(2):
			var crop:=Rect2i(col*627,row*627,627,627)
			var image:Image=raw.get_region(crop)
			for y in range(image.get_height()):
				for x in range(image.get_width()):
					if image.get_pixel(x,y).a<32.0/255.0:image.set_pixel(x,y,Color.TRANSPARENT)
			var size:=Vector2i(roundi(627*scale),roundi(627*scale))
			image.resize(size.x,size.y,Image.INTERPOLATE_LANCZOS)
			var case_left:int=203 if col==0 else 772
			var case_floor:int=(617 if col==0 else 618) if row==0 else 1192
			var placement:=Vector2i(roundi(75-(case_left-crop.position.x)*scale),roundi(222-(case_floor-crop.position.y)*scale))
			var frame:=Image.create(256,256,false,Image.FORMAT_RGBA8);frame.fill(Color.TRANSPARENT)
			frame.blit_rect(image,Rect2i(Vector2i.ZERO,size),placement)
			var path:String=OUT+"rise-v2/"+mode+"/%03d.png"%col
			if frame.save_png(path)!=OK:quit(2);return
			cells.append({"mode":mode,"index":col,"source":path,"crop":[crop.position.x,crop.position.y,627,627],"sharedScale":scale,"cell":[size.x,size.y],"caseLeftRaw":case_left,"caseFloorRaw":case_floor,"placement":[placement.x,placement.y]})
	var file:=FileAccess.open(OUT+"rise-v2-package-evidence.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"selected":false,"raw":"rise-generated-v2.png","cells":cells,"canvas":[256,256],"pivot":[128,224],"standingHeight":148,"scope":"Native shared scale from original44px case width/reference raw148ruler; per-cell authored case left/floor landmarks translated to75/222. No per-pose height normalization or grade/axis warp. Draft original endpoint/helmet/proportion/spacing review pending."},"  "))
	if not FileAccess.file_exists(OUT+"package_rise_v2.gd.uid"):
		var uid:=FileAccess.open(OUT+"package_rise_v2.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES RISE V2 PACKAGE: four paired interiors; common44/148scale; p128224/H148; unselected")
	quit(0)
