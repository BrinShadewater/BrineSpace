extends RefCounted

static func remedy(status: String) -> String:
	if status == "INTAKE BLOCKED":
		return "Clear the ocean cell indicated by the turbine's intake arrow. Rooms, queued construction, wrecks, rock and finite resource deposits obstruct the intake."
	if status == "NEEDS ACTIVE REACTOR":
		return "Place or resume a Reactor beside this room. Each adjacent functioning Reactor supplies 2 reclaimed Power, up to 4; a shared wall is enough."
	if status == "SUSPENDED":
		return "Resume this room below. It will be evaluated again next cycle."
	if status == "HABITATS FULL":
		return "Add crew capacity before producing more crew."
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
	for room in rooms:
		var reason := str(forecast.offline.get(room.pos,""))
		if reason.is_empty() or reason == "SUSPENDED": continue
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
