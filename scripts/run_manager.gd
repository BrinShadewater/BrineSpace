extends RefCounted
class_name RunManager
const TIME_SPEEDS := [1.0, 2.0, 4.0]

const RoomDatabaseScript := preload("res://scripts/room_database.gd")

const DOCTRINE_ORDER := ["industry", "biosphere", "science", "recovery", "anomaly"]
const DOCTRINES := {
	"industry": {
		"name": "Industrial Mandate",
		"short_name": "INDUSTRY",
		"color": "d8b84a",
		"description": "Power, extraction, storage, and hard station infrastructure.",
		"rooms": ["reactor", "battery_array", "mining_drone_bay", "salvage_drone_bay", "ore_refinery", "storage_bay", "maintenance_bay", "shield_generator", "tidal_condenser"],
		"mastery_bonus": {"metal": 2}
	},
	"biosphere": {
		"name": "Biosphere Protocol",
		"short_name": "BIOSPHERE",
		"color": "63bd72",
		"description": "Food, oxygen, biomass, and living station systems.",
		"rooms": ["hydroponics_bay", "life_support", "biodome", "bio_lab", "crew_hab", "crew_lounge", "mycelium_nursery", "tidal_condenser"],
		"mastery_bonus": {"food": 1, "oxygen": 1}
	},
	"science": {
		"name": "Signal Cartography",
		"short_name": "SCIENCE",
		"color": "55a6d8",
		"description": "Research, command telemetry, archives, and deep-space signals.",
		"rooms": ["research_lab", "data_archive", "radio_lab", "command_center", "holographic_core", "xeno_lab", "anomaly_lab", "gravity_loom"],
		"mastery_bonus": {"data": 1}
	},
	"recovery": {
		"name": "Crew Recovery",
		"short_name": "RECOVERY",
		"color": "d7814d",
		"description": "Habitats, medicine, cryonics, and survivor support.",
		"rooms": ["crew_hab", "crew_lounge", "cryo_chamber", "clone_lab", "med_bay", "med_center", "med_office", "life_support", "quarantine_cell", "mycelium_nursery"],
		"mastery_bonus": {"metal": 1, "food": 1}
	},
	"anomaly": {
		"name": "Anomaly Compact",
		"short_name": "ANOMALY",
		"color": "a66be2",
		"description": "Containment, alien materials, and dangerous research shortcuts.",
		"rooms": ["xeno_lab", "anomaly_lab", "quarantine_cell", "research_lab", "holographic_core", "shield_generator", "gravity_loom"],
		"mastery_bonus": {"rare_minerals": 1}
	}
}

const ESSENTIAL_BLUEPRINTS := ["current_turbine", "solar_array", "mining_drone_bay", "construction_drone_bay", "corridor", "corner", "tee_corridor", "storage_bay", "hydroponics_bay", "life_support"]

const PAIR_DIRECTIVE_VARIANTS := [
	{
		"id": "synchronize_doctrines",
		"name": "SYNCHRONIZE %s / %s",
		"briefing": "Bring three %s and three %s modules online.",
		"target": 3,
		"deadline": 24,
		"reward": {"resources": {"metal": 6, "data": 4}, "rerolls": 1}
	},
	{
		"id": "cross_compile_doctrines",
		"name": "CROSS-COMPILE %s / %s",
		"briefing": "Restore three %s and three %s modules to cross-compile the station.",
		"target": 3,
		"deadline": 25,
		"reward": {"resources": {"metal": 4, "data": 6}, "rerolls": 1}
	}
]


static func doctrine(id: String) -> Dictionary:
	return DOCTRINES.get(id, {})

static func build_deck(selected_doctrines: Array, unlocked_room_ids: Dictionary) -> Array[String]:
	var room_ids := {}
	if selected_doctrines.is_empty():
		for id in unlocked_room_ids:
			if id != "brine_core" and not RoomDatabaseScript.get_room(str(id)).is_empty():
				room_ids[id] = true
	for id in ESSENTIAL_BLUEPRINTS:
		room_ids[id] = true
	for doctrine_id_value in selected_doctrines:
		var doctrine_data: Dictionary = doctrine(str(doctrine_id_value))
		for room_id_value in doctrine_data.get("rooms", []):
			room_ids[str(room_id_value)] = true

	# One rare specialist opportunity per deck, rather than three guaranteed cards.
	var specialists: Array[String]=[]
	for id in ["pressure_control","listening_post","isolation_vault"]:
		if room_ids.has(id) and unlocked_room_ids.has(id):specialists.append(id)
	if not specialists.is_empty():
		var selected_specialist: String=specialists.pick_random()
		for id in specialists:
			if id!=selected_specialist:room_ids.erase(id)
	var deck: Array[String] = []
	for room_id_value in room_ids:
		var room_id := str(room_id_value)
		if not unlocked_room_ids.has(room_id):
			continue
		var room := RoomDatabaseScript.get_room(room_id)
		var copies := 1
		if str(room.get("rarity", "common")) == "common":
			copies = 2
		if room_id in ["hydroponics_bay", "life_support"]:
			var doctrine_room := false
			for doctrine_id in selected_doctrines:
				if doctrine(str(doctrine_id)).get("rooms", []).has(room_id):
					doctrine_room = true
			if not doctrine_room:
				copies = 1
		if room_id == "corridor":
			copies = 3
		for _copy_index in range(copies):
			deck.append(room_id)
	return deck





static func count_doctrine_rooms(placed_rooms: Array, selected_doctrines: Array) -> Dictionary:
	var counts := {}
	for id_value in selected_doctrines:
		counts[str(id_value)] = 0
	for room_value in placed_rooms:
		var room: Dictionary = room_value
		var room_id := str(room.get("id", ""))
		if room_id == "brine_core":
			continue
		for doctrine_id_value in selected_doctrines:
			var doctrine_id := str(doctrine_id_value)
			if doctrine(doctrine_id).get("rooms", []).has(room_id):
				counts[doctrine_id] = int(counts.get(doctrine_id, 0)) + 1
	return counts

static func doctrine_pair_name(selected_doctrines: Array) -> String:
	var names: Array[String] = []
	for id_value in selected_doctrines:
		var data := doctrine(str(id_value))
		names.append(str(data.get("short_name", str(id_value).to_upper())))
	return " + ".join(names)
