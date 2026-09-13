extends SceneTree
const Fire=preload("res://scripts/room_fire.gd")
const Flood=preload("res://scripts/room_flooding.gd")
const Repairs=preload("res://scripts/hull_repair.gd")
var failures := 0
func check(ok: bool,message: String):
	if not ok: failures+=1;push_error(message)
func _init(): call_deferred("run")
func run():
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://fire-gameplay-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	game.meta.selected_architect="bill"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.minimize();game.crew_comms.set_process(false)
	game.running=true;game.paused=false
	game.wrecks[Vector2i(24,20)]=game.wrecks[Vector2i(22,20)]
	game.wrecks.erase(Vector2i(22,20))
	game.wrecks.erase(Vector2i(23,20));game.drone_fleet.orders.clear();game.drone_fleet.sites.clear()
	game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear()
	for x in range(20,24):
		var id: String=["brine_core","reactor","corridor","storage_bay"][x-20]
		var added: Dictionary=game.RoomDatabaseScript.get_room(id).duplicate(true)
		added.pos=Vector2i(x,20);added.rotation=1 if id=="corridor" else 0
		game.placed_rooms.append(added);game.occupied[added.pos]=added
	game.resources.power=40;game.resources.water=20;game.resources.food=100;game.resources.oxygen=100
	game._check_synergies()
	game._apply_room_economy() # Establish operation through the actual paid cycle.
	var cell := Vector2i(21,20)
	var room: Dictionary=game.occupied[cell]
	var sound=game.station_sound
	sound.set_process(false)
	game.hardware.pumps=false;game.hardware.doors=false;game.hardware.sprinklers=false
	room.fire_heat=0.8;room.electrical_fault=true
	sound.observe_hazards()
	check(sound.voices.has("electrical_crackle"),"Powered fault emits spatial crackle")
	room.suspended=true;sound.observe_hazards()
	check(not sound.voices.has("electrical_crackle"),"Isolation immediately stops electrical sound")
	room.suspended=false;room.fire_heat=0.99
	Fire.cycle(game)
	check(Fire.burning(room),"Operating reactor ignites from heat")
	for i in range(400):
		Fire.advance(game,0.1);Flood.step_water(game,0.1)
	check(room.hull_crack>0 and room.water_level>0,"Unsuppressed fire creates a real hull leak and rising water")
	sound.observe_hazards()
	check(sound.voices.has("leak_drip"),"Leaking room emits drips")
	print("CHAIN AFTER 40s fire=",room.fire," crack=",room.hull_crack," water=",room.water_level)
	game.hardware.sprinklers=true
	Fire.advance(game,0.1);sound.observe_hazards()
	check(sound.voices.has("sprinkler_hiss"),"Paid active spray emits hiss")
	await physics_frame
	await process_frame
	var before_age: float=sound.voices.sprinkler_hiss.age
	game.paused=true;sound._process(0.1)
	check(sound.voices.sprinkler_hiss.age==before_age,"Pause freezes hazard audio lifetime")
	if DisplayServer.get_name()!="headless": check(sound.voices.sprinkler_hiss.player.stream_paused,"Pause freezes active hazard audio")
	game.paused=false;game.hardware.power=false;sound.observe_hazards()
	check(not sound.voices.has("sprinkler_hiss"),"Power loss silences spray")
	game.hardware.power=true
	for i in range(200):
		Fire.advance(game,0.1);Flood.step_water(game,0.1)
		if not Fire.burning(room): break
	sound.observe_hazards()
	check(not Fire.burning(room) and not sound.voices.has("sprinkler_hiss"),"Suppression clears flames and hiss")
	check(room.hull_crack>0 and room.water_level>0,"Suppression leaves structural damage and floodwater")
	game.resources.metal=20
	preload("res://scripts/architects.gd").advance_core(game,10.0)
	var actor=game.bill_npc
	actor.rebuild(game)
	actor.active=true
	var initial_foot: Vector2=actor.foot
	check(Repairs.request(game,cell,true),"Emergency patch queues against actual fire damage")
	for i in range(1800):
		game._update_test_walker(0.1)
		if not room.has("leak_repair"): break
	print("CHAIN PATCH ",room.get("leak_repair",{})," actor=",actor.activity," foot=",actor.foot)
	check(room.get("hull_patched",false) and actor.foot!=initial_foot,"Crew travel to reactor and physically patch it")
	check(Repairs.request(game,cell),"Permanent weld queues after patch")
	for i in range(1200):
		game._update_test_walker(0.1)
		if not room.has("leak_repair"): break
	sound.observe_hazards()
	check(room.hull_crack==0 and not sound.voices.has("leak_drip"),"Full weld seals damage and silences drips")
	check(not actor.dead and game.resources.metal==17,"Crew survive and both repair costs are charged")
	game.hardware.pumps=true
	for i in range(1500):
		game._update_test_walker(0.1)
		if room.water_level<=0: break
	check(room.water_level<=0,"Powered pumps clear residual floodwater")
	sound.prior_crack_stages[cell]=0;room.hull_crack=0.36;sound.elapsed+=20;sound.observe_hazards()
	check(sound.voices.has("crack_creak"),"Crossing damage stage emits creak")
	var stamp: float=sound.last_event.crack_creak
	sound.observe_hazards()
	check(sound.last_event.crack_creak==stamp,"Unchanged crack stage does not repeat creak")
	room.hull_crack=0
	for kind in sound.HAZARD_EVENTS:
		var stream=preload("res://scripts/station_audio_cues.gd").get_stream(kind)
		check(stream.data.size()>0,"Hazard cue has PCM data: "+kind)
		stream.save_to_wav("res://output/"+kind+".wav")
	print("HAZARD CHAIN ","PASS" if failures==0 else "FAIL"," failures=",failures)
	DirAccess.remove_absolute(game.run_save_path);DirAccess.remove_absolute(game.meta.save_path)
	quit(0 if failures==0 else 1)
