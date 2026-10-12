extends RefCounted

# Keep keyboard traversal inside the active modal, including dynamically disabled controls.
# Buttons use a subtle focus brightness change without a persistent selection outline.
# Keyboard/controller traversal remains contained within the active modal.
static var focus_style: StyleBoxFlat

static func set_keyboard_navigation(active: bool) -> void:
	_focus().border_color.a = 1.0 if active else 0.0

static func _focus() -> StyleBoxFlat:
	if focus_style == null:
		focus_style = StyleBoxFlat.new()
		focus_style.bg_color = Color(0, 0, 0, 0)
		focus_style.draw_center = false
		focus_style.border_color = Color(Color("698e89"), 0.0)
		focus_style.set_border_width_all(0)
		focus_style.expand_margin_left = 3
		focus_style.expand_margin_right = 3
		focus_style.expand_margin_top = 3
		focus_style.expand_margin_bottom = 3
	return focus_style

static func contain_tab(event: InputEvent, scope: Node) -> void:
	var tab: bool = event is InputEventKey and event.pressed and event.keycode == KEY_TAB
	var directional := event.is_action_pressed("ui_up") or event.is_action_pressed("ui_down") or event.is_action_pressed("ui_left") or event.is_action_pressed("ui_right")
	if not tab and not directional:
		return
	set_keyboard_navigation(true)
	var controls: Array[Control] = []
	_collect_focus(scope, controls)
	if controls.is_empty():
		return
	var viewport := scope.get_viewport()
	var focused := viewport.gui_get_focus_owner()
	var index := controls.find(focused)
	if directional:
		# Text entry, sliders, tabs and reading areas keep their native arrow behavior.
		if focused is LineEdit or focused is Range or focused is TabBar or focused is RichTextLabel or focused is ScrollContainer:
			return
		var direction := Vector2.LEFT if event.is_action_pressed("ui_left") else (Vector2.RIGHT if event.is_action_pressed("ui_right") else (Vector2.UP if event.is_action_pressed("ui_up") else Vector2.DOWN))
		var target: Control = focused if index >= 0 else controls[0]
		var best := INF
		if index >= 0:
			for candidate in controls:
				if candidate == focused:
					continue
				var offset := candidate.get_global_rect().get_center() - focused.get_global_rect().get_center()
				var forward := offset.dot(direction)
				if forward <= 1:
					continue
				var score := forward + absf(offset.cross(direction)) * 3.0
				if score < best:
					best = score
					target = candidate
		target.grab_focus()
		viewport.set_input_as_handled()
		return
	var step := -1 if event.shift_pressed else 1
	if index < 0:
		index = 0 if event.shift_pressed else -1
	controls[posmod(index + step, controls.size())].grab_focus()
	viewport.set_input_as_handled()

static func _collect_focus(node: Node, controls: Array[Control]) -> void:
	if node is Window:
		return
	if node is Control:
		if not node.is_visible_in_tree():
			return
		if node.focus_mode == Control.FOCUS_ALL and not (node is BaseButton and node.disabled):
			controls.append(node)
	for child in node.get_children():
		_collect_focus(child, controls)
static func menu_theme() -> Theme:
	var result := preload("res://scripts/ui_fonts.gd").apply(Theme.new(), 17)
	result.set_stylebox("focus", "RichTextLabel", _flat("102e2e", "648d88", 8))
	result.set_stylebox("focus", "ScrollContainer", _flat("102e2e", "648d88", 2))
	result.set_stylebox("normal", "LineEdit", _flat("0b2427", "596664", 14))
	result.set_stylebox("focus", "LineEdit", _flat("102e2e", "648d88", 14))
	result.set_color("font_color", "LineEdit", Color("d4edf0"))
	result.set_color("font_placeholder_color", "LineEdit", Color("8eafb9"))
	result.set_color("selection_color", "LineEdit", Color("386b69"))
	result.set_stylebox("tab_selected", "TabBar", _flat("244442", "648d88", 16))
	result.set_stylebox("tab_unselected", "TabBar", _flat("0b2427", "424e50", 16))
	result.set_stylebox("tab_hovered", "TabBar", _flat("294847", "789c96", 16))
	result.set_color("font_selected_color", "TabBar", Color("ddf8f4"))
	result.set_color("font_unselected_color", "TabBar", Color("9dbac5"))
	result.set_stylebox("panel", "PopupMenu", _flat("0b2427", "596664", 12))
	result.set_stylebox("hover", "PopupMenu", _flat("294847", "648d88", 8))
	result.set_color("font_color", "PopupMenu", Color("cbe7ec"))
	result.set_color("font_hover_color", "PopupMenu", Color("f0fffc"))
	result.set_constant("v_separation", "PopupMenu", 14)
	result.set_stylebox("background", "ProgressBar", _flat("091e21", "465556", 0))
	result.set_stylebox("fill", "ProgressBar", _flat("386b69", "4c7672", 0))
	for control in ["VScrollBar", "HScrollBar"]:
		result.set_stylebox("scroll", control, _flat("091e21", "303d3f", 6))
		result.set_stylebox("grabber", control, _flat("465f5e", "647a75", 6))
		result.set_stylebox("grabber_highlight", control, _flat("5c7670", "81938f", 6))
		result.set_stylebox("grabber_pressed", control, _flat("6b7b79", "84938f", 6))
	var rail := _flat("102e2e", "465556", 0)
	rail.content_margin_top = 3
	rail.content_margin_bottom = 3
	result.set_stylebox("slider", "HSlider", rail)
	result.set_stylebox("grabber_area", "HSlider", _flat("386b69", "4c7672", 0))
	result.set_stylebox("grabber_area_highlight", "HSlider", _flat("466f6d", "6c8c85", 0))
	for state in ["grabber", "grabber_highlight", "grabber_disabled"]:
		var fill := "#89918f" if state == "grabber_highlight" else ("#476775" if state == "grabber_disabled" else "#697573")
		var handle := Image.new()
		handle.load_svg_from_string('<svg xmlns="http://www.w3.org/2000/svg" width="14" height="22"><path d="M3 1H11L13 3V19L11 21H3L1 19V3Z" fill="%s" stroke="#929a96"/><path d="M5 6V16M9 6V16" stroke="#163845"/></svg>' % fill)
		result.set_icon(state, "HSlider", ImageTexture.create_from_image(handle))
	for kind in ["Button", "OptionButton", "MenuButton"]:
		for state in ["normal", "hover", "pressed", "disabled"]:
			result.set_stylebox(state, kind, panel(160, 38, state))
		result.set_stylebox("hover_pressed", kind, panel(160, 38, "pressed"))
		result.set_stylebox("focus", kind, _focus())
		result.set_font("font", kind, preload("res://scripts/ui_fonts.gd").interface_bold())
		result.set_color("font_color", kind, Color("dddeda"))
		result.set_color("font_disabled_color", kind, Color("99a5a2"))
		result.set_constant("icon_max_width", kind, 18)
	result.set_stylebox("panel", "PanelContainer", panel_frame())
	result.set_stylebox("panel", "TooltipPanel", _flat("0b2427", "596664", 10))
	result.set_color("font_color", "TooltipLabel", Color("dddeda"))
	var icons := preload("res://scripts/ui_icons.gd")
	for kind in ["CheckBox", "CheckButton"]:
		for key in ["checked", "checked_disabled", "on", "on_disabled"]: result.set_icon(key, kind, icons.glyph("confirm"))
		for key in ["unchecked", "unchecked_disabled", "off", "off_disabled"]: result.set_icon(key, kind, icons.glyph("frame_on"))
		result.set_icon("radio_checked", kind, icons.glyph("confirm"))
		result.set_icon("radio_unchecked", kind, icons.glyph("frame_on"))
	result.set_icon("clear", "LineEdit", icons.glyph("close"))
	preload("res://scripts/ui_widgets.gd").apply_theme(result)
	return result

static func _flat(fill: String, border: String, padding: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(fill)
	style.border_color = Color(border)
	style.set_border_width_all(1)
	style.content_margin_left = padding
	style.content_margin_right = padding
	style.content_margin_top = padding * 0.6
	style.content_margin_bottom = padding * 0.6
	return style

# Containers retain the previous understated panel chrome; hull fittings belong to buttons.
static func panel_frame() -> StyleBox:
	var style := preload("res://scripts/terminal_frame_style.gd").new()
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 6
	style.content_margin_bottom = 8
	return style

# Shared thin matte hull surface; drawing preserves rail width without texture stretching.
static func panel(_width: int, _height: int, state: String, _primary: bool = false) -> StyleBox:
	if state == "focus": return _focus()
	var skin := preload("res://scripts/ui_hull_style.gd").new()
	skin.state = state
	return skin

# A clicked button keeps focus, which left a white ring around the last thing pressed (owner
# playtest, Sept 17). The ring belongs to keyboard navigation, so a mouse press drops focus.
# A clicked button should not keep the white focus ring, but it must still register the click.
# Releasing focus on the press - even deferred - lands between press and release, and Godot cancels
# a press whose control loses focus: the button emitted button_down and button_up and never
# pressed, so clicking did nothing at all (owner report, Sept 17). The ring is hidden on the press,
# which is all that was wanted visually, and focus is only dropped once the click has resolved.
static func drop_focus_on_click(button: BaseButton) -> void:
	button.gui_input.connect(func(event: InputEvent) -> void:
		if event is InputEventMouseButton and event.pressed:
			set_keyboard_navigation(false))
	button.button_up.connect(func() -> void:
		if button.has_focus(): button.release_focus.call_deferred())

static func apply(button: Button, width: int, height: int, primary: bool = false) -> void:
	if button.has_meta("hull_styled"): return
	button.set_meta("hull_styled", true)
	button.add_theme_font_override("font", preload("res://scripts/ui_fonts.gd").interface_bold())
	var symbols := {"SETTINGS":"settings", "CLOSE":"close", "BACK":"back", "CANCEL":"cancel", "CONFIRM":"confirm", "REPAIR":"repair", "SCRAP":"scrap", "PAUSE":"pause", "RESUME":"play", "SEARCH":"search", "FILTER":"filter"}
	for caption in symbols:
		if button.text.begins_with(caption):
			preload("res://scripts/ui_icons.gd").apply(button, symbols[caption])
			break
	drop_focus_on_click(button)
	# Menu buttons stay about half their column's width instead of stretching across it (owner
	# playtest, Sept 17: settings buttons spanned ~30% of a 2560 screen). A button that asks to
	# fill keeps doing so; captions still size the button up when they need more room.
	if button.size_flags_horizontal == Control.SIZE_FILL:
		button.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		button.custom_minimum_size.x = maxf(button.custom_minimum_size.x, width * 0.55)
	button.mouse_entered.connect(_tooltip_enter.bind(button))
	button.mouse_exited.connect(_tooltip_leave.bind(button))
	button.button_down.connect(_tooltip_leave.bind(button))
	button.mouse_entered.connect(func() -> void: _feedback(button, 1.02))
	button.mouse_exited.connect(func() -> void: _feedback(button, 1.04 if button.has_focus() else 1.0))
	button.focus_entered.connect(_tooltip_enter.bind(button))
	button.focus_exited.connect(_tooltip_leave.bind(button))
	button.focus_entered.connect(func() -> void: _feedback(button, 1.04))
	button.focus_exited.connect(func() -> void: _feedback(button, 1.02 if button.is_hovered() else 1.0))
	button.button_down.connect(func() -> void: _feedback(button, 1.0))
	button.button_up.connect(func() -> void: _feedback(button, 1.02 if button.is_hovered() else 1.0))
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		button.add_theme_stylebox_override(state, panel(width, height, state, primary))
	button.add_theme_stylebox_override("hover_pressed", panel(width, height, "pressed", primary))
	button.add_theme_color_override("font_color", Color("dddeda"))
	button.add_theme_color_override("font_hover_color", Color("ecece5"))
	button.add_theme_color_override("font_pressed_color", Color("ecece5"))
	button.add_theme_color_override("font_hover_pressed_color", Color("ecece5"))
	button.add_theme_color_override("font_disabled_color", Color("99a5a2"))
	button.add_theme_color_override("font_shadow_color", Color("020c13"))
	button.add_theme_constant_override("shadow_offset_x", 1)
	button.add_theme_constant_override("shadow_offset_y", 1)

static func _feedback(button: Button, brightness: float) -> void:
	var previous: Tween = button.get_meta("feedback_tween") if button.has_meta("feedback_tween") else null
	if previous and previous.is_running():
		previous.kill()
	var tint := Color(brightness, brightness, brightness)
	if preload("res://scripts/title_settings.gd").reduced_motion or not button.is_inside_tree():
		button.self_modulate = tint
		return
	var tween := button.create_tween()
	button.set_meta("feedback_tween", tween)
	tween.tween_property(button, "self_modulate", tint, 0.10)

## Keep live hints current while the native tooltip text is temporarily suppressed.
static func set_hint(button: Button, text: String) -> void:
	if button.has_meta("menu_tooltip_text"):
		button.set_meta("menu_tooltip_text",text)
		button.tooltip_text = ""
	else:
		button.tooltip_text = text
	if button.has_meta("tooltip_layer"):
		var layer = button.get_meta("tooltip_layer")
		if is_instance_valid(layer):
			layer.get_node("HintCard/Body/HintText").text = text
			layer.get_node("HintCard/Body/Unavailable").visible = button.disabled
			_place_tooltip.call_deferred(button)

static func _tooltip_enter(button: Button) -> void:
	var text := button.tooltip_text if not button.tooltip_text.is_empty() else str(button.get_meta("menu_tooltip_text",""))
	if text.is_empty(): return
	_tooltip_leave(button)
	button.set_meta("menu_tooltip_text", text)
	button.tooltip_text = ""
	var ticket: int = int(button.get_meta("tooltip_ticket", 0)) + 1
	button.set_meta("tooltip_ticket", ticket)
	var weak: WeakRef = weakref(button)
	await button.get_tree().create_timer(preload("res://scripts/title_settings.gd").tooltip_delay).timeout
	if weak.get_ref() == null or not button.is_inside_tree() or not (button.is_hovered() or button.has_focus()) or button.get_meta("tooltip_ticket", 0) != ticket: return
	var layer := CanvasLayer.new()
	layer.name = "ControlHint"
	layer.layer = 100
	button.add_child(layer)
	button.set_meta("tooltip_layer", layer)
	var panel := PanelContainer.new()
	panel.name = "HintCard"
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_theme_stylebox_override("panel",_flat("0b2427","596664",14))
	var body := VBoxContainer.new()
	body.name = "Body"
	body.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.add_child(body)
	var heading := Label.new()
	heading.name = "Unavailable"
	heading.text = "UNAVAILABLE"
	heading.visible = button.disabled
	heading.mouse_filter = Control.MOUSE_FILTER_IGNORE
	heading.add_theme_font_override("font",preload("res://scripts/ui_fonts.gd").interface_bold())
	heading.add_theme_font_size_override("font_size",15)
	heading.add_theme_color_override("font_color",Color("b29b6d"))
	body.add_child(heading)
	var label := Label.new()
	label.name = "HintText"
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.text = str(button.get_meta("menu_tooltip_text",text))
	label.custom_minimum_size.x = minf(360,button.get_viewport_rect().size.x-52)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_override("font",preload("res://scripts/ui_fonts.gd").interface_font())
	label.add_theme_font_size_override("font_size",17)
	label.add_theme_color_override("font_color",Color("dddeda"))
	body.add_child(label)
	layer.add_child(panel)
	await button.get_tree().process_frame
	if weak.get_ref()!=null and button.get_meta("tooltip_ticket",0)==ticket: _place_tooltip(button)

static func _place_tooltip(button: Button) -> void:
	if not is_instance_valid(button): return
	if not button.has_meta("tooltip_layer"): return
	var layer = button.get_meta("tooltip_layer")
	if not is_instance_valid(layer): return
	var panel: PanelContainer = layer.get_node("HintCard")
	panel.reset_size()
	var button_origin := button.get_global_transform_with_canvas().origin
	var origin := button_origin + Vector2(0,button.size.y+8)
	var bounds := button.get_viewport_rect().size
	if origin.y+panel.size.y > bounds.y-12:
		origin.y = button_origin.y-panel.size.y-8
	panel.position = Vector2(clampf(origin.x,12,maxf(12,bounds.x-panel.size.x-12)),clampf(origin.y,12,maxf(12,bounds.y-panel.size.y-12)))

static func _tooltip_leave(button: Button) -> void:
	button.set_meta("tooltip_ticket",int(button.get_meta("tooltip_ticket",0))+1)
	if button.has_meta("menu_tooltip_text"):
		if button.tooltip_text.is_empty(): button.tooltip_text = str(button.get_meta("menu_tooltip_text"))
		button.remove_meta("menu_tooltip_text")
	if button.has_meta("tooltip_layer"):
		var layer = button.get_meta("tooltip_layer")
		if is_instance_valid(layer): layer.queue_free()
		button.remove_meta("tooltip_layer")

## Compact utility controls keep a quiet face and a visible selected state.
static func apply_plain(button: Button, active := false) -> void:
	apply(button, 160, 38)
	for state in ["normal", "hover", "pressed", "hover_pressed", "disabled", "focus"]:
		var skin := StyleBoxFlat.new()
		skin.bg_color = Color("23454b") if state in ["pressed", "hover_pressed"] or (active and state == "normal") else (Color("15343b") if state in ["hover","focus"] else Color(0,0,0,0))
		if state == "focus":
			skin.border_color = Color("81a8a2")
			skin.border_width_bottom = 2
		skin.set_corner_radius_all(4)
		skin.content_margin_left = 8
		skin.content_margin_right = 8
		skin.content_margin_top = 4
		skin.content_margin_bottom = 4
		button.add_theme_stylebox_override(state, skin)
