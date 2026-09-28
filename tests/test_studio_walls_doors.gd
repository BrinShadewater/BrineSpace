extends SceneTree
## Studio Walls / Wall Art / Doors (owner, Sept 27-28): the lists offer department looks,
## every room's painted riser and the door styles, and the choices reach the shell and the
## live door lookup.
const Editor = preload("res://scripts/room_layout_editor.gd")
const Store = preload("res://scripts/room_layout_store.gd")
const Shell = preload("res://rooms/whole-room/painted_shell.gd")
const Doors = preload("res://rooms/doors/painted_door.gd")
const DepartmentDoor = preload("res://rooms/doors/department_door.gd")
var failures := 0

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)

func items(editor) -> Array:
	var result: Array = []
	for i in editor.library_list.item_count:
		result.append([editor.library_list.get_item_text(i), str(editor.library_list.get_item_metadata(i))])
	return result

func show(editor, filter: int) -> Array:
	editor.library_filter.select(filter)
	editor.library_signature.clear()
	editor.rebuild_library()
	return items(editor)

func _init() -> void: call_deferred("run")

func run() -> void:
	Store.path = "res://output/studio-walls-doors/layouts.json"
	Store.loaded = true
	Store.data = {}
	preload("res://scripts/title_settings.gd").save_path = Store.path + ".cfg"
	var host := Control.new()
	root.add_child(host)
	var editor = Editor.open(host)
	editor.autosave_enabled = false
	editor.scale_actor.hide_all()
	for i in editor.entries.size():
		if editor.entries[i].room == "reactor": editor.index = i
	editor.load_room()
	await process_frame
	check(Shell.enabled(editor.room), "Reactor uses the painted shell")

	var walls := show(editor, Editor.TRAY_WALLS)
	check(walls.size() == 9 and walls[0][0] == "✓ Room default", "Walls lists the default and eight department looks: %d" % walls.size())
	var art := show(editor, Editor.TRAY_WALL_ART)
	check(art.size() == Shell.catalog().size() + 1 and art[0][0] == "✓ Room default", "Wall Art lists the default and every room's riser: %d" % art.size())
	check(art.any(func(e): return e[1] == "wall/riser:room:galley"), "Wall Art offers the galley's riser")
	var doors := show(editor, Editor.TRAY_DOORS)
	Doors.family_for("")
	check(doors.size() == Doors.catalog.styles.size() + 1 and doors[0][0] == "✓ Department default (engineering)", "Doors lists the ticked default and each style: " + str(doors.slice(0, 2)))

	# Choices save per rotation and reach the painted shell through the live draft.
	editor.apply_door_style("science")
	editor.apply_riser("room:galley")
	check(editor.draft.get("door/style") == "science" and editor.draft.get("wall/riser") == "room:galley", "Choices are saved in the draft")
	var ctx = Shell.context(editor.room)
	check(ctx.door_style() == "science", "Shell draws the chosen door style")
	check(ctx.registrations["reactor"].source == Shell.catalog()["galley"].base.source, "Shell borrows the galley's painted riser")
	check(show(editor, Editor.TRAY_DOORS)[0][0].begins_with("Department default") and show(editor, Editor.TRAY_DOORS).any(func(e): return e[0] == "✓ Science"), "The chosen door is ticked")
	editor.apply_door_style("")
	check(not editor.draft.has("door/style"), "Default clears the door choice")
	editor.queue_free()
	host.queue_free()
	await process_frame

	# Live doors: a saved style overrides the department table for that room and rotation.
	Store.data = {"room-reactor/1": {"door/style": "science"}}
	check(DepartmentDoor.department({"id": "reactor", "rotation": 1}) == "science", "Live door honours the saved style")
	check(DepartmentDoor.department({"id": "reactor", "rotation": 0}) == "engineering", "Other rotations keep the department door")
	Store.data = {"room-reactor/1": {"door/style": "not-a-style"}}
	check(DepartmentDoor.department({"id": "reactor", "rotation": 1}) == "engineering", "Unknown styles fall back to the department")
	check(not FileAccess.file_exists(Store.path), "The test never writes a layout file")
	print("STUDIO WALLS DOORS failures=", failures)
	quit(0 if failures == 0 else 1)
