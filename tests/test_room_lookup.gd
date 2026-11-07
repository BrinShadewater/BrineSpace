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
	assert(not Rooms.has_room("missing-room") and not Rooms.has_room(""))
	for id in Rooms.all_rooms():
		assert(Rooms.has_room(id))
		assert(Rooms.room_color(id) == old_color(id), "Color lookup preserves every room override/category")
	assert(Rooms.room_color("missing-room") == old_color("missing-room"))
	first.category = "fixture-only"
	assert(Rooms.room_color("reactor") == old_color("reactor"), "Caller mutations do not change catalog colors")
	var old_color_expected := old_color("hydroponics_bay")
	for optimized_first in [false,true]:
		for optimized in [optimized_first,not optimized_first]:
			var start := Time.get_ticks_usec()
			for i in range(10000):
				var color: Color = Rooms.room_color("hydroponics_bay") if optimized else old_color("hydroponics_bay")
				assert(color == old_color_expected)
			print("ROOM COLOR %s 10000 calls: %d us" % ["direct" if optimized else "copy",Time.get_ticks_usec()-start])
	var begin := Time.get_ticks_usec()
	for iteration in range(10000):
		var room := Rooms.get_room("reactor")
		assert(room.id == "reactor")
	print("ROOM LOOKUP PASS: 10000 lookups in %d us" % (Time.get_ticks_usec() - begin))
	quit()

func old_color(id: String) -> Color:
	if Rooms.ROOM_COLORS.has(id): return Rooms.ROOM_COLORS[id]
	return Rooms.category_color(str(Rooms.get_room(id).get("category","")))
