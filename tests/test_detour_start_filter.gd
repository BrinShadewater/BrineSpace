extends SceneTree
## A crew stand-off tried a detour from every start in the room, each a failed search:
## 269 starts, 500 ms, repeated per step-aside spot (1 s frames, Sept 26 review run).
## One fill from the target predicts which starts can reach it; it must match the search.
var failures := 0

class Corridor1D extends "res://scripts/bill_npc.gd":
	func avoidance_peers() -> PackedVector2Array: return PackedVector2Array([Vector2(120,100)])

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var actor := Corridor1D.new()
	actor.movement_medium = "dry"
	var cell := Vector2i(0,0)
	actor.geometry = {cell: {"open": [0,1,2,3], "blockers": []}}
	actor.room_nodes = {cell: [0,1,2,3,4]}
	# A single lane: the peer stands on node 2, so only its own start can pass it.
	for i in range(5):
		actor.graph.add_point(i, Vector2(40 + 40*i, 100))
		if i > 0: actor.graph.connect_points(i-1, i)
	actor.foot = Vector2(40, 100)
	var target := 4
	var reach: Variant = actor._detour_reach(target)
	check(reach is Dictionary, "Walking crew get a reach fill")
	var expected := {0: false, 1: false, 2: true, 3: true, 4: true}
	for start in range(5):
		var padding: Array[int] = actor._crew_padding(start, target)
		for id in padding: actor.graph.set_point_disabled(id, true)
		var route: PackedVector2Array = actor.route_between(start, target, true)
		for id in padding: actor.graph.set_point_disabled(id, false)
		var predicted: bool = actor._detour_start_joins(start, reach)
		check(predicted == (not route.is_empty()), "Start %d: fill (%s) matches the padded search (%s)" % [start, predicted, not route.is_empty()])
		check(predicted == expected[start], "Start %d reachability is %s" % [start, expected[start]])
	actor.movement_medium = "flooded"
	check(actor._detour_reach(target) == null, "Swimmers keep the full search (facing-dependent)")
	print("DETOUR START FILTER failures=", failures)
	quit(0 if failures == 0 else 1)
