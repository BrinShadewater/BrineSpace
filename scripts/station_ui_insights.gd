extends RefCounted

static func remedy(status: String) -> String:
	if status == "FIRE":
		return "Enable sprinklers and maintain emergency power and stored Water. Production resumes after extinction; weld any hull damage."
	if status == "INTAKE BLOCKED":
		return "Clear the ocean cell indicated by the turbine's intake arrow. Rooms, queued construction, wrecks, rock and finite resource deposits obstruct the intake."
	if status == "NEEDS ACTIVE REACTOR":
		return "Place or resume a Reactor beside this room. Each adjacent functioning Reactor supplies 2 reclaimed Power, up to 4; a shared wall is enough."
	if status == "SUSPENDED":
		return "Resume this room below. It will be evaluated again next cycle."
	if status == "HABITATS FULL":
		return "Add crew capacity before producing more crew."
	if status == "POWER BLACKOUT":
		return "Power demand is higher than generation plus the reserve, so every Power-drawing room is dark. Add generation or suspend consumers; generators recharge the reserve, and rooms restart once it covers demand."
	if status.begins_with("NEEDS "):
		return "Increase " + status.trim_prefix("NEEDS ").to_lower() + " supply or suspend competing consumers. Rooms share the cycle input budget; non-power outputs become available next cycle."
	if status == "AWAITING CYCLE":
		return "Advance a cycle to observe this room. The forecast below uses current supplies."
	return "Room operated last cycle. Keep its inputs supplied. Matching doors enable neighboring synergy patterns."

static func guide(game) -> String:
	var jobs: Array = game.drone_fleet.orders.duplicate()
	for drone in game.drone_fleet.drones.values():
		if not drone.order.is_empty(): jobs.append(drone.order)
	if not jobs.is_empty():
		var job: Dictionary = jobs[0]
		var name: String = game.RoomDatabaseScript.get_room(job.id).display_name
		return "BUILDING " + name + "\n" + ("Close dialogue or resume time to continue assembly." if game.paused else game.drone_fleet.construction_status(job.pos,game.powered_room_cells)) + "\nMaterials are already paid. Select the site for details."
	var has_generation := false
	for room in game.placed_rooms:
		if room.id != "brine_core" and int(room.get("production",{}).get("power",0)) > 0:
			has_generation = true
	if not has_generation:
		return "FIRST: CONNECT POWER\nChoose a power blueprint and match a door to the Core.\nCheck its cost and intake before placing."
	var net: Dictionary = game._project_cycle_delta()
	for key in ["oxygen","power","food","water"]:
		if int(net.get(key,0)) >= 0: continue
		if int(game.resources.get(key,0)) + int(net[key]) * 2 > 0: continue
		var suggestion := "Inspect supply rooms or suspend a competing consumer."
		for id in game.hand:
			var card: Dictionary = game.RoomDatabaseScript.get_room(str(id))
			if int(card.get("production",{}).get(key,0)) > 0 and game._can_afford(card.get("cost",{})):
				suggestion = "Consider " + str(card.display_name) + " in your hand; check its inputs."
				break
		return key.to_upper() + " IS FALLING\n" + suggestion + "\nCurrent rate: %d stored, %+d per cycle." % [game.resources.get(key,0),net[key]]
	for id in game.run_discovered_synergy_ids:
		if game.meta.stabilized_synergy_ids.has(id): continue
		var recipe: Dictionary = game.SynergyManagerScript.get_synergy(str(id))
		return "STABILIZE: " + str(recipe.name) + "\n%d / 3 consecutive functioning cycles.\nKeep both rooms supplied; an interrupted cycle resets progress." % int(game.synergy_stabilization_progress.get(id,0))
	return "EXPAND, THEN OBSERVE\nConnect different rooms through matching doors.\nSupply them and run a cycle to see what works."

static func construction(game) -> Array[String]:
	var lines: Array[String] = []
	var jobs: Array = []
	for drone in game.drone_fleet.drones.values():
		if not drone.order.is_empty(): jobs.append(drone.order)
	jobs.append_array(game.drone_fleet.orders)
	for job in jobs:
		var cell: Vector2i = job.pos
		var status: String = game.drone_fleet.construction_status(cell, game.powered_room_cells)
		for drone in game.drone_fleet.drones.values():
			if not drone.order.is_empty() and drone.order.pos == cell and drone.get("route_wait",false):
				status = "ROUTE BLOCKED / clear an exterior path to this footprint"
		if game.paused: status = "PAUSED / " + status
		lines.append("[url=%d,%d]%s / %s[/url]\n%s\nMaterials already paid.\n" % [cell.x,cell.y,game.RoomDatabaseScript.get_room(job.id).display_name,cell,status])
	if lines.is_empty(): lines.append("No construction orders. The fabrication rig is waiting.")
	return lines

static func priorities(game, forecast: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	var net: Dictionary = game._project_cycle_delta(forecast)
	for key in ["oxygen", "food", "power"]:
		if int(net.get(key,0)) < 0 and int(game.resources.get(key,0))+int(net[key]) <= 0:
			lines.append("[url=resource:%s]%s RESERVE AT RISK[/url] / %d stored, %+d next cycle. Inspect supply and consumers." % [key,key.to_upper(),game.resources.get(key,0),net[key]])
	var demand: Dictionary = game.drone_fleet.charge_demand(game.powered_room_cells,int(game.resources.power))
	if int(demand.waiting) > 0:
		lines.append("[url=resource:power]DRONES WAITING FOR STORED POWER[/url] / %d docked, %d Power needed to refill active bays. Add generation or suspend a competing consumer." % [demand.waiting,demand.power])
	var rooms: Array = game.placed_rooms.duplicate()
	rooms.sort_custom(func(a: Dictionary,b: Dictionary) -> bool: return str(a.pos)<str(b.pos))
	var blackout_rooms := 0
	for room in rooms:
		if str(forecast.offline.get(room.pos,"")) == "POWER BLACKOUT": blackout_rooms += 1
	var blackout_listed := false
	for room in rooms:
		var reason := str(forecast.offline.get(room.pos,""))
		if reason.is_empty() or reason == "SUSPENDED": continue
		if reason == "POWER BLACKOUT":
			# Every powered room carries the same reason: one station-wide entry, not three copies.
			if blackout_listed: continue
			blackout_listed = true
			lines.append("[url=resource:power]STATION BLACKOUT[/url] / %d rooms dark\n%s" % [blackout_rooms,remedy(reason)])
			continue
		lines.append("[url=%d,%d]%s / %s[/url]\n%s" % [room.pos.x,room.pos.y,room.display_name,reason,remedy(reason)])
	return lines.slice(0,3)

static func learning(game) -> Array[String]:
	var lines: Array[String] = []
	var ids: Array = game.meta.discovered_synergy_ids.keys()
	ids.sort_custom(func(a: Variant,b: Variant) -> bool: return int(game.synergy_stabilization_progress.get(a,0))>int(game.synergy_stabilization_progress.get(b,0)) if int(game.synergy_stabilization_progress.get(a,0))!=int(game.synergy_stabilization_progress.get(b,0)) else str(a)<str(b))
	for id in ids:
		if game.meta.stabilized_synergy_ids.has(id): continue
		var connected := false
		for link in game.connected_synergy_links:
			if str(link.get("id","")) == str(id): connected = true
		if not connected: continue
		var data: Dictionary = game.SynergyManagerScript.get_synergy(str(id))
		var progress := int(game.synergy_stabilization_progress.get(id,0))
		lines.append("%s / %d of 3 cycles / %s" % [data.get("name",id),progress,"KEEP BOTH ROOMS FUNCTIONING" if progress>0 else "DORMANT - restore both rooms"])
	return lines

static func power_demand(game) -> String:
	var demand: Dictionary = game.drone_fleet.charge_demand(game.powered_room_cells,int(game.resources.power))
	var message := "DRONE CHARGING // %d Power to refill docked drones; %d stored.\n%d waiting for Power / %d charging / %d bays offline.\n1 Power buys 6 battery seconds. Refills draw between cycles, separately from the room forecast." % [demand.power,game.resources.power,demand.waiting,demand.charging,demand.offline]
	if game.paused: message += "\nTime paused; charging resumes with the station."
	if demand.waiting > 0: message += "\nAdd generation or suspend a competing Power consumer to leave a reserve for drones."
	if demand.offline > 0: message += "\nRestore offline bay inputs or resume suspended bays before charging."
	return message

static func power_balance(game, forecast: Dictionary) -> String:
	var stored := int(game.resources.power)
	var change := int(forecast.delta.get("power",0))
	var flow := "Reserve unchanged"
	if change < 0: flow = "Battery discharge: %d Power" % -change
	elif change > 0: flow = "Battery charge: %d Power" % change
	return "POWER // NEXT CYCLE\nGeneration: %d / Requested: %d / Supplied: %d\n%s / Stored: %d -> %d%s\n%s Battery Arrays add capacity; they do not generate Power. Drone and Marsh charging draw from storage between cycles." % [forecast.generation,game._project_power_demand(),forecast.power_used,flow,stored,stored+change,power_vented_note(int(forecast.get("power_vented",0))),"BLACKOUT AHEAD: generation plus the reserve cannot power every room, so all Power consumers go dark next cycle while generators recharge the reserve." if forecast.get("blackout",false) else "The reserve covers generation shortfalls until it runs dry; then the whole station blacks out."]

# Surplus above the storage cap is discarded; say so rather than showing a silent +0.
static func power_vented_note(vented: int) -> String:
	if vented <= 0: return ""
	return "\nRESERVE FULL // %d Power vented next cycle. Battery Arrays raise the cap; new generation adds nothing until then." % vented

# Placement is allowed, but some cells silently break existing systems: a room on a
# turbine's intake stops its generation, and a room can wall an extraction bay off
# from every deposit it could reach. Name both before the player pays.
static func placement_hazards(game, room_id: String, cell: Vector2i, rotation: int) -> Array[String]:
	var hazards: Array[String] = []
	for room in game.placed_rooms:
		if room.id == "current_turbine" and game._turbine_intake_cell(room) == cell:
			hazards.append("WARNING // BLOCKS CURRENT TURBINE INTAKE AT %s: it stops generating Power" % room.pos)
	var fleet = game.drone_fleet
	if fleet.drones.is_empty() or fleet.sites.is_empty(): return hazards
	var Routes := preload("res://scripts/drone_routes.gd")
	var Rooms := preload("res://scripts/room_database.gd")
	var before: Dictionary = fleet.route_blockers.duplicate()
	var after: Dictionary = before.duplicate()
	# Judge the finished room: its matching ports stay passable as a service route.
	var doors: Array = []
	for side in Rooms.get_layout(Rooms.get_room(room_id).get("layout","cross")).get("doors",[]):
		doors.append(Routes.STEPS[(["north","east","south","west"].find(side)+rotation)%4])
	after[cell] = {"doors":doors}
	for home in fleet.drones:
		var drone: Dictionary = fleet.drones[home]
		if not drone.kind in ["mining","salvage"] or not game.occupied.has(home): continue
		var reachable_before := false
		var reachable_after := false
		for site_cell in fleet.sites:
			var site: Dictionary = fleet.sites[site_cell]
			if site.kind != drone.kind or not site.discovered or not site.active or site.units <= 0: continue
			if Routes.find_path(home,site_cell,before).is_empty(): continue
			reachable_before = true
			if site_cell != cell and not Routes.find_path(home,site_cell,after).is_empty():
				reachable_after = true
				break
		if reachable_before and not reachable_after:
			hazards.append("WARNING // CUTS %s DRONE BAY AT %s OFF FROM EVERY %s" % [drone.kind.to_upper(),home,"DEPOSIT" if drone.kind == "mining" else "SCRAP PILE"])
	return hazards

static func turbine_intake(game, room: Dictionary) -> String:
	var names := ["NORTH","EAST","SOUTH","WEST"]
	var reason: String = game._turbine_intake_problem(room)
	var line := "INTAKE %s %s: %s" % [names[posmod(int(room.get("rotation",0)),4)],game._turbine_intake_cell(room),"CLEAR / 4 Power per functioning cycle" if reason.is_empty() else "BLOCKED BY " + reason + " / NO POWER"]
	if reason.is_empty(): line += power_vented_note(int(game.forecast_power_vented))
	return line
