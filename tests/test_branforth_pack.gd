extends SceneTree
const NPC = preload("res://scripts/branforth_npc.gd")
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func _init() -> void:
	var player = Player.new()
	player.load_manifest("res://character/chief-engineer-branforth-v1/final/manifest.json")
	for direction in ["north", "south", "east", "west"]:
		for action in ["idle", "walk"]:
			check(player.frames.has(action + "-" + direction), "Directional coverage")
	for action in ["interact", "kneel", "repair", "stand"]:
		check(player.frames.has(action + "-east"), "Engineering action coverage")
	for key in player.frames:
		check(player.frames[key].size() == 6, key + " frame count")
		for texture in player.frames[key]:
			check(texture.get_size() == Vector2(92, 92), "Crew frame geometry")
		# Exercise every timed pose through the actual runtime player, including
		# a second loop and one-shot clamping. Walking advances by distance.
		var sample_player = Player.new()
		sample_player.frames = player.frames
		sample_player.timing = player.timing
		sample_player.strides = player.strides
		var parts: PackedStringArray = key.split("-")
		var cycle: float = sample_player.cycle_seconds(key)
		sample_player.frame(parts[0], parts[1], 10.0, Vector2.ZERO)
		for loop_index in range(2):
			var elapsed := 0.0
			for index in range(6):
				var duration: float = float(player.timing[key].durations[index]) / 1000.0
				var time: float = loop_index * cycle + elapsed + duration * 0.5
				var pos := Vector2(time / cycle * 0.12, 0) if parts[0] == "walk" else Vector2.ZERO
				var actual = sample_player.frame(parts[0], parts[1], 10.0 + time, pos)
				var expected: int = index if player.timing[key].loop or loop_index == 0 else 5
				check(actual == player.frames[key][expected], key + " timed frame %d loop %d" % [index, loop_index])
				elapsed += duration
	for pair in [["idle-east",0,"kneel-east",0],["kneel-east",5,"repair-east",0],["repair-east",5,"stand-east",0],["stand-east",5,"idle-east",0],["idle-east",0,"interact-east",0],["interact-east",5,"idle-east",0]]:
		check(player.frames[pair[0]][pair[1]].get_image().get_data() == player.frames[pair[2]][pair[3]].get_image().get_data(), "Action endpoint continuity")
	var npc = NPC.new()
	var other = NPC.new()
	npc.needs.maintenance = 0.0
	check(other.needs.maintenance == 80.0, "Needs are independent")
	check(npc.decision_rng != other.decision_rng, "Independent random streams")
	npc.goal = "maintenance"
	npc.arrive()
	check(npc.state == "kneel" and npc.stage == "kneel", "Engineering work starts kneeling")
	check(npc.activity == "servicing equipment", "Engineer action meaning")
	npc.goal = "curiosity"
	npc.arrive()
	check(npc.state == "interact" and npc.direction == "east", "Diagnostics use authored direction")
	check(NPC.valid_snapshot(npc.snapshot()), "Engineer snapshot validates")
	print("BRANFORTH PACK: %d failures" % failures)
	quit(1 if failures else 0)
