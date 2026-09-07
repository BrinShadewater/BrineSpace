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
	print("NPC MOVEMENT TRACE: ","PASS" if failures==0 else str(failures)+" failures")
	quit(1 if failures else 0)
