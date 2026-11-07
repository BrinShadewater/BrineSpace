extends SceneTree
const Store = preload("res://scripts/room_layout_store.gd")
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok:
		failures += 1
		push_error(message)
func run():
	if DisplayServer.get_name() == "headless":
		quit(2)
		return
	Store.loaded = true
	Store.data = {}
	for q in range(4):
		Store.data["room-salvage_drone_bay/%d" % q] = {
			"full_wall_salvage-disassembly-wall": null,
			"salvage_rov": null, "salvage_hatch": null, "salvage_winch": null,
			"salvage_sorter": [-168, 110],
			"library/tileset-mms-73": [-24, -100]}
	Store.prime()
	var room = load("res://rooms/full-wall-v1/salvage_drone_bay_view.gd").new()
	room.embedded = true
	room.hide()
	root.add_child(room)
	for cycle in range(2):
		for q in range(4):
			room.configure_embedded(q, [], true, float(cycle))
			var ids: Array = []
			for prop in room.props: ids.append(str(prop.id))
			for removed in ["salvage_rov", "salvage_hatch", "salvage_winch", "full_wall_salvage-disassembly-wall"]:
				check(not ids.has(removed), "Deleted equipment restored q%d: %s" % [q, removed])
			check(ids.count("salvage_sorter") == 1, "Sorter lost or duplicated q%d" % q)
			check(ids.count("library/tileset-mms-73") == 1, "Bought tool storage lost or duplicated q%d" % q)
	print("SALVAGE SAVED DELETIONS: four rotations, repeated setup; %d failures" % failures)
	quit(1 if failures else 0)
