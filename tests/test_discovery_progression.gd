extends SceneTree

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")

var failures := 0

func _init() -> void:
	_test_foundation_pool_is_intentionally_small()
	_test_every_recipe_has_progression_metadata()
	_test_unlock_graph_reaches_every_room()
	_test_reward_rooms_continue_or_end_explicitly()
	_test_both_endpoints_are_required_for_functioning()
	_test_only_functioning_links_contribute_cycle_bonuses()
	_test_first_functioning_cycle_discovers_and_starts_progress()
	_test_duplicate_links_advance_once_and_stabilize_on_three()
	_test_inactive_cycle_resets_unfinished_progress()
	if failures > 0:
		push_error("Discovery progression tests failed: %d" % failures)
		quit(1)
		return
	print("Discovery progression tests passed.")
	quit(0)

func _test_foundation_pool_is_intentionally_small() -> void:
	var expected := [
		"solar_array", "reactor", "mining_drone_bay", "hydroponics_bay",
		"life_support", "crew_hab", "research_lab", "storage_bay",
		"med_bay", "quarantine_cell", "corridor", "corner"
	]
	_expect_equal(RoomDatabaseScript.STARTING_UNLOCKS, expected, "clean saves should begin with the authored foundation")

func _test_every_recipe_has_progression_metadata() -> void:
	for synergy_value in SynergyManagerScript.all_synergies():
		var synergy: Dictionary = synergy_value
		_expect_true(int(synergy.get("stabilize_cycles", 0)) == 3, "%s should stabilize in three cycles" % synergy.get("id", "missing"))
		_expect_true(not str(synergy.get("fx_profile", "")).is_empty(), "%s should define an FX profile" % synergy.get("id", "missing"))
		_expect_true(not str(synergy.get("fx_color", "")).is_empty(), "%s should define an FX color" % synergy.get("id", "missing"))
		var has_unlock := not str(synergy.get("unlock_room_id", "")).is_empty()
		var terminal_reward: Dictionary = synergy.get("terminal_reward", {})
		var has_terminal_reward := not terminal_reward.is_empty()
		_expect_true(has_unlock != has_terminal_reward, "%s should define exactly one stabilization reward" % synergy.get("id", "missing"))

func _test_unlock_graph_reaches_every_room() -> void:
	var errors := DiscoveryManagerScript.validate_unlock_graph(
		RoomDatabaseScript.all_rooms(),
		SynergyManagerScript.all_synergies(),
		RoomDatabaseScript.STARTING_UNLOCKS
	)
	_expect_equal(errors, PackedStringArray(), "the authored discovery graph should have no unreachable rooms")

func _test_reward_rooms_continue_or_end_explicitly() -> void:
	var recipe_rooms := {}
	for synergy_value in SynergyManagerScript.all_synergies():
		for room_id_value in synergy_value.get("rooms", []):
			recipe_rooms[str(room_id_value)] = true
	for synergy_value in SynergyManagerScript.all_synergies():
		var reward_id := str(synergy_value.get("unlock_room_id", ""))
		if not reward_id.is_empty():
			_expect_true(recipe_rooms.has(reward_id), "%s should participate in a later or terminal recipe" % reward_id)

func _test_both_endpoints_are_required_for_functioning() -> void:
	var link := {"id": "closed_air_loop", "cells": [Vector2i(1, 1), Vector2i(2, 1)], "bonus": {"oxygen": 1}}
	var one_powered := {Vector2i(1, 1): true}
	_expect_equal(DiscoveryManagerScript.functioning_links([link], one_powered).size(), 0, "one powered endpoint should leave a link dormant")
	var both_powered := {Vector2i(1, 1): true, Vector2i(2, 1): true}
	_expect_equal(DiscoveryManagerScript.functioning_links([link], both_powered).size(), 1, "two powered endpoints should activate a link")

func _test_only_functioning_links_contribute_cycle_bonuses() -> void:
	var active := [{"id": "closed_air_loop", "cells": [Vector2i.ZERO, Vector2i.RIGHT], "bonus": {"oxygen": 1}}]
	_expect_equal(SynergyManagerScript.cycle_bonus(active), {"oxygen": 1}, "active links should contribute their authored bonus")
	_expect_equal(SynergyManagerScript.cycle_bonus([]), {}, "dormant links should contribute no bonus")

func _test_first_functioning_cycle_discovers_and_starts_progress() -> void:
	var link := _test_link("closed_air_loop")
	var result := DiscoveryManagerScript.advance_cycle([link], {}, {}, {})
	_expect_equal(result["new_discovery_ids"], ["closed_air_loop"], "first functioning cycle should discover the recipe")
	_expect_equal(int(result["progress"].get("closed_air_loop", 0)), 1, "discovery cycle should count as cycle one")

func _test_duplicate_links_advance_once_and_stabilize_on_three() -> void:
	var first := _test_link("closed_air_loop")
	var second := _test_link("closed_air_loop", Vector2i(4, 4))
	var discovered := {"closed_air_loop": true}
	var cycle_two := DiscoveryManagerScript.advance_cycle([first, second], {"closed_air_loop": 1}, discovered, {})
	_expect_equal(int(cycle_two["progress"]["closed_air_loop"]), 2, "duplicate copies should advance one cycle")
	var cycle_three := DiscoveryManagerScript.advance_cycle([first, second], cycle_two["progress"], discovered, {})
	_expect_equal(cycle_three["new_stabilization_ids"], ["closed_air_loop"], "third consecutive cycle should stabilize once")

func _test_inactive_cycle_resets_unfinished_progress() -> void:
	var result := DiscoveryManagerScript.advance_cycle([], {"closed_air_loop": 2}, {"closed_air_loop": true}, {})
	_expect_equal(int(result["progress"].get("closed_air_loop", 0)), 0, "losing every functioning copy should reset progress")

func _test_link(id: String, origin := Vector2i.ZERO) -> Dictionary:
	for synergy_value in SynergyManagerScript.all_synergies():
		if str(synergy_value.get("id", "")) == id:
			var link: Dictionary = synergy_value.duplicate(true)
			link["cells"] = [origin, origin + Vector2i.RIGHT]
			return link
	return {}

func _expect_equal(actual, expected, message: String) -> void:
	if actual != expected:
		failures += 1
		push_error("%s: expected %s, got %s" % [message, str(expected), str(actual)])

func _expect_true(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)
