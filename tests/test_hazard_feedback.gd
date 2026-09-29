extends SceneTree
## Hazard feedback rules (owner-approved Sept 29): the red edge tint appears only when oxygen or
## integrity run low and pulses slowly, Reduced Motion holds it steady and never shakes, Low quality
## draws nothing, and a creak is brief, small, and only at low integrity.
const Hazard = preload("res://scripts/hazard_feedback.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	expect(Hazard.PULSE_PERIOD >= 1.0, "The tint pulses at most once a second")
	expect(Hazard.CREAK_PIXELS <= 3.0 and Hazard.CREAK_LENGTH <= 1.0, "A creak is small and brief")
	expect(Hazard.tint_alpha(0.0, 1.0, false) == 0.0, "No tint when nothing is wrong")
	expect(is_equal_approx(Hazard.tint_alpha(1.0, 0.0, true), Hazard.tint_alpha(1.0, 2.0, true)), "Reduced Motion holds the tint steady")
	expect(Hazard.creak_offset(0.1, 100.0) == Vector2.ZERO, "No creak at healthy integrity")
	var moved := false
	for i in range(60): moved = moved or Hazard.creak_offset(17.0 * 0.0 + float(i) * 0.01 + (Hazard.CREAK_PERIOD - 17.0), 30.0) != Vector2.ZERO
	expect(moved, "A creak shivers the view at low integrity")
	expect(Hazard.creak_offset(20.0, 30.0) == Vector2.ZERO, "The creak is over between shivers")
	TitleSettings.save_path = "user://hazard_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://hazard_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://hazard_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game._set_paused(true, false)
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = false
	game.resources["integrity"] = 100
	game.resources["oxygen"] = game._get_resource_capacity("oxygen")
	Hazard.update(game)
	expect(not game.hazard_tint.visible, "A healthy station shows no tint")
	game.resources["integrity"] = 10
	Hazard.update(game)
	expect(game.hazard_tint.visible and game.hazard_tint.modulate.a > 0.1, "Low integrity shows the tint")
	TitleSettings.effects_quality = 0
	Hazard.update(game)
	expect(not game.hazard_tint.visible, "Low quality shows no tint")
	TitleSettings.effects_quality = 1
	game.resources["integrity"] = 100
	game.resources["oxygen"] = 0
	Hazard.update(game)
	expect(game.hazard_tint.visible, "Empty oxygen shows the tint")
	# Venting draws without error for a cracked room at every quality, including Reduced Motion.
	game._place_room("hydroponics_bay", Vector2i(21, 19), true) if game.placed_rooms.is_empty() else null
	var room: Dictionary = game.placed_rooms[0]
	room["hull_crack"] = 1.0
	var canvas := Node2D.new()
	canvas.draw.connect(func() -> void:
		for quality in [0, 1, 2]:
			TitleSettings.effects_quality = quality
			for reduced in [false, true]:
				TitleSettings.reduced_motion = reduced
				preload("res://scripts/station_effects.gd").draw_hazards(canvas, game, game.placed_rooms, 96.0))
	root.add_child(canvas)
	canvas.queue_redraw()
	await process_frame
	await process_frame
	room.erase("hull_crack")
	# Build flourishes: a room that appears after the view has started gets a scan line, and none of it
	# draws under Reduced Motion or at Low quality.
	var Effects = preload("res://scripts/station_effects.gd")
	Effects._seen_game = 0
	var flourish := Node2D.new()
	flourish.draw.connect(func() -> void: Effects.draw_build_flourish(flourish, game, game.placed_rooms, 96.0))
	root.add_child(flourish)
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = false
	flourish.queue_redraw()
	await process_frame
	await process_frame
	expect(Effects._scan_start.is_empty(), "Rooms already on the map get no scan line")
	game.testing_free_build = true
	game._place_room("galley", Vector2i(23, 19), true)
	flourish.queue_redraw()
	await process_frame
	await process_frame
	expect(not Effects._scan_start.is_empty() or not Effects._awaiting.is_empty(), "A room built later starts a scan line")
	print("HAZARD FEEDBACK: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
