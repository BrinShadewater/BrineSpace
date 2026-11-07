extends RefCounted
## Presentation only: rewards are recorded by main before this report is built.
const Shop = preload("res://scripts/meta_shop.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
const Patterns = preload("res://scripts/synergy_manager.gd")
const Counter = preload("res://scripts/reward_count.gd")

static func _reveal_sound(kind: String, game, ticking: bool, source = null, hero = null) -> void:
	if kind == "ui_reward_tick" and not ticking: return
	# A late frame can land several counters at once. Keep the final chime clear.
	if kind == "ui_reward_land" and is_instance_valid(hero) and hero.landed: return
	if kind == "ui_reward_tick" and source != null:
		if is_instance_valid(game.station_sound):
			game.station_sound.play_reward_tick((source.elapsed - source.delay) / source.duration)
		return
	game.play_station_sound(kind)

static func animate(game) -> void:
	var hero := game.summary_panel.find_child("ExpeditionEarnings", true, false) as Label
	if hero == null or hero.has_node("RewardCount"): return
	var counter := Counter.new()
	# One-step values only land; a tick leader needs intermediate values.
	var ticking := hero.text.trim_prefix("+").to_int() > 1
	counter.sound_requested.connect(_reveal_sound.bind(game, ticking, counter))
	counter.duration = 0.9
	counter.configure(hero, hero.text.trim_prefix("+").to_int(), "+" if hero.text.begins_with("+") else "", 0.12, true)
	var index := 0
	for tile in game.summary_stats.get_children():
		var figure := tile.get_child(0).get_child(0) as Label
		if figure.text == "--" or figure.has_node("RewardCount"): continue
		var tick := Counter.new()
		var value := figure.text.trim_prefix("x").to_int()
		tick.sound_requested.connect(_reveal_sound.bind(game, not ticking and value > 1, tick, counter))
		if value > 1: ticking = true
		tick.duration = 0.58
		tick.configure(figure, value, "x" if figure.text.begins_with("x") else "", index * 0.045, false)
		index += 1

static func pattern_data(ids: Array) -> int:
	var total := 0
	for id in ids:
		total += int(Patterns.get_synergy(id).get("terminal_reward", {}).get("research", 0)) + Shop.STABILIZE_DATA
	return total

static func label(text: String, size: int, color := Color("#bdd5df")) -> Label:
	var result := Label.new()
	result.text = text
	result.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result.add_theme_font_size_override("font_size", size)
	result.add_theme_color_override("font_color", color)
	return result

static func entry(parent: Control, title: String, detail: String, textures: Array) -> PanelContainer:
	var card := PanelContainer.new()
	card.add_theme_stylebox_override("panel", Widgets.surface("field", "normal", 14))
	parent.add_child(card)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 16)
	card.add_child(row)
	var images := HBoxContainer.new()
	images.custom_minimum_size = Vector2(148, 76) if not textures.is_empty() else Vector2.ZERO
	images.alignment = BoxContainer.ALIGNMENT_CENTER
	images.add_theme_constant_override("separation", 6)
	row.add_child(images)
	for texture in textures:
		if texture == null: continue
		var art := TextureRect.new()
		art.texture = texture
		art.custom_minimum_size = Vector2(68, 76)
		art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		images.add_child(art)
	var words := VBoxContainer.new()
	words.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	words.add_theme_constant_override("separation", 5)
	row.add_child(words)
	words.add_child(label(title, 21, Color("#dddeda")))
	var split := detail.split("  ·  ", true, 1)
	if split.size() > 1:
		var status := Widgets.badge(split[0], "selected" if split[0] in ["STABILIZED", "OWNED"] else "normal")
		status.name = "EntryStatus"
		status.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
		words.add_child(status)
		var description := label(split[1], 16, Color("#a4b9bb"))
		description.name = "EntryDetail"
		words.add_child(description)
	else:
		words.add_child(label(detail, 16, Color("#a4b9bb")))
	return card

static func refresh_balance(game) -> void:
	var balance := game.summary_panel.find_child("AvailableData", true, false) as Label
	if balance != null:
		balance.text = "%d AVAILABLE TO SPEND" % Shop.balance(game.meta)

static func refresh_after_progression(game) -> void:
	refresh_balance(game)
	var highlights: VBoxContainer = game.summary_panel.find_child("Highlights", true, false)
	# Update existing rows in place: rebuilding resets the scroll range during layout.
	for card in highlights.get_children():
		if not card.has_meta("character_id"): continue
		var owned := Shop.character_owned(game.meta, str(card.get_meta("character_id")))
		var status := card.find_child("EntryStatus", true, false) as Label
		var detail := card.find_child("EntryDetail", true, false) as Label
		status.text = "OWNED" if owned else "ENCOUNTERED"
		status.add_theme_stylebox_override("normal", Widgets.surface("badge", "selected" if owned else "normal", 20))
		detail.text = "Available for future expeditions." if owned else "Purchase their return in Upgrades & Unlocks."

static func populate(game, archived: bool) -> void:
	var highlights: VBoxContainer = game.summary_panel.find_child("Highlights", true, false)
	highlights.set_meta("archived", archived)
	for child in highlights.get_children():
		highlights.remove_child(child)
		child.queue_free()
	var earnings: VBoxContainer = game.summary_panel.find_child("Earnings", true, false)
	for child in earnings.get_children():
		earnings.remove_child(child)
		child.queue_free()
	var patterns := pattern_data(game.run_stabilized_synergy_ids)
	var total: int = game.run_awarded_research + patterns
	earnings.add_child(label("EARNED THIS EXPEDITION", 14, Color("#8fa2a5")))
	var amount := label("+%d" % total if total > 0 else "0", 44, Color("#a9e7d4"))
	amount.name = "ExpeditionEarnings"
	earnings.add_child(amount)
	earnings.add_child(label("ARCHIVED DATA", 18, Color("#dddeda")))
	earnings.add_child(label("%d from score\n%d from patterns (already banked)" % [game.run_awarded_research, patterns], 16, Color("#a4b9bb")))
	var balance := Widgets.badge("", "selected")
	balance.name = "AvailableData"
	earnings.add_child(balance)
	refresh_balance(game)
	var ids: Array = game.run_stabilized_synergy_ids.duplicate()
	for id in game.run_discovered_synergy_ids:
		if not ids.has(id): ids.append(id)
	if not ids.is_empty(): highlights.add_child(label("PATTERNS // %02d" % ids.size(), 14, Color("#8fa2a5")))
	for id in ids:
		var pattern: Dictionary = Patterns.get_synergy(id)
		var stabilized: bool = game.run_stabilized_synergy_ids.has(id)
		var art: Array = []
		for room in pattern.get("rooms", []):
			art.append(game.card_textures.get(room))
		entry(highlights, str(pattern.get("name", id)), "STABILIZED  ·  Double pattern bonuses in later loops. Related blueprint costs half." if stabilized else "DISCOVERED  ·  Remembered in your Codex. Sustain it for three functioning cycles to stabilize.", art)
	if not game.run_discovered_character_ids.is_empty(): highlights.add_child(label("CREW & COMPANIONS // %02d" % game.run_discovered_character_ids.size(), 14, Color("#8fa2a5")))
	for id in game.run_discovered_character_ids:
		var name: String = game.Architects.NAMES.get(id, game.Companions.NAMES.get(id, id))
		var card := entry(highlights, name, "OWNED  ·  Available for future expeditions." if Shop.character_owned(game.meta, id) else "ENCOUNTERED  ·  Purchase their return in Upgrades & Unlocks.", [Shop.portrait(id)])
		card.set_meta("character_id", id)
	if game.largest_cascade > 1:
		entry(highlights, "%d patterns linked in one placement" % game.largest_cascade, "Your strongest cascade this expedition.", [])
	if ids.is_empty() and game.run_discovered_character_ids.is_empty():
		highlights.add_child(label("No new patterns or characters recorded. Your expedition earnings remain in the archive.", 17))
	var closing := "The station goes quiet. I will remember what worked."
	if not archived: closing = "I could not keep the station. I have kept the record."
	game.summary_panel.find_child("ClosingLine", true, false).text = "BRINE // “%s”" % closing
	game.summary_text.text = "[color=#8fa2a5]RECOVERED RESOURCES[/color]\n" + game.ResourceIcons.bbcode(game.run_earned, 17) + "\nLearned patterns and purchased blueprints and characters remain in your profile."
	var scroll := highlights.get_parent().get_parent() as ScrollContainer
	scroll.scroll_vertical = 0
