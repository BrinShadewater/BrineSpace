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
		player.frame("death-ground", "east", 20.0, Vector2.ZERO)
		var elapsed := 0.0
		for index in range(6):
			var duration: float = player.timing[key].durations[index] / 1000.0
			check(player.frame("death-ground", "east", 20.0 + elapsed + duration * 0.5, Vector2.ZERO) == player.frames[key][index], "Timed death frame")
			var phase_clock: Dictionary = player.snapshot()
			check(player.frame("death-ground", "east", 20.0 + elapsed + duration * 0.5, Vector2.ZERO, "diving-helmet") == player.equipment_frames["diving-helmet"][key][index], "Equipped death matches phase")
			check(player.snapshot() == phase_clock, "Helmet preserves death clock")
			elapsed += duration
		var terminal = player.frames[key].back()
		check(player.frame("death-ground", "east", 50.0, Vector2.ZERO) == terminal, "Death holds after many cycles")
		var saved: Dictionary = player.snapshot()
		player.frame("idle", "east", 51.0, Vector2.ZERO)
		player.restore_snapshot(saved)
		check(player.frame("death-ground", "east", 50.0, Vector2.ZERO) == terminal, "Saved terminal playback restores")
		check(player.frame("death-ground", "east", 50.0, Vector2.ZERO, "diving-helmet") == player.equipment_frames["diving-helmet"][key].back(), "Saved equipped terminal holds")
		var water_key := "death-water-east"
		player.load_manifest("res://character/crew-underwater-v1/pilot/%s-death-water-east/manifest.json" % pair[0], true)
		check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-death-water-east/manifest.json" % pair[0]), "Water-death helmet loads")
		player.frame("death-water", "east", 52.0, Vector2.ZERO)
		var water_elapsed := 0.0
		for index in range(6):
			var duration: float = player.timing[water_key].durations[index] / 1000.0
			for equipped in [false,true]:
				var expected = player.equipment_frames["diving-helmet"][water_key][index] if equipped else player.frames[water_key][index]
				check(player.frame("death-water", "east", 52.0 + water_elapsed + duration*0.5, Vector2.ZERO, "diving-helmet" if equipped else "") == expected, "Water death exact phase")
			water_elapsed += duration
		check(player.frame("death-water", "east", 500.0, Vector2.ZERO) == player.frames[water_key].back(), "Water death holds terminal frame")
		for transition in ["equip-helmet", "remove-helmet"]:
			var transition_key: String = transition + "-east"
			player.load_manifest("res://character/crew-underwater-v1/locker/%s-%s/manifest.json" % [pair[0], transition_key], true)
			player.frame(transition, "east", 60.0, Vector2.ZERO)
			var transition_elapsed := 0.0
			check(player.frames[transition_key].size() == 12, "Full locker sequence has twelve poses")
			for index in range(12):
				var duration: float = player.timing[transition_key].durations[index] / 1000.0
				var pose = player.frame(transition, "east", 60.0 + transition_elapsed + duration * 0.5, Vector2.ZERO)
				check(pose == player.frames[transition_key][index], "Transition timed pose " + transition_key)
				check(pose.get_size() == Vector2(92,104) and pose.get_meta("crew_pivot") == Vector2(46,98), "Tall transition registration")
				transition_elapsed += duration
			check(player.frame(transition, "east", 100.0, Vector2.ZERO) == player.frames[transition_key].back(), "Transition holds instead of looping " + transition_key)
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
