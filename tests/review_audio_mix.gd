extends SceneTree
## Native stereo mixer capture: Godot --audio-driver Dummy --path . --script res://tests/review_audio_mix.gd
## Writes a 32-second mix audition under output/audio-polish; isolated fixture saves.
const Preferences = preload("res://scripts/title_settings.gd")
var capture := AudioEffectCapture.new()
var pcm := PackedByteArray()
var peak := 0.0
var total_frames := 0
func _init() -> void:
	call_deferred("run")
func collect() -> void:
	var available := capture.get_frames_available()
	if available == 0: return
	var buffer := capture.get_buffer(available)
	var offset := pcm.size()
	pcm.resize(offset+buffer.size()*4)
	for i in buffer.size():
		peak = maxf(peak,maxf(absf(buffer[i].x),absf(buffer[i].y)))
		pcm.encode_s16(offset+i*4,roundi(clampf(buffer[i].x,-1.0,1.0)*32767.0))
		pcm.encode_s16(offset+i*4+2,roundi(clampf(buffer[i].y,-1.0,1.0)*32767.0))
	total_frames += buffer.size()
func run() -> void:
	if AudioServer.get_speaker_mode() != AudioServer.SPEAKER_MODE_STEREO:
		push_error("Use --audio-driver Dummy for a stereo capture; surround devices append multiple speaker pairs.")
		quit(1)
		return
	Preferences.save_path = "user://mix_review_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://mix_review_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://mix_review_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	Preferences.music_volume = 1.0
	AudioServer.set_bus_mute(0,false)
	AudioServer.set_bus_volume_linear(0,1.0)
	var music = preload("res://scripts/station_music.gd").ensure(game)
	await process_frame
	music.player.seek(20.0)
	capture.buffer_length = 2.0
	var effect_index := AudioServer.get_bus_effect_count(0)
	AudioServer.add_bus_effect(0,capture)
	var events := {1:"ui_comms",3:"placement",5:"ui_saved",6:"door",9:"power_on",12:"cargo",15:"terminal",19:"discovery",25:"warning"}
	if "--missing-cues" in OS.get_cmdline_user_args():
		events = {1:"build_complete",4:"build_blocked",7:"launch",10:"footstep",13:"tools",16:"repair",20:"ui_end",26:"ui_failure"}
		for kind in ["build_complete","build_blocked","launch","footstep","tools","repair","ui_end","ui_failure","refrigeration","workshop"]:
			assert(preload("res://scripts/station_audio_cues.gd").get_stream(kind).save_to_wav("res://output/audio-missing-cues/"+kind+".wav") == OK)
	var sent := {}
	var expanded := "--expanded" in OS.get_cmdline_user_args()
	if expanded:
		events = {1:"swim",3:"suit",5:"bubbles",7:"mining_work",10:"salvage_work",13:"galley_work",17:"medical_work",21:"lab_work",25:"cultivation_work",29:"warning_oxygen",33:"warning_power",37:"warning_hull"}
		for kind in preload("res://scripts/station_audio_cues.gd").EXPANDED_DURATIONS:
			assert(preload("res://scripts/station_audio_cues.gd").get_stream(kind).save_to_wav("res://output/audio-expanded/"+kind+".wav") == OK)
	if "--variation" in OS.get_cmdline_user_args():
		events = {1:"footstep",2:"footstep",3:"footstep",4:"footstep",6:"tools",10:"tools",14:"repair",18:"repair",22:"launch",27:"launch"}
	if "--recovery" in OS.get_cmdline_user_args():
		events = {2:"crew_dispatch",8:"crew_awake",15:"warning",22:"all_clear"}
		for kind in ["crew_dispatch","crew_awake","all_clear"]:
			assert(preload("res://scripts/station_audio_cues.gd").get_stream(kind).save_to_wav("res://output/audio-recovery/"+kind+".wav") == OK)
	var started := Time.get_ticks_msec()
	if "--equipment" in OS.get_cmdline_user_args():
		events = {2:"helmet_lock",9:"helmet_release",18:"site_empty"}
		for kind in ["helmet_lock","helmet_release","site_empty"]:
			assert(preload("res://scripts/station_audio_cues.gd").get_stream(kind).save_to_wav("res://output/audio-equipment/"+kind+".wav") == OK)
	if "--airlock-cues" in OS.get_cmdline_user_args():
		events = {2:"airlock_pressure",6:"airlock_release",9:"airlock_ready",15:"ui_recall",23:"crew_return"}
		for kind in ["airlock_pressure","airlock_release","airlock_ready","ui_recall","crew_return"]:
			assert(preload("res://scripts/station_audio_cues.gd").get_stream(kind).save_to_wav("res://output/audio-airlock/"+kind+".wav") == OK)
	while Time.get_ticks_msec()-started < (42000 if expanded else 32000):
		var seconds := float(Time.get_ticks_msec()-started)/1000.0
		for at in events:
			if seconds >= float(at) and not sent.has(at):
				if expanded and str(events[at]).begins_with("warning_"):
					var condition: String = {"warning_oxygen":"oxygen","warning_power":"power_reserve","warning_hull":"integrity"}[events[at]]
					game.station_sound.warning_state = {condition:true}
					game.station_sound.last_event.erase("warning")
					game.play_station_sound("warning")
				else: game.play_station_sound(events[at])
				sent[at] = true
		if seconds >= 22.0 and not sent.has("crossfade"):
			music.player.seek(music.player.stream.get_length()-5.8)
			sent["crossfade"] = true
		collect()
		await create_timer(0.03).timeout
	collect()
	AudioServer.remove_bus_effect(0,effect_index)
	var wav := AudioStreamWAV.new()
	wav.format = AudioStreamWAV.FORMAT_16_BITS
	wav.stereo = true
	wav.mix_rate = roundi(AudioServer.get_mix_rate())
	wav.data = pcm
	var output_path := "res://output/audio-polish/in-engine-mix.wav"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--output="): output_path = argument.trim_prefix("--output=")
	var error := wav.save_to_wav(output_path)
	print("MIX CAPTURE: frames=%d peak_db=%.2f dropped=%d saved=%d" % [total_frames,linear_to_db(maxf(peak,0.00001)),capture.get_discarded_frames(),error])
	game.queue_free()
	music.queue_free()
	await process_frame
	await create_timer(0.2).timeout
	quit(0 if error == OK and peak > 0.0001 and peak < 1.0 and capture.get_discarded_frames() == 0 else 1)
