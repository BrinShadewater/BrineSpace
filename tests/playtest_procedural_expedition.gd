extends SceneTree
## Native, real-clock, dealt-hand paid expedition. No resource/blueprint injection.
const Save=preload("res://scripts/run_save.gd")
const Generator=preload("res://scripts/site_generator.gd")
const Route=preload("res://tests/procedural_route.gd")
var game
var failures := 0
var seed_value := 32
var seconds := 420
var events: Array=[]
var out: String
var tag := ""
var resume_path := ""
var profile_path := ""
var restored := false
var recovered := false
var all_crew := false
var watch_recharge := false
var saw_charging := false
var saw_charge_complete := false
var recorded_rescues: Array=[]
var last_action := -100
var last_reroll := -100
var measured_frames := 0
var frame_totals: Dictionary={}
var slowest_frames: Array=[]
func _init(auto_run: bool=true):
	if not auto_run: return # Native strategy fixtures call choose_build explicitly.
	for arg in OS.get_cmdline_user_args():
		if arg=="--all-crew": all_crew=true
		if arg=="--watch-recharge": watch_recharge=true
		if arg.begins_with("--resume="): resume_path=arg.trim_prefix("--resume=")
		if arg.begins_with("--profile="): profile_path=arg.trim_prefix("--profile=")
		if arg.begins_with("--seed="): seed_value=int(arg.trim_prefix("--seed="))
		if arg.begins_with("--tag="): tag=arg.trim_prefix("--tag=")
		if arg.begins_with("--seconds="): seconds=int(arg.trim_prefix("--seconds="))
	call_deferred("run")
func check(ok: bool, message: String):
	if not ok: failures+=1;push_error(message)
func record(kind: String, data: Dictionary={}):
	data.kind=kind;data.cycle=game.cycle;data.resources=game.resources.duplicate();data.rooms=game.placed_rooms.size();data.wall_ms=Time.get_ticks_msec()
	events.append(data)
	FileAccess.open(out+"events.json",FileAccess.WRITE).store_string(JSON.stringify(events,"  "))
func screenshot(label: String):
	game._fit_station_view(false)
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png(out+label+".png")
func observe_frame():
	if game.paused or not game.running: return
	measured_frames+=1
	for system in ["crew","drones_wrecks","cryo","airlocks","interface","station_total"]:
		frame_totals[system]=float(frame_totals.get(system,0.0))+float(game.frame_timing_usec.get(system,0))
	var elapsed: int=game.frame_timing_usec.get("station_total",0)
	if slowest_frames.size()<10 or elapsed>int(slowest_frames.back().usec):
		var actors: Array=[]
		for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:
			if actor.active: actors.append({"cell":str(actor.cell_at(actor.foot)),"activity":actor.activity,"medium":actor.movement_medium})
		slowest_frames.append({"usec":elapsed,"cycle":game.cycle,"systems":game.frame_timing_usec.duplicate(),"actors":actors})
		slowest_frames.sort_custom(func(a,b):return a.usec>b.usec)
		if slowest_frames.size()>10: slowest_frames.resize(10)
func salvage_reserve() -> int:
	if not all_crew or not has_recovered_guest() or game.drone_fleet.has_worker("salvage",game.placed_rooms): return 0
	if not game.meta.unlocked_room_ids.has("salvage_drone_bay"): return 0
	var mining_loads := 0
	var has_scrap := false
	for site in game.drone_fleet.sites.values():
		if not site.discovered or not site.active: continue
		if site.kind=="mining": mining_loads+=int(site.units)
		elif site.kind=="salvage" and site.units>0: has_scrap=true
	if not has_scrap or mining_loads>3: return 0
	for cell in game.wrecks:
		var rock: Dictionary=game.wrecks[cell]
		if rock.kind=="basalt" and not rock.cleared and game.surveyed_water.has(cell) and game.WreckField.reachable(game.occupied,cell,game.wrecks): return 0
	return int(game.RoomDatabaseScript.get_room("salvage_drone_bay").cost.get("metal",0))
func has_recovered_guest() -> bool:
	return game.recovered_crew.any(func(member):return member.get("architect_id","")!=game.architect_run.selected)
func keep_support_card(id: String, net: Dictionary) -> bool:
	return (id=="life_support" and int(net.get("oxygen",0))<1) or (id=="hydroponics_bay" and int(net.get("food",0))<2) or (id in ["solar_array","current_turbine","reactor"] and (game.power_blackout or int(game.resources.power)<4))
func planned_reactor_cell() -> Vector2i:
	# Use a recipe this profile actually learned; never inspect hidden recipes.
	if not all_crew or not game.meta.discovered_synergy_ids.has("industrial_heat_capture") or int(game.resources.rare_minerals)<1: return Vector2i(-1,-1)
	if game.placed_rooms.any(func(room):return room.id=="reactor"): return Vector2i(-1,-1)
	var options: Array=[]
	for room in game.placed_rooms:
		if room.id!="mining_drone_bay": continue
		for offset in Generator.DIRECTIONS:
			var cell: Vector2i=room.pos+offset
			if not Route.buildable(cell,game.occupied,game.wrecks,game.drone_fleet.sites): continue
			if not game._doors_connect("reactor",0,room.pos-cell,room): continue
			if game.placed_rooms.any(func(other):return other.id=="current_turbine" and game._turbine_intake_cell(other)==cell): continue
			for direction in Generator.DIRECTIONS:
				if game.occupied.has(cell+direction) and game._doors_connect("reactor",0,direction,game.occupied[cell+direction]):
					options.append(cell);break
	options.sort_custom(func(a,b):return Generator.distance(a)<Generator.distance(b) if Generator.distance(a)!=Generator.distance(b) else (a.x<b.x if a.x!=b.x else a.y<b.y))
	return options[0] if not options.is_empty() else Vector2i(-1,-1)
func choose_build(now: int):
	if game.paused or not game.running or not game.drone_fleet.orders.is_empty(): return
	var oxygen_ready: bool=game.placed_rooms.any(func(room):return room.id=="life_support") or game.placed_rooms.filter(func(room):return room.id=="hydroponics_bay").size()>=2
	var power_ready: bool=game.placed_rooms.any(func(room):return room.id=="reactor" or (room.id=="current_turbine" and game._turbine_intake_clear(room))) or game.placed_rooms.filter(func(room):return room.id=="solar_array").size()>=2
	var metal_reserve := salvage_reserve()
	# Repair only through the normal paid interaction once a surveyed ward is connected.
	for cell in game.site_layout.recovery_cells:
		var ward: Dictionary=game.wrecks[cell]
		if ward.kind in ["cryo","charging"] and not ward.cleared:
			if not ward.active and int(game.resources.metal)-8<metal_reserve: continue
			if all_crew and not ward.active and (not oxygen_ready or not power_ready): continue
			if game.CryoRecovery.repair_blocker(game,cell,"cryo_chamber",int(ward.rotation),8).is_empty():
				if not ward.active: game._toggle_wreck_work(cell);record("repair",{"cell":str(cell)})
				return
	# Finite deposits run out. Use surveyed, reachable rock through the normal mining rig.
	if all_crew and power_ready and int(game.resources.power)>=4 and int(game.resources.metal)<8 and game.drone_fleet.has_worker("mining",game.placed_rooms):
		for at in game.wrecks:
			if game.wrecks[at].active: return
		var rocks: Array=[]
		for at in game.wrecks:
			if game.wrecks[at].kind=="basalt" and not game.wrecks[at].cleared and game.surveyed_water.has(at) and game.WreckField.reachable(game.occupied,at,game.wrecks): rocks.append(at)
		rocks.sort_custom(func(a,b):return Generator.distance(a)<Generator.distance(b))
		if not rocks.is_empty():
			game._toggle_wreck_work(rocks[0])
			if game.wrecks[rocks[0]].active:
				record("excavate",{"cell":str(rocks[0])});return
	var ward_cell: Vector2i=game.site_layout.recovery_cells[0]
	var needs_route := false
	var pending_rescues := 0
	for cell in game.site_layout.recovery_cells:
		var ward: Dictionary=game.wrecks[cell]
		if not ward.cleared: needs_route=true
		if ward.kind=="recovery": pending_rescues+=1
		else:
			for pod in ward.pods:
				if not pod.recovered: pending_rescues+=1
	var needs_berths: bool=game._get_crew_capacity()-game.crew_count<pending_rescues
	if all_crew:
		for cell in game.site_layout.recovery_cells:
			if not game.wrecks[cell].cleared:
				ward_cell=cell;break
	var route_occupied: Dictionary=game.occupied.duplicate()
	var reactor_cell:=planned_reactor_cell()
	if reactor_cell!=Vector2i(-1,-1): route_occupied[reactor_cell]=true
	for room in game.placed_rooms:
		if room.id=="current_turbine": route_occupied[game._turbine_intake_cell(room)]=true
	var distances := Route.distances(ward_cell,route_occupied,game.wrecks,game.drone_fleet.sites)
	var connected := false
	for offset in [Vector2i.UP,Vector2i.DOWN]:
		if game.occupied.has(ward_cell+offset) and game._doors_connect("cryo_chamber",0,offset,game.occupied[ward_cell+offset]): connected=true
	connected=connected and not game.wrecks[ward_cell].cleared
	var counts := {}
	for room in game.placed_rooms: counts[room.id]=int(counts.get(room.id,0))+1
	var candidates: Array=[]
	for room in game.placed_rooms:
		for d in Generator.DIRECTIONS:
			var cell: Vector2i=room.pos+d
			if not Route.buildable(cell,route_occupied,game.wrecks,game.drone_fleet.sites): continue
			if not game._room_doors(room.id,int(room.get("rotation",0))).has(game._side_from_offset(d)): continue
			if not candidates.has(cell): candidates.append(cell)
	candidates.sort_custom(func(a,b): return int(distances.get(a,10000))<int(distances.get(b,10000)))
	var best_distance: int=int(distances.get(candidates[0],10000)) if not candidates.is_empty() else 10000
	var net: Dictionary=game._project_cycle_delta(game._simulate_room_economy(true,game.cycle+1))
	var priorities: Array=["solar_array","mining_drone_bay","hydroponics_bay","current_turbine","life_support","corridor","crew_hab","salvage_drone_bay","storage_bay"]
	if all_crew:
		priorities.append_array(["corner","tee_corridor","reactor"])
		if int(game.resources.water)>=8 and int(game.resources.biomass)>=4:
			priorities.push_front("galley")
		if needs_berths:
			priorities.erase("crew_hab");priorities.push_front("crew_hab")
		if not game.drone_fleet.has_worker("salvage",game.placed_rooms):
			priorities.erase("salvage_drone_bay");priorities.push_front("salvage_drone_bay")
	for id in priorities:
		if not game.hand.has(id): continue
		# A Hab adds a resident immediately; budget food for them and the next rescue.
		if all_crew and id=="crew_hab" and (not needs_berths or int(net.get("food",0))<2 or int(game.resources.food)<8): continue
		if all_crew and id=="galley" and int(net.get("food",0))>=2: continue
		var limit := 2 if id in ["solar_array","hydroponics_bay"] else 5 if id=="corridor" else 1
		if all_crew and has_recovered_guest():
			limit=12 if id in ["corridor","corner","tee_corridor"] else 4 if id in ["solar_array","hydroponics_bay","life_support"] else 2
		if all_crew and id in ["mining_drone_bay","salvage_drone_bay"]: limit=1
		if int(counts.get(id,0))>=limit: continue
		if id!="salvage_drone_bay" and int(game.resources.metal)-int(game.RoomDatabaseScript.get_room(id).cost.get("metal",0))<metal_reserve: continue
		# Keep a ward's eight-Metal repair reserve once its approach is already built.
		if connected and id not in ["solar_array","current_turbine","reactor"] and not (all_crew and ((id=="life_support" and not oxygen_ready) or (id=="salvage_drone_bay" and metal_reserve>0))): continue
		game._on_card_pressed(id)
		var building_candidates: Array=candidates.duplicate()
		if id=="reactor" and reactor_cell!=Vector2i(-1,-1): building_candidates.push_front(reactor_cell)
		for cell in building_candidates:
			var rotations: Array=[0,1,2,3]
			if all_crew:
				rotations.sort_custom(func(a,b):return exit_distance(id,cell,a,distances)<exit_distance(id,cell,b,distances))
			for q in rotations:
				game.selected_rotation=q
				if not game.get_placement_problem(id,cell).is_empty(): continue
				if all_crew and cell!=reactor_cell and needs_route and not connected and int(distances.get(cell,10000))==best_distance:
					var exits: Array=[]
					for direction in Generator.DIRECTIONS:
						if game._room_doors(id,q).has(game._side_from_offset(direction)): exits.append(direction)
					if not Route.preserves_route(cell,exits,distances): continue
				if Generator.distance(cell,ward_cell)==1 and not game._doors_connect("cryo_chamber",0,cell-ward_cell,{"id":id,"rotation":q}): continue
				if id=="current_turbine" and not game._turbine_intake_problem({"pos":cell,"rotation":q}).is_empty(): continue
				if id=="current_turbine" and game._turbine_intake_cell({"pos":cell,"rotation":q})==reactor_cell: continue
				game._on_grid_clicked(cell)
				record("build",{"id":id,"cell":str(cell),"rotation":q})
				game.selected_card_id="";game.hovered_card_id=""
				return
	game.selected_card_id="";game.hovered_card_id=""
	if all_crew:
		# Waiting for the repair reserve is not a reason to discard usable support.
		if connected and int(game.resources.metal)<8 and metal_reserve==0: return
	if now-last_reroll>=(6 if all_crew else 25) and game.rerolls_remaining>0:
		# Use the normal full-hand control when there is no food/berth card to retain.
		if all_crew and not game.hand.any(func(id):return id in ["hydroponics_bay","crew_hab","galley"] or keep_support_card(id,net)):
			var previous: Array=game.hand.duplicate()
			game._discard_all_cards();last_reroll=now;record("reroll_hand",{"cards":previous});return
		# Normal per-card reroll control, including its price and recovery rules.
		var retained_hab := false
		for id in game.hand:
			if all_crew and keep_support_card(id,net): continue
			# A Hab adds one resident and two berths: reserve its net spare berth
			# for a pending rescue while other cards establish the food budget.
			if all_crew and id=="crew_hab" and needs_berths and not retained_hab:
				retained_hab=true;continue
			# With no bay able to harvest, an unaffordable card can never be built: holding it froze
			# the seed-101 review run from cycle 29 to 173 (Sept 26). Reroll toward a cheap route.
			var stranded: bool=int(game.RoomDatabaseScript.get_room(id).cost.get("metal",0))>int(game.resources.metal) and not metal_income()
			if stranded or int(counts.get(id,0))>=1 or id not in priorities or (all_crew and id=="crew_hab" and int(net.get("food",0))<2):
				game._on_card_pressed(id);game._discard_selected_card();last_reroll=now;record("reroll",{"id":id});return
func metal_income() -> bool:
	for room in game.placed_rooms:
		if room.id in ["mining_drone_bay","salvage_drone_bay"] and str(game.drone_fleet.harvest_route_plan(room.pos,game.wrecks).get("state",""))=="open": return true
	return false
func exit_distance(id: String, cell: Vector2i, rotation: int, distances: Dictionary) -> int:
	var nearest:=10000
	for direction in Generator.DIRECTIONS:
		var next: Vector2i=cell+direction
		if game.occupied.has(next): continue
		if game._room_doors(id,rotation).has(game._side_from_offset(direction)):
			nearest=mini(nearest,int(distances.get(next,10000)))
	return nearest
func restore_checkpoint():
	game._set_paused(true,false)
	check(Save.write(game,game.run_save_path)==OK,"paid checkpoint writes")
	var saved:=Save.read(game.run_save_path)
	check(not saved.is_empty(),"paid checkpoint reads")
	if saved.is_empty(): return
	var profile: String=game.meta.save_path
	var path: String=game.run_save_path
	game.free()
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path=profile;game.run_save_path=path
	Save.pending=saved
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	check(game.wrecks==saved.wrecks and game.site_layout==saved.site_layout and game.resources==saved.state.resources,"paid Continue preserves map and resources")
	game.Preferences.pause_unfocused=false
	game._set_time_speed(2)
	game._set_paused(false,false)
	record("continued")
func run():
	out="res://output/procedural-sites-2026-09-23/expedition-%d%s/"%[seed_value,tag]
	DirAccess.make_dir_recursive_absolute(out)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://procedural_paid_%d_%d.meta"%[seed_value,OS.get_process_id()]
	if not profile_path.is_empty(): game.meta.save_path=profile_path
	game.run_save_path=game.meta.save_path+".loop"
	var resumed: Dictionary={}
	if not resume_path.is_empty():
		resumed=Save.read(resume_path)
		if resumed.is_empty() or profile_path.is_empty():
			push_error("Resume requires a valid checkpoint and its isolated profile");quit(1);return
		Save.pending=resumed
	game.set_meta("site_seed",seed_value)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game.Preferences.pause_unfocused=false
	game._set_time_speed(2)
	check(not game.testing_free_build and not game.testing_disable_failures,"paid rules enabled")
	record("start",{"seed":seed_value,"speed":4,"resume":resume_path,"recovery_cells":str(game.site_layout.recovery_cells)})
	if not resumed.is_empty():
		check(game.wrecks==resumed.wrecks and game.site_layout==resumed.site_layout and game.resources==resumed.state.resources,"resumed paid evidence preserves map and resources")
		restored=true
		for member in game.recovered_crew:
			var character_id: String=member.get("architect_id","")
			if character_id in ["veld","branforth","marsh"]: recorded_rescues.append(character_id)
		recovered=recorded_rescues.has("veld")
		record("continued",{"prior_rescues":recorded_rescues.duplicate()})
	var start:=Time.get_ticks_msec()
	var last_second := -1
	while game.running and Time.get_ticks_msec()-start<seconds*1000:
		await process_frame
		observe_frame()
		if watch_recharge:
			if game.marsh_npc.recharge_docked and not saw_charging:
				saw_charging=true;record("charging",{"battery":game.marsh_npc.battery})
			if saw_charging and not saw_charge_complete and not game.marsh_npc.returning_to_pod and game.marsh_npc.battery>=99.9:
				saw_charge_complete=true;record("charge_complete",{"battery":game.marsh_npc.battery})
		var now:=int((Time.get_ticks_msec()-start)/1000)
		if now==last_second: continue
		last_second=now
		if game.crew_comms.panel.visible: game.crew_comms.advance()
		elif game.paused: game._set_paused(false,false)
		if now%3==0 and not watch_recharge: choose_build(now)
		if now%30==0: record("state",{"paused":game.paused,"hand":game.hand.duplicate(),"crew":game.crew_count,"orders":str(game.drone_fleet.orders)})
		if now%90==0: await screenshot("view-%03d"%now)
		if not restored and now>=90:
			await restore_checkpoint();restored=true
		if not recovered and game.recovered_crew.any(func(member):return member.get("architect_id","")=="veld"):
			recovered=true;record("first_rescue");await screenshot("first-rescue")
			if now>100 and not all_crew: break
		if all_crew:
			for member in game.recovered_crew:
				var character_id: String=member.get("architect_id","")
				if character_id in ["veld","branforth","marsh"] and not recorded_rescues.has(character_id):
					recorded_rescues.append(character_id);record("rescue",{"character":character_id})
					check(Save.write(game,out+"latest.loop")==OK,"rescue evidence checkpoint writes")
					await screenshot("rescue-"+character_id)
			if recorded_rescues.size()==3 and restored: break
		elif recovered and restored and now>100: break
	if all_crew:
		if game.running: check(Save.write(game,out+"final.loop")==OK,"final evidence checkpoint writes")
		record("extended_result",{"rescues":recorded_rescues,"crew":game.crew_count,"capacity":game._get_crew_capacity(),"wards":game.site_layout.recovery_cells.map(func(cell):return {"cell":str(cell),"ward":game.wrecks[cell],"status":game.CryoRecovery.status(game,cell) if game.wrecks[cell].kind in ["cryo","charging"] else "UNIDENTIFIED"})})
		check(recorded_rescues.size()==3,"all three recoveries reached under normal costs")
	check(game.running,"paid expedition survives")
	check(restored,"Continue exercised")
	var any_recovered: bool=has_recovered_guest() if all_crew else recovered
	check(any_recovered,"first recovery reached under normal costs")
	if watch_recharge:
		check(saw_charging and saw_charge_complete,"saved Marsh walks home and completes a normal powered recharge")
	# Retain the actual active profile beside the active loop before conclusion awards.
	var active_profile:=FileAccess.get_file_as_string(game.meta.save_path)
	check(not active_profile.is_empty(),"active profile available for evidence")
	if not active_profile.is_empty(): FileAccess.open(out+"active.meta",FileAccess.WRITE).store_string(active_profile)
	var means: Dictionary={}
	for system in frame_totals: means[system]=float(frame_totals[system])/maxi(1,measured_frames)/1000.0
	FileAccess.open(out+"frame-profile.json",FileAccess.WRITE).store_string(JSON.stringify({"frames":measured_frames,"mean_ms":means,"slowest":slowest_frames,"scope":"Main controller timings sampled during native real-clock play; excludes draw/GPU time."},"  "))
	if game.running: game._end_expedition()
	check(game.summary_layer.visible,"explicit conclusion")
	await screenshot("conclusion")
	record("end",{"recovered":any_recovered,"veld_recovered":recovered,"failures":failures,"free_build":game.testing_free_build,"disabled_failures":game.testing_disable_failures})
	print("PROCEDURAL PAID: seed=",seed_value," failures=",failures," recovered=",any_recovered," rescues=",recorded_rescues," cycle=",game.cycle)
	quit(0 if failures==0 else 1)
