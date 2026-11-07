extends SceneTree
## Interactive owner preview. Requires an explicitly isolated APPDATA and audible opt-in.
const Report = preload("res://scripts/expedition_report.gd")
const Preferences = preload("res://scripts/title_settings.gd")
const Buttons = preload("res://scripts/title_button_style.gd")
var game
var replay_button: Button

func _initialize() -> void: run.call_deferred()

func run() -> void:
	var scratch := OS.get_environment("APPDATA").replace("\\", "/")
	if not "/output/expedition-ending-preview-" in scratch or not OS.get_user_data_dir().replace("\\", "/").begins_with(scratch + "/"):
		push_error("Ending preview requires its own output/expedition-ending-preview-*/scratch-appdata"); quit(1); return
	if not OS.get_cmdline_user_args().has("--audible-preview") or DisplayServer.get_name() == "headless":
		push_error("Interactive preview requires a real display and --audible-preview"); quit(1); return
	root.title = "BrineSpace // Expedition ending preview // Temporary profile"
	root.size = Vector2i(1600, 900)
	Preferences.reduced_motion = true
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture", true)
	game.meta.save_path = "user://ending-preview.meta"
	game.run_save_path = "user://ending-preview.loop"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.minimize(); game.crew_comms.set_process(false)
	game._place_room("storage_bay", Vector2i(20,19), true)
	game._place_room("solar_array", Vector2i(19,19), true)
	game.run_discovered_synergy_ids.assign(["parts_passage", "shared_table"])
	game.run_stabilized_synergy_ids.assign(["parts_passage"])
	game.run_discovered_character_ids.assign(["josh", "margot"])
	game.meta.unlocked_companion_ids.erase("josh")
	game.meta.unlocked_companion_ids["margot"] = true
	game.cycle = 24; game.crew_count = 3
	game.resonance_score = 350; game.links_formed = 12; game.largest_cascade = 3
	game.resources.data = 135; game.meta.total_research_points = 17
	game._show_reboot_summary("Preview expedition archived. Illustrative results; your real progress is untouched.",false,true)
	# Startup is silent. Sound begins only when the owner presses Play.
	Preferences.reduced_motion = false
	var controls := CanvasLayer.new()
	controls.layer = 120
	root.add_child(controls)
	var bar := HBoxContainer.new()
	bar.theme = Buttons.menu_theme()
	controls.add_child(bar)
	bar.set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM)
	bar.offset_left = -420; bar.offset_right = 420
	bar.offset_top = -66; bar.offset_bottom = -18
	bar.add_theme_constant_override("separation", 12)
	var caption := Report.label("INTERACTIVE PREVIEW",14)
	caption.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_child(caption)
	replay_button = Button.new()
	replay_button.text = "PLAY REVEAL  [R]"
	replay_button.custom_minimum_size = Vector2(260,48)
	Buttons.apply(replay_button,260,48)
	replay_button.pressed.connect(replay)
	bar.add_child(replay_button)
	var close := Button.new()
	close.text = "CLOSE PREVIEW"
	close.custom_minimum_size = Vector2(210,48)
	Buttons.apply(close,210,48)
	close.pressed.connect(func(): preload("res://scripts/audio_shutdown.gd").request(game))
	bar.add_child(close)
	replay_button.grab_focus()
	root.grab_focus()
	print("ENDING PREVIEW READY // Click PLAY REVEAL or press R. Temporary user folder: ", OS.get_user_data_dir())
	var receipt := FileAccess.open("res://output/expedition-ending-preview-20261024/ready.json",FileAccess.WRITE)
	receipt.store_string(JSON.stringify({"pid":OS.get_process_id(),"user_dir":OS.get_user_data_dir(),"ready":true}))

func replay() -> void:
	if not is_instance_valid(game) or not game.summary_layer.visible: return
	# Clear any prior reveal tail before restarting; no reward/payment code runs here.
	for kind in ["ui_end","ui_reward_tick","ui_reward_land","ui_reward_chime"]:
		if game.station_sound.voices.has(kind):
			game.station_sound.voices[kind].player.stop()
			game.station_sound.voices[kind].player.queue_free()
			game.station_sound.voices.erase(kind)
		game.station_sound.last_event.erase(kind)
	Preferences.allow_sound_in_tests = true
	Preferences.effects_volume = 0.8; Preferences.music_volume = 0.3
	Preferences.ambience_volume = 0.25; Preferences.muted = false
	AudioServer.set_bus_mute(0,false)
	game._refresh_summary_figures(0)
	Report.populate(game,true)
	Preferences.apply_menu_text(game.summary_layer)
	game.play_station_sound("ui_end")
	Report.animate(game)
	replay_button.text = "REPLAY REVEAL  [R]"

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_R:
		replay(); root.set_input_as_handled()
