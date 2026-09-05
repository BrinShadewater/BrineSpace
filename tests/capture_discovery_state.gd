extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")
const TEST_SAVE_PATH := "user://brine_discovery_visual_test.json"

func _init() -> void:
	call_deferred("_stage")

func _stage() -> void:
	seed(4404)
	var game = MainScene.instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	game.testing_free_build = true
	game.meta.save_path = TEST_SAVE_PATH
	game.rng.seed = 4404
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._place_room("life_support", Vector2i(19, 20), true)
	game._place_room("hydroponics_bay", Vector2i(18, 20), true)
	for room_value in game.placed_rooms:
		game.powered_room_cells[room_value["pos"]] = true
	game.active_synergy_links = DiscoveryManagerScript.functioning_links(game.connected_synergy_links, game.powered_room_cells)
	for link in game.active_synergy_links:
		game.active_synergies[link["id"]] = link
	var state := "active"
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--state="):
			state = argument.trim_prefix("--state=")
	match state:
		"unknown":
			game.meta.discovered_synergy_ids.erase("closed_air_loop")
		"dormant":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.active_synergy_links.clear()
			game.active_synergies.clear()
		"stabilizing":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.synergy_stabilization_progress["closed_air_loop"] = 2
		"active":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.meta.stabilized_synergy_ids["closed_air_loop"] = true
		"journal":
			game.meta.discovered_synergy_ids["closed_air_loop"] = true
			game.synergy_stabilization_progress["closed_air_loop"] = 2
			game._toggle_journal()
	print("Visual scenario: ", state)
	game.hand.assign(["hydroponics_bay", "life_support", "biodome"])
	game.prototype_card_seen_cycle["biodome"] = 0
	game.selected_card_id = ""
	game.hover_cell = Vector2i(18, 20)
	game._refresh_all()
	game._fit_station_view.call_deferred()
	_remove_test_save()

func _remove_test_save() -> void:
	if FileAccess.file_exists(TEST_SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_SAVE_PATH))
