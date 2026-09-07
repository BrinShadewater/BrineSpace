extends SceneTree
## Checkout-independent dependency smoke pack; not a release export.
var files: Dictionary = {}
var failures: Array[String] = []

func include_path(path: String) -> void:
	# A fixture's output directory is a write destination, never an input asset.
	if path == "res://output" or path.begins_with("res://output/"): return
	if files.has(path): return
	if DirAccess.dir_exists_absolute(path):
		for child in DirAccess.get_files_at(path):
			if child.get_extension() in ["png", "jpg", "json"]:
				include_path(path.path_join(child))
		for child in DirAccess.get_directories_at(path):
			include_path(path.path_join(child))
		return
	if not FileAccess.file_exists(path):
		failures.append(path)
		return
	files[path] = true
	# Raw image consumers and RichTextLabel resource consumers coexist. Keep
	# both the source bytes and Godot's import remap/dependency when available.
	if FileAccess.file_exists(path + ".import"):
		include_path(path + ".import")
	if path.get_extension() == "gd" and FileAccess.file_exists(path + ".uid"):
		files[path + ".uid"] = true
	if path.get_extension() not in ["gd", "tscn", "godot", "json", "import"]: return
	var source := FileAccess.get_file_as_string(path)
	var pattern := RegEx.new()
	pattern.compile('"(res://[^"\\n]+)"')
	for match in pattern.search_all(source):
		var dependency: String = match.get_string(1)
		# Runtime animation loaders construct filenames under these directories.
		if "%" in dependency:
			dependency = dependency.substr(0, dependency.find("%")).get_base_dir()
		if dependency.begins_with("res://output/") or dependency == "res://": continue
		include_path(dependency)

func _init() -> void:
	var destination := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--package="): destination = arg.trim_prefix("--package=")
	if not destination.is_absolute_path() or FileAccess.file_exists(destination):
		push_error("Supply a new absolute --package=path.pck")
		quit(1)
		return
	include_path("res://project.godot")
	include_path("res://NOTICE.md")
	include_path("res://tests/playtest_underwater_station.gd")
	if "--finite-harvest" in OS.get_cmdline_user_args():
		include_path("res://tests/playtest_finite_harvest.gd")
		include_path("res://tests/test_finite_harvest.gd")
	if "--drone-fleet" in OS.get_cmdline_user_args():
		# Crew manifests contain relative frame paths outside their final/ folder.
		include_path("res://character")
		include_path("res://tests/playtest_drone_fleet.gd")
		include_path("res://tests/test_drone_jobs.gd")
		include_path("res://assets/drones/fleet-v1/")
	if "--production-ten" in OS.get_cmdline_user_args():
		include_path("res://rooms/production-ten/manifest.json")
		include_path("res://tests/test_production_ten_connections.gd")
		var batch: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/production-ten/manifest.json"))
		for entry in batch:
			include_path("res://"+entry.integration.view)
			include_path("res://"+entry.integration.card)
			include_path("res://tests/playtest_"+entry.id+".gd")
	if not failures.is_empty():
		push_error("Unresolved package dependencies: " + str(failures))
		quit(1)
		return
	var pack := PCKPacker.new()
	var error := pack.pck_start(destination)
	var paths := files.keys()
	paths.sort()
	var records: Array = []
	for path in paths:
		if error != OK: break
		error = pack.add_file(path, path)
		records.append({"path": path, "sha256": FileAccess.get_sha256(path)})
	if error == OK: error = pack.flush()
	if error == OK:
		var manifest := FileAccess.open(destination + ".json", FileAccess.WRITE)
		manifest.store_string(JSON.stringify({"scope": "Station fixture dependencies, raw assets; not release export", "files": records}, "\t"))
		print("STATION PACKAGE PASS: %d files; %s" % [files.size(), destination])
	else: push_error(error_string(error))
	quit(0 if error == OK else 1)
