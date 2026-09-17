extends VBoxContainer
## Settings (owner playtest, Sept 17: a clearer design). A category sidebar on the left shows one
## page at a time on the right; each setting is a compact row with its name and hint on the left
## and a switch, list or slider on the right, and key bindings form a two-column table. Every
## page is built each time and the others are hidden, so controls keep their names and state.

const Preferences = preload("res://scripts/title_settings.gd")
const Style = preload("res://scripts/title_button_style.gd")
signal preferences_changed
const PAGES := ["DISPLAY", "AUDIO", "CONTROLS & PAUSE", "ACCESSIBILITY"]
const PAGE_HINTS := {
	"DISPLAY": "Resolution, window mode and frame rate. Display changes ask you to keep or revert them.",
	"AUDIO": "Volume for music, effects and the station's ambience.",
	"CONTROLS & PAUSE": "Zoom, pausing and keyboard shortcuts. Select a key to change it; Escape cancels.",
	"ACCESSIBILITY": "Readability, motion and on-screen guides.",
}
const PAGE_GLYPHS := {"DISPLAY": "▣", "AUDIO": "♪", "CONTROLS & PAUSE": "⌨", "ACCESSIBILITY": "◎"}
const ACCENT := Color("5fd3c4")
static var current_page := "DISPLAY"
var sections: GridContainer # Kept for callers that measure the panel; holds the page area.
var pages := {}
var tabs := {}
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
	if event.ctrl_pressed or event.alt_pressed or event.meta_pressed or event.shift_pressed or event.keycode in [KEY_TAB, KEY_ENTER, KEY_KP_ENTER, KEY_NONE, KEY_F7, KEY_F8, KEY_F9]:
		feedback.text = "Choose a single key. F7: performance; F8: bug report; F9: Studio. Escape, Tab and Enter remain menu controls."
		feedback.show()
		preferences_changed.emit()
		return
	for action in Preferences.keys:
		if action != binding_action and int(Preferences.keys[action]) == event.keycode:
			feedback.text = "KEY IN USE // " + action.to_upper()
			feedback.show()
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
			Preferences.hand_backdrop = true
			Preferences.tooltip_delay = 0.5
		"DISPLAY":
			# Defaults fill the screen the game is on (owner playtest: restoring used to drop a
			# fullscreen player into a small 1600x900 window).
			var window := get_window()
			var default_size := DisplayServer.screen_get_size(window.current_screen)
			var already: bool = Preferences.get_window_mode(window) == 1 and window.size == default_size and Preferences.fps_cap == 0 and DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED
			if already:
				feedback.text = "DISPLAY IS ALREADY AT ITS DEFAULTS."
				feedback.show()
				return
			_preview_display(func() -> void:
				Preferences.window_size = _fitting_size(DisplayServer.screen_get_usable_rect(window.current_screen).size)
				Preferences.apply_window_mode(window, 1, false)
				Preferences.fps_cap = 0
				DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)
			)
			return
	_commit()
	_rebuild.call_deferred()

func _aspect_caption(value: Vector2i) -> String:
	var ratio := float(value.x) / float(value.y)
	if ratio > 3.2: return "  (32:9)"
	if ratio > 2.2: return "  (21:9)"
	return ""

func _fitting_size(area: Vector2i) -> Vector2i:
	var best := Vector2i(1280, 720)
	for value in [Vector2i(1600,900),Vector2i(1920,1080),Vector2i(2560,1440),Vector2i(3840,2160)]:
		if value.x <= area.x and value.y <= area.y: best = value
	return best

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
		feedback.show()
		preferences_changed.emit()
		_rebuild.call_deferred()

func _exit_tree() -> void:
	exiting = true
	_revert_display()

func _ready() -> void:
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_theme_constant_override("separation", 14)
	pages.clear()
	tabs.clear()
	var body := HBoxContainer.new()
	body.name = "SettingsBody"
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 22)
	add_child(body)
	var sidebar := VBoxContainer.new()
	sidebar.name = "SettingsSidebar"
	sidebar.custom_minimum_size.x = 260
	sidebar.add_theme_constant_override("separation", 8)
	body.add_child(sidebar)
	for page in PAGES:
		var tab := Button.new()
		tab.name = "SettingsTab" + page.replace(" ", "").replace("&", "")
		tab.text = "  %s   %s" % [PAGE_GLYPHS[page], page.replace(" & PAUSE", "")]
		tab.alignment = HORIZONTAL_ALIGNMENT_LEFT
		tab.toggle_mode = true
		tab.custom_minimum_size = Vector2(260, 52)
		tab.add_theme_font_size_override("font_size", 18)
		_style_tab(tab, page == current_page)
		tab.pressed.connect(_show_page.bind(page))
		sidebar.add_child(tab)
		tabs[page] = tab
	var saved_note := _label("Settings are remembered between sessions.", 13)
	saved_note.add_theme_color_override("font_color", Color("6f8e98"))
	saved_note.custom_minimum_size.x = 250
	sidebar.add_child(saved_note)
	feedback = _label("", 14)
	feedback.add_theme_color_override("font_color", ACCENT)
	feedback.custom_minimum_size.x = 250
	feedback.hide()
	sidebar.add_child(feedback)
	sections = GridContainer.new()
	sections.name = "SettingsPages"
	sections.columns = 1
	sections.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_child(sections)

	var display := _page("DISPLAY")
	# 16:9 plus wide and ultrawide sizes, limited to what fits the screen (owner playtest). The
	# 1920x1080 design widens to the window's aspect, so wider sizes show more station.
	var screen_area := DisplayServer.screen_get_usable_rect(get_window().current_screen).size
	var sizes: Array[Vector2i] = []
	for value in [Vector2i(1280,720),Vector2i(1600,900),Vector2i(1920,1080),Vector2i(2560,1080),Vector2i(2560,1440),Vector2i(3440,1440),Vector2i(3840,1600),Vector2i(3840,2160),Vector2i(5120,1440)]:
		if value.x <= screen_area.x and value.y <= screen_area.y: sizes.append(value)
	var fullscreen: bool = Preferences.is_fullscreen(get_window())
	var current: Vector2i = Preferences.window_size if fullscreen else get_window().size
	if not sizes.has(current):
		sizes.append(current)
	var captions: Array[String] = []
	for value in sizes:
		captions.append("%d × %d%s" % [value.x, value.y, _aspect_caption(value)])
	var screen_size := DisplayServer.screen_get_size(get_window().current_screen)
	# Choosing a size from fullscreen switches to a centred window of that size, under the same
	# keep/revert check (owner playtest: the list was greyed out in fullscreen).
	_select(display, "Resolution", "Window resolution", "Fullscreen uses the screen's own %d × %d; choosing a size switches to a window." % [screen_size.x, screen_size.y] if fullscreen else "Size of the game window.", captions, sizes.find(current), func(index: int) -> void:
		Preferences.window_size = sizes[index]
		Preferences.apply_window_mode(get_window(), 0, false)
	)
	_select(display, "WindowMode", "Window mode", "Borderless fills the screen and switches apps quickly.", ["Windowed", "Borderless Fullscreen", "Exclusive Fullscreen"], Preferences.get_window_mode(get_window()), func(index: int) -> void:
		Preferences.apply_window_mode(get_window(), index)
	)
	_toggle(display, "VSync", "V-sync", "Matches frames to your display to prevent tearing.", DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED, func(enabled: bool) -> void:
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if enabled else DisplayServer.VSYNC_DISABLED)
	)
	var caps := [0, 30, 60, 120, 144, 240]
	_select(display, "FrameLimit", "Frame-rate limit", "V-sync can limit the frame rate further.", ["Unlimited", "30 FPS", "60 FPS", "120 FPS", "144 FPS", "240 FPS"], caps.find(Preferences.fps_cap), func(index: int) -> void:
		Preferences.fps_cap = caps[index]
	)

	var audio := _page("AUDIO")
	_slider(audio, "MasterVolume", "Master volume", "", 0, 100, 1, AudioServer.get_bus_volume_linear(0) * 100, "%", func(value: float) -> void:
		AudioServer.set_bus_volume_linear(0, value / 100.0)
	)
	_toggle(audio, "MasterMute", "Mute all audio", "Silences everything without changing the volume level.", Preferences.muted, func(enabled: bool) -> void: Preferences.muted = enabled)
	_slider(audio, "MusicVolume", "Music", "", 0, 100, 1, Preferences.music_volume * 100, "%", func(value: float) -> void: Preferences.music_volume = value / 100.0)
	_slider(audio, "EffectsVolume", "Effects", "", 0, 100, 1, Preferences.effects_volume * 100, "%", func(value: float) -> void: Preferences.effects_volume = value / 100.0)
	_slider(audio, "AmbienceVolume", "Ambience", "", 0, 100, 1, Preferences.ambience_volume * 100, "%", func(value: float) -> void: Preferences.ambience_volume = value / 100.0)
	_toggle(audio, "MuteUnfocused", "Mute when unfocused", "Silences audio while another window is active.", Preferences.mute_unfocused, func(enabled: bool) -> void: Preferences.mute_unfocused = enabled)

	var controls := _page("CONTROLS & PAUSE")
	_slider(controls, "ZoomSensitivity", "Wheel zoom sensitivity", "Shift + wheel zooms the station.", 50, 200, 10, Preferences.zoom_sensitivity * 100, "%", func(value: float) -> void: Preferences.zoom_sensitivity = value / 100.0)
	_toggle(controls, "InvertZoom", "Invert wheel zoom", "Reverses the direction of Shift + wheel zoom.", Preferences.invert_zoom, func(enabled: bool) -> void: Preferences.invert_zoom = enabled)
	_toggle(controls, "PauseUnfocused", "Pause when unfocused", "Pauses a running station when the game loses focus; resume manually.", Preferences.pause_unfocused, func(enabled: bool) -> void: Preferences.pause_unfocused = enabled)
	var keys_heading := _label("KEYBOARD SHORTCUTS", 15)
	keys_heading.add_theme_color_override("font_color", Color("8fb3bd"))
	controls.add_child(keys_heading)
	var bindings := GridContainer.new()
	bindings.name = "KeyBindings"
	bindings.columns = 2
	bindings.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bindings.add_theme_constant_override("h_separation", 12)
	bindings.add_theme_constant_override("v_separation", 8)
	controls.add_child(bindings)
	for action in Preferences.DEFAULT_KEYS:
		var cell := _row_panel()
		cell.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		bindings.add_child(cell)
		var line := HBoxContainer.new()
		cell.add_child(line)
		var name_label := _label(str(action).capitalize(), 16)
		name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		name_label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		line.add_child(name_label)
		var binding := Button.new()
		binding.name = "Bind" + action.replace(" ", "")
		binding.text = Preferences.key_name(action)
		binding.tooltip_text = "Change the key for " + str(action)
		Style.apply(binding, 150, 40)
		binding.custom_minimum_size = Vector2(150, 40)
		binding.size_flags_horizontal = Control.SIZE_SHRINK_END
		binding.pressed.connect(func() -> void:
			binding_action = action
			binding_button = binding
			binding.text = "PRESS A KEY"
		)
		line.add_child(binding)
	var help := _label("Left click: place or select.  Escape: menu or back.  Tab / Shift+Tab: move focus.  Enter: activate.", 13)
	help.add_theme_color_override("font_color", Color("6f8e98"))
	controls.add_child(help)

	var access := _page("ACCESSIBILITY")
	_toggle(access, "RaisedWalls", "Raised room walls", "Shows the tall north walls of rooms.", Preferences.raised_walls, func(enabled: bool) -> void: Preferences.raised_walls = enabled)
	_toggle(access, "PlacementGuides", "Placement door indicators", "Marks which doors will connect while placing a room.", Preferences.placement_guides, func(enabled: bool) -> void: Preferences.placement_guides = enabled)
	_toggle(access, "HandBackdrop", "Draft hand backdrop", "Off: the station view runs behind the cards.", Preferences.hand_backdrop, func(enabled: bool) -> void: Preferences.hand_backdrop = enabled)
	_toggle(access, "PixelFrames", "Pixel panel frames", "Textured pixel-art HUD frames; applies next loop.", Preferences.pixel_frames, func(enabled: bool) -> void: Preferences.pixel_frames = enabled)
	_toggle(access, "ReducedMotion", "Reduced motion", "Pauses the title cover and removes menu fades. Gameplay timing is unchanged.", Preferences.reduced_motion, func(enabled: bool) -> void: Preferences.reduced_motion = enabled)
	_slider(access, "MenuTextSize", "Menu text size", "Scales menus, journal and summaries.", 100, 130, 5, Preferences.text_scale * 100, "%", func(value: float) -> void: Preferences.text_scale = value / 100.0)
	_slider(access, "TooltipDelay", "Tooltip delay", "How long to hover before a tooltip shows.", 100, 1500, 100, Preferences.tooltip_delay * 1000, " ms", func(value: float) -> void: Preferences.tooltip_delay = value / 1000.0)
	_show_page(current_page if pages.has(current_page) else "DISPLAY", false)
	resized.connect(_layout)
	_layout()

func _show_page(page: String, focus := true) -> void:
	current_page = page
	for id in pages:
		pages[id].visible = id == page
		_style_tab(tabs[id], id == page)
		tabs[id].set_pressed_no_signal(id == page)
	if focus and is_instance_valid(tabs.get(page)): tabs[page].grab_focus()

func _style_tab(tab: Button, active: bool) -> void:
	for state in ["normal", "hover", "pressed", "focus", "hover_pressed"]:
		var box := StyleBoxFlat.new()
		box.bg_color = Color("153a42") if active else (Color("10262e") if state in ["hover", "focus"] else Color("0b1a21"))
		box.border_color = ACCENT if active else (Color("3a6470") if state in ["hover", "focus"] else Color("1f3a44"))
		box.set_border_width_all(1)
		box.border_width_left = 4 if active else 1
		box.set_corner_radius_all(6)
		box.content_margin_left = 14
		tab.add_theme_stylebox_override(state, box)
	tab.add_theme_color_override("font_color", Color("e6f6f3") if active else Color("9fb8c0"))
	tab.add_theme_color_override("font_hover_color", Color("e6f6f3"))
	tab.add_theme_color_override("font_pressed_color", Color("e6f6f3"))
	tab.add_theme_color_override("font_focus_color", Color("e6f6f3"))

func _layout() -> void:
	var narrow := size.x < 900 * Preferences.text_scale
	var bindings := find_child("KeyBindings", true, false) as GridContainer
	if bindings != null: bindings.columns = 1 if narrow else 2

func _page(title: String) -> VBoxContainer:
	var page := VBoxContainer.new()
	page.name = "Page" + title.replace(" ", "").replace("&", "")
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation", 8)
	sections.add_child(page)
	pages[title] = page
	var header := HBoxContainer.new()
	page.add_child(header)
	var heading := _label(title, 24)
	heading.add_theme_color_override("font_color", Color("e6f6f3"))
	heading.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(heading)
	var defaults := Button.new()
	defaults.name = "Defaults" + title.replace(" ", "")
	defaults.text = "RESTORE DEFAULTS"
	defaults.tooltip_text = "Restore %s settings to their defaults" % title.to_lower()
	Style.apply(defaults, 220, 42)
	defaults.custom_minimum_size = Vector2(220, 42)
	defaults.size_flags_horizontal = Control.SIZE_SHRINK_END
	defaults.pressed.connect(_defaults.bind(title))
	header.add_child(defaults)
	var hint := _label(PAGE_HINTS[title], 14)
	hint.add_theme_color_override("font_color", Color("7f9aa3"))
	page.add_child(hint)
	return page

func _label(text: String, font_size: int) -> Label:
	var label := Label.new()
	label.text = text
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", Color("b9dce5"))
	return label

func _row_panel() -> PanelContainer:
	var panel := PanelContainer.new()
	var box := StyleBoxFlat.new()
	box.bg_color = Color("0c1e26")
	box.border_color = Color("1c3842")
	box.set_border_width_all(1)
	box.set_corner_radius_all(6)
	box.content_margin_left = 16
	box.content_margin_right = 14
	box.content_margin_top = 10
	box.content_margin_bottom = 10
	panel.add_theme_stylebox_override("panel", box)
	return panel

# One setting: name and optional hint on the left, the control on the right.
func _row(parent: Control, title: String, hint: String) -> HBoxContainer:
	var panel := _row_panel()
	panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(panel)
	var line := HBoxContainer.new()
	line.add_theme_constant_override("separation", 18)
	panel.add_child(line)
	var text := VBoxContainer.new()
	text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	text.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	text.add_theme_constant_override("separation", 2)
	line.add_child(text)
	text.add_child(_label(title, 17))
	if not hint.is_empty():
		var small := _label(hint, 13)
		small.add_theme_color_override("font_color", Color("6f8e98"))
		text.add_child(small)
	return line

func _toggle(parent: Control, id: String, title: String, hint: String, value: bool, action: Callable) -> Button:
	var line := _row(parent, title, hint)
	var state := _label("ON" if value else "OFF", 15)
	state.autowrap_mode = TextServer.AUTOWRAP_OFF
	state.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	state.add_theme_color_override("font_color", ACCENT if value else Color("6f8e98"))
	line.add_child(state)
	var button := CheckButton.new()
	button.name = id
	button.tooltip_text = hint if not hint.is_empty() else title
	button.button_pressed = value
	button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	button.add_theme_icon_override("checked", _switch_icon(true))
	button.add_theme_icon_override("unchecked", _switch_icon(false))
	button.add_theme_icon_override("checked_mirrored", _switch_icon(true))
	button.add_theme_icon_override("unchecked_mirrored", _switch_icon(false))
	button.toggled.connect(func(enabled: bool) -> void:
		state.text = "ON" if enabled else "OFF"
		state.add_theme_color_override("font_color", ACCENT if enabled else Color("6f8e98"))
		action.call(enabled)
		_commit()
	)
	line.add_child(button)
	return button

# Clearly visible pill switches (the default dark switch disappeared when off).
static var switch_icons := {}
static func _switch_icon(on: bool) -> Texture2D:
	if switch_icons.has(on): return switch_icons[on]
	var width := 52
	var height := 28
	var image := Image.create(width, height, false, Image.FORMAT_RGBA8)
	var track := Color("2f9c8f") if on else Color("34505a")
	var edge := Color("7fe6d6") if on else Color("6f8e98")
	var knob := Color("f2fffc") if on else Color("b8ccd2")
	var knob_center := Vector2(width - 14.0, 14.0) if on else Vector2(14.0, 14.0)
	for x in range(width):
		for y in range(height):
			var p := Vector2(x + 0.5, y + 0.5)
			var nearest := Vector2(clampf(p.x, 14.0, width - 14.0), 14.0)
			var d := p.distance_to(nearest)
			var color := Color(0, 0, 0, 0)
			if d <= 13.5: color = track
			if d > 12.0 and d <= 13.5: color = edge
			if p.distance_to(knob_center) <= 9.5: color = knob
			image.set_pixel(x, y, color)
	switch_icons[on] = ImageTexture.create_from_image(image)
	return switch_icons[on]

func _select(parent: Control, id: String, title: String, hint: String, captions: Array[String], index: int, action: Callable) -> OptionButton:
	var line := _row(parent, title, hint)
	var button := OptionButton.new()
	button.name = id
	button.add_theme_font_size_override("font_size", 16)
	for caption in captions:
		button.add_item(caption)
	button.select(maxi(0,index))
	Style.apply(button, 300, 44)
	button.custom_minimum_size = Vector2(300, 44)
	button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	button.item_selected.connect(func(selected: int) -> void:
		if id in ["Resolution", "WindowMode"]:
			_preview_display(action.bind(selected))
			return
		action.call(selected)
		_commit()
	)
	line.add_child(button)
	return button

func _slider(parent: Control, id: String, title: String, hint: String, minimum: float, maximum: float, step: float, value: float, suffix: String, action: Callable) -> void:
	var line := _row(parent, title, hint)
	var slider := HSlider.new()
	slider.name = id
	slider.min_value = minimum
	slider.max_value = maximum
	slider.step = step
	slider.value = value
	slider.custom_minimum_size = Vector2(240, 30)
	slider.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	line.add_child(slider)
	var readout := _label("%d%s" % [roundi(value), suffix], 16)
	readout.name = id + "Value"
	readout.autowrap_mode = TextServer.AUTOWRAP_OFF
	readout.custom_minimum_size.x = 64
	readout.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	readout.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	readout.add_theme_color_override("font_color", Color("91e2dd"))
	line.add_child(readout)
	slider.value_changed.connect(func(next: float) -> void:
		readout.text = "%d%s" % [roundi(next),suffix]
		action.call(next)
		_commit()
	)

func _commit() -> void:
	if not display_previous.is_empty():
		return
	Preferences.apply_runtime(get_window())
	_layout()
	var ok := Preferences.save(get_window()) == OK
	feedback.text = "SETTINGS SAVED." if ok else "SETTINGS COULD NOT BE SAVED."
	feedback.show()
	preferences_changed.emit()
