extends SceneTree
## Starting unlocks, legacy-profile admission and real opening-draft methods.
const Rooms = preload("res://scripts/room_database.gd")
const Meta = preload("res://scripts/meta_state.gd")
class Station extends "res://scripts/main.gd":
	func _refresh_all() -> void: pass
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		push_error(message)
func _init() -> void:
	var actual := ProjectSettings.globalize_path("user://").replace("\\","/").trim_suffix("/").to_lower()
	var expected := OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").trim_suffix("/").to_lower()
	if expected.is_empty() or actual!=expected:
		push_error("Refusing salvage fixture outside the isolated test profile")
		quit(1)
		return
	var profile = Meta.new()
	profile.save_path = "user://salvage-opening.meta"
	check(profile.unlocked_room_ids.has("salvage_drone_bay"),"A clean profile owns Salvage Drone Bay without a progression purchase")
	var old_record := JSON.stringify({"unlocked_room_ids":["biodome"],"discovered_synergy_ids":["closed_air_loop"],"total_research_points":37,"purchased_ids":{"room:biodome":6}})
	var file := FileAccess.open(profile.save_path,FileAccess.WRITE)
	file.store_string(old_record)
	file.close()
	profile._reset_profile()
	profile.load_from_disk()
	check(profile.unlocked_room_ids.has("salvage_drone_bay"),"An older profile receives the new foundation unlock on load")
	check(profile.unlocked_room_ids.has("biodome") and profile.discovered_synergy_ids.has("closed_air_loop"),"Existing purchases and discoveries remain owned")
	check(profile.total_research_points==37 and profile.purchased_ids=={"room:biodome":6},"Loading the new foundation does not spend, refund or reset progress")
	check(FileAccess.get_file_as_string(profile.save_path)==old_record,"Profile loading itself does not rewrite the old record")
	var game := Station.new()
	game.meta.save_path = "user://salvage-opening-deck.meta"
	var first_seven := ["solar_array","mining_drone_bay","hydroponics_bay","current_turbine","salvage_drone_bay","life_support","desalination_unit"]
	for cohort in ["starting","expanded"]:
		game.meta.unlocked_room_ids.clear()
		for id in Rooms.STARTING_UNLOCKS: game.meta.unlocked_room_ids[id] = true
		if cohort=="expanded":
			for id in Rooms.all_rooms(): game.meta.unlocked_room_ids[id] = true
		for run_seed in range(32):
			game.rng.seed = run_seed
			game._build_run_deck()
			var deck: Array = game.draw_pile.duplicate()
			deck.reverse()
			check(deck.slice(0,7)==first_seven,"Salvage is fifth with opening power, mining, food and oxygen intact: "+cohort)
			check(deck.count("salvage_drone_bay")==2,"Staging moves an existing common copy without adding extra cards")
			game._draw_hand()
			check(game.hand==first_seven.slice(0,3),"The original opening hand remains available")
			game.hand.erase("solar_array")
			game._refill_hand()
			check(game.hand.has("current_turbine"),"First normal replacement offers the second generator")
			game.hand.erase("mining_drone_bay")
			game._refill_hand()
			check(game.hand.has("salvage_drone_bay"),"Second normal replacement offers Salvage Drone Bay")
	game.free()
	print("SALVAGE OPENING: %d checks / %d failures / 32 starting + 32 expanded seeds" % [checks,failures])
	quit(1 if failures else 0)
