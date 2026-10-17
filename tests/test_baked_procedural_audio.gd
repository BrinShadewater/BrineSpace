extends SceneTree
const Cues = preload("res://scripts/station_audio_cues.gd")
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void:
	var synth_usec := 0
	var loaded_usec := 0
	var worst_load := 0
	for kind in Cues.BAKED:
		var stamp := Time.get_ticks_usec()
		var reference := Cues.synthesize(kind)
		synth_usec += Time.get_ticks_usec() - stamp
		Cues.cache.erase(kind)
		stamp = Time.get_ticks_usec()
		var actual := Cues.get_stream(kind)
		var duration := Time.get_ticks_usec() - stamp
		loaded_usec += duration
		worst_load = maxi(worst_load,duration)
		check(actual.data==reference.data,"Exact PCM: "+kind)
		for field in ["format","mix_rate","stereo","loop_mode","loop_begin","loop_end"]:
			check(actual.get(field)==reference.get(field),"Playback metadata: "+kind+" / "+field)
		check(actual.get_length()==reference.get_length(),"Exact duration: "+kind)
		check(actual==Cues.get_stream(kind),"Cached stream identity: "+kind)
	check(Cues.BAKED.size()==45,"Every authored procedural cue covered")
	print("BAKED AUDIO ","PASS" if failures==0 else "FAIL"," checks=",checks," failures=",failures," synth_usec=",synth_usec," load_usec=",loaded_usec," worst_load_usec=",worst_load)
	quit(0 if failures==0 else 1)
