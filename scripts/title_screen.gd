extends Control

const GAME_SCENE := "res://scenes/main.tscn"
const CoverScene = preload("res://scripts/title_cover.gd")
const COVER_DURATION := 8.0
const COVER_RATIO := 1584.0 / 672.0
const ButtonStyle := preload("res://scripts/title_button_style.gd")
const RunSave := preload("res://scripts/run_save.gd")
var continue_button: Button
var settings_button: Button
var run_save_path := RunSave.PATH
const CODEX_BADGE := preload("res://brineui/title/codex-badge.svg")
const PROGRESSION_BADGE := preload("res://brineui/title/progression-badge.svg")

var cover: Control
var controls: VBoxContainer
var start_button: Button
var quit_button: Button
var status: Label
var starting := false
var meta_state = preload("res://scripts/meta_state.gd").new()
var badges: HBoxContainer
var codex_button: Button
var progression_button: Button
var archive: Control
var archive_opener: Button
var about_button: Button
var checkpoint_label: Label
var error_label: Label

func _ready() -> void:
	preload("res://scripts/title_settings.gd").initialize(get_window())
	get_window().min_size = Vector2i(960, 540)
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Cascadia Mono", "Consolas", "Lucida Console"])
	var ui_theme := Theme.new()
	ui_theme.default_font = font
	theme = ui_theme
	var background := ColorRect.new()
	background.color = Color("07151f")
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cover = CoverScene.new()
	cover.name = "LayeredCover"
	add_child(cover)
	controls = VBoxContainer.new()
	controls.size.x = 380
	controls.alignment = BoxContainer.ALIGNMENT_CENTER
	controls.add_theme_constant_override("separation", 12)
	add_child(controls)
	status = Label.new()
	status.text = "THE STATION IS QUIET. FOR NOW."
	status.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
	status.add_theme_font_size_override("font_size", 18)
	status.add_theme_color_override("font_color", Color("88aebc"))
	add_child(status)
	var awakening := Label.new()
	awakening.text = "Awaken Architect.."
	awakening.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	awakening.add_theme_font_size_override("font_size", 23)
	awakening.add_theme_color_override("font_color", Color("c3d9d8"))
	controls.add_child(awakening)
	checkpoint_label = Label.new()
	checkpoint_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	checkpoint_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	checkpoint_label.add_theme_font_size_override("font_size", 15)
	checkpoint_label.add_theme_color_override("font_color", Color("aed4dc"))
	controls.add_child(checkpoint_label)
	error_label = Label.new()
	error_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	error_label.add_theme_font_size_override("font_size", 20)
	error_label.add_theme_color_override("font_color", Color("ffd1bd"))
	add_child(error_label)
	continue_button = _button("CONTINUE LOOP", false)
	var checkpoint := RunSave.read(run_save_path)
	continue_button.visible = not checkpoint.is_empty()
	checkpoint_label.visible = continue_button.visible
	if not checkpoint.is_empty():
		checkpoint_label.text = preload("res://scripts/checkpoint_preview.gd").summary(checkpoint)
		var preview := preload("res://scripts/checkpoint_preview.gd").new()
		preview.name = "CheckpointPreview"
		preview.configure(checkpoint)
		controls.add_child(preview)
		controls.move_child(preview,checkpoint_label.get_index()+1)
		if checkpoint.has("saved_at"):
			checkpoint_label.text += "\nSAVED " + Time.get_datetime_string_from_unix_time(int(checkpoint.saved_at)).replace("T", " ") + " UTC"
		if checkpoint.get("_recovered_backup", false):
			error_label.text = "PRIMARY CHECKPOINT UNAVAILABLE. Continue will restore the backup."
	elif FileAccess.file_exists(run_save_path) or FileAccess.file_exists(run_save_path + ".bak"):
		error_label.text = "CHECKPOINT UNAVAILABLE // " + (RunSave.last_error if not RunSave.last_error.is_empty() else "The recorded loop cannot be restored.")
	continue_button.pressed.connect(_continue_loop)
	start_button = _button("NEW LOOP", true)
	start_button.tooltip_text = "Start a fresh loop. Your previous checkpoint remains until you save the new loop."
	start_button.pressed.connect(_choose_architect)
	quit_button = _button("QUIT", false)
	controls.remove_child(quit_button)
	add_child(quit_button)
	quit_button.pressed.connect(func() -> void: get_tree().quit())
	settings_button = _button("SETTINGS", false)
	controls.remove_child(settings_button)
	add_child(settings_button)
	settings_button.pressed.connect(func() -> void: _open_archive("settings", settings_button))
	about_button = _button("CREDITS / BUILD", false)
	controls.remove_child(about_button)
	add_child(about_button)
	about_button.pressed.connect(func() -> void: _open_archive("about", about_button))
	if OS.has_feature("web"):
		quit_button.hide()
	badges = HBoxContainer.new()
	badges.add_theme_constant_override("separation", 20)
	add_child(badges)
	var recovered_rooms := 0
	for entry in preload("res://scripts/codex_catalog.gd").room_entries(meta_state):
		if entry.known:
			recovered_rooms += 1
	codex_button = _badge("CODEX", "res://brineui/title/codex-badge.svg", "%d ROOMS RECOVERED" % recovered_rooms)
	codex_button.set_meta("recovered_count", recovered_rooms)
	progression_button = _badge("META PROGRESSION", "res://brineui/title/progression-badge.svg", "%d RESEARCH" % meta_state.total_research_points)
	codex_button.tooltip_text = "Recovered rooms, discovered synergies, and clues to missing signals."
	progression_button.tooltip_text = "Research, discoveries, and knowledge retained between loops."
	codex_button.pressed.connect(func() -> void: _open_archive("codex", codex_button))
	progression_button.pressed.connect(func() -> void: _open_archive("progression", progression_button))
	resized.connect(_layout)
	controls.minimum_size_changed.connect(func() -> void: _layout.call_deferred())
	_layout()
	start_button.grab_focus()
	_refresh_unread_badges()

func _button(caption: String, primary: bool) -> Button:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size = Vector2(360 if primary else 240, 66 if primary else 48)
	button.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	button.add_theme_font_size_override("font_size", 24 if primary else 17)
	button.add_theme_color_override("font_color", Color("c1f4fc"))
	ButtonStyle.apply(button, 360 if primary else 240, 66 if primary else 48, primary)
	controls.add_child(button)
	return button

func _layout() -> void:
	if not is_instance_valid(cover):
		return
	var footer_height := 360.0 if continue_button.visible else 280.0
	footer_height = maxf(footer_height, controls.get_combined_minimum_size().y + 32)
	var cover_height := minf(size.x / COVER_RATIO, maxf(1.0, size.y - footer_height))
	cover.size = Vector2(cover_height * COVER_RATIO, cover_height)
	cover.position = Vector2((size.x - cover.size.x) * 0.5, (size.y - cover_height - footer_height) * 0.5)
	var bar_top := cover.position.y + cover_height
	var center_y := (bar_top + size.y) * 0.5
	controls.size = Vector2(380, footer_height - 32)
	controls.position = Vector2((size.x - 380) * 0.5, center_y - controls.size.y * 0.5)
	status.text = "BRINE // STANDBY\nTHE STATION IS QUIET.\nFOR NOW." if not starting else status.text
	status.visible = size.x >= 1300
	var left_height := 240.0 if status.visible else 160.0
	var left_top := center_y - left_height * 0.5
	status.position = Vector2(48, left_top)
	settings_button.position = Vector2(48, left_top + (80 if status.visible else 0))
	settings_button.size = Vector2(240, 48)
	quit_button.position = settings_button.position + Vector2(0, 56)
	quit_button.size = settings_button.size
	about_button.position = quit_button.position + Vector2(0, 56)
	about_button.size = settings_button.size
	error_label.position = Vector2(48, 12)
	error_label.size = Vector2(size.x - 96, 64)
	badges.position = Vector2(size.x - 516, center_y - 92)
	badges.size = Vector2(468, 184)
	queue_redraw()

func _draw() -> void:
	if is_instance_valid(cover):
		var y := cover.position.y + cover.size.y
		draw_line(Vector2(32, y + 1), Vector2(size.x - 32, y + 1), Color("345b6c"), 2)
		for x in [40.0, size.x - 48]:
			draw_rect(Rect2(x, y + 14, 8, 8), Color("76dce6"))

func _badge(caption: String, icon_path: String, detail: String) -> Button:
	var button := Button.new()
	button.custom_minimum_size = Vector2(224, 184)
	button.tooltip_text = caption.capitalize()
	button.set_meta("label", caption)
	ButtonStyle.apply(button, 224, 184)
	badges.add_child(button)
	var box := VBoxContainer.new()
	box.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.add_theme_constant_override("separation", 5)
	button.add_child(box)
	box.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	box.offset_left = 16
	box.offset_right = -16
	box.offset_top = 16
	box.offset_bottom = -16
	box.alignment = BoxContainer.ALIGNMENT_CENTER
	var icon := TextureRect.new()
	icon.texture = CODEX_BADGE if icon_path.ends_with("codex-badge.svg") else PROGRESSION_BADGE
	icon.custom_minimum_size = Vector2(80, 80)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	box.add_child(icon)
	for text in [caption, detail]:
		var label := Label.new()
		label.text = text
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		label.add_theme_font_size_override("font_size", 17 if text == caption else 13)
		label.add_theme_color_override("font_color", Color("bde8eb") if text == caption else Color("759ca9"))
		box.add_child(label)
		if text == detail:
			button.set_meta("detail_label", label)
	return button

func _open_archive(kind: String, opener: Button) -> void:
	if starting or is_instance_valid(archive):
		return
	archive_opener = opener
	archive = preload("res://scripts/title_archive.gd").new()
	archive.meta_state = meta_state
	archive.mode = kind
	add_child(archive)
	for button in [start_button, quit_button, codex_button, progression_button, continue_button, settings_button, about_button]:
		button.disabled = true
	archive.closed.connect(func() -> void:
		archive = null
		for button in [start_button, quit_button, codex_button, progression_button, continue_button, settings_button, about_button]:
			button.disabled = false
		archive_opener.grab_focus()
		_refresh_unread_badges()
	)

func _refresh_unread_badges() -> void:
	if error_label.text.is_empty():
		if not meta_state.last_error.is_empty(): error_label.text = meta_state.last_error
		elif meta_state.recovered_backup: error_label.text = "PROGRESSION RECOVERED // Loaded the previous intact record."
	var codex_new := 0
	var mastery_new := 0
	for key in meta_state.unread_records:
		if str(key).begins_with("mastery:"):
			mastery_new += 1
		else:
			codex_new += 1
	(codex_button.get_meta("detail_label") as Label).text = "%d NEW RECORDS" % codex_new if codex_new > 0 else "%d ROOMS RECOVERED" % int(codex_button.get_meta("recovered_count", 0))
	(progression_button.get_meta("detail_label") as Label).text = "%d NEW RANKS" % mastery_new if mastery_new > 0 else "%d RESEARCH" % meta_state.total_research_points

func _choose_architect() -> void:
	if starting or is_instance_valid(archive): return
	var picker = preload("res://scripts/architect_selection.gd").new()
	picker.meta_state = meta_state
	archive = picker
	add_child(picker)
	picker.closed.connect(func():
		archive = null
		start_button.grab_focus()
	)
	picker.chosen.connect(func(_id: String):
		archive = null
		_start_game()
	)

func _continue_loop() -> void:
	if starting or is_instance_valid(archive):
		return
	RunSave.pending = RunSave.read(run_save_path)
	if RunSave.pending.is_empty():
		error_label.text = "CHECKPOINT UNAVAILABLE // " + RunSave.last_error
		return
	_start_game(true)

func _start_game(continuing := false) -> void:
	if starting or is_instance_valid(archive):
		return
	if not continuing:
		RunSave.pending = {}
	starting = true
	start_button.disabled = true
	quit_button.disabled = true
	continue_button.disabled = true
	settings_button.disabled = true
	codex_button.disabled = true
	progression_button.disabled = true
	about_button.disabled = true
	status.text = "RESTORING STATION INTERFACE..."
	var fade := ColorRect.new()
	fade.color = Color("07151f")
	fade.modulate.a = 0.0
	add_child(fade)
	fade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		await create_tween().tween_property(fade, "modulate:a", 1.0, 0.24).finished
	else:
		await get_tree().process_frame
	var error := get_tree().change_scene_to_file(GAME_SCENE)
	if error != OK:
		fade.queue_free()
		starting = false
		start_button.disabled = false
		quit_button.disabled = false
		continue_button.disabled = false
		settings_button.disabled = false
		codex_button.disabled = false
		progression_button.disabled = false
		about_button.disabled = false
		error_label.text = "INTERFACE UNAVAILABLE. RETRY."
		start_button.grab_focus()
		push_error("Could not open station scene: %s" % error)
