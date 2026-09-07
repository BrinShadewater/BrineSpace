extends RefCounted
const Rooms = preload("res://scripts/room_database.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const CLUES := {
	"substrate_recovery": "Discarded growing cultures may still be useful on the other side of containment.",
	"culture_exchange": "Let the station's fungal growth meet a place that studies living tissue.",
	"restorative_culture": "Some cultures belong near the wounded, rather than in the disposal stream.",
	"closed_air_loop": "Plants and breathable air share a debt. Look for the water they leave behind.",
	"green_commons": "The crew might eat better if something green grew closer to home.",
	"industrial_chain": "Raw ore is only the beginning. Shorten the route from extraction to processing.",
	"stable_power_flow": "A restless power source needs somewhere nearby to put its excess.",
	"research_pipeline": "An experiment becomes useful when its findings have somewhere to stay.",
	"safe_wake_protocol": "Before waking the sleepers, consider what they will breathe.",
	"containment_sector": "The unfamiliar samples should not travel far before they can be isolated.",
	"crew_commons": "Survival is not the only reason people leave their quarters.",
	"field_clinic": "A long walk from home is an unhelpful feature of emergency care.",
	"shielded_reactor": "The most energetic machinery may benefit from a protective neighbor.",
	"signal_command": "Listening is one task. Deciding what the signal means is another.",
	"drone_foundry": "Machines returning with salvage should not travel far for repairs.",
	"living_circuit": "Living tissue and projected computation may have something to say to each other.",
	"biodome_atmosphere": "A larger enclosed ecosystem could help the machinery that keeps the air moving.",
	"core_relay": "BRINE's thoughts require a shorter route to station control.",
	"logistics_spine": "Stores are useful only if there is a working route out of them.",
	"medical_network": "Treatment and clinical administration should not work in isolation.",
	"clinical_airlock": "Recovery depends on more than medicine. Clean air is a reasonable beginning.",
	"ore_buffer": "Extraction becomes less wasteful when the next shipment has somewhere close to wait.",
	"load_balancing": "Two different ways to generate power may smooth each other's weaknesses.",
	"core_diagnostics": "BRINE has questions about its own condition. Put an investigator within reach.",
	"sterile_observation": "Study the isolated specimens without making the rest of the station part of the experiment.",
	"signal_triangulation": "A signal received is not yet a signal understood.",
	"genomic_triage": "Replacement tissue is more useful when complex care can reach it.",
	"impossible_model": "Something inexplicable may become visible inside a projected model."
}

static func clue(pattern: Dictionary) -> String:
	return CLUES.get(pattern.id, "Keep complementary neighboring systems functioning. An unfamiliar pattern may emerge.")

static func room_entries(meta_state) -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var rooms: Dictionary = Rooms.all_rooms()
	var ids := rooms.keys()
	ids.sort()
	for index in range(ids.size()):
		var id: String = ids[index]
		var room: Dictionary = rooms[id]
		var known: bool = id == "brine_core" or meta_state.unlocked_room_ids.has(id)
		var hint := "Explore functioning room combinations. Stabilize a pattern to recover its blueprint."
		for pattern in Synergies.all_synergies():
			if pattern.get("unlock_room_id", "") == id:
				if meta_state.discovered_synergy_ids.has(pattern.id) or meta_state.stabilized_synergy_ids.has(pattern.id):
					hint = 'Stabilize "%s": keep its linked rooms functioning for %d consecutive cycles.' % [pattern.name, pattern.get("stabilize_cycles", 3)]
				else:
					hint = clue(pattern) + " Keep the resulting link functioning for three consecutive cycles."
				break
		entries.append({"id": id, "known": known, "title": room.display_name if known else "UNRECOVERED ROOM // %02d" % (index + 1),
			"category": room.category, "clue": hint, "data": room})
	return entries

static func synergy_entries(meta_state) -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var patterns: Array = Synergies.all_synergies()
	for index in range(patterns.size()):
		var pattern: Dictionary = patterns[index]
		var known: bool = meta_state.discovered_synergy_ids.has(pattern.id) or meta_state.stabilized_synergy_ids.has(pattern.id)
		entries.append({"id": pattern.id, "known": known, "title": pattern.name if known else "UNIDENTIFIED PATTERN // %02d" % (index + 1),
			"category": "SYNERGY", "clue": clue(pattern), "data": pattern})
	return entries

