extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
const Field = preload("res://scripts/wreck_field.gd")
func _init() -> void:
	for kind in ["mining","salvage"]:
		var fleet = Fleet.new()
		fleet.sites_initialized = true # Isolate clearance cargo from other finite deposits.
		var home := Vector2i(20,20)
		var target := Vector2i(20,21)
		var rooms: Array = [{"id":kind+"_drone_bay","pos":home}]
		var field := {target:{"kind":"basalt" if kind=="mining" else "engineering","progress":0.0,"active":true,"cleared":false}}
		var power := 0
		var metal := 0
		for frame in range(250):
			fleet.advance(0.1,rooms,{home:true},field,power)
			Field.advance(field,{home:true},0.1,fleet.clearance_seconds)
			metal += int(fleet.delivered.get("metal",0))
		assert(is_equal_approx(field[target].progress,12.0),"Empty battery interrupts work and preserves cuts")
		assert(fleet.drones[home].phase=="docked" and metal==0,"Returns safely and cannot charge without station energy")
		var saved: Dictionary = fleet.snapshot()
		assert(Fleet.valid(saved,rooms))
		fleet.restore(saved)
		power = 2
		for frame in range(300):
			fleet.advance(0.1,rooms,{home:true},field,power)
			power -= fleet.power_spent
			assert(power>=0,"Shared station reserve cannot go negative")
			Field.advance(field,{home:true},0.1,fleet.clearance_seconds)
			metal += int(fleet.delivered.get("metal",0))
		assert(field[target].cleared and metal==Field.YIELDS[field[target].kind],"Recharged drone resumes and delivers clearance yield once")
		assert(power==0,"A full empty battery consumes two station Power")
		var bad: Dictionary = fleet.snapshot()
		bad.drones[home].battery = NAN
		assert(not Fleet.valid(bad,rooms),"Invalid saved charge rejected")
		# Stored battery powers field work even if the station loses power.
		fleet.restore(null)
		fleet.sites_initialized = true
		fleet.sites = {target:Fleet.Sites.make_site(kind)}
		fleet.advance(6.0,rooms,{home:true},{},0)
		var before: float = fleet.drones[home].battery
		fleet.advance(0.2,rooms,{}, {},0)
		assert(fleet.drones[home].battery<before,"Battery supplies work independently of station power")
	var shared = Fleet.new()
	var bays: Array = [{"id":"mining_drone_bay","pos":Vector2i(20,20)},{"id":"salvage_drone_bay","pos":Vector2i(21,20)}]
	shared.synchronize(bays)
	for drone in shared.drones.values(): drone["battery"] = 0.0
	shared.advance(0.5,bays,{Vector2i(20,20):true,Vector2i(21,20):true},{},1)
	assert(shared.power_spent==1,"Two bays share a single station power budget")
	var charging_save: Dictionary = shared.snapshot()
	assert(Fleet.valid(charging_save,bays))
	shared.restore(charging_save)
	shared.advance(0.5,bays,{Vector2i(20,20):true,Vector2i(21,20):true},{},0)
	assert(shared.power_spent==0 and shared.drones[Vector2i(20,20)].battery==3.0,"Saved prepaid charge continues without double billing")
	print("DRONE BATTERY PASS: depletion, return, paid charging, saved charge, resumed jobs and one-time yields")
	quit()
