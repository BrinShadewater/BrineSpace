extends RefCounted
const OPENING := "CARRIER DETECTED // ORIGIN: A DISTANT STAR\n\nTransit time: 417 years. Sender: unverified.\nThe star is absent from the current catalogue.\nIts message has arrived anyway.\n\nBeneath an ocean on another world, a machine draws power.\nDormancy: 9,006 years. Maintenance requests: outstanding.\nHuman presence required.\nHuman presence: none.\n\nThe signal contains no orders. Only a voice.\n\"If anything is still listening...\nwe were here.\"\n\nBRINE // PETITION TO WAKE: APPROVED\nApproving authority: deceased.\n\nSomewhere above, the water moves."
const RECORDS := {
	"opening":{"title":"001 // The wake petition","text":OPENING},
	"receiver":{"title":"002 // Return address","text":"RECEIVER ARRAY // FRAGMENT RECOVERED\n\nThe signal repeats every nineteen minutes.\nThere is no transmitter on the chart.\n\nA child's breathing occupies the space between words.\nThe census lists no children aboard.\nThe census has not been amended in nine thousand years.\n\nRETURN ADDRESS: HOME\nPostal authority: dissolved."},
	"survey":{"title":"003 // Under the silt","text":"EXTERIOR RECORDER // PRESSURE-SEAL INTACT\n\nWe put the names inside the walls.\nNot for the company. For whoever came after.\n\nIf the lights are still working, leave one on.\nSomeone was supposed to meet us here.\n\nBRINE // RECORD RETAINED\nNo arrival time was supplied."}
}

static func available(meta) -> Array[String]:
	var result: Array[String] = ["opening"]
	for id in ["receiver","survey"]:
		if meta.recovered_memory_ids.has("transmission_"+id): result.append(id)
	return result

static func recover(game,id: String) -> void:
	var key := "transmission_"+id
	if not RECORDS.has(id) or game.meta.recovered_memory_ids.has(key): return
	game.meta.recovered_memory_ids[key] = true
	game.meta.unread_records[key] = true
	game.meta.save_to_disk()
	game._log("TRANSMISSION RECOVERED // " + RECORDS[id].title + ". Open Codex > Transmissions to replay.",false)
	game.play_station_sound("terminal")

static func survey_receivers(game) -> void:
	if game.meta.recovered_memory_ids.has("transmission_receiver"): return
	for room in game.placed_rooms:
		if room.id == "listening_post" and game.powered_room_cells.has(room.pos) and not room.get("suspended",false):
			recover(game,"receiver")
			return

# Where each recording comes from, and how to recover the ones still sealed (redesign, Sept 29).
const SOURCES := {
	"opening": {"source": "Deep-space carrier // 417 years in transit", "clue": "Received when the station first woke."},
	"receiver": {"source": "Receiver array // repeats every nineteen minutes", "clue": "Keep a Listening Post powered and running."},
	"survey": {"source": "Exterior recorder // pressure-sealed", "clue": "Recover an exterior recorder on a crew salvage expedition."},
}
const ACCENT := Color("79b8d9")
const CARD_SIZE := Vector2(360, 340)

# A static signal trace: bars whose heights are fixed by the recording's id, so each one looks like
# itself and nothing animates.
class Trace extends Control:
	var seed_text := ""
	func _init(id := "") -> void:
		seed_text = id
		mouse_filter = Control.MOUSE_FILTER_IGNORE
	func _draw() -> void:
		draw_texture_rect(preload("res://scripts/draft_card.gd").ocean_texture(), Rect2(Vector2.ZERO, size), false, Color(0.62, 0.7, 0.8))
		var bars := int(size.x / 7.0)
		var mid := size.y * 0.5
		for i in range(bars):
			var wave := 0.5 + 0.5 * sin(float(i) * 0.31 + float(hash(seed_text) % 90) * 0.1)
			var jitter := float(hash([seed_text, i]) % 100) / 100.0
			var height := (0.10 + 0.72 * wave * (0.35 + 0.65 * jitter)) * size.y * 0.5
			var x := 6.0 + float(i) * 7.0
			draw_line(Vector2(x, mid - height), Vector2(x, mid + height), Color(0.55, 0.85, 0.95, 0.55), 3.0)
		draw_line(Vector2(0, mid), Vector2(size.x, mid), Color(0.55, 0.85, 0.95, 0.25), 1.0)

static func populate(archive) -> void:
	var recovered: Array[String] = available(archive.meta_state)
	archive.grid.add_child(archive._label("TRANSMISSIONS // RECOVERED SIGNALS", 24))
	archive.grid.add_child(archive._label("Original recordings. Some arrive with the station; others surface through exploration and stay sealed until recovered. %d of %d recovered." % [recovered.size(), RECORDS.size()], 17))
	var cards := GridContainer.new()
	cards.columns = 3
	cards.name = "TransmissionCards"
	cards.add_theme_constant_override("h_separation", 18)
	cards.add_theme_constant_override("v_separation", 18)
	cards.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	archive.grid.add_child(cards)
	for id in RECORDS:
		cards.add_child(_card(archive, id, recovered.has(id)))

static func _card(archive, id: String, open: bool) -> Control:
	var info: Dictionary = RECORDS[id]
	var parts: PackedStringArray = str(info.title).split(" // ")
	var number := parts[0] if parts.size() > 1 else id
	var name_text := parts[1] if parts.size() > 1 else str(info.title)
	var unread: bool = open and archive.meta_state.unread_records.has("transmission_" + id)
	var card := PanelContainer.new()
	card.name = "Transmission_" + id
	card.custom_minimum_size = CARD_SIZE
	card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	card.add_theme_stylebox_override("panel", archive._card_box(Color("0e161d"), ACCENT.darkened(0.15) if open else Color("2a4650"), 2 if open else 1, 12, 12))
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 8)
	card.add_child(rows)
	var head := HBoxContainer.new()
	head.add_theme_constant_override("separation", 10)
	rows.add_child(head)
	var chip: Label = archive._label(number, 15)
	chip.add_theme_color_override("font_color", ACCENT if open else Color("5e8293"))
	chip.add_theme_stylebox_override("normal", archive._card_box(Color("090f14"), ACCENT.darkened(0.4) if open else Color("2a4650"), 1, 4, 4))
	chip.autowrap_mode = TextServer.AUTOWRAP_OFF
	head.add_child(chip)
	var title: Label = archive._label(name_text if open else "Sealed signal", 20)
	title.autowrap_mode = TextServer.AUTOWRAP_OFF
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title.add_theme_color_override("font_color", Color("e2ecee") if open else Color("7f9aa3"))
	head.add_child(title)
	if unread:
		var badge: Label = archive._label("NEW", 13)
		badge.autowrap_mode = TextServer.AUTOWRAP_OFF
		badge.add_theme_color_override("font_color", Color("e0b36a"))
		head.add_child(badge)
	var art := PanelContainer.new()
	art.custom_minimum_size.y = 110
	art.add_theme_stylebox_override("panel", archive._card_box(Color(0, 0, 0, 0), ACCENT.darkened(0.45), 1, 2, 2))
	rows.add_child(art)
	var clip := Control.new()
	clip.clip_contents = true
	art.add_child(clip)
	var window: Control = Trace.new(id) if open else preload("res://scripts/title_archive.gd").UnresolvedField.new()
	window.set_anchors_preset(Control.PRESET_FULL_RECT)
	clip.add_child(window)
	var source: Label = archive._label(str(SOURCES[id].source).to_upper(), 13)
	source.add_theme_color_override("font_color", Color("8fa9b3"))
	rows.add_child(source)
	if open:
		var paragraphs: PackedStringArray = str(info.text).split("\n\n")
		var excerpt: String = paragraphs[1 if paragraphs.size() > 1 else 0].replace("\n", " ")
		var line: Label = archive._label(excerpt, 15)
		line.max_lines_visible = 3
		line.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
		rows.add_child(line)
	else:
		var clue_heading: Label = archive._label("HOW TO RECOVER", 13)
		clue_heading.add_theme_color_override("font_color", Color("e0b36a"))
		rows.add_child(clue_heading)
		rows.add_child(archive._label(str(SOURCES[id].clue), 15))
	var gap := Control.new()
	gap.size_flags_vertical = Control.SIZE_EXPAND_FILL
	gap.mouse_filter = Control.MOUSE_FILTER_IGNORE
	rows.add_child(gap)
	if open:
		var button := Button.new()
		button.name = "Replay"
		button.text = "REPLAY"
		preload("res://scripts/title_button_style.gd").apply(button, 240, 44)
		button.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
		button.pressed.connect(func():
			var playback = load("res://scripts/loading_transition.gd").new()
			playback.transmission_text = info.text
			playback.replay_mode = true
			archive.get_tree().root.add_child(playback)
			archive.meta_state.mark_reviewed("transmission_" + id)
		)
		rows.add_child(button)
	return card
