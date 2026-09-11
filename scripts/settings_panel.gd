extends VBoxContainer

const Preferences = preload("res://scripts/title_settings.gd")
const Style = preload("res://scripts/title_button_style.gd")
signal preferences_changed
var sections: GridContainer
var feedback: Label
var display_dialog: ConfirmationDialog
var display_previous := {}
var display_seconds := 0
var display_timer: Timer
var binding_action := ""
var binding_button: Button
var exiting := false

func _input(event: InputEvent) -> void:
	if binding_action.is_empty() or not event is InputEventKey or not event.pressed or event.echo:
		return
	get_viewport().set_input_as_handled()
	if event.keycode == KEY_ESCAPE:
		binding_action = ""
		_rebuild.call_deferred()
		return
	if event.ctrl_pressed or event.alt_pressed or event.meta_pressed or event.shift_pressed or event.keycode in [KEY_TAB, KEY_ENTER, KEY_KP_ENTER, KEY_NONE, KEY_F8]:
		feedback.text = "Choose a single key. Escape, Tab and Enter remain menu controls; F8 opens bug reports."
		preferences_changed.emit()
		return
	for action in Preferences.keys:
		if action != binding_action and int(Preferences.keys[action]) == event.keycode:
			feedback.text = "KEY IN USE // " + action.to_upper()
			preferences_changed.emit()
			return
	Preferences.keys[binding_action] = event.keycode
	binding_action = ""
	_commit()
	_rebuild.call_deferred()

func _rebuild() -> void:
	if get_viewport() == null: return # Deferred rebuild can fire after the panel leaves the tree.
	var focused := get_viewport().gui_get_focus_owner()
	var focus_name := focused.name if focused != null else StringName("")
	if resized.is_connected(_layout):
		resized.disconnect(_layout)
	for child in get_children():
		remove_child(child)
		child.queue_free()
	_ready()
	Preferences.apply_menu_text(self)
	var replacement := find_child(str(focus_name), true, false) as Control if not str(focus_name).is_empty() else null
	if replacement != null:
		replacement.grab_focus()

func _defaults(section: String) -> void:
	match section:
		"AUDIO":
			Preferences.muted = false
			Preferences.music_volume = 1.0
			Preferences.effects_volume = 1.0
			Preferences.ambience_volume = 1.0
			Preferences.mute_unfocused = false
			AudioServer.set_bus_volume_linear(0, 1.0)
		"CONTROLS & PAUSE":
			Preferences.keys = Preferences.DEFAULT_KEYS.duplicate()
			Preferences.zoom_sensitivity = 1.0
			Preferences.invert_zoom = false
			Preferences.pause_unfocused = false
		"ACCESSIBILITY":
			Preferences.text_scale = 1.0
			Preferences.reduced_motion = false
			Preferences.placement_guides = true
			Preferences.raised_walls = true
			Preferences.tooltip_delay = 0.5
		"DISPLAY":
			_preview_display(func() -> void:
				Preferences.window_size = Vector2i(1600, 900)
				Preferences.apply_window_mode(get_window(), 0, false)
				Preferences.fps_cap = 0
				DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)
			)
			return
	_commit()
	_rebuild.call_deferred()

func _preview_display(action: Callable) -> void:
	if not display_previous.is_empty():
		return
	var window := get_window()
	display_previous = {"mode": Preferences.get_window_mode(window), "size": window.size, "window_size": Preferences.window_size, "position": window.position, "screen": window.current_screen, "fps": Preferences.fps_cap, "vsync": DisplayServer.window_get_vsync_mode()}
	action.call()
	Preferences.apply_runtime(window)
	display_seconds = 15
	display_dialog = ConfirmationDialog.new()
	display_dialog.title = "DISPLAY CHECK"
	display_dialog.ok_button_text = "Keep Changes"
	display_dialog.cancel_button_text = "Revert"
	display_dialog.exclusive = true
	display_dialog.dialog_close_on_escape = true
	display_dialog.theme = Style.menu_theme()
	display_dialog.theme.set_stylebox("panel", "AcceptDialog", Style._flat("10232e", "76b8c4", 20))
	var border := Style._flat("10232e", "76b8c4", 12)
	border.expand_margin_top = 32
	display_dialog.theme.set_stylebox("embedded_border", "Window", border)
	display_dialog.theme.set_font_size("title_font_size", "Window", 20)
	display_dialog.get_label().add_theme_font_size_override("font_size", 22)
	Style.apply(display_dialog.get_ok_button(), 230, 52, true)
	Style.apply(display_dialog.get_cancel_button(), 230, 52)
	for button in [display_dialog.get_ok_button(), display_dialog.get_cancel_button()]:
		button.custom_minimum_size = Vector2(230, 52)
		button.add_theme_font_size_override("font_size", 20)
	display_dialog.confirmed.connect(_keep_display)
	display_dialog.canceled.connect(_revert_display)
	add_child(display_dialog)
	display_timer = Timer.new()
	display_timer.wait_time = 1.0
	display_timer.timeout.connect(func() -> void:
		if not window.has_focus() and not display_dialog.has_focus():
			_revert_display()
			return
		display_seconds -= 1
		display_dialog.dialog_text = "Keep this display configuration?\nReverting in %d seconds." % display_seconds
		if display_seconds <= 0:
			_revert_display()
	)
	display_dialog.add_child(display_timer)
	display_dialog.dialog_text = "Keep this display configuration?\nReverting in 15 seconds."
	display_dialog.popup_centered(Vector2i(680, 230))
	display_timer.start()
	display_dialog.get_cancel_button().grab_focus()

func _keep_display() -> void:
	display_previous.clear()
	display_timer.stop()
	display_dialog.hide()
	_commit()
	_rebuild.call_deferred()

func _revert_display() -> void:
	if display_previous.is_empty():
		return
	var window := get_window()
	Preferences.window_size = display_previous.window_size
	window.current_screen = display_previous.screen
	Preferences.apply_window_mode(window, display_previous.mode, false)
	if display_previous.mode == 0:
		window.size = display_previous.size
		window.position = display_previous.position
	Preferences.fps_cap = display_previous.fps
	DisplayServer.window_set_vsync_mode(display_previous.vsync)
	Preferences.apply_runtime(window)
	display_previous.clear()
	if is_instance_valid(display_timer):
		display_timer.stop()
	if is_instance_valid(display_dialog):
		display_dialog.hide()
	if is_inside_tree() and not exiting:
		feedback.text = "DISPLAY RESTORED."
		preferences_changed.emit()
		_rebuild.call_deferred()

func _exit_tree() -> void:
	exiting = true
	_revert_display()

func _ready() -> void:
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_theme_constant_override("separation", 18)
	add_child(_label("Settings are remembered between sessions. Display changes require confirmation; other changes apply immediately.", 17))
	sections = GridContainer.new()
	sections.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sections.add_theme_constant_override("h_separation", 20)
	sections.add_theme_constant_override("v_separation", 20)
	add_child(sections)
	feedback = _label("", 16)
	feedback.hide()
	var display := _section("DISPLAY")
	var sizes: Array[Vector2i] = [Vector2i(1280,720),Vector2i(1600,900),Vector2i(1920,1080),Vector2i(2560,1440)]
	var current: Vector2i = Preferences.window_size if Preferences.is_fullscreen(get_window()) else get_window().size
	if not sizes.has(current):
		sizes.append(current)
	var captions: Array[String] = []
	for value in sizes:
		captions.append("%d × %d" % [value.x, value.y])
	var resolution := _select(display, "Resolution", "Window resolution", captions, sizes.find(current), func(index: int) -> void:
		get_window().size = sizes[index]
		Preferences.window_size = sizes[index]
	)
	resolution.disabled = Preferences.is_fullscreen(get_window())
	_select(display, "WindowMode", "Window mode", ["Windowed", "Borderless Fullscreen", "Exclusive Fullscreen"], Preferences.get_window_mode(get_window()), func(index: int) -> void:
		Preferences.apply_window_mode(get_window(), index)
		resolution.disabled = index != 0
	)
	_toggle(display, "VSync", "V-sync", DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED, func(enabled: bool) -> void:
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if enabled else DisplayServer.VSYNC_DISABLED)
	)
	var caps := [0, 30, 60, 120, 144, 240]
	_select(display, "FrameLimit", "Frame-rate limit", ["Unlimited", "30 FPS", "60 FPS", "120 FPS", "144 FPS", "240 FPS"], caps.find(Preferences.fps_cap), func(index: int) -> void:
		Preferences.fps_cap = caps[index]
	)
	display.add_child(_label("V-sync can limit the frame rate further to match your display.", 15))
	var audio := _section("AUDIO")
	_slider(audio, "MasterVolume", "Master volume", 0, 100, 1, AudioServer.get_bus_volume_linear(0) * 100, "%", func(value: float) -> void:
		AudioServer.set_bus_volume_linear(0, value / 100.0)
	)
	_toggle(audio, "MasterMute", "Mute all audio", Preferences.muted, func(enabled: bool) -> void: Preferences.muted = enabled)
	_slider(audio, "MusicVolume", "Music volume", 0, 100, 1, Preferences.music_volume * 100, "%", func(value: float) -> void: Preferences.music_volume = value / 100.0)
	_slider(audio, "EffectsVolume", "Effects volume", 0, 100, 1, Preferences.effects_volume * 100, "%", func(value: float) -> void: Preferences.effects_volume = value / 100.0)
	_slider(audio, "AmbienceVolume", "Ambience volume", 0, 100, 1, Preferences.ambience_volume * 100, "%", func(value: float) -> void: Preferences.ambience_volume = value / 100.0)
	_toggle(audio, "MuteUnfocused", "Mute when unfocused", Preferences.mute_unfocused, func(enabled: bool) -> void: Preferences.mute_unfocused = enabled)
	audio.add_child(_label("Muting preserves the volume level. Background muting ends when you return to the game.", 15))
	var controls := _section("CONTROLS & PAUSE")
	_slider(controls, "ZoomSensitivity", "Wheel zoom sensitivity", 50, 200, 10, Preferences.zoom_sensitivity * 100, "%", func(value: float) -> void: Preferences.zoom_sensitivity = value / 100.0)
	_toggle(controls, "InvertZoom", "Invert wheel zoom", Preferences.invert_zoom, func(enabled: bool) -> void: Preferences.invert_zoom = enabled)
	_toggle(controls, "PauseUnfocused", "Pause when unfocused", Preferences.pause_unfocused, func(enabled: bool) -> void: Preferences.pause_unfocused = enabled)
	controls.add_child(_label("Shift + wheel: zoom. Left click: place/select. Escape: menu/back. Tab / Shift+Tab: menu focus. Enter: activate.\nFocus-loss pausing stays paused until you resume. Select an action below to change its key; Escape cancels.", 15))
	for action in Preferences.DEFAULT_KEYS:
		var binding := Button.new()
		binding.name = "Bind" + action.replace(" ", "")
		binding.text = action.to_upper() + "  [" + Preferences.key_name(action) + "]"
		Style.apply(binding, 380, 48)
		binding.pressed.connect(func() -> void:
			binding_action = action
			binding_button = binding
			binding.text = "PRESS A KEY  [ESC TO CANCEL]"
		)
		controls.add_child(binding)
	var access := _section("ACCESSIBILITY")
	_toggle(access, "RaisedWalls", "Raised room walls", Preferences.raised_walls, func(enabled: bool) -> void: Preferences.raised_walls = enabled)
	_toggle(access, "PlacementGuides", "Placement door indicators", Preferences.placement_guides, func(enabled: bool) -> void: Preferences.placement_guides = enabled)
	_toggle(access, "ReducedMotion", "Reduced motion", Preferences.reduced_motion, func(enabled: bool) -> void: Preferences.reduced_motion = enabled)
	access.add_child(_label("Pauses the title cover and removes menu fades. Gameplay timing is unchanged.", 15))
	_slider(access, "MenuTextSize", "Menu panel text size", 100, 130, 5, Preferences.text_scale * 100, "%", func(value: float) -> void: Preferences.text_scale = value / 100.0)
	access.add_child(_label("Scales menu panels, doctrine choices, journal and run summaries. Title artwork and station HUD retain their designed size.", 15))
	_slider(access, "TooltipDelay", "Menu tooltip delay", 100, 1500, 100, Preferences.tooltip_delay * 1000, " ms", func(value: float) -> void: Preferences.tooltip_delay = value / 1000.0)
	add_child(feedback)
	resized.connect(_layout)
	_layout()

func _layout() -> void:
	sections.columns = 2 if size.x >= 980 * Preferences.text_scale else 1

func _section(title: String) -> VBoxContainer:
	var panel := PanelContainer.new()
	panel.custom_minimum_size.x = 420
	panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var skin := StyleBoxFlat.new()
	skin.bg_color = Color("0b1d28")
	skin.border_color = Color("345969")
	skin.set_border_width_all(1)
	skin.content_margin_left = 22
	skin.content_margin_right = 22
	skin.content_margin_top = 20
	skin.content_margin_bottom = 20
	panel.add_theme_stylebox_override("panel", skin)
	sections.add_child(panel)
	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	box.add_theme_constant_override("separation", 14)
	panel.add_child(box)
	box.add_child(_label(title, 22))
	var defaults := Button.new()
	defaults.name = "Defaults" + title.replace(" ", "")
	defaults.text = "RESTORE " + title + " DEFAULTS"
	Style.apply(defaults, 380, 48)
	defaults.pressed.connect(_defaults.bind(title))
	box.add_child(defaults)
	return box

func _label(text: String, font_size: int) -> Label:
	var label := Label.new()
	label.text = text
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", Color("b9dce5"))
	return label

func _toggle(parent: Control, id: String, title: String, value: bool, action: Callable) -> Button:
	var button := Button.new()
	button.name = id
	button.tooltip_text = {
		"MasterMute": "Silences every audio source without changing the volume level.",
		"MuteUnfocused": "Silences audio while another window is active.",
		"PauseUnfocused": "Pauses a running station when the game loses focus. Resume manually when you return.",
		"InvertZoom": "Reverses the direction of Shift + mouse-wheel zoom.",
		"ReducedMotion": "Freezes ambient cover motion and removes menu fades."
	}.get(id, title)
	button.toggle_mode = true
	button.button_pressed = value
	button.text = title.to_upper() + (": ON" if value else ": OFF")
	button.custom_minimum_size.y = 52
	button.add_theme_font_size_override("font_size", 17)
	Style.apply(button, 380, 52)
	button.toggled.connect(func(enabled: bool) -> void:
		button.text = title.to_upper() + (": ON" if enabled else ": OFF")
		action.call(enabled)
		_commit()
	)
	parent.add_child(button)
	return button

func _select(parent: Control, id: String, title: String, captions: Array[String], index: int, action: Callable) -> OptionButton:
	parent.add_child(_label(title.to_upper(), 17))
	var button := OptionButton.new()
	button.name = id
	button.custom_minimum_size.y = 52
	button.add_theme_font_size_override("font_size", 17)
	for caption in captions:
		button.add_item(caption)
	button.select(maxi(0,index))
	Style.apply(button, 380, 52)
	button.item_selected.connect(func(selected: int) -> void:
		if id in ["Resolution", "WindowMode"]:
			_preview_display(action.bind(selected))
			return
		action.call(selected)
		_commit()
	)
	parent.add_child(button)
	return button

func _slider(parent: Control, id: String, title: String, minimum: float, maximum: float, step: float, value: float, suffix: String, action: Callable) -> void:
	var heading := HBoxContainer.new()
	parent.add_child(heading)
	var label := _label(title.to_upper(), 17)
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	heading.add_child(label)
	var readout := _label("%d%s" % [roundi(value), suffix], 17)
	readout.name = id + "Value"
	readout.autowrap_mode = TextServer.AUTOWRAP_OFF
	readout.add_theme_color_override("font_color", Color("91e2dd"))
	heading.add_child(readout)
	var slider := HSlider.new()
	slider.name = id
	slider.min_value = minimum
	slider.max_value = maximum
	slider.step = step
	slider.value = value
	slider.custom_minimum_size.y = 36
	slider.value_changed.connect(func(next: float) -> void:
		readout.text = "%d%s" % [roundi(next),suffix]
		action.call(next)
		_commit()
	)
	parent.add_child(slider)

func _commit() -> void:
	if not display_previous.is_empty():
		return
	Preferences.apply_runtime(get_window())
	_layout()
	feedback.text = "SETTINGS RECORDED." if Preferences.save(get_window()) == OK else "SETTINGS COULD NOT BE SAVED."
	preferences_changed.emit()
