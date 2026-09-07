extends SceneTree
func _init() -> void:
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
