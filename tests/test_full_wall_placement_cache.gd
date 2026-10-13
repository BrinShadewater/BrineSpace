extends SceneTree
const Placement = preload("res://rooms/full-wall-v1/full_wall_prop.gd")
class Room extends RefCounted:
	var layout := [{"cell": Vector2i.ZERO, "rotation": 0, "kind": 2}]
	func prop_visual_bounds(prop: Dictionary) -> Rect2: return prop.rect
func _init() -> void: call_deferred("run")
func run() -> void:
	var helper := Placement.new("thermal-control-wall")
	var room := Room.new()
	var original := {"id": "first", "rect": Rect2(-130, -130, 24, 24), "sort_y": -106.0, "art_offset": Vector2(2, 3)}
	var first := helper.vacant_placement(room, original, [])
	var second := helper.vacant_placement(room, original, [])
	var checks := [not first.is_empty(), first == second, helper.placement_cache_hits == 1]
	original.id = "edited-metadata"
	var edited := helper.vacant_placement(room, original, [])
	checks.append(edited.id == "edited-metadata" and helper.placement_cache_hits == 2)
	var blocked := helper.vacant_placement(room, original, [first])
	checks.append(blocked != edited and helper.placement_cache_hits == 2)
	helper.reuse_placements = false
	checks.append(helper.vacant_placement(room, original, [first]) == blocked)
	helper.reuse_placements = true
	room.layout[0].rotation = 1
	var turned := helper.vacant_placement(room, original, [first], Vector2(100, 100))
	helper.reuse_placements = false
	checks.append(turned == helper.vacant_placement(room, original, [first], Vector2(100, 100)))
	var passed := checks.all(func(value): return value)
	print("FULL WALL PLACEMENT CACHE ", "PASS" if passed else "FAIL", ": ", checks)
	quit(0 if passed else 1)
