extends RefCounted
class_name SynergyManager

const RoomDatabaseScript := preload("res://scripts/room_database.gd")

const SYNERGIES := [
	{
		"id": "closed_air_loop",
		"name": "Closed Air Loop",
		"rooms": ["hydroponics_bay", "life_support"],
		"bonus": {"oxygen": 1},
		"effect": "+1 Oxygen per cycle while both rooms are adjacent and connected.",
		"message": "BRINE recovered a life-support pattern: Closed Air Loop."
	},
	{
		"id": "green_commons",
		"name": "Green Commons",
		"rooms": ["hydroponics_bay", "crew_hab"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while living plants are adjacent to crew quarters.",
		"message": "Crew morale improves near living plants."
	},
	{
		"id": "industrial_chain",
		"name": "Industrial Chain",
		"rooms": ["mining_drone_bay", "ore_refinery"],
		"bonus": {"metal": 2},
		"effect": "+2 Metal per cycle while drone mining feeds an adjacent refinery.",
		"message": "Ore processing route optimized."
	},
	{
		"id": "stable_power_flow",
		"name": "Stable Power Flow",
		"rooms": ["reactor", "battery_array"],
		"bonus": {"power": 1},
		"effect": "+1 Power per cycle while a Battery Array buffers an adjacent Reactor.",
		"message": "Power surge buffering stabilized."
	},
	{
		"id": "research_pipeline",
		"name": "Research Pipeline",
		"rooms": ["research_lab", "data_archive"],
		"bonus": {"data": 2},
		"effect": "+2 Data per cycle while a Research Lab is adjacent to a Data Archive.",
		"message": "Data indexing increased research yield."
	},
	{
		"id": "safe_wake_protocol",
		"name": "Safe Wake Protocol",
		"rooms": ["cryo_chamber", "life_support"],
		"bonus": {},
		"effect": "Cryo survivors wake faster and more safely with adjacent medical or life support.",
		"message": "Cryo recovery protocol restored."
	},
	{
		"id": "containment_sector",
		"name": "Containment Sector",
		"rooms": ["xeno_lab", "quarantine_cell"],
		"bonus": {},
		"effect": "Reduces future anomaly spread risk when quarantine borders anomaly research.",
		"message": "Anomaly spread contained."
	},
	{
		"id": "crew_commons",
		"name": "Crew Commons",
		"rooms": ["crew_hab", "crew_lounge"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while crew quarters share a connected commons.",
		"message": "Crew schedules converge around a shared commons."
	},
	{
		"id": "field_clinic",
		"name": "Field Clinic",
		"rooms": ["crew_hab", "med_bay"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while medical care is embedded in a crew sector.",
		"message": "A field clinic comes online beside crew quarters."
	},
	{
		"id": "shielded_reactor",
		"name": "Shielded Reactor",
		"rooms": ["reactor", "shield_generator"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while shielding contains reactor stress.",
		"message": "Reactor stress falls inside the shield envelope."
	},
	{
		"id": "signal_command",
		"name": "Signal Command",
		"rooms": ["radio_lab", "command_center"],
		"bonus": {"data": 2},
		"effect": "+2 Data per cycle while command systems decode radio traffic.",
		"message": "Command begins resolving patterns in the orbital static."
	},
	{
		"id": "drone_foundry",
		"name": "Drone Foundry",
		"rooms": ["salvage_drone_bay", "maintenance_bay"],
		"bonus": {"metal": 1, "integrity": 1},
		"effect": "+1 Metal and +1 Integrity per cycle from recovered drone parts.",
		"message": "Salvage parts feed directly into station maintenance."
	},
	{
		"id": "living_circuit",
		"name": "Living Circuit",
		"rooms": ["bio_lab", "holographic_core"],
		"bonus": {"biomass": 1, "data": 1},
		"effect": "+1 Biomass and +1 Data per cycle while living samples inform BRINE's models.",
		"message": "Organic telemetry begins teaching the holographic core."
	},
	{
		"id": "biodome_atmosphere",
		"name": "Biodome Atmosphere",
		"rooms": ["biodome", "life_support"],
		"bonus": {"oxygen": 2},
		"effect": "+2 Oxygen per cycle while life support circulates the biodome canopy.",
		"message": "The biodome canopy joins the station air loop."
	},
	{
		"id": "core_relay",
		"name": "Core Relay",
		"rooms": ["brine_core", "command_center"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while command telemetry routes through BRINE.",
		"message": "BRINE accepts the command center as a trusted relay."
	},
	{
		"id": "logistics_spine",
		"name": "Logistics Spine",
		"rooms": ["storage_bay", "corridor"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while storage opens directly onto a routing corridor.",
		"message": "Material traffic stabilizes along a logistics spine."
	},
	{
		"id": "medical_network",
		"name": "Medical Network",
		"rooms": ["med_center", "med_office"],
		"bonus": {"data": 1, "integrity": 1},
		"effect": "+1 Data and +1 Integrity per cycle from coordinated medical telemetry.",
		"message": "Medical records begin predicting station failures."
	}
]

static func evaluate(placed_rooms: Array, occupied: Dictionary, discovered: Dictionary) -> Dictionary:
	var active := {}
	var newly_discovered := []
	var links := []
	var seen_links := {}
	for synergy in SYNERGIES:
		var pairs := _find_adjacent_pairs(synergy["rooms"], occupied)
		for pair in pairs:
			_add_link(links, seen_links, synergy, pair)
		if not pairs.is_empty():
			active[synergy["id"]] = synergy
			if not discovered.has(synergy["id"]):
				newly_discovered.append(synergy)
	for room in placed_rooms:
		if room["id"] != "cryo_chamber":
			continue
		var safe_wake := _get_synergy("safe_wake_protocol")
		for neighbor_pos in _adjacent_tagged_cells(room["pos"], occupied, "medical"):
			_add_link(links, seen_links, safe_wake, [room["pos"], neighbor_pos])
			active[safe_wake["id"]] = safe_wake
			if not discovered.has(safe_wake["id"]) and not newly_discovered.has(safe_wake):
				newly_discovered.append(safe_wake)
	return {"active": active, "new": newly_discovered, "links": links}

static func cycle_bonus(active_links) -> Dictionary:
	var bonus := {}
	var sources: Array = active_links.values() if typeof(active_links) == TYPE_DICTIONARY else active_links
	for link in sources:
		for key in link.get("bonus", {}):
			bonus[key] = bonus.get(key, 0) + link["bonus"][key]
	return bonus

static func all_synergies() -> Array:
	return SYNERGIES

static func _find_adjacent_pairs(room_ids: Array, occupied: Dictionary) -> Array:
	var pairs := []
	var seen := {}
	for pos in occupied:
		var room: Dictionary = occupied[pos]
		if room["id"] != room_ids[0] and room["id"] != room_ids[1]:
			continue
		for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var neighbor_pos: Vector2i = pos + offset
			if not occupied.has(neighbor_pos):
				continue
			var neighbor: Dictionary = occupied[neighbor_pos]
			if room["id"] != neighbor["id"] and room_ids.has(neighbor["id"]):
				if not _rooms_connected(room, neighbor, offset):
					continue
				var key := _cell_pair_key(pos, neighbor_pos)
				if not seen.has(key):
					seen[key] = true
					pairs.append([pos, neighbor_pos])
	return pairs

static func _adjacent_tagged_cells(pos: Vector2i, occupied: Dictionary, tag: String) -> Array:
	var cells := []
	var room: Dictionary = occupied.get(pos, {})
	for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
		var neighbor_pos: Vector2i = pos + offset
		if occupied.has(neighbor_pos) and occupied[neighbor_pos].get("tags", []).has(tag) and _rooms_connected(room, occupied[neighbor_pos], offset):
			cells.append(neighbor_pos)
	return cells

static func _rooms_connected(room: Dictionary, neighbor: Dictionary, offset: Vector2i) -> bool:
	if room.is_empty() or neighbor.is_empty():
		return false
	var side := _side_from_offset(offset)
	var opposite := _opposite_side(side)
	return _room_doors(room).has(side) and _room_doors(neighbor).has(opposite)

static func _room_doors(room: Dictionary) -> Array:
	var layout: Dictionary = RoomDatabaseScript.get_layout(str(room.get("layout", "layout_05_cross")))
	var rotated: Array = []
	for side_value in layout.get("doors", []):
		rotated.append(_rotate_side(str(side_value), int(room.get("rotation", 0))))
	return rotated

static func _side_from_offset(offset: Vector2i) -> String:
	if offset == Vector2i.UP:
		return "north"
	if offset == Vector2i.RIGHT:
		return "east"
	if offset == Vector2i.DOWN:
		return "south"
	return "west"

static func _opposite_side(side: String) -> String:
	match side:
		"north":
			return "south"
		"east":
			return "west"
		"south":
			return "north"
		_:
			return "east"

static func _rotate_side(side: String, rotation_steps: int) -> String:
	var sides := ["north", "east", "south", "west"]
	var index := sides.find(side)
	if index < 0:
		return side
	return sides[(index + rotation_steps) % sides.size()]

static func _add_link(links: Array, seen_links: Dictionary, synergy: Dictionary, cells: Array) -> void:
	var key := "%s:%s" % [synergy["id"], _cell_pair_key(cells[0], cells[1])]
	if seen_links.has(key):
		return
	seen_links[key] = true
	var link := synergy.duplicate(true)
	link["cells"] = cells.duplicate()
	link["key"] = key
	links.append(link)

static func _cell_pair_key(a: Vector2i, b: Vector2i) -> String:
	var first := a
	var second := b
	if b.x < a.x or (b.x == a.x and b.y < a.y):
		first = b
		second = a
	return "%d,%d-%d,%d" % [first.x, first.y, second.x, second.y]

static func _get_synergy(id: String) -> Dictionary:
	for synergy in SYNERGIES:
		if synergy["id"] == id:
			return synergy
	return {}
