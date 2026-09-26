extends RefCounted
## Simulation coordinates are grid cells. Rendering never advances jobs or rewards.
const BAY_KINDS := {"mining_drone_bay":"mining", "salvage_drone_bay":"salvage", "construction_drone_bay":"construction"}
const PHASE_SECONDS := {"launching":1.2, "working":6.0, "docking":1.2, "docked":2.0}
const BATTERY_CAPACITY := 12.0 # Seconds of active extraction; propulsion has a separate return reserve.
const CHARGE_PER_POWER := 6.0
const CHARGE_RATE := 3.0
const CHARGE_POWER_RESERVE := 3
const Sites = preload("res://scripts/harvest_sites.gd")
const Routes = preload("res://scripts/drone_routes.gd")
var sites: Dictionary = {}
var sites_initialized := false
var route_blockers: Dictionary = {}
var power_spent := 0
var drones: Dictionary = {}
var orders: Array = []
var clearance_seconds: Dictionary = {}
var delivered: Dictionary = {}
# Drone perks from Meta Progression, set by the station each frame (the fleet has no profile).
var battery_drain_rate := 1.0
var travel_rate := 1.0
var build_rate := 1.0

func synchronize(rooms: Array) -> void:
	var homes := {}
	for room in rooms:
		if not BAY_KINDS.has(room.id) and room.id != "brine_core": continue
		var home: Vector2i = room.pos
		homes[home] = true
		if not drones.has(home):
			drones[home] = {"kind":BAY_KINDS.get(room.id,"construction"), "bootstrap":room.id == "brine_core", "home":home, "target":Vector2(home), "position":Vector2(home), "phase":"docked", "elapsed":0.0, "job":"", "order":{}}
	for home in drones.keys():
		if not homes.has(home):
			if not drones[home].order.is_empty(): orders.push_front(drones[home].order)
			drones.erase(home)

func enqueue(room_id: String, cell: Vector2i, rotation: int) -> void:
	orders.append({"id":room_id, "pos":cell, "rotation":rotation})

func deployed(home: Vector2i) -> bool:
	return drones.has(home) and drones[home].phase != "docked"

func hatch_fraction(home: Vector2i) -> float:
	if not drones.has(home): return 0.0
	var drone: Dictionary = drones[home]
	if drone.phase == "launching": return clampf(drone.elapsed/0.35,0,1)
	if drone.phase == "docking": return 1.0-clampf((drone.elapsed-0.85)/0.35,0,1)
	return 0.0

func advance(delta: float, rooms: Array, powered: Dictionary, wrecks: Dictionary, station_power: int = 100000, crew_builders := false) -> Array:
	synchronize(rooms)
	if not sites_initialized:
		sites = Sites.seed_sites(rooms,wrecks)
		for cell in sites.keys():
			if reserved(cell): sites.erase(cell) # Migration must not obstruct paid queued construction.
		sites_initialized = true
	Sites.discover(sites,rooms)
	# Drones travel beneath the station (owner playtest: a bay without a matching door sealed its
	# drone outside), so rooms never block a route; they already draw below every floor. Rock,
	# wrecks, deposits and queued construction still do.
	route_blockers = {}
	for cell in wrecks:
		if preload("res://scripts/wreck_field.gd").blocks(wrecks,cell): route_blockers[cell] = true
	for cell in sites:
		if Sites.blocks(sites,cell): route_blockers[cell] = true
	for order in orders: route_blockers[order.pos] = true
	for worker in drones.values():
		if not worker.order.is_empty(): route_blockers[worker.order.pos] = true
	clearance_seconds.clear()
	delivered.clear()
	power_spent = 0
	var completed: Array = []
	var suspended := {}
	for room in rooms:
		if room.get("suspended",false): suspended[room.pos]=true
	for home in drones:
		var drone: Dictionary = drones[home]
		if crew_builders and drone.bootstrap:
			# Migrate an old emergency-drone job without losing its paid order or work.
			if not drone.order.is_empty():
				if drone.phase=="working": drone.order["work"]=minf(10.0,float(drone.elapsed))
				orders.push_front(drone.order)
				drone.order={}
			drone.phase="docked"
			drone.job=""
			drone.elapsed=0.0
			continue
		# Core's emergency builder prevents power/build bootstrap deadlock.
		var extractor: bool = drone.kind in ["mining","salvage"]
		if extractor and not drone.has("battery"): drone["battery"] = BATTERY_CAPACITY
		if not drone.bootstrap and not powered.has(home) and not extractor: continue
		if drone.job == "harvest" and drone.phase not in ["returning","docking"]:
			var target_cell := Vector2i(drone.target)
			var site: Dictionary = sites.get(target_cell,{})
			var obstructed: bool = site.is_empty() or not site.get("active",false) or int(site.get("units",0))<=0 or reserved(target_cell) or preload("res://scripts/wreck_field.gd").blocks(wrecks,target_cell)
			for room in rooms:
				if room.pos == target_cell: obstructed = true
			if obstructed:
				drone["return_from"] = drone.position
				drone.phase = "returning"
				drone.elapsed = 0.0
		if drone.job == "clear" and drone.phase not in ["returning","docking"]:
			var wreck: Dictionary = wrecks.get(Vector2i(drone.target),{})
			if wreck.is_empty() or not wreck.active or wreck.cleared:
				drone["return_from"] = drone.position
				drone.phase = "returning"
				drone.elapsed = 0.0
		var remaining := maxf(delta,0.0)
		while remaining > 0.00001:
			if extractor and drone.phase == "docked" and suspended.has(home): break
			if drone.phase in ["outbound","returning"]:
				var goal: Vector2i = drone.home if drone.phase == "returning" else Vector2i(drone.target)
				remaining = Routes.travel(drone,remaining*travel_rate,goal,route_blockers)/travel_rate
				if drone.get("route_wait",false) or not Vector2(drone.position).is_equal_approx(Vector2(goal)): break
				drone.phase = "docking" if drone.phase == "returning" else "working"
				drone.elapsed = 0.0
				if drone.phase=="working" and drone.job=="construct": drone.elapsed=float(drone.order.get("work",0.0))*(1.0 if drone.bootstrap else .6)
				drone.erase("route")
				continue
			if extractor and drone.phase == "docked" and drone.battery < BATTERY_CAPACITY-0.00001:
				if float(drone.get("charge_credit",0.0)) <= 0.00001:
					if station_power-power_spent <= CHARGE_POWER_RESERVE: break
					power_spent += 1
					drone["charge_credit"] = CHARGE_PER_POWER
				var charge := minf(minf(remaining*CHARGE_RATE,BATTERY_CAPACITY-drone.battery),drone.charge_credit)
				drone.battery += charge
				if drone.battery>BATTERY_CAPACITY-0.00001: drone.battery = BATTERY_CAPACITY
				drone.charge_credit -= charge
				remaining -= charge/CHARGE_RATE
				continue
			# Charging draws stored energy independently of the bay's cycle inputs.
			# Launching a new job still requires an operational bay.
			if extractor and drone.phase == "docked" and not powered.has(home): break
			if drone.phase == "docked" and drone.job.is_empty():
				if float(drone.get("idle_retry",0.0))>0:
					var retry_step := minf(remaining,drone.idle_retry)
					drone.idle_retry -= retry_step
					remaining -= retry_step
					if drone.idle_retry>0.0: break
					continue
				if drone.bootstrap and _dedicated_builder_ready(powered): break
				_assign(drone,wrecks,rooms,powered)
				if drone.job.is_empty():
					drone["idle_retry"] = 1.0
					break
			var duration: float = PHASE_SECONDS.get(drone.phase, maxf(0.5,Vector2(home).distance_to(drone.target)/1.5))
			if drone.phase == "working" and drone.job == "clear":
				duration = maxf(0.0001,18.0-float(wrecks[Vector2i(drone.target)].progress)-float(clearance_seconds.get(Vector2i(drone.target),0.0)))
				drone.elapsed = 0.0
			elif drone.phase == "working" and drone.job == "harvest":
				duration = maxf(0.00001,Sites.WORK_SECONDS-float(sites[Vector2i(drone.target)].progress))
				drone.elapsed = 0.0
			elif drone.phase == "working" and drone.bootstrap: duration = 10.0/build_rate
			elif drone.phase == "working" and drone.job == "construct": duration /= build_rate
			var step := minf(remaining,maxf(0.0,duration-float(drone.elapsed)))
			if extractor and drone.phase == "working":
				step = minf(step,drone.battery/battery_drain_rate)
				drone.battery = maxf(0.0,drone.battery-step*battery_drain_rate)
			if drone.phase == "working" and drone.job == "clear":
				var target_cell := Vector2i(drone.target)
				clearance_seconds[target_cell] = float(clearance_seconds.get(target_cell,0.0))+step
			if drone.phase == "working" and drone.job == "harvest":
				sites[Vector2i(drone.target)].progress += step
			drone.elapsed += step
			drone["clock"] = float(drone.get("clock",0.0))+step
			remaining -= step
			if drone.elapsed < duration:
				if extractor and drone.phase == "working" and drone.battery <= 0.00001:
					drone["return_from"] = drone.position
					drone.phase = "returning"
					drone.elapsed = 0.0
					continue
				break
			drone.elapsed = 0.0
			match drone.phase:
				"docked": drone.phase = "launching"
				"launching": drone.phase = "outbound"
				"outbound": drone.phase = "working"
				"working":
					if drone.job == "clear":
						drone["cargo"] = {"metal":preload("res://scripts/wreck_field.gd").YIELDS[wrecks[Vector2i(drone.target)].kind]}
					if drone.job == "harvest":
						var site: Dictionary = sites[Vector2i(drone.target)]
						site.units -= 1
						site.progress = 0.0
						drone["cargo"] = Sites.LOADS[site.kind].duplicate()
						for key in drone.get("pending_yield",{}):
							drone.cargo[key] = int(drone.cargo.get(key,0))+int(drone.pending_yield[key])
						drone.erase("pending_yield") # Deliver pre-migration earned credit once.
					if not drone.order.is_empty():
						completed.append(drone.order.duplicate(true))
						drone.order = {}
					drone.phase = "returning"
				"returning": drone.phase = "docking"
				"docking":
					for key in drone.get("cargo",{}): delivered[key] = int(delivered.get(key,0))+int(drone.cargo[key])
					drone["cargo"] = {}
					drone.phase = "docked"
					drone.job = ""
					drone.erase("return_from")
	return completed

func _dedicated_builder_ready(powered: Dictionary) -> bool:
	for drone in drones.values():
		if drone.kind == "construction" and not drone.bootstrap and powered.has(drone.home) and drone.phase == "docked":
			for order in orders:
				if not str(order.get("builder","")).is_empty(): continue
				if not Routes.find_path(drone.home,order.pos,route_blockers).is_empty(): return true
	return false

func _assign(drone: Dictionary, wrecks: Dictionary, rooms: Array, powered: Dictionary = {}) -> void:
	if drone.kind == "construction":
		if orders.is_empty(): return
		var chosen := -1
		for i in range(orders.size()):
			if not str(orders[i].get("builder","")).is_empty(): continue
			var path := Routes.find_path(drone.home,orders[i].pos,route_blockers)
			if path.is_empty(): continue
			# With drones passing under rooms every bay can reach every site: leave an order to a
			# closer free bay rather than sending a far one across the station.
			if not drone.bootstrap and _closer_free_builder(drone,orders[i].pos,path.size(),powered): continue
			chosen = i
			break
		if chosen<0:
			drone["route_wait"] = true
			return
		drone.order = orders.pop_at(chosen)
		drone.target = Vector2(drone.order.pos)
		drone.job = "construct"
		drone["route_wait"] = false
		return
	for cell in wrecks:
		var wreck: Dictionary = wrecks[cell]
		if not wreck.active or wreck.cleared or wreck.kind in ["cryo","charging","river","josh","margot"]: continue
		if float(clearance_seconds.get(cell,0.0)) >= 18.0-float(wreck.progress): continue
		if (wreck.kind == "basalt") != (drone.kind == "mining"): continue
		var claimed := false
		for other in drones.values():
			if other != drone and other.job == "clear" and other.target == Vector2(cell): claimed = true
		if claimed: continue
		if Routes.find_path(drone.home,cell,route_blockers).is_empty(): continue
		drone.target = Vector2(cell)
		drone.job = "clear"
		drone["route_wait"] = false
		return
	var best_length := 10000
	var claimed := {}
	for other in drones.values():
		if other.home != drone.home and other.job == "harvest": claimed[Vector2i(other.target)] = true
	var candidates: Array = sites.keys()
	candidates.sort_custom(func(a,b): return Vector2(a).distance_squared_to(Vector2(drone.home))<Vector2(b).distance_squared_to(Vector2(drone.home)))
	for cell in candidates:
		var site: Dictionary = sites[cell]
		if site.kind!=drone.kind or not site.discovered or not site.active or site.units<=0 or claimed.has(cell) or reserved(cell): continue
		var occupied := false
		for room in rooms:
			if room.pos == cell: occupied = true
		if occupied: continue
		var path := Routes.find_path(drone.home,cell,route_blockers)
		if path.is_empty() or path.size()>=best_length: continue
		best_length = path.size()
		drone.target = Vector2(cell)
		drone.job = "harvest"
	drone["route_wait"] = drone.job.is_empty()

func _closer_free_builder(drone: Dictionary, cell: Vector2i, length: int, powered: Dictionary) -> bool:
	for other in drones.values():
		if other == drone or other.kind != "construction" or other.bootstrap or other.phase != "docked" or not other.job.is_empty(): continue
		if not powered.has(other.home): continue
		var other_path := Routes.find_path(other.home,cell,route_blockers)
		if not other_path.is_empty() and (other_path.size() < length or (other_path.size() == length and Vector2(other.home) < Vector2(drone.home))): return true
	return false

func reserved(cell: Vector2i) -> bool:
	for order in orders:
		if order.pos == cell: return true
	for drone in drones.values():
		if not drone.order.is_empty() and drone.order.pos == cell: return true
	return false

func order_at(cell: Vector2i) -> Dictionary:
	for order in orders:
		if order.pos == cell: return order
	for drone in drones.values():
		if not drone.order.is_empty() and drone.order.pos == cell: return drone.order
	return {}

func construction_status(cell: Vector2i, powered: Dictionary) -> String:
	for order in orders:
		if order.pos==cell and not str(order.get("builder","")).is_empty():
			return "%s / ASSEMBLING %d%%" % [preload("res://scripts/architects.gd").NAMES[order.builder],roundi(float(order.get("work",0.0))*10)]
	for drone in drones.values():
		if drone.order.is_empty() or drone.order.pos != cell: continue
		if not drone.bootstrap and not powered.has(drone.home): return "BUILDER OFFLINE / awaiting bay power"
		if drone.phase == "working":
			var duration := 10.0 if drone.bootstrap else 6.0
			return "ASSEMBLING / %d%%" % roundi(clampf(drone.elapsed/duration,0,1)*100)
		return "BUILDER " + str(drone.phase).to_upper()
	return "QUEUED / awaiting architect access or a powered builder bay"

func construction_progress(cell: Vector2i) -> float:
	for d in drones.values():
		if not d.order.is_empty() and d.order.pos==cell:
			return clampf(float(d.elapsed)/(10.0 if d.bootstrap else 6.0),0,1) if d.phase=="working" else float(d.order.get("work",0.0))/10.0
	return float(order_at(cell).get("work",0.0))/10.0

func accrue(home: Vector2i, production: Dictionary) -> void:
	# Compatibility for older consumers: deposits now own output, never cycle credits.
	pass

func has_worker(kind: String, rooms: Array) -> bool:
	for room in rooms:
		if BAY_KINDS.get(room.id,"") == kind: return true
	return false

func clearance_status(cell: Vector2i, powered: Dictionary) -> String:
	for drone in drones.values():
		if drone.job != "clear" or Vector2i(drone.target) != cell: continue
		if not powered.has(drone.home) and drone.phase == "docked": return "DRONE OFFLINE / awaiting bay power"
		match drone.phase:
			"docked": return "DRONE ASSIGNED / preparing launch"
			"launching": return "DRONE LAUNCHING"
			"outbound": return "DRONE EN ROUTE"
			"working": return ("DRILLING" if drone.kind == "mining" else "DISMANTLING")+" / BATTERY %d%%" % roundi(float(drone.get("battery",BATTERY_CAPACITY))/BATTERY_CAPACITY*100)
			"returning", "docking": return "RETURNING / cargo delivery and recharge"
	for drone in drones.values():
		if drone.kind in ["mining","salvage"] and drone.phase == "docked" and float(drone.get("battery",BATTERY_CAPACITY)) < BATTERY_CAPACITY:
			return "WAITING / drone battery recharging at bay"
	return "WAITING FOR AVAILABLE DRONE"

func charge_demand(_powered: Dictionary, station_power: int, rooms: Array = []) -> Dictionary:
	var result := {"power":0,"waiting":0,"charging":0,"offline":0}
	var suspended := {}
	for room in rooms:
		if room.get("suspended",false): suspended[room.pos]=true
	for home in drones:
		var d: Dictionary = drones[home]
		if d.kind not in ["mining","salvage"] or d.phase != "docked": continue
		var deficit := BATTERY_CAPACITY-float(d.get("battery",BATTERY_CAPACITY))
		if deficit <= 0.00001: continue
		if suspended.has(home):
			result.offline += 1
			continue
		var credit := float(d.get("charge_credit",0.0))
		result.power += ceili(maxf(0.0,deficit-credit)/CHARGE_PER_POWER)
		if station_power <= CHARGE_POWER_RESERVE and credit <= 0.00001: result.waiting += 1
		else: result.charging += 1
	return result

func battery_status(home: Vector2i, station_power := -1, bay_powered := true, paused := false, wrecks: Dictionary = {}, bay_suspended := false) -> String:
	if not drones.has(home): return "BATTERY / ready"
	var d: Dictionary = drones[home]
	var percent := roundi(float(d.get("battery",BATTERY_CAPACITY))/BATTERY_CAPACITY*100)
	var state := str(d.phase).to_upper()
	if d.phase == "docked" and bay_suspended:
		state = "BAY SUSPENDED / resume the bay to charge"
	elif d.phase == "docked" and float(d.get("battery",BATTERY_CAPACITY)) < BATTERY_CAPACITY-0.00001:
		state = "CHARGING"
		if station_power >= 0 and station_power <= CHARGE_POWER_RESERVE and float(d.get("charge_credit",0.0)) <= 0.00001:
			state = "WAITING FOR STORED POWER / preserving 3 Power; resumes above 3"
	elif d.phase == "docked" and not bay_powered:
		state = "BAY OFFLINE / battery ready; restore room inputs to launch"
	elif d.get("route_wait",false): state = harvest_route_hint(home,wrecks)
	return ("PAUSED / " if paused else "") + "BATTERY %d%% / %s" % [percent,state]

# A stalled extraction bay usually means its last reachable deposit is spent and the
# rest lie behind the rock shelves. Name the first rock or wreck to clear, cheapest
# route first (each obstacle costs one clearance), under the router's port rules.
func harvest_route_hint(home: Vector2i, wrecks: Dictionary) -> String:
	var plan := harvest_route_plan(home,wrecks)
	var noun := "DEPOSIT" if plan.get("kind","mining") == "mining" else "SCRAP PILE"
	match str(plan.state):
		"depleted": return "NO SURVEYED %sS LEFT / build outward to survey new seabed" % noun
		"sealed": return "ROUTE BLOCKED / no clearance reaches a surveyed %s; %s" % [noun.to_lower(),plan.seal]
		"recover":
			var title: String = preload("res://scripts/companions.gd").TITLES.get(wrecks[plan.obstacle].kind,"derelict ward")
			return "NO ROUTE TO A %s / %srecover the %s at %s (8 Metal, from a room with a matching door) toward %s" % [noun,_route_step(plan.steps),title,plan.obstacle,plan.goal]
		"clear":
			var what := "rock" if plan.obstacle_kind == "basalt" else "wreck"
			return "NO ROUTE TO A %s / %sselect the %s at %s to %s it (%s Drone Bay) toward %s" % [noun,_route_step(plan.steps),what,plan.obstacle,"break" if what == "rock" else "dismantle","Mining" if what == "rock" else "Salvage",plan.goal]
	return "ROUTE BLOCKED / check surveyed sites and bay ports"

# Structured form of the stalled-bay advice. state: "depleted" (nothing harvestable
# surveyed), "open" (a route exists), "clear"/"recover" (act on obstacle first,
# steps obstacles in total toward goal) or "sealed" (seal names the nearest blocker).
func harvest_route_plan(home: Vector2i, wrecks: Dictionary) -> Dictionary:
	if not drones.has(home): return {"state":"unknown"}
	var kind: String = drones[home].kind
	var goals: Array = []
	for cell in sites:
		var site: Dictionary = sites[cell]
		if site.kind == kind and site.discovered and site.active and site.units > 0: goals.append(cell)
	if goals.is_empty(): return {"state":"depleted","kind":kind}
	var clearable := {}
	var solid: Dictionary = route_blockers.duplicate()
	var Rooms := preload("res://scripts/room_database.gd")
	for cell in wrecks:
		var wreck: Dictionary = wrecks[cell]
		if wreck.cleared or not solid.has(cell) or solid[cell] is Dictionary: continue
		if wreck.kind in ["cryo","charging","river","josh","margot"]:
			# A paid recovery turns the site into a room; route through its future ports.
			var future: String = preload("res://scripts/companions.gd").ROOMS.get(wreck.kind,"cryo_chamber")
			var turn: int = int(wreck.get("rotation",0)) if wreck.kind in ["cryo","charging"] else 0
			var doors: Array = []
			for side in Rooms.get_layout(Rooms.get_room(future).get("layout","cross")).get("doors",[]):
				doors.append(Routes.STEPS[(["north","east","south","west"].find(side)+turn)%4])
			solid[cell] = {"doors":doors}
			clearable[cell] = "recover"
			continue
		clearable[cell] = wreck.kind
		solid.erase(cell)
	var best: Array = []
	var best_cost := 1 << 30
	for goal in goals:
		var result := _cheapest_clearance(home,goal,solid,clearable)
		if result.is_empty(): continue
		var score: int = int(result.cost) * 10000 + int(result.steps)
		if score < best_cost:
			best_cost = score
			best = [goal,result.first,int(result.obstacles)]
	if best.is_empty(): return {"state":"sealed","kind":kind,"seal":_route_seal(home,solid,clearable,wrecks)}
	if best[1] == null: return {"state":"open","kind":kind,"goal":best[0]}
	var obstacle: Vector2i = best[1]
	return {"state":"recover" if clearable[obstacle] == "recover" else "clear","kind":kind,"goal":best[0],"obstacle":obstacle,"obstacle_kind":clearable[obstacle],"steps":best[2]}

static func _route_step(total: int) -> String:
	return "" if total <= 1 else "step 1 of %d: " % total

# Name the nearest thing sealing the region a bay can reach (with rock and wrecks
# counted as clearable). Reports the obstacle; it does not promise a route beyond it.
func _route_seal(home: Vector2i, solid: Dictionary, clearable: Dictionary, wrecks: Dictionary) -> String:
	var queued := {}
	for order in orders: queued[order.pos] = true
	for worker in drones.values():
		if not worker.order.is_empty(): queued[worker.order.pos] = true
	var seen := {home: true}
	var queue: Array = [home]
	var head := 0
	var seal := {}
	while head < queue.size():
		var cell: Vector2i = queue[head]
		head += 1
		for offset in Routes.STEPS:
			var next: Vector2i = cell+offset
			if next.x < 0 or next.y < 0 or next.x >= 40 or next.y >= 40 or seen.has(next): continue
			if Routes.can_step(cell,next,home,Vector2i(-1,-1),solid,true):
				seen[next] = true
				queue.append(next)
			elif not seal.has(next):
				seal[next] = true
	var best := ""
	var best_distance := 1 << 30
	for cell in seal:
		var reason := ""
		if queued.has(cell): reason = "queued construction at %s blocks it until built" % cell
		elif wrecks.has(cell) and not wrecks[cell].cleared and wrecks[cell].kind in ["cryo","charging"]: reason = "sealed by the derelict ward at %s" % cell
		elif wrecks.has(cell) and not wrecks[cell].cleared and not clearable.has(cell): reason = "sealed by the recovery site at %s" % cell
		elif solid.get(cell) is Dictionary: reason = "the room at %s has no port facing that way" % cell
		else: continue
		var distance: int = absi(cell.x-home.x)+absi(cell.y-home.y)
		if distance < best_distance:
			best_distance = distance
			best = reason
	return best if not best.is_empty() else "check surveyed sites and bay ports"

func _cheapest_clearance(start: Vector2i, goal: Vector2i, solid: Dictionary, clearable: Dictionary) -> Dictionary:
	# Fewest clearances first, then the shortest route: entering a clearable obstacle
	# moves to the next bucket. Room ports are honoured as the router's service fallback.
	var cost := {start: 0}
	var steps := {start: 0}
	var first := {start: null}
	var obstacles := {start: 0}
	var buckets: Array = [[start]]
	var level := 0
	while level < buckets.size():
		var bucket: Array = buckets[level]
		var head := 0
		while head < bucket.size():
			var cell: Vector2i = bucket[head]
			head += 1
			if int(cost[cell]) != level: continue
			for offset in Routes.STEPS:
				var next: Vector2i = cell+offset
				if next.x < 0 or next.y < 0 or next.x >= 40 or next.y >= 40: continue
				if not Routes.can_step(cell,next,start,goal,solid,true): continue
				# Recovery costs Metal, so a free rock or wreck clearance is preferred.
				var step := (2 if clearable[next] == "recover" else 1) if clearable.has(next) and next != goal else 0
				var total: int = level + step
				var length: int = int(steps[cell]) + 1
				if cost.has(next) and (int(cost[next]) < total or (int(cost[next]) == total and int(steps[next]) <= length)): continue
				cost[next] = total
				steps[next] = length
				first[next] = next if step > 0 and first[cell] == null else first[cell]
				obstacles[next] = int(obstacles[cell]) + (1 if step > 0 else 0)
				while buckets.size() <= total: buckets.append([])
				buckets[total].append(next)
		level += 1
	if not cost.has(goal): return {}
	return {"cost": cost[goal], "steps": steps[goal], "first": first[goal], "obstacles": obstacles[goal]}

func snapshot() -> Dictionary:
	var state := {"drones":drones.duplicate(true), "orders":orders.duplicate(true)}
	if sites_initialized: state["sites"] = sites.duplicate(true)
	return state

static func valid(value: Variant, rooms: Array) -> bool:
	if value == null: return true
	if not value is Dictionary or not value.get("drones") is Dictionary or not value.get("orders") is Array: return false
	if value.has("sites") and not Sites.valid(value.sites): return false
	if value.drones.size()>1600 or value.orders.size()>1600: return false
	var homes := {}
	var occupied := {}
	for room in rooms:
		if not room is Dictionary or not room.get("pos") is Vector2i: return false
		occupied[room.pos] = true
		if room.id == "brine_core" or BAY_KINDS.has(room.id): homes[room.pos] = room.id
	for cell in value.get("sites",{}):
		if occupied.has(cell) and value.sites[cell].units>0: return false
	var pending: Array = value.orders.duplicate()
	for home in value.drones:
		var d = value.drones[home]
		if not homes.has(home) or not d is Dictionary: return false
		if d.get("home") != home or d.get("kind") != BAY_KINDS.get(homes[home],"construction"): return false
		if d.get("bootstrap") != (homes[home]=="brine_core"): return false
		if not d.get("position") is Vector2 or not d.position.is_finite() or not d.get("target") is Vector2 or not d.target.is_finite(): return false
		if not d.get("elapsed") is float or not is_finite(d.elapsed) or d.elapsed<0.0 or d.elapsed>120.0: return false
		if d.get("phase") not in ["docked","launching","outbound","working","returning","docking"] or d.get("job") not in ["","construct","clear","harvest"]: return false
		if d.has("return_from") and (not d.return_from is Vector2 or not d.return_from.is_finite()): return false
		if not d.get("order") is Dictionary: return false
		if d.has("clock") and (not d.clock is float or not is_finite(d.clock) or d.clock<0): return false
		if d.has("route"):
			if not d.route is Array or d.route.size()>1601: return false
			for point in d.route:
				if not point is Vector2 or not point.is_finite() or point.x<0 or point.y<0 or point.x>=40 or point.y>=40: return false
		for field in ["route_goal","last_cell"]:
			if d.has(field) and not d[field] is Vector2i: return false
		if d.has("route_wait") and not d.route_wait is bool: return false
		if d.has("idle_retry") and (not d.idle_retry is float or not is_finite(d.idle_retry) or d.idle_retry<0 or d.idle_retry>1): return false
		for field in ["battery","charge_credit"]:
			if d.has(field) and (not d[field] is float or not is_finite(d[field]) or d[field]<0 or d[field]>(BATTERY_CAPACITY if field=="battery" else CHARGE_PER_POWER)): return false
		for field in ["cargo","pending_yield"]:
			if not d.get(field,{}) is Dictionary: return false
			for key in d.get(field,{}):
				if key not in ["metal","data"] or not d[field][key] is int or d[field][key]<0 or d[field][key]>100000: return false
		if not d.order.is_empty():
			if d.kind != "construction" or d.job != "construct": return false
			pending.append(d.order)
	var reserved_cells := {}
	var manual_builders := {}
	for order in pending:
		if not order is Dictionary or not order.get("pos") is Vector2i or not order.get("rotation") is int: return false
		if order.has("work") and (not order.work is float or not is_finite(order.work) or order.work<0 or order.work>10): return false
		if order.has("builder"):
			if order.builder not in ["bill","veld","branforth","marsh"]: return false
			if manual_builders.has(order.builder): return false
			manual_builders[order.builder]=true
			if not order.get("work_cell") is Vector2i or not occupied.has(order.work_cell): return false
			if not order.get("work_point") is Vector2 or not order.work_point.is_finite(): return false
			if Vector2i(floori(order.work_point.x/384),floori(order.work_point.y/384))!=order.work_cell: return false
			if order.get("facing") not in ["north","east","south","west"]: return false
			if order.pos-order.work_cell != Routes.STEPS[["north","east","south","west"].find(order.facing)]: return false
		if order.rotation<0 or order.rotation>3 or preload("res://scripts/room_database.gd").get_room(str(order.get("id",""))).is_empty(): return false
		var cell: Vector2i = order.pos
		if cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40 or occupied.has(cell) or reserved_cells.has(cell): return false
		reserved_cells[cell] = true
	return true

func restore(value: Variant) -> void:
	drones = {} if value == null else value.drones.duplicate(true)
	orders = [] if value == null else value.orders.duplicate(true)
	sites_initialized = value != null and value.has("sites")
	sites = value.sites.duplicate(true) if sites_initialized else {}
	clearance_seconds.clear()
	delivered.clear()
