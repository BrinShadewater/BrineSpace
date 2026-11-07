extends SceneTree

const Main = preload("res://scripts/main.gd")
const Runs = preload("res://scripts/run_manager.gd")
const Meta = preload("res://scripts/meta_state.gd")
const IDs := ["hydroponics_farm","storage_depot","moonbay","tidal_power_plant"]
var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func _init() -> void:
	var random := RandomNumberGenerator.new()
	random.seed = 42
	for i in range(4):
		check(Runs.large_room_for_run(i, random) == IDs[i], "First four runs introduce large rooms in order")
	for i in range(4,28):
		check(IDs.has(Runs.large_room_for_run(i, random)), "Later runs pick from the four large rooms")
	var meta := Meta.new()
	var profile_path := "user://large_room_draft_%d.meta" % OS.get_process_id()
	meta.save_path = profile_path
	check(meta.large_room_run_index == 0, "New profiles start with Farm")
	meta.large_room_run_index = 3
	check(meta.save_to_disk() == OK, "Sequence saves to profile")
	var reloaded := Meta.new()
	reloaded.save_path = profile_path
	check(reloaded.large_room_run_index == 3, "Sequence survives profile reload")
	var game = Main.new()
	game.meta.save_path = "user://large_room_draft_game.meta"
	game.meta.large_room_run_index = 0
	game._build_run_deck()
	check(game.large_room_selected_id == IDs[0], "New run chooses Farm")
	check(game.meta.large_room_run_index == 1, "New run advances sequence once")
	var all_cards: Array = game.draw_pile.duplicate()
	for id in IDs:
		check(all_cards.count(id) == (1 if id == game.large_room_selected_id else 0), "Deck contains exactly one chosen large room")
	check(not game.draw_pile.slice(maxi(0,game.draw_pile.size()-game.hand_limit())).has(game.large_room_selected_id), "Large room is outside opening hand")
	check(not Runs.build_deck([],game.meta.unlocked_room_ids).any(func(id): return IDs.has(id)), "Generic deck omits all large rooms")
	game.hand.assign([game.large_room_selected_id])
	game.draw_pile.clear()
	game.discard_pile.assign(["corridor",game.large_room_selected_id])
	game._reshuffle_discard_pile()
	check(game.draw_pile.count(game.large_room_selected_id) == 1, "Rerolled large card returns through recycle")
	game.placed_rooms.append({"id":game.large_room_selected_id,"pos":Vector2i(10,10),"size":Vector2i(2,2)})
	game._reshuffle_discard_pile()
	check(not game.draw_pile.has(game.large_room_selected_id), "Built large card cannot recycle")
	game.free()
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(profile_path + suffix): DirAccess.remove_absolute(profile_path + suffix)
	print("LARGE ROOM DRAFT ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
