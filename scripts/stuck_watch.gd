extends RefCounted
## Watches for work that stops happening (owner request, Sept 17). Frame timings never show a
## crew member standing still with a job, a drone parked mid-route or a paid build nobody starts,
## so those are checked here: if nothing moves for a while, the station logs it once and the
## performance timeline records it, which makes the bug reportable instead of invisible.

const CREW_SECONDS := 30.0
const DRONE_SECONDS := 30.0
const ORDER_SECONDS := 90.0
const MOVED := 6.0 # World units that count as progress.

static var watched := {}
static var reported := {}

static func reset() -> void:
	watched.clear()
	reported.clear()

# Called every half second from the station. Returns the warnings raised this call.
static func check(game, dt: float) -> Array:
	var raised: Array = []
	if not game.running or game.paused: return raised
	for id in ["bill", "veld", "branforth", "marsh"]:
		var actor = preload("res://scripts/architects.gd").actor_for(game, id)
		if actor == null or not actor.active or actor.dead: continue
		var busy: bool = not str(actor.goal).is_empty() or not actor.path.is_empty()
		_track(raised, game, "crew:" + id, busy, actor.foot, CREW_SECONDS, dt,
			"%s has been stuck for %d seconds with the job '%s'" % [preload("res://scripts/architects.gd").NAMES.get(id, id), int(CREW_SECONDS), actor.goal if not str(actor.goal).is_empty() else actor.activity])
	for key in game.drone_fleet.drones:
		var drone: Dictionary = game.drone_fleet.drones[key]
		var working: bool = drone.phase != "docked" and not str(drone.get("job", "")).is_empty()
		_track(raised, game, "drone:" + str(key), working, Vector2(drone.position) * 384.0, DRONE_SECONDS, dt,
			"A %s drone from %s has not moved for %d seconds" % [str(drone.get("job", "idle")), key, int(DRONE_SECONDS)])
	for order in game.drone_fleet.orders:
		var cell = order.get("pos", order.get("cell", Vector2i(-1, -1)))
		_track(raised, game, "order:" + str(cell), true, Vector2(float(order.get("work", 0.0)), 0.0), ORDER_SECONDS, dt,
			"The build order at %s has made no progress for %d seconds" % [cell, int(ORDER_SECONDS)])
	return raised

static func _track(raised: Array, game, key: String, busy: bool, at: Vector2, limit: float, dt: float, message: String) -> void:
	if not busy:
		watched.erase(key)
		reported.erase(key)
		return
	var entry: Dictionary = watched.get(key, {"at": at, "still": 0.0})
	if Vector2(entry.at).distance_to(at) > MOVED:
		entry.at = at
		entry.still = 0.0
		reported.erase(key)
	else:
		entry.still = float(entry.still) + dt
	watched[key] = entry
	if float(entry.still) < limit or reported.has(key): return
	reported[key] = true
	raised.append(message)
	game._log("STUCK // " + message + ". Please send an F8 report.", true)
