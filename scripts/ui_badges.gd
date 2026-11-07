extends RefCounted
## Additive badge auditions. Callers supply actual state; these expose no gameplay unlocks.
const Icons = preload("res://scripts/ui_badge_icons.gd")
const Fonts = preload("res://scripts/ui_fonts.gd")
const TONES := {
	"normal": Color("74888b"), "online": Color("779a8c"),
	"warning": Color("b29b6d"), "danger": Color("ad7778"),
	"disabled": Color("64747a"), "research": Color("8795af")
}

static func plate(accent: Color, compact: bool) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color("102a30")
	style.border_color = Color("526067")
	style.set_border_width_all(1)
	style.border_width_left = 3
	# The painted inner lip is quiet enough to sit alongside the card's department paint.
	style.border_color = accent.lerp(Color("526067"),.45)
	style.set_corner_radius_all(4)
	style.content_margin_left = 8
	style.content_margin_right = 9
	style.content_margin_top = 3 if compact else 5
	style.content_margin_bottom = style.content_margin_top
	return style

static func make(caption: String, icon_id: String, tone := "normal", count := -1, compact := false, paint := Color.TRANSPARENT) -> PanelContainer:
	var result := PanelContainer.new()
	result.mouse_filter = Control.MOUSE_FILTER_IGNORE
	result.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	result.custom_minimum_size.y = 28 if compact else 36
	result.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	result.set_meta("badge_icon",icon_id)
	result.set_meta("badge_tone",tone)
	var accent: Color = TONES.get(tone,TONES.normal) if paint == Color.TRANSPARENT else paint
	result.add_theme_stylebox_override("panel",plate(accent,compact))
	var row := HBoxContainer.new()
	row.name = "Content"
	row.add_theme_constant_override("separation",6 if compact else 8)
	result.add_child(row)
	var icon := TextureRect.new()
	icon.name = "Icon"
	icon.texture = Icons.texture(icon_id)
	icon.custom_minimum_size = Vector2(20,20) if compact else Vector2(26,26)
	icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	row.add_child(icon)
	var label := Label.new()
	label.name = "Caption"
	label.text = caption.to_upper()
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.add_theme_font_override("font",Fonts.interface_bold())
	label.add_theme_font_size_override("font_size",13 if compact else 15)
	label.add_theme_color_override("font_color",Color("98a7a7") if tone == "disabled" else Color("d4d9d0"))
	row.add_child(label)
	if count >= 0:
		var number := Label.new()
		number.name = "Count"
		number.text = "99+" if count > 99 else str(count)
		number.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		number.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		number.custom_minimum_size.x = 24
		number.add_theme_font_size_override("font_size",13 if compact else 15)
		var segment := StyleBoxFlat.new()
		segment.bg_color = Color("091e24")
		segment.set_corner_radius_all(3)
		segment.content_margin_left = 6
		segment.content_margin_right = 6
		number.add_theme_stylebox_override("normal",segment)
		row.add_child(number)
	return result

static func department(caption: String, icon_id: String, color: Color, compact := false) -> PanelContainer:
	return make(caption,icon_id,"normal",-1,compact,color.lerp(Color("728488"),.45))

## Readouts preserve signed values and units rather than applying notification count caps.
static func readout(caption: String, icon_id: String, value: String, tone := "normal", compact := false) -> PanelContainer:
	var result := make(caption,icon_id,tone,0,compact)
	result.get_node("Content/Count").name = "Value"
	var amount: Label = result.get_node("Content/Value")
	amount.text = value
	amount.add_theme_color_override("font_color",Color("d4d9d0"))
	return result

static func flow(resource: String, amount: int, compact := false) -> PanelContainer:
	var caption := resource.replace("_"," ")
	var value := ("+" if amount > 0 else "") + str(amount) + " / CYCLE"
	return readout(caption,resource,value,"online" if amount > 0 else ("warning" if amount < 0 else "normal"),compact)

static func vital(caption: String, icon_id: String, percent: int, tone := "normal", compact := false) -> PanelContainer:
	return readout(caption,icon_id,str(clampi(percent,0,100))+"%",tone,compact)

static func update(host: Container, entries: Array) -> void:
	var signature := str(entries)
	if host.get_meta("badge_signature","") == signature: return
	host.set_meta("badge_signature",signature)
	for child in host.get_children(): child.free()
	for entry in entries:
		var item: PanelContainer
		if entry.size() > 3 and entry[3] is String:
			item = readout(entry[0],entry[1],entry[3],entry[2],true)
		else:
			item = make(entry[0],entry[1],entry[2],int(entry[3]) if entry.size()>3 else -1,true)
		host.add_child(item)
	host.visible = not entries.is_empty()
