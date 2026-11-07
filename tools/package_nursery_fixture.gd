extends SceneTree
## Local dependency smoke package, not a full-game release export.

func _init() -> void:
	var destination := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--package="):
			destination = arg.trim_prefix("--package=")
	if not destination.is_absolute_path() or FileAccess.file_exists(destination):
		push_error("Supply a new absolute --package=path.pck")
		quit(1)
		return
	var files: Array[String] = ["NOTICE.md", "rooms/modular/nursery.tscn", "rooms/modular/nursery_view.gd", "rooms/modular/nursery_view.gd.uid", "tools/modular_room_geometry.gd", "tools/modular_room_geometry.gd.uid", "tools/test_nursery_embedding.gd", "tools/test_nursery_embedding.gd.uid", "rooms/modular/nursery-room.json", "rooms/modular/nursery-card.png"]
	var recipe: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://rooms/modular/nursery-room.json"))
	for folder in recipe.asset_roots:
		files.append(str(folder).trim_prefix("res://") + "registration.json")
		var registration: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(str(folder) + "registration.json"))
		for record in registration.assets.values():
			if record.get("enabled_in_pilot", false):
				files.append(str(folder).trim_prefix("res://") + str(record.file))
	var pack := PCKPacker.new()
	var error := pack.pck_start(destination)
	if error == OK:
		error = pack.add_file("res://project.godot", "res://tools/nursery_fixture_project.godot")
	for path in files:
		if error != OK:
			break
		error = pack.add_file("res://" + path, "res://" + path)
	if error == OK:
		error = pack.flush()
	if error != OK:
		push_error("Nursery fixture packaging failed: " + error_string(error))
	else:
		print("PACKAGE PASS: %d explicit files including raw PNGs, JSON and structural dependency; %s" % [files.size() + 1, destination])
	quit(0 if error == OK else 1)
