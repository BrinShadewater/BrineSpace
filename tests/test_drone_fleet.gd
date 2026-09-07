extends SceneTree
const Fleet = preload("res://scripts/drone_fleet.gd")
func _init() -> void:
	var fleet = Fleet.new()
	var home := Vector2i(20,20)
	var rooms: Array = [{"id":"construction_drone_bay","pos":home}]
	fleet.enqueue("corridor",Vector2i(20,21),0)
	fleet.advance(20.0,rooms,{}, {})
	assert(not fleet.deployed(home),"Unpowered bays cannot launch")
	assert(fleet.orders.size()==1,"Unpowered bays retain paid orders")
	fleet.advance(2.5,rooms,{home:true},{})
	assert(fleet.deployed(home),"Drone leaves its cradle")
	assert(fleet.advance(0.0,rooms,{home:true},{}).is_empty(),"Zero simulation time cannot finish work")
	var completed = fleet.advance(20.0,rooms,{home:true},{})
	assert(completed.size()==1 and completed[0].id=="corridor","Construction finishes once")
	assert(fleet.advance(60.0,rooms,{home:true},{}).is_empty(),"Completed orders cannot replay")
	assert(not fleet.deployed(home),"Idle construction drone returns to its bay")
	var miner = Fleet.new()
	var mining_rooms: Array = [{"id":"mining_drone_bay","pos":home}]
	miner.synchronize(mining_rooms)
	# One finite load isolates duplicate delivery from legitimate new extraction.
	miner.sites_initialized = true
	miner.sites = {Vector2i(22,22): Fleet.Sites.make_site("mining",1)}
	miner.advance(8.0,mining_rooms,{home:true},{})
	assert(miner.delivered.is_empty(),"Harvest is not paid before returning")
	miner.advance(20.0,mining_rooms,{home:true},{})
	assert(miner.delivered.get("metal",0)==2,"Harvest cargo reaches storage at dock")
	miner.advance(30.0,mining_rooms,{home:true},{})
	assert(miner.delivered.is_empty(),"No duplicate cargo payment")
	var snapshot = miner.snapshot()
	assert(Fleet.valid(snapshot,mining_rooms),"Cargo and animation clocks survive save validation")
	snapshot.drones[home].elapsed = NAN
	assert(not Fleet.valid(snapshot,mining_rooms),"Invalid timing is rejected")
	var salvager = Fleet.new()
	var salvage_rooms: Array = [{"id":"salvage_drone_bay","pos":home}]
	salvager.synchronize(salvage_rooms)
	salvager.sites_initialized = true
	salvager.sites = {Vector2i(22,22): Fleet.Sites.make_site("salvage",1)}
	salvager.advance(11.1,salvage_rooms,{home:true},{})
	assert(salvager.delivered.is_empty(),"Salvage cargo remains aboard during return")
	var cargo_save: Dictionary = salvager.snapshot()
	assert(Fleet.valid(cargo_save,salvage_rooms),"Salvage cargo checkpoint validates")
	var resumed = Fleet.new()
	resumed.restore(cargo_save)
	resumed.advance(10.0,salvage_rooms,{home:true},{})
	assert(resumed.delivered=={"metal":1,"data":1},"Saved salvage cargo pays both resources at dock")
	resumed.advance(30.0,salvage_rooms,{home:true},{})
	assert(resumed.delivered.is_empty(),"Salvage return cannot pay twice")
	print("Drone fleet state-machine tests passed")
	quit()
