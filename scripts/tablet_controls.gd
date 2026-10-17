extends Node
## iPad-only camera arbitration. A map tap commits on release so the first
## finger of a pinch cannot accidentally spend a blueprint.
const CARD_SCALE := 1.5
const TAP_SLOP := 20.0
var game
var fingers := {}
var map_sequence := false
var suppress_mouse := false
var multiple := false
var moved := false
var press_at := Vector2.ZERO
var previous_center := Vector2.ZERO
var previous_span := 0.0
var scroll_position := Vector2.ZERO
var pair_tap := false
var pair_origins := {}
var pair_started := 0
var pair_card := ""

static func enabled(node: Node) -> bool:
	return OS.has_feature("ios") or bool(node.get_meta("tablet_controls", false)) or (node.is_inside_tree() and bool(node.get_tree().root.get_meta("tablet_controls",false)))

func _ready() -> void:
	name = "TabletControls"
	configure_layout()

func configure_layout() -> void:
	preload("res://scripts/tablet_touch_ui.gd").install(game)
	var dock: Control = game.get_node("Root/SideDock")
	dock.offset_left = -608
	game.get_node("Root/SideDock/SideScroll").custom_minimum_size.x = 600
	game.get_node("Root/SideDock/SideScroll/SidePanel").custom_minimum_size.x = 578
	game.station_center.offset_right = -620
	game.hand_panel.offset_right = -620
	var controls: Node = game.get_node("Root/SideDock/ControlsPanel/ControlsBox")
	var actions := HBoxContainer.new()
	actions.name = "TouchActions"
	actions.add_theme_constant_override("separation", 12)
	controls.add_child(actions)
	for spec in [["TouchRotate", "ROTATE", game._rotate_selected_room], ["TouchCancel", "CANCEL", cancel_blueprint]]:
		var button := Button.new()
		button.name = spec[0]; button.text = spec[1]
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		game._style_hud_button(button)
		button.pressed.connect(spec[2])
		actions.add_child(button)
	var fit: Button = game.find_child("RecenterButton",true,false)
	var camera := HBoxContainer.new()
	camera.name = "TouchCamera"
	camera.add_theme_constant_override("separation",12)
	controls.add_child(camera)
	for direction in [-1,1]:
		var zoom := Button.new()
		zoom.name = "TouchZoomOut" if direction < 0 else "TouchZoomIn"
		zoom.text = "−" if direction < 0 else "+"
		zoom.custom_minimum_size = Vector2(100,72)
		zoom.pressed.connect(func(): game._request_grid_zoom(game.grid_zoom+direction*game.Preferences.zoom_step()))
		camera.add_child(zoom)
	fit.reparent(camera)
	camera.move_child(fit,1)
	fit.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	var reroll := Button.new()
	reroll.name = "TouchReroll"
	reroll.text = "REROLL CARD"
	reroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	reroll.pressed.connect(game._discard_selected_card)
	actions.add_child(reroll)
	fit.remove_meta("key_hint")
	fit.text = "FIT STATION"
	fit.custom_minimum_size.x = 170
	game.zoom_slider.custom_minimum_size.y = 72
	var row: HBoxContainer = game.hand_panel.get_child(0)
	var status: VBoxContainer = row.get_child(0)
	# Keep the five hand actions compact enough for the 50% larger cards.
	for label in game.hand_chrome: label.hide()
	game.hand_chrome.clear()
	var scroll := ScrollContainer.new()
	scroll.name = "TouchHandScroll"
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
	scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	row.add_child(scroll)
	game.hand_box.reparent(scroll)
	game.hand_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	game.hand_box.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	status.add_theme_constant_override("separation", 12)
	game.hand_backdrop_shown = -1
	game._apply_hand_backdrop()
	# Keep hardware and time reachable; only the Inspector/guide region scrolls.
	game.get_node("Root/SideDock/SideScroll/SidePanel").size_flags_vertical = Control.SIZE_EXPAND_FILL
	game.find_child("PreviewPanel",true,false).size_flags_vertical = Control.SIZE_EXPAND_FILL
	game.hardware_panel.reparent(dock)
	dock.move_child(game.hardware_panel,1)
	for overlay in [game.journal_layer,game.menu_center,game.summary_layer]:
		preload("res://scripts/tablet_touch_ui.gd").prepare(overlay)
	refresh_targets()
	game.get_node("Root").resized.connect(_fit_layout)
	_fit_layout.call_deferred()

func _fit_layout() -> void:
	if not is_instance_valid(game) or not game.is_inside_tree(): return
	var root: Control = game.get_node("Root")
	var safe := Rect2(Vector2.ZERO,root.size)
	if OS.has_feature("ios"):
		var pixels := Rect2(DisplayServer.get_display_safe_area())
		var inverse: Transform2D = game.get_viewport().get_final_transform().affine_inverse()
		safe = safe.intersection(Rect2(inverse*pixels.position,inverse.basis_xform(pixels.size)))
	var header: Control = game.get_node("Root/TopCommandBar")
	header.offset_left = safe.position.x + 8
	header.offset_right = safe.end.x - root.size.x - 8
	header.offset_top = safe.position.y + 8
	var bar: HBoxContainer = header.get_node("TopBar")
	# Brand is already on the title screen; give resources and navigation its space.
	bar.get_child(0).hide()
	game.resource_bar.columns = 6 if safe.size.x >= 1700 else 4
	for id in game.resource_labels:
		game.resource_labels[id].add_theme_font_size_override("font_size",25)
		game.resource_icon_rects[id].custom_minimum_size = Vector2(32,32)
		game.resource_chips[id].custom_minimum_size.y = 72
	var height := maxf(172,bar.get_combined_minimum_size().y+24)
	header.offset_bottom = header.offset_top+height
	game.station_center.offset_top = header.offset_bottom+8
	game.station_center.offset_left = safe.position.x+8
	var dock: Control = game.get_node("Root/SideDock")
	dock.offset_top = header.offset_bottom+8
	dock.offset_right = safe.end.x-root.size.x-8
	dock.offset_left = dock.offset_right-600
	dock.offset_bottom = safe.end.y-root.size.y-8
	game.station_center.offset_right = dock.offset_left-12
	game.hand_panel.offset_right = dock.offset_left-12
	game.hand_panel.offset_bottom = safe.end.y-root.size.y-8
	game.hand_panel.offset_left = safe.position.x+8
	game.hand_panel.offset_top = game.hand_panel.offset_bottom+(-100 if game.hand_collapsed else -530)
	game.station_center.offset_bottom = game.hand_panel.offset_top-8 if preload("res://scripts/title_settings.gd").hand_backdrop else safe.end.y-root.size.y-8

func refresh_blueprint_actions() -> void:
	var actions: Node = game.find_child("TouchActions",true,false)
	if actions != null:
		actions.visible = not game.selected_card_id.is_empty() and not game._dialogue_open()
		var reroll: Button = actions.get_node("TouchReroll")
		reroll.disabled = game.rerolls_remaining <= 0 or not game.running

func refresh_targets() -> void:
	refresh_blueprint_actions()
	for path in ["Root/SideDock", "Root/TopCommandBar", "Root/BottomHand"]:
		_size_targets(game.get_node(path))
	if is_instance_valid(game.menu_center): _size_targets(game.menu_center,false,true)
	_fit_layout.call_deferred()

func _size_targets(node: Node, compact := false, menu := false) -> void:
	compact = compact or node.name in ["PreviewPanel","ControlsPanel"]
	# Card typography and art grow together through the card transform.
	if node.has_meta("card_id"): return
	if node is Button:
		node.custom_minimum_size = node.custom_minimum_size.max(Vector2(72,72))
		var font_size := 26 if menu else (20 if compact else 22)
		if node.get_theme_font_size("font_size") != font_size: node.add_theme_font_size_override("font_size",font_size)
		if menu: node.custom_minimum_size.y = maxf(node.custom_minimum_size.y,84)
		if compact: compact_button(node)
	elif node is Label:
		if node.get_theme_font_size("font_size") < 20: node.add_theme_font_size_override("font_size",20)
	elif node is RichTextLabel:
		if node.get_theme_font_size("normal_font_size") < 22: node.add_theme_font_size_override("normal_font_size",22)
		if node.get_theme_font_size("bold_font_size") < 22: node.add_theme_font_size_override("bold_font_size",22)
	for child in node.get_children(): _size_targets(child,compact,menu)

func cancel_blueprint() -> void:
	if game._gameplay_input_blocked(): return
	game.card_drag._finish()
	game.selected_card_id = ""
	game.selected_rotation = 0
	game.hovered_card_id = ""
	game._refresh_all()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT or what == NOTIFICATION_APPLICATION_PAUSED:
		fingers.clear()
		pair_tap = false
		map_sequence = false
		multiple = true
		suppress_mouse = true
		if is_instance_valid(game) and is_instance_valid(game.card_drag): game.card_drag._finish()

func _input(event: InputEvent) -> void:
	# Dialogue is above the map: never claim its buttons or allow clicks through it.
	if not game._gameplay_input_blocked() and is_instance_valid(game.crew_comms) and game.crew_comms.panel.visible:
		map_sequence = false
		suppress_mouse = false
		if game.card_drag.pressing: game.card_drag._finish()
		if event is InputEventMouse or event is InputEventScreenTouch or event is InputEventScreenDrag:
			if game.station_clear_rect().has_point(event.position) and not game.crew_comms.panel.get_global_rect().has_point(event.position):
				if event is InputEventScreenTouch and not event.pressed: fingers.erase(event.index)
				get_viewport().set_input_as_handled()
				return
	# Godot emits an emulated mouse event BEFORE the corresponding raw touch.
	# Classify the first press here too; otherwise a fresh pinch can place on press.
	if event is InputEventMouseButton and event.device == InputEvent.DEVICE_ID_EMULATION and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed and fingers.is_empty():
			map_sequence = not game._gameplay_input_blocked() and game.station_clear_rect().has_point(event.position) and not game.hand_panel.get_global_rect().has_point(event.position) and not _over_dialogue(event.position)
			suppress_mouse = false
		elif not event.pressed and event.canceled:
			game.card_drag._finish()
			suppress_mouse = true
	# Godot's mouse emulation is dispatched separately from the raw touch;
	# consume only that synthetic stream for a sequence owned by the map.
	if event is InputEventMouse and event.device == InputEvent.DEVICE_ID_EMULATION and (map_sequence or suppress_mouse):
		get_viewport().set_input_as_handled()
		return
	if not (event is InputEventScreenTouch or event is InputEventScreenDrag): return
	if game._gameplay_input_blocked():
		fingers.clear(); map_sequence = false; multiple = true
		return
	if event is InputEventScreenTouch:
		if event.pressed:
			if fingers.is_empty():
				map_sequence = game.station_clear_rect().has_point(event.position) and not game.hand_panel.get_global_rect().has_point(event.position) and not _over_dialogue(event.position)
				pair_tap = false; pair_origins.clear()
				multiple = false; moved = false; suppress_mouse = false; press_at = event.position
			fingers[event.index] = event.position
			if fingers.size() > 1:
				multiple = true
				suppress_mouse = true
				game.card_drag._finish()
				if fingers.size() == 2 and map_sequence:
					pair_tap = not moved and not game.selected_card_id.is_empty()
					pair_origins = fingers.duplicate()
					pair_started = Time.get_ticks_msec()
					pair_card = game.selected_card_id
				elif fingers.size() > 2: pair_tap = false
				if map_sequence: _rebase_pair()
			if not map_sequence: return
		else:
			if not fingers.has(event.index): return
			if event.canceled:
				pair_tap = false
				suppress_mouse = true
				multiple = true
				game.card_drag._finish()
			var return_to_hand: bool = map_sequence and fingers.size()==1 and not multiple and not event.canceled and not game.selected_card_id.is_empty() and game.hand_panel.get_global_rect().has_point(event.position)
			var tap: bool = map_sequence and fingers.size() == 1 and not multiple and not moved and not event.canceled and press_at.distance_to(event.position) <= TAP_SLOP
			if pair_origins.has(event.index) and pair_origins[event.index].distance_to(event.position) > TAP_SLOP: pair_tap = false
			fingers.erase(event.index)
			if return_to_hand: cancel_blueprint()
			if fingers.is_empty() and pair_tap:
				pair_tap = false
				if Time.get_ticks_msec()-pair_started <= 350 and game.selected_card_id == pair_card:
					game._rotate_selected_room()
			if map_sequence and tap and game.station_clear_rect().has_point(event.position):
				var local: Vector2 = game.grid_view.get_global_transform_with_canvas().affine_inverse() * event.position
				var crew_id: String = game.crew_comms.crew_at(local,game.get_cell_size()) if game.selected_card_id.is_empty() and is_instance_valid(game.crew_comms) else ""
				if crew_id.is_empty() or not game.crew_comms.open_crew(crew_id):
					game._on_grid_clicked(Vector2i(floori(local.x/game.get_cell_size()),floori(local.y/game.get_cell_size())))
			if fingers.size() >= 2: _rebase_pair()
	else:
		if not fingers.has(event.index): return
		fingers[event.index] = event.position
		if pair_origins.has(event.index) and pair_origins[event.index].distance_to(event.position) > TAP_SLOP: pair_tap = false
		if not map_sequence: return
		if fingers.size() == 2:
			if not pair_tap: _move_pair()
		elif not multiple:
			moved = moved or press_at.distance_to(event.position) > TAP_SLOP
			var local: Vector2 = game.grid_view.get_global_transform_with_canvas().affine_inverse() * event.position
			game._on_grid_hovered(Vector2i(floori(local.x/game.get_cell_size()),floori(local.y/game.get_cell_size())))
	if map_sequence: get_viewport().set_input_as_handled()

func _rebase_pair() -> void:
	if fingers.size() != 2: return
	var points: Array = fingers.values()
	previous_center = (points[0] + points[1]) * 0.5
	previous_span = points[0].distance_to(points[1])
	scroll_position = Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)
	game.camera_view_revision += 1
	game.camera_zoom_target = -1.0
	game.camera_center_target = Vector2.INF

func _move_pair() -> void:
	var points: Array = fingers.values()
	var center: Vector2 = (points[0]+points[1])*0.5
	var span: float = points[0].distance_to(points[1])
	if previous_span < 1.0 or span < 1.0:
		_rebase_pair(); return
	var origin: Vector2 = game.grid_scroll.global_position
	var anchor: Vector2 = (scroll_position + previous_center - origin) / game.grid_zoom
	var zoom: float = clampf(game.grid_zoom * span/previous_span,game._minimum_map_zoom(),game.MAX_GRID_ZOOM)
	game.camera_view_revision += 1
	game.camera_zoom_target = -1.0
	game.grid_zoom = zoom
	game._apply_grid_zoom()
	scroll_position = anchor * zoom - (center-origin)
	game.grid_scroll.scroll_horizontal = roundi(scroll_position.x)
	game.grid_scroll.scroll_vertical = roundi(scroll_position.y)
	# Respect the engine's scroll limits while retaining subpixel travel elsewhere.
	if absf(game.grid_scroll.scroll_horizontal-scroll_position.x) > 1.0: scroll_position.x = game.grid_scroll.scroll_horizontal
	if absf(game.grid_scroll.scroll_vertical-scroll_position.y) > 1.0: scroll_position.y = game.grid_scroll.scroll_vertical
	previous_center = center; previous_span = span

func _over_dialogue(at: Vector2) -> bool:
	return is_instance_valid(game.crew_comms) and game.crew_comms.panel.visible and game.crew_comms.panel.get_global_rect().has_point(at)

static func compact_button(button: Button) -> void:
	# Inset the artwork while keeping a 72-design-pixel hit region.
	for state in ["normal","hover","pressed","disabled"]:
		var style := button.get_theme_stylebox(state)
		if style == null or style.get_meta("tablet_compact",false): continue
		if style is StyleBoxFlat or style is StyleBoxTexture:
			style = style.duplicate()
			style.set_meta("tablet_compact",true)
			style.expand_margin_left = -4
			style.expand_margin_right = -4
			style.expand_margin_top = -4
			style.expand_margin_bottom = -4
			button.add_theme_stylebox_override(state,style)

func center_station() -> void:
	if game.placed_rooms.is_empty(): return
	game.camera_view_revision += 1
	game.camera_zoom_target = -1.0
	game.camera_center_target = Vector2.INF
	var target: Vector2 = game._station_bounds().get_center()*game.get_cell_size()
	var local_center: Vector2 = game.station_clear_rect().get_center()-game.grid_scroll.global_position
	game.grid_scroll.scroll_horizontal = roundi(target.x-local_center.x)
	game.grid_scroll.scroll_vertical = roundi(target.y-local_center.y)
