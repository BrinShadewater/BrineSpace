extends RefCounted
## The tooltip over a placed room in the station view (owner playtest, Sept 29): its name, whether it is
## working, and what it gives and takes each cycle with the resource icons the HUD and cards use. The grid
## sets a "room:x,y" marker as its tooltip text and builds this panel when Godot asks for the tooltip.

const DraftCard = preload("res://scripts/draft_card.gd")
const Rooms = preload("res://scripts/room_database.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
const GREEN := Color("7fd6a6")
const AMBER := Color("efb777")
const RED := Color("ef987c")
const DIM := Color("8fa9b3")

static func marker(cell: Vector2i) -> String:
	return "room:%d,%d" % [cell.x, cell.y]

static func cell_from(text: String) -> Vector2i:
	if not text.begins_with("room:"): return Vector2i(-1, -1)
	var parts := text.trim_prefix("room:").split(",")
	if parts.size() != 2 or not parts[0].is_valid_int() or not parts[1].is_valid_int(): return Vector2i(-1, -1)
	return Vector2i(int(parts[0]), int(parts[1]))

# [text, colour] for the status line, or an empty array for a room with no working state to report.
static func status(game, cell: Vector2i, room: Dictionary) -> Array:
	if room.get("suspended", false): return ["SUSPENDED", AMBER]
	var reason := str(game.offline_reasons.get(cell, ""))
	if not reason.is_empty() and reason != "FUNCTIONING": return ["OFFLINE  //  " + reason, RED]
	if game.powered_room_cells.has(cell): return ["FUNCTIONING", GREEN]
	if room.get("consumption", {}).is_empty() and room.get("production", {}).is_empty(): return []
	return ["WAITING FOR THE NEXT CYCLE", DIM]

static func build(game, cell: Vector2i) -> Control:
	var room: Dictionary = game.occupied.get(cell, {})
	if room.is_empty(): return null
	var accent: Color = Rooms.room_color(str(room.get("id", "")))
	var panel := PanelContainer.new()
	panel.name = "RoomTooltip"
	var style := StyleBoxFlat.new()
	style.bg_color = Color("0b151c")
	style.border_color = DraftCard.muted(accent)
	style.set_border_width_all(1)
	style.set_corner_radius_all(8)
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	panel.add_theme_stylebox_override("panel", style)
	var rows := VBoxContainer.new()
	rows.add_theme_constant_override("separation", 6)
	panel.add_child(rows)
	var title := Label.new()
	title.text = str(room.get("display_name", room.get("id", "Room")))
	title.add_theme_font_size_override("font_size", 18)
	title.add_theme_color_override("font_color", DraftCard.muted_bright(accent))
	rows.add_child(title)
	var state := status(game, cell, room)
	if not state.is_empty():
		var status_label := Label.new()
		status_label.name = "Status"
		status_label.text = str(state[0])
		status_label.add_theme_font_size_override("font_size", 14)
		status_label.add_theme_color_override("font_color", state[1])
		rows.add_child(status_label)
	var flow := RichTextLabel.new()
	flow.name = "Flow"
	flow.bbcode_enabled = true
	flow.fit_content = true
	flow.scroll_active = false
	flow.autowrap_mode = TextServer.AUTOWRAP_OFF
	flow.custom_minimum_size.x = 190
	flow.add_theme_font_size_override("normal_font_size", 16)
	flow.add_theme_color_override("default_color", Color("dff7ee"))
	flow.text = "\n".join(PackedStringArray(DraftCard.rule_lines(room)))
	rows.add_child(flow)
	TitleSettings.apply_menu_text(panel)
	return panel
