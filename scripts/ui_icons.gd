extends RefCounted
## Shared whole-path icon registry; PNG loading also works before editor imports.
const PATHS := {
	"metal": "res://brineui/badge-icons-v3/icons/metal.png",
	"power": "res://brineui/badge-icons-v3/icons/power.png",
	"oxygen": "res://brineui/badge-icons-v3/icons/oxygen.png",
	"water": "res://brineui/badge-icons-v3/icons/water.png",
	"food": "res://brineui/badge-icons-v3/icons/food.png",
	"data": "res://brineui/badge-icons-v3/icons/data.png",
	"biomass": "res://brineui/badge-icons-v3/icons/biomass.png",
	"rare_minerals": "res://brineui/badge-icons-v3/icons/rare_minerals.png",
	"integrity": "res://brineui/badge-icons-v3/icons/integrity.png",
	"crew": "res://brineui/badge-icons-v3/icons/crew.png",
	"corruption": "res://brineui/badge-icons-v3/icons/corruption.png",
	"archived_data": "res://brineui/hull-ui-v2/icons/archived_data.png",
	"anomaly": "res://brineui/badge-icons-v3/icons/anomaly.png",
	"orbit": "res://brineui/badge-icons-v3/icons/orbit.png",
	"fire": "res://brineui/badge-icons-v3/icons/fire.png",
	"freeze": "res://brineui/badge-icons-v3/icons/freeze.png",
	"sensor": "res://brineui/badge-icons-v3/icons/sensor.png",
	"repair": "res://brineui/badge-icons-v3/icons/repair.png",
	"scrap": "res://brineui/badge-icons-v3/icons/scrap.png",
	"assign_workplace": "res://brineui/badge-icons-v3/icons/assign_workplace.png",
	"focus_room": "res://brineui/badge-icons-v3/icons/focus_room.png",
	"doors_open": "res://brineui/badge-icons-v3/icons/doors_open.png",
	"doors_closed": "res://brineui/badge-icons-v3/icons/doors_closed.png",
	"hull_intact": "res://brineui/badge-icons-v3/icons/hull_intact.png",
	"fan": "res://brineui/hull-ui-v2/icons/fan.png",
	"row": "res://brineui/hull-ui-v2/icons/row.png",
	"show_hand": "res://brineui/hull-ui-v2/icons/show_hand.png",
	"hide_hand": "res://brineui/hull-ui-v2/icons/hide_hand.png",
	"frame_on": "res://brineui/hull-ui-v2/icons/frame_on.png",
	"frame_off": "res://brineui/hull-ui-v2/icons/frame_off.png",
	"reroll": "res://brineui/hull-ui-v2/icons/reroll.png",
	"health": "res://brineui/badge-icons-v3/icons/health.png",
	"fatigue": "res://brineui/badge-icons-v3/icons/fatigue.png",
	"hunger": "res://brineui/badge-icons-v3/icons/hunger.png",
	"activity": "res://brineui/badge-icons-v3/icons/activity.png",
	"assigned_room": "res://brineui/badge-icons-v3/icons/assigned_room.png",
	"idle": "res://brineui/badge-icons-v3/icons/idle.png",
	"working": "res://brineui/badge-icons-v3/icons/working.png",
	"unassigned": "res://brineui/badge-icons-v3/icons/unassigned.png",
	"resting": "res://brineui/badge-icons-v3/icons/resting.png",
	"archive": "res://brineui/badge-icons-v3/icons/archive.png",
	"diagnostics": "res://brineui/badge-icons-v3/icons/diagnostics.png",
	"journal": "res://brineui/badge-icons-v3/icons/journal.png",
	"menu": "res://brineui/badge-icons-v3/icons/menu.png",
	"settings": "res://brineui/badge-icons-v3/icons/settings.png",
	"search": "res://brineui/badge-icons-v3/icons/search.png",
	"filter": "res://brineui/badge-icons-v3/icons/filter.png",
	"close": "res://brineui/badge-icons-v3/icons/close.png",
	"back": "res://brineui/badge-icons-v3/icons/back.png",
	"expand": "res://brineui/badge-icons-v3/icons/expand.png",
	"collapse": "res://brineui/badge-icons-v3/icons/collapse.png",
	"locked": "res://brineui/badge-icons-v3/icons/locked.png",
	"unlocked": "res://brineui/badge-icons-v3/icons/unlocked.png",
	"pause": "res://brineui/badge-icons-v3/icons/pause.png",
	"play": "res://brineui/badge-icons-v3/icons/play.png",
	"confirm": "res://brineui/badge-icons-v3/icons/confirm.png",
	"cancel": "res://brineui/badge-icons-v3/icons/cancel.png",
	"info": "res://brineui/badge-icons-v3/icons/info.png",
	"warning": "res://brineui/badge-icons-v3/icons/warning.png",
	"help": "res://brineui/badge-icons-v3/icons/help.png",
	"rare": "res://brineui/badge-icons-v3/icons/rare_minerals.png",
}
static var _textures: Dictionary = {}

static func texture(id: String) -> Texture2D:
	if _textures.has(id): return _textures[id]
	if not PATHS.has(id): return null
	var image := Image.new()
	if image.load_png_from_buffer(FileAccess.get_file_as_bytes(PATHS[id])) != OK: return null
	var result := ImageTexture.create_from_image(image)
	_textures[id] = result
	return result

## Theme glyphs have a fixed layout extent; resample from the master, not a small export.
static func glyph(id: String, side := 20) -> Texture2D:
	var key := "%s:%d" % [id, side]
	if _textures.has(key): return _textures[key]
	var master := texture(id)
	if master == null: return null
	var source := master.get_image()
	source.resize(side, side, Image.INTERPOLATE_LANCZOS)
	var result := ImageTexture.create_from_image(source)
	_textures[key] = result
	return result

static func apply(button: Button, id: String, side := 18) -> void:
	button.icon = texture(id)
	button.expand_icon = true
	button.add_theme_constant_override("icon_max_width", side)
	button.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	button.set_meta("hull_icon", id)

