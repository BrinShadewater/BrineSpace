extends RefCounted
## Scrapping a built room (owner, Sept 26): half its Metal back. Added with the emergency
## trickle after the seed-101 review run hit a zero-metal softlock; it also undoes a bad
## placement. Rescue wards, crew habs, the core, occupied rooms and rooms that hold other
## rooms to the core stay put.
const Architects=preload("res://scripts/architects.gd")
const Companions=preload("res://scripts/companions.gd")
const HullRepair=preload("res://scripts/hull_repair.gd")
const Expedition=preload("res://scripts/crew_expedition.gd")
const Footprint=preload("res://scripts/room_footprint.gd")

static func refund(room: Dictionary) -> int:
	return int(floor(float(room.get("cost", {}).get("metal", 0)) / 2.0))

# Why this room cannot be scrapped, or "" when it can.
static func blocker(game, cell: Vector2i) -> String:
	if not game.occupied.has(cell): return "Nothing built here."
	var room: Dictionary = game.occupied[cell]
	var covered: Array[Vector2i] = Footprint.cells(room.pos,room.get("size",Vector2i.ONE))
	if room.id == "brine_core": return "BRINE Core cannot be scrapped."
	if room.id == "crew_hab": return "A resident lives here."
	if room.id == "cryo_chamber" or room.get("recovered_derelict", false) or covered.any(func(part): return game.site_layout.get("recovery_cells", []).has(part) or Companions.is_site(game,part)):
		return "Recovery wards stay."
	for actor in Companions.all_actors(game):
		if actor.active and not actor.dead and covered.has(actor.cell_at(actor.foot)): return "Crew are inside."
	if _strands_rooms(game, room): return "Other rooms connect to the core through it."
	# Edge cases found in review (Sept 26): an away expedition returns through its airlock,
	# queued construction attaches to or is built from a neighbour, and a smaller store
	# would silently drop resources at the next cycle's clamp.
	for part in covered:
		if Expedition.reserved(game, part): return "An expedition returns here."
	for order in game.drone_fleet.orders:
		var at: Vector2i = order.get("pos", Vector2i(-9999, -9999))
		for part in covered:
			if absi(at.x - part.x) + absi(at.y - part.y) == 1 or order.get("work_cell", Vector2i(-9999, -9999)) == part:
				return "Construction next door depends on it."
	for key in room.get("storage", {}):
		if game.resources.has(key) and int(game.resources[key]) > game._get_resource_capacity(str(key)) - int(room.storage[key]):
			return "Stored resources exceed capacity without it."
	return ""

static func _core_cell(game) -> Vector2i:
	for room in game.placed_rooms:
		if room.id == "brine_core": return room.pos
	return Vector2i(-1, -1)

static func _reachable(game, skip: Dictionary) -> Dictionary:
	var core := _core_cell(game)
	var seen := {}
	if core == Vector2i(-1, -1): return seen
	var skipped := {}
	if not skip.is_empty():
		for part in Footprint.cells(skip.pos,skip.get("size",Vector2i.ONE)): skipped[part]=true
	seen[core] = true
	var queue: Array = [core]
	while not queue.is_empty():
		var current: Vector2i = queue.pop_back()
		for next in game._connected_neighbor_cells(current):
			if skipped.has(next) or seen.has(next): continue
			seen[next] = true
			queue.append(next)
	return seen

static func _strands_rooms(game, room: Dictionary) -> bool:
	var before := _reachable(game, {})
	var after := _reachable(game, room)
	var removed: Array[Vector2i] = Footprint.cells(room.pos,room.get("size",Vector2i.ONE))
	for other in before:
		if not removed.has(other) and not after.has(other): return true
	return false

# Returns the Metal refunded (0 when refused).
static func scrap(game, cell: Vector2i) -> int:
	if not blocker(game, cell).is_empty(): return 0
	var room: Dictionary = game.occupied[cell]
	var covered: Array[Vector2i] = Footprint.cells(room.pos,room.get("size",Vector2i.ONE))
	# A queued repair paid its Metal up front: refund the unused part and release the welder.
	if room.has("leak_repair"): HullRepair.cancel(game, room.pos)
	var metal := refund(room)
	game.placed_rooms.erase(room)
	for part in covered:
		game.occupied.erase(part)
		game.powered_room_cells.erase(part)
		game.unpowered_room_cells.erase(part)
	for id in Architects.IDS:
		var actor = Architects.actor_for(game, id)
		if covered.has(actor.primary_room): actor.primary_room = Vector2i(-1, -1)
		if covered.has(actor.goal_cell) and not actor.goal.is_empty():
			actor.goal = ""
			actor.path.clear()
	# Drones follow their bay; crew routes rebuild on their next topology check.
	game.drone_fleet.synchronize(game.placed_rooms)
	game.resources.metal = int(game.resources.metal) + metal
	game._log("Scrapped %s at %s: +%d Metal." % [room.display_name, cell, metal])
	game._check_synergies()
	game._apply_unlocks()
	return metal
