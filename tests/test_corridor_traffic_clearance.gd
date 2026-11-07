extends SceneTree
## Retained three-crew blockage: a sampled shortcut skimmed the concave elbow.
## The whole shortcut passed, but incremental movement could not execute it.
const Actor=preload("res://scripts/bill_npc.gd")
const Turn=preload("res://tools/modular_room_geometry.gd")
var failures:=0
func check(ok:bool,message:String)->void:
	if not ok:failures+=1;print("FAIL: ",message)
func _initialize()->void:
	var cell:=Vector2i(24,20)
	var center:=(Vector2(cell)+Vector2.ONE*.5)*384.0
	for q in range(4):
		var actor=Actor.new()
		var room:Dictionary={"id":"corner","rotation":q}
		actor.geometry[cell]={"corridor":true,"room":room,"open":[posmod(3+q,4),posmod(2+q,4)],"blockers":[]}
		# Source was rotation 1; preserve its local contacts in every rotation.
		var a:=center+Turn.turn(Vector2(-39.1377,-42.6465),q-1)
		var b:=center+Turn.turn(Vector2(-80,-16),q-1)
		actor.foot=a
		check(actor.can_stand(a) and actor.can_stand(b),"Both original endpoints fit rotation %d"%q)
		check(not actor.segment_clear(a,b),"Reject shortcut whose foot area clips elbow rotation %d"%q)
		var route:=actor.smooth_route(PackedVector2Array([a,center,b]))
		check(not route.is_empty(),"Retain a clear turn through the elbow rotation %d"%q)
		actor.path=route
		for step in range(600):
			if actor.path.is_empty():break
			var before:Vector2=actor.foot
			actor.move(.01)
			check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Movement keeps floor clearance")
		check(actor.foot.distance_to(b)<.15,"Planned turn executes at small steps rotation %d: %s -> %s (%s)"%[q,actor.foot,b,actor.activity])
	var straight=Actor.new()
	straight.geometry[Vector2i(20,12)]={"corridor":true,"room":{"id":"corridor","rotation":0},"open":[0,2],"blockers":[]}
	var seam:=Vector2(7876.594,4615.921)
	var target:=Vector2(7856,4688)
	check(straight.segment_clear(seam,target),"Straight mouth has a valid long join")
	check(straight.segment_clear(seam,seam.move_toward(target,4.6)),"Clipped foot samples at a cell seam keep a valid movement step")
	print("CORRIDOR TRAFFIC CLEARANCE failures=",failures)
	quit(1 if failures else 0)
