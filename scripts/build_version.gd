extends RefCounted
## One source for the game's version (project.godot application/config/version) and the build
## identity an export writes to res://build_info.json. Shown on the title screen, in Credits /
## Build and in bug reports (owner playtest, Sept 16).

static func version() -> String:
	return str(ProjectSettings.get_setting("application/config/version", "0.0.0"))

static func build() -> Dictionary:
	if OS.has_feature("editor"):
		return {"build_id":"unpackaged-source", "note":"Running editable source; release identities apply only to exported builds."}
	if FileAccess.file_exists("res://build_info.json"):
		var value = JSON.parse_string(FileAccess.get_file_as_string("res://build_info.json"))
		if value is Dictionary: return value
	return {"build_id":"unpackaged-source", "note":"No release manifest has been generated."}

# Short form for the title screen: "v0.5.0-prototype · dev" or "v0.5.0-prototype · build 3f2a91c0".
static func label() -> String:
	var id := str(build().get("build_id", "unpackaged-source"))
	return "v%s · %s" % [version(), "dev" if id == "unpackaged-source" else "build " + id.right(8)]

static func details() -> String:
	var info := build()
	var lines := ["VERSION  v" + version(), "BUILD  " + str(info.get("build_id", "unpackaged-source"))]
	if info.has("git_commit"): lines.append("COMMIT  %s%s" % [str(info.git_commit).left(12), " (modified)" if info.get("working_tree_modified", false) else ""])
	lines.append("ENGINE  " + str(Engine.get_version_info().string))
	return "\n".join(lines)
