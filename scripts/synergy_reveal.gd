extends RefCounted
## Synergy reward notification (owner playtest, Sept 17: finding a synergy needs a visible reward
## on screen). A synergy toast grows into a reveal card inside the existing clickable toast:
## the two linked room cards pop in side by side, the pattern name and its per-cycle bonus with
## resource icons, and for a stabilized pattern the doubled bonus and Archived Data paid. Other
## toasts keep their plain text. Clicking still opens the pattern in the codex.

const ResourceIcons = preload("res://scripts/resource_icons.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const Rooms = preload("res://scripts/room_database.gd")
const PLAIN_SIZE := Vector2(470, 68)
const REVEAL_SIZE := Vector2(520, 330)
const SECONDS := 5.0

# Returns true when the toast is a synergy reveal (and so should stay up longer).
static func configure(game, panel: PanelContainer, label: Label, message: String, record: String) -> bool:
	var reveal: VBoxContainer = panel.get_node_or_null("SynergyReveal")
	var synergy_id := record.trim_prefix("synergy:") if record.begins_with("synergy:") else ""
	var synergy: Dictionary = Synergies.get_synergy(synergy_id) if not synergy_id.is_empty() else {}
	var active := not synergy.is_empty() and (message.begins_with("PATTERN DISCOVERED") or message.begins_with("PATTERN STABILIZED"))
	_size_panel(panel, REVEAL_SIZE if active else PLAIN_SIZE)
	label.visible = not active
	if reveal != null:
		panel.remove_child(reveal)
		reveal.queue_free()
	if not active: return false
	var stabilized := message.begins_with("PATTERN STABILIZED")
	var accent := Color("#" + str(synergy.get("fx_color", "55E6FF")).trim_prefix("#"))
	reveal = VBoxContainer.new()
	reveal.name = "SynergyReveal"
	reveal.mouse_filter = Control.MOUSE_FILTER_IGNORE
	reveal.alignment = BoxContainer.ALIGNMENT_CENTER
	reveal.add_theme_constant_override("separation", 6)
	panel.add_child(reveal)
	var header := _text("[center][color=#%s]◆  %s  ◆[/color][/center]" % [accent.lightened(0.25).to_html(false), "PATTERN STABILIZED" if stabilized else "PATTERN DISCOVERED"], 19)
	reveal.add_child(header)
	var pair := HBoxContainer.new()
	pair.name = "Cards"
	pair.alignment = BoxContainer.ALIGNMENT_CENTER
	pair.mouse_filter = Control.MOUSE_FILTER_IGNORE
	pair.add_theme_constant_override("separation", 14)
	reveal.add_child(pair)
	var rooms: Array = synergy.get("rooms", [])
	for index in range(rooms.size()):
		if index > 0:
			var plus := Label.new()
			plus.name = "Plus"
			plus.text = "+"
			plus.add_theme_font_size_override("font_size", 36)
			plus.add_theme_color_override("font_color", accent.lightened(0.3))
			plus.size_flags_vertical = Control.SIZE_SHRINK_CENTER
			plus.mouse_filter = Control.MOUSE_FILTER_IGNORE
			pair.add_child(plus)
		pair.add_child(_card(game, str(rooms[index])))
	reveal.add_child(_text("[center][font_size=24]%s[/font_size][/center]" % str(synergy.get("name", synergy_id)).to_upper(), 24))
	var bonus: Dictionary = synergy.get("bonus", {})
	var line := ""
	if stabilized:
		var doubled := {}
		for key in bonus: doubled[key] = int(bonus[key]) * 2
		var paid := int(synergy.get("terminal_reward", {}).get("research", 0)) + preload("res://scripts/meta_shop.gd").STABILIZE_DATA
		line = "BONUS DOUBLED" + (": +%s per cycle" % ResourceIcons.bbcode(doubled, 18) if not doubled.is_empty() else "") + "   ·   " + ResourceIcons.amount("archived_data", paid, 18, true)
	elif not bonus.is_empty():
		line = "+%s per functioning cycle" % ResourceIcons.bbcode(bonus, 18)
	else:
		line = ResourceIcons.decorate(str(synergy.get("effect", "")), 18)
	reveal.add_child(_text("[center]%s[/center]" % line, 16))
	reveal.add_child(_text("[center][color=#7f9aa3]Click to review in the Codex[/color][/center]", 12))
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		_animate(reveal, pair, accent)
	return true

static func _size_panel(panel: Control, size: Vector2) -> void:
	panel.offset_left = -size.x * 0.5
	panel.offset_right = size.x * 0.5
	panel.offset_bottom = panel.offset_top + size.y

static func _text(bbcode: String, font_size: int) -> RichTextLabel:
	var label := RichTextLabel.new()
	label.bbcode_enabled = true
	label.fit_content = true
	label.scroll_active = false
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("normal_font_size", font_size)
	label.add_theme_color_override("default_color", Color("#dff7ee"))
	label.text = bbcode
	return label

static func _card(game, room_id: String) -> Control:
	var room: Dictionary = Rooms.get_room(room_id)
	var accent: Color = Rooms.category_color(str(room.get("category", "")))
	var frame := PanelContainer.new()
	frame.name = "Card_" + room_id
	frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var box := StyleBoxFlat.new()
	box.bg_color = Color("#05090c")
	box.border_color = accent
	box.set_border_width_all(2)
	box.set_corner_radius_all(8)
	box.set_content_margin_all(5)
	frame.add_theme_stylebox_override("panel", box)
	var rows := VBoxContainer.new()
	rows.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rows.add_theme_constant_override("separation", 3)
	frame.add_child(rows)
	var art := TextureRect.new()
	art.custom_minimum_size = Vector2(120, 120)
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	art.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	art.texture = game.card_textures.get(room_id) if "card_textures" in game else null
	rows.add_child(art)
	var name := Label.new()
	name.text = str(room.get("display_name", room_id))
	name.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	name.custom_minimum_size.x = 120
	name.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	name.add_theme_font_size_override("font_size", 12)
	name.add_theme_color_override("font_color", accent.lightened(0.25))
	name.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rows.add_child(name)
	return frame

# Cards pop in from the sides one after the other, the plus pulses, and the header flashes.
static func _animate(reveal: Control, pair: HBoxContainer, accent: Color) -> void:
	var delay := 0.08
	for child in pair.get_children():
		child.modulate.a = 0.0
		child.pivot_offset = child.get_combined_minimum_size() * 0.5
		child.scale = Vector2.ONE * 0.6
		var tween := child.create_tween().set_parallel()
		tween.tween_property(child, "modulate:a", 1.0, 0.22).set_delay(delay)
		tween.tween_property(child, "scale", Vector2.ONE, 0.34).set_delay(delay).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
		if child.name == "Plus":
			tween.chain().tween_property(child, "scale", Vector2.ONE * 1.35, 0.18)
			tween.chain().tween_property(child, "scale", Vector2.ONE, 0.24)
		delay += 0.14
	reveal.modulate = Color(accent.lightened(0.6), 1.0)
	reveal.create_tween().tween_property(reveal, "modulate", Color.WHITE, 0.6)
