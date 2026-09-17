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
		check(intake == turbine.pos + [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][q],"Intake independently matches clockwise arrow direction")
		add(game,"corridor",intake)
		check(game._turbine_intake_problem(turbine)=="ROOM","Feedback names blocking room")
		check(game._simulate_room_economy().generation==0,"Occupied intake blocks at rotation %d" % q)
		game.occupied.erase(intake)
		game.placed_rooms.pop_back()
		game.wrecks[intake] = {"cleared":false}
		check(game._turbine_intake_problem(turbine)=="WRECK","Feedback names blocking wreck")
		check(game._simulate_room_economy().offline.get(turbine.pos)=="INTAKE BLOCKED","Uncleared site blocks intake")
		game.wrecks[intake].cleared = true
		check(game._simulate_room_economy().generation==4,"Cleared site restores intake")
		game.drone_fleet.sites[intake] = preload("res://scripts/harvest_sites.gd").make_site("mining")
		check(game._turbine_intake_problem(turbine)=="RESOURCE DEPOSIT","Feedback names blocking deposit")
		check(game._simulate_room_economy().generation==0,"Finite deposit blocks intake")
		game.drone_fleet.sites[intake].units = 0
		check(game._simulate_room_economy().generation==4,"Depleted deposit restores intake")
		game.drone_fleet.enqueue("corridor",intake,0)
		check(game._turbine_intake_problem(turbine)=="QUEUED CONSTRUCTION","Feedback names blocking construction")
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
	# Owner direction (Sept 15): a Power cost never blocks building, lights flicker at a quarter of
	# capacity or less, and a reserve that cannot power every room blacks the whole station out.
	game = fresh()
	game.resources.metal = 20
	check(game._can_afford({"metal":6,"power":3}) and game._missing_cost({"metal":6,"power":3}).is_empty(),"A Power cost never blocks building")
	check(not game._can_afford({"metal":30,"power":1}) and game._missing_cost({"metal":30,"power":1})=={"metal":10},"Other costs still block")
	var Lighting = preload("res://rooms/whole-room/room_lighting.gd")
	check(not Lighting.low_power(4,12) and Lighting.low_power(3,12) and Lighting.low_power(1,12) and not Lighting.low_power(0,12),"Lights warn at a quarter of capacity or less, before the blackout")
	var dark_samples := 0
	var dip_starts: Array = []
	var was_lit := true
	var deepest := 1.0
	# Sample 60 seconds at 60 fps: the stutter must be visible but never a strobe. Lights brown
	# out rather than switching fully off (owner playtest, Sept 16).
	for frame in range(3600):
		var level: float = Lighting.power_flicker(Vector2i(3,4),1,12,frame/60.0)
		deepest = minf(deepest, level)
		var lit: bool = level >= 1.0
		if not lit: dark_samples += 1
		if was_lit and not lit: dip_starts.append(frame)
		was_lit = lit
	check(dark_samples>0 and dark_samples<1800,"A nearly empty reserve dims part of the time: %d of 3600 frames" % dark_samples)
	check(deepest < 0.5 and deepest > 0.0,"Dips brown out deeply without going fully black: lowest %.2f" % deepest)
	var worst := 0
	for i in range(dip_starts.size()):
		var within := 0
		for j in range(i, dip_starts.size()):
			if dip_starts[j] - dip_starts[i] < 60: within += 1
		worst = maxi(worst, within)
	check(worst<=3,"No room dips more than three times in any second: worst %d" % worst)
	var other_room_differs := false
	for frame in range(600):
		if Lighting.power_flicker(Vector2i(3,4),1,12,frame/60.0) != Lighting.power_flicker(Vector2i(9,2),1,12,frame/60.0): other_room_differs = true
	check(other_room_differs,"Rooms flicker on their own timing")
	check(Lighting.power_flicker(Vector2i(3,4),6,12,1.0)==1.0 and Lighting.power_flicker(Vector2i(3,4),2,12,1.0,true)==0.6,"Healthy reserves stay lit; reduced motion dims instead of flickering")
	var steady_dark := 0
	for frame in range(600):
		if Lighting.power_flicker(Vector2i(3,4),1,12,frame/60.0,false,true)<1.0: steady_dark += 1
	check(steady_dark==0,"A paused station holds its lights steady")
	add(game,"current_turbine",Vector2i(10,10))
	var consumers: Array = []
	for x in range(5): consumers.append(add(game,"cold_store",Vector2i(12+x,12)))
	var lounge := add(game,"observation_room",Vector2i(12,14))
	game.resources.power = 0
	result = game._simulate_room_economy()
	var dark := 0
	for store in consumers:
		if result.offline.get(store.pos,"")=="POWER BLACKOUT" and not result.working_cells.has(store.pos): dark += 1
	check(result.blackout and dark==5,"Generation 4 cannot power 5 rooms: every powered room blacks out, not just one (%d dark)" % dark)
	check(result.delta.power==4 and result.working_cells.has(Vector2i(10,10)),"Generators keep running and recharge the reserve during a blackout")
	check(result.working_cells.has(lounge.pos),"Rooms that draw no Power keep working")
	game.resources.power = 4
	result = game._simulate_room_economy()
	check(not result.blackout and result.working_cells.size()==7 and result.delta.power==-1,"A recharged reserve restarts every room, draining 1 a cycle")
	game.free()
	# A blackout darkens BRINE's core but only ends the run when the reserve cannot cover the core alone.
	game = fresh()
	var core := add(game,"brine_core",Vector2i(20,20))
	var turbine := add(game,"current_turbine",Vector2i(10,10))
	for x in range(5): add(game,"cold_store",Vector2i(12+x,12))
	result = game._simulate_room_economy()
	check(result.blackout and result.offline.get(core.pos,"")=="POWER BLACKOUT","The core goes dark with the station")
	check(not result.power_failures.has("BRINE Core"),"A blackout the generators can recharge does not count as losing the core")
	game.occupied.erase(turbine.pos)
	game.placed_rooms.erase(turbine)
	result = game._simulate_room_economy()
	check(result.blackout and result.power_failures.has("BRINE Core"),"No generation and no reserve still loses the core")
	game.free()
	# A Clone Lab with full habitats draws nothing, so it must not black the station out.
	game = fresh()
	add(game,"brine_core",Vector2i(20,20))
	add(game,"current_turbine",Vector2i(10,10))
	for x in range(3): add(game,"cold_store",Vector2i(12+x,12))
	var lab := add(game,"clone_lab",Vector2i(12,14))
	game.resources.biomass = 1
	game.resources.data = 1
	game.crew_count = game._get_crew_capacity()
	result = game._simulate_room_economy()
	check(not result.blackout and result.offline.get(lab.pos,"")=="HABITATS FULL" and result.power_failures.is_empty(),"A full-habitat Clone Lab does not trigger a blackout: %s" % str(result.offline))
	game.crew_count = 0
	result = game._simulate_room_economy()
	check(result.blackout,"A Clone Lab that would run and cannot be powered does black out the station")
	game.free()
	# Exterior lamps and their beams follow the same rule: dark in a blackout, flickering when low.
	game = fresh()
	var Hardware = preload("res://scripts/station_hardware.gd")
	var store := add(game,"cold_store",Vector2i(12,12))
	game.powered_room_cells[store.pos] = true
	game.power_capacity = 12
	game.resources.power = 12
	check(Hardware.exterior_light_level(game,store)==1.0,"A healthy reserve keeps exterior lamps lit")
	game.power_blackout = true
	check(Hardware.exterior_light_level(game,store)==0.0,"A blackout turns exterior lamps off")
	game.power_blackout = false
	game.resources.power = 1
	var lamp_off := 0
	for frame in range(1200):
		game.unscaled_time_seconds = frame/60.0
		if Hardware.exterior_light_level(game,store)<1.0: lamp_off += 1
	check(lamp_off>0 and lamp_off<1200,"A low reserve flickers exterior lamps: %d of 1200 frames dimmed" % lamp_off)
	game.paused = true
	var lamp_off_paused := 0
	for frame in range(600):
		game.unscaled_time_seconds = frame/60.0
		if Hardware.exterior_light_level(game,store)<1.0: lamp_off_paused += 1
	check(lamp_off_paused==0,"A paused station holds exterior lamps steady")
	game.paused = false
	game.free()
	print("POWER EXPANSION: %s" % ("PASS" if failures==0 else "%d failures" % failures))
	quit(0 if failures==0 else 1)
