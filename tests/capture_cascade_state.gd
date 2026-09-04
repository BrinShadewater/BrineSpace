extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const TEST_SAVE_PATH := "user://brine_visual_test_save.json"

func _init() -> void:
	call_deferred("_stage_cascade")

func _stage_cascade() -> void:
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game.meta.save_path = TEST_SAVE_PATH
	game.meta.discovered_synergy_ids.clear()
	game.pending_doctrines.assign(["industry", "biosphere"])
	game._confirm_doctrines()
	game._place_room("life_support", Vector2i(19, 20))
	game._place_room("crew_hab", Vector2i(17, 20))
	game._place_room("hydroponics_bay", Vector2i(18, 20))
	game.selected_card_id = ""
	game.hover_cell = Vector2i(18, 20)
	game._refresh_all()
	game._center_grid_on_station_deferred()
	if FileAccess.file_exists(TEST_SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_SAVE_PATH))
