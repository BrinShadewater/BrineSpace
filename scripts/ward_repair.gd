extends RefCounted
## Crew repair derelict wards in person (owner playtest, Sept 17). Starting a ward repair still
## pays its Metal and claims the one exterior rig, but the work only advances while a crew
## member stands in the connected room beside the shared door, welding toward the ward.

const Architects = preload("res://scripts/architects.gd")
const Companions = preload("res://scripts/companions.gd")
const WreckField = preload("res://scripts/wreck_field.gd")
const KINDS := ["cryo", "charging", "river", "josh", "margot"]
const REACH := 70.0

# The room a ward connects through, and which way the ward lies from it.
static func worksite(game, cell: Vector2i) -> Dictionary:
	var ward: Dictionary = game.wrecks.get(cell, {})
	if ward.is_empty(): return {}
	var door_room: String = Companions.ROOMS[ward.kind] if Companions.ROOMS.has(ward.kind) else "cryo_chamber"
	var rotation: int = int(ward.get("rotation", 0)) if ward.kind in ["cryo", "charging"] else 0
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		var neighbor: Vector2i = cell + offset
		if game.occupied.has(neighbor) and game._doors_connect(door_room, rotation, offset, game.occupied[neighbor]):
			return {"room": neighbor, "toward": -Vector2(offset)}
	return {}

# Transient job state: {cell, worker, point, work, status}. Welding time is handed to
# WreckField.advance each frame through take_work(); ward progress itself is what saves.
static func job(game) -> Dictionary:
	if not game.has_meta("ward_repair_job"): game.set_meta("ward_repair_job", {})
	return game.get_meta("ward_repair_job")

# Fixtures that exercise ward rewards rather than crew pathing switch this off to keep the old
# clock-driven progress; every normal run requires crew.
static var crew_required := true

static func use_clock(enabled := true) -> void:
	crew_required = not enabled

static func take_work(game) -> Variant:
	if not crew_required: return null
	var state := job(game)
	var work := {}
	if state.has("cell"):
		work[state.cell] = float(state.get("work", 0.0))
		state.work = 0.0
	return work

static func status(game, cell: Vector2i) -> String:
	var state := job(game)
	return str(state.get("status", "")) if state.get("cell", Vector2i(-1, -1)) == cell else ""

static func active_ward(game) -> Vector2i:
	for cell in game.wrecks:
		var ward: Dictionary = game.wrecks[cell]
		if ward.kind in KINDS and ward.get("active", false) and not ward.get("cleared", false): return cell
	return Vector2i(-1, -1)

# The weld spot is just inside the connected room, beside the doorway that leads to the ward
# (owner playtest: Marsh welded mid-room). Nearest standable spots are tried in order, and at
# most MAX_ROUTES searches run: a failed search explores the whole crew graph, and trying
# every nearby node each frame cost over a second per frame (F8 report 20260917-042558).
const MAX_ROUTES := 3
const RETRY_MSEC := 2000

static func approach(actor, room_cell: Vector2i, toward: Vector2) -> Dictionary:
	var center := (Vector2(room_cell) + Vector2.ONE * 0.5) * 384.0
	var desired := center + toward * 150.0 + Vector2(-toward.y, toward.x) * 48.0
	if actor.cell_at(actor.foot) == room_cell and actor.foot.distance_to(desired) < 24.0 and actor.can_stand(actor.foot):
		return {"point": actor.foot, "route": PackedVector2Array()}
	var start: int = actor.nearest_in_room(actor.foot, actor.cell_at(actor.foot))
	if start < 0: return {}
	var candidates: Array = []
	for node in actor.room_nodes.get(room_cell, []):
		var point: Vector2 = actor.graph.get_point_position(node)
		if point.distance_to(desired) <= REACH * 2.0 and actor.can_stand(point): candidates.append([point.distance_to(desired), node, point])
	candidates.sort_custom(func(a, b): return a[0] < b[0])
	for i in range(mini(MAX_ROUTES, candidates.size())):
		var path: PackedVector2Array = actor.route_between(start, candidates[i][1])
		if path.is_empty() or not actor.segment_clear(actor.foot, path[0]): continue
		return {"point": candidates[i][2], "route": path}
	return {}

# Called from the crew update chain; returns true while this crew member is on the job.
static func advance(game, actor, dt: float) -> bool:
	var id: String = "bill" if actor == game.bill_npc else "veld" if actor == game.veld_npc else "marsh" if actor == game.marsh_npc else "branforth"
	var state := job(game)
	var cell := active_ward(game)
	if cell.x < 0 or state.get("cell", cell) != cell:
		if actor.goal == "ward-repair": _release(actor)
		state.clear()
		if cell.x < 0: return false
	state.cell = cell
	var worker := str(state.get("worker", ""))
	if not worker.is_empty() and worker != id:
		var assigned = Architects.actor_for(game, worker)
		if assigned.dead or not Architects.present(game, worker) or assigned.goal != "ward-repair":
			state.worker = ""
			worker = ""
	if not worker.is_empty() and worker != id: return false
	if not game.running or game.paused: return actor.goal == "ward-repair"
	var eligible: bool = actor.expedition.is_empty() and not actor.helmet_action_active() and actor.locker_request.is_empty() and actor.goal not in ["construction", "hull-repair"] and actor.movement_medium == "dry"
	if not eligible:
		if actor.goal == "ward-repair":
			state.worker = ""
			_release(actor)
		return false
	var site := worksite(game, cell)
	if site.is_empty():
		state.status = "No connected room to work from"
		return false
	if worker.is_empty():
		if Time.get_ticks_msec() < int(state.get("retry_" + id, 0)): return false
		var found := approach(actor, site.room, site.toward)
		if found.is_empty():
			state.status = "Path blocked / crew cannot reach the ward door"
			state["retry_" + id] = Time.get_ticks_msec() + RETRY_MSEC
			return false
		state.worker = id
		state.point = found.point
		actor.path = found.route
		actor.goal = "ward-repair"
		actor.goal_cell = site.room
		actor.stage = ""
		actor.timer = 0
	var point: Vector2 = state.get("point", actor.foot)
	var who: String = Architects.NAMES.get(id, id)
	if actor.foot.distance_to(point) > 1:
		actor.activity = "heading to repair the derelict ward"
		state.status = "%s on the way" % who
		if actor.path.is_empty():
			var again := approach(actor, site.room, site.toward)
			if again.is_empty():
				state["retry_" + id] = Time.get_ticks_msec() + RETRY_MSEC
				state.worker = ""
				_release(actor)
				return true
			state.point = again.point
			actor.path = again.route
		actor.move(dt)
		return true
	actor.path.clear()
	var facing: Vector2 = site.toward
	actor.direction = "north" if facing.y < 0 else "south" if facing.y > 0 else "east" if facing.x > 0 else "west"
	actor.state = "weld"
	var ward: Dictionary = game.wrecks[cell]
	actor.activity = "repairing derelict ward / %d%%" % roundi(float(ward.progress) / WreckField.DURATION * 100.0)
	state.status = "%s welding" % who
	state.work = float(state.get("work", 0.0)) + dt * preload("res://scripts/research_tree.gd").repair_rate(game.meta)
	return true

static func _release(actor) -> void:
	actor.goal = ""
	actor.path.clear()
	actor.state = "idle"
	actor.timer = 0.5
