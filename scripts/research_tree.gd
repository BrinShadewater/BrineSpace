extends RefCounted
## Temporary meta progression research tree (owner request, Sept 16). Research banked at the
## end of each loop (Data / 5 plus Resonance / 50) buys perks in three branches; each perk
## needs the one before it in its branch. Owned perks are stored in MetaState.brine_upgrades
## (an existing, previously unused profile set), so no new save field is needed, and the
## spendable balance is lifetime Research minus the cost of owned perks. The tree is a
## prototype: every perk can be refunded from the Meta Progression page.

const BRANCHES := [
	{"id":"engineering", "name":"ENGINEERING", "color":Color("d8913f")},
	{"id":"life_support", "name":"LIFE SUPPORT", "color":Color("6fc27a")},
	{"id":"discovery", "name":"DISCOVERY", "color":Color("5fa8e0")},
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
	"disc_research_grant": {"branch":"discovery", "tier":3, "cost":15, "name":"Research Grant", "text":"+25% Research at the end of each loop.", "research_bonus":0.25},
	"disc_rare_samples": {"branch":"discovery", "tier":4, "cost":25, "name":"Rare Samples", "text":"Start each loop with +2 Rare Minerals, and +20 Data storage.", "start":{"rare_minerals":2}, "capacity":{"data":20}},
	"disc_endowment": {"branch":"discovery", "tier":5, "cost":40, "name":"Endowment", "text":"A further +25% Research at the end of each loop.", "research_bonus":0.25},
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

static func available(meta) -> int:
	return maxi(0, int(meta.total_research_points) - spent(meta)) if meta != null else 0

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
