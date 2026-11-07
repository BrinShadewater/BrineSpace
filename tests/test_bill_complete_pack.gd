extends SceneTree
## Verify the selected consumer, not just manifests sitting on disk.
## Bill's clips are compared with tests/crew-art-baseline.json, the record of what the
## game loaded when the art was last approved (tools/build_crew_art_baseline.gd).
const Baseline := preload("res://tests/crew_art_baseline.gd")
var failures := 0
var count := 0
func check(ok: bool, message: String) -> void:
	count += 1
	if not ok:
		failures += 1
		if failures <= 40: push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var grid = Baseline.load_grid()
	var player = grid.human_water_player
	var recorded: Dictionary = Baseline.read().get("actors", {}).get("bill", {})
	check(not recorded.is_empty(), "Bill is in the crew art record")
	check(player.frames.size() == recorded.get("body", {}).size(), "All %d recorded body states selected" % recorded.get("body", {}).size())
	check(player.equipment_frames["diving-helmet"].size() == recorded.get("equipment", {}).get("diving-helmet", {}).size(), "All recorded equipped states selected")
	Baseline.compare(recorded, Baseline.describe(player), "bill", check)
	Baseline.playback(player, "bill", check)
	for key in player.equipment_frames["diving-helmet"]:
		var body: Array = player.frames[key]
		var gear: Array = player.equipment_frames["diving-helmet"][key]
		check(not gear.is_empty(), key + " gear frames present")
		if gear.size() == body.size():
			var matched := true
			for i in gear.size():
				# Canvas and pivot may differ (helmeted walk-north is still on the 184 canvas);
				# the drawn scale must not.
				if gear[i].get_meta("crew_standing_height") != body[i].get_meta("crew_standing_height"): matched = false
			check(matched, key + " gear is drawn at the body's scale")
	for facing in ["east", "west", "north", "south"]:
		var key: String = "walk-" + facing
		var stride: float = player.strides.get(key, player.strides.walk)
		player.current_key = ""
		player.frame("walk", facing, 0.0, Vector2.ZERO)
		player.frame("walk", facing, 1.0, Vector2(stride * 0.34, 0))
		var expected: float = player.cycle_seconds(key) * 0.34
		check(is_equal_approx(player.phase, expected), key + " calibrated distance phase")
		grid.human_animation_key = ""
		grid._advance_human_animation(key, 0.0, Vector2.ZERO)
		check(is_equal_approx(grid._advance_human_animation(key, 1.0, Vector2(stride * 0.34, 0)), expected), key + " legacy renderer calibrated phase")
		check(is_equal_approx(grid._advance_human_animation(key, 1.0, Vector2(stride * 0.34, 0)), expected), key + " paused gait remains fixed")
	var npc = load("res://scripts/bill_npc.gd").new()
	npc.active = true
	check(npc.begin_helmet_action(true), "New locker manifest starts equip action")
	check(npc.timer > 0, "Locker duration retained")
	grid.free()
	print("BILL COMPLETE PACK: %d checks, %d failures" % [count, failures])
	quit(1 if failures else 0)
