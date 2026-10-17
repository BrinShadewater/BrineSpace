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
	for i in range(12000):
		var a := Vector2(rng.randi_range(-10000,10000),rng.randi_range(-10000,10000))
		var b: Vector2 = a + [Vector2.ZERO,Vector2(16,0),Vector2(0,16),Vector2(16,16),Vector2(-16,16)][i%5]
		var rect := Rect2(a+Vector2(rng.randf_range(-24,24),rng.randf_range(-24,24)),Vector2(rng.randf_range(0,40),rng.randf_range(0,40)))
		if i%8==0: rect.position=a
		if i%8==1: rect.position=a-rect.size
		var blockers: Array[Rect2] = [rect,Rect2(a+Vector2(8,-12),Vector2(4,24))]
		var reference := true
		for blocker in blockers:
			if npc.segment_hits_rect(a,b,blocker): reference=false;break
		checked+=1
		if npc._template_segment_clear(a,b,blockers)!=reference:
			failures+=1
			if failures<10: push_error("Template bounds disagreement: %s -> %s" % [a,b])
	standing_parity()
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

class StandingOracle extends "res://scripts/bill_npc.gd":
	func can_stand(point: Vector2) -> bool:
		var cell := cell_at(point)
		if not geometry.has(cell): return false
		var data: Dictionary = geometry[cell]
		var local := point - (Vector2(cell) + Vector2.ONE * 0.5) * CELL
		# Closed sockets remain walls even in the corridor and legacy renderers.
		for side in range(4):
			var normal: Vector2 = Vector2(Geometry.DIRS[side])
			if local.dot(normal) > 176 and not data.open.has(side): return false
		if data.get("corridor", false):
			for rect in data.get("blockers",[]):
				if rect.has_point(local): return false
			return Corridor.contains_foot(data.room, local, 10.0)
		if data.get("large_room", false):
			for rect in data.get("blockers",[]):
				if rect.has_point(local): return false
			return true
		if data.get("legacy", false):
			# Legacy art has no authored prop map. Retain conservative perimeter lanes
			# around its central equipment instead of inventing a clear room interior.
			if maxf(absf(local.x), absf(local.y)) > 174 and minf(absf(local.x), absf(local.y)) > 26: return false
			return maxf(absf(local.x), absf(local.y)) >= 104
		for rect in data.blockers:
			if rect.has_point(local): return false
		return true

func standing_parity()->void:
	var reference=StandingOracle.new()
	var candidate=NPC.new()
	var rng:=RandomNumberGenerator.new();rng.seed=10112026
	for kind in ["authored","large","legacy","corridor","corner","tee_corridor"]:
		for mask in range(16):
			var open:Array=[]
			for side in range(4):
				if mask&(1<<side):open.append(side)
			var data:Dictionary={"open":open,"blockers":[Rect2(-110,-75,62,81),Rect2(44,30,95,41)],"room":{"id":kind,"rotation":mask%4}}
			if kind=="large":data.large_room=true
			elif kind=="legacy":data.legacy=true
			elif kind in ["corridor","corner","tee_corridor"]:data.corridor=true
			for anchor in [-20,20,100000]:
				for actor in [reference,candidate]:
					actor.geometry.clear()
					for y in range(anchor-1,anchor+2):
						for x in range(anchor-1,anchor+2):actor.geometry[Vector2i(x,y)]=data
				var center:Vector2=(Vector2(anchor,anchor)+Vector2.ONE*.5)*384
				for i in range(400):
					var point:Vector2=center+Vector2(rng.randf_range(-384,384),rng.randf_range(-384,384))
					if i<100:point=center+Vector2([-192.0,-176.0,-104.0,0.0,104.0,176.0,192.0,191.999,175.999,-175.999][i%10],[-192.0,-176.0,-104.0,0.0,104.0,176.0,192.0,191.999,175.999,-175.999][i/10])
					if reference.can_stand(point)!=candidate.can_stand(point):
						failures+=1
						if failures<10:push_error("Standing mismatch "+kind+" "+str(point))
					checked+=1
