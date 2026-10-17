extends SceneTree
func _init():
	assert(OS.get_environment("APPDATA").contains("brine-james-native-"))
	for path in ["res://character/james-meal-service-south-open-v1/native-contact.gd.uid","res://character/james-meal-service-south-open-v1/native-north-regression.gd.uid","res://character/james-meal-service-south-open-v1/prepare-uids.gd.uid"]:
		if FileAccess.file_exists(path):continue
		var file:=FileAccess.open(path,FileAccess.WRITE);file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close()
	print("South contact fixture UID pairs prepared")
	quit()
