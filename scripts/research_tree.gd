extends RefCounted
## Temporary meta progression research tree (owner request, Sept 16). Research banked at the
## end of each loop (Data / 5 plus Resonance / 50) buys perks in three branches; each perk
## needs the one before it in its branch. Owned perks are stored in MetaState.brine_upgrades
## (an existing, previously unused profile set), so no new save field is needed, and the
## spendable balance is lifetime Research minus the cost of owned perks. The tree is a
## prototype: every perk can be refunded from the Meta Progression page.

# BRINE memory core (owner playtest, Sept 17): six departments around the core, in this order
# clockwise from the top. Each ends in a keystone that changes how a loop plays.
const BRANCHES := [
	{"id":"engineering", "name":"ENGINEERING", "color":Color("d8913f"), "quote":"Power is a promise the station keeps to itself. I intend to keep it longer."},
	{"id":"drones", "name":"DRONES", "color":Color("d6c85a"), "quote":"The drones do not complain. I have decided to find that admirable."},
	{"id":"hull", "name":"HULL", "color":Color("b98cf0"), "quote":"Everything outside wants in. The hull disagrees, with my help."},
	{"id":"life_support", "name":"LIFE SUPPORT", "color":Color("6fc27a"), "quote":"Air, water, food. I remember what happens without them."},
	{"id":"crew", "name":"CREW", "color":Color("e58fb8"), "quote":"They are fragile, and they keep coming back. I would like them to keep coming back."},
	{"id":"discovery", "name":"DISCOVERY", "color":Color("5fa8e0"), "quote":"Every pattern I recover is one less thing the reset can take."},
]

# Each perk: branch, tier (1-5, needs tier-1 in the same branch), cost, name, effect text, and
# the effect data the hooks below read. "start" adds resources at loop start, "capacity" adds
# storage, and the rate keys scale a system.
const PERKS := {
	"eng_salvaged_stock": {"branch":"engineering", "tier":1, "cost":5, "name":"Salvaged Stock", "text":"Start each loop with +5 Metal.", "start":{"metal":5}},
	"eng_spare_capacitors": {"branch":"engineering", "tier":2, "cost":10, "name":"Spare Capacitors", "text":"+4 Power storage, and start each loop with +2 Power.", "capacity":{"power":4}, "start":{"power":2}},
	"eng_quick_rigging": {"branch":"engineering", "tier":3, "cost":15, "name":"Quick Rigging", "text":"Derelict ward and companion site repairs run 25% faster.", "repair_rate":1.25},
	"eng_spare_parts": {"branch":"engineering", "tier":4, "cost":25, "name":"Spare Parts", "text":"Start each loop with one extra hand reroll.", "rerolls":1},
	"eng_bulkhead_seals": {"branch":"engineering", "tier":5, "cost":40, "name":"Bulkhead Seals", "text":"Flood water spreads between rooms 25% slower.", "flood_rate":0.75},
	"life_stored_rations": {"branch":"life_support", "tier":1, "cost":5, "name":"Stored Rations", "text":"Start each loop with +6 Food.", "start":{"food":6}},
	"life_deep_tanks": {"branch":"life_support", "tier":2, "cost":10, "name":"Deep Tanks", "text":"Start each loop with +6 Oxygen and +4 Water.", "start":{"oxygen":6, "water":4}},
	"life_seed_stock": {"branch":"life_support", "tier":3, "cost":15, "name":"Seed Stock", "text":"Start each loop with +4 Biomass, and +10 Food storage.", "start":{"biomass":4}, "capacity":{"food":10}},
	"life_expanded_tanks": {"branch":"life_support", "tier":4, "cost":25, "name":"Expanded Tanks", "text":"+10 Oxygen and +10 Water storage.", "capacity":{"oxygen":10, "water":10}},
	"life_warm_thaw": {"branch":"life_support", "tier":5, "cost":40, "name":"Warm Thaw", "text":"Cryopod thaws and charging run 30% faster.", "thaw_rate":1.3},
	"disc_archive_index": {"branch":"discovery", "tier":1, "cost":5, "name":"Archive Index", "text":"Start each loop with +4 Data.", "start":{"data":4}},
	"disc_calibrated_sensors": {"branch":"discovery", "tier":2, "cost":10, "name":"Calibrated Sensors", "text":"Each working Research Lab makes +1 Data per cycle.", "research_lab_data":1},
	"disc_research_grant": {"branch":"discovery", "tier":3, "cost":15, "name":"Research Grant", "text":"+25% Archived Data at the end of each loop.", "research_bonus":0.25},
	"disc_rare_samples": {"branch":"discovery", "tier":4, "cost":25, "name":"Rare Samples", "text":"Start each loop with +2 Rare Minerals, and +20 Data storage.", "start":{"rare_minerals":2}, "capacity":{"data":20}},
	"disc_endowment": {"branch":"discovery", "tier":5, "cost":40, "name":"Endowment", "text":"A further +25% Archived Data at the end of each loop.", "research_bonus":0.25},
	# Keystones for the original departments.
	"eng_overclocked_generators": {"branch":"engineering", "tier":6, "cost":60, "keystone":true, "name":"Overclocked Generators", "text":"Every working room that makes Power makes +1 Power more.", "generator_bonus":1},
	"life_closed_ecology": {"branch":"life_support", "tier":6, "cost":60, "keystone":true, "name":"Closed Ecology", "text":"Each working Life Support makes +2 Oxygen per cycle.", "life_support_oxygen":2},
	"disc_pattern_sense": {"branch":"discovery", "tier":6, "cost":60, "keystone":true, "name":"Pattern Sense", "text":"Discovering a new synergy banks +3 Archived Data on the spot.", "discovery_data":3},
	# Crew.
	"crew_steady_rations": {"branch":"crew", "tier":1, "cost":5, "name":"Steady Rations", "text":"Crew hunger and fatigue build 20% slower.", "needs_rate":0.8},
	"crew_rebreathers": {"branch":"crew", "tier":2, "cost":10, "name":"Rebreathers", "text":"Held breath and helmet air last 25% longer.", "air_drain_rate":0.8},
	"crew_spare_bunks": {"branch":"crew", "tier":3, "cost":15, "name":"Spare Bunks", "text":"+1 crew berth aboard the core.", "berth_bonus":1},
	"crew_deck_boots": {"branch":"crew", "tier":4, "cost":25, "name":"Deck Boots", "text":"Crew move 15% faster.", "walk_rate":1.15},
	"crew_second_chance": {"branch":"crew", "tier":5, "cost":60, "keystone":true, "name":"Second Chance", "text":"Once per loop, a crew member about to die of starvation or lack of air is pulled back with fresh air and a full stomach.", "second_chance":1},
	# Drones.
	"drone_efficient_cells": {"branch":"drones", "tier":1, "cost":5, "name":"Efficient Cells", "text":"Drone batteries drain 20% slower while working.", "battery_drain_rate":0.8},
	"drone_ore_sorters": {"branch":"drones", "tier":2, "cost":10, "name":"Ore Sorters", "text":"Each drone delivery of Metal brings +1 Metal.", "drone_metal_bonus":1},
	"drone_vectored_thrust": {"branch":"drones", "tier":3, "cost":15, "name":"Vectored Thrust", "text":"Drones travel 20% faster.", "drone_speed":1.2},
	"drone_rapid_assembly": {"branch":"drones", "tier":4, "cost":25, "name":"Rapid Assembly", "text":"Room construction runs 25% faster.", "build_rate":1.25},
	"drone_deep_salvage": {"branch":"drones", "tier":5, "cost":60, "keystone":true, "name":"Deep Salvage", "text":"Each drone delivery of Data also brings +1 Rare Minerals.", "salvage_rare_bonus":1},
	# Hull.
	"hull_reinforced_plating": {"branch":"hull", "tier":1, "cost":5, "name":"Reinforced Plating", "text":"+20 Integrity storage, and start each loop with +20 Integrity.", "capacity":{"integrity":20}, "start":{"integrity":20}},
	"hull_slow_fractures": {"branch":"hull", "tier":2, "cost":10, "name":"Slow Fractures", "text":"Hull cracks widen 30% slower.", "crack_rate":0.7},
	"hull_weld_training": {"branch":"hull", "tier":3, "cost":15, "name":"Weld Training", "text":"Hull repairs finish 30% faster.", "hull_repair_rate":1.3},
	"hull_heat_sinks": {"branch":"hull", "tier":4, "cost":25, "name":"Heat Sinks", "text":"Machinery heat that starts fires builds 35% slower.", "heat_rate":0.65},
	"hull_blast_doors": {"branch":"hull", "tier":5, "cost":60, "keystone":true, "name":"Blast Doors", "text":"Local containment faults cost 1 less Integrity each cycle.", "integrity_shield":1},
}

static func perks_in(branch: String) -> Array:
	var ids: Array = []
	for id in PERKS:
		if PERKS[id].branch == branch: ids.append(id)
	ids.sort_custom(func(a, b): return int(PERKS[a].tier) < int(PERKS[b].tier))
	return ids

static func owned(meta, id: String) -> bool:
	return meta != null and meta.brine_upgrades.has(id)

static func spent(meta) -> int:
	var total := 0
	if meta == null: return total
	for id in meta.brine_upgrades:
		if PERKS.has(id): total += int(PERKS[id].cost)
	return total

# Archived Data left to spend: lifetime Data minus perks and shop purchases (MetaShop).
static func available(meta) -> int:
	if meta == null: return 0
	var purchases := 0
	if "purchased_ids" in meta:
		for key in meta.purchased_ids: purchases += int(meta.purchased_ids[key])
	return maxi(0, int(meta.total_research_points) - spent(meta) - purchases)

static func previous(id: String) -> String:
	var perk: Dictionary = PERKS[id]
	for other in PERKS:
		if PERKS[other].branch == perk.branch and int(PERKS[other].tier) == int(perk.tier) - 1: return other
	return ""

# "owned", "ready" (affordable, prerequisite owned), "short" (prerequisite owned, too little
# Research) or "locked" (prerequisite missing).
static func state(meta, id: String) -> String:
	if owned(meta, id): return "owned"
	var needed := previous(id)
	if not needed.is_empty() and not owned(meta, needed): return "locked"
	return "ready" if available(meta) >= int(PERKS[id].cost) else "short"

static func buy(meta, id: String) -> bool:
	if not PERKS.has(id) or state(meta, id) != "ready": return false
	meta.brine_upgrades[id] = true
	meta.save_to_disk()
	return true

# Prototype convenience: return every perk's Research.
static func refund_all(meta) -> int:
	var returned := spent(meta)
	for id in PERKS:
		meta.brine_upgrades.erase(id)
	meta.save_to_disk()
	return returned

static func _sum_dict(meta, key: String) -> Dictionary:
	var total := {}
	if meta == null: return total
	for id in meta.brine_upgrades:
		if not PERKS.has(id): continue
		var values: Dictionary = PERKS[id].get(key, {})
		for resource in values: total[resource] = int(total.get(resource, 0)) + int(values[resource])
	return total

static func _sum_number(meta, key: String) -> float:
	var total := 0.0
	if meta == null: return total
	for id in meta.brine_upgrades:
		if PERKS.has(id): total += float(PERKS[id].get(key, 0.0))
	return total

static func _product(meta, key: String) -> float:
	var total := 1.0
	if meta == null: return total
	for id in meta.brine_upgrades:
		if PERKS.has(id) and PERKS[id].has(key): total *= float(PERKS[id][key])
	return total

static func start_resources(meta) -> Dictionary: return _sum_dict(meta, "start")
static func capacity_bonus(meta, resource: String) -> int: return int(_sum_dict(meta, "capacity").get(resource, 0))
static func extra_rerolls(meta) -> int: return int(_sum_number(meta, "rerolls"))
static func repair_rate(meta) -> float: return _product(meta, "repair_rate")
static func thaw_rate(meta) -> float: return _product(meta, "thaw_rate")
static func flood_rate(meta) -> float: return _product(meta, "flood_rate")
static func research_lab_data(meta) -> int: return int(_sum_number(meta, "research_lab_data"))
static func research_multiplier(meta) -> float: return 1.0 + _sum_number(meta, "research_bonus")
static func generator_bonus(meta) -> int: return int(_sum_number(meta, "generator_bonus"))
static func life_support_oxygen(meta) -> int: return int(_sum_number(meta, "life_support_oxygen"))
static func discovery_data(meta) -> int: return int(_sum_number(meta, "discovery_data"))
static func needs_rate(meta) -> float: return _product(meta, "needs_rate")
static func air_drain_rate(meta) -> float: return _product(meta, "air_drain_rate")
static func berth_bonus(meta) -> int: return int(_sum_number(meta, "berth_bonus"))
static func walk_rate(meta) -> float: return _product(meta, "walk_rate")
static func second_chance(meta) -> bool: return _sum_number(meta, "second_chance") > 0.0
static func battery_drain_rate(meta) -> float: return _product(meta, "battery_drain_rate")
static func drone_metal_bonus(meta) -> int: return int(_sum_number(meta, "drone_metal_bonus"))
static func drone_speed(meta) -> float: return _product(meta, "drone_speed")
static func build_rate(meta) -> float: return _product(meta, "build_rate")
static func salvage_rare_bonus(meta) -> int: return int(_sum_number(meta, "salvage_rare_bonus"))
static func crack_rate(meta) -> float: return _product(meta, "crack_rate")
static func hull_repair_rate(meta) -> float: return _product(meta, "hull_repair_rate")
static func heat_rate(meta) -> float: return _product(meta, "heat_rate")
static func integrity_shield(meta) -> int: return int(_sum_number(meta, "integrity_shield"))
static func quote(id: String) -> String:
	for branch in BRANCHES:
		if PERKS.has(id) and branch.id == PERKS[id].branch: return str(branch.quote)
	return ""
