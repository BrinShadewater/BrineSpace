extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
const Routes = preload("res://scripts/drone_routes.gd")
const HOME = Vector2i(2,2)
const GOAL = Vector2i(20,20)
var checks := 0
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func setup():
	var fleet=Fleet.new();fleet.sites_initialized=true
	fleet.synchronize(rooms())
	var drone: Dictionary=fleet.drones[HOME]
	drone.phase="outbound";drone.job="construct";drone.target=Vector2(GOAL)
	drone.order={"id":"corridor","pos":GOAL,"rotation":0}
	return fleet
func rooms() -> Array:return [{"id":"construction_drone_bay","pos":HOME}]
func wall() -> Dictionary:
	var result:={}
	for offset in Routes.STEPS:result[GOAL+offset]={"kind":"basalt","cleared":false,"active":true,"progress":0.0}
	return result
func run():
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected.replace("\\","/").simplify_path():
		push_error("Drone cache test requires isolated profile");quit(2);return
	for speed in [1.0,2.0,4.0]:
		var fleet=setup();var wrecks:=wall()
		for i in range(60):fleet.advance(speed/60.0,rooms(),{HOME:true},wrecks)
		check(fleet.failed_routes.size()==1,"One cached failure across rebuilt blocker maps")
		check(fleet.drones[HOME].position==Vector2(HOME) and fleet.drones[HOME].route_wait,"Blocked drone waits without moving")
		var saved: Dictionary=fleet.snapshot()
		check(Fleet.valid(saved,rooms()),"Waiting drone remains save-valid")
		check(not saved.has("failed_routes"),"Cache is not persisted")
		fleet.restore(saved)
		check(fleet.failed_routes.is_empty(),"Restore clears transient failures")
		fleet.advance(speed/60.0,rooms(),{HOME:true},wrecks)
		wrecks[GOAL+Vector2i.UP].cleared=true
		fleet.advance(speed/60.0,rooms(),{HOME:true},wrecks)
		check(fleet.failed_routes.is_empty() and not fleet.drones[HOME].route_wait,"Excavation opens path on next advance")
		check(fleet.drones[HOME].position!=Vector2(HOME),"Resumes movement immediately")
	# Each blocker source must invalidate even when its entry count is unchanged.
	for source in ["site","order","worker"]:
		var fleet=setup();var wrecks:=wall();var door:=GOAL+Vector2i.UP
		wrecks.erase(door)
		if source=="site":fleet.sites[door]=Fleet.Sites.make_site("mining",1)
		elif source=="order":fleet.enqueue("corridor",door,0)
		else:
			var second: Array=rooms()+[{"id":"construction_drone_bay","pos":Vector2i(3,2)}]
			fleet.synchronize(second);fleet.drones[Vector2i(3,2)].order={"id":"corridor","pos":door,"rotation":0}
		var active_rooms: Array=rooms() if source!="worker" else rooms()+[{"id":"construction_drone_bay","pos":Vector2i(3,2)}]
		fleet.advance(0.01,active_rooms,{HOME:true},wrecks)
		check(fleet.drones[HOME].route_wait,"Source blocks: "+source)
		if source=="site":fleet.sites[door].units=0
		elif source=="order":fleet.orders.clear()
		else:fleet.drones[Vector2i(3,2)].order={}
		fleet.advance(0.01,active_rooms,{HOME:true},wrecks)
		check(not fleet.drones[HOME].route_wait,"Source removal recovers: "+source)
	var fleet=setup();var wrecks:=wall()
	fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	fleet.drones[HOME].phase="returning" # Cancelled outbound work returns home.
	fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	check(fleet.drones[HOME].phase=="docking","Changed destination is not blocked by old failure")
	fleet=setup();fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	fleet.drones[HOME].position=Vector2(GOAL);fleet.drones[HOME].last_cell=GOAL
	fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	check(fleet.drones[HOME].phase=="working","Changed origin does not reuse old failure")
	# Same-sized topology replacement must invalidate by contents, not size/hash alone.
	fleet=setup();fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	wrecks.erase(GOAL+Vector2i.UP);wrecks[Vector2i(30,30)]={"kind":"basalt","cleared":false}
	fleet.advance(0.01,rooms(),{HOME:true},wrecks)
	check(not fleet.drones[HOME].route_wait,"Equal-size topology replacement invalidates")
	# Dictionary room blockers still get the port-aware fallback.
	var blockers:={}
	for y in range(40):blockers[Vector2i(10,y)]=true
	blockers[Vector2i(10,2)]={"doors":[Vector2i.LEFT,Vector2i.RIGHT]}
	check(not Routes.find_path(HOME,Vector2i(12,2),blockers).is_empty(),"Room-port fallback preserved")
	blockers[Vector2i(10,2)].doors=[Vector2i.UP,Vector2i.DOWN]
	check(Routes.find_path(HOME,Vector2i(12,2),blockers).is_empty(),"Closed room ports remain impassable")
	var failures_cache:={}
	var enclosed:={Vector2i(1,2):true,Vector2i(2,1):true,Vector2i(3,2):true,Vector2i(2,3):true}
	var drone: Dictionary=setup().drones[HOME]
	for i in range(100):Routes.travel(drone,0.01,Vector2i(10+i%20,10+i/20),enclosed,failures_cache)
	check(failures_cache.size()<=64,"Failure cache is bounded")
	print("DRONE ROUTE CACHE: %d checks; %d failures"%[checks,failures])
	quit(1 if failures else 0)
