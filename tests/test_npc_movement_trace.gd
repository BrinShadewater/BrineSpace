extends SceneTree
const Traced=preload("res://tests/traced_bill_npc.gd")
var failures:=0
func expect(value: bool,message: String) -> void:
	if not value:
		failures+=1
		push_error(message)
func _init() -> void:
	var npc=Traced.new()
	var center:=Vector2(7488,7872)
	npc.geometry[Vector2i(19,20)]={"open":[0,1,2,3],"blockers":[Rect2(-2,-2,2,2)]}
	var start:=center+Vector2(-1,0.5)
	var bend:=center+Vector2(0.5,0.5)
	var finish:=center+Vector2(0.5,-1)
	npc.foot=start
	npc.path=PackedVector2Array([bend,finish])
	expect(not npc.segment_clear(start,finish),"Endpoint chord cuts the literal obstacle")
	npc.move(3.0/46.0)
	expect(npc.traveled_points==PackedVector2Array([start,bend,finish]),"Observer retains the actual within-tick bend")
	expect(npc.traveled_clear(),"Two safe traveled legs are accepted")
	expect(is_equal_approx(npc.traveled_distance(),3.0),"Travel distance sums both legs, not their chord")
	# A captured direct shortcut must still fail; the observer is not a bypass.
	npc.traveled_points=PackedVector2Array([start,finish])
	expect(not npc.traveled_clear(),"Actual corner-cutting movement is rejected")
	npc.foot=start
	npc.path=PackedVector2Array([finish])
	npc.move(0.1)
	expect(npc.foot==start and npc.traveled_points==PackedVector2Array([start]),"Rejected attempted movement is not recorded as travel")
	expect(npc.traveled_clear() and npc.traveled_distance()==0.0,"Stationary clear foot has zero travel")
	# At this world position, float rounding makes short diagonal steps alternate
	# their dominant axis. Facing must follow the waypoint rather than each step.
	var diagonal=Traced.new()
	for cell in [Vector2i(20,21),Vector2i(21,21),Vector2i(20,22),Vector2i(21,22)]:
		diagonal.geometry[cell]={"open":[0,1,2,3],"blockers":[]}
	diagonal.foot=Vector2(7960,8215)
	diagonal.direction="south"
	diagonal.path=PackedVector2Array([diagonal.foot+Vector2(60,60)])
	var rounded_east_steps:=0
	for tick in range(120):
		var before:Vector2=diagonal.foot
		diagonal.move(1.0/120)
		var step:Vector2=diagonal.foot-before
		if absf(step.x)>absf(step.y):rounded_east_steps+=1
		expect(diagonal.direction=="south","Diagonal facing stable at tick %d"%tick)
		expect(diagonal.traveled_clear(),"Diagonal travel retains segment clearance")
	expect(rounded_east_steps>0,"Fixture exercises misleading rounded east steps")
	var saved:Dictionary=diagonal.snapshot()
	expect(Traced.valid_snapshot(saved),"Saved waypoint heading accepted")
	var invalid:Dictionary=saved.duplicate(true)
	invalid.movement_heading.target="invalid"
	expect(not Traced.valid_snapshot(invalid),"Malformed saved heading rejected")
	invalid=saved.duplicate(true);invalid.movement_heading.target+=Vector2.ONE
	expect(not Traced.valid_snapshot(invalid),"Saved heading must belong to current waypoint")
	invalid=saved.duplicate(true);invalid.erase("movement_heading")
	expect(Traced.valid_snapshot(invalid),"Older snapshots retain compatibility")
	print("NPC MOVEMENT TRACE: ","PASS" if failures==0 else str(failures)+" failures")
	quit(1 if failures else 0)
