extends RefCounted
## Shared widget assets and palette. Panel frames and illustrated action buttons stay separate.
const Surface = preload("res://scripts/ui_component_style.gd")
static var icons: Dictionary = {}

static func surface(kind: String, state := "normal", padding := 12) -> StyleBox:
	var result := Surface.new()
	result.kind = kind
	result.state = state
	result.content_margin_left = padding
	result.content_margin_right = padding
	return result

static func track(fill: String, edge: String, thickness := 6) -> StyleBoxFlat:
	var result := StyleBoxFlat.new()
	result.bg_color = Color(fill)
	result.border_color = Color(edge)
	result.set_border_width_all(1)
	result.set_corner_radius_all(3)
	result.content_margin_top = thickness*.5
	result.content_margin_bottom = thickness*.5
	return result

static func glyph(kind: String, active := false) -> Texture2D:
	var key := [kind,active]
	if icons.has(key): return icons[key]
	var ink := "b9c6c3" if active else "829391"
	var path := '<path d="M5 8L9 12L14 6" fill="none" stroke="#%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % ink
	if kind == "radio": path = '<circle cx="10" cy="10" r="3" fill="#%s"/>' % ink if active else ''
	if kind == "arrow": path = '<path d="M5 7L10 12L15 7" fill="none" stroke="#%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % ink
	if kind == "arrow_up": path = '<path d="M5 12L10 7L15 12" fill="none" stroke="#%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % ink
	if kind == "close": path = '<path d="M6 6L14 14M14 6L6 14" stroke="#%s" stroke-width="1.7" stroke-linecap="round"/>' % ink
	if kind == "checkbox" and not active: path = ''
	var border := '<rect x="2" y="2" width="16" height="16" rx="4" fill="#102a30" stroke="#5f6d72"/>' if kind == "checkbox" else ('<circle cx="10" cy="10" r="8" fill="#102a30" stroke="#5f6d72"/>' if kind == "radio" else '')
	var source := Image.new()
	source.load_svg_from_string('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20">'+border+path+'</svg>')
	icons[key] = ImageTexture.create_from_image(source)
	return icons[key]

static func switch_texture(on: bool) -> Texture2D:
	var key := ["switch",on]
	if icons.has(key): return icons[key]
	var source := Image.new()
	var knob := 38 if on else 14
	var fill := "315658" if on else "162e36"
	var light := "81a8a2" if on else "41555a"
	source.load_svg_from_string('<svg xmlns="http://www.w3.org/2000/svg" width="156" height="84" viewBox="0 0 52 28"><rect x="1" y="2" width="50" height="24" rx="12" fill="#%s" stroke="#66777c"/><path d="M14 4H38" stroke="#95a19f" stroke-opacity=".2"/><circle cx="%d" cy="14" r="9" fill="#637178" stroke="#899492"/><path d="M%d 10V18M%d 10V18" stroke="#233b44"/><circle cx="%d" cy="14" r="2" fill="#%s"/></svg>' % [fill,knob,knob-2,knob+2,14 if on else 38,light])
	icons[key] = ImageTexture.create_from_image(source)
	return icons[key]

static func apply_theme(theme: Theme) -> void:
	for state in ["selected","unselected","hovered","disabled"]:
		theme.set_stylebox("tab_"+state,"TabBar",surface("tab",{"unselected":"normal","hovered":"hover"}.get(state,state),14))
	theme.set_color("font_selected_color","TabBar",Color("dedfd8"))
	theme.set_color("font_unselected_color","TabBar",Color("92a3a5"))
	theme.set_color("font_hovered_color","TabBar",Color("d0d9d5"))
	theme.set_color("font_disabled_color","TabBar",Color("5c6d71"))
	for state in ["normal","focus","read_only"]:
		theme.set_stylebox(state,"LineEdit",surface("field","disabled" if state=="read_only" else state))
	theme.set_color("font_color","LineEdit",Color("dddeda"))
	theme.set_color("font_placeholder_color","LineEdit",Color("83959a"))
	theme.set_icon("clear","LineEdit",glyph("close"))
	theme.set_icon("arrow","OptionButton",glyph("arrow"))
	theme.set_stylebox("panel","PopupMenu",surface("menu"))
	theme.set_stylebox("hover","PopupMenu",surface("menu","hover",8))
	theme.set_color("font_color","PopupMenu",Color("dddeda"))
	theme.set_color("font_hover_color","PopupMenu",Color("efeee5"))
	theme.set_color("font_disabled_color","PopupMenu",Color("73858a"))
	theme.set_stylebox("panel","TooltipPanel",surface("field"))
	theme.set_color("font_color","TooltipLabel",Color("dddeda"))
	for control in ["CheckBox","CheckButton"]:
		for state in ["normal","hover","pressed","hover_pressed","disabled","focus"]:
			var quiet := StyleBoxFlat.new()
			quiet.bg_color = Color(.08,.20,.23,.5) if state in ["hover","hover_pressed"] else Color.TRANSPARENT
			quiet.set_corner_radius_all(4)
			quiet.content_margin_left = 4
			quiet.content_margin_right = 4
			quiet.content_margin_top = 4
			quiet.content_margin_bottom = 4
			theme.set_stylebox(state,control,quiet)
		for state in ["checked","checked_disabled"]: theme.set_icon(state,control,glyph("checkbox",true))
		for state in ["unchecked","unchecked_disabled"]: theme.set_icon(state,control,glyph("checkbox"))
		theme.set_icon("radio_checked",control,glyph("radio",true))
		theme.set_icon("radio_unchecked",control,glyph("radio"))
	theme.set_constant("icon_max_width","CheckButton",52)
	for state in ["checked","on","checked_disabled","on_disabled","checked_mirrored","on_mirrored"]: theme.set_icon(state,"CheckButton",switch_texture(true))
	for state in ["unchecked","off","unchecked_disabled","off_disabled","unchecked_mirrored","off_mirrored"]: theme.set_icon(state,"CheckButton",switch_texture(false))
	theme.set_stylebox("background","ProgressBar",track("081d23","414e54",8))
	theme.set_stylebox("fill","ProgressBar",track("416d6d","668581",8))
	theme.set_color("font_color","ProgressBar",Color("dddeda"))
	theme.set_stylebox("slider","HSlider",track("0b2229","49585e"))
	theme.set_stylebox("grabber_area","HSlider",track("3d6367","66817f"))
	theme.set_stylebox("grabber_area_highlight","HSlider",track("50787a","7a9690"))
	for control in ["VScrollBar","HScrollBar"]:
		theme.set_stylebox("scroll",control,track("0a2026","33474e",6))
		theme.set_stylebox("grabber",control,track("465d65","687c80",8))
		theme.set_stylebox("grabber_highlight",control,track("5c777b","849995",8))
		theme.set_stylebox("grabber_pressed",control,track("668784","9baba4",8))

static func badge(text: String, state := "normal") -> Label:
	var result := Label.new()
	result.text = text
	result.custom_minimum_size.y = 30
	result.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	result.add_theme_font_size_override("font_size",14)
	result.add_theme_color_override("font_color",Color("c9d3cd"))
	result.add_theme_stylebox_override("normal",surface("badge",state,20))
	return result

static func text_label(text: String, font_size := 17, dim := false) -> Label:
	var result := Label.new()
	result.text = text
	result.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	result.add_theme_font_size_override("font_size",font_size)
	result.add_theme_color_override("font_color",Color("8fa2a5") if dim else Color("dddeda"))
	return result

## Body remains an ordinary container so callers can supply real actions and data.
static func notice(title: String, description: String, icon_id := "info", state := "normal") -> PanelContainer:
	var result := PanelContainer.new()
	var body := VBoxContainer.new()
	body.name = "Body"
	body.add_theme_constant_override("separation",10)
	result.add_child(body)
	var heading := HBoxContainer.new()
	heading.add_theme_constant_override("separation",10)
	body.add_child(heading)
	var icon := TextureRect.new()
	icon.name = "NoticeIcon"
	icon.texture = preload("res://scripts/ui_badge_icons.gd").texture(icon_id)
	icon.custom_minimum_size = Vector2(30,30)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	heading.add_child(icon)
	var caption := text_label(title,18)
	caption.autowrap_mode = TextServer.AUTOWRAP_OFF
	caption.add_theme_font_override("font",preload("res://scripts/ui_fonts.gd").interface_bold())
	heading.add_child(caption)
	if state != "normal": heading.add_child(badge({"selected":"NEW","warning":"WARNING","danger":"FAULT"}.get(state,state.to_upper()),state))
	var detail := text_label(description,16,true)
	detail.custom_minimum_size.x = 240
	body.add_child(detail)
	return result

static func empty_state(title: String, description: String) -> PanelContainer:
	var result := notice(title,description,"search")
	result.name = "ArchiveEmptyState"
	return result

static func loading(title: String, description: String, progress: float) -> PanelContainer:
	var result := notice(title,description,"sensor")
	var meter := ProgressBar.new()
	meter.name = "LoadingProgress"
	meter.value = clampf(progress,0,100)
	meter.show_percentage = false
	meter.custom_minimum_size.y = 14
	result.get_node("Body").add_child(meter)
	return result

## Actions are named controls; callers connect their existing confirmation flow.
static func confirmation(title: String, description: String, accept_text: String, cancel_text := "CANCEL") -> PanelContainer:
	var result := notice(title,description,"warning")
	var actions := HBoxContainer.new()
	actions.name = "Actions"
	actions.add_theme_constant_override("separation",12)
	result.get_node("Body").add_child(actions)
	for entry in [["CancelAction",cancel_text],["ConfirmAction",accept_text]]:
		var button := Button.new()
		button.name = entry[0]
		button.text = entry[1]
		button.custom_minimum_size = Vector2(150,38)
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		actions.add_child(button)
	return result

static func keycap(caption: String) -> Label:
	var result := text_label(caption,14)
	result.autowrap_mode = TextServer.AUTOWRAP_OFF
	result.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	result.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	result.custom_minimum_size = Vector2(32,28)
	result.add_theme_stylebox_override("normal",surface("field","normal",8))
	return result

## Callers provide their actual portrait; this never replaces character artwork.
static func portrait_row(title: String, detail: String, portrait: Texture2D, selected := false) -> PanelContainer:
	var result := PanelContainer.new()
	result.add_theme_stylebox_override("panel",surface("field","selected" if selected else "normal",8))
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation",12)
	result.add_child(row)
	var picture := TextureRect.new()
	picture.name = "Portrait"
	picture.texture = portrait
	picture.custom_minimum_size = Vector2(48,48)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	row.add_child(picture)
	var captions := VBoxContainer.new()
	captions.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(captions)
	captions.add_child(text_label(title,17))
	captions.add_child(text_label(detail,14,true))
	if selected: row.add_child(badge("SELECTED","selected"))
	return result

static func chip(caption: String, selected := false) -> Button:
	var result := Button.new()
	result.text = caption
	result.toggle_mode = true
	result.button_pressed = selected
	result.custom_minimum_size.y = 34
	result.add_theme_font_size_override("font_size",15)
	for state in ["normal","hover","pressed","hover_pressed","disabled","focus"]:
		result.add_theme_stylebox_override(state,surface("tab",{"pressed":"selected","hover_pressed":"selected"}.get(state,state),12))
	return result

static func filter_chips(captions: Array[String], selected_index := 0) -> HFlowContainer:
	var result := HFlowContainer.new()
	result.add_theme_constant_override("h_separation",8)
	result.add_theme_constant_override("v_separation",8)
	selected_index = clampi(selected_index,0,maxi(0,captions.size()-1))
	var group := ButtonGroup.new()
	for index in range(captions.size()):
		var button := chip(captions[index],index == selected_index)
		button.button_group = group
		button.set_meta("choice_index",index)
		result.add_child(button)
	return result

static func resource_tile(id: String, value: int, delta := 0) -> PanelContainer:
	var result := PanelContainer.new()
	result.add_theme_stylebox_override("panel",surface("field"))
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation",6)
	result.add_child(body)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation",10)
	body.add_child(top)
	var icon := TextureRect.new()
	icon.name = "ResourceIcon"
	icon.texture = preload("res://scripts/ui_badge_icons.gd").texture(id)
	icon.custom_minimum_size = Vector2(32,32)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	icon.self_modulate = Color(1.18,1.18,1.18)
	top.add_child(icon)
	top.add_child(text_label(preload("res://scripts/resource_icons.gd").display_name(id).to_upper(),14,true))
	var amount := text_label(str(value),24)
	amount.name = "Amount"
	body.add_child(amount)
	var change := text_label("%+d / CYCLE" % delta if delta != 0 else "NO CHANGE",14,true)
	change.name = "Change"
	if delta < 0: change.add_theme_color_override("font_color",Color("bc9690"))
	body.add_child(change)
	change.hide()
	var flow_badge := preload("res://scripts/ui_badges.gd").flow(id,delta,true)
	flow_badge.get_node("Content/Caption").text = "NET"
	body.add_child(flow_badge)
	return result

static func pagination(total_pages: int, current_page := 0, changed := Callable()) -> HBoxContainer:
	var result := HBoxContainer.new()
	result.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	result.add_theme_constant_override("separation",10)
	var previous := chip("PREVIOUS")
	var next := chip("NEXT")
	previous.name = "PreviousPage"
	next.name = "NextPage"
	previous.toggle_mode = false
	next.toggle_mode = false
	var readout := text_label("",15)
	readout.name = "PageReadout"
	readout.autowrap_mode = TextServer.AUTOWRAP_OFF
	readout.custom_minimum_size.x = 80
	readout.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	readout.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	result.add_child(previous)
	result.add_child(readout)
	result.add_child(next)
	var count := maxi(1,total_pages)
	result.set_meta("page",clampi(current_page,0,count-1))
	var update := func() -> void:
		var page := int(result.get_meta("page"))
		readout.text = "%d / %d" % [page+1,count]
		previous.disabled = page == 0
		next.disabled = page == count-1
	update.call()
	for entry in [[previous,-1],[next,1]]:
		var button: Button = entry[0]
		var direction: int = entry[1]
		button.pressed.connect(func() -> void:
			var before := int(result.get_meta("page"))
			var after := clampi(before+direction,0,count-1)
			result.set_meta("page",after)
			update.call()
			if changed.is_valid() and before != after: changed.call(after)
		)
	return result

static func breadcrumbs(captions: Array[String]) -> HBoxContainer:
	var result := HBoxContainer.new()
	result.add_theme_constant_override("separation",8)
	for index in range(captions.size()):
		if index > 0:
			var separator := text_label("›",18,true)
			separator.autowrap_mode = TextServer.AUTOWRAP_OFF
			separator.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			separator.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
			result.add_child(separator)
		if index == captions.size()-1:
			var current := text_label(captions[index],15)
			current.autowrap_mode = TextServer.AUTOWRAP_OFF
			current.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			current.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
			current.add_theme_stylebox_override("normal",surface("tab","selected",12))
			result.add_child(current)
		else:
			var button := chip(captions[index])
			button.toggle_mode = false
			button.set_meta("path_index",index)
			result.add_child(button)
	return result

static func disclosure(caption: String, content: Control, expanded := false) -> VBoxContainer:
	var result := VBoxContainer.new()
	result.add_theme_constant_override("separation",8)
	var header := chip(caption,expanded)
	header.name = "DisclosureHeader"
	header.alignment = HORIZONTAL_ALIGNMENT_LEFT
	header.expand_icon = true
	header.add_theme_constant_override("icon_max_width",18)
	header.icon = glyph("arrow_up" if expanded else "arrow")
	result.add_child(header)
	content.name = "DisclosureBody"
	content.visible = expanded
	result.add_child(content)
	header.toggled.connect(func(open: bool) -> void:
		content.visible = open
		header.icon = glyph("arrow_up" if open else "arrow")
	)
	return result

static func sort_controls(captions: Array[String], selected_index := 0, changed := Callable()) -> HBoxContainer:
	var result := HBoxContainer.new()
	result.add_theme_constant_override("separation",8)
	result.set_meta("sort_index",clampi(selected_index,0,maxi(0,captions.size()-1)))
	result.set_meta("ascending",true)
	var update := func() -> void:
		for index in range(result.get_child_count()):
			var button: Button = result.get_child(index)
			var active := index == int(result.get_meta("sort_index"))
			button.set_pressed_no_signal(active)
			button.text = captions[index] + (" ↑" if result.get_meta("ascending") else " ↓") if active else captions[index]
	for index in range(captions.size()):
		var button := chip(captions[index])
		result.add_child(button)
		button.pressed.connect(func() -> void:
			var active := int(result.get_meta("sort_index")) == index
			result.set_meta("sort_index",index)
			result.set_meta("ascending",not bool(result.get_meta("ascending")) if active else true)
			update.call()
			if changed.is_valid(): changed.call(index,bool(result.get_meta("ascending")))
		)
	update.call()
	return result
