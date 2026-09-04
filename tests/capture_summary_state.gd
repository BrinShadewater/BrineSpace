extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const TEST_SAVE_PATH := "user://brine_summary_test_save.json"

func _init() -> void:
	call_deferred("_stage_summary")

func _stage_summary() -> void:
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game.meta.save_path = TEST_SAVE_PATH
	game.meta.doctrine_mastery.clear()
	game.meta.total_victories = 0
	game.pending_doctrines.assign(["industry", "biosphere"])
	game._confirm_doctrines()
	game.completed_directives.assign(["RESTORE A FOOTHOLD", "PROVE THE PATTERN", "ACHIEVE HARMONIC STATION"])
	game.cycle = 34
	game.resonance_score = 220
	game.resonance_tier_index = 3
	game.links_formed = 14
	game.largest_cascade = 3
	game.resources["data"] = 18
	game.completed_pois.assign(["Asteroid Field", "Derelict Freighter"])
	game._show_reboot_summary("All reconstruction directives complete. BRINE has stabilized this orbital sector.", true)
	if FileAccess.file_exists(TEST_SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_SAVE_PATH))
