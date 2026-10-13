extends SceneTree
# Crew waiting in the Diving Airlock's pressure chamber stand wholly inside it. A chamber
# lying east-west is shallower than a standing figure: on its centre line the head crossed
# the far wall (owner report, October 13, 2026, "Marsh's head popping through the wall").
const Expedition := preload("res://scripts/crew_expedition.gd")
const View := preload("res://rooms/underwater/airlock-v1/airlock_view.gd")
const Geometry := preload("res://tools/modular_room_geometry.gd")
const STANDING := 65.28 # A crew member's standing height in world units.
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func turned(rect: Rect2, quarter: int) -> Rect2:
	var a := Geometry.turn(rect.position, quarter)
	var b := Geometry.turn(rect.end, quarter)
	return Rect2(Vector2(minf(a.x, b.x), minf(a.y, b.y)), (b - a).abs())
func run() -> void:
	for quarter in range(4):
		var room := {"id": "airlock", "pos": Vector2i(23, 21), "rotation": quarter}
		var centre: Vector2 = Expedition.point(room, Vector2.ZERO)
		# The chamber's walls are 8 units thick, set 4 inside and 4 outside its rectangle.
		var inside: Rect2 = turned(View.CHAMBER, quarter).grow(-4)
		inside.position += centre
		var foot: Vector2 = Expedition.chamber_stand(room)
		check(inside.has_point(foot), "Rotation %d: feet are on the chamber floor at %s" % [quarter, foot - centre])
		check(foot.y - STANDING > inside.position.y, "Rotation %d: the head is below the far wall, %.1f units clear" % [quarter, foot.y - STANDING - inside.position.y])
		check(inside.end.y - foot.y >= 8.0, "Rotation %d: feet stand clear of the near wall" % quarter)
		if quarter % 2 == 0:
			check(foot.is_equal_approx(Expedition.point(room, Vector2(0, -70))), "Rotation %d: an upright chamber keeps its centre-line spot" % quarter)
	print("AIRLOCK CHAMBER STAND: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
