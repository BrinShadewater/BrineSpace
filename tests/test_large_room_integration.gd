extends SceneTree

const Main = preload("res://scripts/main.gd")
const Grid = preload("res://scripts/grid_canvas.gd")
const Flood = preload("res://scripts/room_flooding.gd")
const Fire = preload("res://scripts/room_fire.gd")
const Save = preload("res://scripts/run_save.gd")
const Footprint = preload("res://scripts/room_footprint.gd")

var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	var game = Main.new()
	game.grid_view = Grid.new()
	var large := {"id": "large_fixture", "pos": Vector2i(5, 5), "size": Vector2i(2, 2), "rotation": 0,
		"branch_owner": Vector2i(-1, -1), "water_level": 0.6, "fire": 0.3,
		"ports": [{"cell": Vector2i(0, 0), "side": "north"}, {"cell": Vector2i(1, 0), "side": "east"},
			{"cell": Vector2i(1, 1), "side": "south"}, {"cell": Vector2i(0, 1), "side": "west"}]}
	var neighbor := {"id": "tee_corridor", "pos": Vector2i(5, 4), "rotation": 0, "layout": "layout_01_tee",
		"branch_owner": Vector2i(-1, -1), "water_level": 0.0}
	game.placed_rooms = [large, neighbor]
	for cell in Footprint.cells(large.pos, large.size): game.occupied[cell] = large
	game.occupied[neighbor.pos] = neighbor
	if not game.has_method("_ports_connect"):
		check(false, "Perimeter-aware connection is missing")
	else:
		check(game.call("_ports_connect", large, neighbor, Vector2i(5, 5), Vector2i(5, 4)), "Matching north port connects at its cell")
		check(not game.call("_ports_connect", large, neighbor, Vector2i(6, 5), Vector2i(6, 4)), "Another north segment does not inherit the port")
		var rotated: Dictionary = large.duplicate(true)
		rotated.rotation = 1
		var east_neighbor := {"id": "tee_corridor", "pos": Vector2i(7, 5), "rotation": 0, "layout": "layout_01_tee"}
		check(game.call("_ports_connect", rotated, east_neighbor, Vector2i(6, 5), Vector2i(7, 5)), "Rotated port connects on its new edge cell")
		check(not game.call("_ports_connect", rotated, east_neighbor, Vector2i(6, 6), Vector2i(7, 6)), "Rotated neighboring segment stays closed")
		check(game.call("_ports_connect", large, large, Vector2i(5, 5), Vector2i(6, 5)), "Interior seam is traversable")
		var reachable: Array = game._connected_neighbor_cells(Vector2i(5, 5))
		check(reachable.has(Vector2i(6, 5)) and reachable.has(Vector2i(5, 6)) and reachable.has(Vector2i(5, 4)), "Crew graph reaches interior and matching exterior cells")
		var pairs: Array = Flood.connected_pairs(game)
		check(pairs.size() == 1, "Flood transfer counts only the one exterior door, never internal seams")
		large.doors_locked = true
		var before: float = large.water_level
		Flood.step_water(game, 0.1)
		check(is_equal_approx(float(large.water_level), before) and is_zero_approx(float(neighbor.water_level)), "Locked perimeter door isolates water")
		check(Fire.burning(game.occupied[Vector2i(6, 6)]) and game.placed_rooms.size() == 2, "All covered cells share one fire state")
		game.powered_room_cells[large.pos] = true
		check(game.powered_room_cells.size() == 1 and game.occupied[Vector2i(6, 6)].pos == large.pos, "Power tracks one large room at its anchor")
	var save_helper = Save.new()
	if not save_helper.has_method("occupancy_for_rooms"):
		check(false, "Save restore lacks footprint occupancy rebuild")
	else:
		var restored: Dictionary = save_helper.call("occupancy_for_rooms", [large, neighbor])
		check(restored.size() == 5 and restored[Vector2i(6, 6)] == large, "New save rebuilds all covered cells")
		check(save_helper.call("occupancy_for_rooms", [neighbor]).size() == 1, "Legacy room without size restores as 1x1")
	game.grid_view.free()
	game.free()
	print("LARGE ROOM INTEGRATION ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
