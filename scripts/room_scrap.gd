extends RefCounted
## Scrapping a built room (owner, Sept 26): half its Metal back. Added with the emergency
## trickle after the seed-101 review run hit a zero-metal softlock; it also undoes a bad
## placement. Rescue wards, crew habs, the core, occupied rooms and rooms that hold other
## rooms to the core stay put.
const Architects=preload("res://scripts/architects.gd")
const Companions=preload("res://scripts/companions.gd")

static func refund(room: Dictionary) -> int:
	return int(floor(float(room.get("cost", {}).get("metal", 0)) / 2.0))

# Why this room cannot be scrapped, or "" when it can.
static func blocker(game, cell: Vector2i) -> String:
	if not game.occupied.has(cell): return "Nothing built here."
	var room: Dictionary = game.occupied[cell]
	if room.id == "brine_core": return "BRINE Core cannot be scrapped."
	if room.id == "crew_hab": return "A resident lives here."
	if room.id == "cryo_chamber" or room.get("recovered_derelict", false) or game.site_layout.get("recovery_cells", []).has(cell) or Companions.is_site(game, cell):
		return "Recovery wards stay."
	for actor in Companions.all_actors(game):
		if actor.active and not actor.dead and actor.cell_at(actor.foot) == cell: return "Crew are inside."
	if _strands_rooms(game, cell): return "Other rooms connect to the core through it."
	return ""

static func _core_cell(game) -> Vector2i:
	for room in game.placed_rooms:
		if room.id == "brine_core": return room.pos
	return Vector2i(-1, -1)

static func _reachable(game, skip: Vector2i) -> Dictionary:
	var core := _core_cell(game)
	var seen := {}
	if core == Vector2i(-1, -1): return seen
	seen[core] = true
	var queue: Array = [core]
	while not queue.is_empty():
		var current: Vector2i = queue.pop_back()
		for next in game._connected_neighbor_cells(current):
			if next == skip or seen.has(next): continue
			seen[next] = true
			queue.append(next)
	return seen

static func _strands_rooms(game, cell: Vector2i) -> bool:
	var before := _reachable(game, Vector2i(-1, -1))
	var after := _reachable(game, cell)
	for other in before:
		if other != cell and not after.has(other): return true
	return false

# Returns the Metal refunded (0 when refused).
static func scrap(game, cell: Vector2i) -> int:
	if not blocker(game, cell).is_empty(): return 0
	var room: Dictionary = game.occupied[cell]
	var metal := refund(room)
	game.placed_rooms.erase(room)
	game.occupied.erase(cell)
	game.powered_room_cells.erase(cell)
	for id in Architects.IDS:
		var actor = Architects.actor_for(game, id)
		if actor.primary_room == cell: actor.primary_room = Vector2i(-1, -1)
		if actor.goal_cell == cell and not actor.goal.is_empty():
			actor.goal = ""
			actor.path.clear()
	# Drones follow their bay; crew routes rebuild on their next topology check.
	game.drone_fleet.synchronize(game.placed_rooms)
	game.resources.metal = int(game.resources.metal) + metal
	game._log("Scrapped %s at %s: +%d Metal." % [room.display_name, cell, metal])
	game._check_synergies()
	game._apply_unlocks()
	return metal
