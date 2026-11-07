extends SceneTree
## Stage 2 lighting rules that must hold without a window: blackout red pulses at most once a second and
## holds still under Reduced Motion, the beacon turns slowly, no emergency light outside a blackout, and
## Low quality hides the light map. Spec: docs/superpowers/specs/2026-09-29-lighting-atmosphere-design.md
const RoomLighting = preload("res://rooms/whole-room/room_lighting.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func run() -> void:
	expect(RoomLighting.EMERGENCY_PERIOD >= 1.0, "The emergency pulse is at most one per second")
	expect(RoomLighting.BEACON_TURNS_PER_SECOND <= 0.5, "The beacon turns slowly (at most half a turn a second)")
	expect(RoomLighting.DARK_AMBIENT >= 0.5, "Unpowered rooms stay readable (ambient floor 0.5 or more)")
	TitleSettings.save_path = "user://light_emergency_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://light_emergency_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://light_emergency_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.tick_timer.stop()
	game._set_paused(true, false)
	game.testing_free_build = true
	game._place_room("hydroponics_bay", Vector2i(21, 19), true)
	game._refresh_all()
	TitleSettings.effects_quality = 1
	TitleSettings.reduced_motion = false
	game.power_blackout = false
	expect(RoomLighting.emergency_phase(game) < 0.0, "No emergency light outside a blackout")
	game.power_blackout = true
	var phase := RoomLighting.emergency_phase(game)
	expect(phase >= 0.0 and phase < 1.0, "A blackout has an emergency phase in 0..1")
	# Reduced Motion: a fixed phase, so the light never pulses.
	TitleSettings.reduced_motion = true
	var still_a := RoomLighting.emergency_phase(game)
	game.visual_time_seconds += 0.7
	var still_b := RoomLighting.emergency_phase(game)
	expect(is_equal_approx(still_a, still_b), "Reduced Motion holds the emergency light still")
	# Normal motion: the phase advances with time, one full pulse per EMERGENCY_PERIOD.
	TitleSettings.reduced_motion = false
	var before := RoomLighting.emergency_phase(game)
	game.visual_time_seconds += RoomLighting.EMERGENCY_PERIOD * 0.25
	var after := RoomLighting.emergency_phase(game)
	expect(absf(fposmod(after - before, 1.0) - 0.25) < 0.02, "A quarter of a period moves the phase a quarter")
	# Low quality hides the light map.
	TitleSettings.effects_quality = 0
	RoomLighting.update_light_map(game)
	expect(not game.light_map.visible, "Low quality hides the light map")
	TitleSettings.effects_quality = 1
	RoomLighting.update_light_map(game)
	expect(game.light_map.visible, "Medium shows the light map")
	print("LIGHT EMERGENCY: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
