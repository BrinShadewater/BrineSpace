extends SceneTree
func _init():call_deferred("run")
func run():
	var args:=OS.get_cmdline_user_args()
	if args.size()!=2 or FileAccess.file_exists("res://project.godot"):
		push_error("Run from an empty directory; pass PCK and expected manifest paths");quit(2);return
	if not ProjectSettings.load_resource_pack(args[0],true):quit(2);return
	var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(args[1]))
	var checked:=0;var missing:=0;var changed:=0;var remapped:=0
	for entry in manifest.files:
		if entry.path.get_extension().to_lower() not in ["png","jpg","jpeg","webp","svg","json","cfg","md"]:continue
		checked+=1
		if not FileAccess.file_exists(entry.path):
			# Scene/resource-referenced textures ship as imported .ctex through a
			# remap instead of raw bytes (see tools/set_raw_png_import_keep.py);
			# they must still be loadable from the mounted pack.
			if ResourceLoader.exists(entry.path):
				remapped+=1
			else:
				missing+=1;push_error("Pack omitted: "+entry.path)
		elif FileAccess.get_sha256(entry.path)!=entry.sha256:
			changed+=1;push_error("Pack differs: "+entry.path)
	print("RELEASE ASSET AUDIT: checked=%d missing=%d changed=%d remapped=%d"%[checked,missing,changed,remapped])
	quit(1 if missing+changed else 0)
