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
	instance.meta.save_path = "user://brine_condenser_gameplay_fixture_%d.json"%OS.get_process_id()
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
	var definition := Rooms.get_room("tidal_condenser")
	expect(not definition.is_empty(), "Condenser definition exists")
	if definition.is_empty():
		quit(1)
		return
	var instance = game()
	expect(not instance.meta.unlocked_room_ids.has("tidal_condenser"), "Condenser starts locked")
	for doctrine in ["industry", "biosphere"]:
		expect(not Runs.build_deck([doctrine], instance.meta.unlocked_room_ids).has("tidal_condenser"), "Locked condenser absent from draft")
	instance.meta.unlocked_room_ids["tidal_condenser"] = true
	for doctrine in ["industry", "biosphere"]:
		expect(Runs.build_deck([doctrine], instance.meta.unlocked_room_ids).has("tidal_condenser"), "Unlocked condenser enters authored doctrine")
	var hint: String = instance._card_synergy_hint("tidal_condenser").to_lower()
	for forbidden in ["nutrient mist", "chilled cells", "hydroponics", "battery"]:
		expect(not hint.contains(forbidden), "Unknown card hint must not reveal " + forbidden)
	instance.running = true
	instance.resources.metal = 7
	instance.resources.data = 1
	instance.hand.assign(["tidal_condenser"])
	instance.selected_card_id = "tidal_condenser"
	instance._on_grid_clicked(Vector2i(10, 10))
	expect(instance.placed_rooms.is_empty() and instance.resources.metal == 7, "Unaffordable build rejected without spending")
	instance.resources.data = 2
	instance._on_grid_clicked(Vector2i(10, 10))
	# Paid placement queues an architect-built order since the Sept 8 construction
	# pass; costs are spent up front. Completion is covered by the crew
	# construction tests, so place the room directly for the economy checks below.
	expect(instance.drone_fleet.reserved(Vector2i(10, 10)) and instance.resources.metal == 0 and instance.resources.data == 0, "Actual build spends 7 Metal and 2 Data and queues construction")
	instance.drone_fleet.orders.clear()
	add_room(instance, "tidal_condenser", Vector2i(10, 10), instance.selected_rotation)
	instance.resources.power = 2
	var before_water: int = instance.resources.water
	instance._apply_room_economy()
	expect(instance.resources.water == before_water + 2, "Functioning condenser produces 2 Water")
	expect(instance.power_used == 2, "Condenser uses two Power")
	before_water = instance.resources.water
	instance.resources.power = 1
	instance._apply_room_economy()
	expect(instance.resources.water == before_water and not instance.powered_room_cells.has(Vector2i(10, 10)), "Insufficient power stops condenser")
	dispose(instance)
	# Real economy/discovery progression, including an interrupted streak.
	instance = game()
	add_room(instance, "reactor", Vector2i(10, 10))
	add_room(instance, "life_support", Vector2i(11, 10))
	instance.resources.power = 2
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("thermal_reclamation", 0) == 1, "Functioning pair starts discovery")
	instance.occupied[Vector2i(11,10)].suspended = true
	instance.resources.power = 0
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("thermal_reclamation", -1) == 0, "Offline cycle resets progress")
	instance.occupied[Vector2i(11,10)].suspended = false
	for cycle_index in range(3):
		instance.resources.power = 2
		instance._apply_room_economy()
		instance._advance_synergy_discovery_cycle()
		if cycle_index < 2:
			expect(not instance.meta.unlocked_room_ids.has("tidal_condenser"), "Unlock must wait for third consecutive cycle")
	expect(instance.meta.unlocked_room_ids.has("tidal_condenser"), "Three functioning cycles unlock condenser")
	expect(instance.draw_pile.count("tidal_condenser") == 1, "One current-run condenser prototype")
	instance._award_synergy_stabilization(Synergies.get_synergy("thermal_reclamation"))
	expect(instance.draw_pile.count("tidal_condenser") == 1, "No repeated prototype reward")
	for id in ["nutrient_mist", "chilled_cells"]:
		var research_before: int = instance.meta.total_research_points
		instance._award_synergy_stabilization(Synergies.get_synergy(id))
		instance._award_synergy_stabilization(Synergies.get_synergy(id))
		expect(instance.meta.total_research_points == research_before + 3, "Terminal reward grants 3 Research once")
	dispose(instance)
	for pattern in ["nutrient_mist", "chilled_cells"]:
		var synergy := Synergies.get_synergy(pattern)
		for q in range(4):
			instance = game()
			var offset := Vector2i.RIGHT
			for unused in range(q):
				offset = Vector2i(-offset.y, offset.x)
			add_room(instance, "tidal_condenser", Vector2i(10, 10), q)
			var partner_q := q
			add_room(instance, str(synergy.rooms[1]), Vector2i(10, 10) + offset, partner_q % 4)
			instance.resources.power = 4
			instance.resources.biomass = 4
			instance.resources.water = 4
			instance._apply_room_economy()
			expect(instance.active_synergies.has(pattern), "Rotated functioning pair activates " + pattern)
			instance.occupied[Vector2i(10, 10)].rotation = (q + 1) % 4
			instance._check_synergies()
			instance._apply_room_economy()
			expect(not instance.active_synergies.has(pattern), "Sealed condenser side prevents " + pattern)
			dispose(instance)
	if failures == 0:
		print("CONDENSER GAMEPLAY PASS: locking/decks, paid click build, economy, starvation, hidden hints, interrupted discovery, prototype and idempotent rewards")
	quit(0 if failures == 0 else 1)
