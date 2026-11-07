extends Node2D
## What every room gives and takes each cycle, drawn as resource icons over the room (owner playtest, Sept 30:
## a hotkey toggle in the style of Civ 6's yield view). It lives in the grid's coordinates, so panning and
## zooming move it for free, and it redraws only when the station, its power or the zoom changes.

const ResourceIcons = preload("res://scripts/resource_icons.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
const GIVES := Color("7fd6a6")
const TAKES := Color("efb777")
const PILL := Color(0.03, 0.07, 0.09, 0.78)

var host
var _signature := -1
var _textures: Dictionary = {}
var _pill := StyleBoxFlat.new()

func _init() -> void:
	name = "YieldOverlay"
	z_index = 4
	_pill.bg_color = PILL
	_pill.set_corner_radius_all(6)
	_pill.content_margin_left = 6
	_pill.content_margin_right = 6
	_pill.content_margin_top = 3
	_pill.content_margin_bottom = 3

func _process(_delta: float) -> void:
	var on: bool = TitleSettings.resource_overlay
	if visible != on: visible = on
	if not on or host == null: return
	var signature := state_signature()
	if signature != _signature:
		_signature = signature
		queue_redraw()

# Everything the drawing reads: the rooms, whether each works, and the zoom.
func state_signature() -> int:
	var main = host._get_main()
	if main == null: return 0
	var parts: Array = [host._cell_size(), main.placed_rooms.size(), main.powered_room_cells.size()]
	for room in main.placed_rooms:
		parts.append([room.pos, room.get("id", ""), room.get("production", {}), room.get("consumption", {}), room.get("suspended", false), main.powered_room_cells.has(room.pos)])
	return hash(parts)

# The lines to show for a room: [[resource id, amount, is_gain]], gains first. Empty for a room that only
# holds or supports (corridors, storage).
static func lines_for(room: Dictionary) -> Array:
	var result: Array = []
	var production: Dictionary = room.get("production", {})
	if str(room.get("id", "")) == "heat_recovery": production = {"power": 4}
	for key in production:
		result.append([str(key), int(production[key]), true])
	var consumption: Dictionary = room.get("consumption", {})
	for key in consumption:
		result.append([str(key), int(consumption[key]), false])
	return result

func _texture(id: String) -> Texture2D:
	if not _textures.has(id):
		var path: String = ResourceIcons.PATHS.get(id, "")
		_textures[id] = load(path) if not path.is_empty() else null
	return _textures[id]

func _draw() -> void:
	if host == null: return
	var main = host._get_main()
	if main == null: return
	var size: float = host._cell_size()
	var icon := clampf(size * 0.10, 8.0, 46.0)
	var font: Font = ThemeDB.fallback_font
	var font_size := int(icon * 0.95)
	for room in main.placed_rooms:
		var lines := lines_for(room)
		if lines.is_empty(): continue
		var footprint: Vector2i = room.get("size", Vector2i.ONE)
		var centre := (Vector2(room.pos) + Vector2(footprint) * 0.5) * size
		var working: bool = main.powered_room_cells.has(room.pos) and not room.get("suspended", false)
		var fade := 1.0 if working else 0.55
		var gains: Array = lines.filter(func(line): return line[2])
		var costs: Array = lines.filter(func(line): return not line[2])
		var rows: Array = []
		if not gains.is_empty(): rows.append(gains)
		if not costs.is_empty(): rows.append(costs)
		var row_height := icon + 8.0
		var top := centre.y - row_height * rows.size() * 0.5
		for row in rows:
			var widths: Array = []
			var total := 0.0
			for line in row:
				var text := "%s%d" % ["+" if line[2] else "-", line[1]]
				var width := icon + 4.0 + font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
				widths.append(width)
				total += width + 8.0
			total -= 8.0
			var x := centre.x - total * 0.5
			draw_style_box(_pill, Rect2(Vector2(x - 6.0, top - 1.0), Vector2(total + 12.0, row_height)))
			for i in range(row.size()):
				var line: Array = row[i]
				var tint := GIVES if line[2] else TAKES
				var texture := _texture(str(line[0]))
				if texture != null:
					draw_texture_rect(texture, Rect2(Vector2(x, top + (row_height - icon) * 0.5 - 1.0), Vector2(icon, icon)), false, Color(1, 1, 1, fade))
				var label := "%s%d" % ["+" if line[2] else "-", line[1]]
				draw_string(font, Vector2(x + icon + 4.0, top + row_height * 0.5 + font_size * 0.34), label, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, Color(tint.r, tint.g, tint.b, fade))
				x += float(widths[i]) + 8.0
			top += row_height
