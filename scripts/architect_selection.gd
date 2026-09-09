extends Control
## Shared new-loop picker. Browsing never changes the saved selection.
signal closed
signal chosen(id: String)
const Architects = preload("res://scripts/architects.gd")
const Style = preload("res://scripts/title_button_style.gd")
const CLASS_ICONS := {"bill":"crew", "veld":"lab_flask", "branforth":"parts", "marsh":"data"}
const SUPPLY_ICONS := {
	"food":"leaf_food", "oxygen":"o2", "data":"data",
	"biomass":"biomass_growth", "metal":"metal_chunk", "rare_minerals":"rare_minerals"
}
const SUPPLY_NAMES := {
	"food":"Food", "oxygen":"Oxygen", "data":"Data",
	"biomass":"Biomass", "metal":"Metal", "rare_minerals":"Rare Mineral"
}
var meta_state
var selected := "bill"
var entries := {}
var confirm: Button
var detail: Label
var finished := false
var companion_choices: Array = []
var companion_buttons := {}

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
	layout.add_child(_label("AWAKEN ARCHITECT // RECOVERY MANIFEST",28))
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
		face.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		if unlocked:
			face.texture = Architects.selection_portrait(id)
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
		info.add_child(_label(Architects.NAMES[id] if unlocked else ("UNKNOWN ANDROID // POWERED DOWN" if id=="marsh" else "UNKNOWN ARCHITECT // IN STASIS"),23))
		if unlocked:
			var role := HBoxContainer.new()
			role.add_theme_constant_override("separation",8)
			role.add_child(_icon(CLASS_ICONS[id],Architects.ROLES[id]))
			var role_label := _label(Architects.ROLES[id],17)
			role_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			role.add_child(role_label)
			info.add_child(role)
			var supplies := HFlowContainer.new()
			supplies.add_theme_constant_override("h_separation",20)
			supplies.add_theme_constant_override("v_separation",4)
			var supply_heading := _label("At loop start:",18)
			supply_heading.autowrap_mode = TextServer.AUTOWRAP_OFF
			supplies.add_child(supply_heading)
			var starting: Dictionary = Architects.starting_supplies(id)
			for resource_id in starting:
				var supply := HBoxContainer.new()
				supply.add_theme_constant_override("separation",6)
				supply.add_child(_icon(SUPPLY_ICONS[resource_id],SUPPLY_NAMES[resource_id]))
				var amount := _label("+%d %s" % [starting[resource_id],SUPPLY_NAMES[resource_id]],18)
				amount.autowrap_mode = TextServer.AUTOWRAP_OFF
				supply.add_child(amount)
				supplies.add_child(supply)
			info.add_child(supplies)
			if id=="marsh": info.add_child(_label("Sealed android: no helmet or Oxygen required. Returns to his pod at 35% battery; charging costs 1 Power per 25% restored.",17))
		else:
			info.add_child(_label("Personnel record sealed",17))
			info.add_child(_label("Reconnect the derelict charging chamber and restore power. Its machine pumps white fluid into the dormant android until he recharges and wakes. A free berth lets him join the crew." if id=="marsh" else "Connect to a derelict cryo ward and repair its hull. Supply power, a free berth, Food and Oxygen to finish thawing its occupant. Rescue permanently reveals this record.",18))
		var button := Button.new()
		button.text = "SELECT" if unlocked else "LOCKED"
		button.disabled = not unlocked
		button.toggle_mode = true
		button.custom_minimum_size = Vector2(160,48)
		button.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		Style.apply(button,160,48)
		button.add_theme_stylebox_override("focus",_selection_focus())
		button.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
		info.add_child(button)
		entries[id] = button
		button.pressed.connect(_select.bind(id))
	list.add_child(_label("COMPANIONS // OPTIONAL",23))
	companion_choices=meta_state.selected_companion_ids.duplicate()
	for id in preload("res://scripts/companions.gd").IDS:
		var unlocked: bool=meta_state.unlocked_companion_ids.has(id)
		var row := HBoxContainer.new()
		list.add_child(row)
		var face := TextureRect.new()
		face.custom_minimum_size=Vector2(160,170)
		face.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
		row.add_theme_constant_override("separation",24)
		face.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
		face.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		if unlocked:face.texture=preload("res://scripts/companions.gd").portrait(id)
		row.add_child(face)
		var button := CheckBox.new()
		button.add_theme_font_size_override("font_size",22)
		button.text=("%s // %s"%[preload("res://scripts/companions.gd").NAMES[id],preload("res://scripts/companions.gd").ROLES[id]]) if unlocked else "LOCKED // Recover the %s"%preload("res://scripts/companions.gd").OBJECTS[id]
		button.disabled=not unlocked
		button.button_pressed=unlocked and companion_choices.has(id)
		button.toggled.connect(func(value: bool):
			if value and not companion_choices.has(id):companion_choices.append(id)
			elif not value:companion_choices.erase(id))
		row.add_child(button);companion_buttons[id]=button
	detail = _label("",18)
	layout.add_child(detail)
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation",20)
	layout.add_child(actions)
	var back := Button.new()
	back.text = "BACK [ESC]"
	Style.apply(back,280,76)
	back.custom_minimum_size = Vector2(280,76)
	back.add_theme_font_size_override("font_size",24)
	back.add_theme_stylebox_override("focus",_selection_focus())
	back.pressed.connect(_close)
	actions.add_child(back)
	confirm = Button.new()
	Style.apply(confirm,440,76,true)
	confirm.custom_minimum_size = Vector2(440,76)
	confirm.add_theme_font_size_override("font_size",24)
	confirm.add_theme_stylebox_override("focus",_selection_focus())
	confirm.pressed.connect(_confirm)
	actions.add_child(confirm)
	preload("res://scripts/title_settings.gd").apply_menu_text(self)
	_select(selected)
	confirm.grab_focus.call_deferred()

func _selection_focus() -> StyleBoxTexture:
	# Follow the pressure-panel's clipped corners without a rectangular outer box.
	var picture := Image.new()
	picture.load_svg_from_string('<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48"><path d="M12 4H36L44 12V36L36 44H12L4 36V12Z" fill="none" stroke="#b5f3ee" stroke-width="2"/></svg>')
	var focus := StyleBoxTexture.new()
	focus.texture = ImageTexture.create_from_image(picture)
	for side in [SIDE_LEFT,SIDE_TOP,SIDE_RIGHT,SIDE_BOTTOM]:
		focus.set_texture_margin(side,16)
	return focus

func _icon(asset: String, description: String) -> TextureRect:
	var icon := TextureRect.new()
	icon.custom_minimum_size = Vector2(32,32)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	icon.tooltip_text = description
	var picture := Image.new()
	var path := "res://Brine icons/icons_64/resource_icon_%s.png" % asset
	if picture.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) == OK:
		icon.texture = ImageTexture.create_from_image(picture)
	return icon

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
	if not meta_state.select_architect(selected,companion_choices):
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
