extends SceneTree

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const SynergyManagerScript := preload("res://scripts/synergy_manager.gd")
const MainScript := preload("res://scripts/main.gd")
const RunManagerScript := preload("res://scripts/run_manager.gd")
const MetaStateScript := preload("res://scripts/meta_state.gd")

var failures := 0

func _init() -> void:
	_run()

func _run() -> void:
	_test_repeated_pairs_stack()
	_test_multi_link_placement_combines_bonuses()
	_test_cryo_links_to_any_medical_room_once()
	_test_disconnected_pairs_do_not_score()
	_test_placement_cascade_scores_and_pulses()
	_test_doctrines_build_a_constrained_deck()
	_test_opening_hand_and_discard_cycle()
	_test_directives_escalate()
	_test_pair_directive_tracks_both_doctrines()
	_test_all_doctrine_pairs_have_viable_decks()
	_test_doctrine_pair_preview_exposes_tradeoffs()
	_test_directive_completion_advances_run()
	_test_final_directive_stabilizes_station()
	_test_missed_directive_ends_run()
	_test_doctrine_mastery_persists_progress()
	if failures > 0:
		push_error("Synergy tests failed: %d" % failures)
		quit(1)
		return
	print("Run-loop tests passed: links, cascades, all doctrine pairs, directives, deck flow, and mastery are valid.")
	quit(0)

func _test_repeated_pairs_stack() -> void:
	var occupied := {}
	_add_room(occupied, "life_support", Vector2i(10, 10))
	_add_room(occupied, "hydroponics_bay", Vector2i(11, 10))
	_add_room(occupied, "life_support", Vector2i(12, 10))
	var result := SynergyManagerScript.evaluate(occupied.values(), occupied, {})
	var links: Array = result["links"]
	_expect_equal(_count_links(links, "closed_air_loop"), 2, "two Closed Air Loop links should be counted")
	var bonus := SynergyManagerScript.cycle_bonus(links)
	_expect_equal(int(bonus.get("oxygen", 0)), 2, "each Closed Air Loop should add Oxygen")
	_expect_equal(result["new"].size(), 1, "a stacked pattern should only be discovered once")

func _test_multi_link_placement_combines_bonuses() -> void:
	var occupied := {}
	_add_room(occupied, "life_support", Vector2i(4, 5))
	_add_room(occupied, "hydroponics_bay", Vector2i(5, 5))
	_add_room(occupied, "crew_hab", Vector2i(6, 5))
	var result := SynergyManagerScript.evaluate(occupied.values(), occupied, {})
	var links: Array = result["links"]
	_expect_equal(_count_links(links, "closed_air_loop"), 1, "hydroponics should link to life support")
	_expect_equal(_count_links(links, "green_commons"), 1, "hydroponics should link to crew quarters")
	var bonus := SynergyManagerScript.cycle_bonus(links)
	_expect_equal(int(bonus.get("oxygen", 0)), 1, "combined link bonus should include Oxygen")
	_expect_equal(int(bonus.get("food", 0)), 1, "combined link bonus should include Food")

func _test_cryo_links_to_any_medical_room_once() -> void:
	var occupied := {}
	_add_room(occupied, "cryo_chamber", Vector2i(20, 20))
	_add_room(occupied, "med_bay", Vector2i(20, 21), 2)
	var result := SynergyManagerScript.evaluate(occupied.values(), occupied, {})
	_expect_equal(_count_links(result["links"], "safe_wake_protocol"), 1, "Cryo should link to a tagged medical neighbor")

func _test_disconnected_pairs_do_not_score() -> void:
	var occupied := {}
	_add_room(occupied, "research_lab", Vector2i(3, 3))
	_add_room(occupied, "data_archive", Vector2i(4, 3))
	var result := SynergyManagerScript.evaluate(occupied.values(), occupied, {})
	_expect_equal(_count_links(result["links"], "research_pipeline"), 0, "adjacent rooms without matching doors should not link")

func _test_placement_cascade_scores_and_pulses() -> void:
	var game = MainScript.new()
	var test_save_path := "user://brine_synergy_test_save.json"
	game.meta.save_path = test_save_path
	game.meta.discovered_synergy_ids.clear()
	game.occupied.clear()
	game.placed_rooms.clear()
	game.active_synergies.clear()
	game.active_synergy_links.clear()
	game.resonance_score = 0
	game.resonance_tier_index = 0
	game.links_formed = 0
	game.largest_cascade = 0
	game._place_room("life_support", Vector2i(9, 10))
	game._place_room("crew_hab", Vector2i(11, 10))
	game._place_room("hydroponics_bay", Vector2i(10, 10))
	_expect_equal(game.resonance_score, 30, "a two-link placement should score a triangular cascade")
	_expect_equal(game.links_formed, 2, "both new placement links should be recorded")
	_expect_equal(game.largest_cascade, 2, "best cascade should retain the placement chain size")
	_expect_equal(game.resonance_tier_index, 1, "a 30-point cascade should reach Aligned tier")
	_expect_equal(int(game.resources.get("oxygen", 0)), 9, "cascade pulse should immediately grant Oxygen")
	_expect_equal(int(game.resources.get("food", 0)), 9, "cascade pulse should immediately grant Food")
	_expect_equal(int(game.resources.get("data", 0)), 1, "multi-link cascades should grant bonus Data")
	game.free()
	if FileAccess.file_exists(test_save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(test_save_path))

func _test_doctrines_build_a_constrained_deck() -> void:
	var unlocked := {}
	for room_id in RoomDatabaseScript.STARTING_UNLOCKS:
		unlocked[str(room_id)] = true
	var deck := RunManagerScript.build_deck(["industry", "biosphere"], unlocked)
	_expect_true(deck.has("solar_array"), "every doctrine deck should include essential power")
	_expect_true(deck.has("reactor"), "Industry should add Reactor")
	_expect_true(deck.has("hydroponics_bay"), "Biosphere should add Hydroponics")
	_expect_true(deck.has("mining_drone_bay"), "every doctrine pair should retain a Metal economy")
	_expect_true(not deck.has("radio_lab"), "unselected Science cards should stay outside the deck")
	_expect_equal(deck.count("corridor"), 3, "the routing staple should have three deck copies")
	_expect_equal(deck.count("reactor"), 2, "common doctrine cards should have two deck copies")

func _test_opening_hand_and_discard_cycle() -> void:
	var game = MainScript.new()
	game.selected_doctrines.assign(["industry", "biosphere"])
	game._build_run_deck()
	game._draw_hand()
	_expect_equal(game.hand.size(), 3, "an opening draw should fill all three hand slots")
	_expect_true(game.hand.has("solar_array"), "the opening hand should guarantee a power source")
	_expect_true(game.hand.has("mining_drone_bay"), "the opening hand should guarantee a Metal economy")
	var spent_card_id := str(game.hand.pop_front())
	game.discard_pile.append(spent_card_id)
	game._refill_hand()
	_expect_equal(game.hand.size(), 3, "spending a card should immediately refill the hand")
	_expect_true(game.discard_pile.has(spent_card_id), "spent blueprints should enter the discard pile")
	game.free()

func _test_directives_escalate() -> void:
	var test_rng := RandomNumberGenerator.new()
	test_rng.seed = 4404
	var directives := RunManagerScript.roll_directives(test_rng, ["industry", "science"])
	_expect_equal(directives.size(), 3, "a reboot should contain three directives")
	_expect_true(int(directives[0]["deadline"]) < int(directives[1]["deadline"]), "second directive deadline should be later")
	_expect_true(int(directives[1]["deadline"]) < int(directives[2]["deadline"]), "final directive deadline should be latest")
	_expect_equal(directives[1].get("metric", ""), "doctrine_pair", "stage two should reflect the selected doctrine pair")
	_expect_true(str(directives[1].get("name", "")).contains("INDUSTRY"), "pair directive should name the first doctrine")
	_expect_true(str(directives[1].get("name", "")).contains("SCIENCE"), "pair directive should name the second doctrine")

func _test_pair_directive_tracks_both_doctrines() -> void:
	var directive := {
		"metric": "doctrine_pair",
		"doctrine_ids": ["industry", "biosphere"],
		"target": 3
	}
	var state := {"doctrine_counts": {"industry": 4, "biosphere": 2}}
	_expect_equal(RunManagerScript.directive_progress(directive, state), 2, "pair progress should use the less-developed doctrine")
	var progress_text := RunManagerScript.directive_progress_text(directive, state)
	_expect_true(progress_text.contains("INDUSTRY 3/3"), "pair progress should show capped Industry progress")
	_expect_true(progress_text.contains("BIOSPHERE 2/3"), "pair progress should show remaining Biosphere work")
	var overlap_counts := RunManagerScript.count_doctrine_rooms(
		[{"id": "brine_core"}, {"id": "xeno_lab"}, {"id": "research_lab"}],
		["science", "anomaly"]
	)
	_expect_equal(int(overlap_counts.get("science", 0)), 2, "overlap rooms should advance their Science doctrine")
	_expect_equal(int(overlap_counts.get("anomaly", 0)), 2, "overlap rooms should also advance their Anomaly doctrine")
	_expect_equal(
		RunManagerScript.directive_progress({"metric": "synergy_types"}, {"synergy_types": 4}),
		4,
		"pattern directives should count distinct active synergy types"
	)

func _test_all_doctrine_pairs_have_viable_decks() -> void:
	var unlocked := {}
	for room_id in RoomDatabaseScript.STARTING_UNLOCKS:
		unlocked[str(room_id)] = true
	var test_rng := RandomNumberGenerator.new()
	test_rng.seed = 8042
	var pair_count := 0
	for first_index in range(RunManagerScript.DOCTRINE_ORDER.size()):
		for second_index in range(first_index + 1, RunManagerScript.DOCTRINE_ORDER.size()):
			var first_id := str(RunManagerScript.DOCTRINE_ORDER[first_index])
			var second_id := str(RunManagerScript.DOCTRINE_ORDER[second_index])
			var pair := [first_id, second_id]
			var deck := RunManagerScript.build_deck(pair, unlocked)
			var pair_name := RunManagerScript.doctrine_pair_name(pair)
			pair_count += 1
			_expect_true(deck.has("solar_array") and deck.has("mining_drone_bay"), "%s should retain power and Metal essentials" % pair_name)
			_expect_true(deck.size() >= 10, "%s should have a playable clean-save deck" % pair_name)
			for doctrine_id in pair:
				var copies_for_doctrine := 0
				for room_id_value in RunManagerScript.doctrine(doctrine_id).get("rooms", []):
					copies_for_doctrine += deck.count(str(room_id_value))
				_expect_true(copies_for_doctrine >= 2, "%s should expose a repeatable foothold for %s" % [pair_name, doctrine_id])
			var directives := RunManagerScript.roll_directives(test_rng, pair)
			_expect_equal(directives[1].get("doctrine_ids", []), pair, "%s should preserve both doctrine ids in stage two" % pair_name)
	_expect_equal(pair_count, 10, "five doctrines should produce ten unique pair balance cases")

func _test_doctrine_pair_preview_exposes_tradeoffs() -> void:
	var game = MainScript.new()
	game.pending_doctrines.assign(["science", "anomaly"])
	var profile := game._doctrine_pair_preview_text()
	_expect_true(profile.contains("BLUEPRINTS"), "pair preview should expose deck size")
	_expect_true(profile.contains("LINK PATTERNS"), "pair preview should expose available synergy breadth")
	_expect_true(profile.contains("Research Lab"), "pair preview should name shared doctrine rooms")
	game.free()

func _test_directive_completion_advances_run() -> void:
	var game = MainScript.new()
	game.running = true
	game.rerolls_remaining = 3
	game.placed_rooms.assign([{"id": "brine_core"}, {"id": "solar_array"}])
	game.run_directives = [
		{"name": "FIRST", "metric": "rooms", "target": 1, "deadline": 5, "reward": {"resources": {"metal": 2}, "rerolls": 1}},
		{"name": "SECOND", "metric": "rooms", "target": 4, "deadline": 10, "reward": {}}
	]
	var metal_before := int(game.resources["metal"])
	game._check_directive_progress()
	_expect_equal(game.directive_index, 1, "completing a directive should advance the run")
	_expect_equal(game.completed_directives.size(), 1, "completed directive should be recorded")
	_expect_equal(game.rerolls_remaining, 4, "directive reward should add a reroll")
	_expect_equal(int(game.resources["metal"]), metal_before + 2, "directive reward should grant resources")
	game.free()

func _test_final_directive_stabilizes_station() -> void:
	var test_save_path := "user://brine_victory_test_save.json"
	var game = MainScript.new()
	game.meta.save_path = test_save_path
	game.meta.doctrine_mastery.clear()
	game.meta.total_victories = 0
	game.summary_layer = CanvasLayer.new()
	game.summary_text = Label.new()
	game.summary_title_label = Label.new()
	game.selected_doctrines.assign(["industry", "biosphere"])
	game.placed_rooms.assign([{"id": "brine_core"}, {"id": "solar_array"}])
	game.run_directives = [{"name": "FINAL", "metric": "rooms", "target": 1, "deadline": 5, "reward": {}}]
	game.running = true
	game._check_directive_progress()
	_expect_true(game.run_victory, "completing the final directive should mark the reboot as a victory")
	_expect_true(not game.running, "victory should stop the active simulation")
	_expect_equal(game.completed_directives.size(), 1, "the final directive should be included in the summary")
	_expect_equal(game.summary_title_label.text, "Station Stabilized", "victory should use the stabilized summary title")
	_expect_equal(game.meta.total_victories, 1, "a stabilized station should persist one victory")
	_expect_true(game.summary_text.text.contains("INDUSTRY R1 2/5  RANK UP"), "victory summary should expose doctrine rank progress")
	_expect_true(game.summary_text.text.contains("Stabilized reboots: 1"), "victory summary should expose the persistent win count")
	game.summary_text.free()
	game.summary_title_label.free()
	game.summary_layer.free()
	game.free()
	if FileAccess.file_exists(test_save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(test_save_path))

func _test_missed_directive_ends_run() -> void:
	var test_save_path := "user://brine_deadline_test_save.json"
	var game = MainScript.new()
	game.meta.save_path = test_save_path
	game.meta.doctrine_mastery.clear()
	game.summary_layer = CanvasLayer.new()
	game.summary_text = Label.new()
	game.summary_title_label = Label.new()
	game.running = true
	game.cycle = 6
	game.run_directives = [{"name": "EXPIRED", "metric": "rooms", "target": 4, "deadline": 5, "reward": {}}]
	game._check_directive_progress()
	_expect_true(not game.running, "a missed directive deadline should end the run")
	_expect_true(game.summary_text.text.contains("deadline missed"), "deadline failure should explain the loss")
	game.summary_text.free()
	game.summary_title_label.free()
	game.summary_layer.free()
	game.free()
	if FileAccess.file_exists(test_save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(test_save_path))

func _test_doctrine_mastery_persists_progress() -> void:
	var test_save_path := "user://brine_meta_test_save.json"
	var test_meta = MetaStateScript.new()
	test_meta.save_path = test_save_path
	test_meta.doctrine_mastery.clear()
	test_meta.total_victories = 0
	var gain := test_meta.record_run(["industry", "biosphere"], true, 180)
	_expect_equal(gain, 2, "victory should grant two mastery")
	_expect_equal(test_meta.get_doctrine_rank("industry"), 1, "two mastery should reach doctrine rank one")
	_expect_equal(test_meta.total_victories, 1, "victory count should persist")
	test_meta.record_run(["industry"], false, 30)
	_expect_equal(test_meta.get_doctrine_mastery("industry"), 3, "a meaningful failed run should still grant one mastery")
	if FileAccess.file_exists(test_save_path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(test_save_path))

func _add_room(occupied: Dictionary, room_id: String, pos: Vector2i, rotation := 0) -> void:
	var room := RoomDatabaseScript.get_room(room_id).duplicate(true)
	room["pos"] = pos
	room["rotation"] = rotation
	occupied[pos] = room

func _count_links(links: Array, synergy_id: String) -> int:
	var count := 0
	for link in links:
		if str(link.get("id", "")) == synergy_id:
			count += 1
	return count

func _expect_equal(actual, expected, message: String) -> void:
	if actual == expected:
		return
	failures += 1
	push_error("%s: expected %s, got %s" % [message, str(expected), str(actual)])

func _expect_true(condition: bool, message: String) -> void:
	if condition:
		return
	failures += 1
	push_error(message)
