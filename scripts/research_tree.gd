extends RefCounted
## Temporary meta progression research tree (owner request, Sept 16). Research banked at the
## end of each loop (Data / 5 plus Resonance / 50) buys perks in three branches; each perk
## needs the one before it in its branch. Owned perks are stored in MetaState.brine_upgrades
## (an existing, previously unused profile set), so no new save field is needed, and the
## spendable balance is lifetime Research minus the cost of owned perks. The tree is a
## prototype: every perk can be refunded from the Meta Progression page.

# BRINE memory core (owner playtest, Sept 17): six departments around the core, in this order
# clockwise from the top. Each ends in a keystone that changes how a loop plays.
# BRINE's memory is lobed, not listed (owner request): eight lobes, each named for a department of
# the station and wearing that department's colour from RoomDatabase. A lobe roots at the core and
# grows two dendrites that go their own way, and each dendrite ends in its own keystone - the
# deepest thing BRINE remembers about that part of the station.
const BRANCH_DEPARTMENTS := {
	"operations": "Core",
	"engineering": "Engineering",
	"science": "Science",
	"life_support": "Bio",
	"crew": "Crew",
	"robotics": "Drone",
	"anomaly": "Anomaly",
	"structure": "",
}
const HULL_COLOR := Color("#9aa2a8")

const BRANCHES := [
	{"id":"operations", "name":"OPERATIONS", "quote":"Someone has to decide what matters first. It appears to be me."},
	{"id":"engineering", "name":"ENGINEERING", "quote":"Power is a promise the station keeps to itself. I intend to keep it longer."},
	{"id":"science", "name":"SCIENCE & MEDICAL", "quote":"Every pattern I recover is one less thing the reset can take."},
	{"id":"life_support", "name":"LIFE SUPPORT", "quote":"Air, water, food. I remember what happens without them."},
	{"id":"crew", "name":"CREW QUARTERS", "quote":"They are fragile, and they keep coming back. I would like them to keep coming back."},
	{"id":"robotics", "name":"AI & ROBOTICS", "quote":"The drones do not complain. I have decided to find that admirable."},
	{"id":"anomaly", "name":"ANOMALY", "quote":"There is a shape in the readings that I have not agreed to yet."},
	{"id":"structure", "name":"STRUCTURE", "quote":"Everything outside wants in. The hull disagrees, with my help."},
]

# The palette lives in RoomDatabase; structure is corridor grey, which is not a department colour.
static func branch_color(branch_id: String) -> Color:
	var department: String = BRANCH_DEPARTMENTS.get(branch_id, "")
	if department.is_empty(): return HULL_COLOR
	return preload("res://scripts/room_database.gd").CATEGORY_COLORS.get(department, Color.WHITE)

# Each perk: branch (its lobe), tier (kept for ordering and the node label), "requires" (every node
# recovered before it), cost, name, effect text, and the effect data the hooks below read. "start"
# adds resources at loop start, "capacity" adds storage, and the rate keys scale a system.
#
# A lobe roots at the core, splits into two dendrites, and each dendrite ends in its own keystone.
# Recovering either keystone never requires the other, so two profiles can remember the station
# differently.
const PERKS := {
	# OPERATIONS // what the station does first when something goes wrong.
	"ops_standing_watch": {"branch":"operations", "tier":1, "cost":5, "name":"Standing Watch", "text":"Someone is always awake. Crew hunger and fatigue build 20% slower.", "needs_rate":0.8},
	"ops_contingency_drills": {"branch":"operations", "tier":2, "requires":["ops_standing_watch"], "cost":12, "name":"Contingency Drills", "text":"Start each loop with one extra hand reroll.", "rerolls":1},
	"ops_command_override": {"branch":"operations", "tier":3, "requires":["ops_contingency_drills"], "cost":40, "keystone":true, "name":"Command Override", "text":"BRINE keeps one more blueprint staged: your hand holds +1 card all loop.", "extra_cards":1},
	"ops_quarantine_protocol": {"branch":"operations", "tier":2, "requires":["ops_standing_watch"], "cost":12, "name":"Quarantine Protocol", "text":"Local containment faults cost 1 less Integrity each cycle.", "integrity_shield":1},
	"crew_second_chance": {"branch":"operations", "tier":3, "requires":["ops_quarantine_protocol"], "cost":40, "keystone":true, "name":"Second Chance", "text":"Once per loop, a crew member about to die of starvation or lack of air is pulled back with fresh air and a full stomach.", "second_chance":1},

	# ENGINEERING // power kept, and the rigs that keep it.
	"eng_salvaged_stock": {"branch":"engineering", "tier":1, "cost":5, "name":"Salvaged Stock", "text":"Start each loop with +5 Metal.", "start":{"metal":5}},
	"eng_spare_capacitors": {"branch":"engineering", "tier":2, "requires":["eng_salvaged_stock"], "cost":12, "name":"Spare Capacitors", "text":"+4 Power storage, and start each loop with +2 Power.", "capacity":{"power":4}, "start":{"power":2}},
	"eng_overclocked_generators": {"branch":"engineering", "tier":3, "requires":["eng_spare_capacitors"], "cost":40, "keystone":true, "name":"Overclocked Generators", "text":"Every working room that makes Power makes +1 Power more.", "generator_bonus":1},
	"eng_quick_rigging": {"branch":"engineering", "tier":2, "requires":["eng_salvaged_stock"], "cost":12, "name":"Quick Rigging", "text":"Derelict ward and companion site repairs run 25% faster.", "repair_rate":1.25},
	"eng_failsafe_welds": {"branch":"engineering", "tier":3, "requires":["eng_quick_rigging"], "cost":40, "keystone":true, "name":"Failsafe Welds", "text":"Hull repairs finish 30% faster, and the seams hold: flood water spreads 25% slower.", "hull_repair_rate":1.3, "flood_rate":0.75},

	# SCIENCE & MEDICAL // what gets learned, and what it is worth.
	"disc_archive_index": {"branch":"science", "tier":1, "cost":5, "name":"Archive Index", "text":"Start each loop with +4 Data.", "start":{"data":4}},
	"disc_calibrated_sensors": {"branch":"science", "tier":2, "requires":["disc_archive_index"], "cost":12, "name":"Calibrated Sensors", "text":"Each working Research Lab makes +1 Data per cycle.", "research_lab_data":1},
	"disc_pattern_sense": {"branch":"science", "tier":3, "requires":["disc_calibrated_sensors"], "cost":40, "keystone":true, "name":"Pattern Sense", "text":"Discovering a new synergy banks +3 Archived Data on the spot.", "discovery_data":3},
	"disc_research_grant": {"branch":"science", "tier":2, "requires":["disc_archive_index"], "cost":12, "name":"Research Grant", "text":"+25% Archived Data at the end of each loop.", "research_bonus":0.25},
	"disc_rehearsed_pattern": {"branch":"science", "tier":3, "requires":["disc_research_grant"], "cost":40, "keystone":true, "name":"Rehearsed Pattern", "text":"BRINE has seen this work before: every synergy stabilizes one cycle sooner.", "stabilize_relief":1},

	# LIFE SUPPORT // air, water, food, and the tanks that hold them.
	"life_stored_rations": {"branch":"life_support", "tier":1, "cost":5, "name":"Stored Rations", "text":"Start each loop with +6 Food.", "start":{"food":6}},
	"life_deep_tanks": {"branch":"life_support", "tier":2, "requires":["life_stored_rations"], "cost":12, "name":"Deep Tanks", "text":"Start each loop with +6 Oxygen and +4 Water.", "start":{"oxygen":6, "water":4}},
	"life_expanded_tanks": {"branch":"life_support", "tier":3, "requires":["life_deep_tanks"], "cost":40, "keystone":true, "name":"Expanded Tanks", "text":"+10 Oxygen and +10 Water storage, and start each loop with +20 Data of margin against a bad cycle.", "capacity":{"oxygen":10, "water":10}, "start":{"data":20}},
	"life_seed_stock": {"branch":"life_support", "tier":2, "requires":["life_stored_rations"], "cost":12, "name":"Seed Stock", "text":"Start each loop with +4 Biomass, and +10 Food storage.", "start":{"biomass":4}, "capacity":{"food":10}},
	"life_closed_ecology": {"branch":"life_support", "tier":3, "requires":["life_seed_stock"], "cost":40, "keystone":true, "name":"Closed Ecology", "text":"Each working Life Support makes +2 Oxygen per cycle.", "life_support_oxygen":2},

	# CREW QUARTERS // the people, and how long they last.
	"crew_steady_rations": {"branch":"crew", "tier":1, "cost":5, "name":"Rebreathers", "text":"Held breath and helmet air last 25% longer.", "air_drain_rate":0.8},
	"crew_spare_bunks": {"branch":"crew", "tier":2, "requires":["crew_steady_rations"], "cost":12, "name":"Spare Bunks", "text":"+1 crew berth aboard the core.", "berth_bonus":1},
	"crew_shift_rotation": {"branch":"crew", "tier":3, "requires":["crew_spare_bunks"], "cost":40, "keystone":true, "name":"Shift Rotation", "text":"A second berth, and crew who walk like they know the route: +1 berth and 15% faster on their feet.", "berth_bonus":1, "walk_rate":1.15},
	"life_warm_thaw": {"branch":"crew", "tier":2, "requires":["crew_steady_rations"], "cost":12, "name":"Warm Thaw", "text":"Cryopod thaws and charging run 30% faster.", "thaw_rate":1.3},
	"crew_deck_boots": {"branch":"crew", "tier":3, "requires":["life_warm_thaw"], "cost":40, "keystone":true, "name":"Deck Boots", "text":"Magnetic soles: crew move 15% faster, and reach a flooding room before it is a story.", "walk_rate":1.15},

	# AI & ROBOTICS // BRINE's own hands.
	"drone_efficient_cells": {"branch":"robotics", "tier":1, "cost":5, "name":"Efficient Cells", "text":"Drone batteries drain 20% slower while working.", "battery_drain_rate":0.8},
	"drone_ore_sorters": {"branch":"robotics", "tier":2, "requires":["drone_efficient_cells"], "cost":12, "name":"Ore Sorters", "text":"Each drone delivery of Metal brings +1 Metal.", "drone_metal_bonus":1},
	"drone_deep_salvage": {"branch":"robotics", "tier":3, "requires":["drone_ore_sorters"], "cost":40, "keystone":true, "name":"Deep Salvage", "text":"Each drone delivery of Data also brings +1 Rare Minerals.", "salvage_rare_bonus":1},
	"drone_vectored_thrust": {"branch":"robotics", "tier":2, "requires":["drone_efficient_cells"], "cost":12, "name":"Vectored Thrust", "text":"Drones travel 20% faster.", "drone_speed":1.2},
	"drone_rapid_assembly": {"branch":"robotics", "tier":3, "requires":["drone_vectored_thrust"], "cost":40, "keystone":true, "name":"Rapid Assembly", "text":"Rooms go up 25% faster, and the crews that build them keep their own pace.", "build_rate":1.25},

	# ANOMALY // the readings BRINE has not agreed to yet.
	"anom_quiet_readings": {"branch":"anomaly", "tier":1, "cost":5, "name":"Quiet Readings", "text":"Start each loop with +2 Rare Minerals.", "start":{"rare_minerals":2}},
	"disc_rare_samples": {"branch":"anomaly", "tier":2, "requires":["anom_quiet_readings"], "cost":12, "name":"Rare Samples", "text":"Start each loop with +2 more Rare Minerals, and +20 Data storage.", "start":{"rare_minerals":2}, "capacity":{"data":20}},
	"disc_endowment": {"branch":"anomaly", "tier":3, "requires":["disc_rare_samples"], "cost":40, "keystone":true, "name":"Endowment", "text":"A further +25% Archived Data at the end of each loop.", "research_bonus":0.25},
	"anom_sympathetic_echo": {"branch":"anomaly", "tier":2, "requires":["anom_quiet_readings"], "cost":12, "name":"Sympathetic Echo", "text":"Discovering a new synergy banks +1 Archived Data on the spot.", "discovery_data":1},
	"anom_borrowed_time": {"branch":"anomaly", "tier":3, "requires":["anom_sympathetic_echo"], "cost":40, "keystone":true, "name":"Borrowed Time", "text":"Something out there keeps the lights on a little longer: machinery heat builds 35% slower and hull cracks widen 30% slower.", "heat_rate":0.65, "crack_rate":0.7},

	# STRUCTURE // the hull, the corridors, and the water outside them.
	"hull_reinforced_plating": {"branch":"structure", "tier":1, "cost":5, "name":"Reinforced Plating", "text":"+20 Integrity storage, and start each loop with +20 Integrity.", "capacity":{"integrity":20}, "start":{"integrity":20}},
	"hull_slow_fractures": {"branch":"structure", "tier":2, "requires":["hull_reinforced_plating"], "cost":12, "name":"Slow Fractures", "text":"Hull cracks widen 30% slower.", "crack_rate":0.7},
	"eng_bulkhead_seals": {"branch":"structure", "tier":3, "requires":["hull_slow_fractures"], "cost":40, "keystone":true, "name":"Bulkhead Seals", "text":"Flood water spreads between rooms 25% slower, and the doors remember which way they were shut.", "flood_rate":0.75},
	"hull_weld_training": {"branch":"structure", "tier":2, "requires":["hull_reinforced_plating"], "cost":12, "name":"Weld Training", "text":"Hull repairs finish 30% faster.", "hull_repair_rate":1.3},
	"hull_blast_doors": {"branch":"structure", "tier":3, "requires":["hull_weld_training"], "cost":40, "keystone":true, "name":"Blast Doors", "text":"Machinery heat that starts fires builds 35% slower, and a sealed section keeps its own air.", "heat_rate":0.65},
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

# Everything a node needs before it can be recovered. A perk without an explicit list falls back
# to the tier below it in the same department, which is how the tree read before it branched.
static func requirements(id: String) -> Array:
	var perk: Dictionary = PERKS[id]
	var listed: Array = perk.get("requires", [])
	if not listed.is_empty(): return listed.duplicate()
	for other in PERKS:
		if PERKS[other].branch == perk.branch and int(PERKS[other].tier) == int(perk.tier) - 1: return [other]
	return []

# The node a purchase pulse travels from: the first requirement still standing, or the first one.
static func previous(id: String) -> String:
	var needed: Array = requirements(id)
	if needed.is_empty(): return ""
	return str(needed[0])

# What is still missing before this node opens.
static func missing(meta, id: String) -> Array:
	var short: Array = []
	for needed in requirements(id):
		if not owned(meta, str(needed)): short.append(str(needed))
	return short

# "owned", "ready" (affordable, every requirement owned), "short" (requirements owned, too little
# Research) or "locked" (a requirement missing).
static func state(meta, id: String) -> String:
	if owned(meta, id): return "owned"
	if not missing(meta, id).is_empty(): return "locked"
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
# Command Override stages an extra blueprint; Rehearsed Pattern shortens every stabilization.
static func extra_cards(meta) -> int: return int(_sum_number(meta, "extra_cards"))
static func stabilize_relief(meta) -> int: return int(_sum_number(meta, "stabilize_relief"))

static func quote(id: String) -> String:
	for branch in BRANCHES:
		if PERKS.has(id) and branch.id == PERKS[id].branch: return str(branch.quote)
	return ""
