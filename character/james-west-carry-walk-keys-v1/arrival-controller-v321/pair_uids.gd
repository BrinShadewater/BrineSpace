extends SceneTree
func _init()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	for path in ["res://character/james-west-carry-walk-keys-v1/arrival-controller-v321/crew_regression.gd.uid","res://character/james-west-carry-walk-keys-v1/arrival-controller-v321/pair_uids.gd.uid"]:
		if not FileAccess.file_exists(path):
			var file:=FileAccess.open(path,FileAccess.WRITE)
			file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES new helper resource UIDs paired")
	quit(0)
