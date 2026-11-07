extends SceneTree
func _initialize() -> void: run.call_deferred()
func run() -> void:
	if DisplayServer.get_name() == "headless": quit(2); return
	if not preload("res://tests/test_synergy_geometry.gd").configure_test_window(root).get("secondary_available", false): quit(2); return
	preload("res://scripts/title_settings.gd").reduced_motion = true
	var samples := []
	var failures := 0
	for i in range(5):
		preload("res://scripts/settings_panel.gd").current_page = "DISPLAY"
		var archive := preload("res://scripts/title_archive.gd").new()
		archive.mode = "settings"
		var start := Time.get_ticks_usec()
		root.add_child(archive)
		samples.append(Time.get_ticks_usec() - start)
		var panel = archive.find_child("SettingsPanel", true, false)
		var textures := 0
		if panel.pages.has("TUTORIAL GUIDE"):
			for section in panel.pages["TUTORIAL GUIDE"].get_children().slice(3):
				for child in section.get_child(0).get_children():
					if child.get_script() == preload("res://scripts/tutorial_picture.gd") and child.preview.texture != null: textures += 1
		print("Settings sample ", i, ": ", samples[-1], " us; tutorial textures=", textures)
		if textures != 0 or panel.pages.has("TUTORIAL GUIDE"):
			failures += 1
			push_error("Unopened tutorial must not allocate its UI or screenshot textures")
		archive.free()
		await process_frame
	print("Settings cost samples (microseconds): ", samples)
	var music := root.get_node_or_null("StationMusic")
	if music != null: music.set_process(false)
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	print("Tutorial cost: %s" % ("PASS" if failures == 0 else "FAIL"))
	quit(0 if failures == 0 else 1)
