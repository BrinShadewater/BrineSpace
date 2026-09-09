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
	var cell:=Vector2i(10,10)
	var galley: Dictionary=add(game,"galley",cell)
	game.resources.biomass=1; game.resources.water=1; game.resources.power=1
	var result: Dictionary=game._simulate_room_economy()
	assert(result.delta.biomass==-1 and result.delta.water==-1 and result.delta.food==4 and result.delta.power==-1)
	assert(game.resources.biomass==1,"Forecast must not spend ingredients")
	add(game,"galley",Vector2i(12,10))
	result=game._simulate_room_economy()
	assert(result.working_cells.size()==1 and result.delta.food==4,"Shared ingredients spent once")
	for resource in ["biomass","water","power"]:
		game.resources.biomass=2; game.resources.water=2; game.resources.power=2
		game.resources[resource]=0
		assert(game._simulate_room_economy().working_cells.is_empty(),"Missing "+resource+" stops cooking")
	game.resources.biomass=2; game.resources.water=2; game.resources.power=4
	galley.suspended=true
	assert(not game._simulate_room_economy().working_cells.has(cell))
	galley.suspended=false
	var hydro: Dictionary=add(game,"hydroponics_bay",Vector2i(10,11))
	game.resources.biomass=0
	result=game._simulate_room_economy()
	assert(not result.working_cells.has(cell) and result.delta.biomass==1,"New growth cannot cook in same cycle")
	var links: Array=Synergy.evaluate(game.placed_rooms,game.occupied).links
	assert(links.size()==1 and links[0].id=="fresh_provisions")
	assert(Discovery.functioning_links(links,{cell:true}).is_empty())
	var active: Array=Discovery.functioning_links(links,{cell:true,hydro.pos:true})
	var discovered: Dictionary={}
	var progress: Dictionary={}
	for cycle in range(1,4):
		var step:=Discovery.advance_cycle(active,progress,discovered,{})
		assert(step.new_stabilization_ids.has("fresh_provisions")==(cycle==3))
		progress=step.progress; discovered.fresh_provisions=true
	assert(Discovery.advance_cycle([],progress,discovered,{}).progress.fresh_provisions==0)
	game.connected_synergy_links=links
	game.resources.biomass=2; game.resources.power=10
	var unknown: Dictionary=game._simulate_room_economy(true)
	var actual: Dictionary=game._simulate_room_economy(false)
	assert(actual.delta.food==unknown.delta.food+1)
	hydro.pos=Vector2i(11,10); game.occupied.erase(Vector2i(10,11)); game.occupied[hydro.pos]=hydro
	assert(Synergy.evaluate(game.placed_rooms,game.occupied).links.is_empty(),"Sealed wall is not a connection")
	assert(Discovery.validate_unlock_graph(Rooms.all_rooms(),Synergy.all_synergies(),Rooms.STARTING_UNLOCKS).is_empty())
	game.free()
	if not FileAccess.file_exists("res://tests/test_galley_economy.gd.uid"):
		var f:=FileAccess.open("res://tests/test_galley_economy.gd.uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("GALLEY ECONOMY PASS: conversion, shared ingredients, shortages, new-growth delay, suspension, connected discovery, hidden forecast and three functioning cycles")
	quit()
