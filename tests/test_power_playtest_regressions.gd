extends SceneTree
const Rooms = preload("res://scripts/room_database.gd")
const Insights = preload("res://scripts/station_ui_insights.gd")
class Game extends "res://scripts/main.gd":
	func _refresh_all() -> void: pass
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func add(game, id: String, cell: Vector2i) -> Dictionary:
	var room := Rooms.get_room(id)
	room.pos = cell
	room.rotation = 0
	game.placed_rooms.append(room)
	game.occupied[cell] = room
	return room
func _init() -> void:
	var game = Game.new()
	var core := add(game,"brine_core",Vector2i(20,20))
	game.resources.power = 2
	var forecast: Dictionary = game._simulate_room_economy()
	check(forecast.generation == 0 and forecast.power_used == 1 and forecast.delta.power == -1,"Reserve alone supplies the core")
	check(Insights.power_balance(game,forecast).contains("Battery discharge: 1 Power"),"Feedback explains reserve discharge")
	game._apply_room_economy()
	check(game.resources.power == 1 and game.powered_room_cells.has(core.pos),"First battery cycle commits its debit")
	game._apply_room_economy()
	check(game.resources.power == 0 and game.powered_room_cells.has(core.pos),"Last reserve unit still buys a full cycle")
	game._apply_room_economy()
	check(game.unpowered_room_cells.has(core.pos),"Core loses power only on the subsequent unpaid cycle")
	add(game,"solar_array",Vector2i(21,20))
	game._apply_room_economy()
	check(game.resources.power == 2 and game.powered_room_cells.has(core.pos),"Generation restores operation and charges surplus")
	game.hardware.power = false
	game._apply_room_economy()
	check(game.resources.power == 2 and game.powered_room_cells.is_empty(),"Master off retains stored energy")
	game.free()
	game = Game.new()
	var bay := add(game,"mining_drone_bay",Vector2i(20,20))
	game.resources.power = 1
	game._apply_room_economy()
	var drone: Dictionary = game.drone_fleet.drones[bay.pos]
	drone.battery = 0.0
	drone.charge_credit = 6.0
	game.running = true
	game.paused = false
	check(game.powered_room_cells.has(bay.pos) and not game._simulate_room_economy().working_cells.has(bay.pos),"Reproduce paid bay with insufficient next-cycle power")
	game._update_wreck_clearance(0.25)
	check(drone.battery > 0.0,"Paid bay continues previously paid charging despite empty reserve")
	check(game.resources.power == 0,"Previously paid charging does not spend reserve twice")
	var fire_room := add(game,"reactor",Vector2i(21,20))
	fire_room.fire=0.5
	preload("res://scripts/room_fire.gd").refresh_operation(game)
	check(game.powered_room_cells.has(bay.pos),"An unrelated fire preserves the already paid bay")
	check(game.offline_reasons.get(fire_room.pos)=="FIRE","Burning machinery immediately goes offline")
	fire_room.fire=0.0
	fire_room.suspended=true
	preload("res://scripts/room_fire.gd").refresh_operation(game)
	check(game.powered_room_cells.has(bay.pos),"Extinguishing another room preserves the already paid bay")
	check(game.offline_reasons.get(fire_room.pos)=="SUSPENDED","Extinguished machinery still respects suspension")
	var charge: float = drone.battery
	game.paused = true
	game._update_wreck_clearance(0.25)
	check(drone.battery == charge,"Pause holds paid charging")
	game.paused = false
	game.hardware.power = false
	game._update_wreck_clearance(0.25)
	check(drone.battery == charge,"Master off holds paid charging")
	game.hardware.power = true
	game._apply_room_economy()
	game._update_wreck_clearance(0.25)
	check(drone.battery == charge,"Next unpaid cycle disables the bay")
	game.free()
	game = Game.new()
	game.meta.unlocked_room_ids.clear()
	for id in Rooms.STARTING_UNLOCKS: game.meta.unlocked_room_ids[id] = true
	game._build_run_deck()
	game._draw_hand()
	check(game.selected_card_id.is_empty() and game.hand.size() == 3,"New opening hand requires explicit blueprint selection")
	game.free()
	# A full reserve discards surplus generation; feedback must name it instead of a silent +0.
	game = Game.new()
	add(game,"brine_core",Vector2i(20,20))
	var turbine := add(game,"current_turbine",Vector2i(19,20))
	turbine.rotation = 3
	game.resources.power = 5
	forecast = game._simulate_room_economy()
	check(forecast.power_vented == 0 and not Insights.power_balance(game,forecast).contains("RESERVE FULL"),"Charging below the cap vents nothing")
	game.resources.power = game._get_power_capacity()
	forecast = game._simulate_room_economy()
	check(forecast.generation == 4 and forecast.delta.power == 0 and forecast.power_vented == 3,"West turbine surplus above a full reserve is vented")
	check(Insights.power_balance(game,forecast).contains("RESERVE FULL // 3 Power vented"),"Power panel names vented surplus")
	game.forecast_power_vented = forecast.power_vented
	check(Insights.turbine_intake(game,turbine).contains("INTAKE WEST") and Insights.turbine_intake(game,turbine).contains("RESERVE FULL"),"Clear turbine status explains why it adds nothing")
	check(Insights.placement_hazards(game,"corridor",Vector2i(18,20),0).any(func(h): return h.contains("BLOCKS CURRENT TURBINE INTAKE")),"Placing on a turbine intake warns")
	check(Insights.placement_hazards(game,"corridor",Vector2i(18,21),0).is_empty(),"A neighbouring cell does not warn about the intake")
	game.free()
	# A deposit reachable only through one approach cell: walling it off must warn.
	game = Game.new()
	add(game,"brine_core",Vector2i(18,20))
	add(game,"mining_drone_bay",Vector2i(22,20))
	for cell in [Vector2i(25,20),Vector2i(24,19),Vector2i(24,21)]:
		game.wrecks[cell] = {"kind":"basalt","progress":0.0,"active":false,"cleared":false}
	var deposit := preload("res://scripts/harvest_sites.gd").make_site("mining")
	deposit.discovered = true
	game.drone_fleet.sites = {Vector2i(24,20): deposit}
	game.drone_fleet.sites_initialized = true
	game.drone_fleet.advance(0.0,game.placed_rooms,{},game.wrecks)
	check(Insights.placement_hazards(game,"corridor",Vector2i(23,20),1).any(func(h): return h.contains("CUTS MINING DRONE BAY")),"Sealing a bay's only route to its deposit warns")
	# The bay launches north/south, so the route turns at (23,20); a corner with north/east ports carries it.
	check(not Insights.placement_hazards(game,"corner",Vector2i(23,20),2).any(func(h): return h.contains("CUTS")),"Matching service ports keep the drone route open")
	check(Insights.placement_hazards(game,"corridor",Vector2i(22,22),1).is_empty(),"An unrelated placement does not warn")
	game.free()
	print("POWER PLAYTEST REGRESSIONS: %s" % ("PASS" if failures == 0 else "%d failures" % failures))
	quit(0 if failures == 0 else 1)
