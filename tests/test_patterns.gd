extends SceneTree
## Patterns: three-room chains that pay on top of the pair synergies inside them (owner-approved Sept 29).
const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const Synergies := preload("res://scripts/synergy_manager.gd")
var failures := 0

func _init() -> void:
	call_deferred("run")

func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _add_room(occupied: Dictionary, room_id: String, pos: Vector2i, rotation := 0) -> void:
	var room := RoomDatabaseScript.get_room(room_id).duplicate(true)
	room["pos"] = pos
	room["rotation"] = rotation
	occupied[pos] = room

func _count(links: Array, id: String) -> int:
	var count := 0
	for link in links:
		if str(link.get("id", "")) == id: count += 1
	return count

# Any arrangement of the three rooms (ends on any two sides of the middle, each turned any of four
# ways) that joins them through matching doors. Returns the rooms, or an empty dictionary.
func _layout(pattern: Dictionary) -> Dictionary:
	var ids: Array = pattern.rooms
	var sides := [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
	var middle := Vector2i(11, 11)
	for center in range(3):
		var others := []
		for index in range(3):
			if index != center: others.append(ids[index])
		for first in sides:
			for second in sides:
				if first == second: continue
				for r0 in range(4):
					for r1 in range(4):
						for r2 in range(4):
							var occupied := {}
							_add_room(occupied, ids[center], middle, r1)
							_add_room(occupied, others[0], middle + first, r0)
							_add_room(occupied, others[1], middle + second, r2)
							if _count(Synergies.evaluate(occupied.values(), occupied)["links"], str(pattern.id)) == 1: return occupied
	return {}

# A hallway piece joins two rooms that do not touch: middle, hallway, end, with the other end beside the
# middle. Returns the rooms, or an empty dictionary.
func _layout_through_hallway(pattern: Dictionary, hallway_id: String) -> Dictionary:
	var ids: Array = pattern.rooms
	var sides := [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
	var middle := Vector2i(11, 11)
	for center in range(3):
		var others := []
		for index in range(3):
			if index != center: others.append(ids[index])
		for first in sides:
			for second in sides:
				if first == second: continue
				for r0 in range(4):
					for r1 in range(4):
						for r2 in range(4):
							for rh in range(4):
								var occupied := {}
								_add_room(occupied, ids[center], middle, r1)
								_add_room(occupied, others[0], middle + first, r0)
								_add_room(occupied, hallway_id, middle + second, rh)
								_add_room(occupied, others[1], middle + second * 2, r2)
								for link in Synergies.evaluate(occupied.values(), occupied)["links"]:
									if str(link.id) == str(pattern.id) and link.cells.size() == 4: return occupied
	return {}

# One tee with a room on each of three sides, none touching another.
func _layout_tee_hub(pattern: Dictionary) -> Dictionary:
	var sides := [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]
	var hub := Vector2i(11, 11)
	for a in range(4):
		for b in range(4):
			for c in range(4):
				if a == b or b == c or a == c: continue
				for rt in range(4):
					for r0 in range(4):
						for r1 in range(4):
							for r2 in range(4):
								var occupied := {}
								_add_room(occupied, "tee_corridor", hub, rt)
								_add_room(occupied, pattern.rooms[0], hub + sides[a], r0)
								_add_room(occupied, pattern.rooms[1], hub + sides[b], r1)
								_add_room(occupied, pattern.rooms[2], hub + sides[c], r2)
								for link in Synergies.evaluate(occupied.values(), occupied)["links"]:
									if str(link.id) == str(pattern.id): return occupied
	return {}

func run() -> void:
	var patterns := Synergies.patterns()
	expect(patterns.size() == 11, "Eleven patterns are authored")
	expect(Synergies.pairs().size() + patterns.size() == Synergies.all_synergies().size(), "Pairs and patterns together are every synergy")
	for pattern in patterns:
		expect(pattern.rooms.size() == 3, "%s names three rooms" % pattern.name)
		expect(int(pattern.terminal_reward.research) == 5, "%s pays 5 Data when stabilized" % pattern.name)
		for room_id in pattern.rooms:
			expect(not RoomDatabaseScript.get_room(str(room_id)).is_empty(), "%s room %s exists" % [pattern.name, room_id])
		expect(not _layout(pattern).is_empty(), "%s can be built as a connected chain" % pattern.name)
		# Each pattern stands on two real pair synergies that share its middle room.
		var shared := 0
		for pair in Synergies.pairs():
			if pair.rooms.has(pattern.rooms[1]) and (pair.rooms.has(pattern.rooms[0]) or pair.rooms.has(pattern.rooms[2])): shared += 1
		expect(shared >= 2, "%s is built from at least two pair synergies" % pattern.name)
	# A chain missing its middle room, or with an end room out of reach, does not pay.
	var pattern: Dictionary = patterns[0]
	var apart := {}
	_add_room(apart, pattern.rooms[0], Vector2i(10, 10))
	_add_room(apart, pattern.rooms[2], Vector2i(14, 10))
	expect(_count(Synergies.evaluate(apart.values(), apart)["links"], str(pattern.id)) == 0, "Two end rooms with no middle room make no pattern")
	# Bonus and doubling work like any synergy, over all three cells.
	var line := _layout(pattern)
	var links: Array = Synergies.evaluate(line.values(), line)["links"]
	var link: Dictionary = {}
	for candidate in links:
		if str(candidate.id) == str(pattern.id): link = candidate
	expect(link.get("cells", []).size() == 3, "A pattern link carries all three cells")
	expect(int(Synergies.cycle_bonus([link]).get("food", 0)) == 2, "Field to Table pays +2 Food")
	expect(int(Synergies.cycle_bonus([link], {str(pattern.id): true}).get("food", 0)) == 4, "Stabilizing doubles a pattern's bonus")
	# Hallways connect patterns too: through a corridor between two rooms, and a tee joining all three.
	var through := _layout_through_hallway(pattern, "corridor")
	expect(not through.is_empty(), "%s can be joined through a corridor" % pattern.name)
	var hub := _layout_tee_hub(pattern)
	expect(not hub.is_empty(), "%s can be joined by a single tee corridor" % pattern.name)
	var depot: Dictionary = {}
	for candidate in patterns:
		if str(candidate.id) == "pattern_parts_depot": depot = candidate
	expect(not depot.is_empty() and not _layout_tee_hub(depot).is_empty(), "Parts Depot can be joined by a single tee corridor")
	var solo := {}
	_add_room(solo, "tee_corridor", Vector2i(11, 11))
	expect(_count(Synergies.evaluate(solo.values(), solo)["links"], str(pattern.id)) == 0, "A hallway alone makes no pattern")
	# In a real game: build one, power it, and it is discovered, then stabilizes on the third cycle.
	var TitleSettings = preload("res://scripts/title_settings.gd")
	TitleSettings.save_path = "user://patterns_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://patterns_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://patterns_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game._set_paused(true, false)
	game.testing_free_build = true
	game.wrecks.clear()
	var shift := Vector2i(20, 20) - Vector2i(11, 11)
	for cell in line:
		var room: Dictionary = line[cell]
		game._place_room(str(room.id), cell + shift, true)
		game.occupied[cell + shift]["rotation"] = int(room.rotation)
	game._check_synergies()
	var pattern_id := str(pattern.id)
	var connected := 0
	for seen in game.connected_synergy_links:
		if str(seen.id) == pattern_id: connected += 1
	expect(connected == 1, "The game sees the built pattern")
	for cell in line: game.powered_room_cells[cell + shift] = true
	game.active_synergy_links = preload("res://scripts/discovery_manager.gd").functioning_links(game.connected_synergy_links, game.powered_room_cells)
	var data_before := int(game.meta.total_research_points)
	for cycle in range(3):
		game._advance_synergy_discovery_cycle()
	expect(game.meta.discovered_synergy_ids.has(pattern_id), "A functioning pattern is discovered")
	expect(game.meta.stabilized_synergy_ids.has(pattern_id), "It stabilizes on the third functioning cycle")
	expect(int(game.meta.total_research_points) - data_before >= 10, "Stabilizing pays at least 10 Archived Data (5 + 5)")
	expect(game.toast_messages.size() > 0 or game.toast_playing, "A toast announced it")
	# Pair synergies link through hallways too, and never pay twice for the same two rooms.
	var closed := Synergies.get_synergy("closed_air_loop")
	var direct_pairs := 0
	var hallway_pairs := 0
	var both_routes := 0
	for r0 in range(4):
		for r1 in range(4):
			for rh in range(4):
				var gap := {}
				_add_room(gap, "life_support", Vector2i(10, 10), r0)
				_add_room(gap, "corridor", Vector2i(11, 10), rh)
				_add_room(gap, "hydroponics_bay", Vector2i(12, 10), r1)
				var found := 0
				for hit in Synergies.evaluate(gap.values(), gap)["links"]:
					if str(hit.id) == "closed_air_loop":
						found += 1
						if hit.get("hallway", false) and hit.cells.size() == 3 and hit.cells[2] == Vector2i(11, 10): hallway_pairs += 1
				if found > 1: both_routes += 1
	expect(hallway_pairs > 0, "Life Support and a Hydroponics Bay pay Closed Air Loop through a corridor")
	expect(both_routes == 0, "A pair never pays the same synergy twice for one route")
	# Joined directly and through a hallway at once: one link, and it is the direct one.
	var doubled := {}
	for r0 in range(4):
		for r1 in range(4):
			for rc in range(4):
				var square := {}
				_add_room(square, "life_support", Vector2i(10, 10), r0)
				_add_room(square, "hydroponics_bay", Vector2i(11, 10), r1)
				_add_room(square, "corner", Vector2i(10, 11), rc)
				_add_room(square, "corner", Vector2i(11, 11), (rc + 1) % 4)
				var count := 0
				var via := 0
				for hit in Synergies.evaluate(square.values(), square)["links"]:
					if str(hit.id) == "closed_air_loop":
						count += 1
						if hit.get("hallway", false): via += 1
				if count == 1 and via == 0: doubled = square
				expect(count <= 1, "Closed Air Loop pays at most once for one pair of rooms")
	expect(not closed.is_empty(), "Closed Air Loop exists")
	print("PATTERNS: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
