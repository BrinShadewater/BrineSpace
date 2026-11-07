extends SceneTree
## List saved drafts; --promote=asset/quarter adopts one validated draft.
const Store=preload("res://scripts/room_layout_store.gd")
const Editor=preload("res://scripts/room_layout_editor.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var promote:=""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--promote="): promote=arg.trim_prefix("--promote=")
		elif arg.begins_with("--draft-file="): Store.path=arg.trim_prefix("--draft-file=")
		elif arg.begins_with("--defaults-file="): Store.defaults_path=arg.trim_prefix("--defaults-file=")
	Store.ensure_loaded()
	print("Saved layouts: "+ProjectSettings.globalize_path(Store.path))
	print(JSON.stringify(Store.data,"  "))
	if promote.is_empty(): quit(); return
	if not Store.data.has(promote): push_error("No saved draft for "+promote); quit(1); return
	var editor=Editor.open(root)
	var found:=false
	for i in range(editor.entries.size()):
		for q in range(4):
			if Store.key(editor.entries[i].asset,q)==promote:
				editor.index=i; editor.quarter=q; found=true
	if not found: push_error("Unknown room or rotation"); quit(1); return
	editor.load_room()
	var problems: PackedStringArray=editor.issues()
	if not problems.is_empty(): push_error("Draft needs correction: "+str(problems)); quit(1); return
	var document: Dictionary={"version":1,"layouts":{}}
	if FileAccess.file_exists(Store.defaults_path):
		var parsed=JSON.parse_string(FileAccess.get_file_as_string(Store.defaults_path))
		if not parsed is Dictionary or parsed.get("version",0)!=1 or not parsed.get("layouts") is Dictionary:
			push_error("Invalid defaults file; preserved without changes"); quit(1); return
		document=parsed
	document.layouts[promote]=Store.positions(editor.entries[editor.index].asset,editor.quarter)
	var file:=FileAccess.open(Store.defaults_path+".tmp",FileAccess.WRITE)
	if file==null: push_error("Cannot write defaults"); quit(1); return
	file.store_string(JSON.stringify(document,"\t")+"\n"); file.close()
	var error:=DirAccess.rename_absolute(ProjectSettings.globalize_path(Store.defaults_path+".tmp"),ProjectSettings.globalize_path(Store.defaults_path))
	if error!=OK: push_error(error_string(error)); quit(1); return
	print("PROMOTED "+promote+" to "+Store.defaults_path+"; local draft preserved.")
	editor.close_editor()
	await process_frame
	quit()
