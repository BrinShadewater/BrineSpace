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
var texture_cache := {}
const Catalog = preload("res://scripts/codex_catalog.gd")
var close_button: Button
var closing := false
var transition: Tween
var codex_query := ""
var codex_filter_index := 0
var codex_scroll := 0
var progression_cards: GridContainer

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
		codex_count = _label("", 16)
		content.add_child(codex_count)
		content.add_child(_label("Connect neighboring rooms and keep both functioning to discover a synergy. Three consecutive functioning cycles stabilize its reward.", 15))
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
		grid.add_child(_label("BUILD  " + str(ProjectSettings.get_setting("application/config/version", "Prototype — development checkout")) + "\nENGINE  " + Engine.get_version_info().string, 18))
		grid.add_child(_label("BrineSpace is source-available. Art, audio, writing and game rights are reserved. See NOTICE.md for the full rights statement.\n\nPowered by Godot Engine (MIT license).", 18))
		var licenses := RichTextLabel.new()
		licenses.custom_minimum_size = Vector2(0, 360)
		licenses.fit_content = true
		licenses.text = Engine.get_license_text()
		grid.add_child(licenses)
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
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", Color("b9dce5"))
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label

func _layout() -> void:
	if is_instance_valid(grid):
		grid.columns = maxi(1, int((size.x - 160) / (340 * preload("res://scripts/title_settings.gd").text_scale))) if mode == "codex" else 1
	if is_instance_valid(progression_cards):
		progression_cards.columns = 2 if size.x >= 1200 else 1

func _populate_cards() -> void:
	scroll.scroll_vertical = 0
	for child in grid.get_children():
		grid.remove_child(child)
		child.queue_free()
	room_ids.clear()
	visible_entries.clear()
	var entries: Array[Dictionary] = Catalog.room_entries(meta_state) if codex_tab == 0 else Catalog.synergy_entries(meta_state)
	# Partition the catalog without changing the stable numbering of hidden entries.
	var recovered: Array[Dictionary] = []
	var hidden: Array[Dictionary] = []
	for entry in entries:
		if entry.known:
			recovered.append(entry)
		else:
			hidden.append(entry)
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
		var data: Dictionary = entry.data
		var accent := Color("45616f")
		if entry.known:
			accent = Rooms.CATEGORY_COLORS.get(entry.category, Color(data.get("fx_color", "72d9dc")))
		var panel := PanelContainer.new()
		panel.custom_minimum_size = Vector2(290, 0)
		panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		panel.add_theme_stylebox_override("panel", _style(accent))
		grid.add_child(panel)
		var body := VBoxContainer.new()
		body.add_theme_constant_override("separation", 10)
		panel.add_child(body)
		body.add_child(_label("%s // %s" % [entry.category.to_upper(), "RECOVERED" if entry.known else "SIGNAL OBSCURED"], 14))
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
			body.add_child(_label("BUILD  " + _resources(data.get("cost", {})), 14))
			if not data.get("production", {}).is_empty():
				body.add_child(_label("OUTPUT  " + _resources(data.production), 14))
			if not data.get("consumption", {}).is_empty():
				body.add_child(_label("UPKEEP  " + _resources(data.consumption), 14))
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
			if ResourceLoader.exists(path):
				texture = ResourceLoader.load(path) as Texture2D
			if texture == null:
				var image := Image.new()
				if image.load(path) == OK:
					texture = ImageTexture.create_from_image(image)
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

func _populate_progression() -> void:
	var summary := _label("%d RESEARCH   /   %d STABILIZED LOOPS   /   %d PATTERNS STABILIZED" % [meta_state.total_research_points, meta_state.total_victories, meta_state.stabilized_synergy_ids.size()], 23)
	grid.add_child(summary)
	grid.add_child(_label("Some knowledge survives the reset. Some of it should not.\nResearch, learned patterns and unlocked blueprints persist between loops.", 18))
	grid.add_child(_label("%d MEMORIES RECOVERED   /   %d CORE UPGRADES RECOVERED" % [meta_state.recovered_memory_ids.size(), meta_state.brine_upgrades.size()], 16))
	for section in [{"title": "RECOVERED MEMORIES", "records": meta_state.recovered_memory_ids}, {"title": "CORE UPGRADES", "records": meta_state.brine_upgrades}]:
		grid.add_child(_label(section.title, 22))
		if section.records.is_empty():
			grid.add_child(_label("NO RECORDS RECOVERED.", 16))
		else:
			var ids: Array = section.records.keys()
			ids.sort()
			for id in ids:
				grid.add_child(_label(str(id).replace("_", " ").capitalize() + "\nRecorded in this profile. Description and effects are not defined in this prototype.", 17))

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

func _close() -> void:
	if closing:
		return
	closing = true
	if transition and transition.is_running():
		transition.kill()
	if not preload("res://scripts/title_settings.gd").reduced_motion:
		transition = create_tween()
		transition.tween_property(self, "modulate:a", 0.0, 0.12)
		await transition.finished
	hide()
	closed.emit()
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
		preload("res://scripts/title_settings.gd").apply_menu_text(self)
		_layout()
	)
	grid.add_child(settings)
	settings.feedback.hide()
