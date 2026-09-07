extends RefCounted

static func remedy(status: String) -> String:
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
	if game.placed_rooms.size() <= 1:
		var pending: int = game.drone_fleet.orders.size()
		for drone in game.drone_fleet.drones.values():
			if not drone.order.is_empty(): pending += 1
		if pending > 0:
			return "1 / 4 — CONSTRUCTION QUEUED\nYour purchase reserved a footprint. Resume time to let the fabrication drone assemble it. Rooms produce nothing until construction finishes."
		return "1 / 4 — BUILD\nSelect a blueprint, then place it beside the core. Rotate its doors to match a neighbor. Purchases use the resources shown on the card."
	if game.connected_synergy_links.is_empty() and game.run_discovered_synergy_ids.is_empty():
		return "2 / 4 — CONNECT\nTry different neighboring room types with matching doors. Select a built room to inspect its supplies and highlight its connections."
	if game.run_discovered_synergy_ids.is_empty() and game.meta.discovered_synergy_ids.is_empty():
		return "3 / 4 — KEEP IT FUNCTIONING\nLet connected rooms operate for a cycle. Inspect any room marked NEEDS; both partners must function to teach a pattern."
	return "4 / 4 — STABILIZE\nKeep a discovered pattern functioning for three consecutive cycles. The Codex records what you learn; stabilized rewards survive a reboot."

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
