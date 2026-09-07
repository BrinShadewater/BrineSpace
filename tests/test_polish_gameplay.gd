extends SceneTree

const MainScript := preload("res://scripts/main.gd")
const Rooms := preload("res://scripts/room_database.gd")
const Synergies := preload("res://scripts/synergy_manager.gd")
const Runs := preload("res://scripts/run_manager.gd")
var failures := 0

func _init() -> void:
	_test_water_opens_the_bio_chain()
	_test_every_doctrine_can_feed_and_support_crew()
	_test_placement_checks_every_neighbor()
	_test_starved_rooms_stop_and_share_inputs()
	_test_forecast_matches_functioning_production()
	_test_unlearned_forecast_does_not_reveal_bonus()
	_test_power_loss_resets_real_discovery_progress()
	_test_orbit_rewards_do_not_bypass_discovery()
	_test_containment_cleans_corruption()
	_test_bursts_expire_without_advancing_paused_motion()
	if failures > 0:
		push_error("Gameplay polish tests failed: %d" % failures)
	quit(1 if failures > 0 else 0)
	if failures == 0:
		print("Gameplay polish tests passed.")

func _game():
	var game = MainScript.new()
	game.meta.save_path = "user://brine_polish_gameplay_test.json"
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.unlocked_room_ids.clear()
	for id in Rooms.STARTING_UNLOCKS:
		game.meta.unlocked_room_ids[id] = true
	return game

func _dispose(game) -> void:
	var path: String = game.meta.save_path
	game.free()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _room(game, id: String, cell: Vector2i, rotation := 0) -> void:
	var room := Rooms.get_room(id).duplicate(true)
	room["pos"] = cell
	room["rotation"] = rotation
	game.placed_rooms.append(room)
	game.occupied[cell] = room
	game._check_synergies()

func _test_water_opens_the_bio_chain() -> void:
	var game = _game()
	_room(game, "reactor", Vector2i(10, 11))
	_room(game, "hydroponics_bay", Vector2i(10, 10))
	_room(game, "life_support", Vector2i(11, 10))
	for index in range(3):
		game.cycle = index + 1
		game._apply_room_economy()
		game._advance_synergy_discovery_cycle()
	_expect(game.meta.unlocked_room_ids.has("biodome"), "three actual powered cycles unlock Biodome")
	_expect(game.resources["water"] >= Rooms.get_room("biodome")["cost"]["water"], "discovery produces enough water to try its prototype")
	_dispose(game)

func _test_every_doctrine_can_feed_and_support_crew() -> void:
	var unlocked := {}
	for id in Rooms.STARTING_UNLOCKS:
		unlocked[id] = true
	for first in range(Runs.DOCTRINE_ORDER.size()):
		for second in range(first + 1, Runs.DOCTRINE_ORDER.size()):
			var deck := Runs.build_deck([Runs.DOCTRINE_ORDER[first], Runs.DOCTRINE_ORDER[second]], unlocked)
			_expect(deck.has("hydroponics_bay") and deck.has("life_support"), "all doctrine pairs need a survival route")

func _test_placement_checks_every_neighbor() -> void:
	var game = _game()
	game.testing_free_build = true
	_room(game, "corridor", Vector2i(9, 10)) # north/south: does not connect east
	_room(game, "storage_bay", Vector2i(11, 10))
	_expect(game.get_placement_problem("life_support", Vector2i(10, 10)).is_empty(), "a valid east door works despite a closed west neighbor")
	_dispose(game)

func _test_starved_rooms_stop_and_share_inputs() -> void:
	var game = _game()
	_room(game, "reactor", Vector2i(10, 10))
	_room(game, "biodome", Vector2i(10, 11))
	game.resources["water"] = 0
	var food_before: int = game.resources["food"]
	game._apply_room_economy()
	_expect(game.resources["water"] == 0 and game.resources["food"] == food_before, "a dry biodome must neither consume negative water nor produce food")
	_expect(not game.powered_room_cells.has(Vector2i(10, 11)), "input-starved rooms must not count as functioning")
	_room(game, "clone_lab", Vector2i(11, 10))
	_room(game, "clone_lab", Vector2i(12, 10))
	game.resources["biomass"] = 1
	game.resources["data"] = 1
	game._apply_room_economy()
	_expect(game.resources["biomass"] >= 0 and game.crew_count <= 1, "two clone labs cannot spend the same inputs twice")
	_dispose(game)

func _test_forecast_matches_functioning_production() -> void:
	var game = _game()
	game.resources["power"] = 0
	_room(game, "hydroponics_bay", Vector2i(10, 10))
	var projected: Dictionary = game._project_cycle_delta()
	var actual: Dictionary = game._apply_room_economy()
	_expect(projected.get("food", 0) == actual.get("food", 0), "forecast must not promise offline food production")
	_dispose(game)

func _test_unlearned_forecast_does_not_reveal_bonus() -> void:
	var game = _game()
	_room(game, "reactor", Vector2i(10, 11))
	_room(game, "hydroponics_bay", Vector2i(10, 10))
	_room(game, "life_support", Vector2i(11, 10))
	_expect(game._project_cycle_delta().get("water", 0) == 0, "an untested layout must not preview a hidden bonus")
	_dispose(game)

func _test_power_loss_resets_real_discovery_progress() -> void:
	var game = _game()
	_room(game, "hydroponics_bay", Vector2i(10, 10))
	_room(game, "life_support", Vector2i(11, 10))
	game.resources["power"] = 2
	game._apply_room_economy()
	game._advance_synergy_discovery_cycle()
	_expect(game.synergy_stabilization_progress.get("closed_air_loop", 0) == 1, "first powered tick learns the pattern")
	game.resources["power"] = 0
	game._apply_room_economy()
	game._advance_synergy_discovery_cycle()
	_expect(game.active_synergy_links.is_empty() and game.synergy_stabilization_progress.get("closed_air_loop", -1) == 0, "a real power loss makes the link dormant and resets unfinished progress")
	_dispose(game)

func _test_orbit_rewards_do_not_bypass_discovery() -> void:
	var game = _game()
	game.orbit.current_poi = {"name": "Solar Flare", "work_required": 0, "expire_effect": {"power": 6}}
	game.orbit.timer = 1
	var before: Dictionary = game.resources.duplicate(true)
	game._apply_orbit_event()
	_expect(game.resources == before and game.orbit.timer == 1, "retired events neither advance nor grant resources")
	_expect(not game.meta.unlocked_room_ids.has("battery_array"), "a solar flare must not bypass load balancing")
	_room(game, "life_support", Vector2i(10, 10))
	game.orbit.current_poi = {"name": "Frozen Escape Pod", "work_required": 1, "work_type": "life_support", "reward": {}}
	game.orbit.timer = 1
	game._apply_orbit_event()
	_expect(not game.meta.unlocked_room_ids.has("cryo_chamber"), "an escape pod must not bypass clinical airlock")
	_expect(game.crew_count == 0, "retired orbital pods cannot rescue crew")
	_dispose(game)

func _test_containment_cleans_corruption() -> void:
	var game = _game()
	_room(game, "reactor", Vector2i(10, 11))
	_room(game, "xeno_lab", Vector2i(10, 10), 3)
	_room(game, "quarantine_cell", Vector2i(11, 10))
	game.corruption = 3
	game._apply_room_economy()
	_expect(game.corruption == 2, "functioning containment has a real recurring benefit")
	game.resources["power"] = 0
	game.occupied[Vector2i(10, 11)]["suspended"] = true
	game._apply_room_economy()
	_expect(game.corruption == 2, "offline containment cannot clean corruption")
	_dispose(game)

func _test_bursts_expire_without_advancing_paused_motion() -> void:
	var game = _game()
	game.paused = true
	game.visual_time_seconds = 1.25
	game.discovery_bursts = [{"cells": [Vector2i.ZERO, Vector2i.RIGHT], "remaining": 0.5}]
	game._process(1.0)
	_expect(game.discovery_bursts.is_empty(), "transient discovery bursts expire even while paused")
	_expect(game.visual_time_seconds == 1.25, "persistent functioning effects freeze with paused time")
	_dispose(game)

func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)
