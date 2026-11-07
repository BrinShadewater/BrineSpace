extends SceneTree
## Offline texture calibration. Original source art is never overwritten.
const Windows = preload("res://rooms/whole-room/ocean_windows.gd")
const OUT = "res://assets/ocean-windows-v3/calibrated"
func _init() -> void:
	if OS.get_environment("BRINE_WINDOW_TEST") != "isolated": quit(2); return
	if not OS.get_user_data_dir().replace("\\","/").contains("ocean-windows-v3/scratch-appdata/"): quit(2); return
	DirAccess.make_dir_recursive_absolute(OUT)
	var overrides: Dictionary={}
	if FileAccess.file_exists("res://assets/ocean-windows-v3/refined/registrations.json"):
		overrides=JSON.parse_string(FileAccess.get_file_as_string("res://assets/ocean-windows-v3/refined/registrations.json"))
	var catalog: Dictionary={}
	var total_bytes:=0
	for kind in Windows.SOURCES:
		var original: Array=Windows.SOURCES[kind]
		var path: String=original[0]
		var source: Rect2=original[1]
		if overrides.has(kind):
			path=overrides[kind].path
			var r: Array=overrides[kind].region
			source=Rect2(r[0],r[1],r[2],r[3])
		var image:=Image.new()
		if image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))!=OK: quit(1); return
		var mount:=Rect2(0,0,80,32)
		if kind.begins_with("square_"): mount=Windows.CENTER_MOUNT
		elif kind in ["corridor","tee_corridor"]: mount=Rect2(0,0,110,23)
		elif kind=="corner": mount=Rect2(0,0,78.4,23)
		var native: Vector2=Windows.fitted_rect(kind,mount).size
		var target:=Vector2i(roundi(native.x*5),roundi(native.y*5))
		var pixels:=image.get_region(Rect2i(source))
		pixels.fix_alpha_edges()
		pixels.resize(target.x,target.y,Image.INTERPOLATE_CUBIC)
		var padded:=Image.create(target.x+8,target.y+8,false,Image.FORMAT_RGBA8)
		padded.fill(Color.TRANSPARENT)
		padded.blit_rect(pixels,Rect2i(Vector2i.ZERO,target),Vector2i(4,4))
		var destination: String=OUT+"/"+kind+".png"
		if padded.save_png(destination)!=OK: quit(1); return
		catalog[kind]={"path":destination,"region":[4,4,target.x,target.y],"input":path,"input_region":[source.position.x,source.position.y,source.size.x,source.size.y],"density":5,"native_reference":[native.x,native.y]}
		total_bytes+=(target.x+8)*(target.y+8)*4
	var file:=FileAccess.open(OUT+"/catalog.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(catalog,"\t"));file.close()
	var uid_path: String=get_script().resource_path+".uid"
	if not FileAccess.file_exists(uid_path):
		file=FileAccess.open(uid_path,FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("WINDOW_CALIBRATION assets=",catalog.size()," rgba_bytes=",total_bytes," density=5")
	quit()
