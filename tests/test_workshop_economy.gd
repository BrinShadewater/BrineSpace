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
	var workshop: Dictionary=add(game,"salvage_workshop",cell)
	game.resources.metal=3; game.resources.power=2
	var result: Dictionary=game._simulate_room_economy()
	assert(result.delta.metal==-3 and result.delta.rare_minerals==1 and result.delta.power==-2)
	assert(game.resources.metal==3,"Forecast must not spend resources")
	add(game,"salvage_workshop",Vector2i(12,10))
	result=game._simulate_room_economy()
	assert(result.working_cells.size()==1 and result.delta.rare_minerals==1,"Shared inputs spent once")
	game.resources.metal=2
	assert(game._simulate_room_economy().working_cells.is_empty(),"No metal, no output")
	game.resources.metal=6; game.resources.power=1
	assert(game._simulate_room_economy().working_cells.is_empty(),"Insufficient power stops conversion")
	game.resources.power=4; workshop.suspended=true
	assert(not game._simulate_room_economy().working_cells.has(cell))
	workshop.suspended=false
	var bay: Dictionary=add(game,"salvage_drone_bay",Vector2i(10,11))
	var links: Array=Synergy.evaluate(game.placed_rooms,game.occupied).links
	assert(links.size()==1 and links[0].id=="parts_reclamation")
	assert(Discovery.functioning_links(links,{cell:true}).is_empty())
	var active: Array=Discovery.functioning_links(links,{cell:true,bay.pos:true})
	var discovered: Dictionary={}
	var progress: Dictionary={}
	for cycle in range(1,4):
		var step:=Discovery.advance_cycle(active,progress,discovered,{})
		assert(step.new_stabilization_ids.has("parts_reclamation")== (cycle==3))
		progress=step.progress; discovered.parts_reclamation=true
	var reset:=Discovery.advance_cycle([],progress,discovered,{})
	assert(reset.progress.parts_reclamation==0)
	game.connected_synergy_links=links
	game.resources.power=10
	var unknown: Dictionary=game._simulate_room_economy(true)
	var actual: Dictionary=game._simulate_room_economy(false)
	assert(actual.delta.metal==unknown.delta.metal+1,"Unknown bonus excluded from known-only forecast")
	bay.rotation=1
	assert(Synergy.evaluate(game.placed_rooms,game.occupied).links.is_empty(),"Matching doors required")
	assert(Discovery.validate_unlock_graph(Rooms.all_rooms(),Synergy.all_synergies(),Rooms.STARTING_UNLOCKS).is_empty())
	game.free()
	if not FileAccess.file_exists("res://tests/test_workshop_economy.gd.uid"):
		var f:=FileAccess.open("res://tests/test_workshop_economy.gd.uid",FileAccess.WRITE)
		f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("WORKSHOP ECONOMY PASS: conversion, shared budget, missing inputs, suspension, matched-door discovery, hidden forecast and three functioning cycles")
	quit()
