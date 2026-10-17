extends "res://scripts/bug_report.gd"
var qa_profile_verified := false
func _enter_tree() -> void:
	var expected := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--user-dir="): expected = arg.trim_prefix("--user-dir=")
	qa_profile_verified = not expected.is_empty() and OS.get_user_data_dir().replace("\\", "/").simplify_path() == expected.replace("\\", "/").simplify_path()
	if not qa_profile_verified:
		push_error("Packaged profile isolation mismatch; refusing session writes")
		get_tree().quit(2)
		return
	super._enter_tree()
func _ready() -> void:
	if qa_profile_verified: super._ready()
