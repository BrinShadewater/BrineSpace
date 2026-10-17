extends SceneTree
func _init()->void:
	if not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return
	for path in ["res://character/james-floor-case-west-v1/rise_floor_state.gd","res://character/james-floor-case-west-v1/rise_floor_actor.gd","res://character/james-floor-case-west-v1/rise_floor_player.gd","res://character/james-floor-case-west-v1/pair_rise_uids.gd"]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("James rise helper script UIDs paired; artwork and motion inputs unchanged")
	quit(0)
