extends SceneTree

const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Footprint = preload("res://scripts/room_footprint.gd")
const CrewExpedition = preload("res://scripts/crew_expedition.gd")

var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	Rooms.get_room("corridor")
	Rooms._lookup_templates["large_fixture"] = {"id": "large_fixture", "display_name": "Large Fixture",
		"size": Vector2i(2, 2), "cost": {}, "ports": [{"cell": Vector2i(0, 0), "side": "north"},
		{"cell": Vector2i(1, 0), "side": "east"}, {"cell": Vector2i(1, 1), "side": "south"},
		{"cell": Vector2i(0, 1), "side": "west"}], "ocean_side": "west"}
	var game = Main.new()
	game.testing_free_build = true
	if not game.has_method("get_footprint_placement_problem"):
		check(false, "Footprint placement validation is missing")
	else:
		check(game.call("get_footprint_placement_problem", "large_fixture", Vector2i(39, 38), 0).contains("outside"), "Far edge rejects second column")
		check(game.call("get_footprint_placement_problem", "large_fixture", Vector2i(0, 8), 0).contains("ocean"), "Ocean hatch needs both exterior cells in bounds")
		game.occupied[Vector2i(6, 6)] = {"display_name": "Blocker", "id": "corridor"}
		check(game.call("get_footprint_placement_problem", "large_fixture", Vector2i(5, 5), 0).contains("contains"), "Collision checks every covered cell")
		game.occupied.clear()
		game.drone_fleet.sites[Vector2i(6, 6)] = {"active": true, "units": 1, "kind": "mining", "discovered": true}
		check(not game.call("get_footprint_placement_problem", "large_fixture", Vector2i(5, 5), 0).is_empty(), "Deposit in second row blocks room")
		game.drone_fleet.sites.clear()
		game.wrecks[Vector2i(6, 6)] = {"kind": "basalt", "cleared": false}
		check(not game.call("get_footprint_placement_problem", "large_fixture", Vector2i(5, 5), 0).is_empty(), "Wreck in second row blocks room")
		game.wrecks.clear()
		game.occupied[Vector2i(6, 4)] = {"display_name": "Intake Blocker", "id": "corridor"}
		check(game.call("get_footprint_placement_problem", "large_fixture", Vector2i(5, 5), 1).contains("ocean"), "Rotation moves the ocean-facing wall")
		game.occupied.clear()
		game.drone_fleet.enqueue("large_fixture", Vector2i(5, 5), 0)
		check(game.drone_fleet.reserved(Vector2i(6, 6)), "Queue reserves all four cells")
		check(game.call("get_footprint_placement_problem", "large_fixture", Vector2i(6, 6), 0).contains("construction"), "Queued build blocks overlapping footprint")
		check(game.call("get_footprint_placement_problem", "tee_corridor", Vector2i(4, 6), 0).contains("ocean"), "Queued ocean face is reserved before construction completes")
		game.drone_fleet.orders.clear()
		game.occupied[Vector2i(10, 10)] = {"display_name": "Late Blocker", "id": "corridor"}
		game.call("_place_room", "large_fixture", Vector2i(9, 9), true)
		check(game.placed_rooms.is_empty() and not game.occupied.has(Vector2i(9, 9)), "Interrupted build cannot occupy a partial footprint")
		game.occupied.clear()
		game.occupied[Vector2i(4,5)] = {"display_name":"Late Ocean Blocker","id":"corridor"}
		game.call("_place_room", "large_fixture", Vector2i(5, 5), false, true)
		check(game.placed_rooms.is_empty(), "Completion rechecks ocean exposure before building")
		game.occupied.clear()
		game.call("_place_room", "large_fixture", Vector2i(5, 5), true)
		var expected := Footprint.cells(Vector2i(5, 5), Vector2i(2, 2))
		check(game.placed_rooms.size() == 1, "Large room is one placed room")
		check(expected.all(func(cell): return game.occupied.has(cell)), "Placed room occupies all four cells atomically")
		check(expected.all(func(cell): return CrewExpedition.blockers(game).has(cell)), "Exterior routes respect all four occupied cells")
		check(game.get_placement_problem("tee_corridor",Vector2i(7,6)).contains("Door does not match"), "Small room cannot connect through a closed 2x2 edge")
		check(game.get_placement_problem("tee_corridor",Vector2i(7,5)).is_empty(), "Small room can connect to the exact 2x2 east port")
		check(game.get_footprint_placement_problem("tee_corridor",Vector2i(4,6),0).contains("ocean"), "Built room keeps its ocean launch wall clear")
	game.free()
	print("LARGE ROOM PLACEMENT ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
