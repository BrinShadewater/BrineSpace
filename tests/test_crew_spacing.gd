extends SceneTree
## Two crew walk toward each other through a shared doorway. They must never come closer than
## MIN_GAP (a standing crew sprite is about 29 units wide), and both must get through.
## Spec: docs/superpowers/specs/2026-09-29-crew-collision-design.md
const CrewPassage = preload("res://scripts/crew_passage.gd")
const MIN_GAP := 29.0
const STEP := 0.05
const MAX_SECONDS := 90.0

var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://crew_spacing_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://crew_spacing_%d.loop" % OS.get_process_id()
	game.Preferences.initialized = true
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.occupied.clear()
	game.placed_rooms.clear()
	var west := Vector2i(19, 20)
	var east := Vector2i(20, 20)
	for cell in [west, east]:
		game._place_room("battery_array", cell, true)
	var bill = game.bill_npc
	var veld = game.veld_npc
	for actor in [bill, veld]:
		actor.rebuild(game)
		actor.active = true
	var west_centre := (Vector2(west) + Vector2.ONE * 0.5) * 384.0
	var east_centre := (Vector2(east) + Vector2.ONE * 0.5) * 384.0
	var bill_start: int = bill.nearest_in_room(west_centre + Vector2(-120, 0), west)
	var bill_goal: int = bill.nearest_in_room(east_centre + Vector2(120, 0), east)
	var veld_start: int = veld.nearest_in_room(east_centre + Vector2(120, 0), east)
	var veld_goal: int = veld.nearest_in_room(west_centre + Vector2(-120, 0), west)
	expect(bill_start >= 0 and bill_goal >= 0 and veld_start >= 0 and veld_goal >= 0, "Both rooms have walkable nodes at both ends")
	bill.foot = bill.graph.get_point_position(bill_start)
	veld.foot = veld.graph.get_point_position(veld_start)
	bill.path = bill.smooth_route(bill.graph.get_point_path(bill_start, bill_goal))
	veld.path = veld.smooth_route(veld.graph.get_point_path(veld_start, veld_goal))
	expect(not bill.path.is_empty() and not veld.path.is_empty(), "Both crew have a route through the doorway")
	var closest := 99999.0
	var seconds := 0.0
	while seconds < MAX_SECONDS and (not bill.path.is_empty() or not veld.path.is_empty()):
		bill.avoidance_positions = PackedVector2Array([veld.foot])
		veld.avoidance_positions = PackedVector2Array([bill.foot])
		for actor in [bill, veld]:
			if not actor.path.is_empty(): actor.move(STEP)
		CrewPassage.update([bill, veld])
		closest = minf(closest, bill.foot.distance_to(veld.foot))
		seconds += STEP
	print("CREW SPACING: closest %.1f units, %.1f s, bill left %d waypoints, veld left %d" % [closest, seconds, bill.path.size(), veld.path.size()])
	expect(closest >= MIN_GAP, "Crew never closer than %.0f units (closest %.1f)" % [MIN_GAP, closest])
	expect(bill.path.is_empty() and veld.path.is_empty(), "Both crew get through the doorway within %.0f s" % MAX_SECONDS)
	print("CREW SPACING: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
