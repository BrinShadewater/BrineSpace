extends SceneTree
const Main=preload("res://scripts/main.gd")
const Rooms=preload("res://scripts/room_database.gd")
const Synergy=preload("res://scripts/synergy_manager.gd")
const Discovery=preload("res://scripts/discovery_manager.gd")
func add(game,id,cell):
	var r: Dictionary=Rooms.get_room(id)
	r.pos=cell; r.rotation=0
	game.placed_rooms.append(r); game.occupied[cell]=r
	return r
func _init() -> void:
	var game=Main.new()
	var food_base: int=game._get_resource_capacity("food")
	var bio_base: int=game._get_resource_capacity("biomass")
	var cell:=Vector2i(10,10)
	var store: Dictionary=add(game,"cold_store",cell)
	assert(game._get_resource_capacity("food")==food_base+40)
	assert(game._get_resource_capacity("biomass")==bio_base+20)
	game.resources.power=1
	var result: Dictionary=game._simulate_room_economy()
	assert(result.delta.power==-1 and result.working_cells.has(cell))
	game.resources.food=food_base+35
	game.resources.power=0
	assert(not game._simulate_room_economy().working_cells.has(cell))
	game._clamp_resource_storage()
	assert(game.resources.food==food_base+35,"Outage must not discard stored food")
	store.suspended=true
	assert(game._get_resource_capacity("food")==food_base+40)
	assert(not game._simulate_room_economy().working_cells.has(cell))
	store.suspended=false
	var other: Dictionary=add(game,"cold_store",Vector2i(12,10))
	assert(game._get_resource_capacity("food")==food_base+80)
	game.placed_rooms.erase(other); game.occupied.erase(other.pos)
	var galley: Dictionary=add(game,"galley",Vector2i(10,9))
	var links: Array=Synergy.evaluate(game.placed_rooms,game.occupied).links
	assert(links.size()==1 and links[0].id=="cold_chain")
	game.connected_synergy_links=links
	game.resources.biomass=1; game.resources.water=1; game.resources.power=2
	result=game._simulate_room_economy()
	assert(result.delta.food==5 and result.links.size()==1 and result.delta.power==-2)
	assert(game._simulate_room_economy(true).delta.food==4,"Undiscovered forecast hides bonus")
	store.suspended=true
	assert(game._simulate_room_economy().delta.food==4)
	store.suspended=false
	var progress: Dictionary={}
	var discovered: Dictionary={}
	for cycle in range(1,4):
		var step:=Discovery.advance_cycle(result.links,progress,discovered,{})
		assert(step.new_stabilization_ids.has("cold_chain")==(cycle==3))
		progress=step.progress; discovered.cold_chain=true
	assert(Discovery.advance_cycle([],progress,discovered,{}).progress.cold_chain==0)
	galley.pos=Vector2i(11,10); game.occupied.erase(Vector2i(10,9)); game.occupied[galley.pos]=galley
	assert(Synergy.evaluate(game.placed_rooms,game.occupied).links.is_empty())
	assert(Discovery.validate_unlock_graph(Rooms.all_rooms(),Synergy.all_synergies(),Rooms.STARTING_UNLOCKS).is_empty())
	game.free()
	if not FileAccess.file_exists("res://tests/test_cold_store_economy.gd.uid"):
		var f:=FileAccess.open("res://tests/test_cold_store_economy.gd.uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("COLD STORE ECONOMY PASS: additive capacity, outage retention, power cost, suspension, galley connection, hidden forecast and three-cycle discovery")
	quit()
