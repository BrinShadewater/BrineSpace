extends SceneTree
## Archived Data shop (owner playtest, Sept 17): one currency buys upgrades, blueprints and
## crew; characters met in a loop are bought for later loops; stabilized patterns double their
## bonus and halve their related blueprint. Uses an isolated profile, never the player's save.
const Preferences = preload("res://scripts/title_settings.gd")
const Research = preload("res://scripts/research_tree.gd")
const Shop = preload("res://scripts/meta_shop.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	var prefix := "user://meta_shop_%d" % OS.get_process_id()
	Preferences.save_path = prefix + ".cfg"
	var meta := MetaState.new()
	meta.save_path = prefix + ".json"
	meta.total_research_points = 100

	# Blueprints.
	check(not Shop.blueprint_ids().has("brine_core"), "The core is not for sale")
	var rare := ""
	for id in Shop.blueprint_ids():
		if not meta.unlocked_room_ids.has(id) and str(preload("res://scripts/room_database.gd").get_room(id).rarity) == "rare" and id != "biomass_digester":
			rare = id
			break
	check(not rare.is_empty() and Shop.room_cost(meta, rare) == 32, "Rare blueprints cost 32")
	check(Shop.room_state(meta, rare) == "ready" and Shop.buy_room(meta, rare), "An affordable blueprint can be bought")
	check(meta.unlocked_room_ids.has(rare) and Research.available(meta) == 68, "Buying unlocks the room and spends Archived Data")
	check(not Shop.buy_room(meta, rare) and Shop.room_state(meta, rare) == "owned", "A blueprint is bought once")
	check(Research.buy(meta, "eng_salvaged_stock") and Research.available(meta) == 63, "Upgrades and shop share one balance")
	var linked := "biomass_digester"
	var pattern := Shop.related_pattern(linked)
	check(not pattern.is_empty(), "Biomass Digester has a related pattern")
	var full := Shop.room_cost(meta, linked)
	meta.stabilized_synergy_ids[pattern.id] = true
	check(Shop.room_cost(meta, linked) == int(ceil(full * 0.5)), "Stabilizing the related pattern halves the blueprint")

	# Crew and companions.
	check(Shop.character_state(meta, "veld") == "unmet" and not Shop.buy_character(meta, "veld"), "Unmet crew cannot be bought")
	check(meta.record_character("veld") and not meta.record_character("veld"), "Meeting a character is recorded once")
	check(not meta.unlocked_architect_ids.has("veld"), "Meeting does not unlock permanently")
	check(Shop.character_state(meta, "veld") == "ready" and Shop.buy_character(meta, "veld"), "Met crew can be bought")
	check(meta.unlocked_architect_ids.has("veld") and meta.select_architect("veld"), "Bought crew can start a loop")
	check(meta.record_character("josh") and Shop.buy_character(meta, "josh") and meta.unlocked_companion_ids.has("josh"), "Met companions can be bought")
	var reloaded := MetaState.new()
	reloaded.save_path = prefix + ".json"
	check(Research.available(reloaded) == Research.available(meta) and reloaded.purchased_ids.size() == 3 and reloaded.met_character_ids.has("josh"), "Purchases and met characters survive a reload")

	# Earlier profiles keep their unlocks for free and count them as met.
	var legacy := FileAccess.open(prefix + "-legacy.json", FileAccess.WRITE)
	legacy.store_string(JSON.stringify({"unlocked_architect_ids": ["bill", "marsh"], "unlocked_companion_ids": ["river"], "total_research_points": 40, "unlocked_room_ids": ["biodome"]}))
	legacy.close()
	var old := MetaState.new()
	old.save_path = prefix + "-legacy.json"
	check(Research.available(old) == 40 and old.met_character_ids.has("marsh") and old.met_character_ids.has("river") and Shop.character_state(old, "marsh") == "owned" and Shop.room_state(old, "biodome") == "owned", "Existing unlocks stay owned and free")

	# Stabilized patterns double their per-cycle bonus.
	var link: Dictionary = Synergies.get_synergy(pattern.id)
	var single := Synergies.cycle_bonus([link])
	var doubled := Synergies.cycle_bonus([link], {pattern.id: true})
	for key in single: check(int(doubled[key]) == int(single[key]) * 2, "Stabilized %s doubles %s" % [pattern.id, key])

	# The page: tabs, blueprint and crew shops.
	var page = preload("res://scripts/title_archive.gd").new()
	page.meta_state = meta
	page.mode = "progression"
	root.add_child(page)
	for i in range(3): await process_frame
	var tabs: TabBar = page.find_child("ProgressionTabs", true, false)
	check(tabs != null and tabs.tab_count == 4, "Meta Progression has four tabs")
	if tabs != null:
		tabs.current_tab = 1
		for i in range(3): await process_frame
		check(page.find_child("BlueprintShop", true, false) != null, "Blueprints tab lists rooms")
		var card: Control = page.find_child("Blueprint_" + linked, true, false)
		if card != null:
			var buy: Button = card.find_child("Buy", true, false)
			var before := Research.available(meta)
			check(not buy.disabled and ("%d DATA" % Shop.room_cost(meta, linked)) in buy.text, "A blueprint card offers to buy")
			buy.pressed.emit()
			for i in range(3): await process_frame
			check(meta.unlocked_room_ids.has(linked) and Research.available(meta) == before - Shop.room_cost(meta, linked), "Buying from the page spends Archived Data")
		else:
			check(false, "Biomass Digester card is listed")
		(page.find_child("ProgressionTabs", true, false) as TabBar).current_tab = 2
		for i in range(3): await process_frame
		var branforth: Control = page.find_child("branforth", true, false)
		check(branforth != null and (branforth.find_child("Buy", true, false) as Button).text == "NOT MET YET", "Unmet crew show how to meet them")
		check(page.find_child("veld", true, false) != null and (page.find_child("veld", true, false).find_child("Buy", true, false) as Button).text == "OWNED", "Bought crew show as owned")
	page.queue_free()
	await process_frame
	for suffix in [".cfg", ".json", ".json.bak", ".json.tmp", "-legacy.json", "-legacy.json.bak", "-legacy.json.tmp"]:
		if FileAccess.file_exists(prefix + suffix): DirAccess.remove_absolute(prefix + suffix)
	print("META SHOP %s: blueprints, shared balance, pattern discount, met and bought crew, legacy unlocks, doubled bonus and page" % ("PASS" if failures == 0 else "FAIL %d" % failures))
	quit(1 if failures else 0)
