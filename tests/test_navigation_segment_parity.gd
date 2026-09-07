extends SceneTree
const NPC = preload("res://scripts/bill_npc.gd")
var failures := 0
var checked := 0
func _init() -> void: call_deferred("run")
func run() -> void:
	var npc := NPC.new()
	var rng := RandomNumberGenerator.new()
	rng.seed = 90626
	var center := Vector2(7872,7872)
	for mask in range(16):
		var openings: Array = []
		for side in range(4):
			if mask & (1<<side): openings.append(side)
		npc.geometry.clear()
		for y in range(19,22):
			for x in range(19,22):
				npc.geometry[Vector2i(x,y)] = {"open":openings,"blockers":[Rect2(-110,-75,62,81),Rect2(44,30,95,41),Rect2(-202,-210,176,36)]}
		for i in range(1600):
			var a := center+Vector2(rng.randf_range(-200,200),rng.randf_range(-200,200))
			var b := center+Vector2(rng.randf_range(-200,200),rng.randf_range(-200,200))
			if i%8 == 0: b = a
			compare(npc,a,b)
		# Include exact half-open blocker edges and room boundary coordinates.
		for x in [-192.0,-176.0,-110.0,-48.0,44.0,139.0,176.0,192.0]:
			for y in [-192.0,-176.0,-75.0,6.0,30.0,71.0,176.0,192.0]:
				compare(npc,center+Vector2(x,y),center+Vector2(-x,-y))
	print("NAVIGATION SEGMENT PARITY: ",checked," comparisons, ",failures," failures")
	quit(1 if failures else 0)
func compare(npc, a: Vector2, b: Vector2) -> void:
	npc.sample_all_segments = true
	var reference: bool = npc.segment_clear(a,b)
	npc.sample_all_segments = false
	var result: bool = npc.segment_clear(a,b)
	checked += 1
	if reference != result:
		failures += 1
		if failures<10: push_error("Navigation disagreement: %s -> %s" % [a,b])
