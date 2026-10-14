extends RefCounted
## The Room Layout Studio's first opening in a session read the whole art catalogue (~190 ms)
## and loaded its first room's drawing code (~160 ms) in the frame it opened. While the title
## screen sits idle, both happen on worker threads instead (owner, October 14, 2026).
const Library = preload("res://scripts/room_asset_library.gd")
const EDITOR_CATALOG := "res://rooms/full-wall-v1/editor-catalog.json"
static var task := -1
static var built: Dictionary = {}
static var view_path := ""
## Held for the session so the loaded script stays in the resource cache.
static var view_script: Resource
static var exit_hooked := false

static func start() -> void:
	if task >= 0 or not view_path.is_empty(): return
	_hook_exit()
	if Library.catalog.is_empty():
		task = WorkerThreadPool.add_task(_build, false, "Studio art catalogue")
	var rooms: Variant = JSON.parse_string(FileAccess.get_file_as_string(EDITOR_CATALOG))
	if rooms is Array and not rooms.is_empty() and rooms[0] is Dictionary:
		var path := str(rooms[0].get("view", ""))
		if path.begins_with("res://") and view_script == null and not ResourceLoader.has_cached(path):
			if ResourceLoader.load_threaded_request(path) == OK: view_path = path

static func _build() -> void:
	built = Library.build_catalog()

## Before the Studio opens, and at exit: hand over what has loaded, waiting for any part that
## is still on its way. A worker task left running at exit crashes the process.
static func finish() -> void:
	if task >= 0:
		WorkerThreadPool.wait_for_task_completion(task)
		task = -1
		if Library.catalog.is_empty(): Library.catalog = built
		built = {}
	if not view_path.is_empty():
		view_script = ResourceLoader.load_threaded_get(view_path)
		view_path = ""

static func _hook_exit() -> void:
	if exit_hooked: return
	var tree := Engine.get_main_loop() as SceneTree
	if tree == null: return
	exit_hooked = true
	tree.root.tree_exiting.connect(finish)
