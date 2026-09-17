extends RefCounted
## Resource icon artwork, shared by the HUD, draft cards and the codex (owner playtest, Sept 17:
## codex cards should show costs with the same icons and colours as the game).

const PATHS := {
	"metal": "res://Brine icons/icons_64/resource_icon_metal_chunk.png",
	"power": "res://Brine icons/icons_64/resource_icon_power_lightning.png",
	"oxygen": "res://Brine icons/icons_64/resource_icon_o2.png",
	"water": "res://Brine icons/icons_64/resource_icon_water_drop.png",
	"food": "res://Brine icons/icons_64/resource_icon_leaf_food.png",
	"data": "res://Brine icons/icons_64/resource_icon_data.png",
	"biomass": "res://Brine icons/icons_64/resource_icon_biomass_growth.png",
	"rare_minerals": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"rare": "res://Brine icons/icons_64/resource_icon_rare_minerals.png",
	"integrity": "res://Brine icons/icons_64/resource_icon_integrity.png",
	"crew": "res://Brine icons/icons_64/resource_icon_crew.png",
	"corruption": "res://Brine icons/icons_64/resource_icon_corruption.png",
	"anomaly": "res://Brine icons/icons_64/anomaly_icon_spiral.png",
	"orbit": "res://Brine icons/icons_64/orbit_icon_moon_asteroid.png",
}

# "[img]Metal 6, [img]Power 1" with each resource's icon, as the draft cards show costs.
static func bbcode(values: Dictionary, icon_size := 16) -> String:
	if values.is_empty(): return "None"
	var parts := PackedStringArray()
	for key in values:
		var id := str(key)
		var icon := "[img=%dx%d]%s[/img] " % [icon_size, icon_size, PATHS[id]] if PATHS.has(id) else ""
		parts.append("%s%s %d" % [icon, id.replace("_", " ").capitalize(), int(values[key])])
	return ", ".join(parts)
