extends SceneTree
const NPC=preload("res://scripts/bill_npc.gd")
var failures:=0
func expect(value: bool,message: String) -> void:
	if not value:
		failures+=1
		push_error(message)
func _init() -> void: call_deferred("run")
func turn(point: Vector2,q: int) -> Vector2:
	for unused in range(q): point=Vector2(-point.y,point.x)
	return point
func run() -> void:
	var center:=Vector2(7488,7872)
	# Literal wall-clearance rectangle from the v22 corner diagnostic.
	var wall:=Rect2(-202,-210,176,36)
	for q in range(4):
		var npc:=NPC.new()
		for cell in [Vector2i(19,20),Vector2i(19,19),Vector2i(20,20),Vector2i(19,21),Vector2i(18,20)]:
			npc.geometry[cell]={"open":[0,1,2,3],"blockers":[]}
		var bounds:=Rect2(turn(wall.position,q),Vector2.ZERO)
		for corner in [Vector2(wall.end.x,wall.position.y),wall.end,Vector2(wall.position.x,wall.end.y)]: bounds=bounds.expand(turn(corner,q))
		npc.geometry[Vector2i(19,20)].blockers=[bounds]
		var a:=center+turn(Vector2(-26.849609375,-169.9697265625),q)
		var b:=center+turn(Vector2(0,-368),q)
		expect(npc.can_stand(a) and npc.can_stand(b),"Corner example endpoints remain clear")
		expect(not npc.segment_clear(a,b),"Near-tangent wall crossing rejected q%d"%q)
		expect(not npc.segment_clear(b,a),"Reverse near-tangent crossing rejected q%d"%q)
		var safe:=center+turn(Vector2(0,-160),q)
		expect(npc.segment_clear(safe,b),"Door centre remains traversable q%d"%q)
		expect(npc.segment_clear(safe,safe),"Clear stationary segment accepted")
		var inside:=center+turn(Vector2(-40,-180),q)
		expect(not npc.segment_clear(inside,inside),"Blocked stationary segment rejected")
		# A valid bend must survive smoothing instead of being shortcut through a corner.
		npc.foot=a
		var route:=npc.smooth_route(PackedVector2Array([safe,b]))
		expect(route.size()==2,"Smoothing retains safe bend at doorway q%d"%q)
	var swimmer:=NPC.new()
	var profile: Dictionary={}
	for facing in ["east","south","west","north"]: profile[facing]=[-4,-4,4,4]
	swimmer.swim_clearance={"bare":profile,"helmet":profile}
	# This prop belongs to room zero but extends across its eastern boundary.
	swimmer.geometry[Vector2i.ZERO]={"blockers":[Rect2(190,-10,30,20)],"swim_blocker_bounds":Rect2(190,-10,30,20)}
	swimmer.geometry[Vector2i(1,0)]={"blockers":[],"swim_blocker_bounds":Rect2()}
	swimmer.geometry[Vector2i(20,20)]={"blockers":[Rect2(-10,-10,20,20)],"swim_blocker_bounds":Rect2(-10,-10,20,20)}
	expect(not swimmer.swim_segment_clear(Vector2(400,192),Vector2(401,192),"east"),"Swim region cache retains overhanging props owned by a neighbouring room")
	expect(not swimmer.swim_region_cache[Vector4i(1,0,1,0)].has(Vector2i(20,20)),"Swim region cache excludes distant owners")
	expect(swimmer.swim_segment_clear(Vector2(450,192),Vector2(460,192),"east"),"Cached region still tests exact blocker bounds")
	if failures==0: print("NPC SEGMENT CLEARANCE PASS: four rotations, reverse paths, doorway, stationary endpoints, smoothing and swim region overhangs")
	quit(1 if failures else 0)
