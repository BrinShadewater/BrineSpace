extends RefCounted
## Real widgets for the Journal's Discoveries and Crew tabs (owner-approved Sept 29, follow-up to the
## journal design pass). The old rich-text version of both tabs is still produced and kept in the
## hidden archive label, so search, tests and screen readers see the same words; these cards, pills,
## bars and buttons are what the player looks at. Built only when the content changes.

const ResourceIcons = preload("res://scripts/resource_icons.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const Companions = preload("res://scripts/companions.gd")
const Architects = preload("res://scripts/architects.gd")
const CryoRecovery = preload("res://scripts/cryo_recovery.gd")
const Widgets = preload("res://scripts/ui_widgets.gd")
const Badges = preload("res://scripts/ui_badges.gd")
const TEAL := Color("6a9490")
const GREEN := Color("86a594")
const AMBER := Color("b29b6d")
const RED := Color("ad7778")
const DIM := Color("8fa9b3")

# ---- small building blocks ----

static func _label(text: String, size: int = 16, colour: Color = Color("c9d9de")) -> Label:
	var label := Label.new()
	label.text = text
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.add_theme_font_size_override("font_size", size)
	label.add_theme_color_override("font_color", colour)
	return label

static func _box(fill: Color, border: Color, radius := 8, margin := 12) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.border_color = border
	style.set_border_width_all(1)
	style.set_corner_radius_all(radius)
	style.content_margin_left = margin
	style.content_margin_right = margin
	style.content_margin_top = maxi(6, margin - 4)
	style.content_margin_bottom = maxi(6, margin - 4)
	return style

static func _card(border: Color = Color("2a4650")) -> PanelContainer:
	var card := PanelContainer.new()
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", _box(Color("0c1820"), border, 10, 14))
	return card

static func _pill(text: String, colour: Color) -> Control:
	var tone := "danger" if colour == RED else "warning" if colour == AMBER else "online" if colour == GREEN else "research"
	var icon := "warning" if tone in ["danger","warning"] else "confirm" if tone == "online" else "search"
	return Badges.make(text,icon,tone,-1,true)

static func _heading(text: String, note := "") -> Control:
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 2)
	rows.add_child(_label(text, 20, Color("a9e7d4")))
	if not note.is_empty(): rows.add_child(_label(note, 15, DIM))
	return rows

static func _bar(value: float, maximum: float, colour: Color) -> ProgressBar:
	var bar := ProgressBar.new()
	bar.min_value = 0.0
	bar.max_value = maximum
	bar.value = clampf(value, 0.0, maximum)
	bar.show_percentage = false
	bar.custom_minimum_size = Vector2(160, 12)
	bar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bar.add_theme_stylebox_override("background",Widgets.track("081d23","414e54",4))
	bar.add_theme_stylebox_override("fill",Widgets.track(colour.to_html(false),"668581",4))
	return bar

static func _action(text: String, callback: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.focus_mode = Control.FOCUS_ALL
	button.custom_minimum_size = Vector2(0, 34)
	button.add_theme_font_size_override("font_size", 14)
	button.pressed.connect(callback)
	return button

static func _clear(box: Container) -> void:
	for child in box.get_children():
		box.remove_child(child)
		child.queue_free()

# Rebuild only when the words behind the widgets changed, so scrolling and hover survive refreshes.
static func _stale(box: Container, signature: String) -> bool:
	if box.has_meta("signature") and str(box.get_meta("signature")) == signature: return false
	box.set_meta("signature", signature)
	return true

# ---- Discoveries ----

static func discoveries(game, box: VBoxContainer, signature: String) -> void:
	if not _stale(box, signature): return
	_clear(box)
	var learned: Array = []
	var stabilized := 0
	var recipes: Array = Synergies.all_synergies().duplicate()
	recipes.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var a_priority: bool = game._active_synergy_link_count(str(a["id"])) > 0 and not game.meta.stabilized_synergy_ids.has(a["id"])
		var b_priority: bool = game._active_synergy_link_count(str(b["id"])) > 0 and not game.meta.stabilized_synergy_ids.has(b["id"])
		return str(a["id"]) < str(b["id"]) if a_priority == b_priority else a_priority)
	for synergy in recipes:
		if game.meta.discovered_synergy_ids.has(synergy["id"]):
			learned.append(synergy)
			if game.meta.stabilized_synergy_ids.has(synergy["id"]): stabilized += 1
	var strip := HBoxContainer.new()
	strip.name = "Stats"
	strip.add_theme_constant_override("separation", 12)
	box.add_child(strip)
	strip.add_child(_stat(learned.size(), "LEARNED", TEAL))
	strip.add_child(_stat(stabilized, "STABILIZED", GREEN))
	strip.add_child(_stat(game.meta.unlocked_room_ids.size(), "BLUEPRINTS AVAILABLE", Color("79b8d9")))
	if learned.is_empty():
		var empty := Widgets.empty_state("NO RECOVERED PATTERNS","Connect different rooms through matching doors and keep them functioning. Three consecutive functioning cycles stabilize a discovered pattern.")
		empty.name = "EmptyRecord"
		box.add_child(empty)
	for synergy in learned:
		box.add_child(_synergy_card(game, synergy))
	var unknown: int = Synergies.all_synergies().size() - learned.size()
	var footer := HBoxContainer.new()
	footer.add_theme_constant_override("separation", 14)
	box.add_child(footer)
	if unknown > 0:
		var note := _label("UNIDENTIFIED SYNERGIES AND PATTERNS REMAIN: %d" % unknown, 15, Color("718a97"))
		note.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		footer.add_child(note)
	var codex := _action("OPEN THE CODEX", func() -> void: game._locate_diagnostic_room("codex"))
	codex.name = "OpenCodex"
	footer.add_child(codex)

static func _stat(number: int, caption: String, colour: Color) -> Control:
	var chip := PanelContainer.new()
	chip.add_theme_stylebox_override("panel", _box(Color("0c1820"), colour.darkened(0.45), 10, 14))
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 10)
	chip.add_child(row)
	var number_label := _label(str(number), 28, colour)
	number_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	row.add_child(number_label)
	var caption_label := _label(caption, 14, DIM)
	caption_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	caption_label.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	row.add_child(caption_label)
	return chip

static func _synergy_card(game, synergy: Dictionary) -> Control:
	var id := str(synergy["id"])
	var accent := Color("#" + str(synergy.get("fx_color", "4fa38d")).trim_prefix("#"))
	var status: String = game._synergy_runtime_status(id)
	var count: int = game._active_synergy_link_count(id)
	var card := _card(accent.darkened(0.35))
	card.name = "Synergy_" + id
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 8)
	card.add_child(rows)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 12)
	rows.add_child(head)
	var title := _label(str(synergy["name"]), 20, accent.lightened(0.35))
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	head.add_child(title)
	var pill_colour := GREEN if status.contains("STABILIZED") else AMBER if status.contains("STABILIZING") else RED if status.begins_with("DORMANT") else DIM
	if Synergies.is_pattern(synergy): head.add_child(_pill("PATTERN", accent.lightened(0.3)))
	head.add_child(_pill(status + (" x%d" % count if count > 1 else ""), pill_colour))
	if status.contains("STABILIZING"):
		var required := int(synergy.get("stabilize_cycles", 3))
		rows.add_child(_bar(float(game.synergy_stabilization_progress.get(id, 0)), float(required), AMBER))
	var pair := HBoxContainer.new()
	pair.add_theme_constant_override("separation", 8)
	rows.add_child(pair)
	var active: bool = game.active_synergies.has(id)
	var index := 0
	for room_id in synergy.get("rooms", []):
		if index > 0: pair.add_child(_label("+", 18, DIM))
		index += 1
		var have: bool = game._has_room(str(room_id))
		var colour: Color = Rooms.room_color(str(room_id)) if have else Color("607784")
		var room_name: String = str(Rooms.get_room(str(room_id)).get("display_name", str(room_id)))
		var chip := PanelContainer.new()
		chip.add_theme_stylebox_override("panel", _box(Color("101a20"), colour.darkened(0.2), 6, 10))
		var chip_label := _label(("◆ " if active else "") + room_name, 15, colour.lightened(0.15) if have else Color("607784"))
		chip_label.autowrap_mode = TextServer.AUTOWRAP_OFF
		chip.add_child(chip_label)
		pair.add_child(chip)
	var effect := RichTextLabel.new()
	effect.bbcode_enabled = true
	effect.fit_content = true
	effect.scroll_active = false
	effect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	effect.add_theme_font_size_override("normal_font_size", 16)
	effect.add_theme_color_override("default_color", Color("c4d1da"))
	effect.text = ResourceIcons.decorate(str(synergy.get("effect", "Special effect restored.")), 16)
	rows.add_child(effect)
	var reward: String = game._synergy_reward_text(synergy)
	if not reward.is_empty():
		var reward_label := RichTextLabel.new()
		reward_label.bbcode_enabled = true
		reward_label.fit_content = true
		reward_label.scroll_active = false
		reward_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		reward_label.add_theme_font_size_override("normal_font_size", 15)
		reward_label.add_theme_color_override("default_color", Color("ecc98d"))
		reward_label.text = ResourceIcons.decorate(reward, 15)
		rows.add_child(reward_label)
	return card

# ---- Crew ----

static func crew(game, box: VBoxContainer, signature: String) -> void:
	if not _stale(box, signature): return
	_clear(box)
	box.add_child(_heading("COMPANIONS", "Separate from architect berths"))
	for id in Companions.IDS:
		box.add_child(_companion_row(game, id))
	var spacer := Control.new()
	spacer.custom_minimum_size.y = 6
	box.add_child(spacer)
	box.add_child(_heading("CREW ROSTER  //  %d / %d BERTHS" % [game.crew_count, game._get_crew_capacity()], "Recovered occupants join after their wake sequence completes."))
	var named_alive := 0
	for member in game.recovered_crew:
		named_alive += int(member.alive)
		box.add_child(_member_row(game, member))
	if game.recovered_crew.is_empty():
		box.add_child(_label("No recovered survivors recorded. The sealed wards remain quiet.", 16, DIM))
	if game.crew_count > named_alive:
		box.add_child(_label("Other station crew: %d" % (game.crew_count - named_alive), 16, DIM))
	for architect in Architects.IDS:
		var actor = Architects.actor_for(game, architect)
		if actor.active and not actor.dead: box.add_child(_vitals_card(architect, actor))
	var wards := VBoxContainer.new()
	wards.add_theme_constant_override("separation", 4)
	for cell in game.wrecks:
		var ward: Dictionary = game.wrecks[cell]
		if ward.kind not in ["cryo", "charging"]: continue
		var waiting := 0
		for pod in ward.pods: waiting += int(not pod.recovered)
		wards.add_child(_label("Ward %s  //  %d in stasis  //  %s" % [cell, waiting, CryoRecovery.status(game, cell)], 15, DIM))
	if wards.get_child_count() > 0:
		box.add_child(_heading("WARDS"))
		box.add_child(wards)

static func _companion_row(game, id: String) -> Control:
	var here: bool = game.companion_roster.has(id)
	var status: String = str(game.companion_actors[id].activity) if here else "Unlocked for future selection" if game.meta.unlocked_companion_ids.has(id) else "Met, buy in Meta Progression to keep" if game.meta.met_character_ids.has(id) else "Not yet recovered"
	var card := _card(Color("2f6a6a") if here else Color("2a4650"))
	card.name = "Companion_" + id
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	card.add_child(row)
	var name_label := _label(str(Companions.NAMES[id]), 18, Color("e2ecee") if here else Color("7f9aa3"))
	name_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	name_label.custom_minimum_size.x = 120
	row.add_child(name_label)
	var status_label := _label(status, 15, GREEN if here else DIM)
	status_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(status_label)
	if here and game.companion_actors[id].active:
		var cell: Vector2i = game.companion_actors[id].cell_at(game.companion_actors[id].foot)
		row.add_child(_action("LOCATE", func() -> void: game._locate_diagnostic_room("%d,%d" % [cell.x, cell.y])))
		if id == "margot":
			if Companions.can_pet(game, true):
				row.add_child(_action("PET MARGOT", func() -> void: game._locate_diagnostic_room("pet:margot")))
			else:
				status_label.text += "  (%s)" % Companions.pet_refusal(game)
	return card

static func _member_row(game, member: Dictionary) -> Control:
	var origin_text := "Awakened in BRINE Core." if member.id == "core_architect" else ("Awakened in charging chamber %s." if member.get("architect_id", "") == "marsh" else "Recovered from cryo ward %s.") % member.origin
	# Whoever was chosen for the loop wakes in the core; only a record without an id means Bill.
	var id: String = str(member.get("architect_id",""))
	if id.is_empty() and member.id == "core_architect": id = "bill"
	var card := Widgets.portrait_row(str(member.name),origin_text,Architects.selection_portrait(id))
	card.get_child(0).get_node("Portrait").visible = Architects.SELECTION_PORTRAITS.has(id)
	var row: HBoxContainer = card.get_child(0)
	row.add_child(_pill("ABOARD" if member.alive else "DECEASED", GREEN if member.alive else RED))
	row.add_child(_action("LOCATE", func() -> void: game._locate_diagnostic_room("%d,%d" % [member.origin.x, member.origin.y])))
	return card

static func _vitals_card(id: String, actor) -> Control:
	var card := _card(Color("3a6470"))
	card.name = "Vitals_" + id
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 6)
	card.add_child(rows)
	rows.add_child(_label(str(Architects.NAMES[id]), 18, Color("e2ecee")))
	if not actor.needs_air():
		rows.add_child(_label(str(actor.battery_status()), 15, DIM))
		return card
	rows.add_child(_vital_row("Tank", "%.0fs" % actor.tank_oxygen, float(actor.tank_oxygen), 60.0, TEAL))
	rows.add_child(_vital_row("Breath", "%.0fs" % actor.breath_oxygen, float(actor.breath_oxygen), 15.0, Color("79b8d9")))
	rows.add_child(_vital_row("Starvation", "%.0f of 90s" % actor.starvation, float(actor.starvation), 90.0, RED))
	return card

static func _vital_row(caption: String, value: String, amount: float, maximum: float, colour: Color) -> Control:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	var name_label := _label(caption, 15, DIM)
	name_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	name_label.custom_minimum_size.x = 100
	row.add_child(name_label)
	row.add_child(_bar(amount, maximum, colour))
	var value_label := _label(value, 15)
	value_label.autowrap_mode = TextServer.AUTOWRAP_OFF
	value_label.custom_minimum_size.x = 90
	row.add_child(value_label)
	return row

## Same forecast used by the HUD, including real recent deliveries and storage caps.
static func reserves(game, box: VBoxContainer, signature: String) -> void:
	if not _stale(box,signature): return
	_clear(box)
	box.add_child(_heading("RESERVES / NEXT CYCLE","Estimates include crew upkeep, learned bonuses and recent deliveries."))
	var forecast: Dictionary = game._simulate_room_economy(true,game.cycle+1)
	var net: Dictionary = game._displayed_cycle_delta(forecast)
	var tiles := GridContainer.new()
	tiles.name = "ResourceReadouts"
	tiles.columns = 3
	tiles.add_theme_constant_override("h_separation",12)
	tiles.add_theme_constant_override("v_separation",12)
	box.add_child(tiles)
	for id in game.BASE_STORAGE_CAPACITY:
		if not game.inspected_resource.is_empty() and game.inspected_resource != id: continue
		var tile := Widgets.resource_tile(str(id),int(game.resources.get(id,0)),int(net.get(id,0)))
		tile.name = "Reserve_"+str(id)
		tile.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		tile.get_child(0).get_node("Amount").text = "%d / %d" % [int(game.resources.get(id,0)),game._get_resource_capacity(str(id))]
		tiles.add_child(tile)
		var inspect := _action("ROOM CONTRIBUTIONS",func() -> void:
			game.inspected_resource = str(id)
			game._refresh_archive()
			var focus = box.find_child("DisclosureHeader",true,false)
			if focus != null: focus.grab_focus.call_deferred())
		inspect.name = "ResourceContributions"
		tile.get_child(0).add_child(inspect)
	if not game.inspected_resource.is_empty():
		box.add_child(_action("SHOW ALL RESERVES",func() -> void:
			game.inspected_resource = ""
			game._refresh_archive()
			var focus = box.find_child("ResourceContributions",true,false)
			if focus != null: focus.grab_focus.call_deferred()))
	var notes := RichTextLabel.new()
	notes.bbcode_enabled = true
	notes.fit_content = true
	notes.scroll_active = false
	if not game.inspected_resource.is_empty():
		notes.text = game._reserve_forecast(game.inspected_resource,int(net.get(game.inspected_resource,0)))+"\n"+"\n".join(game._resource_contribution_lines(game.inspected_resource,forecast))
	else:
		var lines: Array[String] = [preload("res://scripts/station_ui_insights.gd").power_balance(game,forecast),preload("res://scripts/station_ui_insights.gd").power_demand(game)]
		for id in game.BASE_STORAGE_CAPACITY: lines.append(game._reserve_forecast(str(id),int(net.get(id,0))))
		notes.text = "\n\n".join(lines)
	notes.add_theme_font_size_override("normal_font_size",16)
	notes.meta_clicked.connect(game._locate_diagnostic_room)
	box.add_child(Widgets.disclosure("FORECAST / CONTRIBUTIONS",notes,not game.inspected_resource.is_empty()))
