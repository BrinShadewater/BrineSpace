extends SceneTree
## Idle and walk clips for Bill, Veld and Branforth: the art the game loads, and the rule
## that walking advances by distance. Art is compared with tests/crew-art-baseline.json,
## the record of what was loaded when it was last approved (tools/build_crew_art_baseline.gd).
const Baseline := preload("res://tests/crew_art_baseline.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		if failures <= 40: push_error(why)
func idle_or_walk(key: String) -> bool:
	return key.begins_with("idle-") or key.begins_with("walk-")
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = Baseline.load_grid()
	var record: Dictionary = Baseline.read().get("actors", {})
	for actor in ["bill", "veld", "branforth"]:
		var p = Baseline.player_of(grid, actor)
		check(record.has(actor), actor + " is in the crew art record")
		var recorded: Dictionary = Baseline.limit(record.get(actor, {}), idle_or_walk)
		check(recorded.body.size() >= 8, actor + " records idle and walk in four facings")
		Baseline.compare(recorded, Baseline.describe(p, idle_or_walk), actor, check)
		Baseline.playback(p, actor, check, idle_or_walk)
		for direction in ["south", "east", "north", "west"]:
			var key: String = "walk-" + direction
			check(p.frames.has(key) and p.timing[key].loop, actor + key + " loops")
			var stride: float = p.strides.get(key, p.strides.walk)
			check(stride > 0.0, actor + key + " has a stride")
			p.current_key = ""
			p.frame("walk", direction, 0, Vector2.ZERO)
			p.frame("walk", direction, 0.75, Vector2(stride * 0.5, 0))
			check(is_equal_approx(p.phase, p.cycle_seconds(key) * 0.5), actor + key + " half physical stride")
			var snapshot: Dictionary = p.snapshot()
			p.frame("walk", direction, 0.75, Vector2(stride * 0.5, 0))
			check(p.snapshot() == snapshot, actor + key + " pause stable")
			for state in ["idle", "walk"]:
				check(not p.equipment_frames["diving-helmet"].get(state + "-" + direction, []).is_empty(), actor + state + "-" + direction + " helmet preserved")
	grid.free()
	print("CREW WALK V2: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
