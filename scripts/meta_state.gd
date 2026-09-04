extends RefCounted
class_name MetaState

const RoomDatabaseScript := preload("res://scripts/room_database.gd")

var unlocked_room_ids := {}
var discovered_synergy_ids := {}
var total_research_points := 0
var recovered_memory_ids := {}
var brine_upgrades := {}
var doctrine_mastery := {}
var total_victories := 0
var save_path := "user://brine_save.json"

const DOCTRINE_RANK_THRESHOLDS := [0, 2, 5, 9, 14]

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

func record_run(doctrine_ids: Array, victory: bool, resonance_score: int) -> int:
	var mastery_gain := 0
	if victory:
		mastery_gain = 2
		total_victories += 1
	elif resonance_score >= 30:
		mastery_gain = 1
	for id_value in doctrine_ids:
		var id := str(id_value)
		doctrine_mastery[id] = int(doctrine_mastery.get(id, 0)) + mastery_gain
	save_to_disk()
	return mastery_gain

func get_doctrine_mastery(doctrine_id: String) -> int:
	return int(doctrine_mastery.get(doctrine_id, 0))

func get_doctrine_rank(doctrine_id: String) -> int:
	var mastery := get_doctrine_mastery(doctrine_id)
	var rank := 0
	for i in range(DOCTRINE_RANK_THRESHOLDS.size()):
		if mastery >= DOCTRINE_RANK_THRESHOLDS[i]:
			rank = i
	return rank

func get_next_doctrine_rank_threshold(doctrine_id: String) -> int:
	var rank := get_doctrine_rank(doctrine_id)
	if rank + 1 >= DOCTRINE_RANK_THRESHOLDS.size():
		return -1
	return DOCTRINE_RANK_THRESHOLDS[rank + 1]

func save_to_disk() -> void:
	var data := {
		"unlocked_room_ids": unlocked_room_ids.keys(),
		"discovered_synergy_ids": discovered_synergy_ids.keys(),
		"total_research_points": total_research_points,
		"recovered_memory_ids": recovered_memory_ids.keys(),
		"brine_upgrades": brine_upgrades.keys(),
		"doctrine_mastery": doctrine_mastery,
		"total_victories": total_victories
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
	var parsed_mastery = parsed.get("doctrine_mastery", {})
	if typeof(parsed_mastery) == TYPE_DICTIONARY:
		for id in parsed_mastery:
			doctrine_mastery[str(id)] = max(0, int(parsed_mastery[id]))
	total_victories = max(0, int(parsed.get("total_victories", 0)))
