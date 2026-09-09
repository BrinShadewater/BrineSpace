extends SceneTree
func _init() -> void:
	var game = load("res://scripts/main.gd").new()
	var sides := ["north", "east", "south", "west"]
	var count := 0
	for room in game.RoomDatabaseScript.all_rooms().values():
		var authored: Array = game.RoomDatabaseScript.get_layout(room.get("layout", "cross")).doors
		for rotation in range(4):
			var expected := []
			for side in authored: expected.append(sides[(sides.find(side)+rotation)%4])
			if room.id == "reactor": expected = sides.duplicate()
			assert(game._room_doors(room.id, rotation) == expected, "Authored ports survive lookup and rotation")
			var result: Array = game._room_doors(room.id, rotation)
			result.clear()
			assert(game._room_doors(room.id, rotation) == expected, "Callers cannot mutate cached ports")
			count += 1
	game.free()
	print("ROOM DOOR LOOKUP: PASS / ", count, " room/rotation cases")
	quit()
