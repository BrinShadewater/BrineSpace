extends SceneTree
const Player = preload("res://scripts/crew_sprite_player.gd")
var failures := 0

func check(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

# A helmet change restarts the current clip (owner decision, October 12, 2026): helmeted
# clips carry their own timing. Every section therefore plays the clip bare first and
# then again from its first frame with the helmet on.
func _init() -> void:
	for pair in [["bill", "major-bill-v2"], ["veld", "dr-veld-v1"], ["branforth", "chief-engineer-branforth-v1"]]:
		var player = Player.new()
		player.load_manifest("res://character/%s/final/manifest.json" % pair[1])
		var dry = player.frame("idle", "south", 1.0, Vector2.ZERO)
		var dry_states := ["idle", "walk", "run", "interact"] if pair[0] == "bill" else ["idle", "walk", "interact"]
		dry_states.append_array(["kneel", "repair", "stand"])
		for dry_state in dry_states:
			for dry_direction in ["south", "north", "east", "west"]:
				if dry_state in ["interact", "kneel", "repair", "stand"] and dry_direction != "east": continue
				var dry_key: String = dry_state + "-" + dry_direction
				check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/dry/%s-%s/manifest.json" % [pair[0], dry_key]), "Dry helmet loads " + dry_key)
				player.frame(dry_state, dry_direction, 0.0, Vector2.ZERO)
				var elapsed := 0.0
				for index in range(6):
					var duration: float = float(player.timing[dry_key].durations[index]) / 1000.0
					var midpoint := elapsed + duration * 0.5
					var position := Vector2.ZERO
					if player.strides.has(dry_state): position.x = midpoint / player.cycle_seconds(dry_key) * float(player.strides[dry_state])
					check(player.frame(dry_state, dry_direction, midpoint, position) == player.frames[dry_key][index], "Dry base phase " + dry_key)
					elapsed += duration
				check(player.frame(dry_state, dry_direction, 100.0, Vector2.ZERO, "diving-helmet") == player.equipment_frames["diving-helmet"][dry_key][0], "Dry helmet restarts the clip " + dry_key)
				elapsed = 0.0
				for index in range(6):
					var duration: float = float(player.timing[dry_key].durations[index]) / 1000.0
					var midpoint := elapsed + duration * 0.5
					var position := Vector2.ZERO
					if player.strides.has(dry_state): position.x = midpoint / player.cycle_seconds(dry_key) * float(player.strides[dry_state])
					check(player.frame(dry_state, dry_direction, 100.0 + midpoint, position, "diving-helmet") == player.equipment_frames["diving-helmet"][dry_key][index], "Dry equipped phase " + dry_key)
					elapsed += duration
		var directions := ["east", "south", "north", "west"]
		for direction in directions:
			player.load_manifest("res://character/crew-underwater-v1/pilot/%s-swim-%s/manifest.json" % [pair[0], direction], true)
			var key: String = "swim-" + direction
			check(player.frames[key].size() == 6, "Six swim poses for " + pair[0] + direction)
			var pivot := Vector2(61, 44) if direction == "east" else Vector2(46, 44)
			if direction == "west": pivot = Vector2(31, 44)
			if direction == "north": pivot = Vector2(46, {"bill":30,"veld":27,"branforth":32}[pair[0]])
			for texture in player.frames[key]:
				check(texture.get_meta("crew_pivot") == pivot, "Direction-specific torso pivot")
			player.frame("idle", "south", 2.0, Vector2.ZERO)
			player.frame("swim", direction, 3.0, Vector2.ZERO)
			check(player.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-swim-%s/manifest.json" % [pair[0], direction]), "Swim helmet matches base: " + direction)
			# A 0.16-cell stride advances one cycle; sample the middle of each phase.
			for index in range(6):
				var distance := 0.16 * (float(index) + 0.5) / 6.0
				check(player.frame("swim", direction, 3.1 + index * 0.1, Vector2(distance, 0)) == player.frames[key][index], "Distance-driven swim phase")
			check(player.frame("swim", direction, 5.0, Vector2(0.16 * (1.0 + 0.5 / 6.0), 0)) == player.frames[key][0], "Swim loops into first phase of next stride")
			check(player.frame("swim", direction, 6.0, Vector2.ZERO, "diving-helmet") == player.equipment_frames["diving-helmet"][key][0], "Swim helmet restarts the stride: " + direction)
			for index in range(6):
				var distance := 0.16 * (float(index) + 0.5) / 6.0
				check(player.frame("swim", direction, 6.1 + index * 0.1, Vector2(distance, 0), "diving-helmet") == player.equipment_frames["diving-helmet"][key][index], "Swim helmet uses distance phase: " + direction)
			check(player.frame("swim", direction, 8.0, Vector2(0.16 * (1.0 + 0.5 / 6.0), 0), "diving-helmet") == player.equipment_frames["diving-helmet"][key][0], "Helmeted swim loops into the next stride: " + direction)
		check(player.frame("idle", "south", 9.0, Vector2.ZERO) == dry, "Dry frame survives both expansions")
	for actor in ["bill", "veld", "branforth"]:
		var west_treader = Player.new()
		west_treader.load_manifest("res://character/crew-underwater-v1/pilot/%s-tread-west/manifest.json" % actor)
		check(west_treader.frames["tread-west"].size() == 6, "Six west tread poses for " + actor)
		west_treader.frame("tread", "west", 40.0, Vector2.ZERO)
		check(west_treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-tread-west/manifest.json" % actor), "West helmet matches base")
		for index in range(6):
			var west_pose = west_treader.frame("tread", "west", 40.0 + (index + 0.5) * 0.16, Vector2.ZERO)
			check(west_pose == west_treader.frames["tread-west"][index], "West tread advances without travel for " + actor)
			check(west_pose.get_meta("crew_pivot") == Vector2(46, 35), "West tread shoulder pivot")
		check(west_treader.frame("tread", "west", 41.04, Vector2.ZERO) == west_treader.frames["tread-west"][0], "West tread loops")
		var west_clock: Array = west_treader.equipment_frames["diving-helmet"]["tread-west"]
		check(west_treader.frame("tread", "west", 42.0, Vector2.ZERO, "diving-helmet") == west_clock[0], "West helmet restarts the tread")
		for index in range(6):
			check(west_treader.frame("tread", "west", 42.0 + (index + 0.5) * 0.16, Vector2.ZERO, "diving-helmet") == west_clock[index], "West helmet follows body phase")
		check(west_treader.frame("tread", "west", 42.0 + 1.04, Vector2.ZERO, "diving-helmet") == west_clock[0], "West tread loops with helmet")
		var rear_treader = Player.new()
		rear_treader.load_manifest("res://character/crew-underwater-v1/pilot/%s-tread-north/manifest.json" % actor)
		check(rear_treader.frames["tread-north"].size() == 6, "Six rear tread poses for " + actor)
		rear_treader.frame("tread", "north", 30.0, Vector2.ZERO)
		check(rear_treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-tread-north/manifest.json" % actor), "Rear helmet matches base")
		for index in range(6):
			var rear_pose = rear_treader.frame("tread", "north", 30.0 + (index + 0.5) * 0.16, Vector2.ZERO)
			check(rear_pose == rear_treader.frames["tread-north"][index], "Rear tread advances without travel for " + actor)
			check(rear_pose.get_meta("crew_pivot") == Vector2(46, 35), "Rear tread shoulder pivot")
		check(rear_treader.frame("tread", "north", 31.04, Vector2.ZERO) == rear_treader.frames["tread-north"][0], "Rear tread loops")
		var rear_clock: Array = rear_treader.equipment_frames["diving-helmet"]["tread-north"]
		check(rear_treader.frame("tread", "north", 32.0, Vector2.ZERO, "diving-helmet") == rear_clock[0], "Rear helmet restarts the tread")
		for index in range(6):
			check(rear_treader.frame("tread", "north", 32.0 + (index + 0.5) * 0.16, Vector2.ZERO, "diving-helmet") == rear_clock[index], "Rear helmet follows body phase")
		check(rear_treader.frame("tread", "north", 32.0 + 1.04, Vector2.ZERO, "diving-helmet") == rear_clock[0], "Rear tread loops with helmet")
		var side_treader = Player.new()
		side_treader.load_manifest("res://character/crew-underwater-v1/pilot/%s-tread-east/manifest.json" % actor)
		check(side_treader.frames["tread-east"].size() == 6, "Six east tread poses for " + actor)
		side_treader.frame("tread", "east", 20.0, Vector2.ZERO)
		check(side_treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-tread-east/manifest.json" % actor), "East tread helmet matches base")
		for index in range(6):
			var pose = side_treader.frame("tread", "east", 20.0 + (index + 0.5) * 0.16, Vector2.ZERO)
			check(pose == side_treader.frames["tread-east"][index], "East tread advances without travel for " + actor)
			check(pose.get_meta("crew_pivot") == Vector2(46, 35), "East tread shoulder pivot")
		check(side_treader.frame("tread", "east", 21.04, Vector2.ZERO) == side_treader.frames["tread-east"][0], "East tread loops")
		var side_clock: Array = side_treader.equipment_frames["diving-helmet"]["tread-east"]
		check(side_treader.frame("tread", "east", 22.0, Vector2.ZERO, "diving-helmet") == side_clock[0], "East tread helmet restarts the tread")
		for index in range(6):
			check(side_treader.frame("tread", "east", 22.0 + (index + 0.5) * 0.16, Vector2.ZERO, "diving-helmet") == side_clock[index], "East tread helmet phase matches body")
		check(side_treader.frame("tread", "east", 22.0 + 1.04, Vector2.ZERO, "diving-helmet") == side_clock[0], "East tread loops with helmet")
		var treader = Player.new()
		treader.load_manifest("res://character/crew-underwater-v1/pilot/%s-tread-south/manifest.json" % actor)
		treader.frame("tread", "south", 10.0, Vector2.ZERO)
		check(treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-tread-south/manifest.json" % actor), "Helmet row matches base timing and pivot")
		check(not treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/pilot/%s-death-water-east/manifest.json" % actor), "Mismatched equipment state rejected without replacing fitted row")
		check(treader.frame("tread", "south", 10.0, Vector2.ZERO, "missing-equipment") == null, "Missing equipment does not expose bare head")
		# Asking for other equipment restarted the clip; start the bare tread again at the same instant.
		treader.frame("tread", "south", 10.0, Vector2.ZERO)
		for index in range(6):
			check(treader.frame("tread", "south", 10.0 + (index + 0.5) * 0.16, Vector2.ZERO) == treader.frames["tread-south"][index], "Treading advances while position remains fixed")
		check(treader.frame("tread", "south", 11.04, Vector2.ZERO) == treader.frames["tread-south"][0], "Stationary treading loops")
		var saved: Dictionary = treader.snapshot()
		treader.frame("tread", "south", 12.0, Vector2.ZERO)
		treader.restore_snapshot(saved)
		check(treader.frame("tread", "south", 11.04, Vector2.ZERO) == treader.frames["tread-south"][0], "Stationary tread phase restores")
		var south_gear: Array = treader.equipment_frames["diving-helmet"]["tread-south"]
		check(treader.frame("tread", "south", 13.0, Vector2.ZERO, "diving-helmet") == south_gear[0], "Equipment switch restarts the tread")
		for index in range(6):
			check(treader.frame("tread", "south", 13.0 + (index + 0.5) * 0.16, Vector2.ZERO, "diving-helmet") == south_gear[index], "Helmet follows its own clock")
		var helmet_saved: Dictionary = treader.snapshot()
		treader.frame("tread", "south", 15.0, Vector2.ZERO, "diving-helmet")
		treader.restore_snapshot(helmet_saved)
		check(treader.snapshot() == helmet_saved and helmet_saved.equipment == "diving-helmet", "Helmeted tread clock restores")
		treader.load_manifest("res://character/crew-underwater-v1/pilot/%s-swim-east/manifest.json" % actor, true)
		check(treader.load_equipment_manifest("diving-helmet", "res://character/crew-underwater-v1/equipment/fitting/%s-swim-east/manifest.json" % actor), "Swim helmet row loads")
		check(treader.equipment_frames["diving-helmet"].has("tread-south"), "Adding swim helmet preserves tread equipment")
		treader.frame("swim", "east", 20.0, Vector2.ZERO, "diving-helmet")
		check(treader.frame("swim", "east", 20.1, Vector2(0.04, 0), "diving-helmet") == treader.equipment_frames["diving-helmet"]["swim-east"][1], "Equipped swim uses distance clock")
	verify_turn_clocks()
	print("CREW SWIM PACKS: %d failures" % failures)
	quit(1 if failures else 0)

func verify_turn_clocks() -> void:
	for pair in [["bill","major-bill-v2"],["veld","dr-veld-v1"],["branforth","chief-engineer-branforth-v1"]]:
		var player = preload("res://scripts/crew_sprite_player.gd").new()
		player.load_manifest("res://character/%s/final/manifest.json" % pair[1])
		for direction in ["east","south"]:
			player.load_manifest("res://character/crew-underwater-v1/revisions/%s-swim-%s-v2/manifest.json" % [pair[0],direction],true)
		for state in ["walk","swim"]:
			player.current_key = ""
			var stride: float = player.strides[state]
			player.frame(state,"east",100.0,Vector2.ZERO)
			player.frame(state,"east",100.1,Vector2(stride*0.375,0))
			var grid = preload("res://scripts/grid_canvas.gd").new()
			grid.human_animation_timing = player.timing.duplicate(true)
			grid.human_stride_distance = player.strides.duplicate(true)
			grid.human_animation_key = player.current_key
			grid.human_animation_phase = player.phase
			grid.human_animation_last_time = player.last_time
			grid.human_animation_last_position = player.last_position
			var position := Vector2(stride*0.375,stride*0.1)
			player.frame(state,"south",100.2,position)
			var expected: float = player.cycle_seconds(state+"-south")*0.475
			check(is_equal_approx(player.phase,expected),"Turn preserves gait fraction and adds traveled distance")
			check(is_equal_approx(grid._advance_human_animation(state+"-south",100.2,position),expected),"Bill clock follows same turn fraction")
			player.frame(state,"south",100.2,position)
			check(is_equal_approx(player.phase,expected),"Repeated sample cannot advance turn twice")
			player.frame(state,"east",100.3,Vector2(10,10))
			check(player.phase==0.0,"Teleport resets gait instead of preserving phase")
			player.frame(state,"south",99.0,Vector2(10,10))
			check(player.phase==0.0,"Rewound time resets facing change")
			grid.free()

