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
	if failures==0: print("NPC SEGMENT CLEARANCE PASS: four rotated near-tangent cases, reverse paths, clear doorway, stationary endpoints and smoothing")
	quit(1 if failures else 0)
