extends SceneTree
## Read-only source inspection: integer nearest-neighbor zoom, no source edits.
func _init() -> void:
	var source := ""
	var output := ""
	var region := Rect2i()
	var zoom := 1
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--source="): source=arg.trim_prefix("--source=")
		if arg.begins_with("--output="): output=arg.trim_prefix("--output=")
		if arg.begins_with("--zoom="): zoom=int(arg.trim_prefix("--zoom="))
		if arg.begins_with("--rect="):
			var parts:=arg.trim_prefix("--rect=").split(",")
			if parts.size()==4: region=Rect2i(int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3]))
	if not source.begins_with("res://rooms/") or not output.begins_with("res://output/") or output.contains("..") or FileAccess.file_exists(output) or FileAccess.file_exists(output+".json"):
		push_error("Use a room source and new output PNG beneath res://output/")
		quit(1)
		return
	var original:=Image.new()
	if original.load_png_from_buffer(FileAccess.get_file_as_bytes(source))!=OK or zoom<1 or zoom>16 or region.size.x<=0 or region.size.y<=0 or not Rect2i(Vector2i.ZERO,original.get_size()).encloses(region):
		push_error("Invalid source, bounded source rectangle, or integer zoom 1..16")
		quit(1)
		return
	var detail:=original.get_region(region)
	detail.resize(region.size.x*zoom,region.size.y*zoom,Image.INTERPOLATE_NEAREST)
	DirAccess.make_dir_recursive_absolute(output.get_base_dir())
	if detail.save_png(output)!=OK:
		push_error("Could not save diagnostic")
		quit(1)
		return
	var record:=FileAccess.open(output+".json",FileAccess.WRITE)
	record.store_string(JSON.stringify({"source":source,"source_sha256":FileAccess.get_sha256(source),"rect":[region.position.x,region.position.y,region.size.x,region.size.y],"integer_zoom":zoom,"interpolation":"nearest","output_sha256":FileAccess.get_sha256(output),"scope":"Diagnostic source crop only; not cleaned art or runtime acceptance"},"\t"))
	print("SOURCE DETAIL: ",region," at integer zoom ",zoom)
	quit()
