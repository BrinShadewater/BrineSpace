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
	dense_reach_parity()
	print("DETOUR START FILTER failures=", failures)
	quit(0 if failures == 0 else 1)

# Match the original fill, including BFS insertion order and sparse fallback.
func dense_reach_parity()->void:
	var reference=preload("res://scripts/bill_npc.gd").new()
	var candidate=preload("res://scripts/bill_npc.gd").new()
	var rng:=RandomNumberGenerator.new();rng.seed=10112026
	var compared:=0
	for revision in range(12):
		for actor in [reference,candidate]:
			actor.navigation_build_revision+=1;actor.graph.clear();actor.room_nodes.clear();actor.fire_cells.clear();actor.movement_medium="dry";actor.foot=Vector2(8,8)
			for i in range(200):
				var point:Vector2=Vector2(i%20,i/20)*64
				actor.graph.add_point(i,point)
				var cell:Vector2i=actor.cell_at(point)
				if not actor.room_nodes.has(cell):actor.room_nodes[cell]=[]
				actor.room_nodes[cell].append(i)
		for i in range(200):
			for step in [1,20,21]:
				if i+step<200 and rng.randf()<.75:
					reference.graph.connect_points(i,i+step);candidate.graph.connect_points(i,i+step)
		for pass_index in range(20):
			var padding:Array[int]=[]
			for actor in [reference,candidate]:actor.fire_cells={Vector2i(2,1):true} if pass_index%3==0 else {}
			for i in range(200):
				var disabled:bool=rng.randf()<.04
				reference.graph.set_point_disabled(i,disabled);candidate.graph.set_point_disabled(i,disabled)
				if rng.randf()<.05:padding.append(i)
			var target:int=rng.randi_range(0,199)
			var a=reference._detour_reach_reference(target,padding);var b=candidate._detour_reach(target,padding)
			if a!=b or (a is Dictionary and a.reached.keys()!=b.reached.keys()):check(false,"Dense reach/order differs");return
			compared+=1
			if a is Dictionary:
				for start in range(200):
					if reference._detour_start_joins(start,a)!=candidate._detour_start_joins(start,b):check(false,"Dense start join differs");return
					compared+=1
	for actor in [reference,candidate]:
		actor.navigation_build_revision+=1;actor.graph.clear();actor.fire_cells.clear();actor.graph.add_point(1000000,Vector2.ZERO);actor.graph.add_point(2000000,Vector2.RIGHT);actor.graph.connect_points(1000000,2000000)
	var padding:Array[int]=[-1,3000000]
	check(reference._detour_reach_reference(1000000,padding)==candidate._detour_reach(1000000,padding),"Sparse IDs and padding preserve original fill")
	for actor in [reference,candidate]:
		actor.graph=AStar2D.new();actor.graph.add_point(0,Vector2.ZERO);actor.graph.add_point(1,Vector2.RIGHT);actor.graph.connect_points(0,1)
	check(reference._detour_reach_reference(0,padding)==candidate._detour_reach(0,padding) and candidate.detour_dense,"Same-count graph replacement refreshes density")
	print("DENSE REACH PARITY comparisons=",compared+2)
