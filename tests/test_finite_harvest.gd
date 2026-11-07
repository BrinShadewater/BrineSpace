extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
const Sites = preload("res://scripts/harvest_sites.gd")
const Routes = preload("res://scripts/drone_routes.gd")
var failures := 0
func check(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)
func _init() -> void:
	var blocked := {Vector2i(11,10):true,Vector2i(11,11):true}
	var path := Routes.find_path(Vector2i(10,10),Vector2i(12,10),blocked)
	check(path.size()>2,"Obstacle routing detours instead of cutting a wall")
	var previous := Vector2(10,10)
	for point in path:
		check(not blocked.has(Vector2i(point)) and previous.distance_to(point)==1.0,"Route steps remain cardinal and clear")
		previous = point
	var drone := {"home":Vector2i(10,10),"position":Vector2(10,10)}
	Routes.travel(drone,0.2,Vector2i(12,10),{})
	var before: Vector2 = drone.position
	Routes.travel(drone,0.1,Vector2i(12,10),blocked)
	check(before.distance_to(drone.position)<=0.15001,"New obstacle triggers backtracking without teleport")
	for frame in range(100): Routes.travel(drone,0.1,Vector2i(12,10),blocked)
	check(drone.position==Vector2(12,10),"Dynamic detour reaches target")
	var enclosed := {Vector2i(9,10):true,Vector2i(11,10):true,Vector2i(10,9):true,Vector2i(10,11):true}
	check(Routes.find_path(Vector2i(10,10),Vector2i(12,10),enclosed).is_empty(),"Fully enclosed bay reports no exterior route")
	enclosed[Vector2i(11,10)] = {"doors":[Vector2i.LEFT,Vector2i.RIGHT]}
	check(not Routes.find_path(Vector2i(10,10),Vector2i(12,10),enclosed).is_empty(),"A matching service passage provides an enclosed bay's fallback route")
	enclosed[Vector2i(11,10)] = {"doors":[Vector2i.UP,Vector2i.DOWN]}
	check(Routes.find_path(Vector2i(10,10),Vector2i(12,10),enclosed).is_empty(),"Room rotation cannot route drones through sealed walls")
	for kind in ["mining","salvage"]:
		var fleet = Fleet.new()
		var home := Vector2i(20,20)
		var target := Vector2i(22,20)
		var rooms: Array = [{"id":kind+"_drone_bay","pos":home}]
		fleet.sites_initialized = true
		fleet.sites = {target:Sites.make_site(kind,3)}
		var resources := {"metal":0,"data":0}
		var charge_cost := 0
		var saw_partial := false
		for frame in range(1200):
			fleet.advance(0.1,rooms,{home:true},{},30-charge_cost)
			charge_cost += fleet.power_spent
			for key in fleet.delivered: resources[key] += fleet.delivered[key]
			saw_partial = saw_partial or fleet.sites[target].progress>0
			if frame%19==0:
				var save: Dictionary = fleet.snapshot()
				check(Fleet.valid(save,rooms),"Finite sites/routes validate at every stage")
				fleet.restore(save)
		check(fleet.sites[target].discovered and saw_partial,"Nearby survey discovers site and records working progress")
		check(fleet.sites[target].units==0,"Deposit exhausts after its finite loads")
		check(resources.metal==3*Sites.LOADS[kind].metal and resources.data==3*Sites.LOADS[kind].get("data",0),"Total delivered resources equal finite stock exactly")
		check(charge_cost==3,"Three extraction loads use three station Power, including final top-up")
		check(not Sites.blocks(fleet.sites,target),"Exhausted site frees construction footprint")
		var saved: Dictionary = fleet.snapshot()
		fleet.restore(saved)
		fleet.advance(300.0,rooms,{home:true},{})
		check(fleet.delivered.is_empty() and fleet.sites[target].units==0,"Continue and long elapsed time cannot regenerate depleted stock")
		var invalid: Dictionary = saved.duplicate(true)
		invalid.sites[target].units = -1
		check(not Fleet.valid(invalid,rooms),"Negative remaining stock is rejected")
		# Partial work survives an individual site pause and a recharge visit.
		fleet.sites[target] = Sites.make_site(kind,2)
		fleet.sites[target].discovered = true
		fleet.drones[home].idle_retry = 0.0
		fleet.advance(7.0,rooms,{home:true},{})
		var progress: float = fleet.sites[target].progress
		check(progress>0,"Work begins on resumed site")
		fleet.sites[target].active = false
		fleet.advance(10.0,rooms,{home:true},{})
		check(fleet.sites[target].progress==progress,"Paused site retains partial extraction")
	var shared = Fleet.new()
	shared.sites_initialized = true
	shared.sites = {Vector2i(21,20):Sites.make_site("mining",2)}
	var bays: Array = [{"id":"mining_drone_bay","pos":Vector2i(20,20)},{"id":"mining_drone_bay","pos":Vector2i(22,20)}]
	var shared_metal := 0
	for frame in range(1000):
		shared.advance(0.1,bays,{Vector2i(20,20):true,Vector2i(22,20):true},{})
		shared_metal += int(shared.delivered.get("metal",0))
	check(shared_metal==4 and shared.sites[Vector2i(21,20)].units==0,"Competing bays cannot duplicate finite stock")
	var old = Fleet.new()
	old.advance(0.0,[{"id":"brine_core","pos":Vector2i(20,20)}],{}, {})
	var seeded: Dictionary = old.snapshot()
	old.restore(seeded)
	old.advance(0.0,[{"id":"brine_core","pos":Vector2i(20,20)}],{}, {})
	check(old.snapshot()==seeded,"Existing site field is not reseeded")
	print("FINITE HARVEST %s: stock conservation, survey, depletion, pause, saves and obstacle detours" % ("PASS" if failures==0 else "FAIL"))
	quit(0 if failures==0 else 1)
