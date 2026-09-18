extends RefCounted
## Archived Data shop (owner playtest, Sept 17): the single meta currency buys upgrades
## (ResearchTree), room blueprints and permanent crew and companions. Archived Data is stored in
## the existing MetaState.total_research_points so older profiles keep their balance; purchases
## are recorded in MetaState.purchased_ids so the balance is lifetime Data minus everything
## bought. Rooms and characters a profile already had before the shop stay free and unlocked.
##
## Characters and companions thawed or rebooted during a loop play for the rest of that loop;
## once met, they can be bought here to join future loops. Stabilizing a pattern halves the cost
## of its related blueprint and doubles the pattern's own bonus.

const Rooms = preload("res://scripts/room_database.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const ResearchTree = preload("res://scripts/research_tree.gd")

const CURRENCY := "Archived Data"
const ROOM_COSTS := {"common": 12, "uncommon": 20, "rare": 32}
const CHARACTER_COSTS := {"veld": 30, "branforth": 30, "marsh": 40, "river": 20, "josh": 20, "margot": 25}
const CHARACTER_NAMES := {"brine": "BRINE", "bill": "Major Bill", "veld": "Dr. Veld", "branforth": "Chief Engineer Branforth", "marsh": "Marsh", "river": "River", "josh": "Josh", "margot": "Margot"}
# The roster the Crew & Companions page shows, in order. BRINE and Bill are aboard from the
# start (owner playtest, Sept 17), so they appear owned and cost nothing.
const ROSTER := ["brine", "bill", "veld", "branforth", "marsh", "river", "josh", "margot"]
const ALWAYS_ABOARD := ["brine", "bill"]
# Class colours match the room departments: operations red, science blue, engineering yellow,
# AI and robotics white, companions purple.
const CHARACTER_COLORS := {"brine": "#e8eef0", "bill": "#d9534f", "veld": "#4f8fe6", "branforth": "#e6c84f", "marsh": "#e8eef0", "river": "#9c5de8", "josh": "#9c5de8", "margot": "#9c5de8"}
const CHARACTER_CLASSES := {"brine": "STATION AI", "bill": "OPERATIONS", "veld": "SCIENCE & MEDICAL", "branforth": "ENGINEERING", "marsh": "AI & ROBOTICS", "river": "COMPANION", "josh": "COMPANION", "margot": "COMPANION"}
const COMPANIONS := ["river", "josh", "margot"]
const STABILIZE_DATA := 5

static func balance(meta) -> int:
	return ResearchTree.available(meta)

static func purchases_spent(meta) -> int:
	var total := 0
	if meta == null: return total
	for key in meta.purchased_ids:
		total += int(meta.purchased_ids[key])
	return total

# The pattern whose stabilization used to decrypt this blueprint, if any.
static func related_pattern(room_id: String) -> Dictionary:
	for pattern in Synergies.all_synergies():
		if str(pattern.get("unlock_room_id", "")) == room_id: return pattern
	return {}

static func room_cost(meta, room_id: String) -> int:
	var room: Dictionary = Rooms.get_room(room_id)
	var cost := int(ROOM_COSTS.get(str(room.get("rarity", "common")), ROOM_COSTS.common))
	var pattern := related_pattern(room_id)
	if not pattern.is_empty() and meta != null and meta.stabilized_synergy_ids.has(pattern.id): cost = int(ceil(cost * 0.5))
	return cost

static func blueprint_ids() -> Array:
	var rooms: Dictionary = Rooms.all_rooms()
	var ids: Array = []
	for id in rooms:
		if str(rooms[id].get("rarity", "")) in ROOM_COSTS: ids.append(id)
	var order := ["common", "uncommon", "rare"]
	ids.sort_custom(func(a, b):
		var ra := order.find(str(rooms[a].rarity))
		var rb := order.find(str(rooms[b].rarity))
		if ra != rb: return ra < rb
		if str(rooms[a].category) != str(rooms[b].category): return str(rooms[a].category) < str(rooms[b].category)
		return str(rooms[a].display_name) < str(rooms[b].display_name))
	return ids

# "owned", "ready" or "short".
static func room_state(meta, room_id: String) -> String:
	if meta.unlocked_room_ids.has(room_id): return "owned"
	return "ready" if balance(meta) >= room_cost(meta, room_id) else "short"

static func buy_room(meta, room_id: String) -> bool:
	if not Rooms.all_rooms().has(room_id) or room_state(meta, room_id) != "ready": return false
	var cost := room_cost(meta, room_id)
	meta.purchased_ids["room:" + room_id] = cost
	meta.unlocked_room_ids[room_id] = true
	if meta.save_to_disk() != OK:
		meta.purchased_ids.erase("room:" + room_id)
		meta.unlocked_room_ids.erase(room_id)
		return false
	return true

static func character_owned(meta, id: String) -> bool:
	if id in ALWAYS_ABOARD: return true
	return meta.unlocked_companion_ids.has(id) if id in COMPANIONS else meta.unlocked_architect_ids.has(id)

# Portrait art for the roster; BRINE uses her comms portrait.
static func portrait(id: String) -> Texture2D:
	if id == "brine":
		var image := Image.new()
		if preload("res://scripts/safe_image.gd").load_png(image, "res://character/brine-comms-v14/portrait.png") != OK: return null
		return ImageTexture.create_from_image(image)
	if id in COMPANIONS: return preload("res://scripts/companions.gd").portrait(id)
	return preload("res://scripts/architects.gd").selection_portrait(id)

# "owned", "ready", "short" or "unmet" (thaw or reboot them during a loop first).
static func character_state(meta, id: String) -> String:
	if character_owned(meta, id): return "owned"
	if not meta.met_character_ids.has(id): return "unmet"
	return "ready" if balance(meta) >= int(CHARACTER_COSTS[id]) else "short"

static func buy_character(meta, id: String) -> bool:
	if not CHARACTER_COSTS.has(id) or character_state(meta, id) != "ready": return false
	meta.purchased_ids["crew:" + id] = int(CHARACTER_COSTS[id])
	if id in COMPANIONS: meta.unlocked_companion_ids[id] = true
	else: meta.unlocked_architect_ids[id] = true
	if meta.save_to_disk() != OK:
		meta.purchased_ids.erase("crew:" + id)
		if id in COMPANIONS: meta.unlocked_companion_ids.erase(id)
		else: meta.unlocked_architect_ids.erase(id)
		return false
	return true

# Stabilized patterns pay double their per-cycle bonus in every later loop.
static func synergy_bonus(meta, link: Dictionary) -> Dictionary:
	var bonus: Dictionary = link.get("bonus", {})
	if meta == null or not meta.stabilized_synergy_ids.has(str(link.get("id", ""))): return bonus
	var doubled := {}
	for key in bonus: doubled[key] = int(bonus[key]) * 2
	return doubled
