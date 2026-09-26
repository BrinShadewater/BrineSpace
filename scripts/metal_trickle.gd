extends RefCounted
## Emergency metal (owner, Sept 26). The seed-101 review run exhausted its surveyed deposits,
## spent down to 0 Metal and could never afford even a corridor to survey new seabed.
## BRINE Core reclaims scrap from its own frame: +1 Metal every INTERVAL cycles, only while
## Metal is below the cheapest room and no mining or salvage bay can harvest.
const CHEAPEST_ROOM_METAL := 2
const INTERVAL := 3

# Returns the Metal added this cycle.
static func apply(game) -> int:
	if not stuck(game, harvest_income(game)): return 0
	if int(game.cycle) % INTERVAL != 0: return 0
	game.resources.metal = int(game.resources.metal) + 1
	game._log("BRINE reclaims scrap from its own frame: +1 Metal.")
	return 1

static func stuck(game, has_income: bool) -> bool:
	return int(game.resources.metal) < CHEAPEST_ROOM_METAL and not has_income

static func harvest_income(game) -> bool:
	for room in game.placed_rooms:
		if room.id in ["mining_drone_bay", "salvage_drone_bay"] and str(game.drone_fleet.harvest_route_plan(room.pos, game.wrecks).get("state", "")) == "open": return true
	return false
