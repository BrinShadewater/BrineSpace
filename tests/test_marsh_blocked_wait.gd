extends SceneTree
# A crew member who cannot pass counts the time he is blocked, and after three seconds gives
# up the route. Marsh's start clips begin again on every blocked attempt, and his wait used
# to advance one frame in seven: he stood "waiting for passage" for good (owner report,
# October 13, 2026, Marsh held by River and Margot).
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(why)
func _init() -> void: call_deferred("run")
func blocked_wait(game, script_path: String, wanted: String, seconds: float) -> Dictionary:
	var npc = load(script_path).new()
	npc.rebuild(game)
	npc.active = true
	# Two navigation points in BRINE's core with a clear straight walk between them, in the
	# wanted compass direction.
	var from := Vector2.INF
	var to := Vector2.INF
	var ids: Array = npc.room_nodes.get(Vector2i(20, 20), [])
	for a in ids:
		for b in ids:
			var start: Vector2 = npc.graph.get_point_position(a)
			var finish: Vector2 = npc.graph.get_point_position(b)
			if start.distance_to(finish) < 60 or not npc.segment_clear(start, finish): continue
			if npc.travel_heading(start, finish, "south") != wanted: continue
			if from.is_finite() and start.distance_to(finish) <= from.distance_to(to): continue
			from = start; to = finish
	if not from.is_finite(): return {"found": false}
	npc.foot = from
	npc.direction = wanted
	# One colleague stands square in the way, inside the clearance distance.
	var peer: Vector2 = from + (to - from).normalized() * 28.0
	npc.avoidance_positions = PackedVector2Array([peer])
	npc.avoidance_position = peer
	npc.goal = "curiosity"
	npc.goal_cell = Vector2i(20, 20)
	npc.path = PackedVector2Array([to])
	npc.traffic_retry = 999.0 # No detours: this measures the wait alone.
	var peak := 0.0
	var gave_up_at := -1.0
	var moved := 0.0
	for step in range(int(seconds * 60.0)):
		var before: Vector2 = npc.foot
		npc.traffic_retry = 999.0
		npc.move(1.0 / 60.0)
		moved += npc.foot.distance_to(before)
		peak = maxf(peak, npc.traffic_wait)
		if npc.path.is_empty():
			gave_up_at = float(step + 1) / 60.0
			break
	return {"found": true, "peak": peak, "gave_up_at": gave_up_at, "moved": moved, "activity": npc.activity}
func run() -> void:
	var Store = preload("res://scripts/room_layout_store.gd")
	Store.loaded = true; Store.data = {}
	var game = load("res://scenes/main.tscn").instantiate()
	game.run_save_path = "user://marsh-blocked-wait-test.loop"; game.meta.save_path = "user://marsh-blocked-wait-test.meta"
	root.add_child(game); current_scene = game
	await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(false, false)
	game.running = true
	for actor in [game.bill_npc, game.veld_npc, game.branforth_npc, game.marsh_npc]: actor.active = false
	for label in [["Bill", "res://scripts/bill_npc.gd"], ["Marsh", "res://scripts/marsh_npc.gd"]]:
		for wanted in ["north", "south", "east", "west"]:
			var result: Dictionary = blocked_wait(game, label[1], wanted, 6.0)
			var where := "%s heading %s" % [label[0], wanted]
			check(result.found, where + " has a straight walk to test in the core")
			if not result.found: continue
			check(result.moved < 4.0, where + " stays put behind a colleague: moved %.1f" % result.moved)
			check(result.gave_up_at > 2.5 and result.gave_up_at < 4.0, where + " gives up after about three seconds, not %.2f (%s)" % [result.gave_up_at, result.activity])
			check(result.peak > 2.5, where + " counted the time he was blocked: %.2f" % result.peak)
	print("MARSH BLOCKED WAIT: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
