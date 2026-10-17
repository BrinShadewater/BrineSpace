extends SceneTree
func _init()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	for path in ["res://character/james-west-carry-walk-keys-v1/water-install-review-v347/installed_native_probe.gd.uid","res://character/james-west-carry-walk-keys-v1/water-install-review-v347/crew_regression.gd.uid","res://character/james-west-carry-walk-keys-v1/water-install-review-v347/allocate_uid.gd.uid"]:
		if not FileAccess.file_exists(path):FileAccess.open(path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	print("JAMES UID installed review scripts paired")
	quit(0)
