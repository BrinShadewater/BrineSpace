extends Node
## One-finger menu/text scrolling, independent of the station camera gestures.
var host: Node
var target: Control
var finger := -1
var origin := Vector2.ZERO
var previous := Vector2.ZERO
var scrolling := false
var block_mouse := false

static func install(owner: Node) -> void:
	if not preload("res://scripts/tablet_controls.gd").enabled(owner): return
	if owner.get_node_or_null("TabletTouchUI") != null: return
	var helper = load("res://scripts/tablet_touch_ui.gd").new()
	helper.name = "TabletTouchUI"; helper.host = owner
	owner.add_child(helper)

static func prepare(node: Node) -> void:
	if node is Button:
		node.custom_minimum_size = node.custom_minimum_size.max(Vector2(72,72))
		if node.get_theme_font_size("font_size") < 22: node.add_theme_font_size_override("font_size",22)
	elif node is TabBar:
		node.custom_minimum_size.y = maxf(72,node.custom_minimum_size.y)
		node.add_theme_font_size_override("font_size",22)
	elif node is Slider:
		node.custom_minimum_size.y = maxf(72,node.custom_minimum_size.y)
	elif node is LineEdit:
		node.custom_minimum_size.y = maxf(72,node.custom_minimum_size.y)
		node.add_theme_font_size_override("font_size",22)
	elif node is Label:
		if node.get_theme_font_size("font_size") < 20: node.add_theme_font_size_override("font_size",20)
	elif node is RichTextLabel:
		for font in ["normal_font_size","bold_font_size","italics_font_size"]:
			if node.get_theme_font_size(font) < 22: node.add_theme_font_size_override(font,22)
	for child in node.get_children(): prepare(child)

func _pick() -> Control:
	var hovered: Control = get_viewport().gui_get_hovered_control()
	if hovered == null or not (hovered == host or host.is_ancestor_of(hovered)): return null
	var node: Node = hovered
	while node != null and node != host.get_parent():
		# Sliders, text entry and scrollbar handles retain their native gestures.
		if node is Slider or node is LineEdit or node is TextEdit or node is ScrollBar: return null
		if node is RichTextLabel and node.scroll_active:
			var bar: VScrollBar = node.get_v_scroll_bar()
			if bar.max_value > bar.page+1: return node
		if node is ScrollContainer:
			if node.name in ["GridScroll","TouchHandScroll"]: return null
			if node.get_v_scroll_bar().max_value > node.get_v_scroll_bar().page+1 or node.get_h_scroll_bar().max_value > node.get_h_scroll_bar().page+1: return node
		node = node.get_parent()
	return null

func _input(event: InputEvent) -> void:
	if event is InputEventMouse and event.device == InputEvent.DEVICE_ID_EMULATION:
		if event is InputEventMouseButton and event.pressed:
			block_mouse = false
		if block_mouse:
			get_viewport().set_input_as_handled()
		return
	if event is InputEventScreenTouch:
		if event.pressed:
			if finger != -1: return
			target = _pick()
			if target == null: return
			finger = event.index; origin = event.position; previous = origin; scrolling = false
		elif event.index == finger:
			if scrolling and is_instance_valid(target): target.propagate_notification(Control.NOTIFICATION_SCROLL_END)
			finger = -1; target = null; scrolling = false
		else: return
		get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag and event.index == finger and is_instance_valid(target):
		if not scrolling and origin.distance_to(event.position) > 16:
			scrolling = true; block_mouse = true
			# Godot buttons cancel their held click when their scroll parent starts moving.
			target.propagate_notification(Control.NOTIFICATION_SCROLL_BEGIN)
		if scrolling:
			var delta: Vector2 = previous-event.position
			if target is ScrollContainer:
				if target.vertical_scroll_mode != ScrollContainer.SCROLL_MODE_DISABLED: target.scroll_vertical += roundi(delta.y)
				if target.horizontal_scroll_mode != ScrollContainer.SCROLL_MODE_DISABLED: target.scroll_horizontal += roundi(delta.x)
			else: target.get_v_scroll_bar().value += delta.y
		previous = event.position
		get_viewport().set_input_as_handled()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED:
		if is_instance_valid(target): target.propagate_notification(Control.NOTIFICATION_SCROLL_BEGIN)
		finger = -1; target = null; scrolling = false; block_mouse = true
