extends Control

const Rooms = preload("res://scripts/room_database.gd")
const Art = preload("res://scripts/room_card_art.gd")
const Runs = preload("res://scripts/run_manager.gd")
signal closed
var meta_state
var mode := ""
var in_game := false
var content: VBoxContainer
var scroll: ScrollContainer
var grid: GridContainer
var search: LineEdit
var room_ids: Array[String] = []
var visible_entries: Array[Dictionary] = []
var codex_tab := 0
var codex_filter: OptionButton
var codex_tabs: TabBar
var codex_count: Label
var codex_hint: Label
var texture_cache := {}
const Catalog = preload("res://scripts/codex_catalog.gd")
const ResearchTree = preload("res://scripts/research_tree.gd")
const ResourceIcons = preload("res://scripts/resource_icons.gd")
const RARITY_ORDER := ["core", "common", "uncommon", "rare", "derelict"]
# Smallest interface text; see settings_panel.gd MIN_TEXT.
const MIN_TEXT := 14
const SHADEWATER_LABS_URL := "https://shadewaterlabs.com/"
const AI_DISCLOSURE := "BrineSpace is made by Brin Shadewater with the help of generative AI. AI tools were used to create or assist with parts of the artwork, animation, audio and code, all directed, selected and edited by a human."
var close_button: Button
var closing := false
var transition: Tween
var codex_query := ""
var codex_filter_index := 0
var codex_scroll := 0
var codex_sort_index := 0
var codex_sort: OptionButton
const SORTS := ["SORT: COLOUR", "SORT: RARITY", "SORT: NAME", "SORT: BUILD COST"]
const CARD_WIDTH := 270
# Every room card is this tall at least, recovered or not, so a row of unrecovered signals is the
# same size as a row of rooms (owner playtest, Sept 28).
const CARD_HEIGHT := 500
const DraftCard = preload("res://scripts/draft_card.gd")
const CARDS_PER_ROW := 4
const SYNERGY_WIDTH := 470
var progression_cards: GridContainer
var progression_tab := 0
const MetaShop = preload("res://scripts/meta_shop.gd")
const PROGRESSION_TABS := ["UPGRADES", "BLUEPRINTS", "CREW & COMPANIONS", "RECORDS"]

func _ready() -> void:
	theme = preload("res://scripts/title_button_style.gd").menu_theme()
	resized.connect(_layout)
	_build()

func show_section(section: String) -> void:
	if closing or section == mode:
		return
	if transition and transition.is_running():
		transition.kill()
	if mode == "codex":
		codex_query = search.text
		codex_filter_index = codex_filter.selected
		codex_scroll = scroll.scroll_vertical
	for child in get_children():
		remove_child(child)
		child.queue_free()
	mode = section
	_build()

func _build() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var shade := ColorRect.new()
	shade.color = Color(0.01, 0.035, 0.055, 0.94)
	add_child(shade)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var margins := MarginContainer.new()
	add_child(margins)
	margins.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left", "right", "top", "bottom"]:
		margins.add_theme_constant_override("margin_" + side, 48)
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", _style(Color("3c6b7d")))
	margins.add_child(panel)
	content = VBoxContainer.new()
	content.add_theme_constant_override("separation", 18)
	panel.add_child(content)
	var header := HBoxContainer.new()
	content.add_child(header)
	var heading := _label({"codex": "CODEX // STATION ARCHIVE", "progression": "BRINE // META PROGRESSION", "settings": "BRINE // SETTINGS", "about": "BRINESPACE // CREDITS & BUILD"}.get(mode, "BRINE"), 28)
	heading.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(heading)
	close_button = Button.new()
	close_button.text = "BACK  [ESC]" if in_game else "CLOSE  [ESC]"
	close_button.custom_minimum_size = Vector2(180, 48)
	preload("res://scripts/title_button_style.gd").apply(close_button, 180, 48)
	close_button.pressed.connect(_close)
	header.add_child(close_button)
	var navigation := HBoxContainer.new()
	navigation.add_theme_constant_override("separation", 12)
	content.add_child(navigation)
	for section in ["settings", "codex", "progression", "about"]:
		var button := Button.new()
		button.name = "Navigate" + section.capitalize()
		button.text = "META PROGRESSION" if section == "progression" else ("CREDITS / BUILD" if section == "about" else section.to_upper())
		button.custom_minimum_size = Vector2(240, 48)
		button.add_theme_font_size_override("font_size", 17)
		button.toggle_mode = true
		button.button_pressed = section == mode
		preload("res://scripts/title_button_style.gd").apply(button, 240, 48)
		button.pressed.connect(_select_section.bind(section, button))
		navigation.add_child(button)
	if mode == "codex":
		search = LineEdit.new()
		search.placeholder_text = "Search names, departments, or clues...  [Ctrl+F]"
		search.custom_minimum_size.y = 48
		search.clear_button_enabled = true
		search.text = codex_query
		search.text_changed.connect(func(_value: String) -> void: _populate_cards())
		content.add_child(search)
		var toolbar := HBoxContainer.new()
		content.add_child(toolbar)
		codex_tabs = TabBar.new()
		codex_tabs.focus_mode = Control.FOCUS_ALL
		codex_tabs.add_tab("ROOMS")
		codex_tabs.add_tab("SYNERGIES")
		codex_tabs.add_tab("TRANSMISSIONS")
		codex_tabs.current_tab = codex_tab
		codex_tabs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		codex_tabs.tab_changed.connect(func(index: int) -> void:
			codex_tab = index
			scroll.scroll_vertical = 0
			_populate_cards()
		)
		toolbar.add_child(codex_tabs)
		codex_filter = OptionButton.new()
		codex_filter.custom_minimum_size = Vector2(220, 48)
		preload("res://scripts/title_button_style.gd").apply(codex_filter, 220, 48)
		for caption in ["ALL ENTRIES", "DISCOVERED", "HIDDEN"]:
			codex_filter.add_item(caption)
		codex_filter.select(codex_filter_index)
		codex_filter.item_selected.connect(func(_index: int) -> void: _populate_cards())
		toolbar.add_child(codex_filter)
		# Room cards can be sorted by department colour, rarity, name or build cost (owner playtest).
		codex_sort = OptionButton.new()
		codex_sort.name = "CodexSort"
		codex_sort.custom_minimum_size = Vector2(240, 48)
		preload("res://scripts/title_button_style.gd").apply(codex_sort, 240, 48)
		for caption in SORTS: codex_sort.add_item(caption)
		codex_sort.select(codex_sort_index)
		codex_sort.item_selected.connect(func(index: int) -> void:
			codex_sort_index = index
			_populate_cards())
		toolbar.add_child(codex_sort)
		codex_count = _label("", 16)
		content.add_child(codex_count)
		codex_hint = _label("Connect neighboring rooms and keep both functioning to discover a synergy. Three consecutive functioning cycles stabilize its reward.", 15)
		content.add_child(codex_hint)
	scroll = ScrollContainer.new()
	scroll.focus_mode = Control.FOCUS_ALL
	scroll.follow_focus = true
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	content.add_child(scroll)
	grid = GridContainer.new()
	grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	grid.add_theme_constant_override("h_separation", 18)
	grid.add_theme_constant_override("v_separation", 18)
	scroll.add_child(grid)
	if mode == "codex":
		_populate_cards()
		scroll.set_deferred("scroll_vertical", codex_scroll)
	elif mode == "settings":
		_populate_settings()
	elif mode == "about":
		grid.add_child(_label("BRINESPACE\nCreated by Alex Yesilcimen\n© 2026 Alex Yesilcimen. All rights reserved.", 24))
		grid.add_child(_label(preload("res://scripts/build_version.gd").details(), 18))
		# Studio link and AI disclosure (owner request, Sept 16).
		var studio := Button.new()
		studio.name = "ShadewaterLabsLink"
		studio.text = "SHADEWATER LABS  //  shadewaterlabs.com"
		studio.tooltip_text = SHADEWATER_LABS_URL
		preload("res://scripts/title_button_style.gd").apply(studio, 420, 48)
		studio.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
		studio.pressed.connect(func() -> void: OS.shell_open(SHADEWATER_LABS_URL))
		grid.add_child(studio)
		var disclosure := _label("AI DISCLOSURE\n" + AI_DISCLOSURE, 17)
		disclosure.name = "AIDisclosure"
		grid.add_child(disclosure)
		grid.add_child(_label("BrineSpace is source-available. Art, audio, writing and game rights are reserved. See NOTICE.md for the full rights statement.\n\nPowered by Godot Engine (MIT license).", 18))
		var licenses := RichTextLabel.new()
		licenses.custom_minimum_size = Vector2(0, 360)
		licenses.fit_content = true
		licenses.text = Engine.get_license_text()
		grid.add_child(licenses)
		# Credits read across the page rather than in a narrow column.
		for child in grid.get_children():
			if child is Label or child is RichTextLabel: child.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	else:
		_populate_progression()
	preload("res://scripts/title_settings.gd").apply_menu_text(self)
	_layout.call_deferred()
	close_button.grab_focus()
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		modulate.a = 0.0
		transition = create_tween()
		transition.tween_property(self, "modulate:a", 1.0, 0.16)

func _select_section(section: String, button: Button) -> void:
	button.set_pressed_no_signal(true)
	show_section(section)

func _style(accent: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color("10232e")
	style.border_color = accent
	style.set_border_width_all(1)
	style.content_margin_left = 20
	style.content_margin_right = 20
	style.content_margin_top = 18
	style.content_margin_bottom = 18
	return style

func _label(text: String, font_size: int = 18) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size", maxi(font_size, MIN_TEXT))
	label.add_theme_color_override("font_color", Color("b9dce5"))
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label

func _layout() -> void:
	if is_instance_valid(grid):
		var scale: float = preload("res://scripts/title_settings.gd").text_scale
		var cell := (CARD_WIDTH + 18) if codex_tab == 0 else (SYNERGY_WIDTH + 18)
		var fits := maxi(1, int((size.x - 140) / (cell * scale)))
		grid.columns = mini(CARDS_PER_ROW if codex_tab == 0 else 2, fits) if mode == "codex" and codex_tab != 2 else 1
		grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	if is_instance_valid(progression_cards):
		var wide: int = CARDS_PER_ROW if progression_cards.name == "BlueprintShop" else 4
		progression_cards.columns = maxi(1, mini(wide, int((size.x - 460) / 300)))

func _populate_cards() -> void:
	scroll.scroll_vertical = 0
	for child in grid.get_children():
		grid.remove_child(child)
		child.queue_free()
	room_ids.clear()
	visible_entries.clear()
	search.visible = codex_tab != 2
	codex_filter.visible = codex_tab != 2
	codex_hint.visible = codex_tab != 2
	codex_sort.visible = codex_tab == 0
	if codex_tab == 2:
		grid.columns = 1
		preload("res://scripts/transmission_archive.gd").populate(self)
		codex_count.text = "%d RECORDINGS RECOVERED" % preload("res://scripts/transmission_archive.gd").available(meta_state).size()
		return
	_layout()
	var entries: Array[Dictionary] = Catalog.room_entries(meta_state) if codex_tab == 0 else Catalog.synergy_entries(meta_state)
	# Partition the catalog without changing the stable numbering of hidden entries.
	var recovered: Array[Dictionary] = []
	var hidden: Array[Dictionary] = []
	for entry in entries:
		if entry.known:
			recovered.append(entry)
		else:
			hidden.append(entry)
	# Room cards sort by the chosen key; colour groups departments, then rarity (owner playtest).
	if codex_tab == 0:
		recovered.sort_custom(_room_order)
		hidden.sort_custom(_room_order)
	else:
		recovered.sort_custom(func(a, b):
			var sa: bool = meta_state.stabilized_synergy_ids.has(a.id)
			var sb: bool = meta_state.stabilized_synergy_ids.has(b.id)
			if sa != sb: return sa
			return str(a.title) < str(b.title))
	entries = recovered + hidden
	var known_count := 0
	for entry in entries:
		if entry.known:
			known_count += 1
		var searchable := "%s %s %s" % [entry.title, entry.category, entry.clue if not entry.known else ""]
		if not search.text.strip_edges().is_empty() and not searchable.to_lower().contains(search.text.strip_edges().to_lower()):
			continue
		if codex_filter.selected == 1 and not entry.known:
			continue
		if codex_filter.selected == 2 and entry.known:
			continue
		visible_entries.append(entry)
		if codex_tab == 0 and entry.known:
			room_ids.append(entry.id)
		if codex_tab == 0:
			grid.add_child(_codex_room_card(entry))
			continue
		if codex_tab == 1:
			grid.add_child(_codex_synergy_card(entry))
			continue
		var data: Dictionary = entry.data
		var accent := Color("45616f")
		if entry.known:
			accent = Rooms.room_color(str(entry.id))
		var panel := PanelContainer.new()
		panel.custom_minimum_size = Vector2(290, 0)
		panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		panel.add_theme_stylebox_override("panel", _style(accent))
		grid.add_child(panel)
		var body := VBoxContainer.new()
		body.add_theme_constant_override("separation", 10)
		panel.add_child(body)
		body.add_child(_label("%s // %s" % [entry.category.to_upper(), "RECOVERED" if entry.known else "SIGNAL OBSCURED"], 15))
		var record_key: String = ("room:" if codex_tab == 0 else "synergy:") + str(entry.id)
		if entry.known and meta_state.unread_records.has(record_key):
			var reviewed := Button.new()
			reviewed.text = "NEW // MARK REVIEWED"
			preload("res://scripts/title_button_style.gd").apply(reviewed, 290, 40)
			reviewed.pressed.connect(func() -> void:
				meta_state.mark_reviewed(record_key)
				reviewed.text = "RECORD REVIEWED"
				reviewed.disabled = true
				scroll.grab_focus()
			)
			body.add_child(reviewed)
		if not entry.known:
			body.add_child(_mystery_picture())
		elif codex_tab == 0:
			body.add_child(_room_picture(entry.id, 180))
		else:
			var linked := HBoxContainer.new()
			linked.custom_minimum_size.y = 180
			linked.alignment = BoxContainer.ALIGNMENT_CENTER
			body.add_child(linked)
			for index in range(data.rooms.size()):
				if index > 0:
					var connector := _label("↔", 28)
					connector.add_theme_color_override("font_color", accent)
					linked.add_child(connector)
				var picture := _room_picture(data.rooms[index], 150)
				picture.size_flags_horizontal = Control.SIZE_EXPAND_FILL
				linked.add_child(picture)
		body.add_child(_label(entry.title, 22))
		if not entry.known:
			body.add_child(_label("CLUE // " + entry.clue, 17))
			continue
		if codex_tab == 0:
			body.add_child(_label(data.get("description", ""), 16))
			body.add_child(_label("BUILD  " + _resources(data.get("cost", {})), 15))
			if not data.get("production", {}).is_empty():
				body.add_child(_label("OUTPUT  " + _resources(data.production), 15))
			if not data.get("consumption", {}).is_empty():
				body.add_child(_label("UPKEEP  " + _resources(data.consumption), 15))
		else:
			var names := PackedStringArray()
			var rooms: Dictionary = Rooms.all_rooms()
			for id in data.rooms:
				names.append(rooms[id].display_name)
			body.add_child(_label(" + ".join(names), 16))
			body.add_child(_label(data.get("effect", ""), 16))
			var stabilized: bool = meta_state.stabilized_synergy_ids.has(entry.id)
			body.add_child(_label("STABILIZED" if stabilized else "DISCOVERED // stabilize over %d consecutive functioning cycles" % data.get("stabilize_cycles", 3), 15))
			var reward: String = data.get("unlock_room_id", "")
			if not reward.is_empty():
				var reward_name: String = rooms[reward].display_name if meta_state.unlocked_room_ids.has(reward) else "Unrecovered blueprint"
				body.add_child(_label("REWARD  " + reward_name, 15))
			elif data.has("terminal_reward"):
				body.add_child(_label("REWARD  " + _resources(data.terminal_reward), 15))
	codex_count.text = "%d / %d %s RECOVERED    //    %d SHOWN" % [known_count, entries.size(), "ROOMS" if codex_tab == 0 else "SYNERGIES", visible_entries.size()]
	if visible_entries.is_empty():
		var empty := VBoxContainer.new()
		empty.add_theme_constant_override("separation", 16)
		grid.add_child(empty)
		empty.add_child(_label("NO MATCHING SIGNALS\nClear the search and filter to scan this archive again.", 20))
		var reset := Button.new()
		reset.name = "ResetCodexSearch"
		reset.text = "CLEAR SEARCH & FILTER"
		preload("res://scripts/title_button_style.gd").apply(reset, 290, 52)
		reset.pressed.connect(func() -> void:
			search.text = ""
			codex_filter.select(0)
			_populate_cards()
			search.grab_focus()
		)
		empty.add_child(reset)
	preload("res://scripts/title_settings.gd").apply_menu_text(grid)

# Room entries as cards, matching the draft hand (owner playtest): title plate, art window,
# category ribbon, description, output and upkeep, and a rarity and cost footer. Unrecovered
# rooms show as a card back with their clue.
func _room_order(a: Dictionary, b: Dictionary) -> bool:
	var ra: int = RARITY_ORDER.find(str(a.data.get("rarity", "common")))
	var rb: int = RARITY_ORDER.find(str(b.data.get("rarity", "common")))
	var ca: int = Rooms.CATEGORY_COLORS.keys().find(str(a.category))
	var cb: int = Rooms.CATEGORY_COLORS.keys().find(str(b.category))
	match codex_sort_index:
		1:
			if ra != rb: return ra < rb
			if ca != cb: return ca < cb
		2:
			pass
		3:
			var costa := 0
			var costb := 0
			for value in a.data.get("cost", {}).values(): costa += int(value)
			for value in b.data.get("cost", {}).values(): costb += int(value)
			if costa != costb: return costa < costb
		_:
			if ca != cb: return ca < cb
			if ra != rb: return ra < rb
	if a.known != b.known: return a.known
	return str(a.title) < str(b.title) if a.known else str(a.id) < str(b.id)

func _codex_room_card(entry: Dictionary) -> Control:
	var data: Dictionary = entry.data
	var known: bool = entry.known
	var accent: Color = Rooms.room_color(str(entry.id)) if known else Color("45616f")
	var card := PanelContainer.new()
	card.name = "CodexCard_" + str(entry.id)
	card.custom_minimum_size = Vector2(CARD_WIDTH, CARD_HEIGHT)
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	card.add_theme_stylebox_override("panel", _card_box(Color("#101a20") if known else Color("#0d161b"), DraftCard.muted(accent), 3, 14, 10))
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 8)
	card.add_child(body)
	var title := _label(entry.title, 18)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", Color("e2ecee") if known else Color("7f9aa3"))
	title.add_theme_stylebox_override("normal", _card_box(Color("16222a"), DraftCard.muted(accent).darkened(0.25), 1, 6, 6))
	body.add_child(title)
	var record_key := "room:" + str(entry.id)
	if known and meta_state.unread_records.has(record_key):
		var reviewed := Button.new()
		reviewed.text = "NEW // MARK REVIEWED"
		preload("res://scripts/title_button_style.gd").apply(reviewed, 260, 38)
		reviewed.pressed.connect(func() -> void:
			meta_state.mark_reviewed(record_key)
			reviewed.text = "RECORD REVIEWED"
			reviewed.disabled = true
			scroll.grab_focus()
		)
		body.add_child(reviewed)
	if not known:
		_unrecovered_body(body, accent, str(entry.clue))
		return card
	var art := PanelContainer.new()
	art.custom_minimum_size.y = 200
	art.add_theme_stylebox_override("panel", _card_box(Color(0, 0, 0, 0), DraftCard.muted(accent), 1, 2, 2))
	body.add_child(art)
	var picture := _room_picture(entry.id, 196)
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	var clip := Control.new()
	clip.clip_contents = true
	art.add_child(clip)
	DraftCard.add_ocean(clip)
	picture.set_anchors_preset(Control.PRESET_FULL_RECT)
	clip.add_child(picture)
	DraftCard.add_rarity_badge(clip, str(data.get("rarity", "common")), DraftCard.muted_bright(accent))
	var ribbon := _label(DraftCard.category_label(data.merged({"id": entry.id})), 12)
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), DraftCard.muted(accent), 1, 3, 2))
	body.add_child(ribbon)
	var rules := PanelContainer.new()
	rules.add_theme_stylebox_override("panel", _card_box(Color("0a1116"), Color(0, 0, 0, 0), 0, 6, 10))
	body.add_child(rules)
	var lines := VBoxContainer.new()
	lines.add_theme_constant_override("separation", 6)
	rules.add_child(lines)
	lines.add_child(_rich("[color=#8fa3ae]BUILD[/color]  [color=#e6eeee]%s[/color]" % ResourceIcons.bbcode(data.get("cost", {})), 15))
	if not data.get("production", {}).is_empty():
		lines.add_child(_rich("[color=#7fd6a6]OUTPUT[/color]  [color=#cfe9dc]+%s[/color]" % ResourceIcons.bbcode(data.production), 15))
	if not data.get("consumption", {}).is_empty():
		lines.add_child(_rich("[color=#e0b36a]UPKEEP[/color]  [color=#e9dcc4]%s[/color]" % ResourceIcons.bbcode(data.consumption), 15))
	if not data.get("storage", {}).is_empty():
		lines.add_child(_rich("[color=#79b8d9]STORAGE[/color]  [color=#cfe3ee]+%s[/color]" % ResourceIcons.bbcode(data.storage), 15))
	lines.add_child(_label(data.get("description", ""), 15))
	return card

# An unrecovered room: the same plates as a recovered one, but the art window is a scanned-water
# static field and the rules box holds the clue.
func _unrecovered_body(body: VBoxContainer, accent: Color, clue: String) -> void:
	var window := PanelContainer.new()
	window.custom_minimum_size.y = 200
	window.add_theme_stylebox_override("panel", _card_box(Color(0, 0, 0, 0), DraftCard.muted(accent), 1, 2, 2))
	var clip := Control.new()
	clip.clip_contents = true
	window.add_child(clip)
	var field := UnresolvedField.new()
	field.set_anchors_preset(Control.PRESET_FULL_RECT)
	clip.add_child(field)
	body.add_child(window)
	var ribbon := _label("SIGNAL OBSCURED", 12)
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), DraftCard.muted(accent), 1, 3, 2))
	body.add_child(ribbon)
	var rules := PanelContainer.new()
	rules.size_flags_vertical = Control.SIZE_EXPAND_FILL
	rules.add_theme_stylebox_override("panel", _card_box(Color("0a1116"), Color(0, 0, 0, 0), 0, 6, 10))
	body.add_child(rules)
	var lines := VBoxContainer.new()
	lines.add_theme_constant_override("separation", 6)
	rules.add_child(lines)
	var heading := _label("CLUE", 13)
	heading.add_theme_color_override("font_color", Color("e0b36a"))
	lines.add_child(heading)
	lines.add_child(_label(clue, 15))
	var footer := _label("UNRECOVERED", 13)
	footer.add_theme_color_override("font_color", Color("5e8293"))
	body.add_child(footer)

# The art window of an unrecovered room: deep water, a survey grid, a reticle hunting for the
# signal, a sweeping scan line and flickering static. Holds still under reduced motion.
class UnresolvedField extends Control:
	var elapsed := 0.0
	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_IGNORE
		set_process(not preload("res://scripts/title_settings.gd").reduced_motion)
	# Hundreds of these can exist (every unrecovered room and unidentified pattern), so only the ones on
	# screen animate, and at 20 frames a second.
	var since_draw := 0.0
	func _process(delta: float) -> void:
		elapsed += delta
		since_draw += delta
		if since_draw < 0.05: return
		since_draw = 0.0
		if get_global_rect().intersects(get_viewport_rect()): queue_redraw()
	func _draw() -> void:
		var area := Rect2(Vector2.ZERO, size)
		draw_texture_rect(preload("res://scripts/draft_card.gd").ocean_texture(), area, false, Color(0.62, 0.7, 0.8))
		var grid := Color(0.45, 0.8, 0.9, 0.07)
		var step := 24.0
		var x := fposmod(elapsed * 2.0, step)
		while x < size.x:
			draw_line(Vector2(x, 0), Vector2(x, size.y), grid, 1.0)
			x += step
		var y := 0.0
		while y < size.y:
			draw_line(Vector2(0, y), Vector2(size.x, y), grid, 1.0)
			y += step
		var c := area.get_center()
		var pulse := 0.5 + 0.5 * sin(elapsed * 1.6)
		for radius in [26.0, 46.0, 68.0]:
			draw_arc(c, radius, 0, TAU, 48, Color(0.45, 0.8, 0.9, 0.10 + 0.10 * pulse), 1.0, true)
		var lock := Color(0.55, 0.85, 0.92, 0.55)
		for corner in [Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1), Vector2(1, 1)]:
			var p: Vector2 = c + corner * 34.0
			draw_line(p, p - Vector2(corner.x * 12.0, 0), lock, 2.0)
			draw_line(p, p - Vector2(0, corner.y * 12.0), lock, 2.0)
		var font := get_theme_default_font()
		draw_string(font, c + Vector2(-8, 12), "?", HORIZONTAL_ALIGNMENT_LEFT, -1, 34, Color(0.7, 0.9, 0.95, 0.75))
		var sweep := fposmod(elapsed * 46.0, size.y + 40.0) - 20.0
		draw_rect(Rect2(0, sweep, size.x, 14), Color(0.5, 0.85, 0.95, 0.05))
		draw_line(Vector2(0, sweep + 14), Vector2(size.x, sweep + 14), Color(0.55, 0.9, 1.0, 0.28), 1.0)
		for i in range(14):
			var seed_value := float(i) * 12.9898 + floorf(elapsed * 3.0 + float(i)) * 78.233
			var rx := fposmod(sin(seed_value) * 43758.5453, 1.0) * size.x
			var ry := fposmod(sin(seed_value * 1.7) * 24634.6345, 1.0) * size.y
			draw_rect(Rect2(rx, ry, 8.0 + fposmod(rx, 18.0), 2.0), Color(0.6, 0.85, 0.95, 0.10))
		draw_string(font, Vector2(8, size.y - 8), "NO LOCK", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.55, 0.8, 0.88, 0.5))

# Synergy entries as cards (owner playtest): the linked rooms side by side in the art window,
# the effect, stabilisation state and reward. Undiscovered patterns show their clue.
# Owner playtest (Sept 17): a synergy shows its two rooms as two cards side by side, joined by
# the link, above the effect. Undiscovered patterns show two card backs and the clue.
func _codex_synergy_card(entry: Dictionary) -> Control:
	var data: Dictionary = entry.data
	var known: bool = entry.known
	var stabilized: bool = meta_state.stabilized_synergy_ids.has(entry.id)
	var accent := Color(str(data.get("fx_color", "72d9dc"))) if known else Color("45616f")
	var card := PanelContainer.new()
	card.name = "CodexSynergy_" + str(entry.id)
	card.custom_minimum_size = Vector2(SYNERGY_WIDTH, 0)
	card.size_flags_horizontal = Control.SIZE_FILL
	card.add_theme_stylebox_override("panel", _card_box(Color(0, 0, 0, 0), Color(0, 0, 0, 0), 0, 0, 0))
	var body := VBoxContainer.new()
	body.add_theme_constant_override("separation", 8)
	card.add_child(body)
	var title := _label(entry.title, 18)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", Color("e2ecee") if known else Color("7f9aa3"))
	title.add_theme_stylebox_override("normal", _card_box(Color("16222a"), accent.darkened(0.4), 1, 6, 6))
	body.add_child(title)
	var record_key := "synergy:" + str(entry.id)
	if known and meta_state.unread_records.has(record_key):
		var reviewed := Button.new()
		reviewed.text = "NEW // MARK REVIEWED"
		preload("res://scripts/title_button_style.gd").apply(reviewed, 260, 38)
		reviewed.pressed.connect(func() -> void:
			meta_state.mark_reviewed(record_key)
			reviewed.text = "RECORD REVIEWED"
			reviewed.disabled = true
			scroll.grab_focus()
		)
		body.add_child(reviewed)
	var pair := HBoxContainer.new()
	pair.name = "LinkedCards"
	pair.alignment = BoxContainer.ALIGNMENT_CENTER
	pair.add_theme_constant_override("separation", 6)
	body.add_child(pair)
	for index in range(data.rooms.size()):
		if index > 0:
			var connector := _label("+", 34)
			connector.autowrap_mode = TextServer.AUTOWRAP_OFF
			connector.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			connector.custom_minimum_size.x = 26
			connector.add_theme_color_override("font_color", accent.lightened(0.2) if known else Color("45616f"))
			connector.size_flags_vertical = Control.SIZE_SHRINK_CENTER
			pair.add_child(connector)
		pair.add_child(_mini_room_card(str(data.rooms[index]), known))
	if not known:
		var hidden_ribbon := _label("SIGNAL OBSCURED", 12)
		hidden_ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		hidden_ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
		hidden_ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), DraftCard.muted(accent), 1, 3, 2))
		body.add_child(hidden_ribbon)
		var hidden_rules := PanelContainer.new()
		hidden_rules.add_theme_stylebox_override("panel", _card_box(Color("0a1116"), Color(0, 0, 0, 0), 0, 6, 10))
		body.add_child(hidden_rules)
		var hidden_lines := VBoxContainer.new()
		hidden_lines.add_theme_constant_override("separation", 6)
		hidden_rules.add_child(hidden_lines)
		var clue_heading := _label("CLUE", 13)
		clue_heading.add_theme_color_override("font_color", Color("e0b36a"))
		hidden_lines.add_child(clue_heading)
		hidden_lines.add_child(_label(str(entry.clue), 15))
		var hidden_footer := _label("UNDISCOVERED", 13)
		hidden_footer.add_theme_color_override("font_color", Color("5e8293"))
		body.add_child(hidden_footer)
		return card
	var ribbon := _label("SYNERGY" if stabilized else "DISCOVERED", 12)
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), DraftCard.muted(accent), 1, 3, 2))
	body.add_child(ribbon)
	var rules := PanelContainer.new()
	rules.add_theme_stylebox_override("panel", _card_box(Color("0a1116"), Color(0, 0, 0, 0), 0, 6, 10))
	body.add_child(rules)
	var lines := VBoxContainer.new()
	lines.add_theme_constant_override("separation", 6)
	rules.add_child(lines)
	var rooms: Dictionary = Rooms.all_rooms()
	lines.add_child(_rich(ResourceIcons.decorate(str(data.get("effect", ""))), 15))
	if stabilized and not data.get("bonus", {}).is_empty():
		var bonus := {}
		for key in data.bonus: bonus[key] = int(data.bonus[key]) * 2
		lines.add_child(_rich("[color=#7fd6a6]DOUBLED[/color]  +%s each functioning cycle" % ResourceIcons.bbcode(bonus), 15))
	if not stabilized:
		lines.add_child(_label("Stabilize over %d consecutive functioning cycles." % data.get("stabilize_cycles", 3), 15))
	var reward: String = data.get("unlock_room_id", "")
	var data_reward := int(data.get("terminal_reward", {}).get("research", 0)) + MetaShop.STABILIZE_DATA
	lines.add_child(_rich("[color=#e0b36a]%s[/color]  Bonus doubled in every loop%s" % ["SYNERGY" if stabilized else "AT STABILIZE", "" if stabilized else ", +%d Archived Data" % data_reward], 15))
	if not reward.is_empty():
		lines.add_child(_rich("[color=#79b8d9]BLUEPRINT[/color]  %s half price once stabilized" % rooms[reward].display_name, 15))
	return card

# A small room card for synergy pairs: title, the whole-room picture and the department ribbon.
func _mini_room_card(room_id: String, known: bool) -> Control:
	var room: Dictionary = Rooms.get_room(room_id)
	var accent: Color = Rooms.room_color(room_id) if known else Color("45616f")
	var card := PanelContainer.new()
	card.name = "Card_" + room_id
	card.custom_minimum_size = Vector2(200, 0)
	card.add_theme_stylebox_override("panel", _card_box(Color("#101a20") if known else Color("#0d161b"), DraftCard.muted(accent), 2, 10, 7))
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 5)
	card.add_child(rows)
	var title := _label(str(room.get("display_name", room_id)) if known else "LINKED ROOM", 15)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", Color("e2ecee") if known else Color("7f9aa3"))
	title.add_theme_stylebox_override("normal", _card_box(Color("16222a"), DraftCard.muted(accent).darkened(0.25), 1, 5, 4))
	rows.add_child(title)
	var art := PanelContainer.new()
	art.custom_minimum_size.y = 160
	art.add_theme_stylebox_override("panel", _card_box(Color(0, 0, 0, 0), DraftCard.muted(accent), 1, 2, 2))
	rows.add_child(art)
	var clip := Control.new()
	clip.clip_contents = true
	art.add_child(clip)
	if not known:
		var field := UnresolvedField.new()
		field.set_anchors_preset(Control.PRESET_FULL_RECT)
		clip.add_child(field)
		return card
	DraftCard.add_ocean(clip)
	var picture := _room_picture(room_id, 156)
	picture.set_anchors_preset(Control.PRESET_FULL_RECT)
	clip.add_child(picture)
	var ribbon := _label(DraftCard.category_label(room.merged({"id": room_id})), 12)
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), DraftCard.muted(accent), 1, 3, 2))
	rows.add_child(ribbon)
	return card

func _rich(text: String, font_size: int) -> RichTextLabel:
	var label := RichTextLabel.new()
	label.bbcode_enabled = true
	label.fit_content = true
	label.scroll_active = false
	label.text = text
	label.add_theme_font_size_override("normal_font_size", maxi(font_size, MIN_TEXT))
	label.add_theme_color_override("default_color", Color("b9dce5"))
	return label

func _card_box(fill: Color, border: Color, width: int, radius: int, margin: int) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = border
	box.set_border_width_all(width)
	box.set_corner_radius_all(radius)
	box.set_content_margin_all(margin)
	return box

func _room_picture(id: String, height: int) -> TextureRect:
	var picture := TextureRect.new()
	picture.custom_minimum_size = Vector2(0, height)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if not texture_cache.has(id):
		var path: String = Art.PATHS.get(id, "")
		var texture: Texture2D
		if not path.is_empty():
			texture = preload("res://scripts/safe_image.gd").raw_texture(path)
		texture_cache[id] = texture
	picture.texture = texture_cache[id]
	return picture

func _mystery_picture() -> Control:
	var panel := PanelContainer.new()
	panel.custom_minimum_size.y = 180
	var style := _style(Color("294a5a"))
	style.bg_color = Color("091c28")
	panel.add_theme_stylebox_override("panel", style)
	var symbol := _label("◇  ?  ◇\nUNRESOLVED SIGNAL", 24)
	symbol.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	symbol.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	symbol.add_theme_color_override("font_color", Color("5e8293"))
	panel.add_child(symbol)
	return panel

func _resources(values: Dictionary) -> String:
	var parts := PackedStringArray()
	for key in values:
		parts.append("%s %s" % [values[key], str(key).replace("_", " ")])
	return "None" if parts.is_empty() else " / ".join(parts)

# Meta Progression (owner playtest, Sept 17): one currency, Archived Data, spent across tabs.
func _populate_progression() -> void:
	# The spendable balance with its icon, always in view (owner playtest, Sept 17).
	var balance := HBoxContainer.new()
	balance.name = "ArchivedDataBalance"
	balance.add_theme_constant_override("separation", 12)
	grid.add_child(balance)
	var coin := TextureRect.new()
	coin.texture = load(ResourceIcons.PATHS.archived_data)
	coin.custom_minimum_size = Vector2(40, 40)
	coin.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	coin.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	coin.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	balance.add_child(coin)
	var summary := _label("%d ARCHIVED DATA AVAILABLE" % ResearchTree.available(meta_state), 28)
	summary.name = "ResearchSummary"
	summary.autowrap_mode = TextServer.AUTOWRAP_OFF
	summary.add_theme_color_override("font_color", Color(ResourceIcons.color("archived_data")))
	balance.add_child(summary)
	var totals := _label("%d EARNED   /   %d PATTERNS STABILIZED   /   %d STABILIZED LOOPS" % [meta_state.total_research_points, meta_state.stabilized_synergy_ids.size(), meta_state.total_victories], 17)
	totals.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	totals.autowrap_mode = TextServer.AUTOWRAP_OFF
	totals.add_theme_color_override("font_color", Color("8fa3ae"))
	balance.add_child(totals)
	var tabs := TabBar.new()
	tabs.name = "ProgressionTabs"
	tabs.focus_mode = Control.FOCUS_ALL
	tabs.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for caption in PROGRESSION_TABS: tabs.add_tab(caption)
	tabs.current_tab = progression_tab
	tabs.tab_changed.connect(func(index: int) -> void:
		progression_tab = index
		scroll.scroll_vertical = 0
		_refresh_progression.call_deferred("ProgressionTabs"))
	grid.add_child(tabs)
	match progression_tab:
		1: _blueprint_shop()
		2: _crew_shop()
		3: _records()
		_:
			grid.add_child(_label("Some knowledge survives the reset. Some of it should not. Spend Archived Data on upgrades that carry into every loop, blueprints for your draft deck, and crew and companions.", 16))
			grid.add_child(_research_tree())

func _shop_grid(name: String) -> GridContainer:
	progression_cards = GridContainer.new()
	progression_cards.name = name
	progression_cards.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	progression_cards.add_theme_constant_override("h_separation", 16)
	progression_cards.add_theme_constant_override("v_separation", 16)
	grid.add_child(progression_cards)
	_layout.call_deferred()
	return progression_cards

func _shop_card(id: String, accent: Color, owned: bool) -> Array:
	var card := PanelContainer.new()
	card.name = id
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", _card_box(Color("0e161d"), accent if owned else accent.darkened(0.45), 2 if owned else 1, 12, 12))
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 6)
	card.add_child(rows)
	return [card, rows]

# A crew or companion as a trading card: full name, department ribbon, portrait in the water
# window, what they bring, where they are found, and a short bio.
func _crew_card(id: String, accent: Color, owned: bool, met: bool) -> Array:
	var frame := DraftCard.muted(accent)
	var card := PanelContainer.new()
	card.name = id
	card.custom_minimum_size = Vector2(250, CARD_HEIGHT + 40)
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", _card_box(Color("#101a20"), frame if met else Color("#33444d"), 3, 14, 10))
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 8)
	card.add_child(rows)
	var title := _label(str(MetaShop.CHARACTER_FULL_NAMES.get(id, id)) if met else "UNKNOWN SIGNAL", 17)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	title.custom_minimum_size.y = 52
	title.add_theme_color_override("font_color", Color("e2ecee") if met else Color("7a959e"))
	title.add_theme_stylebox_override("normal", _card_box(Color("16222a"), frame.darkened(0.25), 1, 6, 6))
	rows.add_child(title)
	var window := PanelContainer.new()
	window.custom_minimum_size.y = 200
	window.add_theme_stylebox_override("panel", _card_box(Color(0, 0, 0, 0), frame, 1, 2, 2))
	var clip := Control.new()
	clip.clip_contents = true
	window.add_child(clip)
	DraftCard.add_ocean(clip)
	if met:
		var portrait := TextureRect.new()
		portrait.set_anchors_preset(Control.PRESET_FULL_RECT)
		portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		portrait.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		portrait.texture = MetaShop.portrait(id)
		clip.add_child(portrait)
	else:
		# Not met yet: the same scanned-water static as an unrecovered room.
		var field := UnresolvedField.new()
		field.set_anchors_preset(Control.PRESET_FULL_RECT)
		clip.add_child(field)
	rows.add_child(window)
	var ribbon := _label(str(MetaShop.CHARACTER_CLASSES.get(id, "CREW")), 12)
	ribbon.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ribbon.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	ribbon.add_theme_stylebox_override("normal", _card_box(Color("090f14"), frame, 1, 3, 2))
	rows.add_child(ribbon)
	var rules := PanelContainer.new()
	rules.add_theme_stylebox_override("panel", _card_box(Color("0a1116"), Color(0, 0, 0, 0), 0, 6, 10))
	rows.add_child(rules)
	var lines := VBoxContainer.new()
	lines.add_theme_constant_override("separation", 6)
	rules.add_child(lines)
	if met:
		var perk: String = str(preload("res://scripts/architects.gd").PERKS.get(id, ""))
		if not perk.is_empty():
			var bonus_label := _label("START BONUS", 12)
			bonus_label.add_theme_color_override("font_color", Color("7fd6a6"))
			lines.add_child(bonus_label)
			lines.add_child(_rich(ResourceIcons.decorate(perk.substr(perk.find(": ") + 2) if ": " in perk else perk, 15), 15))
		if id in MetaShop.COMPANIONS:
			var found := _label("FOUND IN  " + str(preload("res://scripts/companions.gd").TITLES.get(id, "")), 13)
			found.add_theme_color_override("font_color", Color("e0b36a"))
			lines.add_child(found)
		var bio := _label(str(MetaShop.CHARACTER_BIOS.get(id, "")), 14)
		bio.add_theme_color_override("font_color", Color("9fb3bd"))
		lines.add_child(bio)
	else:
		lines.add_child(_label("Found in a derelict %s. Repair it during a loop to meet them." % ("companion site" if id in MetaShop.COMPANIONS else "cryo ward"), 15))
	return [card, rows]

# A stretchy gap above the buy button, so it sits at the foot of every card whatever the text above
# it takes (owner playtest, Sept 28).
func _pin_to_bottom(rows: VBoxContainer) -> void:
	var gap := Control.new()
	gap.size_flags_vertical = Control.SIZE_EXPAND_FILL
	gap.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rows.add_child(gap)

func _shop_button(text: String, enabled: bool, action: Callable) -> Button:
	var button := Button.new()
	button.name = "Buy"
	button.text = text
	button.disabled = not enabled
	preload("res://scripts/title_button_style.gd").apply(button, 240, 40)
	button.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	button.pressed.connect(action)
	if "DATA" in text and not text.begins_with("NOT"):
		button.icon = load(ResourceIcons.PATHS.archived_data)
		button.expand_icon = false
		button.add_theme_constant_override("icon_max_width", 22)
	return button

# Blueprints: rooms for the draft deck, priced by rarity; a stabilized related pattern halves it.
func _blueprint_shop() -> void:
	grid.add_child(_label("Bought blueprints join the draft deck in every loop. Stabilizing a room's related pattern halves its price.", 17))
	var cards := _shop_grid("BlueprintShop")
	for id in MetaShop.blueprint_ids():
		var state := MetaShop.room_state(meta_state, id)
		var cost := MetaShop.room_cost(meta_state, id)
		var room_id: String = id
		var card := _codex_room_card({"id": id, "known": true, "title": str(Rooms.get_room(id).display_name), "category": str(Rooms.get_room(id).category), "clue": "", "data": Rooms.get_room(id)})
		card.name = "Blueprint_" + id
		var rows: VBoxContainer = card.get_child(0)
		var pattern := MetaShop.related_pattern(id)
		if not pattern.is_empty() and state != "owned":
			var half: bool = meta_state.stabilized_synergy_ids.has(pattern.id)
			rows.add_child(_label(("HALF PRICE // %s stabilized" if half else "Stabilize %s for half price") % (str(pattern.name) if meta_state.discovered_synergy_ids.has(pattern.id) else "its hidden pattern"), 13))
		_pin_to_bottom(rows)
		rows.add_child(_shop_button({"owned": "OWNED", "ready": "%d DATA" % cost, "short": "%d DATA" % cost}[state], state == "ready", func() -> void:
			if MetaShop.buy_room(meta_state, room_id): _refresh_progression(room_id)))
		cards.add_child(card)

# Crew & companions: met during a loop (thawed or rebooted), then bought for future loops.
func _crew_shop() -> void:
	grid.add_child(_label("Thaw a crew member or reboot a companion during a loop and they play for the rest of it. Buy them here to bring them into future loops.", 17))
	var cards := _shop_grid("CrewShop")
	for id in MetaShop.ROSTER:
		var state := MetaShop.character_state(meta_state, id)
		var owned: bool = state == "owned"
		var met: bool = state != "unmet"
		var accent := Color(MetaShop.CHARACTER_COLORS.get(id, "#9fb8c0"))
		var parts := _crew_card(id, accent, owned, met)
		var rows: VBoxContainer = parts[1]
		var character_id: String = id
		var cost := int(MetaShop.CHARACTER_COSTS.get(id, 0))
		_pin_to_bottom(rows)
		rows.add_child(_shop_button({"owned": "ABOARD" if id in MetaShop.ALWAYS_ABOARD else "OWNED", "ready": "%d DATA" % cost, "short": "%d DATA" % cost, "unmet": "NOT MET YET"}[state], state == "ready", func() -> void:
			if MetaShop.buy_character(meta_state, character_id): _refresh_progression(character_id)))
		cards.add_child(parts[0])

func _records() -> void:
	grid.add_child(_label("%d MEMORIES RECOVERED" % meta_state.recovered_memory_ids.size(), 16))
	grid.add_child(_label("RECOVERED MEMORIES", 22))
	if meta_state.recovered_memory_ids.is_empty():
		grid.add_child(_label("NO RECORDS RECOVERED.", 16))
	else:
		var ids: Array = meta_state.recovered_memory_ids.keys()
		ids.sort()
		for id in ids:
			grid.add_child(_label(str(id).replace("_", " ").capitalize() + "\nRecorded in this profile.", 17))

# BRINE memory core (owner playtest, Sept 17: Meta Progression option A). The upgrade web on the
# left, the selected node's details and purchase on the right.
var core_web: Control
var perk_detail: VBoxContainer
static var core_selected := "eng_salvaged_stock"

func _research_tree() -> Control:
	var box := VBoxContainer.new()
	box.name = "ResearchTree"
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	box.add_theme_constant_override("separation", 10)
	var title := _label("BRINE MEMORY CORE", 18)
	title.add_theme_color_override("font_color", Color("9ff3df"))
	box.add_child(title)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 24)
	box.add_child(row)
	core_web = preload("res://scripts/memory_core_web.gd").new()
	core_web.name = "MemoryCore"
	core_web.meta_state = meta_state
	core_web.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(core_web)
	var side := PanelContainer.new()
	side.custom_minimum_size = Vector2(380, 0)
	side.size_flags_vertical = Control.SIZE_SHRINK_BEGIN
	side.add_theme_stylebox_override("panel", _card_box(Color("0c1c23"), Color("2e5d66"), 1, 12, 18))
	row.add_child(side)
	perk_detail = VBoxContainer.new()
	perk_detail.name = "PerkDetail"
	perk_detail.add_theme_constant_override("separation", 12)
	side.add_child(perk_detail)
	core_web.node_selected.connect(_show_perk)
	if not ResearchTree.PERKS.has(core_selected): core_selected = "eng_salvaged_stock"
	core_web.selected = core_selected
	_show_perk(core_selected)
	var footer := HBoxContainer.new()
	footer.add_theme_constant_override("separation", 18)
	box.add_child(footer)
	var note := _label("Select a node to see it. Each loop banks Archived Data from its Data and Resonance. Each department's nodes open in order, ending in a keystone, and start-of-loop upgrades apply from your next loop.", 15)
	note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	footer.add_child(note)
	var refund := Button.new()
	refund.name = "RefundResearch"
	refund.text = "REFUND ALL UPGRADES"
	refund.disabled = ResearchTree.spent(meta_state) == 0
	preload("res://scripts/title_button_style.gd").apply(refund, 260, 44)
	refund.pressed.connect(func() -> void:
		ResearchTree.refund_all(meta_state)
		_refresh_progression("RefundResearch"))
	footer.add_child(refund)
	return box

func _show_perk(id: String) -> void:
	core_selected = id
	if not is_instance_valid(perk_detail): return
	for child in perk_detail.get_children():
		perk_detail.remove_child(child)
		child.queue_free()
	var perk: Dictionary = ResearchTree.PERKS[id]
	var state := ResearchTree.state(meta_state, id)
	var color := Color.WHITE
	var branch_name := ""
	for branch in ResearchTree.BRANCHES:
		if branch.id == perk.branch:
			color = ResearchTree.branch_color(str(branch.id))
			branch_name = branch.name
	var keystone: bool = perk.get("keystone", false)
	var kind := _label("%s  ·  %s" % [branch_name, "KEYSTONE" if keystone else "TIER %d" % int(perk.tier)], 15)
	kind.add_theme_color_override("font_color", color)
	perk_detail.add_child(kind)
	var perk_name := _label(str(perk.name).to_upper(), 24)
	perk_name.name = "PerkName"
	perk_name.add_theme_color_override("font_color", Color("f1d58a") if keystone else Color("e6f6f3"))
	perk_detail.add_child(perk_name)
	var effect := _rich(ResourceIcons.decorate(str(perk.text), 18), 17)
	perk_detail.add_child(effect)
	var waiting: Array = ResearchTree.missing(meta_state, id).map(func(other): return str(ResearchTree.PERKS[other].name))
	var status: String = {"owned": "INSTALLED IN BRINE'S MEMORY", "ready": "READY TO RECOVER", "short": "NOT ENOUGH ARCHIVED DATA", "locked": "RECOVER %s FIRST" % " AND ".join(waiting).to_upper()}[state]
	var status_label := _label(status, 15)
	status_label.add_theme_color_override("font_color", color if state in ["owned", "ready"] else Color("7f9aa3"))
	perk_detail.add_child(status_label)
	var action := Button.new()
	action.name = "Buy"
	action.text = {"owned": "OWNED", "ready": "%d DATA" % int(perk.cost), "short": "%d DATA" % int(perk.cost), "locked": "LOCKED  ·  %d DATA" % int(perk.cost)}[state]
	action.disabled = state != "ready"
	preload("res://scripts/title_button_style.gd").apply(action, 300, 50)
	action.custom_minimum_size = Vector2(300, 50)
	if state != "owned":
		action.icon = load(ResourceIcons.PATHS.archived_data)
		action.add_theme_constant_override("icon_max_width", 24)
	action.pressed.connect(func() -> void:
		if ResearchTree.buy(meta_state, id):
			core_web.celebrate(id)
			_refresh_progression(id))
	perk_detail.add_child(action)
	var line := _rich("[i][color=#8fb3bd]BRINE: \"%s\"[/color][/i]" % ResearchTree.quote(id), 15)
	perk_detail.add_child(line)
	if is_instance_valid(core_web): core_web.queue_redraw()

# Rebuild the page in place after a purchase or refund, keeping the scroll position and focus.
func _refresh_progression(focus_name: String) -> void:
	var keep := scroll.scroll_vertical
	for child in grid.get_children():
		grid.remove_child(child)
		child.queue_free()
	_populate_progression()
	preload("res://scripts/title_settings.gd").apply_menu_text(self)
	scroll.set_deferred("scroll_vertical", keep)
	var target := grid.find_child(focus_name, true, false)
	if target is PanelContainer: target = target.find_child("Buy", true, false)
	if ResearchTree.PERKS.has(focus_name): target = grid.find_child("PerkDetail", true, false).find_child("Buy", true, false) if grid.find_child("PerkDetail", true, false) != null else target
	if target is Control and target.focus_mode != Control.FOCUS_NONE and not (target is Button and target.disabled):
		target.grab_focus.call_deferred()
	else:
		close_button.grab_focus.call_deferred()

func _input(event: InputEvent) -> void:
	if not closing:
		preload("res://scripts/title_button_style.gd").contain_tab(event, self)
		if mode == "codex" and event is InputEventKey and event.pressed and event.keycode == KEY_F and (event.ctrl_pressed or event.meta_pressed):
			search.grab_focus()
			search.select_all()
			get_viewport().set_input_as_handled()

func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		_close()

# Closing releases the title screen first and fades afterwards. It used to await the fade tween's
# finished signal before emitting: a tween that is killed never emits it, which left a fully
# transparent archive over the title, still swallowing every click, with the title's own buttons
# still disabled behind it. Nothing was on screen to explain it and nothing was logged.
func _close() -> void:
	if closing:
		return
	closing = true
	# The page stops taking input the moment it starts to go, whatever happens to the fade.
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_process_input(false)
	set_process_unhandled_key_input(false)
	closed.emit()
	if transition and transition.is_running():
		transition.kill()
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		transition = create_tween()
		transition.tween_property(self, "modulate:a", 0.0, 0.12)
		# A timer, not the tween: this wait only delays the free, and can never strand the page.
		await get_tree().create_timer(0.14).timeout
	hide()
	queue_free()

func _populate_settings() -> void:
	var status := _label("", 15)
	status.custom_minimum_size.y = 24
	content.add_child(status)
	content.move_child(status, content.get_children().find(scroll))
	var settings := preload("res://scripts/settings_panel.gd").new()
	settings.name = "SettingsPanel"
	settings.preferences_changed.connect(func() -> void:
		status.text = settings.feedback.text
		# The save note already shows above the page; the sidebar copy would repeat it.
		if settings.feedback.text.begins_with("SETTINGS SAVED"): settings.feedback.hide()
		preload("res://scripts/title_settings.gd").apply_menu_text(self)
		_layout()
	)
	grid.add_child(settings)
	settings.feedback.hide()
