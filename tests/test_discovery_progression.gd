extends SceneTree

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const DiscoveryManagerScript := preload("res://scripts/discovery_manager.gd")
const MetaStateScript := preload("res://scripts/meta_state.gd")
const MainScript := preload("res://scripts/main.gd")

var failures := 0

func _init() -> void:
	_test_new_room_patterns()
	_test_foundation_pool_is_intentionally_small()
	_test_every_recipe_has_progression_metadata()
	_test_medical_airlock_progression()
	_test_unlock_graph_reaches_every_room()
	_test_reward_rooms_continue_or_end_explicitly()
	_test_both_endpoints_are_required_for_functioning()
	_test_only_functioning_links_contribute_cycle_bonuses()
	_test_first_functioning_cycle_discovers_and_starts_progress()
	_test_duplicate_links_advance_once_and_stabilize_on_three()
	_test_inactive_cycle_resets_unfinished_progress()
	_test_stabilization_persists_idempotently()
	_test_old_save_without_stabilization_loads_additively()
	_test_blueprint_reward_unlocks_and_becomes_next_draw()
	_test_already_unlocked_reward_does_not_inject_a_duplicate_prototype()
	_test_terminal_stabilization_grants_research_once()
	_test_prototype_marker_survives_one_full_cycle_or_clears_on_selection()
	_test_three_functioning_cycles_complete_the_clean_unlock_chain()
	_test_run_summary_names_new_progression_events()
	_test_resource_thresholds_do_not_bypass_the_discovery_graph()
	_test_unknown_card_hint_never_names_partner_or_recipe()
	_test_known_card_hint_may_name_learned_recipe()
	_test_cascade_name_stays_generic_until_discovery()
	_test_toast_queue_preserves_discovery_order()
	if failures > 0:
		push_error("Discovery progression tests failed: %d" % failures)
		quit(1)
		return
	print("Discovery progression tests passed.")
	quit(0)

func _test_foundation_pool_is_intentionally_small() -> void:
	var expected := [
		"observation_room", "salvage_workshop", "galley", "cold_store", "current_turbine", "airlock",
		"construction_drone_bay",
		"solar_array", "reactor", "mining_drone_bay", "hydroponics_bay",
		"life_support", "crew_hab", "research_lab", "storage_bay",
		"med_bay", "quarantine_cell", "corridor", "corner", "tee_corridor",
		"pressure_control", "listening_post", "isolation_vault"
	]
	_expect_equal(RoomDatabaseScript.STARTING_UNLOCKS, expected, "clean saves should begin with the authored foundation")

func _test_medical_airlock_progression() -> void:
	var link := _test_link("clinical_airlock")
	_expect_equal(link.get("unlock_room_id"),"cryo_chamber","Medical care retains Cryo reward")
	var progress := {}
	var discovered := {}
	for cycle in range(1,4):
		var result := DiscoveryManagerScript.advance_cycle([link],progress,discovered,{})
		progress=result.progress
		discovered["clinical_airlock"]=true
		_expect_equal(result.new_stabilization_ids,["clinical_airlock"] if cycle==3 else [],"Medical pattern stabilizes only on third functioning cycle")

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

func _test_stabilization_persists_idempotently() -> void:
	var save_path := "user://brine_discovery_meta_test.json"
	var meta = MetaStateScript.new()
	meta.save_path = save_path
	if not _require_property(meta, "stabilized_synergy_ids") or not _require_method(meta, "stabilize_synergy"):
		return
	meta.stabilized_synergy_ids.clear()
	_expect_true(meta.stabilize_synergy("closed_air_loop"), "first stabilization should persist")
	_expect_true(not meta.stabilize_synergy("closed_air_loop"), "repeat stabilization should not reward twice")
	var loaded = MetaStateScript.new()
	loaded.save_path = save_path
	loaded.stabilized_synergy_ids.clear()
	loaded.load_from_disk()
	_expect_true(loaded.stabilized_synergy_ids.has("closed_air_loop"), "stabilization should survive reload")
	_remove_test_save(save_path)

func _test_old_save_without_stabilization_loads_additively() -> void:
	var save_path := "user://brine_old_save_test.json"
	var file := FileAccess.open(save_path, FileAccess.WRITE)
	file.store_string(JSON.stringify({
		"unlocked_room_ids": ["biodome"],
		"discovered_synergy_ids": ["closed_air_loop"]
	}))
	file.close()
	var meta = MetaStateScript.new()
	meta.save_path = save_path
	if not _require_property(meta, "stabilized_synergy_ids"):
		_remove_test_save(save_path)
		return
	meta.stabilized_synergy_ids.clear()
	meta.load_from_disk()
	_expect_true(meta.unlocked_room_ids.has("biodome"), "older unlocked rooms should remain unlocked")
	_expect_true(meta.discovered_synergy_ids.has("closed_air_loop"), "older discoveries should remain learned")
	_expect_equal(meta.stabilized_synergy_ids, {}, "a missing stabilization field should load as empty")
	_remove_test_save(save_path)

func _test_blueprint_reward_unlocks_and_becomes_next_draw() -> void:
	var save_path := "user://brine_prototype_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	if not _require_property(game.meta, "stabilized_synergy_ids") or not _require_property(game, "run_decrypted_blueprint_ids") or not _require_method(game, "_award_synergy_stabilization"):
		game.free()
		return
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids.erase("biodome")
	game.draw_pile.clear()
	game.discard_pile.assign(["corridor"])
	game._award_synergy_stabilization(_test_link("closed_air_loop"))
	_expect_true(game.meta.unlocked_room_ids.has("biodome"), "stabilization should unlock the authored blueprint")
	_expect_equal(game.draw_pile.back(), "biodome", "prototype should be the next card drawn")
	_expect_equal(game.run_decrypted_blueprint_ids, ["biodome"], "run summary should record the decrypt")
	game._refill_hand()
	_expect_equal(game.hand[0], "biodome", "an empty draw pile should yield the prototype before discard reshuffling")
	game.free()
	_remove_test_save(save_path)

func _test_already_unlocked_reward_does_not_inject_a_duplicate_prototype() -> void:
	var save_path := "user://brine_existing_unlock_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	if not _require_property(game.meta, "stabilized_synergy_ids") or not _require_method(game, "_award_synergy_stabilization"):
		game.free()
		return
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids["biodome"] = true
	game.draw_pile.assign(["corridor"])
	game._award_synergy_stabilization(_test_link("closed_air_loop"))
	_expect_true(game.meta.stabilized_synergy_ids.has("closed_air_loop"), "the recipe should still stabilize")
	_expect_equal(game.draw_pile.count("biodome"), 0, "an older unlock should not inject a duplicate prototype")
	game.free()
	_remove_test_save(save_path)

func _test_terminal_stabilization_grants_research_once() -> void:
	var save_path := "user://brine_terminal_reward_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	if not _require_property(game.meta, "stabilized_synergy_ids") or not _require_method(game, "_award_synergy_stabilization"):
		game.free()
		return
	game.meta.stabilized_synergy_ids.erase("drone_foundry")
	var research_before: int = int(game.meta.total_research_points)
	game._award_synergy_stabilization(_test_link("drone_foundry"))
	game._award_synergy_stabilization(_test_link("drone_foundry"))
	_expect_equal(game.meta.total_research_points, research_before + 3, "terminal Research should be awarded exactly once")
	game.free()
	_remove_test_save(save_path)

func _test_prototype_marker_survives_one_full_cycle_or_clears_on_selection() -> void:
	var game = MainScript.new()
	if not _require_property(game, "prototype_card_seen_cycle") or not _require_method(game, "_expire_prototype_markers") or not _require_method(game, "_clear_prototype_marker"):
		game.free()
		return
	game.prototype_card_seen_cycle = {"biodome": 4}
	game.cycle = 5
	game._expire_prototype_markers()
	_expect_true(game.prototype_card_seen_cycle.has("biodome"), "the NEW marker should survive one full following cycle")
	game.cycle = 6
	game._expire_prototype_markers()
	_expect_true(not game.prototype_card_seen_cycle.has("biodome"), "the NEW marker should expire after that following cycle")
	game.prototype_card_seen_cycle["biodome"] = 6
	game._clear_prototype_marker("biodome")
	_expect_true(not game.prototype_card_seen_cycle.has("biodome"), "selecting the prototype should clear its NEW marker")
	game.free()

func _test_three_functioning_cycles_complete_the_clean_unlock_chain() -> void:
	var save_path := "user://brine_clean_chain_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	if not _require_property(game.meta, "stabilized_synergy_ids") or not _require_method(game, "_award_synergy_stabilization"):
		game.free()
		return
	game.meta.discovered_synergy_ids.erase("closed_air_loop")
	game.meta.stabilized_synergy_ids.erase("closed_air_loop")
	game.meta.unlocked_room_ids.erase("biodome")
	game.draw_pile.assign(["corridor"])
	game.active_synergy_links = [_test_link("closed_air_loop")]
	for _cycle_index in range(3):
		game._advance_synergy_discovery_cycle()
	_expect_true(game.meta.discovered_synergy_ids.has("closed_air_loop"), "the recipe should be learned")
	_expect_true(game.meta.stabilized_synergy_ids.has("closed_air_loop"), "the recipe should be stabilized")
	_expect_true(game.meta.unlocked_room_ids.has("biodome"), "Biodome should be permanent")
	_expect_true(game.draw_pile.has("biodome"), "the current run should contain a Biodome prototype")
	_expect_equal(game.run_discovered_synergy_ids.count("closed_air_loop"), 1, "discovery should be recorded once")
	_expect_equal(game.run_stabilized_synergy_ids.count("closed_air_loop"), 1, "stabilization should be recorded once")
	game.free()
	_remove_test_save(save_path)

func _test_run_summary_names_new_progression_events() -> void:
	var save_path := "user://brine_discovery_summary_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	if not _require_property(game, "run_decrypted_blueprint_ids"):
		game.free()
		return
	game.summary_layer = CanvasLayer.new()
	game.summary_text = Label.new()
	game.summary_title_label = Label.new()
	game.run_discovered_synergy_ids.assign(["closed_air_loop"])
	game.run_stabilized_synergy_ids.assign(["closed_air_loop"])
	game.run_decrypted_blueprint_ids.assign(["biodome"])
	game._show_reboot_summary("Test run complete.")
	_expect_true(game.summary_text.text.contains("Patterns discovered: Closed Air Loop"), "summary should name recipes discovered this run")
	_expect_true(game.summary_text.text.contains("Patterns stabilized: Closed Air Loop"), "summary should name recipes stabilized this run")
	_expect_true(game.summary_text.text.contains("Blueprints decrypted: Biodome"), "summary should name blueprints decrypted this run")
	game.summary_text.free()
	game.summary_title_label.free()
	game.summary_layer.free()
	game.free()
	_remove_test_save(save_path)

func _test_resource_thresholds_do_not_bypass_the_discovery_graph() -> void:
	var save_path := "user://brine_discovery_bypass_test.json"
	var game = MainScript.new()
	game.meta.save_path = save_path
	game.meta.unlocked_room_ids.erase("clone_lab")
	game.meta.unlocked_room_ids.erase("data_archive")
	game.resources["biomass"] = 100
	game.resources["data"] = 100
	game._apply_unlocks()
	_expect_true(not game.meta.unlocked_room_ids.has("clone_lab"), "resource totals must not bypass Safe Wake Protocol")
	_expect_true(not game.meta.unlocked_room_ids.has("data_archive"), "resource totals must not bypass Core Diagnostics")
	game.free()
	_remove_test_save(save_path)

func _test_unknown_card_hint_never_names_partner_or_recipe() -> void:
	var game = MainScript.new()
	game.meta.discovered_synergy_ids.clear()
	var hint := game._card_synergy_hint("hydroponics_bay")
	_expect_true(not hint.contains("Life Support"), "unknown hint should not name a partner")
	_expect_true(not hint.contains("Closed Air Loop"), "unknown hint should not name a recipe")
	_expect_true(hint.contains("EXPERIMENTAL"), "unknown hint should use universal experimental wording")
	game.free()

func _test_known_card_hint_may_name_learned_recipe() -> void:
	var game = MainScript.new()
	game.meta.discovered_synergy_ids = {"closed_air_loop": true}
	var hint := game._card_synergy_hint("hydroponics_bay")
	_expect_true(hint.contains("Closed Air Loop"), "learned recipe may appear on its room card")
	game.free()

func _test_cascade_name_stays_generic_until_discovery() -> void:
	var game = MainScript.new()
	if not _require_method(game, "_synergy_display_name"):
		game.free()
		return
	game.meta.discovered_synergy_ids.clear()
	_expect_equal(game._synergy_display_name("closed_air_loop"), "UNRESOLVED PATTERN", "candidate cascades must not reveal unknown recipe names")
	game.meta.discovered_synergy_ids["closed_air_loop"] = true
	_expect_equal(game._synergy_display_name("closed_air_loop"), "Closed Air Loop", "known cascades may use the learned recipe name")
	game.free()

func _test_toast_queue_preserves_discovery_order() -> void:
	var game = MainScript.new()
	if not _require_property(game, "toast_playing") or not _require_property(game, "toast_messages") or not _require_method(game, "_queue_center_toast"):
		game.free()
		return
	game.toast_playing = true
	game._queue_center_toast("PATTERN DISCOVERED\nFIRST")
	game._queue_center_toast("PATTERN DISCOVERED\nSECOND")
	_expect_equal(game.toast_messages, ["PATTERN DISCOVERED\nFIRST", "PATTERN DISCOVERED\nSECOND"], "simultaneous discoveries should retain their order")
	game.free()

func _remove_test_save(save_path: String) -> void:
	if FileAccess.file_exists(save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(save_path))

func _require_property(object: Object, property_name: String) -> bool:
	for property_value in object.get_property_list():
		if str(property_value.get("name", "")) == property_name:
			return true
	_expect_true(false, "%s should expose property %s" % [object.get_class(), property_name])
	return false

func _require_method(object: Object, method_name: String) -> bool:
	if object.has_method(method_name):
		return true
	_expect_true(false, "%s should expose method %s" % [object.get_class(), method_name])
	return false

func _expect_equal(actual, expected, message: String) -> void:
	if actual != expected:
		failures += 1
		push_error("%s: expected %s, got %s" % [message, str(expected), str(actual)])

func _expect_true(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)

func _test_new_room_patterns() -> void:
	for id in ["chilled_air_recovery","shared_table","field_notes"]:
		var recipe: Dictionary = SynergyManagerScript.get_synergy(id)
		var first: Dictionary = RoomDatabaseScript.get_room(recipe.rooms[0]).duplicate(true)
		var second: Dictionary = RoomDatabaseScript.get_room(recipe.rooms[1]).duplicate(true)
		first.pos = Vector2i(10,10)
		second.pos = Vector2i(10,11)
		first.rotation = 0
		var links: Array = []
		for rotation in range(4):
			if second.has("fixed_rotation") and rotation != int(second.fixed_rotation): continue
			second.rotation = rotation
			links = SynergyManagerScript.evaluate([first,second],{first.pos:first,second.pos:second}).links
			if not links.is_empty(): break
		_expect_true(not links.is_empty(),id + " has a legal matching-door layout")
		if links.is_empty(): continue
		_expect_equal(links[0].id,id,"New pair selects the expected recipe")
		var offline := DiscoveryManagerScript.functioning_links(links,{first.pos:true})
		_expect_true(offline.is_empty(),"Both new partners must function")
		var active := DiscoveryManagerScript.functioning_links(links,{first.pos:true,second.pos:true})
		var state := DiscoveryManagerScript.advance_cycle(active,{}, {}, {})
		_expect_true(state.new_discovery_ids.has(id),"First functioning cycle reveals new pattern")
		_expect_true(state.new_stabilization_ids.is_empty(),"New pattern does not stabilize early")
		state = DiscoveryManagerScript.advance_cycle(active,state.progress,{id:true},{})
		state = DiscoveryManagerScript.advance_cycle([],state.progress,{id:true},{})
		_expect_equal(state.progress[id],0,"Interrupted new pattern resets progress")
		for cycle in range(3): state = DiscoveryManagerScript.advance_cycle(active,state.progress,{id:true},{})
		_expect_true(state.new_stabilization_ids.has(id),"Three consecutive functioning cycles stabilize new pattern")
		second.pos = Vector2i(10,12)
		_expect_true(SynergyManagerScript.evaluate([first,second],{first.pos:first,second.pos:second}).links.is_empty(),"Separated new partners do not link")
