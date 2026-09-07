extends Control
## Shared new-loop picker. Browsing never changes the saved selection.
signal closed
signal chosen(id: String)
const Architects = preload("res://scripts/architects.gd")
const Style = preload("res://scripts/title_button_style.gd")
var meta_state
var selected := "bill"
var entries := {}
var confirm: Button
var detail: Label
var finished := false

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	theme = Style.menu_theme()
	theme.default_font.multichannel_signed_distance_field = true
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	selected = meta_state.selected_architect
	if not meta_state.unlocked_architect_ids.has(selected): selected = "bill"
	var shade := ColorRect.new()
	shade.color = Color("07131ff5")
	add_child(shade)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var margin := MarginContainer.new()
	add_child(margin)
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for edge in ["left","right","top","bottom"]:
		margin.add_theme_constant_override("margin_"+edge,32)
	var layout := VBoxContainer.new()
	layout.add_theme_constant_override("separation",18)
	margin.add_child(layout)
	layout.add_child(_label("AWAKEN ARCHITECT // CRYO MANIFEST",28))
	layout.add_child(_label("Choose who wakes in the BRINE Core. The others remain somewhere in the dark.",18))
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.mouse_force_pass_scroll_events = false
	layout.add_child(scroll)
	var list := VBoxContainer.new()
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	list.add_theme_constant_override("separation",16)
	scroll.add_child(list)
	for id in Architects.IDS:
		var unlocked: bool = meta_state.unlocked_architect_ids.has(id)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",24)
		var panel := PanelContainer.new()
		var frame := StyleBoxFlat.new()
		frame.bg_color = Color("0d2430")
		frame.border_color = Color("315867")
		frame.set_border_width_all(1)
		frame.content_margin_left = 20
		frame.content_margin_right = 20
		frame.content_margin_top = 14
		frame.content_margin_bottom = 14
		panel.add_theme_stylebox_override("panel",frame)
		list.add_child(panel)
		panel.add_child(row)
		var face := TextureRect.new()
		face.custom_minimum_size = Vector2(160,170)
		face.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		if unlocked:
			face.texture = Architects.portrait(id)
			row.add_child(face)
		else:
			face.free()
			var unknown := _label("?",64)
			unknown.custom_minimum_size = Vector2(160,170)
			unknown.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			unknown.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			row.add_child(unknown)
		var info := VBoxContainer.new()
		info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(info)
		info.add_child(_label(Architects.NAMES[id] if unlocked else "UNKNOWN ARCHITECT // IN STASIS",23))
		info.add_child(_label(Architects.ROLES[id] if unlocked else "Personnel record sealed",17))
		info.add_child(_label(Architects.PERKS[id] if unlocked else "Connect to a derelict cryo ward and repair its hull. Supply power, a free berth, Food and Oxygen to finish thawing its occupant. Rescue permanently reveals this record.",18))
		var button := Button.new()
		button.text = "SELECT" if unlocked else "LOCKED"
		button.disabled = not unlocked
		button.toggle_mode = true
		button.custom_minimum_size = Vector2(160,48)
		button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		Style.apply(button,160,48)
		button.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
		info.add_child(button)
		entries[id] = button
		button.pressed.connect(_select.bind(id))
	detail = _label("",18)
	layout.add_child(detail)
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation",20)
	layout.add_child(actions)
	var back := Button.new()
	back.text = "BACK [ESC]"
	Style.apply(back,200,52)
	back.pressed.connect(_close)
	actions.add_child(back)
	confirm = Button.new()
	Style.apply(confirm,340,52)
	confirm.pressed.connect(_confirm)
	actions.add_child(confirm)
	preload("res://scripts/title_settings.gd").apply_menu_text(self)
	_select(selected)
	confirm.grab_focus.call_deferred()

func _label(value: String, font_size: int) -> Label:
	var label := Label.new()
	label.text = value
	label.custom_minimum_size.y = ceilf(font_size * 1.8)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size",font_size)
	label.add_theme_color_override("font_color",Color("c1e4e8"))
	return label

func _select(id: String) -> void:
	if not meta_state.unlocked_architect_ids.has(id): return
	selected = id
	for key in entries:
		entries[key].set_pressed_no_signal(key == selected)
		entries[key].text = "SELECTED" if key == selected else ("SELECT" if meta_state.unlocked_architect_ids.has(key) else "LOCKED")
	detail.text = "Selected: %s. Starting supplies apply once; rescued crew grant no extra starting cache." % Architects.NAMES[id]
	confirm.text = "AWAKEN // NEW LOOP"

func _confirm() -> void:
	if finished: return
	if not meta_state.select_architect(selected):
		detail.text = "PROGRESSION NOT SAVED // " + meta_state.last_error
		return
	finished = true
	hide()
	chosen.emit(selected)
	queue_free()

func _close() -> void:
	if finished: return
	finished = true
	hide()
	closed.emit()
	queue_free()

func _input(event: InputEvent) -> void:
	if finished: return
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		_close()
	else:
		Style.contain_tab(event,self)
		# Prevent gameplay shortcuts while retaining normal GUI pointer handling.
		if event is InputEventKey and not event.is_action_pressed("ui_accept"):
			get_viewport().set_input_as_handled()

