extends SceneTree
func _init()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	for name in ["inventory_probe","allocate_uid"]:
		var path="res://character/james-west-carry-walk-keys-v1/selected-family-audit-v333/"+name+".gd.uid"
		if not FileAccess.file_exists(path):
			var file=FileAccess.open(path,FileAccess.WRITE)
			file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");file.close()
	print("JAMES UID pairing allocated for new review probes")
	quit(0)
