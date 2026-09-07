extends "res://scripts/bill_npc.gd"
## Test-only observer. Production movement remains in the parent controller.
var traveled_points:=PackedVector2Array()
var observing_move:=false

func update(main,delta: float) -> void:
	traveled_points=PackedVector2Array([foot])
	super.update(main,delta)
	record_foot()

func move(delta: float) -> void:
	traveled_points=PackedVector2Array([foot])
	observing_move=true
	super.move(delta)
	record_foot()
	observing_move=false

func segment_clear(a: Vector2,b: Vector2) -> bool:
	# Each movement leg is checked before assignment. Observe the previous
	# assignment at the next check, and the final assignment after move returns.
	# Planning queries do not move the foot and therefore add no points.
	if observing_move: record_foot()
	return super.segment_clear(a,b)

func record_foot() -> void:
	if traveled_points.is_empty() or traveled_points[-1]!=foot:
		traveled_points.append(foot)

func traveled_clear() -> bool:
	for i in range(traveled_points.size()):
		if not can_stand(traveled_points[i]): return false
		if i>0 and not segment_clear(traveled_points[i-1],traveled_points[i]): return false
	return not traveled_points.is_empty()

func traveled_distance() -> float:
	var distance:=0.0
	for i in range(1,traveled_points.size()):
		distance+=traveled_points[i-1].distance_to(traveled_points[i])
	return distance
