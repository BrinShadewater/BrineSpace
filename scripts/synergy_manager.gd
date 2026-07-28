extends RefCounted
class_name SynergyManager

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
	}
]

static func evaluate(placed_rooms: Array, occupied: Dictionary, discovered: Dictionary) -> Dictionary:
	var active := {}
	var newly_discovered := []
	for synergy in SYNERGIES:
		var found := _has_adjacent_pair(synergy["rooms"], occupied)
		if found:
			active[synergy["id"]] = synergy
			if not discovered.has(synergy["id"]):
				newly_discovered.append(synergy)
	for room in placed_rooms:
		if room["id"] == "cryo_chamber" and _has_adjacent_tag(room["pos"], occupied, "medical"):
			var safe_wake := _get_synergy("safe_wake_protocol")
			active[safe_wake["id"]] = safe_wake
			if not discovered.has(safe_wake["id"]):
				newly_discovered.append(safe_wake)
	return {"active": active, "new": newly_discovered}

static func cycle_bonus(active_synergies: Dictionary) -> Dictionary:
	var bonus := {}
	for synergy in active_synergies.values():
		for key in synergy["bonus"]:
			bonus[key] = bonus.get(key, 0) + synergy["bonus"][key]
	return bonus

static func all_synergies() -> Array:
	return SYNERGIES

static func _has_adjacent_pair(room_ids: Array, occupied: Dictionary) -> bool:
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
				return true
	return false

static func _has_adjacent_tag(pos: Vector2i, occupied: Dictionary, tag: String) -> bool:
	for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
		var neighbor_pos: Vector2i = pos + offset
		if occupied.has(neighbor_pos) and occupied[neighbor_pos].get("tags", []).has(tag):
			return true
	return false

static func _get_synergy(id: String) -> Dictionary:
	for synergy in SYNERGIES:
		if synergy["id"] == id:
			return synergy
	return {}
