extends SceneTree
## Controlled paid-build comparison, using normal cycle costs and failures.
var game
var elapsed := 0.0
var cycle_clock := 0.0
var rows: Array = []
var delivered := 0
var charging := 0
var work_seconds := 0.0
var travel_seconds := 0.0
var waiting_seconds := 0.0
var recording := false
var failures := 0
var kind := "mining"
# A run that ends mid-measurement says nothing about the economy unless it says why.
var ended_reason := ""
var ended_resources: Dictionary = {}
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg=="--kind=salvage": kind = "salvage"
	call_deferred("run")
func step() -> void:
	if not game.running:
		if ended_reason.is_empty():
			ended_reason = str(game.summary_outcome_label.text) if game.summary_outcome_label != null else "unknown"
			ended_resources = game.resources.duplicate()
		return
	game.paused = false
	if recording:
		for drone in game.drone_fleet.drones.values():
			if drone.kind!=kind: continue
			if drone.phase=="working": work_seconds += 0.1
			elif drone.phase in ["outbound","returning","launching","docking"]: travel_seconds += 0.1
			elif game.resources.power==0 and drone.get("battery",12.0)<11.99: waiting_seconds += 0.1
	preload("res://scripts/ward_repair.gd").use_clock() # Ward rewards, not crew pathing, are under test.
	game._update_wreck_clearance(0.1)
	# Rooms are built by the crew, and the core's emergency builder stands down whenever
	# crew builders are available - which _update_wreck_clearance always requests. Advance
	# the crew and the core pod alongside the fleet or the paid orders are never put up.
	game._update_test_walker(0.1)
	preload("res://scripts/architects.gd").advance_core(game,0.1)
	if recording:
		delivered += int(game.drone_fleet.delivered.get("metal",0))
		charging += game.drone_fleet.power_spent
	elapsed += 0.1
	cycle_clock += 0.1
	if cycle_clock>=20.0:
		cycle_clock -= 20.0
		game._advance_cycle()
# A loop has no crew until the architect wakes out of the core pod. Without this the
# fixture paid for rooms nobody could ever put up: it reported a station that never
# built, delivered no metal and ran its whole 300 seconds with work_seconds at zero.
func wake_architect() -> bool:
	var Architects = preload("res://scripts/architects.gd")
	for frame in range(600):
		if Architects.present(game,"bill"): return true
		Architects.advance_core(game,0.1)
		game._update_test_walker(0.1)
	return Architects.present(game,"bill")

# The seabed around the core is not empty: wreckage sits on some of it, and which cells
# are free depends on the run. Try the ring rather than one hard-coded cell.
const RING := [Vector2i(20,21),Vector2i(19,21),Vector2i(21,21),Vector2i(19,19),Vector2i(21,19),
	Vector2i(18,20),Vector2i(22,20),Vector2i(20,18),Vector2i(20,22),Vector2i(18,21),Vector2i(22,21)]
# A paid opening cannot afford a solar array, life support, hydroponics and a drone bay
# at once - it is about two Metal short. A player waits a cycle or two; so does this.
func wait_for(id: String, limit: int) -> bool:
	var cost: Dictionary = game.RoomDatabaseScript.get_room(id).cost
	for frame in range(limit):
		var affordable := true
		for resource in cost:
			if int(game.resources.get(resource,0)) < int(cost[resource]): affordable = false
		if affordable: return true
		step()
	return false

func build_somewhere(id: String, used: Array) -> bool:
	for cell in RING:
		if cell in used or game.occupied.has(cell): continue
		if build(id,cell):
			used.append(cell)
			return true
	return false

func build(id: String, cell: Vector2i) -> bool:
	game.hand.assign([id]) # Controlled available blueprint, not free construction.
	game._on_card_pressed(id)
	var rotation := -1
	for q in range(4):
		game.selected_rotation = q
		if game.get_placement_problem(id,cell).is_empty():
			rotation = q
			break
	if rotation<0: return false
	game._on_grid_clicked(cell)
	for frame in range(1000):
		if game.occupied.has(cell): return true
		step()
	return false
func run() -> void:
	for solar_count in [1,2]:
		game = load("res://scenes/main.tscn").instantiate()
		game.meta.save_path = "user://drone_economy_%d_%d.meta" % [OS.get_process_id(),solar_count]
		game.run_save_path = game.meta.save_path+".loop"
		root.add_child(game)
		current_scene = game
		game._confirm_doctrines()
		game.set_process(false)
		game.tick_timer.stop()
		game.paused = false
		elapsed = 0.0
		cycle_clock = 0.0
		recording = false
		var crewed := wake_architect()
		if not crewed:
			failures += 1
			push_error("No architect woke out of the core pod; nothing can build")
		# The crew member who builds the station also breathes, eats and drinks. Without
		# these the run is not a drone-economy scenario, it is a suffocation scenario: it
		# ended at cycle 12 on "Crew population reached 0." with food, oxygen and water at
		# zero. Both arms carry the same base load, so the difference between them is still
		# exactly one solar array.
		var used: Array = []
		var built := build("solar_array",Vector2i(19,20))
		if not built: push_error("Could not build the first solar_array: %s" % game.get_placement_problem("solar_array",Vector2i(19,20)))
		# Power first, then the rooms that draw it: life support and hydroponics together
		# cost 2 power a cycle, and building them before any array ended the run at cycle 3
		# on "BRINE Core lost power." No condenser - it costs 2 Data the opening does not
		# have - so water is left to the station's own supply.
		if built:
			for id in ["life_support","hydroponics_bay"]:
				if build_somewhere(id,used): continue
				built = false
				push_error("Could not place %s anywhere on the ring (metal %d, power %d, data %d, biomass %d)" % [
					id,int(game.resources.metal),int(game.resources.power),
					int(game.resources.data),int(game.resources.biomass)])
				break
		if built and not wait_for(kind+"_drone_bay",4000):
			built = false
			push_error("Never accumulated enough to buy the %s drone bay (metal %d)" % [kind,int(game.resources.metal)])
		if built and not build(kind+"_drone_bay",Vector2i(20,19)):
			built = false
			push_error("Could not build the %s drone bay at (20,19): %s" % [kind,game.get_placement_problem(kind+"_drone_bay",Vector2i(20,19))])
		if built and solar_count==2 and not build("solar_array",Vector2i(21,20)):
			built = false
			push_error("Could not build the second solar_array at (21,20): %s" % game.get_placement_problem("solar_array",Vector2i(21,20)))
		if not built:
			failures += 1
			push_error("Paid economy fixture could not construct its station")
		delivered = 0
		charging = 0
		work_seconds = 0.0
		travel_seconds = 0.0
		waiting_seconds = 0.0
		recording = true
		ended_reason = ""
		ended_resources = {}
		for frame in range(3000): step()
		rows.append({"solar_rooms":solar_count,"paid_setup":built,"survived":game.running,"observed_seconds":300,"metal_delivered":delivered,"charging_power":charging,"work_seconds":snappedf(work_seconds,0.1),"travel_seconds":snappedf(travel_seconds,0.1),"waiting_for_power_seconds":snappedf(waiting_seconds,0.1),"final_power":game.resources.power,"final_metal":game.resources.metal,"cycle":game.cycle,"free_build":game.testing_free_build,"failures_disabled":game.testing_disable_failures,"ended_reason":ended_reason,"ended_resources":ended_resources})
		if not game.running or game.testing_free_build or game.testing_disable_failures:
			failures += 1
			push_error("Paid drone station must remain viable under normal rules")
		game.free()
		await process_frame
	var file := FileAccess.open("res://output/finite-drone-economy-"+kind+".json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope":"Controlled 300-second normal-economy comparison; not human playtesting or full-game balance", "runs":rows},"\t"))
	print("DRONE ECONOMY %s: %s" % ["PASS" if failures==0 else "FAIL",JSON.stringify(rows)])
	quit(0 if failures==0 else 1)
