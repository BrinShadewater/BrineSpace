extends SceneTree
## Smoothing a swim route must keep a facing the next stroke can turn from. A greedy
## shortcut arriving west at a spot where a west-to-north turn does not fit threw away
## every graph-valid escape route in the Sept 23 doorway report (262 ms, no escape).
const P := Vector2(0,-32)
const EXIT := Vector2(0,-48)
var failures := 0

class TurnLimitedSwimmer extends "res://scripts/bill_npc.gd":
	func segment_clear(_a: Vector2, _b: Vector2) -> bool: return true
	func swim_segment_clear(a: Vector2, b: Vector2, facing: String, previous_facing: String = "", _treading: bool = false, _extent: Array = []) -> bool:
		# The swimmer cannot turn from west to north at P, and EXIT is only visible from P.
		if a == P and previous_facing == "west" and facing == "north": return false
		if b == EXIT and a != P: return false
		return true

func _init(): call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok: failures += 1; push_error(message)

func run() -> void:
	var actor := TurnLimitedSwimmer.new()
	actor.movement_medium = "flooded"
	actor.direction = "west"
	actor.foot = Vector2(64,0)
	var raw := PackedVector2Array([Vector2(48,0),Vector2(32,0),Vector2(16,0),Vector2(0,0),Vector2(0,-16),P,EXIT])
	var smooth: PackedVector2Array = actor.smooth_route(raw)
	check(not smooth.is_empty(), "Graph-valid swim route survives smoothing")
	check(not smooth.is_empty() and smooth[smooth.size()-1] == EXIT, "Smoothed route still ends at the exit")
	# Every kept segment must pass the same facing-aware check movement uses.
	var from := actor.foot
	var facing := actor.direction
	for point in smooth:
		var heading: String = actor.travel_heading(from, point, facing)
		check(actor.swim_segment_clear(from, point, heading, facing), "Kept segment %s -> %s fits the swimmer" % [from, point])
		facing = heading
		from = point
	check(smooth.size() < raw.size(), "Straight stretches are still shortened")
	# Dry routes keep the plain greedy shortcut: facing does not constrain walking.
	actor.movement_medium = "dry"
	var dry: PackedVector2Array = actor.smooth_route(PackedVector2Array([Vector2(48,0),Vector2(32,0),Vector2(16,0),Vector2(0,0)]))
	check(dry.size() == 1 and dry[0] == Vector2(0,0), "Dry smoothing still takes the longest clear shortcut")
	print("SWIM SMOOTHING FACING failures=", failures)
	quit(0 if failures == 0 else 1)
