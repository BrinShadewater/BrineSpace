extends SceneTree
## A stand-off nobody can step out of must not sweep every step-aside spot on every step. In a
## packaged soak (October 12, 2026) that was 52 spots and 4,992 route searches a frame for six
## seconds. The sweep is bounded per step and pauses after a full failure, and a stand-off that
## can be resolved still resolves at the nearest working spot.
const Passage = preload("res://scripts/crew_passage.gd")
var checks := 0
var failures := 0

## Only what the passage step reads; detour_around_crew counts calls and opens for one spot.
class Actor extends RefCounted:
	var active := true
	var dead := false
	var path := PackedVector2Array()
	var traffic_wait := 0.0
	var foot := Vector2.ZERO
	var direction := "south"
	var movement_medium := "dry"
	var state := "walk"
	var timer := 0.0
	var activity := ""
	var goal := "curiosity"
	var moonbay_assignment := {}
	var room_nodes := {}
	var graph := AStar2D.new()
	var avoidance_positions := PackedVector2Array()
	var avoidance_position := Vector2.INF
	var detours := 0
	var opening_spots: Array[Vector2] = []
	func helmet_action_active() -> bool: return false
	func can_step_aside() -> bool: return true
	func needs_air() -> bool: return true
	func cell_at(_point: Vector2) -> Vector2i: return Vector2i.ZERO
	func travel_segment_clear(_a: Vector2, _b: Vector2, _facing: String) -> bool: return true
	func crew_clear(_a: Vector2, _b: Vector2) -> bool: return true
	func travel_heading(_a: Vector2, _b: Vector2, fallback: String) -> String: return fallback
	func prepare_to_step_aside() -> void: pass
	func detour_around_crew() -> bool:
		detours += 1
		for spot in opening_spots:
			if avoidance_positions.has(spot): return true
		return false

const SPOTS := 20
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func spot(index: int) -> Vector2:
	# East of the yielder, nearest first, all further from the mover than the yielder is.
	return Vector2(32 + 20 + index * 2, 0)
func stand_off(opening: Array[Vector2]) -> Array:
	var mover := Actor.new()
	var yielder := Actor.new()
	yielder.foot = Vector2(32, 0)
	var ids := []
	for index in SPOTS:
		yielder.graph.add_point(index, spot(index))
		ids.append(index)
	ids.reverse() # Stored far-first; the sweep itself must order them nearest-first.
	yielder.room_nodes[Vector2i.ZERO] = ids
	mover.path = PackedVector2Array([Vector2(200, 0)])
	mover.traffic_wait = 1.0
	mover.avoidance_positions = PackedVector2Array([yielder.foot])
	mover.avoidance_position = yielder.foot
	mover.opening_spots = opening
	return [mover, yielder]
func _init() -> void:
	Passage.sweeps.clear()
	var per_step: int = Passage.SPOTS_PER_STEP
	check(per_step >= 1 and per_step < SPOTS, "Fixture has more spots than one step may test")

	# Nobody can step aside anywhere: bounded per step, every spot once, then a pause.
	var pair := stand_off([])
	var mover: Actor = pair[0]
	var yielder: Actor = pair[1]
	var steps := int(ceil(float(SPOTS) / per_step))
	var bounded := true
	for step in steps:
		var before := mover.detours
		if Passage.update(pair): bounded = false
		if mover.detours - before > per_step: bounded = false
	check(bounded, "A failing sweep tests at most SPOTS_PER_STEP spots a step and yields nobody")
	check(mover.detours == SPOTS, "A full sweep tests every step-aside spot exactly once")
	check(yielder.path.is_empty() and mover.path.size() == 1 and mover.avoidance_positions[0] == yielder.foot, "A failed sweep leaves both actors as they were")
	for step in 30: Passage.update(pair)
	check(mover.detours == SPOTS, "After a failed sweep the pair waits: no searches while the mover's wait has not advanced")
	mover.traffic_wait += Passage.RETRY_SECONDS - 0.02
	for step in 5: Passage.update(pair)
	check(mover.detours == SPOTS, "The pair still waits just short of the retry time")
	mover.traffic_wait += 0.04
	Passage.update(pair)
	check(mover.detours == SPOTS + per_step, "The sweep starts again once the retry time has passed")
	# A new stand-off (the mover's wait fell) never inherits the old sweep or its pause.
	for step in steps: Passage.update(pair)
	var paused_at := mover.detours
	Passage.update(pair)
	check(mover.detours == paused_at, "Second failed sweep pauses again")
	mover.traffic_wait = 0.3
	Passage.update(pair)
	check(mover.detours == paused_at + per_step, "A new stand-off sweeps at once, from the nearest spot")

	# A stand-off that can be resolved resolves, at the nearest spot that opens the route.
	Passage.sweeps.clear()
	var seventh := spot(6)
	pair = stand_off([spot(15), seventh])
	mover = pair[0]
	yielder = pair[1]
	var resolved_at := -1
	for step in steps:
		if Passage.update(pair):
			resolved_at = step
			break
	check(resolved_at == int(ceil(7.0 / per_step)) - 1, "A resolvable stand-off resolves as soon as the sweep reaches the working spot")
	check(mover.detours == 7, "The sweep stops at the first working spot")
	check(yielder.path.size() >= 1 and yielder.path[0] == seventh, "The yielder steps to the nearest working spot, as an unbounded sweep would choose")
	check(mover.traffic_wait == 0.0 and yielder.traffic_wait == 0.0, "Resolving clears both waits")
	check(not Passage.sweeps.has([mover.get_instance_id(), yielder.get_instance_id()]), "A resolved pair keeps no sweep record")
	check(mover.avoidance_positions[0] == yielder.foot and mover.avoidance_position == yielder.foot, "The mover's view of its peers is restored")
	Passage.sweeps.clear()
	print("CREW PASSAGE BUDGET: checks=", checks, " failures=", failures)
	quit(0 if failures == 0 else 1)
