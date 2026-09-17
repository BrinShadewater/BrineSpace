extends RefCounted
## Room Layout Studio view options (owner playtest): toggles, zoom and the scale character
## survive room and rotation changes, closing the Studio and relaunching. Layout data such
## as Free placement stays in the layout itself.
##
## Only the player's own Studio writes the file, beside the real layout store. Fixtures that
## redirect Store.path keep options in memory for their run, so one test run can never
## change where the next one starts; a test that checks persistence sets `path` itself.

const Store = preload("res://scripts/room_layout_store.gd")
const PLAYER_STORE := "user://room_layouts.json"
const SECTION := "studio"

static var path := ""
static var session: Dictionary = {}

static func file_path() -> String:
	if not path.is_empty(): return path
	return Store.path + ".studio.cfg" if Store.path == PLAYER_STORE else ""

static func load_values() -> Dictionary:
	var values := session.duplicate()
	var file := file_path()
	var config := ConfigFile.new()
	if file.is_empty() or config.load(file) != OK or not config.has_section(SECTION): return values
	for key in config.get_section_keys(SECTION): values[key] = config.get_value(SECTION, key)
	return values

# Written only when the user changes a control, never on open or close.
static func save_value(key: String, value: Variant) -> void:
	session[key] = value
	var file := file_path()
	if file.is_empty(): return
	var config := ConfigFile.new()
	config.load(file)
	if config.get_value(SECTION, key, null) == value: return
	config.set_value(SECTION, key, value)
	config.save(file)
