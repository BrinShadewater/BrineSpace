extends SceneTree
## Paid opening station with live Architect wake and full frame simulation.
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
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg=="--kind=salvage": kind = "salvage"
	call_deferred("run")
func step() -> void:
	if not game.running: return
	game.paused = false
	if recording:
		for drone in game.drone_fleet.drones.values():
			if drone.kind!=kind: continue
			if drone.phase=="working": work_seconds += 0.1
			elif drone.phase in ["outbound","returning","launching","docking"]: travel_seconds += 0.1
			elif game.resources.power==0 and drone.get("battery",12.0)<11.99: waiting_seconds += 0.1
	game._process(0.1)
	if recording:
		delivered += int(game.drone_fleet.delivered.get("metal",0))
		charging += game.drone_fleet.power_spent
	elapsed += 0.1
	cycle_clock += 0.1
	if cycle_clock>=20.0:
		cycle_clock -= 20.0
		game._advance_cycle()
func build(id: String, cell: Vector2i) -> bool:
	game.hand.assign([id]) # Controlled available blueprint, not free construction.
	game._on_card_pressed(id)
	var rotation := -1
	for retry in range(1200):
		for q in range(4):
			game.selected_rotation = q
			if game.get_placement_problem(id,cell).is_empty():
				rotation = q
				break
		if rotation >= 0: break
		step()
	if rotation<0:
		push_error("Cannot stage %s: %s" % [id,game.get_placement_problem(id,cell)])
		return false
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
		game.meta.selected_architect = "bill"
		game.meta.discovered_synergy_ids.clear()
		game.meta.stabilized_synergy_ids.clear()
		root.add_child(game)
		current_scene = game
		game._confirm_doctrines()
		game.set_process(false)
		game.tick_timer.stop()
		game.paused = false
		elapsed = 0.0
		cycle_clock = 0.0
		recording = false
		var built := build("solar_array",Vector2i(19,20)) and build(kind+"_drone_bay",Vector2i(20,19))
		built = built and build("hydroponics_bay",Vector2i(21,20)) and build("life_support",Vector2i(20,21))
		if solar_count == 2:
			built = built and build("solar_array",Vector2i(19,19))
		if not built:
			failures += 1
			push_error("Paid economy fixture could not construct its station")
		delivered = 0
		charging = 0
		work_seconds = 0.0
		travel_seconds = 0.0
		waiting_seconds = 0.0
		recording = true
		for frame in range(3000): step()
		rows.append({"solar_rooms":solar_count,"paid_setup":built,"survived":game.running,"observed_seconds":300,"metal_delivered":delivered,"charging_power":charging,"work_seconds":snappedf(work_seconds,0.1),"travel_seconds":snappedf(travel_seconds,0.1),"waiting_for_power_seconds":snappedf(waiting_seconds,0.1),"final_power":game.resources.power,"final_metal":game.resources.metal,"crew_count":game.crew_count,"architect_awake":game.architect_run.core.recovered,"cycle":game.cycle,"free_build":game.testing_free_build,"failures_disabled":game.testing_disable_failures})
		if not game.running or game.testing_free_build or game.testing_disable_failures:
			failures += 1
			push_error("Paid drone station must remain viable under normal rules")
		game.free()
		await process_frame
	var file := FileAccess.open("res://output/paid-opening-full-frame.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope":"One/two-generator paid opening comparison with Architect awake and full frame updates; controlled blueprints, not human playtesting", "runs":rows},"\t"))
	print("PAID OPENING %s: %s" % ["PASS" if failures==0 else "FAIL",JSON.stringify(rows)])
	quit(0 if failures==0 else 1)
