extends SceneTree

var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	var path := "res://scripts/room_footprint.gd"
	if not ResourceLoader.exists(path):
		check(false, "RoomFootprint helper is missing")
	else:
		var footprint = load(path)
		check(footprint.cells(Vector2i(4, 5), Vector2i.ONE) == [Vector2i(4, 5)], "Existing one-cell rooms occupy one cell")
		var four: Array = footprint.cells(Vector2i(4, 5), Vector2i(2, 2))
		check(four.size() == 4 and four.has(Vector2i(5, 6)), "A 2x2 room covers all four cells")
		var room := {"pos": Vector2i(4, 5), "size": Vector2i(2, 2), "rotation": 0,
			"ports": [
				{"cell": Vector2i(0, 0), "side": "north"},
				{"cell": Vector2i(1, 0), "side": "east"},
				{"cell": Vector2i(1, 1), "side": "south"},
				{"cell": Vector2i(0, 1), "side": "west"}]}
		var ports: Array = footprint.ports(room)
		check(ports.size() == 4, "Four ports remain four after placement")
		check(ports.has({"cell": Vector2i(4, 5), "side": "north"}), "Port uses an exact perimeter cell")
		room.rotation = 1
		ports = footprint.ports(room)
		check(ports.size() == 4 and ports.has({"cell": Vector2i(5, 5), "side": "east"}), "Rotation moves cell and side together")
		var invalid := room.duplicate(true)
		invalid.ports = [{"cell": Vector2i(0, 0), "side": "east"}]
		check(footprint.ports(invalid).is_empty(), "Internal seam cannot become an exterior door")
		check(footprint.exterior_cells(room, "north") == [Vector2i(4, 4), Vector2i(5, 4)], "Ocean side checks both exterior cells")
		var occupied := {Vector2i(4, 5): room, Vector2i(5, 5): room}
		check(footprint.room_at(occupied, Vector2i(5, 5)) == room, "Covered cells resolve to one room")
	print("ROOM FOOTPRINT ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
