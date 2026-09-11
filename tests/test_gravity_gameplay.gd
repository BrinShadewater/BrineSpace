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
	instance.meta.save_path = "user://brine_gravity_gameplay_fixture_%d.json"%OS.get_process_id()
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
	var instance=game()
	expect(not instance.meta.unlocked_room_ids.has("gravity_loom"),"Loom starts locked")
	for doctrine in ["science","anomaly"]:
		expect(not Runs.build_deck([doctrine],instance.meta.unlocked_room_ids).has("gravity_loom"),"Locked loom absent from draft")
	instance.meta.unlocked_room_ids["gravity_loom"]=true
	for doctrine in ["science","anomaly"]:
		expect(Runs.build_deck([doctrine],instance.meta.unlocked_room_ids).has("gravity_loom"),"Unlocked loom enters doctrine")
	instance.running=true
	instance.resources.metal=12
	instance.resources.data=8
	instance.resources.rare_minerals=2
	instance.hand.assign(["gravity_loom"])
	instance.selected_card_id="gravity_loom"
	instance._on_grid_clicked(Vector2i(10,10))
	expect(instance.placed_rooms.is_empty(),"Missing rare mineral rejects paid build")
	instance.resources.rare_minerals=3
	instance._on_grid_clicked(Vector2i(10,10))
	# Paid placement queues an architect-built order since the Sept 8 construction
	# pass; costs are spent up front. Completion is covered by the crew
	# construction tests, so place the room directly for the economy checks below.
	expect(instance.drone_fleet.reserved(Vector2i(10,10)) and instance.resources.metal==0 and instance.resources.data==0 and instance.resources.rare_minerals==0,"Paid loom spends 12 metal 8 data 3 rare and queues construction")
	instance.drone_fleet.orders.clear()
	add_room(instance,"gravity_loom",Vector2i(10,10),instance.selected_rotation)
	instance.resources.power=4
	instance._apply_room_economy()
	expect(instance.resources.data==1 and instance.resources.rare_minerals==1 and instance.power_used==4,"Loom produces data and rare using four power")
	instance.resources.power=3
	instance._apply_room_economy()
	expect(instance.resources.data==1 and instance.resources.rare_minerals==1 and not instance.powered_room_cells.has(Vector2i(10,10)),"Starved loom produces nothing")
	for id in ["inertial_containment","mass_sorting","geometric_echo"]:
		expect(not Synergies.get_synergy(id).is_empty(),"Authored pattern exists: "+id)
	dispose(instance)
	var definition=Rooms.get_room("gravity_loom")
	for field in ["cost","production","consumption"]:
		for resource in definition[field]:
			expect(Rooms.RESOURCE_ICONS.has(resource),"Canonical resource key: "+resource)
	instance=game()
	add_room(instance,"anomaly_lab",Vector2i(10,10),3)
	add_room(instance,"shield_generator",Vector2i(11,10),1)
	instance.resources.power=8
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("inertial_containment",0)==1,"Connected functioning pair starts loom discovery")
	instance.occupied[Vector2i(11,10)].suspended=true
	instance._apply_room_economy()
	instance._advance_synergy_discovery_cycle()
	expect(instance.synergy_stabilization_progress.get("inertial_containment",-1)==0,"Suspension interrupts loom streak")
	instance.occupied[Vector2i(11,10)].suspended=false
	for cycle in range(3):
		instance.resources.power=8
		instance._apply_room_economy()
		instance._advance_synergy_discovery_cycle()
		if cycle<2: expect(not instance.meta.unlocked_room_ids.has("gravity_loom"),"Loom waits for third functioning cycle")
	expect(instance.meta.unlocked_room_ids.has("gravity_loom"),"Loom blueprint unlocked")
	expect(instance.draw_pile.count("gravity_loom")==1,"One loom prototype delivered")
	instance._award_synergy_stabilization(Synergies.get_synergy("inertial_containment"))
	expect(instance.draw_pile.count("gravity_loom")==1,"Loom prototype is idempotent")
	dispose(instance)
	for pattern in ["mass_sorting","geometric_echo"]:
		for q in range(4):
			instance=game()
			var offset=Vector2i.RIGHT
			for unused in range(q): offset=Vector2i(-offset.y,offset.x)
			var partner=str(Synergies.get_synergy(pattern).rooms[1])
			add_room(instance,"gravity_loom",Vector2i(10,10),q)
			add_room(instance,partner,Vector2i(10,10)+offset,(q+1)%4 if partner=="mining_drone_bay" else q)
			var research_before: int=instance.meta.total_research_points
			for cycle in range(3):
				instance.resources.power=10
				instance._apply_room_economy()
				expect(instance.active_synergies.has(pattern),"Functioning rotated terminal pair: "+pattern)
				instance._advance_synergy_discovery_cycle()
			expect(instance.meta.total_research_points==research_before+3,"Terminal grants three research after stabilization")
			instance._award_synergy_stabilization(Synergies.get_synergy(pattern))
			expect(instance.meta.total_research_points==research_before+3,"Terminal research is idempotent")
			instance.occupied[Vector2i(10,10)].suspended=true
			instance._apply_room_economy()
			expect(not instance.active_synergies.has(pattern),"Suspended loom stops terminal bonus")
			dispose(instance)
	if failures==0: print("GRAVITY GAMEPLAY PASS: canonical resources, paid build/economy, interrupted three-cycle unlock, one prototype, rotated terminal progression and idempotent rewards")
	quit(0 if failures==0 else 1)
