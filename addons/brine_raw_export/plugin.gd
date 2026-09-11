@tool
extends EditorPlugin
class RawPNGs extends EditorExportPlugin:
	func _get_name() -> String: return "BRINE raw PNG and room JSON sources"
	func include_directory(path: String) -> void:
		for name in DirAccess.get_files_at(path):
			# Runtime room profiles are file reads, not imported resource links.
			# Include them directly even when the editor's file scan predates them.
			var extension := name.get_extension().to_lower()
			if extension=="png" or (extension=="json" and path.begins_with("res://rooms")):
				var source: String = path.path_join(name)
				add_file(source,FileAccess.get_file_as_bytes(source),false)
		for name in DirAccess.get_directories_at(path):
			if not name.begins_with("."): include_directory(path.path_join(name))
	func _export_begin(features: PackedStringArray,_debug: bool,_path: String,_flags: int) -> void:
		if features.has("room_validation") or features.has("menu_validation") or features.has("environment_validation"):
			for folder in ["rooms","character","Brine icons","brineui","mining-drone-animation","brinecore-animation","assets"]:
				var source: String = "res://"+folder
				if DirAccess.dir_exists_absolute(source): include_directory(source)
			return
		var manifest_path := "res://assets/runtime-release.json"
		var manifest = JSON.parse_string(FileAccess.get_file_as_string(manifest_path)) if FileAccess.file_exists(manifest_path) else null
		if not manifest is Dictionary or not manifest.get("files") is Array:
			push_error("Release manifest missing. Run tools/build_release_manifest.py before Windows Game export.")
			return
		for entry in manifest.files:
			var source: String = entry.path
			if not FileAccess.file_exists(source) or FileAccess.get_sha256(source) != entry.sha256:
				push_error("Release manifest is stale: " + source + ". Regenerate before exporting.")
				continue
			if source.get_extension().to_lower() in ["png","jpg","jpeg","webp"]:
				# Shipped rasters carry importer="keep" (tools/set_raw_png_import_keep.py)
				# and export raw through Godot's own pass; adding them here again
				# stored every texture twice in the pack.
				continue
			# Imported scene/audio/font dependencies are handled by Godot. These
			# sources are read directly at runtime and must also exist as raw bytes.
			if source.get_extension().to_lower() in ["png","jpg","jpeg","webp","svg","json","cfg","md"]:
				add_file(source,FileAccess.get_file_as_bytes(source),false)
		add_file("res://build_info.json",FileAccess.get_file_as_bytes("res://build_info.json"),false)

var exporter: RawPNGs
func _enter_tree() -> void:
	exporter=RawPNGs.new()
	add_export_plugin(exporter)
func _exit_tree() -> void:
	remove_export_plugin(exporter)
