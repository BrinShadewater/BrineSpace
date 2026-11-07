extends SceneTree
## Real draft operations; no scene, free-building or survival overrides.
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
	var game := Station.new()
	game.running = true
	var repeats := 0
	for run_seed in range(64):
		game.rng.seed = run_seed
		game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
		game.draw_pile.assign(["life_support", "solar_array", "corridor", "mining_drone_bay", "hydroponics_bay", "storage_bay"])
		game._shuffle_draw_pile()
		game.discard_pile.clear()
		game.rerolls_remaining = 3
		var resources_before: Dictionary = game.resources.duplicate(true)
		game._discard_card("solar_array")
		if game.hand.has("solar_array"): repeats += 1
		check(not game.hand.has("solar_array"), "Single reroll prefers a different blueprint when available")
		check(game.rerolls_remaining == 2 and game.resources == resources_before, "Reroll spends one charge and no construction resources")
		check(game.draw_pile.size()+game.discard_pile.size()+game.hand.size()==9, "Reroll preserves every blueprint copy")
	game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
	game.draw_pile.assign(["life_support", "corridor", "storage_bay", "solar_array", "mining_drone_bay", "hydroponics_bay"])
	game.discard_pile.clear()
	game.rerolls_remaining = 3
	game._discard_all_cards()
	check(not game.hand.has("solar_array") and not game.hand.has("mining_drone_bay") and not game.hand.has("hydroponics_bay"), "Whole-hand reroll prefers alternatives to every rejected card")
	check(game.rerolls_remaining == 2 and game.hand.size()==3, "Whole-hand reroll retains hand size and one-charge price")
	# A recycle at the draw boundary must also respect the rejected blueprint.
	game.hand.assign(["solar_array", "mining_drone_bay", "hydroponics_bay"])
	game.draw_pile.clear()
	game.discard_pile.assign(["solar_array", "life_support"])
	game._discard_card("solar_array")
	check(game.hand.has("life_support") and not game.hand.has("solar_array"), "Recycled discard alternatives take priority too")
	# Small decks still refill; avoiding an old card is a preference, not card deletion.
	game.hand.assign(["solar_array"])
	game.draw_pile.clear()
	game.discard_pile.clear()
	game.rerolls_remaining = 1
	game._discard_card("solar_array")
	check(game.hand==["solar_array"] and game.rerolls_remaining==0, "An unavoidable repeat remains available in an exhausted deck")
	check(game.meta.discovered_synergy_ids.is_empty(), "Reroll fairness reveals no hidden recipes")
	print("DRAFT REROLL: %d checks / %d failures / immediate repeats %d of 64" % [checks,failures,repeats])
	game.free()
	quit(1 if failures else 0)
