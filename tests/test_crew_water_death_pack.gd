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
		check(original.get_meta("crew_pivot") == Vector2(46, 86), "Dry frames retain floor pivot")
		var before: Dictionary = player.snapshot()
		player.load_manifest("res://character/crew-underwater-v1/pilot/%s-death-water-east/manifest.json" % pair[0], true)
		check(player.frames.size() == old_count + 1, "Expansion retains dry states")
		check(player.snapshot() == before, "Loading expansion preserves current clock")
		check(player.frame("idle", "east", 10.0, Vector2.ZERO) == original, "Expansion retains dry texture")
		check(player.strides.has("walk"), "Expansion preserves locomotion stride")
		var key := "death-water-east"
		check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-death-water-east/manifest.json" % pair[0]), "Water death helmet timing matches")
		player.frame("death-water", "east", 20.0, Vector2.ZERO)
		var elapsed := 0.0
		for index in range(6):
			var duration: float = player.timing[key].durations[index] / 1000.0
			check(player.frame("death-water", "east", 20.0 + elapsed + duration * 0.5, Vector2.ZERO) == player.frames[key][index], "Timed death frame")
			elapsed += duration
		var terminal = player.frames[key].back()
		for texture in player.frames[key]:
			check(texture.get_meta("crew_pivot") == Vector2(61, 44), "Every water pose carries its torso pivot")
		check(player.frame("death-water", "east", 50.0, Vector2.ZERO) == terminal, "Death holds after many cycles")
		var equipped_terminal = player.equipment_frames["diving-helmet"][key].back()
		check(player.frame("death-water", "east", 50.0, Vector2.ZERO, "diving-helmet") == equipped_terminal, "Helmet remains on terminal death pose")
		var saved: Dictionary = player.snapshot()
		player.frame("idle", "east", 51.0, Vector2.ZERO)
		player.restore_snapshot(saved)
		check(player.frame("death-water", "east", 50.0, Vector2.ZERO) == terminal, "Saved terminal playback restores")
	print("CREW WATER DEATH PACK: %d failures" % failures)
	quit(1 if failures else 0)
