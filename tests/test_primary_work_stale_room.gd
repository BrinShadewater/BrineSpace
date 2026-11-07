extends SceneTree
const Work = preload("res://scripts/crew_primary_work.gd")
class Actor extends RefCounted:
	var foot := Vector2.ZERO
	var needs := {"hunger": 70, "fatigue": 0}
	var helmet_equipped := false
	var room_nodes := {Vector2i(1, 1): [1]}
	var service_preferences := {"hunger": ["galley"], "fatigue": ["crew_hab"]}
	func needs_air() -> bool: return true
	func nearest_in_room(_foot, _cell) -> int: return 0
	func cell_at(_foot) -> Vector2i: return Vector2i.ZERO
	func service_available(_game, _cell) -> bool: return true
	func can_reach_any(_from, targets: Dictionary) -> bool: return not targets.is_empty()
func _init() -> void:
	var actor := Actor.new()
	var game := {"resources": {"food": 10}, "occupied": {}}
	var checks := [not Work.break_needed(game, actor)]
	game.occupied[Vector2i(2, 2)] = {"id": "galley"}
	actor.room_nodes[Vector2i(2, 2)] = [2]
	checks.append(Work.break_needed(game, actor))
	game.resources.food = 0
	checks.append(not Work.break_needed(game, actor))
	var passed := checks.all(func(value): return value)
	print("PRIMARY WORK STALE ROOM ", "PASS" if passed else "FAIL", ": ", checks)
	quit(0 if passed else 1)
