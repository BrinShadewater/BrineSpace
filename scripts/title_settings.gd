extends RefCounted
const PATH := "user://brine_settings.cfg"
static var save_path := PATH
static var initialized := false
static var window_size := Vector2i(1600, 900)
static var reduced_motion := false
static var placement_guides := true
static var raised_walls := true
static var fps_cap := 0
static var muted := false
static var music_volume := 1.0
static var effects_volume := 1.0
static var ambience_volume := 1.0
static var mute_unfocused := false
static var pause_unfocused := false
static var zoom_sensitivity := 1.0
static var invert_zoom := false
static var tooltip_delay := 0.5
static var text_scale := 1.0
static var window_focused := true
const DEFAULT_KEYS := {"Pan left": KEY_A, "Pan right": KEY_D, "Pan up": KEY_W, "Pan down": KEY_S, "Pause": KEY_SPACE, "Fit station": KEY_F, "Journal": KEY_J, "Rotate blueprint": KEY_R, "Admin view": KEY_F3, "Placement guides": KEY_V}
static var keys: Dictionary = DEFAULT_KEYS.duplicate()

static func pressed(event: InputEvent, action: String) -> bool:
	return event is InputEventKey and event.pressed and not event.echo and event.keycode == int(keys[action]) and not event.ctrl_pressed and not event.alt_pressed and not event.meta_pressed

static func key_name(action: String) -> String:
	return OS.get_keycode_string(int(keys[action]))

static func apply_key_hints(node: Node) -> void:
	if node.has_meta("key_hint"):
		var caption: String = node.get_meta("key_hint")
		for action in keys:
			caption = caption.replace("{" + action + "}", key_name(action))
		node.text = caption
	for child in node.get_children():
		apply_key_hints(child)

static func initialize(window: Window) -> void:
	if initialized:
		return
	initialized = true
	window_focused = window.has_focus()
	if not window.focus_entered.is_connected(_on_focus.bind(true)):
		window.focus_entered.connect(_on_focus.bind(true))
		window.focus_exited.connect(_on_focus.bind(false))
	var config := ConfigFile.new()
	raised_walls = true
	if config.load(save_path) != OK:
		window_size = window.size
		apply_runtime(window)
		return
	var saved_size = config.get_value("display", "size", Vector2i(1600, 900))
	keys = DEFAULT_KEYS.duplicate()
	var saved_keys = config.get_value("controls", "keys", {})
	if saved_keys is Dictionary:
		var candidate: Dictionary = DEFAULT_KEYS.duplicate()
		for action in DEFAULT_KEYS:
			candidate[action] = int(saved_keys.get(action, DEFAULT_KEYS[action]))
		var used := {}
		var valid := true
		for key in candidate.values():
			if key <= 0 or key in [KEY_ESCAPE, KEY_TAB, KEY_ENTER, KEY_KP_ENTER] or used.has(key):
				valid = false
			used[key] = true
		if valid:
			keys = candidate
	# Migrate the retired forced-low setting to the new owner-directed default.
	# A new explicit choice remains persistent after this migration.
	raised_walls = bool(config.get_value("display", "riser_walls_enabled", true))
	placement_guides = bool(config.get_value("accessibility", "placement_guides", true))
	reduced_motion = bool(config.get_value("accessibility", "reduced_motion", false))
	fps_cap = int(config.get_value("display", "fps_cap", 0))
	if fps_cap not in [0, 30, 60, 120, 144, 240]:
		fps_cap = 0
	muted = bool(config.get_value("audio", "muted", false))
	music_volume = clampf(float(config.get_value("audio", "music_volume", 1.0)), 0.0, 1.0)
	effects_volume = clampf(float(config.get_value("audio", "effects_volume", 1.0)), 0.0, 1.0)
	ambience_volume = clampf(float(config.get_value("audio", "ambience_volume", 1.0)), 0.0, 1.0)
	mute_unfocused = bool(config.get_value("audio", "mute_unfocused", false))
	pause_unfocused = bool(config.get_value("controls", "pause_unfocused", false))
	zoom_sensitivity = clampf(float(config.get_value("controls", "zoom_sensitivity", 1.0)), 0.5, 2.0)
	invert_zoom = bool(config.get_value("controls", "invert_zoom", false))
	tooltip_delay = clampf(float(config.get_value("accessibility", "tooltip_delay", 0.5)), 0.1, 1.5)
	text_scale = clampf(float(config.get_value("accessibility", "text_scale", 1.0)), 1.0, 1.3)
	if saved_size is Vector2i and saved_size.x >= 960 and saved_size.y >= 540:
		window_size = saved_size
		window.size = window_size
	var saved_mode := int(config.get_value("display", "window_mode", 1 if config.get_value("display", "fullscreen", false) else 0))
	apply_window_mode(window, saved_mode, false)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_ENABLED if config.get_value("display", "vsync", true) else DisplayServer.VSYNC_DISABLED)
	AudioServer.set_bus_volume_linear(0, clampf(float(config.get_value("audio", "volume", 1.0)), 0.0, 1.0))
	apply_runtime(window)

static func _on_focus(focused: bool) -> void:
	window_focused = focused
	AudioServer.set_bus_mute(0, muted or (mute_unfocused and not focused))

static func apply_runtime(window: Window) -> void:
	Engine.max_fps = fps_cap
	apply_key_hints(window)
	# Menu tooltips use a timer in title_button_style; the engine's built-in
	# viewport tooltip delay is fixed when the viewport is constructed.
	_on_focus(window_focused)

static func zoom_step() -> float:
	return 0.05 * zoom_sensitivity * (-1.0 if invert_zoom else 1.0)

static func apply_menu_text(node: Node) -> void:
	if node is RichTextLabel:
		for font_key in ["normal_font_size", "bold_font_size", "italics_font_size", "bold_italics_font_size", "mono_font_size"]:
			var base_key: String = "menu_base_" + font_key
			if not node.has_meta(base_key):
				node.set_meta(base_key, node.get_theme_font_size(font_key))
			node.add_theme_font_size_override(font_key, roundi(node.get_meta(base_key) * text_scale))
	if node is Label or node is Button or node is LineEdit or node is TabBar:
		if not node.has_meta("menu_base_font_size"):
			node.set_meta("menu_base_font_size", node.get_theme_font_size("font_size"))
		node.add_theme_font_size_override("font_size", roundi(node.get_meta("menu_base_font_size") * text_scale))
		if node is OptionButton:
			node.get_popup().add_theme_font_size_override("font_size", roundi(17 * text_scale))
	for child in node.get_children():
		apply_menu_text(child)

static func is_fullscreen(window: Window) -> bool:
	return get_window_mode(window) != 0

static func get_window_mode(window: Window) -> int:
	if window.borderless:
		return 1
	if window.mode == Window.MODE_EXCLUSIVE_FULLSCREEN:
		return 2
	if window.mode == Window.MODE_FULLSCREEN or window.borderless:
		return 1
	return 0

static func apply_window_mode(window: Window, value: int, remember_size := true) -> void:
	if remember_size and get_window_mode(window) == 0 and window.mode == Window.MODE_WINDOWED:
		window_size = window.size
	var screen := window.current_screen
	var screen_position := DisplayServer.screen_get_position(screen)
	var screen_size := DisplayServer.screen_get_size(screen)
	window.mode = Window.MODE_WINDOWED
	window.borderless = value == 1
	match value:
		1:
			window.position = screen_position
			window.size = screen_size
		2:
			window.mode = Window.MODE_EXCLUSIVE_FULLSCREEN
		_:
			window.size = window_size
			window.position = screen_position + Vector2i(maxi(0, int((screen_size.x - window_size.x) * 0.5)), maxi(0, int((screen_size.y - window_size.y) * 0.5)))

static func save(window: Window) -> Error:
	if window.mode == Window.MODE_WINDOWED and not is_fullscreen(window):
		window_size = window.size
	var config := ConfigFile.new()
	config.set_value("display", "size", window_size)
	config.set_value("display", "fullscreen", is_fullscreen(window))
	config.set_value("display", "window_mode", get_window_mode(window))
	config.set_value("display", "vsync", DisplayServer.window_get_vsync_mode() != DisplayServer.VSYNC_DISABLED)
	config.set_value("audio", "volume", AudioServer.get_bus_volume_linear(0))
	config.set_value("accessibility", "reduced_motion", reduced_motion)
	config.set_value("accessibility", "placement_guides", placement_guides)
	config.set_value("display", "raised_walls", raised_walls)
	config.set_value("display", "riser_walls_enabled", raised_walls)
	config.set_value("display", "fps_cap", fps_cap)
	config.set_value("audio", "muted", muted)
	config.set_value("audio", "music_volume", music_volume)
	config.set_value("audio", "effects_volume", effects_volume)
	config.set_value("audio", "ambience_volume", ambience_volume)
	config.set_value("audio", "mute_unfocused", mute_unfocused)
	config.set_value("controls", "pause_unfocused", pause_unfocused)
	config.set_value("controls", "zoom_sensitivity", zoom_sensitivity)
	config.set_value("controls", "invert_zoom", invert_zoom)
	config.set_value("controls", "keys", keys)
	config.set_value("accessibility", "tooltip_delay", tooltip_delay)
	config.set_value("accessibility", "text_scale", text_scale)
	return config.save(save_path)
