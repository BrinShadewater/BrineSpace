extends SceneTree
func _init():
	assert(OS.get_environment("APPDATA").contains("brine-james-native-"))
	var created:=0
	for path in ["res://character/james-case-release-south-v1/native-world.gd.uid","res://character/james-case-release-south-v1/native-indexed.gd.uid","res://character/james-case-release-south-v1/prepare-uids.gd.uid","res://character/james-case-release-north-v1/native-world.gd.uid","res://character/james-case-release-north-v1/native-indexed.gd.uid"]:
		if FileAccess.file_exists(path):
			var text:=FileAccess.get_file_as_string(path).strip_edges()
			if ResourceUID.id_to_text(ResourceUID.text_to_id(text))==text:continue
			print("Noncanonical newly generated fixture UID: ",path)
		var file:=FileAccess.open(path,FileAccess.WRITE)
		file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));file.close();created+=1
	print("Fixture UIDs created/corrected: ",created)
	quit()
