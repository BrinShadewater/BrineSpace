extends RefCounted
## Resource icon artwork and colours, shared by the HUD, draft cards, codex and Meta Progression
## (owner playtest, Sept 17: resources should read with the same icon and colour everywhere).

const PATHS := {
	"metal": "res://Brine icons/icons_64/resource_icon_metal_chunk.png",
	"power": "res://Brine icons/icons_64/resource_icon_power_lightning.png",
	"oxygen": "res://Brine icons/icons_64/resource_icon_o2.png",
	"water": "res://Brine icons/icons_64/resource_icon_water_drop.png",
	"food": "res://Brine icons/icons_64/resource_icon_leaf_food.png",
	"data": "res://Brine icons/icons_64/resource_icon_data.png",
	"archived_data": "res://Brine icons/icons_64/resource_icon_data.png",
	"biomass": "res://Brine icons/icons_64/resource_icon_biomass_growth.png",
	"rare_minerals": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"rare": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"integrity": "res://Brine icons/icons_64/resource_icon_integrity.png",
	"crew": "res://Brine icons/icons_64/resource_icon_crew.png",
	"corruption": "res://Brine icons/icons_64/resource_icon_corruption.png",
	"anomaly": "res://Brine icons/icons_64/anomaly_icon_spiral.png",
	"orbit": "res://Brine icons/icons_64/orbit_icon_moon_asteroid.png",
}

# The HUD resource chip colours.
const COLORS := {
	"metal": "#b8c0c6", "power": "#f5c542", "oxygen": "#7fd4ff", "water": "#719bff",
	"food": "#f0903c", "data": "#4fd0e0", "archived_data": "#8fe8f2", "biomass": "#5fc46a",
	"rare_minerals": "#b07ff0", "rare": "#b07ff0", "integrity": "#9fd8b0", "crew": "#e6c6a0",
	"corruption": "#d95b63", "anomaly": "#c58af0", "orbit": "#9fb3c8",
}

static func icon(id: String, icon_size := 16) -> String:
	return "[img=%dx%d]%s[/img]" % [icon_size, icon_size, PATHS[id]] if PATHS.has(id) else ""

static func color(id: String) -> String:
	return str(COLORS.get(id, "#d8e6ea"))

static func display_name(id: String) -> String:
	return "Archived Data" if id == "archived_data" else ("Rare Minerals" if id == "rare" else id.replace("_", " ").capitalize())

# One amount with its icon and colour: "[img] Metal 6" or, with sign, "[img] +6 Metal".
static func amount(id: String, value: int, icon_size := 16, signed := false) -> String:
	var text := ("%+d %s" % [value, display_name(id)]) if signed else ("%s %d" % [display_name(id), value])
	return "%s [color=%s]%s[/color]" % [icon(id, icon_size), color(id), text]

# "[img]Metal 6, [img]Power 1" with each resource's icon and colour, as the draft cards show costs.
static func bbcode(values: Dictionary, icon_size := 16) -> String:
	if values.is_empty(): return "None"
	var parts := PackedStringArray()
	for key in values:
		parts.append(amount(str(key), int(values[key]), icon_size))
	return ", ".join(parts)

const WORDS := {
	"archived data": "archived_data", "rare minerals": "rare_minerals", "rare mineral": "rare_minerals",
	"metal": "metal", "power": "power", "oxygen": "oxygen", "water": "water", "food": "food",
	"data": "data", "biomass": "biomass", "integrity": "integrity",
}
static var _pattern: RegEx

# Adds icons and colours to resource amounts written in plain sentences, such as perk and
# synergy text: "Start each loop with +5 Metal." The amount and resource are coloured and the
# icon sits before them. Text must not already contain BBCode.
static func decorate(text: String, icon_size := 16) -> String:
	if _pattern == null:
		_pattern = RegEx.new()
		# The amount may sit before or after its resource ("+5 Metal", "WATER 30%"), but always on
		# the same line: a number ending one line was being pulled into the next line's resource
		# ("Stabilized: 1" then "Archived Data banked").
		_pattern.compile("(?i)([+-]?\\d+%?[ \\t]+)?\\b(archived data|rare minerals?|metal|power|oxygen|water|food|data|biomass|integrity)\\b([ \\t]+[+-]?\\d+%?)?")
	var result := ""
	var last := 0
	for found in _pattern.search_all(text):
		var id: String = WORDS[found.get_string(2).to_lower()]
		result += text.substr(last, found.get_start() - last)
		result += "%s [color=%s]%s[/color]" % [icon(id, icon_size), color(id), found.get_string()]
		last = found.get_end()
	return result + text.substr(last)
