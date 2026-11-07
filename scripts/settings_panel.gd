extends VBoxContainer
## Settings (owner playtest, Sept 17: a clearer design). A category sidebar on the left shows one
## page at a time on the right; each setting is a compact row with its name and hint on the left
## and a switch, list or slider on the right, and key bindings form a two-column table. Every
## settings page is built each time; the illustrated guide is built only when selected.

const Preferences = preload("res://scripts/title_settings.gd")
const Style = preload("res://scripts/title_button_style.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
signal preferences_changed
const PAGES := ["DISPLAY", "AUDIO", "CONTROLS & PAUSE", "ACCESSIBILITY", "TUTORIAL GUIDE"]
const PAGE_HINTS := {
	"DISPLAY": "Resolution, window mode and frame rate. Display changes ask you to keep or revert them.",
	"AUDIO": "Volume for music, effects and the station's ambience.",
	"CONTROLS & PAUSE": "Zoom, pausing and keyboard shortcuts. Select a key to change it; Escape cancels.",
	"ACCESSIBILITY": "Readability, motion and on-screen guides.",
	"TUTORIAL GUIDE": "Station fundamentals. The archive does not contain every answer. Some must be built.",
}
const PAGE_GLYPHS := {"DISPLAY": "▣", "AUDIO": "♪", "CONTROLS & PAUSE": "⌨", "ACCESSIBILITY": "◎", "TUTORIAL GUIDE": "?"}
const ACCENT := Color("648d88")
# Smallest interface text. At the default 1600x900 window the 1920x1080 layout is scaled by 0.83, so
# anything under this reads under about 12 px on screen.
const MIN_TEXT := 14
static var current_page := "DISPLAY"
var sections: GridContainer # Kept for callers that measure the panel; holds the page area.
var pages := {}
var tabs := {}
var feedback: Label
var display_dialog: ConfirmationDialog
var display_message: Label
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
			Preferences.resource_overlay = false
			Preferences.raised_walls = true
			Preferences.hand_backdrop = true
			Preferences.tooltip_delay = 0.5
		"DISPLAY":
			if preload("res://scripts/tablet_controls.gd").enabled(self):
				Preferences.fps_cap=0; Preferences.effects_quality=1; Preferences.auto_graphics=false
				DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)
				_commit(); _rebuild.call_deferred(); return
			# Defaults fill the screen the game is on (owner playtest: restoring used to drop a
			# fullscreen player into a small 1600x900 window).
			var window := get_window()
			var default_size := DisplayServer.screen_get_size(window.current_screen)
			var already: bool = Preferences.get_window_mode(window) == 1 and window.size == default_size and Preferences.fps_cap == 0 and Preferences.effects_quality == 1 and not Preferences.auto_graphics and DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED
			if already:
				feedback.text = "DISPLAY IS ALREADY AT ITS DEFAULTS."
				feedback.show()
				return
			_preview_display(func() -> void:
				Preferences.window_size = _fitting_size(DisplayServer.screen_get_usable_rect(window.current_screen).size)
				Preferences.apply_window_mode(window, 1, false)
				Preferences.fps_cap = 0
				Preferences.effects_quality = 1
				Preferences.auto_graphics = false
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
	display_dialog.theme.set_stylebox("panel", "AcceptDialog", Style._flat("10232e", "596664", 20))
	var border := Style._flat("10232e", "596664", 12)
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
	var confirmation := Widgets.confirmation("KEEP DISPLAY CHANGES?","Reverting in 15 seconds.","KEEP CHANGES","REVERT")
	confirmation.name = "DisplayConfirmation"
	# Native dialog buttons retain Enter/Escape and window focus handling.
	confirmation.get_node("Body/Actions").hide()
	display_message = confirmation.get_node("Body").get_child(1)
	display_dialog.add_child(confirmation)
	add_child(display_dialog)
	display_timer = Timer.new()
	display_timer.wait_time = 1.0
	display_timer.timeout.connect(func() -> void:
		if not window.has_focus() and not display_dialog.has_focus():
			_revert_display()
			return
		display_seconds -= 1
		display_dialog.dialog_text = "Keep this display configuration?\nReverting in %d seconds." % display_seconds
		display_message.text = "Reverting in %d seconds." % display_seconds
		display_dialog.get_label().hide()
		if display_seconds <= 0:
			_revert_display()
	)
	display_dialog.add_child(display_timer)
	display_dialog.dialog_text = "Keep this display configuration?\nReverting in 15 seconds."
	display_dialog.popup_centered(Vector2i(680, 230))
	display_dialog.get_label().hide()
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
	var tablet := preload("res://scripts/tablet_controls.gd").enabled(self)
	if tablet:
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED)
		if Preferences.fps_cap not in [0,30,60]: Preferences.fps_cap=0
		Engine.max_fps=Preferences.fps_cap
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_theme_constant_override("separation", 10 if preload("res://scripts/tablet_controls.gd").enabled(self) else 14)
	pages.clear()
	tabs.clear()
	var body := HBoxContainer.new()
	body.name = "SettingsBody"
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 14 if preload("res://scripts/tablet_controls.gd").enabled(self) else 22)
	add_child(body)
	var sidebar := VBoxContainer.new()
	sidebar.name = "SettingsSidebar"
	sidebar.custom_minimum_size.x = 220 if preload("res://scripts/tablet_controls.gd").enabled(self) else 260
	sidebar.add_theme_constant_override("separation", 8)
	body.add_child(sidebar)
	for page in PAGES:
		var tab := Button.new()
		tab.name = "SettingsTab" + page.replace(" ", "").replace("&", "")
		tab.text = "  %s   %s" % [("↔" if tablet and page=="CONTROLS & PAUSE" else PAGE_GLYPHS[page]), page.replace(" & PAUSE", "")]
		if tablet and page=="CONTROLS & PAUSE":
			tab.text="CONTROLS"
			preload("res://scripts/ui_icons.gd").apply(tab,"focus_room",28)
		tab.alignment = HORIZONTAL_ALIGNMENT_LEFT
		tab.toggle_mode = true
		tab.custom_minimum_size = Vector2(220 if preload("res://scripts/tablet_controls.gd").enabled(self) else 260, 52)
		tab.add_theme_font_size_override("font_size", 18)
		_style_tab(tab, page == current_page)
		tab.pressed.connect(_show_page.bind(page))
		sidebar.add_child(tab)
		tabs[page] = tab
	var saved_note := _label("Settings are remembered between sessions.", 13)
	saved_note.add_theme_color_override("font_color", Color("8aa6af"))
	saved_note.custom_minimum_size.x = 216 if preload("res://scripts/tablet_controls.gd").enabled(self) else 250
	sidebar.add_child(saved_note)
	var report := Button.new()
	report.name = "ReportBugButton"
	report.text = "REPORT A BUG" if preload("res://scripts/tablet_controls.gd").enabled(self) else "  REPORT A BUG   [F8]"
	report.alignment = HORIZONTAL_ALIGNMENT_LEFT
	report.custom_minimum_size = Vector2(220 if preload("res://scripts/tablet_controls.gd").enabled(self) else 260, 44)
	report.add_theme_font_size_override("font_size", 16)
	_style_tab(report, false)
	report.tooltip_text = "Save a bug report with your log, screenshot and last save"
	report.pressed.connect(func() -> void:
		var reporter := get_node_or_null("/root/BugReport")
		if reporter != null: reporter.open_report())
	sidebar.add_child(report)
	feedback = _label("", 14)
	feedback.add_theme_color_override("font_color", ACCENT)
	feedback.custom_minimum_size.x = 216 if preload("res://scripts/tablet_controls.gd").enabled(self) else 250
	feedback.hide()
	sidebar.add_child(feedback)
	sections = GridContainer.new()
	sections.name = "SettingsPages"
	sections.columns = 1
	sections.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_child(sections)

	var display := _page("DISPLAY")
	if not tablet:
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
	_select(display, "EffectsQuality", "Visual effects", "Lower effects can reduce heat and battery use on your iPad." if tablet else "Light shafts, caustics, drifting particles, colour grading and bloom. High adds the full grade and bloom. Lower this on slower computers.", ["Low", "Medium", "High"], Preferences.effects_quality, func(index: int) -> void:
		Preferences.effects_quality = index
		Preferences.auto_graphics = false
		_rebuild.call_deferred()
	)
	_toggle(display, "AutoGraphics", "Automatic quality" if tablet else "Auto-detect graphics", "Choose effects for this iPad. Selecting a quality manually turns this off." if tablet else "Choose visual effects for this computer now and at startup. Selecting Low, Medium or High overrides automatic detection.", Preferences.auto_graphics, func(enabled: bool) -> void:
		Preferences.auto_graphics = enabled
		if enabled: Preferences.effects_quality = Preferences.detect_graphics()
		_rebuild.call_deferred()
	)
	var cap_captions: Array[String] = []
	cap_captions.assign(["Match iPad display", "30 FPS", "60 FPS"] if tablet else ["Unlimited", "30 FPS", "60 FPS", "120 FPS", "144 FPS", "240 FPS"])
	var caps := [0, 30, 60] if tablet else [0, 30, 60, 120, 144, 240]
	_select(display, "FrameLimit", "Frame rate" if tablet else "Frame-rate limit", "30 FPS uses less power; 60 FPS gives smoother motion." if tablet else "V-sync can limit the frame rate further.", cap_captions, caps.find(Preferences.fps_cap), func(index: int) -> void:
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
	if not tablet:
		_toggle(audio, "MuteUnfocused", "Mute when unfocused", "Silences audio while another window is active.", Preferences.mute_unfocused, func(enabled: bool) -> void: Preferences.mute_unfocused = enabled)

	else:
		audio.add_child(_label("Sound follows your iPad’s Silent Mode. Turn Silent Mode off in Control Centre to hear the station.",20))

	var controls := _page("CONTROLS & PAUSE")
	if tablet:
		var guide := VBoxContainer.new(); guide.name="TouchGuide"
		guide.add_theme_constant_override("separation",12); controls.add_child(guide)
		var cards := GridContainer.new(); cards.columns=2
		cards.add_theme_constant_override("h_separation",12); cards.add_theme_constant_override("v_separation",12)
		guide.add_child(cards)
		for spec in [["row","BUILD & RETURN","Tap a blueprint, then tap the station to place it. Drag back to the hand and release to put it down."],["focus_room","MOVE & ZOOM","Pinch to zoom. Drag with two fingers to pan. Fit Station recenters the view."],["reroll","ROTATE & CANCEL","Tap the station with two fingers to rotate a selected room. Rotate and Cancel buttons are also available."],["journal","MENUS & READING","Swipe with one finger to scroll menus and text. Use Next to advance dialogue, or Close to dismiss it."]]:
			var panel:=_row_panel(); panel.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			panel.custom_minimum_size=Vector2(0,164); cards.add_child(panel)
			var box:=VBoxContainer.new(); box.add_theme_constant_override("separation",8); panel.add_child(box)
			var heading_row:=HBoxContainer.new(); box.add_child(heading_row)
			var icon:=TextureRect.new(); icon.texture=preload("res://scripts/ui_icons.gd").texture(spec[0]); icon.custom_minimum_size=Vector2(28,28)
			icon.expand_mode=TextureRect.EXPAND_IGNORE_SIZE; icon.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED; heading_row.add_child(icon)
			var heading:=_label(spec[1],22); heading.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			heading_row.add_child(heading)
			box.add_child(_label(spec[2],20))
		guide.add_child(_label("LEAVING THE APP\nAn active loop saves and pauses when you leave. After returning, tap Resume when you’re ready.",20))
	else:
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
		var help := _label("Left click: place or select.  Escape: menu or back.  Tab / Shift+Tab: move focus.  Enter: activate.", 15)
		help.add_theme_color_override("font_color", Color("8aa6af"))
		controls.add_child(help)

	var access := _page("ACCESSIBILITY")
	_toggle(access, "RaisedWalls", "Raised room walls", "Shows the tall north walls of rooms.", Preferences.raised_walls, func(enabled: bool) -> void: Preferences.raised_walls = enabled)
	_toggle(access, "PlacementGuides", "Placement door indicators", "Marks which doors will connect while placing a room.", Preferences.placement_guides, func(enabled: bool) -> void: Preferences.placement_guides = enabled)
	_toggle(access, "ResourceOverlay", "Resource overlay", "Shows what each room gives and takes over the station." if tablet else "Shows what each room gives and takes over the station. Hotkey: %s." % Preferences.key_name("Resource overlay"), Preferences.resource_overlay, func(enabled: bool) -> void: Preferences.resource_overlay = enabled)
	_toggle(access, "HandBackdrop", "Draft hand backdrop", "Off: the station view runs behind the cards.", Preferences.hand_backdrop, func(enabled: bool) -> void: Preferences.hand_backdrop = enabled)
	_toggle(access, "PixelFrames", "Pixel panel frames", "Textured pixel-art HUD frames; applies next loop.", Preferences.pixel_frames, func(enabled: bool) -> void: Preferences.pixel_frames = enabled)
	_toggle(access, "ReducedMotion", "Reduced motion", "Pauses the title cover and removes menu fades. Gameplay timing is unchanged.", Preferences.reduced_motion, func(enabled: bool) -> void: Preferences.reduced_motion = enabled)
	_slider(access, "MenuTextSize", "Menu text size", "Scales menus, journal and summaries.", 100, 130, 5, Preferences.text_scale * 100, "%", func(value: float) -> void: Preferences.text_scale = value / 100.0)
	if not tablet:
		_slider(access, "TooltipDelay", "Tooltip delay", "How long to hover before a tooltip shows.", 100, 1500, 100, Preferences.tooltip_delay * 1000, " ms", func(value: float) -> void: Preferences.tooltip_delay = value / 1000.0)
	_show_page(current_page if tabs.has(current_page) else "DISPLAY", false)
	resized.connect(_layout)
	_layout()

func _show_page(page: String, focus := true) -> void:
	current_page = page
	# The illustrated guide is optional. Build it on first use, not every time
	# someone opens Display/Audio or adjusts a setting that rebuilds the panel.
	if page == "TUTORIAL GUIDE" and not pages.has(page):
		_build_tutorial()
		Preferences.apply_menu_text(pages[page])
	for id in pages:
		pages[id].visible = id == page
		_style_tab(tabs[id], id == page)
		tabs[id].set_pressed_no_signal(id == page)
	if focus and is_instance_valid(tabs.get(page)): tabs[page].grab_focus()

func _build_tutorial() -> void:
	var guide := _page("TUTORIAL GUIDE")
	var topics := OptionButton.new()
	topics.name = "TutorialTopics"
	topics.add_item("JUMP TO A TOPIC…")
	topics.custom_minimum_size.y = 44
	topics.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	topics.fit_to_longest_item = false
	topics.clip_text = true
	topics.add_theme_font_size_override("font_size", 18)
	guide.add_child(topics)
	var targets: Array[Control] = []
	topics.item_selected.connect(func(index: int) -> void:
		if index > 0:
			_tutorial_scroll_to(targets[index - 1])
			topics.select(0)
	)
	for entry in [
		["1 // PAUSE AND TAKE STOCK", "Pause with {Pause} to inspect the station and consider your next room. Resource totals are reserves; income and consumption determine whether they will last. Open the Journal with {Journal} to revisit recorded information."],
		["2 // BUILD A WORKING CONNECTION", "Choose a blueprint from your hand and inspect its cost and placement warnings. Rotate with {Rotate blueprint}. Doors must line up, and crew need a reachable worksite to construct the room. A placed blueprint is a construction job, not an operating room. If work stalls, inspect the job and the route to it.\n\nBuilding draws a replacement blueprint. Right-click a card to reroll that card, or use Reroll Hand to replace the whole hand. Either action costs one charge from the same pool. The hand shows your remaining charges and recovery countdown; recovery advances through running cycles, not while paused."],
		["3 // KEEP ROOMS FUNCTIONING", "Read each room's inputs, outputs and operating status. Adding production can also add demand. Use the resource overlay ({Resource overlay}) to see what rooms give and take, and inspect warnings before expanding. Leave room for exterior intakes where the blueprint requires them.\n\nPower reserves act as a battery. If generation plus stored Power cannot meet demand, the station can black out for the cycle while generators recharge the reserve. Inspect the next-cycle forecast before adding demand. Suspend an optional room through its inspector to stop its production and functioning links; resuming takes effect next cycle. Master Power and Pumps switches can also explain offline rooms. BRINE’s core cannot be manually suspended."],
		["4 // CREW NEED PHYSICAL ACCESS", "Crew walk to work, repairs and rest. A nearby room is not necessarily reachable: check connected doors, obstructions and local hazards. Flooding and fire can interrupt work and threaten crew. Inspect the affected room and crew instead of assuming the job has finished.\n\nCrew also take meal breaks and rest. Keep Food available and give them reachable places to eat and rest; beds behind a blocked route do not solve an access problem. Inspect a crew member’s current activity before treating a pause in their work as a fault. A room’s Assign Primary Workplace control gives a crew member a regular job. Workplace Notes explain suitable assignments; a work bonus requires the crew member to actually attend a functioning room, not merely be assigned to it. Diving equipment does not provide unlimited air: check air supply and access to safety before sending human crew into water."],
		["5 // HAZARDS: FLOODING AND FIRE", "Pause and select the affected room when a warning appears. Hull damage lets water in; use the room inspector to assign a paid crew repair. Repairing the leak and draining the water are separate tasks: drainage needs power. Locked doors seal water routes, but also block crew access. Ordinary closed, unlocked doors can still leak. Check the crew's route before isolating a compartment.\n\nMachinery can develop heat and electrical faults. Inspect its warning and operating state. Emergency sprinklers need their switch enabled, power and Water. Fire can damage the hull and interrupt work. Keep food and oxygen available too: a station can fail without a fire. Watch station Integrity and Corruption as well. Zero Integrity or maximum Corruption ends the expedition. Read alerts and the station log for the cause; local containment faults can spread and need repair or isolation."],
		["6 // MINING AND SALVAGE", "Build and power a Mining Drone Bay to harvest surveyed deposits; a Salvage Drone Bay works scrap sites. Drones need a clear route from the bay. Cargo becomes station resources when the drone docks, not when it starts drilling. Drones return to recharge using station Power, so a quiet bay may be charging or waiting for power.\n\nSelect the bay for its status and route advice. If rock blocks the route, select it and use Break & Clear Rock with a Mining Drone Bay available. Wreck clearance uses salvage drones. Clearance and harvesting are different jobs. Deposits are finite: build outward to survey more seabed when nearby sites are exhausted."],
		["7 // FIND CREW AND COMPANIONS", "Expand your station's survey light into unexplored seabed to identify sealed compartments and recovery sites. Select a revealed site to inspect it. Building a new cryo room does not create new occupants; survivors belong to the derelict compartments you find.\n\nConnect a matching, reachable doorway, pay the listed restoration cost and let an architect complete the repairs. Repaired crew wards need power, a free berth, food and oxygen to thaw their occupants. Charging chambers need powered recharge and a free berth. Companion containers have their own open or thaw action in the inspector. Read the status when recovery waits; discovering a site is only the first step."],
		["8 // EXPERIMENT WITH PLACEMENT", "Try connecting different kinds of rooms and keep them functioning. Placement cues suggest experiments, not guaranteed recipes. Watch for a response and consult the Journal or Codex when a pattern is discovered. Three consecutive functioning cycles stabilize a pattern; an interruption breaks the streak. Specific recipes remain hidden until discovered."],
		["9 // META PROGRESSION AND ARCHIVED DATA", "Station Data is a resource used during the expedition. Archived Data is the persistent currency spent in Meta Progression. The expedition summary reports the Archived Data banked from your score and patterns. Stabilizing a pattern pays Archived Data, doubles its per-cycle bonus in later loops and halves the Archived Data price of its related blueprint. It does not automatically unlock that blueprint.\n\nOpen Meta Progression from the menu to buy upgrades, room blueprints, crew and companions. Read each upgrade's effect and prerequisites before spending: these purchases share the same Archived Data balance. Use End Expedition when you choose to finish the current loop."],
		["10 // WHAT AN UNLOCK MEANS", "Buying a room blueprint makes it available for future expedition drafts; it does not place a free room or waive normal construction costs. Learned patterns and purchased unlocks remain in your profile between loops.\n\nRecovered crew and companions join the current expedition. Recover them first to meet them, then buy their permanent unlock in Meta Progression for future loops. Merely sighting their compartment is not enough. The shop shows whether a character is unmet, owned or needs more Archived Data; characters you already own stay owned."],
		["11 // SAVE, CONTINUE OR END", "Save Game records your current expedition. Save & Return to Title and Save & Quit preserve it so you can choose Continue later; Continue restores the saved expedition paused. Check the menu’s save status before leaving.\n\nEnd Expedition finishes the current loop and banks its Archived Data. It is different from taking a break with Save & Quit. Read the expedition summary to see what was retained before starting another loop."],
		["12 // DIVING AND AIRLOCKS", "Select a Diving Airlock to choose a crew member and use its equipment and refill controls. A human diver needs a helmet, air and a reachable locker; watch the status if another job prevents service. The chamber cycles between station and ocean access. Power and a clear route matter on the return trip too.\n\nThe airlock can dispatch a crew member to mine or salvage a reachable surveyed site. Read the route or range warning before dispatching, and use Recall to bring an active expedition home. Cargo must return to the station to be delivered. Keep the return airlock available."],
		["13 // MOONBAY MISSIONS", "A built Moonbay has its own mission panel. Choose an available crew member, an order and a target, then read the launch requirements. Survey, recovery and deep-access orders serve different purposes; the panel explains the selected mission. Prepare human crew with the helmet and refill controls when needed.\n\nA mission occupies its crew and bay through departure, work and return. Watch the mission status, use Recall if needed, and let the return and unloading finish before expecting cargo. Inspect and repair a damaged bay before sending another mission."],
		["14 // SCRAPPING AND STORAGE", "Select a built room and inspect its Scrap action. Scrapping returns half the room's Metal cost, rounded down, and requires a second press to confirm. This removes the room; suspending it only stops its operation.\n\nThe game blocks scrapping when crew are inside, when other rooms or construction depend on it, when an expedition needs it to return, or when removing its storage would leave excess resources. The core, crew habitats and recovery wards stay. Read the blocker instead of assuming every room can be undone. Resource capacity also limits how much you can store; production and storage solve different problems."],
		["15 // SPECIALIZED ROOM CONTROLS", "Some advanced rooms have controls beyond Suspend. Select the room and read its inspector before activating them. Branch controls require a valid connected branch; preview which rooms are affected and keep crew clear. Isolation or deliberate flooding can interrupt production and access as well as contain a problem.\n\nOther specialized actions depend on the room’s power, supplies and operating state. Their inspector shows costs, blockers and progress. Discover the effects through play; this guide does not list hidden room combinations."],
		["WHEN SOMETHING STOPS", "Inspect the room first: is construction complete, is it functioning, are its required supplies available, and can crew reach it? Use {Fit station} to fit the station on screen and {Placement guides} to toggle placement guides. Controls & Pause lists your current bindings. Station Diagnostics helps locate interrupted rooms; the Journal keeps recorded events and discoveries. Hover resource readouts for details. If something appears broken rather than blocked by a game rule, Settings has Report a Bug (F8)."]
	]:
		var panel := _row_panel()
		panel.focus_mode = Control.FOCUS_ALL
		guide.add_child(panel)
		targets.append(panel)
		topics.add_item(entry[0])
		var body := VBoxContainer.new()
		body.add_theme_constant_override("separation", 8)
		panel.add_child(body)
		body.add_child(_label(entry[0], 20))
		var explanation := _label(entry[1], 18)
		explanation.set_meta("key_hint", entry[1])
		body.add_child(explanation)
		var back := Button.new()
		back.text = "BACK TO TOPICS"
		back.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
		Style.apply(back, 180, 36)
		back.pressed.connect(_tutorial_scroll_to.bind(topics))
		body.add_child(back)
		if preload("res://scripts/tutorial_picture.gd").EXAMPLES.has(targets.size()):
			var example := preload("res://scripts/tutorial_picture.gd").new()
			example.topic = targets.size()
			body.add_child(example)
	Preferences.apply_key_hints(guide)

func _tutorial_scroll_to(target: Control) -> void:
	target.grab_focus()
	# The shared archive follows keyboard focus. Let that scroll settle before
	# aligning the heading, or its offset is counted twice with stale geometry.
	await get_tree().process_frame
	if not is_instance_valid(target) or not is_inside_tree(): return
	var ancestor := get_parent()
	while ancestor != null:
		if ancestor is ScrollContainer:
			ancestor.scroll_vertical += roundi(target.get_global_rect().position.y - ancestor.get_global_rect().position.y)
			return
		ancestor = ancestor.get_parent()

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
	if preload("res://scripts/tablet_controls.gd").enabled(self): preload("res://scripts/tablet_touch_ui.gd").prepare(self)
	var narrow := size.x < 900 * Preferences.text_scale
	var bindings := find_child("KeyBindings", true, false) as GridContainer
	if bindings != null: bindings.columns = 1 if narrow else 2

func _page(title: String) -> VBoxContainer:
	var page := VBoxContainer.new()
	page.name = "Page" + title.replace(" ", "").replace("&", "")
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation", 6 if preload("res://scripts/tablet_controls.gd").enabled(self) else 8)
	sections.add_child(page)
	pages[title] = page
	var header := HBoxContainer.new()
	page.add_child(header)
	var heading := _label("TOUCH & PAUSE" if title=="CONTROLS & PAUSE" and preload("res://scripts/tablet_controls.gd").enabled(self) else title, 24)
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
	if title == "TUTORIAL GUIDE":
		header.remove_child(defaults)
		defaults.queue_free()
	if preload("res://scripts/tablet_controls.gd").enabled(self) and title=="CONTROLS & PAUSE": defaults.hide()
	var hints := {"DISPLAY":"Graphics quality and power use for this iPad.","AUDIO":"Station sound and your iPad volume.","CONTROLS & PAUSE":"Touch gestures and returning to your loop.","ACCESSIBILITY":"Readability, motion and on-screen guides."}
	var hint := _label(hints.get(title, PAGE_HINTS[title]) if preload("res://scripts/tablet_controls.gd").enabled(self) else PAGE_HINTS[title], 15)
	hint.add_theme_color_override("font_color", Color("7f9aa3"))
	page.add_child(hint)
	return page

func _label(text: String, font_size: int) -> Label:
	var label := Label.new()
	label.text = text
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", maxi(font_size, MIN_TEXT))
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
	box.content_margin_top = 6 if preload("res://scripts/tablet_controls.gd").enabled(self) else 10
	box.content_margin_bottom = 6 if preload("res://scripts/tablet_controls.gd").enabled(self) else 10
	panel.add_theme_stylebox_override("panel", box)
	return panel

# One setting: name and optional hint on the left, the control on the right.
func _row(parent: Control, title: String, hint: String) -> HBoxContainer:
	var panel := _row_panel()
	panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(panel)
	var line := HBoxContainer.new()
	line.add_theme_constant_override("separation", 12 if preload("res://scripts/tablet_controls.gd").enabled(self) else 18)
	panel.add_child(line)
	var text := VBoxContainer.new()
	text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	text.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	text.add_theme_constant_override("separation", 2)
	line.add_child(text)
	text.add_child(_label(title, 17))
	if not hint.is_empty():
		var small := _label(hint, 15)
		small.add_theme_color_override("font_color", Color("8aa6af"))
		text.add_child(small)
	return line

func _toggle(parent: Control, id: String, title: String, hint: String, value: bool, action: Callable) -> Button:
	var line := _row(parent, title, hint)
	var state := _label("ON" if value else "OFF", 15)
	state.autowrap_mode = TextServer.AUTOWRAP_OFF
	state.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	state.add_theme_color_override("font_color", ACCENT if value else Color("8aa6af"))
	line.add_child(state)
	var button := CheckButton.new()
	button.name = id
	button.tooltip_text = hint if not hint.is_empty() else title
	button.button_pressed = value
	button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	button.add_theme_constant_override("icon_max_width", 52)
	button.add_theme_icon_override("checked", _switch_icon(true))
	button.add_theme_icon_override("unchecked", _switch_icon(false))
	button.add_theme_icon_override("checked_mirrored", _switch_icon(true))
	button.add_theme_icon_override("unchecked_mirrored", _switch_icon(false))
	button.toggled.connect(func(enabled: bool) -> void:
		state.text = "ON" if enabled else "OFF"
		state.add_theme_color_override("font_color", ACCENT if enabled else Color("8aa6af"))
		action.call(enabled)
		_commit()
	)
	line.add_child(button)
	return button

# Clearly visible pill switches (the default dark switch disappeared when off).
static func _switch_icon(on: bool) -> Texture2D:
	return preload("res://scripts/ui_widgets.gd").switch_texture(on)

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
