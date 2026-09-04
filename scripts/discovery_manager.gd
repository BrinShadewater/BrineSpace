extends RefCounted
class_name DiscoveryManager

static func functioning_links(connected_links: Array, powered_cells: Dictionary) -> Array:
	var functioning := []
	for link_value in connected_links:
		var link: Dictionary = link_value
		var cells: Array = link.get("cells", [])
		if cells.size() >= 2 and powered_cells.has(cells[0]) and powered_cells.has(cells[1]):
			functioning.append(link)
	return functioning

static func validate_unlock_graph(all_rooms: Dictionary, synergies: Array, foundation_ids: Array) -> PackedStringArray:
	var errors := PackedStringArray()
	var reachable := {"brine_core": true}
	for id_value in foundation_ids:
		var room_id := str(id_value)
		if not all_rooms.has(room_id):
			errors.append("Unknown foundation room: %s" % room_id)
		else:
			reachable[room_id] = true
	for synergy_value in synergies:
		var synergy: Dictionary = synergy_value
		var reward_id := str(synergy.get("unlock_room_id", ""))
		if not reward_id.is_empty() and not all_rooms.has(reward_id):
			errors.append("Unknown unlock target: %s" % reward_id)
	var changed := true
	while changed:
		changed = false
		for synergy_value in synergies:
			var synergy: Dictionary = synergy_value
			var reward_id := str(synergy.get("unlock_room_id", ""))
			if reward_id.is_empty() or reachable.has(reward_id):
				continue
			var requirements_met := true
			for room_id_value in synergy.get("rooms", []):
				if not reachable.has(str(room_id_value)):
					requirements_met = false
					break
			if requirements_met:
				reachable[reward_id] = true
				changed = true
	for room_id_value in all_rooms:
		var room_id := str(room_id_value)
		if not reachable.has(room_id):
			errors.append("Unreachable room: %s" % room_id)
	return errors
