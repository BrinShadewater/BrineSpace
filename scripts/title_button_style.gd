extends RefCounted

# Keep keyboard traversal inside the active modal, including dynamically disabled controls.
static func contain_tab(event: InputEvent, scope: Node) -> void:
	var tab: bool = event is InputEventKey and event.pressed and event.keycode == KEY_TAB
	var directional := event.is_action_pressed("ui_up") or event.is_action_pressed("ui_down") or event.is_action_pressed("ui_left") or event.is_action_pressed("ui_right")
	if not tab and not directional:
		return
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
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Cascadia Mono", "Consolas", "Lucida Console"])
	var result := Theme.new()
	result.default_font = font
	result.default_font_size = 17
	result.set_stylebox("focus", "RichTextLabel", _flat("102b38", "86d9df", 8))
	result.set_stylebox("focus", "ScrollContainer", _flat("102b38", "86d9df", 2))
	result.set_stylebox("normal", "LineEdit", _flat("0a1c28", "416577", 14))
	result.set_stylebox("focus", "LineEdit", _flat("102b38", "86d9df", 14))
	result.set_color("font_color", "LineEdit", Color("d4edf0"))
	result.set_color("font_placeholder_color", "LineEdit", Color("8eafb9"))
	result.set_color("selection_color", "LineEdit", Color("326074"))
	result.set_stylebox("tab_selected", "TabBar", _flat("214552", "85d7dc", 16))
	result.set_stylebox("tab_unselected", "TabBar", _flat("0a1c28", "385363", 16))
	result.set_stylebox("tab_hovered", "TabBar", _flat("2b5361", "a2e9e7", 16))
	result.set_color("font_selected_color", "TabBar", Color("ddf8f4"))
	result.set_color("font_unselected_color", "TabBar", Color("9dbac5"))
	result.set_stylebox("panel", "PopupMenu", _flat("10232e", "669aa9", 12))
	result.set_stylebox("hover", "PopupMenu", _flat("2c5363", "8ed8dc", 8))
	result.set_color("font_color", "PopupMenu", Color("cbe7ec"))
	result.set_color("font_hover_color", "PopupMenu", Color("f0fffc"))
	result.set_constant("v_separation", "PopupMenu", 14)
	result.set_stylebox("background", "ProgressBar", _flat("081820", "385666", 0))
	result.set_stylebox("fill", "ProgressBar", _flat("5daab5", "8fd7d9", 0))
	for control in ["VScrollBar", "HScrollBar"]:
		result.set_stylebox("scroll", control, _flat("091923", "223c4b", 6))
		result.set_stylebox("grabber", control, _flat("3a6274", "65919f", 6))
		result.set_stylebox("grabber_highlight", control, _flat("639ca8", "abdfe0", 6))
		result.set_stylebox("grabber_pressed", control, _flat("89c8cc", "d0f5ef", 6))
	var rail := _flat("102733", "3a5c6b", 0)
	rail.content_margin_top = 3
	rail.content_margin_bottom = 3
	result.set_stylebox("slider", "HSlider", rail)
	result.set_stylebox("grabber_area", "HSlider", _flat("478896", "6cb6c0", 0))
	result.set_stylebox("grabber_area_highlight", "HSlider", _flat("6cb7bf", "bbefea", 0))
	for state in ["grabber", "grabber_highlight", "grabber_disabled"]:
		var fill := "#b9eeeb" if state == "grabber_highlight" else ("#476775" if state == "grabber_disabled" else "#6aafba")
		var handle := Image.new()
		handle.load_svg_from_string('<svg xmlns="http://www.w3.org/2000/svg" width="14" height="22"><path d="M3 1H11L13 3V19L11 21H3L1 19V3Z" fill="%s" stroke="#b8e1df"/><path d="M5 6V16M9 6V16" stroke="#163845"/></svg>' % fill)
		result.set_icon(state, "HSlider", ImageTexture.create_from_image(handle))
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

# Procedural nine-slice pressure-panel artwork; no external raster dependency.
static func panel(width: int, height: int, state: String, primary: bool = false) -> StyleBox:
	if state == "focus":
		var focus := StyleBoxFlat.new()
		focus.bg_color = Color(0, 0, 0, 0)
		focus.draw_center = false
		focus.border_color = Color("b5f3ee")
		focus.set_border_width_all(2)
		focus.expand_margin_left = 3
		focus.expand_margin_right = 3
		focus.expand_margin_top = 3
		focus.expand_margin_bottom = 3
		return focus
	var active := state == "hover"
	var pressed := state == "pressed"
	var disabled := state == "disabled"
	var edge := "#b8fff2" if active else "#617f90"
	var face := "#286078" if active else "#102c3b"
	var light := "#b2fff3" if active else ("#72d9dc" if primary else "#77a4b4")
	if pressed:
		face = "#347e89"
		edge = "#e0fff3"
		light = "#ffffff"
	if disabled:
		face = "#14242b"
		light = "#465b62"
	var svg := '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % [width, height, width, height]
	svg += '<path d="M10 1H%dL%d 10V%dL%d %dH10L1 %dV10Z" fill="#030d15" stroke="#1c3545" stroke-width="2"/>' % [width-10,width-1,height-10,width-10,height-1,height-10]
	svg += '<path d="M12 4H%dL%d 12V%dL%d %dH12L4 %dV12Z" fill="#304b5d" stroke="%s" stroke-width="2"/>' % [width-12,width-4,height-12,width-12,height-4,height-12,edge]
	svg += '<path d="M16 10H%dL%d 16V%dL%d %dH16L10 %dV16Z" fill="%s" stroke="#081923" stroke-width="2"/>' % [width-16,width-10,height-16,width-16,height-10,height-16,face]
	svg += '<path d="M20 12H%dM12 20V%d" stroke="#496779" stroke-width="2"/>' % [width-20,height-20]
	svg += '<path d="M20 %dH%dM%d 20V%d" stroke="#071722" stroke-width="3"/>' % [height-11,width-20,width-11,height-20]
	for x in [7, width-9]:
		for y in [7, height-9]:
			svg += '<rect x="%d" y="%d" width="3" height="3" fill="#acbcc2"/>' % [x,y]
	svg += '<path d="M25 6H%d" stroke="%s" stroke-width="2"/>' % [width-25,light]
	if primary:
		svg += '<path d="M24 %dL31 %dL24 %dM%d %dL%d %dL%d %d" fill="none" stroke="%s" stroke-width="2"/>' % [height/2-5,height/2,height/2+5,width-24,height/2-5,width-31,height/2,width-24,height/2+5,light]
	else:
		svg += '<path d="M18 %dH27M%d %dH%d" stroke="%s" stroke-width="2"/>' % [height-6,width-27,height-6,width-18,light]
	svg += '</svg>'
	var image := Image.new()
	image.load_svg_from_string(svg)
	var style := StyleBoxTexture.new()
	style.texture = ImageTexture.create_from_image(image)
	for side in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
		style.set_texture_margin(side, 16)
	style.content_margin_left = 24
	style.content_margin_right = 24
	style.content_margin_top = 12
	style.content_margin_bottom = 12
	return style

static func apply(button: Button, width: int, height: int, primary: bool = false) -> void:
	button.mouse_entered.connect(_tooltip_enter.bind(button))
	button.mouse_exited.connect(_tooltip_leave.bind(button))
	button.button_down.connect(_tooltip_leave.bind(button))
	button.mouse_entered.connect(func() -> void: _feedback(button, 1.08))
	button.mouse_exited.connect(func() -> void: _feedback(button, 1.04 if button.has_focus() else 1.0))
	button.focus_entered.connect(func() -> void: _feedback(button, 1.04))
	button.focus_exited.connect(func() -> void: _feedback(button, 1.08 if button.is_hovered() else 1.0))
	button.button_down.connect(func() -> void: _feedback(button, 1.15))
	button.button_up.connect(func() -> void: _feedback(button, 1.08 if button.is_hovered() else 1.0))
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		button.add_theme_stylebox_override(state, panel(width, height, state, primary))
	button.add_theme_stylebox_override("hover_pressed", panel(width, height, "pressed", primary))
	button.add_theme_color_override("font_color", Color("d3ecec"))
	button.add_theme_color_override("font_hover_color", Color("effff9"))
	button.add_theme_color_override("font_pressed_color", Color("ffffff"))
	button.add_theme_color_override("font_hover_pressed_color", Color("ffffff"))
	button.add_theme_color_override("font_disabled_color", Color("5c737d"))
	button.add_theme_color_override("font_shadow_color", Color("020c13"))
	button.add_theme_constant_override("shadow_offset_x", 1)
	button.add_theme_constant_override("shadow_offset_y", 2)

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

static func _tooltip_enter(button: Button) -> void:
	if button.tooltip_text.is_empty() or button.disabled:
		return
	var text := button.tooltip_text
	button.set_meta("menu_tooltip_text", text)
	button.tooltip_text = ""
	var ticket: int = int(button.get_meta("tooltip_ticket", 0)) + 1
	button.set_meta("tooltip_ticket", ticket)
	var weak: WeakRef = weakref(button)
	await button.get_tree().create_timer(preload("res://scripts/title_settings.gd").tooltip_delay).timeout
	if weak.get_ref() == null or not button.is_inside_tree() or not button.is_hovered() or button.disabled or button.get_meta("tooltip_ticket", 0) != ticket:
		return
	var layer := CanvasLayer.new()
	layer.layer = 100
	button.add_child(layer)
	button.set_meta("tooltip_layer", layer)
	var panel := PanelContainer.new()
	panel.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var skin := StyleBoxFlat.new()
	skin.bg_color = Color("0b202e")
	skin.border_color = Color("76b8c4")
	skin.set_border_width_all(1)
	skin.content_margin_left = 14
	skin.content_margin_right = 14
	skin.content_margin_top = 12
	skin.content_margin_bottom = 12
	panel.add_theme_stylebox_override("panel", skin)
	var label := Label.new()
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.text = text
	label.custom_minimum_size.x = 330
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", 17)
	panel.add_child(label)
	layer.add_child(panel)
	var origin := button.get_global_transform_with_canvas().origin + Vector2(0, button.size.y + 8)
	var bounds := button.get_viewport_rect().size
	panel.position = Vector2(clampf(origin.x, 12, bounds.x - panel.size.x - 12), clampf(origin.y, 12, bounds.y - panel.size.y - 12))

static func _tooltip_leave(button: Button) -> void:
	button.set_meta("tooltip_ticket", int(button.get_meta("tooltip_ticket", 0)) + 1)
	if button.has_meta("menu_tooltip_text"):
		button.tooltip_text = button.get_meta("menu_tooltip_text")
		button.remove_meta("menu_tooltip_text")
	if button.has_meta("tooltip_layer"):
		var layer = button.get_meta("tooltip_layer")
		if is_instance_valid(layer):
			layer.queue_free()
		button.remove_meta("tooltip_layer")
