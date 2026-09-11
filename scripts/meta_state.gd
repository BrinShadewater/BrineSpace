extends RefCounted
class_name MetaState

const RoomDatabaseScript := preload("res://scripts/room_database.gd")

var unlocked_room_ids := {}
var discovered_synergy_ids := {}
var stabilized_synergy_ids := {}
var total_research_points := 0
var recovered_memory_ids := {}
var brine_upgrades := {}
var doctrine_mastery := {}
var total_victories := 0
var unread_records := {}
var guide_completed := false
var unlocked_architect_ids := {"bill":true}
var selected_architect := "bill"
var unlocked_companion_ids := {}
var selected_companion_ids: Array = []
var last_error := ""
var recovered_backup := false

func unlock_companion(id: String) -> bool:
	if id not in ["river","josh","margot"] or unlocked_companion_ids.has(id):return false
	unlocked_companion_ids[id]=true
	if save_to_disk()!=OK:
		unlocked_companion_ids.erase(id);return false
	return true

func unlock_architect(id: String) -> bool:
	if not preload("res://scripts/architects.gd").IDS.has(id) or unlocked_architect_ids.has(id): return false
	unlocked_architect_ids[id]=true
	save_to_disk()
	return true

func select_architect(id: String, companions: Variant = null) -> bool:
	if not unlocked_architect_ids.has(id): return false
	var previous_companions := selected_companion_ids.duplicate()
	if companions != null:
		if not companions is Array:return false
		for companion in companions:
			if companion not in ["river","josh","margot"] or not unlocked_companion_ids.has(companion) or companions.count(companion)!=1:return false
		selected_companion_ids=companions.duplicate()
	var previous := selected_architect
	selected_architect=id
	if save_to_disk() != OK:
		selected_architect = previous
		selected_companion_ids=previous_companions
		return false
	return true

func mark_reviewed(key: String) -> void:
	if unread_records.erase(key):
		save_to_disk()
var save_path := "user://brine_save.json":
	set(value):
		# Redirecting the save (fixtures do this) must not leak the previously loaded
		# profile: reset to defaults and load the new path instead.
		var changed := save_path != value
		save_path = value
		if changed and _profile_loaded:
			_reset_profile()
			load_from_disk()
var _profile_loaded := false

const DOCTRINE_RANK_THRESHOLDS := [0, 2, 5, 9, 14]

func _init() -> void:
	for id in RoomDatabaseScript.STARTING_UNLOCKS:
		unlocked_room_ids[id] = true
	load_from_disk()
	_profile_loaded = true

func _reset_profile() -> void:
	unlocked_room_ids = {}
	for id in RoomDatabaseScript.STARTING_UNLOCKS:
		unlocked_room_ids[id] = true
	discovered_synergy_ids = {}
	stabilized_synergy_ids = {}
	total_research_points = 0
	recovered_memory_ids = {}
	brine_upgrades = {}
	doctrine_mastery = {}
	total_victories = 0
	unread_records = {}
	guide_completed = false
	unlocked_architect_ids = {"bill":true}
	selected_architect = "bill"
	unlocked_companion_ids = {}
	selected_companion_ids = []
	last_error = ""
	recovered_backup = false

func unlock_room(id: String) -> bool:
	if unlocked_room_ids.has(id):
		return false
	unlocked_room_ids[id] = true
	unread_records["room:" + id] = true
	save_to_disk()
	return true

func discover_synergy(id: String) -> bool:
	if discovered_synergy_ids.has(id):
		return false
	discovered_synergy_ids[id] = true
	unread_records["synergy:" + id] = true
	save_to_disk()
	return true

func stabilize_synergy(id: String) -> bool:
	if stabilized_synergy_ids.has(id):
		return false
	stabilized_synergy_ids[id] = true
	unread_records["synergy:" + id] = true
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
		var previous_rank := get_doctrine_rank(id)
		doctrine_mastery[id] = int(doctrine_mastery.get(id, 0)) + mastery_gain
		if get_doctrine_rank(id) > previous_rank:
			unread_records["mastery:" + id] = true
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

func save_to_disk() -> Error:
	last_error = ""
	var data := {
		"unlocked_architect_ids":unlocked_architect_ids.keys(),
		"selected_architect":selected_architect,
		"unlocked_companion_ids":unlocked_companion_ids.keys(),
		"selected_companion_ids":selected_companion_ids,
		"unread_records": unread_records.keys(),
		"guide_completed": guide_completed,
		"unlocked_room_ids": unlocked_room_ids.keys(),
		"discovered_synergy_ids": discovered_synergy_ids.keys(),
		"stabilized_synergy_ids": stabilized_synergy_ids.keys(),
		"total_research_points": total_research_points,
		"recovered_memory_ids": recovered_memory_ids.keys(),
		"brine_upgrades": brine_upgrades.keys(),
		"doctrine_mastery": doctrine_mastery,
		"total_victories": total_victories
	}
	var temp := save_path + ".tmp"
	var backup := save_path + ".bak"
	var file := FileAccess.open(temp, FileAccess.WRITE)
	if file == null: return _save_failed(FileAccess.get_open_error(), "Cannot write progression record. Check storage access and retry Save Game.")
	file.store_string(JSON.stringify(data, "\t"))
	file.flush()
	var error := file.get_error()
	file.close()
	if error != OK: return _save_failed(error, "Progression write failed. Previous record retained; retry Save Game.")
	if FileAccess.file_exists(save_path):
		# Never overwrite a good backup with a damaged primary record.
		if _read_record(save_path) is Dictionary:
			error = DirAccess.copy_absolute(save_path, backup)
			if error != OK: return _save_failed(error, "Cannot protect previous progression record. Retry Save Game.")
		error = DirAccess.remove_absolute(save_path)
		if error != OK: return _save_failed(error, "Cannot replace progression record. Retry Save Game.")
	error = DirAccess.rename_absolute(temp, save_path)
	if error != OK:
		if FileAccess.file_exists(backup): DirAccess.copy_absolute(backup, save_path)
		return _save_failed(error, "Progression replacement failed. Recovery record retained; retry Save Game.")
	recovered_backup = false
	return OK

func _save_failed(error: Error, message: String) -> Error:
	last_error = message
	return error

static func _read_record(path: String) -> Variant:
	if not FileAccess.file_exists(path): return null
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null: return null
	var parser := JSON.new()
	if parser.parse(file.get_as_text()) != OK: return null
	return parser.data

func load_from_disk() -> void:
	last_error = ""
	recovered_backup = false
	var parsed = _read_record(save_path)
	if not parsed is Dictionary:
		parsed = _read_record(save_path + ".bak")
		recovered_backup = parsed is Dictionary
	if not parsed is Dictionary:
		if FileAccess.file_exists(save_path) or FileAccess.file_exists(save_path + ".bak"):
			last_error = "Progression record unreadable. No usable recovery record found."
		return
	for id in _saved_ids(parsed, "unlocked_architect_ids"):
		if preload("res://scripts/architects.gd").IDS.has(id): unlocked_architect_ids[id]=true
	for id in _saved_ids(parsed,"unlocked_companion_ids"):
		if id in ["river","josh","margot"]:unlocked_companion_ids[id]=true
	selected_companion_ids.clear()
	for id in _saved_ids(parsed,"selected_companion_ids"):
		if unlocked_companion_ids.has(id) and not selected_companion_ids.has(id):selected_companion_ids.append(id)
	var selected: String=str(parsed.get("selected_architect","bill"))
	selected_architect=selected if unlocked_architect_ids.has(selected) else "bill"
	for key in _saved_ids(parsed, "unread_records"):
		unread_records[str(key)] = true
	guide_completed = bool(parsed.get("guide_completed", not _saved_ids(parsed, "discovered_synergy_ids").is_empty()))
	for id in _saved_ids(parsed, "unlocked_room_ids"):
		unlocked_room_ids[str(id)] = true
	for id in _saved_ids(parsed, "discovered_synergy_ids"):
		discovered_synergy_ids[str(id)] = true
	for id in _saved_ids(parsed, "stabilized_synergy_ids"):
		stabilized_synergy_ids[str(id)] = true
	total_research_points = _saved_count(parsed.get("total_research_points", 0))
	for id in _saved_ids(parsed, "recovered_memory_ids"):
		recovered_memory_ids[str(id)] = true
	for id in _saved_ids(parsed, "brine_upgrades"):
		brine_upgrades[str(id)] = true
	var parsed_mastery = parsed.get("doctrine_mastery", {})
	if typeof(parsed_mastery) == TYPE_DICTIONARY:
		for id in parsed_mastery:
			doctrine_mastery[str(id)] = _saved_count(parsed_mastery[id])
	total_victories = _saved_count(parsed.get("total_victories", 0))

# Damaged optional fields must not prevent the remaining records from loading.
static func _saved_ids(data: Dictionary, key: String) -> Array:
	var value = data.get(key, [])
	if not value is Array: return []
	return value.filter(func(id): return id is String and not id.is_empty())

static func _saved_count(value: Variant) -> int:
	if not (value is int or value is float): return 0
	if not is_finite(float(value)): return 0
	return clampi(int(value), 0, 2147483647)
