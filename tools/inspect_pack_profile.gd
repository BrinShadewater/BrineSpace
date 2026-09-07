extends SceneTree
## Read-only JSON/PNG diagnostic: mount an existing package, never export/repair it.
func _init() -> void:
	var args:=OS.get_cmdline_user_args()
	if args.size() not in [2,3]:
		push_error("Pass an existing PCK, res:// JSON or PNG asset and optional source path")
		quit(2)
		return
	if FileAccess.file_exists("res://project.godot"):
		push_error("Run with --path pointing to an empty directory to prevent checkout fallback")
		quit(2)
		return
	if not ProjectSettings.load_resource_pack(args[0],true):
		push_error("Package must mount")
		quit(2)
		return
	var path:=args[1]
	var bytes:=FileAccess.get_file_as_bytes(path)
	if path.get_extension().to_lower()=="png":
		var image:=Image.new()
		var status:=ERR_FILE_NOT_FOUND if bytes.is_empty() else image.load_png_from_buffer(bytes)
		print(JSON.stringify({"pack":args[0],"asset":path,"exists":FileAccess.file_exists(path),"bytes":bytes.size(),"sha256":FileAccess.get_sha256(path),"decode_status":status,"width":image.get_width(),"height":image.get_height()}))
		quit(0 if status==OK else 1)
		return
	var parser:=JSON.new()
	var status:=parser.parse(bytes.get_string_from_utf8())
	print(JSON.stringify({"pack":args[0],"profile":path,"exists":FileAccess.file_exists(path),"bytes":bytes.size(),"sha256":FileAccess.get_sha256(path),"prefix_hex":bytes.slice(0,24).hex_encode(),"parse_status":status,"error_line":parser.get_error_line(),"error":parser.get_error_message()}))
	if args.size()==3: print(FileAccess.get_file_as_string(args[2]))
	quit(0 if status==OK else 1)
