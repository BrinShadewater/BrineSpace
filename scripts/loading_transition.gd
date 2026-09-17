extends "res://scripts/restore_overlay.gd"
## Kept under the window, independent of either scene being replaced.
const TRANSMISSION := preload("res://scripts/transmission_archive.gd").OPENING
var transmission_text: String = TRANSMISSION
var replay_mode := false
var transcript: RichTextLabel
var transmission_window: Control
var continue_button: Button
var finished_reading := false
var progress: Control
# The transmission types itself out like an old terminal message sent across time before the
# station starts loading (owner playtest, Sept 17). A click, Enter or Space shows it all at once.
const TYPE_CHARACTERS_PER_SECOND := 70.0
var typing := false
var type_skipped := false


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
	progress = Control.new()
	progress.custom_minimum_size = Vector2(1000, 8)
	progress.mouse_filter = Control.MOUSE_FILTER_IGNORE
	column.add_child(progress)
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

func begin_station_build() -> void:
	detail.text = "STATION SYSTEMS // BUILDING STATION"

# Called while the station builds, from inside one long frame (ImagePrefetch forces a draw
# between image decodes). Control updates would wait for a frame that has not happened yet, so
# the bar is drawn straight into its canvas item, which the forced draw shows at once. The
# first launch has no image count to measure against, so it sweeps instead.
func show_startup_progress(fraction: float) -> void:
	if replay_mode or not is_instance_valid(progress): return
	var item := progress.get_canvas_item()
	var bar := Rect2(Vector2.ZERO, progress.size)
	RenderingServer.canvas_item_clear(item)
	RenderingServer.canvas_item_add_rect(item, bar, Color("123040"))
	if fraction >= 0.0:
		RenderingServer.canvas_item_add_rect(item, Rect2(bar.position, Vector2(bar.size.x * fraction, bar.size.y)), Color("7ac4b5"))
	else:
		var sweep := fposmod(Time.get_ticks_msec() / 1400.0, 1.0)
		RenderingServer.canvas_item_add_rect(item, Rect2(Vector2(bar.size.x * sweep * 0.8, 0), Vector2(bar.size.x * 0.2, bar.size.y)), Color("7ac4b5"))

func _continue() -> void:
	if continue_button.disabled or finished_reading:
		return
	finished_reading = true
	continue_button.disabled = true
	if replay_mode:
		queue_free()

func type_transmission() -> void:
	if replay_mode or preload("res://scripts/title_settings.gd").reduced_motion or DisplayServer.get_name() == "headless":
		transcript.visible_characters = -1
		return
	typing = true
	type_skipped = false
	detail.text = "RECEIVER // DECODING TRANSMISSION"
	transcript.visible_characters = 0
	var total := transcript.get_total_character_count()
	var shown := 0.0
	while shown < total and not type_skipped:
		await get_tree().process_frame
		shown += get_process_delta_time() * TYPE_CHARACTERS_PER_SECOND
		# Hold briefly at the end of each line, as a slow link would.
		var next := mini(int(shown), total)
		if next > transcript.visible_characters:
			var line_break: bool = transcript.get_parsed_text().substr(transcript.visible_characters, next - transcript.visible_characters).contains("\n")
			transcript.visible_characters = next
			if line_break: shown -= TYPE_CHARACTERS_PER_SECOND * 0.12
	transcript.visible_characters = -1
	typing = false
	detail.text = "STATION SYSTEMS // RECOVERING"

func _input(event: InputEvent) -> void:
	if typing and (event.is_action_pressed("ui_accept") or (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT)):
		type_skipped = true
		get_viewport().set_input_as_handled()
		return
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
	preload("res://scripts/image_prefetch.gd").end()
	if is_instance_valid(progress): RenderingServer.canvas_item_clear(progress.get_canvas_item())
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

