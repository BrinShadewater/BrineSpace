extends SceneTree

class CountingMeta extends "res://scripts/meta_state.gd":
	var writes := 0
	var fail_write := false
	func save_to_disk() -> Error:
		writes += 1
		if fail_write: return ERR_CANT_CREATE
		return super.save_to_disk()

func _test_stabilization_reward() -> void:
	var meta := CountingMeta.new()
	meta.save_path = "user://stabilization_reward_test.json"
	var awarded := meta.stabilize_synergy("power_bridge", 5)
	assert(awarded and meta.writes == 1)
	var restored := preload("res://scripts/meta_state.gd").new()
	restored.save_path = meta.save_path
	restored.load_from_disk()
	assert(restored.stabilized_synergy_ids.has("power_bridge") and restored.total_research_points == 5)
	var duplicate := meta.stabilize_synergy("power_bridge", 5)
	assert(not duplicate and meta.writes == 1 and meta.total_research_points == 5)
	var legacy := meta.stabilize_synergy("legacy_pattern")
	assert(legacy and meta.writes == 2 and meta.total_research_points == 5)
	var negative := meta.stabilize_synergy("negative_reward", -3)
	assert(negative and meta.writes == 3 and meta.total_research_points == 5)
	var disk_before := FileAccess.get_file_as_string(meta.save_path)
	meta.fail_write = true
	var failed := meta.stabilize_synergy("failed_write", 7)
	# Preserve existing mutation-on-write-failure behavior; prior disk stays intact.
	assert(failed and meta.writes == 4 and meta.total_research_points == 12)
	assert(FileAccess.get_file_as_string(meta.save_path) == disk_before)
	meta.fail_write = false
	var retry := meta.save_to_disk()
	assert(retry == OK and meta.writes == 5)
	restored.load_from_disk()
	assert(restored.stabilized_synergy_ids.has("failed_write") and restored.total_research_points == 12)
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(meta.save_path + suffix): DirAccess.remove_absolute(meta.save_path + suffix)

func _init() -> void:
	_test_stabilization_reward()
	var meta = preload("res://scripts/meta_state.gd").new()
	meta.save_path = "user://meta_field_validation_test.json"
	var file := FileAccess.open(meta.save_path,FileAccess.WRITE)
	file.store_string(JSON.stringify({"unlocked_architect_ids":null,"unread_records":12,"discovered_synergy_ids":{},"unlocked_room_ids":["research_lab",null,7],"total_research_points":{},"total_victories":-3,"doctrine_mastery":{"industry":[]},"recovered_memory_ids":false,"brine_upgrades":"bad"}))
	file.close()
	meta.load_from_disk()
	assert(meta.unlocked_room_ids.has("research_lab"))
	assert(not meta.unlocked_room_ids.has("7"))
	assert(meta.selected_architect == "bill")
	assert(meta.total_research_points == 0 and meta.total_victories == 0)
	assert(meta.get_doctrine_mastery("industry") == 0)
	DirAccess.remove_absolute(meta.save_path)
	print("META FIELD VALIDATION PASS")
	quit()
