extends SceneTree
## Native stereo render: Godot --audio-driver Dummy --path . --script res://tests/test_audio_space.gd
const Space = preload("res://scripts/station_audio_space.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var capture := AudioEffectCapture.new()
var game
var probe: AudioStreamPlayer2D
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
		push_error(label)
func sample(cell: Vector2) -> Vector2:
	Space.configure(probe,game,cell)
	await create_timer(0.3).timeout # Allow buffered spatial gain ramps to settle before measuring.
	capture.clear_buffer()
	await create_timer(0.3).timeout
	var frames := capture.get_buffer(capture.get_frames_available())
	print("PROBE cell=%s position=%s listener=%s playing=%s mute=%s frames=%d radius=%.1f" % [cell,probe.position,game.station_sound.listener.position,probe.playing,AudioServer.is_bus_mute(0),frames.size(),probe.max_distance])
	var energy := Vector2.ZERO
	for frame in frames: energy += frame*frame
	return energy/maxi(1,frames.size())
func run() -> void:
	check(AudioServer.get_speaker_mode() == AudioServer.SPEAKER_MODE_STEREO,"Use the stereo Dummy driver")
	Preferences.save_path = "user://audio_space_%d.cfg" % OS.get_process_id()
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://audio_space_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://audio_space_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	game.station_sound.set_process(false)
	game.crew_comms.set_process(false)
	Preferences.effects_volume = 0.0
	for voice in game.station_sound.voices.values(): voice.player.stop()
	for layer in game.station_sound.layers.values(): layer.stop()
	var music = preload("res://scripts/station_music.gd").ensure(game)
	await process_frame
	music.set_process(false)
	for deck in music.decks: deck.stop()
	AudioServer.set_bus_mute(0,false)
	AudioServer.set_bus_volume_linear(0,1.0)
	await create_timer(0.6).timeout # Let the normal deferred opening camera settle.
	game.station_sound.listener.position = Space.listener_position(game)
	var center: Vector2 = (game.grid_view.get_global_transform().affine_inverse()*Space.listener_position(game))/game.get_cell_size()-Vector2.ONE*0.5
	probe = AudioStreamPlayer2D.new()
	probe.stream = preload("res://scripts/station_audio_cues.gd").get_stream("core")
	probe.volume_db = -12.0
	game.station_sound.add_child(probe)
	probe.play()
	capture.buffer_length = 2.0
	var effect_index := AudioServer.get_bus_effect_count(0)
	AudioServer.add_bus_effect(0,capture)
	var left := await sample(center-Vector2(2,0))
	var right := await sample(center+Vector2(2,0))
	var near := await sample(center)
	var far := await sample(center+Vector2(40,0))
	check(left.x > left.y*1.05,"Left source is louder in the left channel")
	check(right.y > right.x*1.05,"Right source is louder in the right channel")
	check(near.length() > 0.000001,"Nearby source reaches the mixer")
	check(far.length() < near.length()*0.01,"Offscreen distant source fades out")
	# Follow the same source through a real scroll, then a zoom change.
	var world_cell := center
	var old_position := Space.screen_position(game,world_cell)
	game.grid_scroll.scroll_horizontal += 100
	await process_frame
	check(Space.screen_position(game,world_cell).x < old_position.x,"Panning moves the audible source with the grid")
	game.station_sound.listener.position = Space.listener_position(game)
	game._set_grid_zoom(game.grid_zoom*0.8)
	await process_frame
	Space.configure(probe,game,world_cell)
	check(probe.position.is_equal_approx(Space.screen_position(game,world_cell)),"Zoom updates the source position")
	check(game.station_sound.layers.size() == 9,"Room sound layers remain bounded")
	AudioServer.remove_bus_effect(0,effect_index)
	print("SPATIAL MIX: left=%s right=%s near=%s far=%s" % [left,right,near,far])
	game.queue_free()
	music.queue_free()
	await process_frame
	await create_timer(0.2).timeout
	print("AUDIO SPACE PASS" if failures == 0 else "AUDIO SPACE FAIL")
	quit(failures)
