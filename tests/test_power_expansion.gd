extends SceneTree
const Main = preload("res://scripts/main.gd")
const Rooms = preload("res://scripts/room_database.gd")
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func add(game, id: String, cell: Vector2i, q := 0) -> Dictionary:
	var room := Rooms.get_room(id)
	room.pos = cell
	room.rotation = q
	game.placed_rooms.append(room)
	game.occupied[cell] = room
	return room
func fresh():
	var game = Main.new()
	game.resources.power = 0
	game.resources.biomass = 0
	game.meta.save_path = "user://power_expansion_test.meta"
	return game
func _init() -> void:
	for q in range(4):
		var game = fresh()
		var turbine := add(game,"current_turbine",Vector2i(10,10),q)
		check(game._simulate_room_economy().generation==4,"Clear intake produces at rotation %d" % q)
		var intake: Vector2i = game._turbine_intake_cell(turbine)
		add(game,"corridor",intake)
		check(game._simulate_room_economy().generation==0,"Occupied intake blocks at rotation %d" % q)
		game.occupied.erase(intake)
		game.placed_rooms.pop_back()
		game.wrecks[intake] = {"cleared":false}
		check(game._simulate_room_economy().offline.get(turbine.pos)=="INTAKE BLOCKED","Uncleared site blocks intake")
		game.wrecks[intake].cleared = true
		check(game._simulate_room_economy().generation==4,"Cleared site restores intake")
		game.drone_fleet.sites[intake] = preload("res://scripts/harvest_sites.gd").make_site("mining")
		check(game._simulate_room_economy().generation==0,"Finite deposit blocks intake")
		game.drone_fleet.sites[intake].units = 0
		check(game._simulate_room_economy().generation==4,"Depleted deposit restores intake")
		game.drone_fleet.enqueue("corridor",intake,0)
		check(game._simulate_room_economy().generation==0,"Paid queue reserves and blocks intake")
		game.drone_fleet.orders.clear()
		turbine.suspended = true
		check(game._simulate_room_economy().generation==0,"Suspension stops turbine")
		game.free()
	var game = fresh()
	add(game,"current_turbine",Vector2i(0,0))
	check(game._simulate_room_economy().generation==0,"Grid boundary is not open intake water")
	game.free()
	game = fresh()
	var a := add(game,"biomass_digester",Vector2i(10,10))
	var b := add(game,"biomass_digester",Vector2i(11,10))
	check(game._simulate_room_economy().generation==0,"Unfuelled digesters never generate")
	game.resources.biomass = 1
	var result: Dictionary = game._simulate_room_economy()
	check(result.generation==4 and result.delta.biomass==-1,"Two digesters share one stored fuel unit")
	check(result.working_cells.size()==1 and result.offline.size()==1,"Only fuelled digester functions")
	check(game.resources.biomass==1,"Forecast does not mutate fuel")
	a.suspended = true
	check(game._simulate_room_economy().working_cells.has(b.pos),"Suspension releases fuel to peer")
	game.free()
	game = fresh()
	add(game,"hydroponics_bay",Vector2i(10,10))
	add(game,"biomass_digester",Vector2i(11,10))
	game.resources.power = 1
	result = game._simulate_room_economy()
	check(result.generation==0 and result.delta.biomass==1,"Fresh growth cannot fuel same-cycle generation")
	game.free()
	game = fresh()
	var heat := add(game,"heat_recovery",Vector2i(10,10))
	check(game._primary_output_line(heat).contains("Power"),"Recovery card identifies conditional power")
	check(game._simulate_room_economy().offline.get(heat.pos)=="NEEDS ACTIVE REACTOR","Recovery explains missing source")
	var reactor := add(game,"reactor",Vector2i(11,10))
	check(game._simulate_room_economy().generation==8,"One reactor supplies two reclaimed power")
	check(" ".join(game._resource_contribution_lines("power",game._simulate_room_economy())).contains("+2 Power"),"Resource inspector includes conditional recovery")
	add(game,"reactor",Vector2i(9,10))
	add(game,"reactor",Vector2i(10,9))
	check(game._simulate_room_economy().generation==22,"Recovery caps at four power")
	reactor.suspended = true
	check(game._simulate_room_economy().generation==16,"Suspended reactor supplies no direct or reclaimed output")
	heat.isolated = true
	check(game._simulate_room_economy().generation==12,"Isolation stops recovery")
	game.free()
	game = fresh()
	game.meta.unlocked_room_ids.clear()
	for id in Rooms.STARTING_UNLOCKS: game.meta.unlocked_room_ids[id] = true
	for seed_value in range(100):
		game.rng.seed = seed_value
		game._build_run_deck()
		game._draw_hand()
		check(game.hand==["solar_array","mining_drone_bay","hydroponics_bay"],"Opening essentials remain available")
		check(game.draw_pile.back()=="current_turbine","Affordable second generator is next")
		check(not game.draw_pile.has("biomass_digester") and not game.draw_pile.has("heat_recovery"),"Discovery locks remain hidden")
	game.free()
	print("POWER EXPANSION: %s" % ("PASS" if failures==0 else "%d failures" % failures))
	quit(0 if failures==0 else 1)
