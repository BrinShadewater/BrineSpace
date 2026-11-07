extends SceneTree
const Generator=preload("res://scripts/site_generator.gd")
const Discovery=preload("res://scripts/site_discovery.gd")
const Architects=preload("res://scripts/architects.gd")
const Meta=preload("res://scripts/meta_state.gd")
class World extends RefCounted:
	var site_layout: Dictionary
	var wrecks: Dictionary
	var surveyed_water: Dictionary={}
	var architect_run: Dictionary
	var meta
var failures := 0
func _init(): call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
func world(seed_value: int, starter: String, profile) -> World:
	var game:=World.new()
	game.site_layout=Generator.generate(seed_value)
	game.wrecks=game.site_layout.wrecks.duplicate(true)
	game.architect_run={"version":5,"selected":starter,"core":Architects.pod(starter,"core_architect")}
	game.meta=profile
	return game
func run():
	for starter in Architects.IDS:
		var profile=Meta.new()
		profile.save_path="user://site_discovery_%s_%d.json"%[starter,OS.get_process_id()]
		profile.unlocked_architect_ids[starter]=true
		profile.sighted_character_ids[starter]=true
		var game:=world(32,starter,profile)
		check(Architects.valid(game.architect_run,game.wrecks,[]),"unidentified validation "+starter)
		check(Discovery.reveal(game).is_empty(),"no unsurveyed discovery")
		var expected: Array=Discovery.ORDER.duplicate();expected.erase(starter);expected.erase("bill")
		if starter!="bill": expected.append("bill")
		for i in range(3):
			# Visit farthest first: assigned identity must follow discovery, not radius.
			var cell: Vector2i=game.site_layout.recovery_cells[2-i]
			game.surveyed_water[cell]=true
			check(Discovery.reveal(game)==[cell],"one newly explored site")
			var ward: Dictionary=game.wrecks[cell]
			check(ward.pods[0].architect_id==expected[i],"first-sighting sequence "+starter)
			check((ward.kind=="charging")== (expected[i]=="marsh"),"matching chamber type")
			check(not profile.met_character_ids.has(expected[i]),"sighting does not unlock shop")
			check(Architects.valid(game.architect_run,game.wrecks,[]),"assigned validation")
		check(Discovery.reveal(game).is_empty(),"repeat survey is stable")
		var reload=Meta.new();reload.save_path=profile.save_path
		check(reload.sighted_character_ids==profile.sighted_character_ids,"sightings persist across abandonment")
		var later:=world(51,starter,reload)
		for cell in later.site_layout.recovery_cells: later.surveyed_water[cell]=true
		check(Discovery.reveal(later).size()==3,"known characters all reveal")
		check(Architects.valid(later.architect_run,later.wrecks,[]),"later expedition no duplicates")
	# Fully known rosters use one shuffle, independent of survey batching and location.
	for starter in Architects.IDS:
		var permutations: Dictionary={}
		for seed_value in range(24):
			var known=Meta.new()
			known.save_path="user://site_known_%s_%d_%d.json"%[starter,seed_value,OS.get_process_id()]
			for id in Architects.IDS: known.sighted_character_ids[id]=true
			var batch:=world(seed_value,starter,known)
			for cell in batch.site_layout.recovery_cells: batch.surveyed_water[cell]=true
			var revealed:=Discovery.reveal(batch)
			var order: Array=[]
			for cell in revealed: order.append(batch.wrecks[cell].pods[0].architect_id)
			permutations[str(order)]=true
			check(order.size()==3 and not order.has(starter),"known shuffle excludes starter")
			var serial:=world(seed_value,starter,known)
			for i in range(3):
				var cell: Vector2i=serial.site_layout.recovery_cells[2-i]
				serial.surveyed_water[cell]=true
				check(Discovery.reveal(serial)==[cell],"known serial discovery")
				check(serial.wrecks[cell].pods[0].architect_id==order[i],"known shuffle independent of location/batching")
				# Reconstruct from saved geography and assigned wards between discoveries.
				var continued:=world(seed_value,starter,known)
				continued.site_layout=serial.site_layout.duplicate(true)
				continued.wrecks=serial.wrecks.duplicate(true)
				continued.surveyed_water=serial.surveyed_water.duplicate()
				serial=continued
			check(Architects.valid(serial.architect_run,serial.wrecks,[]),"known shuffle no duplicates after Continue")
		check(permutations.size()==6,"all known roster permutations occur across seeds: "+starter)
	var profile=Meta.new();profile.save_path="user://site_discovery_batch_%d.json"%OS.get_process_id()
	var game:=world(5,"bill",profile)
	for cell in game.site_layout.recovery_cells: game.surveyed_water[cell]=true
	var cells:=Discovery.reveal(game)
	for i in range(3): check(game.wrecks[cells[i]].pods[0].architect_id==Discovery.ORDER[i],"simultaneous distance order")
	# A partial profile skips a previously sighted Veld, even if never rescued.
	profile=Meta.new();profile.save_path="user://site_discovery_partial_%d.json"%OS.get_process_id()
	profile.record_sighting("veld")
	game=world(9,"bill",profile)
	game.surveyed_water[game.site_layout.recovery_cells[0]]=true
	cells=Discovery.reveal(game)
	check(game.wrecks[cells[0]].pods[0].architect_id=="branforth","partial profile advances")
	# Old progression migrates met/owned characters without changing purchase state.
	var path: String="user://site_discovery_old_%d.json"%OS.get_process_id()
	FileAccess.open(path,FileAccess.WRITE).store_string(JSON.stringify({"met_character_ids":["veld"],"unlocked_architect_ids":["bill","branforth"]}))
	profile=Meta.new();profile.save_path=path
	check(profile.sighted_character_ids.has("veld") and profile.sighted_character_ids.has("branforth"),"legacy profile migration")
	profile.save_path="user://missing_site_folder/profile.json"
	game=world(18,"bill",profile)
	game.surveyed_water[game.site_layout.recovery_cells[0]]=true
	check(Discovery.reveal(game).is_empty(),"failed progression write cannot advance discovery")
	var save=preload("res://scripts/run_save.gd")
	check(not save.valid_site({"architects":{"version":"bad"}}),"malformed legacy version rejected")
	var malformed: Dictionary={"architects":{"version":5},"site_layout":game.site_layout,"wrecks":null}
	check(not save.valid_site(malformed),"null terrain rejected")
	malformed.wrecks=game.wrecks.duplicate(true)
	malformed.wrecks[game.site_layout.recovery_cells[0]]=null
	check(not save.valid_site(malformed),"null recovery site rejected")
	print("SITE DISCOVERY: failures=",failures)
	quit(0 if failures==0 else 1)
