extends SceneTree
## Crew swim or walk per room (room_flooding.step_crew), so a swimmer's route plans dry rooms
## with the walking check (owner, Sept 26). Branforth, swimming in a flooded reactor, could
## not route to a crew hab whose furniture blocks a swimming outline; every failing search
## explored the whole station.
const WET := Vector2i(0,0)
var failures := 0

class TightDryRoom extends "res://scripts/bill_npc.gd":
	# The swimming outline fits nowhere deeper than x=400 (inside the dry room's furniture).
	func segment_clear(_a: Vector2, _b: Vector2) -> bool: return true
	func swim_segment_clear(a: Vector2, b: Vector2, _facing: String, _previous: String = "", _treading: bool = false, _extent: Array = []) -> bool:
		return a.x <= 400 and b.x <= 400

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func build() -> TightDryRoom:
	var actor := TightDryRoom.new()
	actor.movement_medium = "flooded"
	actor.direction = "east"
	var points := [Vector2(100,100),Vector2(200,100),Vector2(300,100),Vector2(390,100),Vector2(500,100),Vector2(600,100)]
	for i in range(points.size()):
		actor.graph.add_point(i, points[i])
		if i > 0: actor.graph.connect_points(i-1, i)
	actor.foot = points[0]
	return actor

func run() -> void:
	var unknown := build()
	check(unknown.route_between(0, 5).is_empty(), "Without a water map, a swimmer plans every room as swimming (previous behaviour)")
	var mapped := build()
	mapped.swim_cells = {WET: true}
	var route: PackedVector2Array = mapped.route_between(0, 5)
	check(route.size() == 6, "A swimmer plans the dry room with the walking check")
	var smooth: PackedVector2Array = mapped.smooth_route(route)
	check(not smooth.is_empty() and smooth[smooth.size()-1] == Vector2(600,100), "Smoothing keeps the dry-room part walkable")
	check(not smooth.is_empty() and smooth[0] == Vector2(390,100), "No shortcut crosses water on foot: the wet part still needs the swim outline")
	var flooded := build()
	flooded.swim_cells = {WET: true, Vector2i(1,0): true}
	check(flooded.route_between(0, 5).is_empty(), "A flooded destination room still needs the swim outline")
	print("SWIM WALK ROUTING failures=", failures)
	quit(0 if failures == 0 else 1)
