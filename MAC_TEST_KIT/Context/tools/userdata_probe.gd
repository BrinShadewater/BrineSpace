extends SceneTree
func _init()->void:
	var expected:String=""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--expected-user-dir="):expected=arg.trim_prefix("--expected-user-dir=")
	var actual:String=OS.get_user_data_dir().simplify_path()
	if expected.is_empty() or actual!=expected.simplify_path():
		push_error("Actual user directory mismatch: "+actual+" expected "+expected)
		quit(2)
		return
	print("MAC_USERDATA_VERIFIED ",actual)
	quit(0)
