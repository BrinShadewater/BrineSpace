extends SceneTree
## CI: load every tracked GDScript in ONE engine launch. The old step started Godot once
## per file (about six minutes for 400 scripts); this does the same check in seconds.
## Usage: godot --headless --path . -s tests/ci_parse_all.gd -- <file with one path per line>
func _init() -> void:
	var args:=OS.get_cmdline_user_args()
	var listing:=FileAccess.get_file_as_string(args[0]) if args.size()>0 else ""
	var failed: Array=[]
	var count:=0
	for line in listing.split("\n"):
		var path:=line.strip_edges()
		if not path.ends_with(".gd"): continue
		count+=1
		var script: Variant=ResourceLoader.load("res://"+path,"GDScript",ResourceLoader.CACHE_MODE_IGNORE)
		if script==null or not (script is GDScript) or not script.can_instantiate() and not script.is_abstract():
			failed.append(path)
	for path in failed: print("PARSE FAIL: "+path)
	print("%d script(s) checked, %d failed" % [count,failed.size()])
	quit(1 if not failed.is_empty() or count==0 else 0)
