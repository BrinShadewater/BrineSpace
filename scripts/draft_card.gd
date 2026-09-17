extends RefCounted
## Card-shaped draft hand (owner playtest, Sept 16 mockup): each blueprint is a real card with a
## title plate, art window, type ribbon, rules box and a rarity/cost footer. The hand shows
## them as a row or as a fan (Preferences.hand_layout); the draw and discard piles are card-back
## stacks. Hover and selection handling stay in main.gd.

const Preferences = preload("res://scripts/title_settings.gd")
const RoomDatabase = preload("res://scripts/room_database.gd")

const CARD_SIZE := Vector2(200, 284)
const ROW_SLOT := Vector2(212, 330)
const FAN_STEP := 150.0
const FAN_DEGREES := 7.0
const FAN_DROP := 10.0
const HOVER_LIFT := 22.0
const HOVER_SCALE := 1.05

static func build(game, id: String) -> PanelContainer:
	var room: Dictionary = RoomDatabase.get_room(id)
	var cost: Dictionary = room.get("cost", {})
	var affordable: bool = game._can_afford(cost)
	var category_color: Color = RoomDatabase.category_color(room["category"])
	var card := PanelContainer.new()
	card.name = "%sCard" % id
	card.size = CARD_SIZE
	card.custom_minimum_size = CARD_SIZE
	card.mouse_filter = Control.MOUSE_FILTER_STOP
	# The game draws with nearest filtering for pixel art; turned (fan) or scaled (hover) text and
	# frames sampled that way look jagged (owner playtest), so cards filter smoothly. The room
	# art keeps its own nearest filter.
	card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.pivot_offset = Vector2(CARD_SIZE.x * 0.5, CARD_SIZE.y)
	# Cards sit outside containers, and before the text has a width it wraps very tall; a
	# Control grows to that and never shrinks back, so pin it to card size once text settles.
	card.resized.connect(_fit_card.bind(card))
	card.minimum_size_changed.connect(_fit_card.bind(card))
	card.set_meta("card_id", id)
	card.set_meta("category_color", category_color)
	card.set_meta("affordable", affordable)
	card.tooltip_text = game._blueprint_decision(room)
	game._apply_card_style(card, category_color, game.selected_card_id == id, affordable)
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 4)
	body.mouse_filter = Control.MOUSE_FILTER_IGNORE
	card.add_child(body)

	var title := Label.new()
	title.text = str(room["display_name"])
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	title.custom_minimum_size = Vector2(0, 28)
	title.clip_text = true
	title.add_theme_font_size_override("font_size", 15 if title.text.length() <= 14 else (13 if title.text.length() <= 18 else 11))
	title.add_theme_color_override("font_color", Color("#e2ecee"))
	title.add_theme_stylebox_override("normal", _box(Color("#16222a"), category_color.darkened(0.45), 1, 6))
	body.add_child(_ignore(title))

	var art_frame := PanelContainer.new()
	art_frame.custom_minimum_size = Vector2(0, 114)
	art_frame.add_theme_stylebox_override("panel", _box(Color("#05090c"), category_color.darkened(0.3), 1, 2, 2))
	body.add_child(_ignore(art_frame))
	var art_clip := Control.new()
	art_clip.clip_contents = true
	art_frame.add_child(_ignore(art_clip))
	var art := TextureRect.new()
	art.set_anchors_preset(Control.PRESET_FULL_RECT)
	art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	art.texture = game.card_textures.get(id)
	art.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	art_clip.add_child(_ignore(art))
	if game.prototype_card_seen_cycle.has(id):
		var prototype := Label.new()
		prototype.text = "NEW PROTOTYPE"
		prototype.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		prototype.position = Vector2(4, 4)
		prototype.custom_minimum_size = Vector2(108, 20)
		prototype.add_theme_font_size_override("font_size", 10)
		prototype.add_theme_color_override("font_color", Color("#d8fff2"))
		game._add_label_panel_style(prototype, Color("#0b3029"), game.UI_ACCENT_BRIGHT)
		art_clip.add_child(_ignore(prototype))

	var ribbon := Label.new()
	ribbon.text = str(room["category"]).to_upper()
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_font_size_override("font_size", 10)
	ribbon.add_theme_color_override("font_color", category_color.lightened(0.1))
	ribbon.add_theme_stylebox_override("normal", _box(Color("#090f14"), category_color.darkened(0.2), 1, 3))
	body.add_child(_ignore(ribbon))

	var rules := PanelContainer.new()
	rules.size_flags_vertical = Control.SIZE_EXPAND_FILL
	rules.add_theme_stylebox_override("panel", _box(Color("#0a1116"), Color(0, 0, 0, 0), 0, 5, 6))
	body.add_child(_ignore(rules))
	var rules_box := VBoxContainer.new()
	rules_box.add_theme_constant_override("separation", 2)
	rules.add_child(_ignore(rules_box))
	var output := RichTextLabel.new()
	output.bbcode_enabled = true
	output.fit_content = true
	output.scroll_active = false
	output.text = game._primary_output_line(room)
	output.add_theme_font_size_override("normal_font_size", 13)
	output.add_theme_color_override("default_color", Color("#a9bcc4"))
	rules_box.add_child(_ignore(output))
	var hint := Label.new()
	hint.text = "CLICK TO SELECT" if affordable else "SHORT: " + game._format_cost(game._missing_cost(cost))
	hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hint.add_theme_font_size_override("font_size", 10)
	hint.add_theme_color_override("font_color", Color("#4a6370") if affordable else Color("#ff8a90"))
	rules_box.add_child(_ignore(hint))

	var footer := HBoxContainer.new()
	footer.add_theme_constant_override("separation", 4)
	body.add_child(_ignore(footer))
	var rarity := Label.new()
	rarity.text = str(room["rarity"]).to_upper()
	rarity.add_theme_font_size_override("font_size", 10)
	rarity.add_theme_color_override("font_color", game._rarity_color(str(room.get("rarity", "common"))).lightened(0.2))
	rarity.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	rarity.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	footer.add_child(_ignore(rarity))
	for key in cost:
		var enough: bool = str(key) == "power" or int(game.resources.get(key, 0)) >= int(cost[key])
		footer.add_child(_ignore(_cost_gem(game, str(key), int(cost[key]), enough)))
	return card

# One cost as a round gem: resource icon and amount, red when that resource is short.
static func _cost_gem(game, resource: String, amount: int, enough: bool) -> Control:
	var gem := RichTextLabel.new()
	gem.bbcode_enabled = true
	gem.fit_content = true
	gem.autowrap_mode = TextServer.AUTOWRAP_OFF
	gem.scroll_active = false
	gem.text = "%s%d" % [game._resource_icon_bbcode(resource, 12), amount]
	gem.add_theme_font_size_override("normal_font_size", 12)
	gem.add_theme_color_override("default_color", Color("#e6eeee") if enough else Color("#ff8a90"))
	gem.add_theme_stylebox_override("normal", _box(Color("#121c22"), Color("#5f7682") if enough else Color("#a2444b"), 1, 10, 3))
	return gem

# Only when the content fits: a card whose text truly overflows stays taller rather than being
# reset every frame.
static func _fit_card(card: Control) -> void:
	var fits: bool = card.get_combined_minimum_size().y <= CARD_SIZE.y + 0.5
	if fits and not card.size.is_equal_approx(CARD_SIZE): card.set_deferred("size", CARD_SIZE)

static func build_piles(game) -> Control:
	var slot := HBoxContainer.new()
	slot.name = "DeckSlot"
	slot.add_theme_constant_override("separation", 10)
	slot.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	slot.add_child(_pile("DRAW", game.draw_pile.size(), 4))
	slot.add_child(_pile("DISCARD", game.discard_pile.size(), 3))
	return slot

# A stack of card backs with the pile's count on the top card.
static func _pile(caption: String, count: int, depth: int) -> Control:
	var back_size := Vector2(128, 182)
	var pile := Control.new()
	pile.name = caption.capitalize() + "Pile"
	pile.custom_minimum_size = back_size + Vector2(4 * depth, 4 * depth)
	pile.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var layers := clampi(count, 1, depth) if count > 0 else 1
	for i in range(layers):
		var back := CardBack.new()
		back.size = back_size
		back.position = Vector2(i * 4, (layers - 1 - i) * 4)
		back.empty = count == 0
		back.mouse_filter = Control.MOUSE_FILTER_IGNORE
		pile.add_child(back)
	var label := Label.new()
	label.text = "%d\n%s" % [count, caption]
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.position = Vector2((layers - 1) * 4, 22)
	label.size = back_size
	label.add_theme_font_size_override("font_size", 15)
	label.add_theme_color_override("font_color", Color("#b9d2d2") if count > 0 else Color("#4a5f66"))
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	pile.add_child(label)
	return pile

class CardBack extends Control:
	var empty := false
	func _draw() -> void:
		var rect := Rect2(Vector2.ZERO, size)
		var fill := StyleBoxFlat.new()
		fill.bg_color = Color("#0c171b") if empty else Color("#10242a")
		fill.set_corner_radius_all(10)
		fill.set_border_width_all(2)
		fill.border_color = Color("#2a3c42") if empty else Color("#4f8a86")
		draw_style_box(fill, rect)
		if empty: return
		var inset := rect.grow(-8)
		var stripe := Color(0.13, 0.26, 0.29, 0.55)
		var step := 12.0
		var height := inset.size.y
		var x := -height
		while x < inset.size.x:
			# A 45-degree stripe from (x, 0) to (x + height, height), clipped to the inset.
			var t0 := clampf(-x / height, 0.0, 1.0)
			var t1 := clampf((inset.size.x - x) / height, 0.0, 1.0)
			if t1 > t0:
				draw_line(inset.position + Vector2(x + t0 * height, t0 * height), inset.position + Vector2(x + t1 * height, t1 * height), stripe, 2.0)
			x += step
		draw_circle(rect.get_center() + Vector2(0, -42), 20.0, Color("#0a1418"))
		draw_arc(rect.get_center() + Vector2(0, -42), 20.0, 0, TAU, 32, Color("#62aa9f"), 2.0)

static func fan_row() -> Control:
	var fan := Control.new()
	fan.name = "FanRow"
	fan.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	fan.custom_minimum_size = Vector2(CARD_SIZE.x + FAN_STEP * 2 + 60, ROW_SLOT.y)
	fan.mouse_filter = Control.MOUSE_FILTER_IGNORE
	fan.resized.connect(layout_fan.bind(fan))
	return fan

# Spread the cards like a held hand: each turns a few degrees about its bottom edge and the
# outer cards sit a little lower. Rest pose is stored for hover to restore.
static func layout_fan(fan: Control) -> void:
	var cards: Array = []
	for child in fan.get_children():
		if child.has_meta("card_id"): cards.append(child)
	cards.sort_custom(func(a, b): return int(a.get_meta("hand_index")) < int(b.get_meta("hand_index")))
	var count := cards.size()
	if count == 0: return
	var mid := (count - 1) * 0.5
	var step := minf(FAN_STEP, (fan.size.x - CARD_SIZE.x - 40.0) / maxf(count - 1, 1)) if count > 1 else 0.0
	for i in range(count):
		var card: Control = cards[i]
		var offset := float(i) - mid
		var at := Vector2(fan.size.x * 0.5 - CARD_SIZE.x * 0.5 + offset * step, 30.0 + offset * offset * FAN_DROP)
		card.set_meta("rest_position", at)
		card.set_meta("rest_rotation", deg_to_rad(offset * FAN_DEGREES))
		card.set_meta("rest_index", i)
		card.size = CARD_SIZE
		card.position = at
		card.rotation = card.get_meta("rest_rotation")
		card.scale = Vector2.ONE

static func _box(fill: Color, border: Color, border_width: int, radius: int, margin: int = 0) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = border
	box.set_border_width_all(border_width)
	box.set_corner_radius_all(radius)
	box.set_content_margin_all(margin)
	return box

static func _ignore(control: Control) -> Control:
	control.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return control
