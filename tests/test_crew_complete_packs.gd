extends SceneTree
## Verify the live renderer's selected packs, not only independent catalog loads.
## Veld, Branforth and Marsh are compared with tests/crew-art-baseline.json, the record of
## what the game loaded when the art was last approved (tools/build_crew_art_baseline.gd).
const Baseline := preload("res://tests/crew_art_baseline.gd")
var failures := 0
var checks := 0
func check(ok: bool, why: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		if failures <= 40: push_error(why)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = Baseline.load_grid()
	var record: Dictionary = Baseline.read().get("actors", {})
	for actor in ["veld", "branforth", "marsh"]:
		var player = grid.get(actor + "_player")
		var recorded: Dictionary = record.get(actor, {})
		check(not recorded.is_empty(), actor + " is in the crew art record")
		check(player.frames.size() == recorded.get("body", {}).size(), actor + " body coverage")
		# Marsh is helmet-free by owner decision.
		check(player.equipment_frames.has("diving-helmet") == (actor != "marsh"), actor + " gear coverage")
		for key in ["bunk-enter-east", "bunk-sleep-east", "bunk-exit-east"]:
			check(player.frames.has(key), actor + " selected bunk " + key)
			if not player.frames.has(key): continue
			check(player.timing[key].loop == (key == "bunk-sleep-east"), actor + " bunk loop " + key)
			if actor != "marsh":
				check(player.equipment_frames["diving-helmet"].get(key, []).size() == player.frames[key].size(), actor + " bunk gear " + key)
		Baseline.compare(recorded, Baseline.describe(player), actor, check)
		Baseline.playback(player, actor, check)
		for direction in ["east", "west", "north", "south"]:
			player.current_key = ""
			player.frame("walk", direction, 0.0, Vector2.ZERO)
			var stride: float = player.strides.get("walk-" + direction, player.strides.walk)
			player.frame("walk", direction, 1.0, Vector2(stride * 0.34, 0))
			check(is_equal_approx(player.phase, player.cycle_seconds("walk-" + direction) * 0.34), actor + " distance cadence " + direction)
			var snapshot: Dictionary = player.snapshot()
			player.frame("walk", direction, 1.0, Vector2(stride * 0.34, 0))
			check(player.snapshot() == snapshot, actor + " paused cadence " + direction)
		var npc = load("res://scripts/" + actor + "_npc.gd").new()
		npc.active = true
		check(npc.begin_helmet_action(true) == (actor != "marsh"), actor + " equipment semantics")
		if actor != "marsh": check(npc.timer > 0, actor + " locker timing")
	grid.free()
	print("CREW COMPLETE PACKS: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
