extends SceneTree
const Rooms = preload("res://scripts/room_database.gd")
func _init() -> void:
	var first := Rooms.get_room("reactor")
	var original: Dictionary = Rooms.all_rooms()["reactor"]
	first.production.power = -999
	first.tags.append("fixture-only")
	assert(Rooms.get_room("reactor") == original, "Room callers must own nested data independently")
	var catalog := Rooms.all_rooms()
	catalog.reactor.cost.clear()
	assert(Rooms.get_room("reactor") == original, "Catalog mutation must not alter cached lookup templates")
	assert(Rooms.get_room("missing-room").is_empty())
	var begin := Time.get_ticks_usec()
	for iteration in range(10000):
		var room := Rooms.get_room("reactor")
		assert(room.id == "reactor")
	print("ROOM LOOKUP PASS: 10000 lookups in %d us" % (Time.get_ticks_usec() - begin))
	quit()
