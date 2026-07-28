extends RefCounted
class_name MetaState

const RoomDatabaseScript := preload("res://scripts/room_database.gd")

var unlocked_room_ids := {}
var discovered_synergy_ids := {}
var total_research_points := 0
var recovered_memory_ids := {}
var brine_upgrades := {}
var save_path := "user://brine_save.json"

func _init() -> void:
	for id in RoomDatabaseScript.STARTING_UNLOCKS:
		unlocked_room_ids[id] = true
	load_from_disk()

func unlock_room(id: String) -> bool:
	if unlocked_room_ids.has(id):
		return false
	unlocked_room_ids[id] = true
	save_to_disk()
	return true

func discover_synergy(id: String) -> bool:
	if discovered_synergy_ids.has(id):
		return false
	discovered_synergy_ids[id] = true
	save_to_disk()
	return true

func add_research_points(amount: int) -> void:
	total_research_points += max(amount, 0)
	save_to_disk()

func save_to_disk() -> void:
	var data := {
		"unlocked_room_ids": unlocked_room_ids.keys(),
		"discovered_synergy_ids": discovered_synergy_ids.keys(),
		"total_research_points": total_research_points,
		"recovered_memory_ids": recovered_memory_ids.keys(),
		"brine_upgrades": brine_upgrades.keys()
	}
	var file := FileAccess.open(save_path, FileAccess.WRITE)
	if file == null:
		return
	file.store_string(JSON.stringify(data, "\t"))

func load_from_disk() -> void:
	if not FileAccess.file_exists(save_path):
		return
	var file := FileAccess.open(save_path, FileAccess.READ)
	if file == null:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return
	for id in parsed.get("unlocked_room_ids", []):
		unlocked_room_ids[str(id)] = true
	for id in parsed.get("discovered_synergy_ids", []):
		discovered_synergy_ids[str(id)] = true
	total_research_points = int(parsed.get("total_research_points", 0))
	for id in parsed.get("recovered_memory_ids", []):
		recovered_memory_ids[str(id)] = true
	for id in parsed.get("brine_upgrades", []):
		brine_upgrades[str(id)] = true
