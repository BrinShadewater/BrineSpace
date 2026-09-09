extends "res://scripts/restore_overlay.gd"
## Kept under the window, independent of either scene being replaced.
const TRANSMISSION := preload("res://scripts/transmission_archive.gd").OPENING
var transmission_text: String = TRANSMISSION
var replay_mode := false
var transcript: RichTextLabel
var transmission_window: Control
var continue_button: Button
var finished_reading := false


func _ready() -> void:
	layer = 110
	var sound := preload("res://scripts/station_audio.gd").new()
	sound.receiver_only = true
	add_child(sound)
	process_mode = Node.PROCESS_MODE_ALWAYS
	var backdrop := ColorRect.new()
	backdrop.color = Color("07151f")
	backdrop.theme = preload("res://scripts/title_button_style.gd").menu_theme()
	backdrop.theme.default_font.multichannel_signed_distance_field = true
	add_child(backdrop)
	backdrop.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var center := CenterContainer.new()
	backdrop.add_child(center)
	center.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var column := VBoxContainer.new()
	column.custom_minimum_size.x = 1000
	column.add_theme_constant_override("separation",24)
	center.add_child(column)
	var title := Label.new()
	title.text = "BRINE // DEEP-TIME RECEIVER"
	title.add_theme_font_size_override("font_size",30)
	title.add_theme_color_override("font_color",Color("7ac4b5"))
	column.add_child(title)
	var rule := HSeparator.new()
	column.add_child(rule)
	transmission_window = Control.new()
	transmission_window.custom_minimum_size = Vector2(1000,660)
	transmission_window.clip_contents = true
	transmission_window.mouse_filter = Control.MOUSE_FILTER_IGNORE
	column.add_child(transmission_window)
	transcript = RichTextLabel.new()
	transcript.fit_content = false
	transcript.scroll_active = true
	transcript.mouse_filter = Control.MOUSE_FILTER_STOP
	transcript.add_theme_font_size_override("normal_font_size",22)
	transcript.add_theme_color_override("default_color",Color("b9d4cf"))
	transmission_window.add_child(transcript)
	transcript.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	detail = Label.new()
	detail.text = "STATION SYSTEMS // RECOVERING"
	if replay_mode: detail.text = "ARCHIVE // RECOVERED RECORDING"
	detail.add_theme_font_size_override("font_size",17)
	detail.add_theme_color_override("font_color",Color("7ac4b5"))
	column.add_child(detail)
	continue_button = Button.new()
	continue_button.text = "RETURN TO ARCHIVE" if replay_mode else "CONTINUE"
	preload("res://scripts/title_button_style.gd").apply(continue_button,1000,56)
	continue_button.disabled = not replay_mode
	continue_button.pressed.connect(_continue)
	column.add_child(continue_button)
	preload("res://scripts/title_settings.gd").apply_menu_text(column)
	# Render the complete intro before synchronous scene setup can stall a frame.
	# It stays readable (and scrollable at larger text sizes) until acknowledged.
	transcript.text = transmission_text

func _continue() -> void:
	if continue_button.disabled or finished_reading:
		return
	finished_reading = true
	continue_button.disabled = true
	if replay_mode:
		queue_free()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		if not event.is_echo():
			_continue()
		get_viewport().set_input_as_handled()

func prepare_scene(path: String) -> PackedScene:
	# Present the opaque loading UI before any expensive load or instantiation.
	await get_tree().process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
	var error := ResourceLoader.load_threaded_request(path)
	if error != OK:
		return null
	while true:
		var state := ResourceLoader.load_threaded_get_status(path)
		if state == ResourceLoader.THREAD_LOAD_LOADED:
			detail.text = "STATION SYSTEMS // RESTORING INTERFACE"
			await get_tree().process_frame
			if DisplayServer.get_name() != "headless":
				await RenderingServer.frame_post_draw
			return ResourceLoader.load_threaded_get(path) as PackedScene
		if state != ResourceLoader.THREAD_LOAD_IN_PROGRESS:
			return null
		await get_tree().process_frame
	return null

func finish_after_scene_change() -> void:
	var tree := get_tree()
	await tree.scene_changed
	# _ready may yield while a saved crew graph is reconstructed.
	var game := tree.current_scene
	while is_instance_valid(game) and not game.get("startup_complete"):
		await tree.process_frame
	if not is_instance_valid(game):
		queue_free()
		return
	# Reading the transmission must not consume oxygen or advance the loop.
	var previous_mode: int = game.process_mode
	game.process_mode = Node.PROCESS_MODE_DISABLED
	detail.text = "STATION SYSTEMS // ONLINE. CONTINUE WHEN READY."
	continue_button.disabled = false
	while not finished_reading:
		await tree.process_frame
	# Allow deferred UI layout and a covered gameplay frame to render first.
	await tree.process_frame
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
	if is_instance_valid(game):
		game.process_mode = previous_mode
	queue_free()

