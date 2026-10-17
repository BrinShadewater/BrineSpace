extends SceneTree
## Oracle for evaluation-local recipe filtering. The legacy traversal below uses
## the unchanged geometry helpers; compare complete ordered results, not sets.
const Synergies = preload("res://scripts/synergy_manager.gd")
const Database = preload("res://scripts/room_database.gd")
const PASSAGES = ["corridor", "corner", "tee_corridor"]
const CROSS = "layout_05_cross"
const STRAIGHT = "layout_03_straight_ew"
var checks := 0
var failures := 0
var cases := 0
var authored_recipes := 0
var random_cases := 0
var mutation_cases := 0
var stabilized := {}

func _init() -> void:
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures += 1
		if failures <= 12: push_error(message)

func run() -> void:
	# This pure evaluator test does not load a scene or touch a save file.
	# Keep the normal isolated-test contract explicit for the maintained runner.
	if OS.get_user_data_dir().replace(char(92), "/") != OS.get_environment("BRINESPACE_TEST_USER_DIR"):
		push_error("Run synergy parity with the maintained scratch-profile runner")
		quit(2)
		return
	var definitions_before := var_to_bytes(Synergies.SYNERGIES)
	for i in range(Synergies.SYNERGIES.size()):
		if i % 3 == 0: stabilized[str(Synergies.SYNERGIES[i].id)] = true
	_test_presence_helper()
	_compare("empty", [], {})
	_test_authored_recipes()
	_test_order_and_alias_cases()
	_test_immediate_mutations()
	_test_random_stations()
	check(var_to_bytes(Synergies.SYNERGIES) == definitions_before, "Authored recipe dictionaries remain immutable")
	print("SYNERGY EVALUATION PARITY ", "PASS" if failures == 0 else "FAIL",
		" checks=", checks, " cases=", cases, " authored_recipes=", authored_recipes,
		" random_cases=", random_cases, " mutation_cases=", mutation_cases, " failures=", failures)
	quit(0 if failures == 0 else 1)

func _test_presence_helper() -> void:
	# Dynamic dispatch lets the unchanged baseline load and fail this contract,
	# rather than fail to parse because the candidate static helper is absent.
	var api: RefCounted = Synergies.new()
	if not api.has_method("_required_rooms_present"):
		check(false, "Evaluation requires a testable required-room presence helper")
		return
	var examples: Array = [
		[[], {}, true],
		[["alpha"], {}, false],
		[["alpha", "beta"], {"alpha": true}, false],
		[["alpha", "beta"], {"alpha": true, "beta": true}, true],
		[["alpha", "alpha"], {"alpha": true}, true],
		[["alpha", "alpha", "beta"], {"alpha": true}, false],
		[["beta", "alpha"], {"alpha": false, "beta": 0}, true],
		[[&"alpha", &"beta"], {"alpha": true, "beta": true}, true],
		[["alpha", &"missing"], {"alpha": true, "unrelated": true}, false],
	]
	for i in range(examples.size()):
		var example: Array = examples[i]
		var before := var_to_bytes([example[0], example[1]])
		var actual: Variant = api.call("_required_rooms_present", example[0], example[1])
		check(actual == example[2], "Required-room presence example %d" % i)
		check(var_to_bytes([example[0], example[1]]) == before, "Presence helper does not mutate example %d" % i)

func _legacy_evaluate(placed_rooms: Array, occupied: Dictionary) -> Dictionary:
	# Frozen from evaluate before presence filtering. Keep traversal and helper
	# calls here literal; this must not call the candidate evaluate recursively.
	var links: Array = Synergies.passage_links(occupied)
	var seen_links := {}
	for synergy in Synergies.SYNERGIES:
		if synergy.get("via_passage", false) or Synergies.is_pattern(synergy):
			continue
		var pairs: Array = Synergies._find_adjacent_pairs(synergy["rooms"], occupied)
		for pair in pairs:
			if not Synergies.within_passage_link(links, pair):
				Synergies._add_link(links, seen_links, synergy, pair)
		if not PASSAGES.has(str(synergy["rooms"][0])) and not PASSAGES.has(str(synergy["rooms"][1])):
			for cells in Synergies._find_passage_pairs(synergy["rooms"], occupied):
				Synergies._add_link(links, seen_links, synergy, cells, true)
	for synergy in Synergies.SYNERGIES:
		if not Synergies.is_pattern(synergy): continue
		for cells in Synergies._find_pattern_chains(synergy["rooms"], occupied):
			Synergies._add_link(links, seen_links, synergy, cells)
	for room in placed_rooms:
		if room["id"] != "cryo_chamber": continue
		var safe_wake: Dictionary = Synergies.get_synergy("safe_wake_protocol")
		for neighbor_pos in Synergies._adjacent_tagged_cells(room["pos"], occupied, "medical"):
			Synergies._add_link(links, seen_links, safe_wake, [room["pos"], neighbor_pos])
	return {"links": links}

func _compare(label: String, placed: Array, occupied: Dictionary) -> Dictionary:
	cases += 1
	var before := var_to_bytes([placed, occupied])
	var placed_refs := placed.duplicate()
	var cells := occupied.keys()
	var occupied_refs := occupied.values()
	var expected := _legacy_evaluate(placed, occupied)
	check(var_to_bytes([placed, occupied]) == before, label + ": legacy input immutability")
	var actual: Dictionary = Synergies.evaluate(placed, occupied)
	check(var_to_bytes([placed, occupied]) == before, label + ": candidate input immutability")
	check(var_to_bytes(actual) == var_to_bytes(expected), label + ": full ordered links, cells and metadata")
	check(var_to_bytes(Synergies.cycle_bonus(actual.links)) == var_to_bytes(Synergies.cycle_bonus(expected.links)), label + ": ordered normal bonus")
	check(var_to_bytes(Synergies.cycle_bonus(actual.links, stabilized)) == var_to_bytes(Synergies.cycle_bonus(expected.links, stabilized)), label + ": ordered stabilized bonus")
	var identities_match := placed.size() == placed_refs.size() and occupied.keys() == cells
	if identities_match:
		for i in range(placed.size()):
			if not is_same(placed[i], placed_refs[i]): identities_match = false
		for i in range(cells.size()):
			if not is_same(occupied[cells[i]], occupied_refs[i]): identities_match = false
	check(identities_match, label + ": room identity and occupied aliases remain intact")
	return actual

func _turn(cell: Vector2i, quarter: int) -> Vector2i:
	var result := cell
	for _i in range(quarter): result = Vector2i(-result.y, result.x)
	return result

func _room(id: String, cell: Vector2i, quarter := 0, layout := STRAIGHT) -> Dictionary:
	var room: Dictionary = Database.get_room(id)
	if room.is_empty(): room = {"id": id, "tags": []}
	room.id = id
	room.pos = cell
	room.rotation = quarter
	room.layout = layout
	return room

func _add(placed: Array, occupied: Dictionary, room: Dictionary, footprint := Vector2i.ONE) -> void:
	placed.append(room)
	for y in range(footprint.y):
		for x in range(footprint.x): occupied[room.pos + Vector2i(x, y)] = room

func _has_link(result: Dictionary, id: String) -> bool:
	for link in result.links:
		if str(link.id) == id: return true
	return false

func _test_authored_recipes() -> void:
	for recipe in Synergies.SYNERGIES:
		authored_recipes += 1
		var ids: Array = recipe.rooms
		for quarter in range(4):
			for passage in [false, true]:
				var placed: Array = []
				var occupied := {}
				for i in range(ids.size()):
					var x: int = i
					if passage: x = -1 if i == 0 else i
					_add(placed, occupied, _room(str(ids[i]), _turn(Vector2i(x, 0), quarter), quarter))
				if passage: _add(placed, occupied, _room("corridor", Vector2i.ZERO, quarter))
				var label := "%s q%d %s" % [recipe.id, quarter, "passage" if passage else "direct"]
				var result := _compare(label, placed, occupied)
				if not passage and not recipe.get("via_passage", false):
					check(_has_link(result, str(recipe.id)), label + ": authored recipe actually exercised")
				elif passage and not ids.any(func(id): return PASSAGES.has(str(id))):
					check(_has_link(result, str(recipe.id)), label + ": one-passage recipe actually exercised")
		# Preserve real blueprint layouts/tags too; these may intentionally fail
		# to connect at this orientation, unlike the positive straight fixtures.
		var authored: Array = []
		var authored_occupied := {}
		for i in range(ids.size()):
			var room: Dictionary = Database.get_room(str(ids[i]))
			if room.is_empty(): room = _room(str(ids[i]), Vector2i(i, 0))
			room.pos = Vector2i(i, -3)
			room.rotation = authored_recipes % 4
			_add(authored, authored_occupied, room)
		_compare(str(recipe.id) + " authored metadata", authored, authored_occupied)
		var partial: Array = []
		var partial_occupied := {}
		_add(partial, partial_occupied, _room(str(ids[0]), Vector2i(-4, -4)))
		_add(partial, partial_occupied, _room("parity-unrelated", Vector2i(-3, -4)))
		_compare(str(recipe.id) + " missing required endpoints", partial, partial_occupied)

func _test_order_and_alias_cases() -> void:
	var placed: Array = []
	var occupied := {}
	# Two one-passage routes to the same endpoint pair exercise first-route
	# precedence and duplicate suppression in both occupied insertion orders.
	_add(placed, occupied, _room("storage_bay", Vector2i(-1, -1), 0, CROSS))
	_add(placed, occupied, _room("salvage_workshop", Vector2i.ZERO, 0, CROSS))
	_add(placed, occupied, _room("corner", Vector2i(0, -1), 0, CROSS))
	_add(placed, occupied, _room("tee_corridor", Vector2i(-1, 0), 0, CROSS))
	_compare("duplicate passage routes negative cells", placed, occupied)
	var reverse_occupied := {}
	var reverse_cells := occupied.keys()
	reverse_cells.reverse()
	for cell in reverse_cells: reverse_occupied[cell] = occupied[cell]
	var reverse_placed := placed.duplicate()
	reverse_placed.reverse()
	_compare("duplicate passage routes reversed insertion", reverse_placed, reverse_occupied)
	# Parts Passage also suppresses an otherwise direct endpoint/corridor
	# recipe within that same three-cell link. Do not turn the result into a set.
	placed = []; occupied = {}
	_add(placed, occupied, _room("storage_bay", Vector2i(-1, 0), 0, CROSS))
	_add(placed, occupied, _room("corridor", Vector2i.ZERO, 0, CROSS))
	_add(placed, occupied, _room("salvage_workshop", Vector2i(1, 0), 0, CROSS))
	_compare("direct pair inside a passage link", placed, occupied)
	# Separate same-ID candidates must never satisfy a missing different ID.
	placed = []; occupied = {}
	_add(placed, occupied, _room("storage_bay", Vector2i(-1, 0), 0, CROSS))
	_add(placed, occupied, _room("storage_bay", Vector2i(1, 0), 0, CROSS))
	_add(placed, occupied, _room("corridor", Vector2i.ZERO, 0, CROSS))
	_compare("same-ID candidates", placed, occupied)
	# Larger owners deliberately alias the exact same dictionary at every cell.
	# Direct and one-passage routes coexist for those owners; current cell-key
	# behavior, including ordered duplicate handling, is the oracle.
	placed = []; occupied = {}
	_add(placed, occupied, _room("storage_bay", Vector2i(-2, -2), 0, CROSS), Vector2i(1, 2))
	_add(placed, occupied, _room("salvage_workshop", Vector2i(-1, -2), 0, CROSS), Vector2i(1, 3))
	_add(placed, occupied, _room("corner", Vector2i(-2, 0), 0, CROSS))
	_compare("large-footprint aliases direct and passage", placed, occupied)
	# Presence filtering must consult occupied, as the geometry helpers do;
	# placed_rooms is used separately by the tagged-medical Cryo tail.
	_compare("occupied-only endpoint presence", [], occupied)
	_compare("placed-only endpoints do not create adjacency", placed, {})

func _test_immediate_mutations() -> void:
	var placed: Array = []
	var occupied := {}
	var cryo := _room("cryo_chamber", Vector2i.ZERO, 0, CROSS)
	var medical := _room("med_bay", Vector2i(1, 0), 0, CROSS)
	medical.tags = ["medical"]
	var support := _room("life_support", Vector2i(-2, 0), 0, CROSS)
	_add(placed, occupied, cryo)
	_add(placed, occupied, medical)
	_add(placed, occupied, support)
	for change in ["initial", "id-missing", "id-restore", "layout-straight", "rotation-blocked", "rotation-restore", "layout-restore", "tags-remove", "tags-restore", "medical-id-change", "medical-id-restore"]:
		match change:
			"id-missing": support.id = "parity-no-life-support"
			"id-restore": support.id = "life_support"
			"layout-straight": medical.layout = STRAIGHT
			"rotation-blocked": medical.rotation = 1
			"rotation-restore": medical.rotation = 0
			"layout-restore": medical.layout = CROSS
			"tags-remove": medical.tags = []
			"tags-restore": medical.tags = ["medical"]
			"medical-id-change": medical.id = "parity-tagged-medical"
			"medical-id-restore": medical.id = "med_bay"
		mutation_cases += 1
		var result := _compare("immediate mutation " + change, placed, occupied)
		check(_has_link(result, "safe_wake_protocol") == (change not in ["rotation-blocked", "tags-remove"]), "Tagged-medical Cryo mutation is nonvacuous: " + change)
	# No Life Support anywhere: the recipe pair cannot pass the new filter,
	# but the independent medical-tag fallback must still produce its link.
	occupied.erase(support.pos); placed.erase(support)
	var result := _compare("Cryo tagged medical without Life Support", placed, occupied)
	check(_has_link(result, "safe_wake_protocol"), "Medical-tag Cryo fallback survives absent Life Support")

func _test_random_stations() -> void:
	var ids: Array = ["parity-unrelated"]
	for recipe in Synergies.SYNERGIES:
		for id in recipe.rooms:
			if not ids.has(str(id)): ids.append(str(id))
	for seed_index in range(3):
		var rng := RandomNumberGenerator.new()
		rng.seed = 20261015 + seed_index * 104729
		for sample in range(16):
			var placed: Array = []
			var occupied := {}
			for _attempt in range(8 + sample):
				var cell := Vector2i(rng.randi_range(-4, 4), rng.randi_range(-4, 4))
				var footprint := Vector2i(2, 2) if rng.randi_range(0, 7) == 0 else Vector2i.ONE
				var clear := true
				for y in range(footprint.y):
					for x in range(footprint.x):
						if occupied.has(cell + Vector2i(x, y)): clear = false
				if not clear: continue
				var id: String = ids[rng.randi_range(0, ids.size() - 1)]
				var layout: String = CROSS if rng.randi_range(0, 2) == 0 else STRAIGHT
				_add(placed, occupied, _room(id, cell, rng.randi_range(0, 3), layout), footprint)
			random_cases += 1
			_compare("seed %d sparse station %d" % [seed_index, sample], placed, occupied)
