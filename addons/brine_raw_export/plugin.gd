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
	func _export_begin(_features: PackedStringArray,_debug: bool,_path: String,_flags: int) -> void:
		for folder in ["rooms","character","Brine icons","brineui","mining-drone-animation","brinecore-animation","assets/environment","assets/drones"]:
			var source: String = "res://"+folder
			if DirAccess.dir_exists_absolute(source): include_directory(source)
var exporter: RawPNGs
func _enter_tree() -> void:
	exporter=RawPNGs.new()
	add_export_plugin(exporter)
func _exit_tree() -> void:
	remove_export_plugin(exporter)
