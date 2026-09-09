extends RefCounted
class_name RoomDatabase

const CATEGORY_COLORS := {
	"Core": Color("#c8fbff"),
	"Engineering": Color("#e6c84f"),
	"Science": Color("#4f8fe6"),
	"Bio": Color("#57c879"),
	"Crew": Color("#e58a45"),
	"Medical": Color("#43d2c6"),
	"Drone": Color("#9aa2a8"),
	"Security": Color("#d34e58"),
	"Anomaly": Color("#9c5de8"),
	"Derelict": Color("#9b6941")
}

const RESOURCE_ICONS := {
	"metal": "□",
	"power": "⚡",
	"oxygen": "○",
	"water": "≈",
	"food": "◆",
	"data": "✦",
	"biomass": "✦",
	"rare_minerals": "◆",
	"integrity": "◇",
	"crew": "▣",
	"corruption": "☣"
}

const STARTING_UNLOCKS := [
	"observation_room",
	"salvage_workshop",
	"galley",
	"cold_store",
	"current_turbine",
	"airlock",
	"construction_drone_bay",
	"solar_array",
	"reactor",
	"mining_drone_bay",
	"hydroponics_bay",
	"life_support",
	"crew_hab",
	"research_lab",
	"storage_bay",
	"med_bay",
	"quarantine_cell",
	"corridor",
	"corner",
	"tee_corridor",
	"pressure_control",
	"listening_post",
	"isolation_vault"
]

const LAYOUTS := {
	"layout_01_tee": {"doors": ["west", "east", "south"], "path": "tee"},
	"layout_02_straight": {"doors": ["north", "south"], "path": "straight"},
	"layout_03_straight_ew": {"doors": ["west", "east"], "path": "straight"},
	"layout_04_corner": {"doors": ["west", "south"], "path": "elbow"},
	"layout_05_cross": {"doors": ["north", "east", "south", "west"], "path": "cross"},
	"layout_06_core": {"doors": ["north", "east", "south", "west"], "path": "perimeter"},
	"layout_dead_south": {"doors": ["south"], "path": "dead"},
	"layout_reactor_cross": {"doors": ["north", "east", "south", "west"], "path": "perimeter"},
	"tee_south": {"doors": ["west", "east", "south"], "path": "tee"},
	"vertical": {"doors": ["north", "south"], "path": "straight"},
	"dead_south": {"doors": ["south"], "path": "dead"},
	"elbow_north_west": {"doors": ["west", "south"], "path": "elbow"},
	"cross": {"doors": ["north", "east", "south", "west"], "path": "cross"},
	"ring_cross": {"doors": ["north", "east", "south", "west"], "path": "ring"}
}

static func all_rooms() -> Dictionary:
	return {
		"cold_store": {
			"id":"cold_store", "display_name":"Cold Store", "category":"Engineering", "rarity":"uncommon",
			"cost":{"metal":8}, "size":Vector2i.ONE, "production":{}, "consumption":{"power":1}, "storage":{"food":40,"biomass":20},
			"tags":["storage","food","logistics"], "layout":"layout_02_straight", "fixed_rotation":0, "unlocked":true,
			"description":"Adds 40 Food and 20 Biomass capacity. Refrigeration uses 1 Power per cycle; storage capacity remains during outages. Fixed north/south aisle. I have labelled the containers. Please stop testing the labels by taste."
		},
		"galley": {
			"id":"galley", "display_name":"Galley", "category":"Crew", "rarity":"uncommon",
			"cost":{"metal":6}, "size":Vector2i.ONE, "production":{"food":4}, "consumption":{"biomass":1,"water":1,"power":1},
			"tags":["crew","food","cooking"], "layout":"layout_dead_south", "fixed_rotation":0, "unlocked":true,
			"description":"Cooks 1 stored Biomass with 1 Water and 1 Power into 4 Food per functioning cycle. Crew collect meals at the serving counter. South entrance; fixed orientation. It is technically soup. That is the most specific promise I can make."
		},
		"salvage_workshop": {
			"id":"salvage_workshop", "display_name":"Salvage Workshop", "category":"Engineering", "rarity":"uncommon",
			"cost":{"metal":8}, "size":Vector2i.ONE, "production":{"rare_minerals":1}, "consumption":{"metal":3,"power":2},
			"tags":["salvage","workshop","engineering"], "layout":"layout_dead_south", "fixed_rotation":0, "unlocked":true,
			"description":"Sorts stored Metal into recoverable components: 3 Metal and 2 Power yield 1 Rare Mineral per functioning cycle. South entrance; fixed orientation. The previous owner called these parts irreparable. They were insufficiently patient."
		},
		"observation_room": {
			"id":"observation_room", "display_name":"Observation Room", "category":"Crew", "rarity":"uncommon",
			"cost":{"metal":6}, "size":Vector2i.ONE, "production":{}, "consumption":{},
			"tags":["crew","observation","library"], "layout":"layout_dead_south", "fixed_rotation":0, "unlocked":true,
			"description":"A north-facing ocean porthole between three walls of books. South entrance; fixed orientation. A quiet room with no resource output. The glass is rated for the pressure. The books are less certain."
		},
		"current_turbine": {
			"id":"current_turbine", "display_name":"Current Turbine", "category":"Engineering", "rarity":"common",
			"cost":{"metal":4}, "size":Vector2i.ONE, "production":{"power":4}, "consumption":{},
			"tags":["power","engineering","current"], "layout":"layout_03_straight_ew", "unlocked":true,
			"description":"Generates 4 Power per cycle while its north-facing intake has an open ocean cell. Rotate to aim the intake; rooms, queued construction and uncleared sites block it. The ocean is moving. We may as well invoice it."
		},
		"biomass_digester": {
			"id":"biomass_digester", "display_name":"Biomass Digester", "category":"Bio", "rarity":"uncommon",
			"cost":{"metal":6,"biomass":2}, "size":Vector2i.ONE, "production":{"power":4}, "consumption":{"biomass":1},
			"tags":["power","bio","engineering"], "layout":"layout_01_tee", "unlocked":false,
			"description":"Converts 1 stored Biomass into 4 Power each cycle. Fresh growth becomes fuel next cycle. The distinction between fuel and dinner remains administrative."
		},
		"heat_recovery": {
			"id":"heat_recovery", "display_name":"Heat Recovery Room", "category":"Engineering", "rarity":"uncommon",
			"cost":{"metal":6,"data":2}, "size":Vector2i.ONE, "production":{}, "consumption":{},
			"tags":["power","engineering","heat_recovery"], "layout":"layout_05_cross", "unlocked":false,
			"description":"Reclaims 2 Power per adjacent functioning Reactor, up to 4 per cycle. Shared walls carry the heat; door connections are not required. Most of that heat was being wasted. Some of it was you."
		},
		"airlock": {
			"id":"airlock","display_name":"Diving Airlock","category":"Engineering","rarity":"common",
			"cost":{"metal":6,"power":1},"size":Vector2i.ONE,"production":{},"consumption":{"power":1},
			"tags":["airlock","equipment","powered"],"layout":"layout_dead_south","unlocked":true,
			"description":"Suit lockers and a separate pressure chamber. Flood and equalize before opening the outer hatch; close, drain and restore station pressure before opening the inner door. Only one door can open at a time."
		},
		"construction_drone_bay": {
			"id":"construction_drone_bay", "display_name":"Construction Drone Bay",
			"category":"Engineering", "rarity":"common", "cost":{"metal":6,"power":1},
			"size":Vector2i.ONE, "production":{}, "consumption":{"power":1},
			"tags":["drone","construction","engineering"], "layout":"layout_02_straight",
			"description":"Houses a fabrication drone. Welds paid room orders into the station. The Core carries an emergency builder.", "unlocked":true
		},
		"brine_core": {
			"id": "brine_core",
			"display_name": "BRINE Core",
			"category": "Core",
			"rarity": "core",
			"cost": {},
			"size": Vector2i.ONE,
			"production": {"data": 1},
			"consumption": {"power": 1},
			"tags": ["core", "data", "powered"],
			"layout": "layout_06_core",
			"description": "Damaged AI heart of the station. Produces Data, but must stay powered.",
			"unlocked": true
		},
		"solar_array": {
			"id": "solar_array",
			"display_name": "Solar Array",
			"category": "Engineering",
			"rarity": "common",
			"cost": {"metal": 4},
			"size": Vector2i.ONE,
			"production": {"power": 3},
			"consumption": {},
			"tags": ["power", "engineering"],
			"layout": "layout_04_corner",
			"description": "Passive solar collection. Steady Power income.",
			"unlocked": true
		},
		"reactor": {
			"id": "reactor",
			"display_name": "Reactor",
			"category": "Engineering",
			"rarity": "common",
			"cost": {"metal": 8, "rare_minerals": 1},
			"size": Vector2i.ONE,
			"production": {"power": 6},
			"consumption": {},
			"tags": ["power", "reactor", "engineering"],
			"layout": "layout_reactor_cross",
			"description": "High output Power. Future meltdown risk lives here.",
			"unlocked": true
		},
		"battery_array": {
			"id": "battery_array",
			"display_name": "Battery Array",
			"category": "Engineering",
			"rarity": "uncommon",
			"cost": {"metal": 6, "data": 2},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {},
			"storage": {"power": 12},
			"tags": ["power_storage", "battery", "engineering"],
			"layout": "layout_05_cross",
			"description": "Adds Power reserve capacity and buffers Reactor surges.",
			"unlocked": false
		},
		"mining_drone_bay": {
			"id": "mining_drone_bay",
			"display_name": "Mining Drone Bay",
			"category": "Drone",
			"rarity": "common",
			"cost": {"metal": 6, "power": 1},
			"size": Vector2i.ONE,
			"production": {"metal": 2},
			"consumption": {"power": 1},
			"tags": ["drone", "mining", "metal"],
			"layout": "layout_02_straight",
			"description": "Extracts Metal from finite mineral deposits and basalt. Battery-powered tools; cargo returns to the bay for unloading and recharge.",
			"unlocked": true
		},
		"salvage_drone_bay": {
			"id": "salvage_drone_bay",
			"display_name": "Salvage Drone Bay",
			"category": "Drone",
			"rarity": "common",
			"cost": {"metal": 5, "power": 1},
			"size": Vector2i.ONE,
			"production": {"metal": 1, "data": 1},
			"consumption": {"power": 1},
			"tags": ["drone", "salvage", "derelict"],
			"layout": "layout_02_straight",
			"description": "Extracts Metal and Data from finite scrap piles and dismantles wrecked rooms. Cargo returns to the bay for unloading and recharge.",
			"unlocked": true
		},
		"gravity_loom": {
			"id": "gravity_loom",
			"display_name": "Gravity Loom",
			"category": "Anomaly",
			"rarity": "rare",
			"cost": {"metal": 12, "data": 8, "rare_minerals": 3},
			"size": Vector2i.ONE,
			"production": {"data": 1, "rare_minerals": 1},
			"consumption": {"power": 4},
			"tags": ["science", "anomaly", "containment"],
			"layout": "layout_06_core",
			"description": "Sorts matter through a contained distortion. The calibration weights disagree.",
			"unlocked": false
		},
		"tidal_condenser": {
			"id": "tidal_condenser",
			"display_name": "Tidal Condenser",
			"category": "Engineering",
			"rarity": "uncommon",
			"cost": {"metal": 7, "data": 2},
			"size": Vector2i.ONE,
			"production": {"water": 2},
			"consumption": {"power": 2},
			"tags": ["engineering", "water", "condensation"],
			"layout": "layout_01_tee",
			"description": "Reclaims Water through chilled coils. The ocean remains on the other side.",
			"unlocked": false
		},
		"mycelium_nursery": {
			"id": "mycelium_nursery",
			"display_name": "Mycelium Nursery",
			"category": "Bio",
			"rarity": "uncommon",
			"cost": {"metal": 7, "biomass": 3},
			"size": Vector2i.ONE,
			"production": {"food": 3},
			"consumption": {"power": 1, "biomass": 1},
			"tags": ["bio", "food"],
			"layout": "layout_01_tee",
			"description": "Cultivates edible tissue from Biomass. The trays do not require sunlight.",
			"unlocked": false
		},
		"hydroponics_bay": {
			"id": "hydroponics_bay",
			"flood_compatible": true,
			"display_name": "Hydroponics Bay",
			"category": "Bio",
			"rarity": "common",
			"cost": {"metal": 5, "biomass": 1},
			"size": Vector2i.ONE,
			"production": {"food": 2, "oxygen": 1, "biomass": 1},
			"consumption": {"power": 1},
			"tags": ["bio", "food", "oxygen", "plants"],
			"layout": "layout_05_cross",
			"description": "Grows food, oxygen, and a little Biomass.",
			"unlocked": true
		},
		"life_support": {
			"id": "life_support",
			"display_name": "Life Support",
			"category": "Bio",
			"rarity": "common",
			"cost": {"metal": 5, "power": 1},
			"size": Vector2i.ONE,
			"production": {"oxygen": 3},
			"consumption": {"power": 1},
			"tags": ["oxygen", "bio", "engineering", "medical_support"],
			"layout": "layout_05_cross",
			"description": "Stabilizes Oxygen. Vital before waking crew.",
			"unlocked": true
		},
		"crew_hab": {
			"id": "crew_hab",
			"display_name": "Crew Hab",
			"category": "Crew",
			"rarity": "common",
			"cost": {"metal": 6, "oxygen": 2, "food": 2},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {},
			"tags": ["crew", "hab"],
			"layout": "layout_01_tee",
			"description": "Adds two berths. One survivor moves in on construction if supplies are stable.",
			"unlocked": true
		},
		"research_lab": {
			"id": "research_lab",
			"display_name": "Research Lab",
			"category": "Science",
			"rarity": "common",
			"cost": {"metal": 6, "power": 1},
			"size": Vector2i.ONE,
			"production": {"data": 2},
			"consumption": {"power": 1},
			"tags": ["science", "data", "crew_bonus"],
			"layout": "layout_dead_south",
			"description": "Produces Data. Scientists improvise if any crew are alive.",
			"unlocked": true
		},
		"cryo_chamber": {
			"id": "cryo_chamber",
			"display_name": "Cryo Chamber",
			"category": "Medical",
			"rarity": "rare",
			"cost": {"metal": 8, "data": 4},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {"power": 1},
			"tags": ["medical", "derelict", "survivor"],
			"layout": "layout_02_straight",
			"description": "A damaged pod. With support nearby, survivors may wake.",
			"unlocked": false
		},
		"clone_lab": {
			"id": "clone_lab",
			"display_name": "Clone Lab",
			"category": "Medical",
			"rarity": "rare",
			"cost": {"metal": 10, "data": 8, "biomass": 8},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {"power": 2, "biomass": 1, "data": 1},
			"tags": ["medical", "bio", "clone"],
			"layout": "layout_01_tee",
			"description": "Creates clone crew from Biomass and Data.",
			"unlocked": false
		},
		"quarantine_cell": {
			"id": "quarantine_cell",
			"display_name": "Quarantine Cell",
			"category": "Security",
			"rarity": "uncommon",
			"cost": {"metal": 7, "data": 2},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {"power": 1},
			"tags": ["security", "medical", "containment"],
			"layout": "layout_03_straight_ew",
			"description": "Reduces hostile or anomalous spread risk.",
			"unlocked": false
		},
		"data_archive": {
			"id": "data_archive",
			"display_name": "Data Archive",
			"category": "Science",
			"rarity": "uncommon",
			"cost": {"metal": 5, "data": 8},
			"size": Vector2i.ONE,
			"production": {"data": 1},
			"consumption": {"power": 1},
			"storage": {"data": 40},
			"tags": ["science", "data", "archive"],
			"layout": "layout_06_core",
			"description": "Boosts Data storage and research indexing.",
			"unlocked": false
		},
		"ore_refinery": {
			"id": "ore_refinery",
			"display_name": "Ore Refinery",
			"category": "Engineering",
			"rarity": "uncommon",
			"cost": {"metal": 8, "power": 1},
			"size": Vector2i.ONE,
			"production": {"metal": 1},
			"consumption": {"power": 1},
			"storage": {"metal": 40, "rare_minerals": 10},
			"tags": ["engineering", "metal", "refinery"],
			"layout": "layout_02_straight",
			"description": "Improves Metal output from Mining Drone Bays.",
			"unlocked": true
		},
		"storage_bay": {
			"id": "storage_bay",
			"display_name": "Storage Bay",
			"category": "Engineering",
			"rarity": "common",
			"cost": {"metal": 6},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {},
			"storage": {"metal": 60, "food": 20, "oxygen": 20, "water": 20},
			"tags": ["engineering", "storage", "logistics"],
			"layout": "layout_05_cross",
			"description": "Expands station stockpiles for common survival and build resources.",
			"unlocked": true
		},
		"med_bay": {
			"id": "med_bay",
			"display_name": "Med Bay",
			"category": "Medical",
			"rarity": "rare",
			"cost": {"metal": 7, "data": 3, "power": 1},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {"power": 1},
			"tags": ["medical", "crew_support", "medical_support"],
			"layout": "layout_dead_south",
			"description": "Keeps recovered crew stable and supports safer cryo wake protocols.",
			"unlocked": true
		},
		"biodome": {
			"id": "biodome",
			"display_name": "Biodome",
			"category": "Bio",
			"rarity": "rare",
			"cost": {"metal": 10, "water": 4, "biomass": 4},
			"size": Vector2i.ONE,
			"production": {"food": 3, "oxygen": 2, "biomass": 2},
			"consumption": {"power": 2, "water": 1},
			"storage": {"food": 30, "oxygen": 30, "biomass": 20},
			"tags": ["bio", "food", "oxygen", "plants", "biodome"],
			"layout": "layout_02_straight",
			"description": "A larger living ecology module with stronger life-support output.",
			"unlocked": false
		},
		"xeno_lab": {
			"id": "xeno_lab",
			"display_name": "Xeno Lab",
			"category": "Anomaly",
			"rarity": "rare",
			"cost": {"metal": 8, "data": 8, "rare_minerals": 2},
			"size": Vector2i.ONE,
			"production": {"data": 3, "rare_minerals": 1},
			"consumption": {"power": 2},
			"tags": ["science", "anomaly", "xeno", "containment_risk"],
			"layout": "layout_dead_south",
			"description": "Studies alien wreckage. Valuable output, but eventually wants containment.",
			"unlocked": true
		},
		"anomaly_lab": {
			"id": "anomaly_lab",
			"display_name": "Anomaly Lab",
			"category": "Anomaly",
			"rarity": "rare",
			"cost": {"metal": 8, "data": 6, "rare_minerals": 1},
			"size": Vector2i.ONE,
			"production": {"data": 2, "rare_minerals": 1},
			"consumption": {"power": 2},
			"tags": ["science", "anomaly", "containment_risk"],
			"layout": "layout_dead_south",
			"description": "Experimental anomaly workspace. Strong research yield, strange side effects later.",
			"unlocked": true
		},
		"bio_lab": {
			"id": "bio_lab",
			"display_name": "Bio Lab",
			"category": "Bio",
			"rarity": "uncommon",
			"cost": {"metal": 6, "biomass": 3, "power": 1},
			"size": Vector2i.ONE,
			"production": {"biomass": 2, "data": 1},
			"consumption": {"power": 1, "water": 1},
			"tags": ["bio", "science", "biomass"],
			"layout": "layout_01_tee",
			"description": "Grows and studies station-compatible organic systems.",
			"unlocked": true
		},
		"command_center": {
			"id": "command_center",
			"display_name": "Command Center",
			"category": "Core",
			"rarity": "rare",
			"cost": {"metal": 10, "data": 6, "power": 2},
			"size": Vector2i.ONE,
			"production": {"data": 2},
			"consumption": {"power": 1},
			"storage": {"data": 20},
			"tags": ["core_support", "command", "data"],
			"layout": "layout_05_cross", # Registered consoles leave central cross aisles.
			"description": "Auxiliary command node for BRINE's station coordination routines.",
			"unlocked": true
		},
		"corridor": {
			"id": "corridor",
			"display_name": "Corridor",
			"category": "Engineering",
			"rarity": "uncommon",
			"cost": {"metal": 2},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {},
			"tags": ["corridor", "routing"],
			"layout": "layout_02_straight",
			"description": "Cheap routing space for extending the station footprint.",
			"unlocked": true
		},
		"corner": {
			"id": "corner",
			"display_name": "Corner Corridor",
			"category": "Engineering",
			"rarity": "uncommon",
			"cost": {"metal": 2},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {},
			"tags": ["corridor", "routing"],
			"layout": "layout_04_corner",
			"description": "Turns station traffic around a corner.",
			"unlocked": true
		},
		"pressure_control": {"id":"pressure_control","display_name":"Pressure Control Chamber","category":"Engineering","rarity":"rare","cost":{"metal": 12, "data": 4},"size":Vector2i.ONE,"production":{},"consumption":{"power":1},"tags":["rare_control","dead_end"],"layout":"layout_dead_south","description":"Pressure tanks and branch flooding controls.","unlocked":true},
		"listening_post": {"id":"listening_post","display_name":"Deepwater Listening Post","category":"Science","rarity":"rare","cost":{"metal": 10, "data": 6},"size":Vector2i.ONE,"production":{},"consumption":{"power":1},"tags":["rare_control","dead_end"],"layout":"layout_dead_south","description":"Investigates distant mineral and salvage signals.","unlocked":true},
		"isolation_vault": {"id":"isolation_vault","display_name":"Emergency Isolation Vault","category":"Engineering","rarity":"rare","cost":{"metal": 14, "data": 4},"size":Vector2i.ONE,"production":{},"consumption":{"power":1},"tags":["rare_control","dead_end"],"layout":"layout_dead_south","description":"Reserve power and emergency branch isolation controls.","unlocked":true},
		"tee_corridor": {
			"id": "tee_corridor", "display_name": "T Corridor",
			"category": "Engineering", "rarity": "uncommon",
			"cost": {"metal": 3}, "size": Vector2i.ONE,
			"production": {}, "consumption": {},
			"tags": ["corridor", "routing"], "layout": "layout_01_tee",
			"description": "Three-way passage linking station branches.", "unlocked": true
		},
		"crew_lounge": {
			"id": "crew_lounge",
			"display_name": "Crew Lounge",
			"category": "Crew",
			"rarity": "uncommon",
			"cost": {"metal": 6, "food": 2, "oxygen": 2},
			"size": Vector2i.ONE,
			"production": {"food": 1},
			"consumption": {"oxygen": 1},
			"tags": ["crew", "morale", "hab"],
			"layout": "layout_01_tee",
			"description": "A softer place for recovered crew to gather and stabilize.",
			"unlocked": true
		},
		"holographic_core": {
			"id": "holographic_core",
			"display_name": "Holographic Core",
			"category": "Science",
			"rarity": "rare",
			"cost": {"metal": 8, "data": 8, "power": 2},
			"size": Vector2i.ONE,
			"production": {"data": 3},
			"consumption": {"power": 2},
			"storage": {"data": 25},
			"tags": ["science", "data", "core_support"],
			"layout": "layout_06_core",
			"description": "A projection lattice that helps BRINE model lost station memories.",
			"unlocked": true
		},
		"maintenance_bay": {
			"id": "maintenance_bay",
			"display_name": "Maintenance Bay",
			"category": "Engineering",
			"rarity": "common",
			"cost": {"metal": 5, "power": 1},
			"size": Vector2i.ONE,
			"production": {"integrity": 1},
			"consumption": {"power": 1},
			"tags": ["engineering", "repair"],
			"layout": "layout_01_tee",
			"description": "Repair tooling for keeping station systems patched together.",
			"unlocked": true
		},
		"med_center": {
			"id": "med_center",
			"display_name": "Med Center",
			"category": "Medical",
			"rarity": "uncommon",
			"cost": {"metal": 8, "data": 4, "power": 1},
			"size": Vector2i.ONE,
			"production": {},
			"consumption": {"power": 1},
			"tags": ["medical", "crew_support", "medical_support"],
			"layout": "layout_02_straight",
			"description": "Expanded medical support for future survivor systems.",
			"unlocked": true
		},
		"med_office": {
			"id": "med_office",
			"display_name": "Med Office",
			"category": "Medical",
			"rarity": "common",
			"cost": {"metal": 5, "data": 2},
			"size": Vector2i.ONE,
			"production": {"data": 1},
			"consumption": {"power": 1},
			"tags": ["medical", "crew_support"],
			"layout": "layout_02_straight",
			"description": "Records symptoms, failures, and recovery protocols.",
			"unlocked": true
		},
		"radio_lab": {
			"id": "radio_lab",
			"display_name": "Radio Lab",
			"category": "Science",
			"rarity": "uncommon",
			"cost": {"metal": 6, "power": 1},
			"size": Vector2i.ONE,
			"production": {"data": 2},
			"consumption": {"power": 1},
			"tags": ["science", "data", "signal"],
			"layout": "layout_03_straight_ew",
			"description": "Listens through orbital static for recoverable station signals.",
			"unlocked": true
		},
		"shield_generator": {
			"id": "shield_generator",
			"display_name": "Shield Generator",
			"category": "Security",
			"rarity": "uncommon",
			"cost": {"metal": 8, "power": 2, "rare_minerals": 1},
			"size": Vector2i.ONE,
			"production": {"integrity": 1},
			"consumption": {"power": 2},
			"tags": ["security", "shield", "engineering"],
			"layout": "layout_02_straight",
			"description": "Prototype shielding for softening future orbital hazards.",
			"unlocked": true
		}
	}

static var _lookup_templates: Dictionary = {}

static func get_room(id: String) -> Dictionary:
	if _lookup_templates.is_empty():
		_lookup_templates = all_rooms()
	# Callers add runtime state and may edit nested rates/tags. Never share templates.
	return _lookup_templates.get(id, {}).duplicate(true)

static func category_color(category: String) -> Color:
	return CATEGORY_COLORS.get(category, Color.WHITE)

static func get_layout(layout_id: String) -> Dictionary:
	return LAYOUTS.get(layout_id, LAYOUTS["layout_05_cross"])

static func resource_icon(resource_id: String) -> String:
	return RESOURCE_ICONS.get(resource_id, "•")
