extends RefCounted
class_name SynergyManager

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const PASSAGE_IDS := ["corridor", "corner", "tee_corridor"]

const SYNERGIES := [
	{
		"id": "parts_passage", "name": "Parts Passage",
		"rooms": ["storage_bay", "salvage_workshop"], "via_passage": true,
		"bonus": {"metal": 1},
		"effect": "+1 Metal per functioning cycle per Storage Bay / Salvage Workshop pair joined through one straight, corner or T corridor. All three rooms must function; extra passages do not stack.",
		"message": "The spare parts now reach the workshop before someone declares them missing.",
		"terminal_reward": {"research": 3}, "stabilize_cycles": 3,
		"fx_profile": "logistics", "fx_color": "B68D55"
	},
	{
		"id":"chilled_air_recovery", "name":"Chilled Air Recovery", "rooms":["cold_store","life_support"],
		"bonus":{"oxygen":1}, "effect":"+1 Oxygen per functioning cycle from recovered cold air.",
		"message":"The cold return air is clean enough to breathe. This was not true of everything in storage.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"flow", "fx_color":"75ABB3"
	},
	{
		"id":"shared_table", "name":"Shared Table", "rooms":["galley","crew_lounge"],
		"bonus":{"food":1}, "effect":"+1 Food per functioning cycle from coordinated meal service.",
		"message":"The portions reach the table before they go cold. Attendance remains below the original estimate.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"care", "fx_color":"BFA76C"
	},
	{
		"id":"field_notes", "name":"Field Notes", "rooms":["observation_room","data_archive"],
		"bonus":{"data":1}, "effect":"+1 Data per functioning cycle from indexed ocean observations.",
		"message":"The shapes beyond the glass now have catalogue entries. Some of them have changed since filing.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"signal", "fx_color":"7BA7B9"
	},
	{
		"id":"cold_chain", "name":"Cold Chain", "rooms":["cold_store","galley"],
		"bonus":{"food":1}, "effect":"+1 Food per functioning cycle from organized chilled provisions.",
		"message":"The ingredients arrive cold and in the correct order. A modest triumph over entropy.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"logistics", "fx_color":"75ABB3"
	},
	{
		"id":"fresh_provisions", "name":"Fresh Provisions", "rooms":["galley","hydroponics_bay"],
		"bonus":{"food":1}, "effect":"+1 Food per functioning cycle from fresh kitchen provisions.",
		"message":"The distance between harvest and dinner has decreased. So have the complaints.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"flow", "fx_color":"BFA76C"
	},
	{
		"id":"parts_reclamation", "name":"Parts Reclamation", "rooms":["salvage_workshop","salvage_drone_bay"],
		"bonus":{"metal":1}, "effect":"+1 Metal per functioning cycle from sorted salvage offcuts.",
		"message":"The discarded fittings still fit something. I have revised the disposal policy.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"logistics", "fx_color":"B68D55"
	},
	{
		"id":"warm_fermentation", "name":"Warm Fermentation", "rooms":["heat_recovery","biomass_digester"],
		"bonus":{"water":1}, "effect":"+1 Water per functioning cycle.",
		"message":"The warm return line has condensed something useful. I checked twice.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"flow", "fx_color":"84938A"
	},
	{
		"id":"cultivated_current", "name":"Cultivated Current", "rooms":["current_turbine","hydroponics_bay"],
		"bonus":{"biomass":1}, "effect":"+1 Biomass per functioning cycle.",
		"message":"The circulation has improved the yield. Something in the tanks approves.",
		"unlock_room_id":"biomass_digester", "stabilize_cycles":3, "fx_profile":"flow", "fx_color":"729278"
	},
	{
		"id":"industrial_heat_capture", "name":"Industrial Heat Capture", "rooms":["reactor","mining_drone_bay"],
		"bonus":{"metal":1}, "effect":"+1 Metal per functioning cycle.",
		"message":"The drill housings are warm. That energy still belongs to us.",
		"unlock_room_id":"heat_recovery", "stabilize_cycles":3, "fx_profile":"power", "fx_color":"A48560"
	},
	{
		"id":"fermentation_feed", "name":"Fermentation Feed", "rooms":["biomass_digester","hydroponics_bay"],
		"bonus":{"power":1}, "effect":"+1 Power per functioning cycle.",
		"message":"The trimmings have found a second occupation.",
		"terminal_reward":{"research":3}, "stabilize_cycles":3, "fx_profile":"power", "fx_color":"87946D"
	},
	{
		"id": "inertial_containment",
		"name": "Inertial Containment",
		"rooms": [
			"anomaly_lab",
			"shield_generator"
		],
		"bonus": {
			"data": 1
		},
		"effect": "+1 Data per functioning cycle.",
		"message": "The field holds. I am no longer certain what it is holding.",
		"unlock_room_id": "gravity_loom",
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "B299CE"
	},
	{
		"id": "mass_sorting",
		"name": "Mass Sorting",
		"rooms": [
			"gravity_loom",
			"mining_drone_bay"
		],
		"bonus": {
			"metal": 3
		},
		"effect": "+3 Metal per functioning cycle.",
		"message": "The heavier fragments arrive first. Distance has declined to explain itself.",
		"terminal_reward": {
			"research": 3
		},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B299CE"
	},
	{
		"id": "geometric_echo",
		"name": "Geometric Echo",
		"rooms": [
			"gravity_loom",
			"holographic_core"
		],
		"bonus": {
			"data": 3
		},
		"effect": "+3 Data per functioning cycle.",
		"message": "The model has acquired an extra angle. I have checked the room twice.",
		"terminal_reward": {
			"research": 3
		},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "B299CE"
	},
	{
		"id": "thermal_reclamation",
		"name": "Thermal Reclamation",
		"rooms": ["reactor", "life_support"],
		"bonus": {"water": 1},
		"effect": "+1 Water per functioning cycle.",
		"message": "The heat was escaping. I have found another use for it.",
		"unlock_room_id": "tidal_condenser",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "79B7C5"
	},
	{
		"id": "nutrient_mist",
		"name": "Nutrient Mist",
		"rooms": ["tidal_condenser", "hydroponics_bay"],
		"bonus": {"food": 1},
		"effect": "+1 Food per functioning cycle.",
		"message": "The roots have stopped rationing moisture. I have not.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "79B7C5"
	},
	{
		"id": "chilled_cells",
		"name": "Chilled Cells",
		"rooms": ["tidal_condenser", "battery_array"],
		"bonus": {"power": 1},
		"effect": "+1 Power per functioning cycle.",
		"message": "The cells run cooler. Their failure estimates remain estimates.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "79B7C5"
	},
	{
		"id": "substrate_recovery",
		"name": "Substrate Recovery",
		"rooms": ["hydroponics_bay", "quarantine_cell"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per functioning cycle from recovered cultivation substrate.",
		"message": "The discarded cultures are still growing. I have revised the disposal protocol.",
		"unlock_room_id": "mycelium_nursery",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "79B7A3"
	},
	{
		"id": "culture_exchange",
		"name": "Culture Exchange",
		"rooms": ["mycelium_nursery", "bio_lab"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per functioning cycle from shared cultures.",
		"message": "The cultures have exchanged more information than the lab reports acknowledge.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "79B7A3"
	},
	{
		"id": "restorative_culture",
		"name": "Restorative Culture",
		"rooms": ["mycelium_nursery", "med_bay"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per functioning cycle from restorative cultures.",
		"message": "The repair cultures have taken hold. I am monitoring where they stop.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "closed_air_loop",
		"name": "Closed Air Loop",
		"rooms": ["hydroponics_bay", "life_support"],
		"bonus": {"oxygen": 1, "water": 2},
		"effect": "Reclaims condensation: +1 Oxygen and +2 Water per functioning cycle.",
		"message": "BRINE recovered a life-support pattern: Closed Air Loop.",
		"unlock_room_id": "biodome",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "55E6FF"
	},
	{
		"id": "green_commons",
		"name": "Green Commons",
		"rooms": ["hydroponics_bay", "crew_hab"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while living plants are adjacent to crew quarters.",
		"message": "Crew morale improves near living plants.",
		"unlock_room_id": "crew_lounge",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "73E59A"
	},
	{
		"id": "industrial_chain",
		"name": "Industrial Chain",
		"rooms": ["mining_drone_bay", "ore_refinery"],
		"bonus": {"metal": 2},
		"effect": "+2 Metal per cycle while drone mining feeds an adjacent refinery.",
		"message": "Ore processing route optimized.",
		"unlock_room_id": "salvage_drone_bay",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "F1B45B"
	},
	{
		"id": "stable_power_flow",
		"name": "Stable Power Flow",
		"rooms": ["reactor", "battery_array"],
		"bonus": {"power": 1},
		"effect": "+1 Power per cycle while a Battery Array buffers an adjacent Reactor.",
		"message": "Power surge buffering stabilized.",
		"unlock_room_id": "shield_generator",
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "FFD65A"
	},
	{
		"id": "research_pipeline",
		"name": "Research Pipeline",
		"rooms": ["research_lab", "data_archive"],
		"bonus": {"data": 2},
		"effect": "+2 Data per cycle while a Research Lab is adjacent to a Data Archive.",
		"message": "Data indexing increased research yield.",
		"unlock_room_id": "radio_lab",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "safe_wake_protocol",
		"name": "Safe Wake Protocol",
		"rooms": ["cryo_chamber", "life_support"],
		"bonus": {},
		"effect": "Revives one survivor every 3 cycles while habitat space remains. Connect Cryo to Life Support or any medical room.",
		"message": "Cryo recovery protocol restored.",
		"unlock_room_id": "clone_lab",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "61E0D1"
	},
	{
		"id": "containment_sector",
		"name": "Containment Sector",
		"rooms": ["xeno_lab", "quarantine_cell"],
		"bonus": {},
		"effect": "Removes 1 Corruption each functioning cycle.",
		"message": "Anomaly spread contained.",
		"unlock_room_id": "anomaly_lab",
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "B774FF"
	},
	{
		"id": "crew_commons",
		"name": "Crew Commons",
		"rooms": ["crew_hab", "crew_lounge"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while crew quarters share a connected commons.",
		"message": "Crew schedules converge around a shared commons.",
		"unlock_room_id": "med_center",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "7DE29A"
	},
	{
		"id": "field_clinic",
		"name": "Field Clinic",
		"rooms": ["crew_hab", "med_bay"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while medical care is embedded in a crew sector.",
		"message": "A field clinic comes online beside crew quarters.",
		"unlock_room_id": "med_office",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "54D8CA"
	},
	{
		"id": "shielded_reactor",
		"name": "Shielded Reactor",
		"rooms": ["reactor", "shield_generator"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while shielding contains reactor stress.",
		"message": "Reactor stress falls inside the shield envelope.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "FFB85A"
	},
	{
		"id": "signal_command",
		"name": "Signal Command",
		"rooms": ["radio_lab", "command_center"],
		"bonus": {"data": 2},
		"effect": "+2 Data per cycle while command systems decode radio traffic.",
		"message": "Command begins resolving patterns in the orbital static.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "6C9DFF"
	},
	{
		"id": "drone_foundry",
		"name": "Drone Foundry",
		"rooms": ["salvage_drone_bay", "maintenance_bay"],
		"bonus": {"metal": 1, "integrity": 1},
		"effect": "+1 Metal and +1 Integrity per cycle from recovered drone parts.",
		"message": "Salvage parts feed directly into station maintenance.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "E8D8B2"
	},
	{
		"id": "living_circuit",
		"name": "Living Circuit",
		"rooms": ["bio_lab", "holographic_core"],
		"bonus": {"biomass": 1, "data": 1},
		"effect": "+1 Biomass and +1 Data per cycle while living samples inform BRINE's models.",
		"message": "Organic telemetry begins teaching the holographic core.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "B7F06D"
	},
	{
		"id": "biodome_atmosphere",
		"name": "Biodome Atmosphere",
		"rooms": ["biodome", "life_support"],
		"bonus": {"oxygen": 2, "water": 1},
		"effect": "Circulates the canopy: +2 Oxygen and +1 Water per functioning cycle.",
		"message": "The biodome canopy joins the station air loop.",
		"unlock_room_id": "bio_lab",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "69EDA7"
	},
	{
		"id": "core_relay",
		"name": "Core Relay",
		"rooms": ["brine_core", "command_center"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while command telemetry routes through BRINE.",
		"message": "BRINE accepts the command center as a trusted relay.",
		"unlock_room_id": "holographic_core",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "76E6FF"
	},
	{
		"id": "logistics_spine",
		"name": "Logistics Spine",
		"rooms": ["storage_bay", "corridor"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while storage opens directly onto a routing corridor.",
		"message": "Material traffic stabilizes along a logistics spine.",
		"unlock_room_id": "maintenance_bay",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "F0D8A0"
	},
	{
		"id": "medical_network",
		"name": "Medical Network",
		"rooms": ["med_center", "med_office"],
		"bonus": {"data": 1, "integrity": 1},
		"effect": "+1 Data and +1 Integrity per cycle from coordinated medical telemetry.",
		"message": "Medical records begin predicting station failures.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "59DED0"
	},
	{
		"id": "clinical_airlock",
		"name": "Clinical Airlock",
		"rooms": ["med_bay", "life_support"],
		"bonus": {"oxygen": 1, "integrity": 1},
		"effect": "+1 Oxygen and +1 Integrity per cycle while clinical air is isolated.",
		"message": "A sterile airlock pattern settles between care and circulation.",
		"unlock_room_id": "cryo_chamber",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "6EEBD8"
	},
	{
		"id": "ore_buffer",
		"name": "Ore Buffer",
		"rooms": ["mining_drone_bay", "storage_bay"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while mined ore is buffered beside storage.",
		"message": "Drone routes begin staging raw ore beside storage.",
		"unlock_room_id": "ore_refinery",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "DDA85B"
	},
	{
		"id": "load_balancing",
		"name": "Load Balancing",
		"rooms": ["solar_array", "reactor"],
		"bonus": {"power": 1},
		"effect": "+1 Power per cycle while solar input smooths reactor load.",
		"message": "BRINE synchronizes the station's two power rhythms.",
		"unlock_room_id": "battery_array",
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "FFE06B"
	},
	{
		"id": "core_diagnostics",
		"name": "Core Diagnostics",
		"rooms": ["brine_core", "research_lab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while researchers decode BRINE telemetry.",
		"message": "Research instruments find a legible rhythm inside BRINE.",
		"unlock_room_id": "data_archive",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "75C8FF"
	},
	{
		"id": "sterile_observation",
		"name": "Sterile Observation",
		"rooms": ["research_lab", "quarantine_cell"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while quarantine specimens are observed safely.",
		"message": "A sterile observation protocol resolves from the quarantine feed.",
		"unlock_room_id": "xeno_lab",
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "A982FF"
	},
	{
		"id": "signal_triangulation",
		"name": "Signal Triangulation",
		"rooms": ["radio_lab", "research_lab"],
		"bonus": {"data": 2},
		"effect": "+2 Data per cycle while laboratory models triangulate radio noise.",
		"message": "Three faint bearings converge into a navigable signal.",
		"unlock_room_id": "command_center",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "6D8FFF"
	},
	{
		"id": "genomic_triage",
		"name": "Genomic Triage",
		"rooms": ["clone_lab", "med_center"],
		"bonus": {"biomass": 1, "integrity": 1},
		"effect": "+1 Biomass and +1 Integrity per cycle from predictive genetic care.",
		"message": "The medical network begins anticipating cellular failure.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "FF8FC7"
	},
	{
		"id": "impossible_model",
		"name": "Impossible Model",
		"rooms": ["anomaly_lab", "holographic_core"],
		"bonus": {"data": 1, "rare_minerals": 1},
		"effect": "+1 Data and +1 Rare Minerals per cycle while BRINE models the anomaly.",
		"message": "The holographic core holds a shape that should not remain stable.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "C16DFF"
	},
	# New-room expansion patterns (owner-approved Sept 27): stabilising halves the related blueprint.
	{
		"id": "resonant_silence",
		"name": "Resonant Silence",
		"rooms": ["listening_post", "isolation_vault"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the isolation vault's stillness sharpens faint returns.",
		"message": "In the vault's silence, the listening post hears its own echo answer.",
		"unlock_room_id": "echo_chamber",
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "B299CE"
	},
	{
		"id": "folded_field",
		"name": "Folded Field",
		"rooms": ["gravity_loom", "anomaly_lab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while loom harmonics fold the anomaly's field.",
		"message": "The anomaly's field creases along the loom's threads and holds.",
		"unlock_room_id": "fold_chamber",
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "A982FF"
	},
	{
		"id": "pressure_grown",
		"name": "Pressure Grown",
		"rooms": ["pressure_control", "hydroponics_bay"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per cycle while pressure cycling toughens the hydroponic stock.",
		"message": "Plants grown under controlled pressure root deeper and waste less.",
		"unlock_room_id": "pressure_garden",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "729278"
	},
	{
		"id": "still_water_watch",
		"name": "Still Water Watch",
		"rooms": ["observation_room", "listening_post"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while observers log the listening post's quiet contacts.",
		"message": "Between the window and the hydrophones, still water starts to show its movement.",
		"unlock_room_id": "stillwater_observatory",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	{
		"id": "breathable_quarters",
		"name": "Breathable Quarters",
		"rooms": ["life_support", "crew_hab"],
		"bonus": {"oxygen": 1},
		"effect": "+1 Oxygen per cycle while life support scrubs the crew quarters directly.",
		"message": "Fresh air reaches the bunks before it reaches anywhere else.",
		"unlock_room_id": "atmospheric_scrubber",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "75ABB3"
	},
	{
		"id": "waste_to_growth",
		"name": "Waste to Growth",
		"rooms": ["biomass_digester", "crew_hab"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per cycle while crew waste feeds the digester.",
		"message": "The crew's leftovers become the digester's best feedstock.",
		"unlock_room_id": "habitat_recovery",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "729278"
	},
	{
		"id": "seed_stock",
		"name": "Seed Stock",
		"rooms": ["cold_store", "hydroponics_bay"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while cold storage keeps the best hydroponic seed.",
		"message": "Cold storage sets aside seed from the strongest crops.",
		"unlock_room_id": "seed_vault",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "BFA76C"
	},
	{
		"id": "condensate_loop",
		"name": "Condensate Loop",
		"rooms": ["tidal_condenser", "life_support"],
		"bonus": {"water": 1},
		"effect": "+1 Water per cycle while the condenser returns life support's moisture.",
		"message": "Moisture pulled from the air runs back through the condenser.",
		"unlock_room_id": "water_reclamation",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "84938A"
	},
	{
		"id": "sealed_sections",
		"name": "Sealed Sections",
		"rooms": ["pressure_control", "corridor"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while pressure control drills the corridor seals.",
		"message": "Corridor seals close on cue; the station learns to hold a breach.",
		"unlock_room_id": "bulkhead_control",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "79B7A3"
	},
	{
		"id": "loading_dock",
		"name": "Loading Dock",
		"rooms": ["storage_bay", "airlock"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while cargo stages beside the airlock.",
		"message": "Salvage stops crossing the station twice: storage meets the airlock.",
		"unlock_room_id": "cargo_dispatch",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "repair_crews",
		"name": "Repair Crews",
		"rooms": ["maintenance_bay", "command_center"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while command routes maintenance crews to faults.",
		"message": "Command starts dispatching repairs before the alarms finish.",
		"unlock_room_id": "damage_control",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "79B7A3"
	},
	{
		"id": "sounding_grid",
		"name": "Sounding Grid",
		"rooms": ["listening_post", "command_center"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while command plots the listening post's soundings.",
		"message": "Soundings resolve into a grid; the seabed takes shape on command's screens.",
		"unlock_room_id": "sonar_mapping",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "window_on_the_deep",
		"name": "Window on the Deep",
		"rooms": ["observation_room", "crew_lounge"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the crew catalogue what drifts past the window.",
		"message": "The crew start naming the fish outside the observation window.",
		"unlock_room_id": "aquarium",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	{
		"id": "found_materials",
		"name": "Found Materials",
		"rooms": ["salvage_workshop", "crew_lounge"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while offcuts from salvage become the crew's art supplies.",
		"message": "Scrap too small to use turns up again, painted, in the lounge.",
		"unlock_room_id": "art_studio",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "warm_water",
		"name": "Warm Water",
		"rooms": ["heat_recovery", "life_support"],
		"bonus": {"water": 1},
		"effect": "+1 Water per cycle while recovered heat warms the station's water loop.",
		"message": "Waste heat runs through the water loop; the pipes stop sweating.",
		"unlock_room_id": "bathhouse",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "84938A"
	},
	{
		"id": "glasshouse",
		"name": "Glasshouse",
		"rooms": ["biodome", "observation_room"],
		"bonus": {"oxygen": 1},
		"effect": "+1 Oxygen per cycle while the biodome grows along the observation glass.",
		"message": "Vines climb toward the observation glass and breathe on it.",
		"unlock_room_id": "botanical_conservatory",
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "75ABB3"
	},
	{
		"id": "projection_night",
		"name": "Projection Night",
		"rooms": ["holographic_core", "crew_lounge"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the holographic core logs the crew's viewing nights.",
		"message": "The holographic core learns what the crew like to watch.",
		"unlock_room_id": "crew_cinema",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "B299CE"
	},
	{
		"id": "physiotherapy",
		"name": "Physiotherapy",
		"rooms": ["med_bay", "crew_lounge"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while the med bay runs recovery sessions in the lounge.",
		"message": "Recovery exercises move out of the med bay and into the lounge.",
		"unlock_room_id": "crew_fitness",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "game_night",
		"name": "Game Night",
		"rooms": ["holographic_core", "crew_hab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the holographic core studies the crew at play.",
		"message": "BRINE starts keeping score, and learning from how the crew play.",
		"unlock_room_id": "games_room",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "B299CE"
	},
	{
		"id": "remembrance",
		"name": "Remembrance",
		"rooms": ["cryo_chamber", "med_center"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while the medical record keeps the names from cryo.",
		"message": "The medical record keeps the names of those still sleeping in cryo.",
		"unlock_room_id": "memorial_room",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "radio_hour",
		"name": "Radio Hour",
		"rooms": ["radio_lab", "crew_hab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the radio lab plays requests into the quarters.",
		"message": "Radio noise becomes music drifting through the bunks at night.",
		"unlock_room_id": "music_room",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "6C9DFF"
	},
	{
		"id": "lending_shelf",
		"name": "Lending Shelf",
		"rooms": ["data_archive", "crew_hab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while crew borrow and annotate the archive.",
		"message": "Crew notes start appearing in the margins of the archive.",
		"unlock_room_id": "reading_room",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "garden_tea",
		"name": "Garden Tea",
		"rooms": ["galley", "biodome"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while the galley brews from the biodome's herbs.",
		"message": "The galley learns which biodome leaves make a decent tea.",
		"unlock_room_id": "tea_lounge",
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "BFA76C"
	},
	{
		"id": "cell_service",
		"name": "Cell Service",
		"rooms": ["battery_array", "maintenance_bay"],
		"bonus": {"power": 1},
		"effect": "+1 Power per cycle while maintenance reconditions the battery cells.",
		"message": "Tired cells come back from maintenance holding a full charge.",
		"unlock_room_id": "battery_service_bay",
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "FFD65A"
	},
	{
		"id": "spare_parts_bench",
		"name": "Spare Parts Bench",
		"rooms": ["salvage_workshop", "maintenance_bay"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while salvage feeds the maintenance bench.",
		"message": "Salvaged parts go straight onto the maintenance bench.",
		"unlock_room_id": "droid_workshop",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "hangar_repairs",
		"name": "Hangar Repairs",
		"rooms": ["construction_drone_bay", "maintenance_bay"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while maintenance services the construction drones.",
		"message": "Construction drones return patched instead of grounded.",
		"unlock_room_id": "drone_repair_depot",
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "79B7A3"
	},
	{
		"id": "tuned_sensors",
		"name": "Tuned Sensors",
		"rooms": ["research_lab", "mining_drone_bay"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while research tunes the mining drones' sensors.",
		"message": "Mining drone sensors come back tuned, with cleaner readings.",
		"unlock_room_id": "sensor_calibration_lab",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "survey_lines",
		"name": "Survey Lines",
		"rooms": ["mining_drone_bay", "observation_room"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while observers chart the mining drones' survey lines.",
		"message": "Drone paths drawn from the window become the station's first survey map.",
		"unlock_room_id": "survey_probe_bay",
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	# Each new room's own recipe (owner-approved Sept 27), ending in a research payout.
	{
		"id": "echo_model",
		"name": "Echo Model",
		"rooms": ["echo_chamber", "holographic_core"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the holographic core models the chamber's echoes.",
		"message": "BRINE rebuilds each echo as a shape it can turn over and study.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "B299CE"
	},
	{
		"id": "folded_shielding",
		"name": "Folded Shielding",
		"rooms": ["fold_chamber", "shield_generator"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while folded space thickens the shield.",
		"message": "The shield borrows a crease from the fold chamber and holds harder.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "containment",
		"fx_color": "A982FF"
	},
	{
		"id": "deep_garden",
		"name": "Deep Garden",
		"rooms": ["pressure_garden", "biodome"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per cycle while pressure-grown cuttings take root in the biodome.",
		"message": "Cuttings from the pressure garden thrive under the dome.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "729278"
	},
	{
		"id": "tide_tables",
		"name": "Tide Tables",
		"rooms": ["stillwater_observatory", "data_archive"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the archive files the observatory's tide records.",
		"message": "Months of still-water readings settle into tide tables.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	{
		"id": "clean_burn",
		"name": "Clean Burn",
		"rooms": ["atmospheric_scrubber", "reactor"],
		"bonus": {"oxygen": 1},
		"effect": "+1 Oxygen per cycle while the scrubber cleans the reactor's exhaust air.",
		"message": "Reactor exhaust leaves the scrubber cleaner than it went in.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "75ABB3"
	},
	{
		"id": "compost_beds",
		"name": "Compost Beds",
		"rooms": ["habitat_recovery", "mycelium_nursery"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per cycle while recovered waste feeds the mycelium beds.",
		"message": "The mycelium spreads fastest through the station's recovered waste.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "729278"
	},
	{
		"id": "heirloom_beds",
		"name": "Heirloom Beds",
		"rooms": ["seed_vault", "biodome"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while vault seed restocks the biodome beds.",
		"message": "Seed kept in the vault comes back as a full harvest.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "BFA76C"
	},
	{
		"id": "clean_kitchen_water",
		"name": "Clean Kitchen Water",
		"rooms": ["water_reclamation", "galley"],
		"bonus": {"water": 1},
		"effect": "+1 Water per cycle while reclaimed water supplies the galley.",
		"message": "The galley cooks with reclaimed water and returns every drop.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "84938A"
	},
	{
		"id": "double_seal",
		"name": "Double Seal",
		"rooms": ["bulkhead_control", "airlock"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while bulkhead control backs up the airlock seals.",
		"message": "Every airlock cycle is checked twice, and nothing leaks.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "79B7A3"
	},
	{
		"id": "ore_manifest",
		"name": "Ore Manifest",
		"rooms": ["cargo_dispatch", "ore_refinery"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while dispatch schedules the refinery's ore.",
		"message": "Ore arrives at the refinery in the order it is needed.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "reactor_watch",
		"name": "Reactor Watch",
		"rooms": ["damage_control", "reactor"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while damage control stands watch on the reactor.",
		"message": "Damage control keeps a crew posted at the reactor.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "79B7A3"
	},
	{
		"id": "seabed_charts",
		"name": "Seabed Charts",
		"rooms": ["sonar_mapping", "mining_drone_bay"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while sonar charts guide the mining drones.",
		"message": "Mining drones follow the sonar charts straight to the richest seams.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "living_specimens",
		"name": "Living Specimens",
		"rooms": ["aquarium", "bio_lab"],
		"bonus": {"biomass": 1},
		"effect": "+1 Biomass per cycle while the bio lab cultures from the aquarium's tank.",
		"message": "The aquarium's tank turns out to be a culture bank.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "729278"
	},
	{
		"id": "painted_views",
		"name": "Painted Views",
		"rooms": ["art_studio", "observation_room"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while artists record what the window shows.",
		"message": "Paintings of the view outside catch details the logs missed.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	{
		"id": "hydrotherapy",
		"name": "Hydrotherapy",
		"rooms": ["bathhouse", "med_bay"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while the med bay prescribes the bathhouse.",
		"message": "Warm water does what painkillers could not.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "green_lungs",
		"name": "Green Lungs",
		"rooms": ["botanical_conservatory", "life_support"],
		"bonus": {"oxygen": 1},
		"effect": "+1 Oxygen per cycle while the conservatory breathes into life support.",
		"message": "The conservatory's plants become part of the air system.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "flow",
		"fx_color": "75ABB3"
	},
	{
		"id": "signal_reels",
		"name": "Signal Reels",
		"rooms": ["crew_cinema", "radio_lab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the cinema replays the radio lab's captures.",
		"message": "Old broadcasts play on the big screen, and someone notices a pattern.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "6C9DFF"
	},
	{
		"id": "morning_drills",
		"name": "Morning Drills",
		"rooms": ["crew_fitness", "crew_hab"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while the crew start each day with drills.",
		"message": "The crew wake to drills and work steadier for it.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "tournament_night",
		"name": "Tournament Night",
		"rooms": ["games_room", "crew_lounge"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while BRINE tracks the lounge tournaments.",
		"message": "The lounge standings become the most-read log on the station.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "B299CE"
	},
	{
		"id": "quiet_window",
		"name": "Quiet Window",
		"rooms": ["memorial_room", "observation_room"],
		"bonus": {"integrity": 1},
		"effect": "+1 Integrity per cycle while the crew keep a quiet watch at the window.",
		"message": "A place to sit by the window keeps the crew going.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "79B7A3"
	},
	{
		"id": "lounge_sessions",
		"name": "Lounge Sessions",
		"rooms": ["music_room", "crew_lounge"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while the lounge hosts the music room's sessions.",
		"message": "Players and listeners fill the lounge; BRINE records every session.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "6C9DFF"
	},
	{
		"id": "night_study",
		"name": "Night Study",
		"rooms": ["reading_room", "research_lab"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while researchers read late beside the lab.",
		"message": "Research continues after hours in the reading room.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "tea_break",
		"name": "Tea Break",
		"rooms": ["tea_lounge", "crew_lounge"],
		"bonus": {"food": 1},
		"effect": "+1 Food per cycle while the tea lounge serves the crew lounge.",
		"message": "Tea breaks turn into the station's best-attended meetings.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "care",
		"fx_color": "BFA76C"
	},
	{
		"id": "charge_rotation",
		"name": "Charge Rotation",
		"rooms": ["battery_service_bay", "solar_array"],
		"bonus": {"power": 1},
		"effect": "+1 Power per cycle while serviced cells rotate onto solar charge.",
		"message": "Batteries rotate through the solar array without a gap.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "power",
		"fx_color": "FFD65A"
	},
	{
		"id": "droid_assembly",
		"name": "Droid Assembly",
		"rooms": ["droid_workshop", "construction_drone_bay"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while the workshop fits out construction drones.",
		"message": "Workshop droids help assemble the construction drones.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "salvage_refit",
		"name": "Salvage Refit",
		"rooms": ["drone_repair_depot", "salvage_drone_bay"],
		"bonus": {"metal": 1},
		"effect": "+1 Metal per cycle while the depot refits salvage drones between runs.",
		"message": "Salvage drones come back from the depot ready for the next run.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "logistics",
		"fx_color": "B68D55"
	},
	{
		"id": "calibrated_hydrophones",
		"name": "Calibrated Hydrophones",
		"rooms": ["sensor_calibration_lab", "listening_post"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while calibrated hydrophones sharpen the listening post.",
		"message": "Calibrated hydrophones pick out sounds the post never heard.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "65A8FF"
	},
	{
		"id": "probe_soundings",
		"name": "Probe Soundings",
		"rooms": ["survey_probe_bay", "sonar_mapping"],
		"bonus": {"data": 1},
		"effect": "+1 Data per cycle while probes confirm the sonar map on site.",
		"message": "Probes drop where sonar pinged; the map stops guessing.",
		"terminal_reward": {"research": 3},
		"stabilize_cycles": 3,
		"fx_profile": "signal",
		"fx_color": "7BA7B9"
	},
	# ---- Patterns: three rooms joined through matching doors (owner-approved Sept 29). All three must
	# function; a pattern pays on top of any pair synergies among its rooms.
	{
		"id": "pattern_field_to_table", "kind": "pattern", "name": "Field to Table",
		"rooms": ["hydroponics_bay", "galley", "crew_lounge"],
		"bonus": {"food": 2},
		"effect": "+2 Food per functioning cycle when the Hydroponics Bay, Galley and Crew Lounge are joined through matching doors.",
		"message": "The salad reaches the table in the same shift it was harvested. Complaints have moved on to the salad.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "care", "fx_color": "BFA76C"
	},
	{
		"id": "pattern_greenhouse_deck", "kind": "pattern", "name": "Greenhouse Deck",
		"rooms": ["life_support", "biodome", "observation_room"],
		"bonus": {"oxygen": 2},
		"effect": "+2 Oxygen per functioning cycle when Life Support, the Biodome and the Observation Room are joined through matching doors.",
		"message": "The plants breathe, the crew watches them breathe, and the station pretends this was the plan.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "flow", "fx_color": "75ABB3"
	},
	{
		"id": "pattern_deep_survey", "kind": "pattern", "name": "Deep Survey",
		"rooms": ["mining_drone_bay", "observation_room", "data_archive"],
		"bonus": {"data": 2},
		"effect": "+2 Data per functioning cycle when the Mining Drone Bay, Observation Room and Data Archive are joined through matching doors.",
		"message": "The drone finds it, the window confirms it, the archive files it. Nobody is sure who asked.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "signal", "fx_color": "7BA7B9"
	},
	{
		"id": "pattern_smelting_line", "kind": "pattern", "name": "Smelting Line",
		"rooms": ["reactor", "mining_drone_bay", "ore_refinery"],
		"bonus": {"metal": 2},
		"effect": "+2 Metal per functioning cycle when the Reactor, Mining Drone Bay and Ore Refinery are joined through matching doors.",
		"message": "Ore goes in warm and comes out useful. The reactor takes the credit.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "logistics", "fx_color": "B68D55"
	},
	{
		"id": "pattern_steady_hands", "kind": "pattern", "name": "Steady Hands",
		"rooms": ["salvage_drone_bay", "maintenance_bay", "command_center"],
		"bonus": {"integrity": 1, "metal": 1},
		"effect": "+1 Integrity and +1 Metal per functioning cycle when the Salvage Drone Bay, Maintenance Bay and Command Center are joined through matching doors.",
		"message": "Repairs are assigned before the damage is admitted.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "containment", "fx_color": "8FB3A0"
	},
	{
		"id": "pattern_recovery_ward", "kind": "pattern", "name": "Recovery Ward",
		"rooms": ["crew_hab", "med_bay", "crew_lounge"],
		"bonus": {"integrity": 1, "food": 1},
		"effect": "+1 Integrity and +1 Food per functioning cycle when the Crew Hab, Med Bay and Crew Lounge are joined through matching doors.",
		"message": "A bed, a clinic and a couch within shouting distance. Recovery statistics have improved.",
		"terminal_reward": {"research": 5}, "stabilize_cycles": 3, "fx_profile": "care", "fx_color": "BFA76C"
	}
]

static func evaluate(placed_rooms: Array, occupied: Dictionary) -> Dictionary:
	var links := passage_links(occupied)
	var seen_links := {}
	for synergy in SYNERGIES:
		if synergy.get("via_passage", false) or is_pattern(synergy):
			continue
		var pairs := _find_adjacent_pairs(synergy["rooms"], occupied)
		for pair in pairs:
			if not within_passage_link(links, pair):
				_add_link(links, seen_links, synergy, pair)
	for synergy in SYNERGIES:
		if not is_pattern(synergy): continue
		for cells in _find_pattern_chains(synergy["rooms"], occupied):
			_add_link(links, seen_links, synergy, cells)
	for room in placed_rooms:
		if room["id"] != "cryo_chamber":
			continue
		var safe_wake := get_synergy("safe_wake_protocol")
		for neighbor_pos in _adjacent_tagged_cells(room["pos"], occupied, "medical"):
			_add_link(links, seen_links, safe_wake, [room["pos"], neighbor_pos])
	return {"links": links}

# Stabilized patterns pay double their authored bonus (owner playtest, Sept 17).
static func cycle_bonus(active_links, stabilized_ids: Dictionary = {}) -> Dictionary:
	var bonus := {}
	var sources: Array = active_links.values() if typeof(active_links) == TYPE_DICTIONARY else active_links
	for link in sources:
		var scale := 2 if stabilized_ids.has(str(link.get("id", ""))) else 1
		for key in link.get("bonus", {}):
			bonus[key] = bonus.get(key, 0) + link["bonus"][key] * scale
	return bonus

static func all_synergies() -> Array:
	return SYNERGIES

static func is_pattern(synergy: Dictionary) -> bool:
	return str(synergy.get("kind", "")) == "pattern"

# The three-room chains, and the two-room pairs, listed separately for the Codex.
static func patterns() -> Array:
	return SYNERGIES.filter(func(synergy: Dictionary) -> bool: return is_pattern(synergy))

static func pairs() -> Array:
	return SYNERGIES.filter(func(synergy: Dictionary) -> bool: return not is_pattern(synergy))

static func get_synergy(id: String) -> Dictionary:
	for synergy in SYNERGIES:
		if synergy["id"] == id:
			return synergy
	return {}

static func involves_room(synergy: Dictionary, room_id: String) -> bool:
	return synergy.get("rooms", []).has(room_id) or (synergy.get("via_passage", false) and PASSAGE_IDS.has(room_id))

# Shared by evaluation and hover previews, without scanning unrelated recipes on hover.
static func passage_links(occupied: Dictionary) -> Array:
	var links := []
	var seen := {}
	for synergy in SYNERGIES:
		if not synergy.get("via_passage", false):
			continue
		for cells in _find_passage_pairs(synergy.rooms, occupied):
			_add_link(links, seen, synergy, cells)
	return links

# A corridor already paying Parts Passage does not also pay Logistics Spine for the same
# storage bay (owner, Sept 27): an adjacent pair inside one passage link does not stack.
static func within_passage_link(links: Array, pair: Array) -> bool:
	for link in links:
		if link.get("via_passage", false) and link.cells.has(pair[0]) and link.cells.has(pair[1]):
			return true
	return false

# Endpoints stay first for pair identity; the passage is also a required functioning cell.
# Only a single passage is traversed. A tee can serve distinct workshops, never a chain.
static func _find_passage_pairs(room_ids: Array, occupied: Dictionary) -> Array:
	var pairs := []
	for pos in occupied:
		var passage: Dictionary = occupied[pos]
		if not PASSAGE_IDS.has(str(passage.get("id", ""))):
			continue
		var starts := []
		var ends := []
		for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
			var neighbor_pos: Vector2i = pos + offset
			var neighbor: Dictionary = occupied.get(neighbor_pos, {})
			if not _rooms_connected(passage, neighbor, offset):
				continue
			if neighbor.get("id", "") == room_ids[0]:
				starts.append(neighbor_pos)
			elif neighbor.get("id", "") == room_ids[1]:
				ends.append(neighbor_pos)
		for start in starts:
			for end in ends:
				pairs.append([start, end, pos])
	return pairs

# A pattern's three rooms must form one connected cluster: some room among them connects through
# matching doors to both of the others. Dead-end rooms (one door) can only be an end, so the middle is
# whichever of the three has the doors. Cells come back as [end, middle, end]; a cluster found from
# more than one middle is one link (the key sorts the cells).
static func _find_pattern_chains(room_ids: Array, occupied: Dictionary) -> Array:
	var chains := []
	for middle_index in [1, 0, 2]:
		var end_ids := []
		for index in range(3):
			if index != middle_index: end_ids.append(room_ids[index])
		for pos in occupied:
			var middle: Dictionary = occupied[pos]
			if str(middle.get("id", "")) != room_ids[middle_index]:
				continue
			var starts := []
			var ends := []
			for offset in [Vector2i.LEFT, Vector2i.RIGHT, Vector2i.UP, Vector2i.DOWN]:
				var neighbor_pos: Vector2i = pos + offset
				var neighbor: Dictionary = occupied.get(neighbor_pos, {})
				if not _rooms_connected(middle, neighbor, offset):
					continue
				if str(neighbor.get("id", "")) == end_ids[0]:
					starts.append(neighbor_pos)
				elif str(neighbor.get("id", "")) == end_ids[1]:
					ends.append(neighbor_pos)
			for start in starts:
				for end in ends:
					chains.append([start, pos, end])
	return chains

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
	var key := "%s:%s" % [synergy["id"], _cell_pair_key(cells[0], cells[1]) if cells.size() == 2 or is_pattern(synergy) == false else _chain_key(cells)]
	if seen_links.has(key):
		return
	seen_links[key] = true
	var link := synergy.duplicate(true)
	link["cells"] = cells.duplicate()
	link["key"] = key
	links.append(link)

static func _chain_key(cells: Array) -> String:
	var parts := []
	for cell in cells: parts.append("%d,%d" % [cell.x, cell.y])
	parts.sort()
	return "-".join(parts)

static func _cell_pair_key(a: Vector2i, b: Vector2i) -> String:
	var first := a
	var second := b
	if b.x < a.x or (b.x == a.x and b.y < a.y):
		first = b
		second = a
	return "%d,%d-%d,%d" % [first.x, first.y, second.x, second.y]
