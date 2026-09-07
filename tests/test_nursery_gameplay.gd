extends SceneTree
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
const Synergies = preload("res://scripts/synergy_manager.gd")
const Runs = preload("res://scripts/run_manager.gd")
var failures := 0

class Fixture extends Main:
	# Skip presentation only; use real click, cost, placement and economy paths.
	func _refresh_all() -> void:
		pass

func expect(value: bool, message: String) -> void:
	if not value:
		failures += 1
		push_error(message)

func game():
	var instance = Fixture.new()
	instance.meta.save_path = "user://brine_nursery_gameplay_fixture.json"
	instance.meta.discovered_synergy_ids.clear()
	instance.meta.stabilized_synergy_ids.clear()
	instance.meta.unlocked_room_ids.clear()
	for id in Rooms.STARTING_UNLOCKS:
		instance.meta.unlocked_room_ids[id] = true
	return instance

func dispose(instance) -> void:
	var path: String = instance.meta.save_path
	instance.free()
	if FileAccess.file_exists(path):
		DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func add_room(instance, id: String, cell: Vector2i, q := 0) -> void:
	var room := Rooms.get_room(id).duplicate(true)
	room.pos = cell
	room.rotation = q
	instance.placed_rooms.append(room)
	instance.occupied[cell] = room
	instance._check_synergies()

func _init() -> void:
	var definition := Rooms.get_room("mycelium_nursery")
	expect(not definition.is_empty(), "Nursery definition exists")
	if definition.is_empty():
		quit(1)
		return
	var instance = game()
	expect(not instance.meta.unlocked_room_ids.has("mycelium_nursery"), "Nursery starts locked")
	for doctrine in ["biosphere", "recovery"]:
		expect(not Runs.build_deck([doctrine], instance.meta.unlocked_room_ids).has("mycelium_nursery"), "Locked nursery absent from draft")
	instance.meta.unlocked_room_ids["mycelium_nursery"] = true
	for doctrine in ["biosphere", "recovery"]:
		expect(Runs.build_deck([doctrine], instance.meta.unlocked_room_ids).has("mycelium_nursery"), "Unlocked nursery enters authored doctrine")
	var hint: String = instance._card_synergy_hint("mycelium_nursery").to_lower()
	for forbidden in ["culture exchange", "restorative culture", "bio lab", "med bay"]:
		expect(not hint.contains(forbidden), "Unknown card hint must not reveal " + forbidden)
	instance.running = true
	instance.resources.metal = 7
	instance.resources.biomass = 2
	instance.hand.assign(["mycelium_nursery"])
	instance.selected_card_id = "mycelium_nursery"
	instance._on_grid_clicked(Vector2i(10, 10))
	expect(instance.placed_rooms.is_empty() and instance.resources.metal == 7, "Unaffordable build rejected without spending")
	instance.resources.biomass = 3
	instance._on_grid_clicked(Vector2i(10, 10))
	expect(instance.placed_rooms.size() == 1 and instance.resources.metal == 0 and instance.resources.biomass == 0, "Actual build spends 7 Metal and 3 Biomass")
	instance.resources.power = 2
	instance.resources.biomass = 1
	var before_food: int = instance.resources.food
	instance._apply_room_economy()
	expect(instance.resources.food == before_food + 3 and instance.resources.biomass == 0, "Functioning nursery consumes Biomass and produces 3 Food")
	expect(instance.power_used == 1, "Nursery uses one Power")
	before_food = instance.resources.food
	instance.resources.power = 2
	instance._apply_room_economy()
	expect(instance.resources.food == before_food and not instance.powered_room_cells.has(Vector2i(10, 10)), "Starved nursery stops")
	dispose(instance)
	# Real economy/discovery progression, including an interrupted streak.
	instance = game()
	add_room(instance, "hydroponics_bay", Vector2i(10, 10))
	add_room(instance, "quarantine_cell", Vector2i(11, 10))
	instance.resources.power = 2
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("substrate_recovery", 0) == 1, "Functioning pair starts discovery")
	instance.resources.power = 0
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("substrate_recovery", -1) == 0, "Offline cycle resets progress")
	for cycle_index in range(3):
		instance.resources.power = 2
		instance._apply_room_economy()
		instance._advance_synergy_discovery_cycle()
		if cycle_index < 2:
			expect(not instance.meta.unlocked_room_ids.has("mycelium_nursery"), "Unlock must wait for third consecutive cycle")
	expect(instance.meta.unlocked_room_ids.has("mycelium_nursery"), "Three functioning cycles unlock nursery")
	expect(instance.draw_pile.count("mycelium_nursery") == 1, "One current-run nursery prototype")
	instance._award_synergy_stabilization(Synergies.get_synergy("substrate_recovery"))
	expect(instance.draw_pile.count("mycelium_nursery") == 1, "No repeated prototype reward")
	for id in ["culture_exchange", "restorative_culture"]:
		var research_before: int = instance.meta.total_research_points
		instance._award_synergy_stabilization(Synergies.get_synergy(id))
		instance._award_synergy_stabilization(Synergies.get_synergy(id))
		expect(instance.meta.total_research_points == research_before + 3, "Terminal reward grants 3 Research once")
	dispose(instance)
	for pattern in ["culture_exchange", "restorative_culture"]:
		var synergy := Synergies.get_synergy(pattern)
		for q in range(4):
			instance = game()
			var offset := Vector2i.RIGHT
			for unused in range(q):
				offset = Vector2i(-offset.y, offset.x)
			add_room(instance, "mycelium_nursery", Vector2i(10, 10), q)
			var partner_q := q + 1 if pattern == "restorative_culture" else q
			add_room(instance, str(synergy.rooms[1]), Vector2i(10, 10) + offset, partner_q % 4)
			instance.resources.power = 4
			instance.resources.biomass = 4
			instance.resources.water = 4
			instance._apply_room_economy()
			expect(instance.active_synergies.has(pattern), "Rotated functioning pair activates " + pattern)
			instance.occupied[Vector2i(10, 10)].rotation = (q + 1) % 4
			instance._check_synergies()
			instance._apply_room_economy()
			expect(not instance.active_synergies.has(pattern), "Sealed nursery side prevents " + pattern)
			dispose(instance)
	if failures == 0:
		print("NURSERY GAMEPLAY PASS: locking/decks, paid click build, economy, starvation, hidden hints, interrupted discovery, prototype and idempotent rewards")
	quit(0 if failures == 0 else 1)
