extends SceneTree
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _init() -> void:
	for pair in [["bill", "major-bill-v2"], ["veld", "dr-veld-v1"], ["branforth", "chief-engineer-branforth-v1"]]:
		var player = Player.new()
		player.load_manifest("res://character/%s/final/manifest.json" % pair[1])
		var old_count: int = player.frames.size()
		var original = player.frame("idle", "east", 10.0, Vector2.ZERO)
		var before: Dictionary = player.snapshot()
		player.load_manifest("res://character/crew-underwater-v1/pilot/%s-death-ground-east/manifest.json" % pair[0], true)
		check(player.frames.size() == old_count + 1, "Expansion retains dry states")
		check(player.snapshot() == before, "Loading expansion preserves current clock")
		check(player.frame("idle", "east", 10.0, Vector2.ZERO) == original, "Expansion retains dry texture")
		check(player.strides.has("walk"), "Expansion preserves locomotion stride")
		var key := "death-ground-east"
		check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-death-ground-east/manifest.json" % pair[0]), "Ground-death helmet loads")
		# A helmet change restarts the clip (owner decision, October 12, 2026): helmeted clips carry
		# their own timing. Bare and helmeted playback are therefore checked as separate passes.
		var helmet_rows: Dictionary = player.equipment_frames["diving-helmet"]
		var clock := 20.0
		for gear in ["", "diving-helmet"]:
			var rows: Dictionary = player.frames if gear.is_empty() else helmet_rows
			var label: String = " bare" if gear.is_empty() else " helmet"
			var clip_timing: Dictionary = player.timing if gear.is_empty() else player.equipment_timing.get(gear, player.timing)
			check(player.frame("death-ground", "east", clock, Vector2.ZERO, gear) == rows[key][0], "Death starts on its first frame" + label)
			check(player.snapshot().equipment == gear and is_equal_approx(float(player.snapshot().started), clock), "Death clock starts with the clip" + label)
			var elapsed := 0.0
			for index in range(6):
				var duration: float = clip_timing[key].durations[index] / 1000.0
				check(player.frame("death-ground", "east", clock + elapsed + duration * 0.5, Vector2.ZERO, gear) == rows[key][index], "Timed death frame" + label)
				elapsed += duration
			var terminal = rows[key].back()
			check(player.frame("death-ground", "east", clock + 30.0, Vector2.ZERO, gear) == terminal, "Death holds after many cycles" + label)
			var saved: Dictionary = player.snapshot()
			player.frame("idle", "east", clock + 31.0, Vector2.ZERO, gear)
			player.restore_snapshot(saved)
			check(player.snapshot() == saved, "Death snapshot round trip" + label)
			check(player.frame("death-ground", "east", clock + 30.0, Vector2.ZERO, gear) == terminal, "Saved terminal playback restores" + label)
			clock += 40.0
		var water_key := "death-water-east"
		player.load_manifest("res://character/crew-underwater-v1/pilot/%s-death-water-east/manifest.json" % pair[0], true)
		check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-death-water-east/manifest.json" % pair[0]), "Water-death helmet loads")
		helmet_rows = player.equipment_frames["diving-helmet"]
		for gear in ["", "diving-helmet"]:
			var rows: Dictionary = player.frames if gear.is_empty() else helmet_rows
			var label: String = " bare" if gear.is_empty() else " helmet"
			var clip_timing: Dictionary = player.timing if gear.is_empty() else player.equipment_timing.get(gear, player.timing)
			check(player.frame("death-water", "east", clock, Vector2.ZERO, gear) == rows[water_key][0], "Water death starts on its first frame" + label)
			var water_elapsed := 0.0
			for index in range(6):
				var duration: float = clip_timing[water_key].durations[index] / 1000.0
				check(player.frame("death-water", "east", clock + water_elapsed + duration * 0.5, Vector2.ZERO, gear) == rows[water_key][index], "Water death exact phase" + label)
				water_elapsed += duration
			check(player.frame("death-water", "east", clock + 400.0, Vector2.ZERO, gear) == rows[water_key].back(), "Water death holds terminal frame" + label)
			clock += 500.0
		for transition in ["equip-helmet", "remove-helmet"]:
			var transition_key: String = transition + "-east"
			player.load_manifest("res://character/crew-underwater-v1/locker/%s-%s/manifest.json" % [pair[0], transition_key], true)
			player.frame(transition, "east", clock, Vector2.ZERO)
			var transition_elapsed := 0.0
			check(player.frames[transition_key].size() == 12, "Full locker sequence has twelve poses")
			for index in range(12):
				var duration: float = player.timing[transition_key].durations[index] / 1000.0
				var pose = player.frame(transition, "east", clock + transition_elapsed + duration * 0.5, Vector2.ZERO)
				check(pose == player.frames[transition_key][index], "Transition timed pose " + transition_key)
				check(pose.get_size() == Vector2(92,104) and pose.get_meta("crew_pivot") == Vector2(46,98), "Tall transition registration")
				transition_elapsed += duration
			check(player.frame(transition, "east", clock + 40.0, Vector2.ZERO) == player.frames[transition_key].back(), "Transition holds instead of looping " + transition_key)
			clock += 50.0
	for script in [preload("res://scripts/bill_npc.gd"), preload("res://scripts/veld_npc.gd"), preload("res://scripts/branforth_npc.gd")]:
		var npc = script.new()
		npc.active = true
		npc.path = PackedVector2Array([Vector2(100,100)])
		npc.goal = "maintenance"
		npc.stage = "repair"
		npc.die()
		var saved: Dictionary = npc.snapshot()
		check(npc.valid_snapshot(saved), "Dead NPC snapshot validates")
		npc.update(null, 10.0)
		npc.move(10.0)
		npc.choose_goal(null)
		npc.arrive()
		npc.rebuild(null)
		npc.die()
		check(npc.snapshot() == saved, "Death stops needs, routes, actions and topology updates")
		var invalid: Dictionary = saved.duplicate(true)
		invalid.path = PackedVector2Array([Vector2.ONE])
		check(not npc.valid_snapshot(invalid), "Dead snapshot cannot contain active travel")
	print("CREW DEATH PACK: %d failures" % failures)
	quit(1 if failures else 0)
