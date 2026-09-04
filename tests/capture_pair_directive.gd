extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const TEST_SAVE_PATH := "user://brine_pair_directive_visual_save.json"

func _init() -> void:
	call_deferred("_stage_pair_directive")

func _stage_pair_directive() -> void:
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game.meta.save_path = TEST_SAVE_PATH
	game.pending_doctrines.assign(["science", "anomaly"])
	game._confirm_doctrines()
	game.directive_index = 1
	game.cycle = 14
	game._place_room("xeno_lab", Vector2i(19, 20), true)
	game._place_room("research_lab", Vector2i(18, 20), true)
	game.selected_card_id = "solar_array"
	game.hover_cell = Vector2i(20, 19)
	game._refresh_all()
	game._center_grid_on_station_deferred()
	if FileAccess.file_exists(TEST_SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_SAVE_PATH))
