extends SceneTree
## Offline-only: preserve the exact procedural PCM and loop settings as import-free data.
const Cues = preload("res://scripts/station_audio_cues.gd")
func _init() -> void:
	var expected := OS.get_environment("APPDATA").replace("\\","/")
	if expected.is_empty() or not OS.get_user_data_dir().replace("\\","/").begins_with(expected+"/") or not "/output/" in expected:
		push_error("Run the baker with an isolated APPDATA under project output"); quit(1); return
	var selected := PackedStringArray()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--only="): selected = arg.trim_prefix("--only=").split(",")
	for kind in selected:
		if not Cues.BAKED.has(kind): push_error("Unknown cue: " + kind); quit(1); return
	var count := 0
	var bytes := 0
	for kind in Cues.BAKED:
		if not selected.is_empty() and kind not in selected: continue
		count += 1
		var stream := Cues.synthesize(kind)
		var path: String = Cues.BAKED[kind]
		DirAccess.make_dir_recursive_absolute(path.get_base_dir())
		var file := FileAccess.open(path,FileAccess.WRITE)
		if file == null: push_error("Cannot write " + path); quit(1); return
		file.store_string(JSON.stringify({"schema":1,"rate":stream.mix_rate,"loop_mode":stream.loop_mode,"loop_end":stream.loop_end,"pcm":Marshalls.raw_to_base64(stream.data)}))
		file.close()
		bytes += stream.data.size()
	print("BAKED PROCEDURAL AUDIO ",count," cues / ",bytes," PCM bytes")
	quit()
