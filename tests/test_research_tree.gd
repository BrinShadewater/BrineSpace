extends SceneTree
## Research tree (owner request, Sept 16): Research buys perks in three five-tier branches,
## each needing the one before it; owned perks persist in the profile, shape new loops and
## show on the Meta Progression page. Uses an isolated profile, never the player's save.
const Preferences = preload("res://scripts/title_settings.gd")
const Research = preload("res://scripts/research_tree.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	var prefix := "user://research_tree_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"

	# Rules on a bare profile.
	var meta := MetaState.new()
	meta.save_path = prefix + ".json"
	meta.total_research_points = 60
	check(Research.PERKS.size() == 15 and Research.BRANCHES.size() == 3, "Three branches of five perks")
	for branch in Research.BRANCHES:
		var tiers: Array = Research.perks_in(branch.id).map(func(id): return int(Research.PERKS[id].tier))
		check(tiers == [1, 2, 3, 4, 5], "%s runs tier 1 to 5" % branch.id)
	check(Research.state(meta, "eng_salvaged_stock") == "ready" and Research.state(meta, "eng_spare_capacitors") == "locked", "Only tier 1 is open at first")
	check(not Research.buy(meta, "eng_spare_capacitors"), "A perk cannot be bought before the one above it")
	check(Research.buy(meta, "eng_salvaged_stock") and Research.available(meta) == 55, "Buying spends its cost from the balance")
	check(not Research.buy(meta, "eng_salvaged_stock"), "A perk is bought once")
	check(Research.buy(meta, "eng_spare_capacitors") and Research.buy(meta, "eng_quick_rigging") and Research.available(meta) == 30, "Tiers open in order")
	check(Research.buy(meta, "eng_spare_parts") and Research.available(meta) == 5, "Tier 4 costs 25")
	check(Research.state(meta, "eng_bulkhead_seals") == "short" and not Research.buy(meta, "eng_bulkhead_seals"), "A perk costing more than the balance waits")
	check(meta.total_research_points == 60, "Spending never reduces Research earned")
	var reloaded := MetaState.new()
	reloaded.save_path = prefix + ".json"
	check(reloaded.brine_upgrades.has("eng_spare_parts") and Research.available(reloaded) == 5, "Owned perks survive a reload of the profile")
	check(Research.refund_all(meta) == 55 and Research.available(meta) == 60 and meta.brine_upgrades.is_empty(), "Refund returns every perk's Research")

	# Effects in a new loop.
	for id in ["eng_salvaged_stock", "eng_spare_capacitors", "eng_quick_rigging", "eng_spare_parts", "eng_bulkhead_seals", "life_stored_rations", "life_deep_tanks", "life_seed_stock", "life_expanded_tanks", "life_warm_thaw", "disc_archive_index", "disc_calibrated_sensors", "disc_research_grant"]:
		meta.brine_upgrades[id] = true
	meta.total_research_points = 500
	meta.save_to_disk()
	var baseline = load("res://scenes/main.tscn").instantiate()
	baseline.meta.save_path = prefix + "-empty.json"
	baseline.run_save_path = prefix + "-baseline.loop"
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix + ".json"
	game.run_save_path = prefix + ".loop"
	root.add_child(baseline)
	baseline._start_reboot_cycle()
	root.add_child(game)
	current_scene = game
	game._start_reboot_cycle()
	for key in ["metal", "power", "food", "oxygen", "water", "biomass", "data"]:
		var expected: int = int(baseline.resources[key]) + int(Research.start_resources(game.meta).get(key, 0))
		check(int(game.resources[key]) == expected, "Loop starts with perk %s: %d, expected %d" % [key, game.resources[key], expected])
	check(game.resources.metal == baseline.resources.metal + 5 and game.resources.data == baseline.resources.data + 4, "Salvaged Stock and Archive Index add their supplies")
	check(game.rerolls_remaining == baseline.rerolls_remaining + 1, "Spare Parts adds a reroll")
	check(game._get_power_capacity() == baseline._get_power_capacity() + 4 and game._get_resource_capacity("oxygen") == baseline._get_resource_capacity("oxygen") + 10 and game._get_resource_capacity("food") == baseline._get_resource_capacity("food") + 10, "Storage perks raise capacity")
	check(is_equal_approx(Research.repair_rate(game.meta), 1.25) and is_equal_approx(Research.thaw_rate(game.meta), 1.3) and is_equal_approx(Research.flood_rate(game.meta), 0.75), "Rate perks report their factors")
	check(is_equal_approx(Research.research_multiplier(game.meta), 1.25) and Research.research_lab_data(game.meta) == 1, "Discovery perks report their bonuses")
	check(is_equal_approx(Research.repair_rate(baseline.meta), 1.0) and is_equal_approx(Research.research_multiplier(baseline.meta), 1.0), "No perks, no change")
	baseline.queue_free()

	# The Meta Progression page shows the tree and buys from it.
	meta.brine_upgrades.clear()
	meta.total_research_points = 20
	meta.save_to_disk()
	game.meta.save_path = prefix + "-page.json"
	game.meta.save_path = prefix + ".json"
	var page = preload("res://scripts/title_archive.gd").new()
	page.meta_state = game.meta
	page.mode = "progression"
	root.add_child(page)
	for i in range(3): await process_frame
	var tree_box: Control = page.find_child("ResearchTree", true, false)
	check(tree_box != null, "Meta Progression shows the research tree")
	var first: Control = page.find_child("life_stored_rations", true, false)
	var second: Control = page.find_child("life_deep_tanks", true, false)
	check(first != null and second != null, "Perk nodes are listed")
	if first != null and second != null:
		var buy: Button = first.find_child("Buy", true, false)
		check(not buy.disabled and "5 DATA" in buy.text, "An open perk offers to unlock")
		check(second.find_child("Buy", true, false).disabled, "The next perk waits for it")
		buy.pressed.emit()
		for i in range(2): await process_frame
		var summary: Label = page.find_child("ResearchSummary", true, false)
		check(summary != null and summary.text.begins_with("15 ARCHIVED DATA AVAILABLE"), "The balance updates after buying: %s" % (summary.text if summary else "missing"))
		check((page.find_child("life_stored_rations", true, false).find_child("Buy", true, false) as Button).text == "OWNED", "The perk shows as owned")
		check(not (page.find_child("life_deep_tanks", true, false).find_child("Buy", true, false) as Button).disabled, "The next perk opens")
		(page.find_child("RefundResearch", true, false) as Button).pressed.emit()
		for i in range(2): await process_frame
		check(Research.available(game.meta) == 20 and (page.find_child("ResearchSummary", true, false) as Label).text.begins_with("20 ARCHIVED DATA AVAILABLE"), "Refund from the page restores the balance")
	page.queue_free()
	game.queue_free()
	await process_frame
	for suffix in [".cfg", ".json", ".json.bak", ".json.tmp", "-empty.json", "-page.json", ".loop", "-baseline.loop", ".loop.comms.json", "-baseline.loop.comms.json"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(prefix + suffix)
	print("RESEARCH TREE %s: rules, persistence, refund, loop-start supplies, capacity, rates, research bonus and page" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
