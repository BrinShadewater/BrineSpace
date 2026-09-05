extends SceneTree

const MainScene := preload("res://scenes/main.tscn")
const Rooms := preload("res://scripts/room_database.gd")
const SAVE_PATH := "user://brine_run_balance_test.json"
var game
var failures := 0

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	game = MainScene.instantiate()
	game.meta.save_path = SAVE_PATH
	root.add_child(game)
	current_scene = game
	await process_frame
	_test_exhausted_draft_recovers_without_buildable_cards()
	_test_recharge_does_not_accumulate_while_full()
	_test_recharge_preserves_banked_directive_rewards()
	_test_pause_and_reboot_keep_recharge_honest()
	await _test_fit_station_contains_an_expanded_station()
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(SAVE_PATH))
	if failures == 0:
		print("Run balance tests passed: draft recovery, reward banking, pause, reboot and expanded-station fit.")
	else:
		push_error("Run balance test failures: %d" % failures)
	quit(1 if failures > 0 else 0)

func _station() -> void:
	game.meta.unlocked_room_ids.clear()
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.doctrine_mastery.clear()
	for id in Rooms.STARTING_UNLOCKS:
		game.meta.unlocked_room_ids[id] = true
	game._start_reboot_cycle()
	game.pending_doctrines.assign(["science", "biosphere"])
	game._confirm_doctrines()
	game._set_paused(true)
	# Connected, sustainable fixture; subsequent cycles and rerolls are real.
	game._place_room("solar_array", Vector2i(21, 20), true)
	game._place_room("mining_drone_bay", Vector2i(20, 19), true)
	game.run_directives = [{"id": "fixture", "name": "FIXTURE", "metric": "rooms", "target": 999, "deadline": 999}]
	game.hand.assign(["biodome", "bio_lab", "clone_lab"])
	game.draw_pile.assign(["hydroponics_bay", "life_support", "solar_array"])
	game.rerolls_remaining = 0
	game._refresh_all()

func _test_exhausted_draft_recovers_without_buildable_cards() -> void:
	_station()
	for id in game.hand:
		_expect(not game._can_afford(Rooms.get_room(id)["cost"]), "fixture hand is blocked on unavailable inputs")
	for _cycle in range(3):
		game._advance_cycle()
	_expect(game.rerolls_remaining == 0, "a recovery charge takes four real cycles")
	_expect(game.reroll_button.text.contains("1C"), "exhausted draft displays its next recovery time")
	game._advance_cycle()
	_expect(game.rerolls_remaining == 1, "a dead hand gets a route back into the deck")
	game._discard_all_cards()
	_expect(game.hand.has("hydroponics_bay") and game.hand.has("solar_array"), "the recovered charge actually draws buildable foundations")
	_expect(game.rerolls_remaining == 0, "the recovered reroll is consumed normally")
	_expect(game.meta.discovered_synergy_ids.is_empty(), "draft recovery does not teach hidden recipes")

func _test_recharge_does_not_accumulate_while_full() -> void:
	_station()
	game.rerolls_remaining = 3
	for _cycle in range(6):
		game._advance_cycle()
	_expect(game.rerolls_remaining == 3, "passive recovery cannot stockpile unlimited rerolls")
	game._discard_all_cards()
	for _cycle in range(3):
		game._advance_cycle()
	_expect(game.rerolls_remaining == 2, "time spent at a full bank cannot become instant credit")
	game._advance_cycle()
	_expect(game.rerolls_remaining == 3, "recovery resumes after a charge is spent")

func _test_recharge_preserves_banked_directive_rewards() -> void:
	_station()
	game.rerolls_remaining = 5
	for _cycle in range(8):
		game._advance_cycle()
	_expect(game.rerolls_remaining == 5, "recharge cap must not erase earned directive rewards")

func _test_pause_and_reboot_keep_recharge_honest() -> void:
	_station()
	for _cycle in range(3):
		game._advance_cycle()
	var cycle_before: int = game.cycle
	for _timeout in range(8):
		game._on_tick_timer_timeout()
	_expect(game.cycle == cycle_before and game.rerolls_remaining == 0, "paused timer callbacks cannot generate recovery charges")
	game._start_reboot_cycle()
	game.pending_doctrines.assign(["science", "biosphere"])
	game._confirm_doctrines()
	game._set_paused(true)
	game._place_room("solar_array", Vector2i(21, 20), true)
	game._discard_all_cards()
	_expect(game.rerolls_remaining == 2, "a fresh reboot starts with three charges")
	game._advance_cycle()
	_expect(game.rerolls_remaining == 2, "unfinished recharge progress cannot carry into a reboot")

func _test_fit_station_contains_an_expanded_station() -> void:
	_station()
	for y in range(21, 35):
		game._place_room("storage_bay", Vector2i(20, y), true)
	game._fit_station_view()
	for _frame in range(6):
		await process_frame
	var visible := Rect2(Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical), game.grid_scroll.size).grow(1.0)
	for room in game.placed_rooms:
		var room_rect := Rect2(Vector2(room["pos"]) * game.get_cell_size(), Vector2.ONE * game.get_cell_size())
		_expect(visible.encloses(room_rect), "Fit Station keeps every expanded room inside the viewport")

func _expect(condition: bool, message: String) -> void:
	if not condition:
		failures += 1
		push_error(message)
