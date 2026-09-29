extends RefCounted
## Tells the player when an extraction bay has nothing left to do (owner playtest, Sept 29: "Why isn't
## the mining drone mining?"). The reason already lived in the bay's inspector, below the fold; now a
## toast and a log line say it once when the bay stalls, and again only after it has worked in between.
## Read-only: it never changes drone jobs, rewards or movement.

const BAYS := ["mining_drone_bay", "salvage_drone_bay"]
const CHECK_SECONDS := 3.0
static var announced: Dictionary = {}   # bay cell -> state already announced
static var _checked_at := -100.0
static var _game_id := 0

static func direction_word(offset: Vector2) -> String:
	if absf(offset.x) >= absf(offset.y): return "east" if offset.x > 0 else "west"
	return "south" if offset.y > 0 else "north"

# The nearest deposit of this kind that no room has surveyed yet, or (-1, -1).
static func nearest_unsurveyed(fleet, home: Vector2i, kind: String) -> Vector2i:
	var best := Vector2i(-1, -1)
	var best_distance := INF
	for cell in fleet.sites:
		var site: Dictionary = fleet.sites[cell]
		if site.kind != kind or site.discovered or not site.active or site.units <= 0: continue
		var distance := Vector2(cell).distance_to(Vector2(home))
		if distance < best_distance:
			best_distance = distance
			best = cell
	return best

static func message(fleet, home: Vector2i, wrecks: Dictionary) -> String:
	var plan: Dictionary = fleet.harvest_route_plan(home, wrecks)
	if str(plan.state) not in ["depleted", "sealed", "recover", "clear"]: return ""
	var kind := str(plan.get("kind", "mining"))
	var noun := "MINING BAY" if kind == "mining" else "SALVAGE BAY"
	if str(plan.state) != "depleted":
		return "%s idle / %s" % [noun, fleet.harvest_route_hint(home, wrecks)]
	var target := nearest_unsurveyed(fleet, home, kind)
	if target.x < 0: return "%s idle / every deposit is spent and none remain unsurveyed" % noun
	var offset := Vector2(target - home)
	return "%s idle / every surveyed %s is spent. The nearest unsurveyed one is about %d cells %s: build a room within 5 cells of it to survey it." % [noun, "deposit" if kind == "mining" else "scrap pile", roundi(offset.length()), direction_word(offset)]

# Called from main's half-second refresh.
static func refresh(game) -> void:
	if not game.running or game.paused: return
	var now := Time.get_ticks_msec() / 1000.0
	if game.get_instance_id() != _game_id:
		_game_id = game.get_instance_id()
		announced.clear()
	if now - _checked_at < CHECK_SECONDS: return
	_checked_at = now
	var fleet = game.drone_fleet
	var present := {}
	for room in game.placed_rooms:
		if str(room.id) not in BAYS or room.get("suspended", false): continue
		var home: Vector2i = room.pos
		present[home] = true
		var drone: Dictionary = fleet.drones.get(home, {})
		var idle: bool = not drone.is_empty() and drone.phase == "docked" and drone.job.is_empty() and drone.get("route_wait", false) and game.powered_room_cells.has(home)
		if not idle:
			announced.erase(home)
			continue
		var text := message(fleet, home, game.wrecks)
		if text.is_empty() or announced.get(home, "") == text: continue
		announced[home] = text
		game._log(text, true)
		game._queue_center_toast(text)
	for home in announced.keys():
		if not present.has(home): announced.erase(home)
