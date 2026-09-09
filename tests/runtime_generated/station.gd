extends "res://tests/runtime_generated/room_base.gd"
const TracedNPC=preload("res://tests/traced_bill_npc.gd")
func evidence_subject() -> String:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--review-rooms="): return "catalog_room_current_routes"
	if "--command-chair-tour" in OS.get_cmdline_user_args(): return "command_chair_current_routes"
	if "--research-services-tour" in OS.get_cmdline_user_args(): return "research_services_current_routes"
	if "--quarantine-services-tour" in OS.get_cmdline_user_args(): return "quarantine_services_current_routes"
	if "--refinery-transfer-tour" in OS.get_cmdline_user_args(): return "refinery_transfer_current_routes"
	if "--battery-group-tour" in OS.get_cmdline_user_args(): return "battery_group_current_routes"
	if "--new-room-review-tour" in OS.get_cmdline_user_args(): return "new_room_review_current_routes"
	if "--routing-detail-tour" in OS.get_cmdline_user_args(): return "routing_detail_current_routes"
	if "--thermal-group-tour" in OS.get_cmdline_user_args(): return "thermal_group_current_routes"
	if "--construction-detail-tour" in OS.get_cmdline_user_args(): return "construction_detail_current_routes"
	if "--office-group-tour" in OS.get_cmdline_user_args(): return "office_group_current_routes"
	if "--biodome-detail-tour" in OS.get_cmdline_user_args(): return "biodome_detail_current_routes"
	if "--drone-detail-tour" in OS.get_cmdline_user_args(): return "drone_detail_current_routes"
	if "--storage-tour" in OS.get_cmdline_user_args(): return "storage_current_routes"
	if "--anomaly-tour" in OS.get_cmdline_user_args(): return "anomaly_current_routes"
	if "--xeno-tour" in OS.get_cmdline_user_args(): return "xeno_current_routes"
	if "--center-tour" in OS.get_cmdline_user_args(): return "center_current_routes"
	if "--loom-tour" in OS.get_cmdline_user_args(): return "loom_current_routes"
	if "--tidal-tour" in OS.get_cmdline_user_args(): return "tidal_current_routes"
	if "--shield-tour" in OS.get_cmdline_user_args(): return "shield_current_routes"
	if "--radio-tour" in OS.get_cmdline_user_args(): return "radio_current_routes"
	if "--holo-tour" in OS.get_cmdline_user_args(): return "holo_current_routes"
	if "--bio-tour" in OS.get_cmdline_user_args(): return "bio_current_routes"
	if "--clone-tour" in OS.get_cmdline_user_args(): return "clone_current_routes"
	if "--archive-tour" in OS.get_cmdline_user_args(): return "archive_current_routes"
	if "--cryo-tour" in OS.get_cmdline_user_args(): return "cryo_current_routes"
	if "--reactor-tour" in OS.get_cmdline_user_args(): return "reactor_current_routes"
	if "--lounge-tour" in OS.get_cmdline_user_args(): return "lounge_current_routes"
	if "--hydro-tour" in OS.get_cmdline_user_args(): return "hydro_current_routes"
	if "--life-support-tour" in OS.get_cmdline_user_args(): return "life_support_current_routes"
	if "--nursery-tour" in OS.get_cmdline_user_args(): return "nursery_current_routes"
	if "--med-bay-tour" in OS.get_cmdline_user_args(): return "med_bay_current_routes"
	if "--crew-hab-tour" in OS.get_cmdline_user_args(): return "crew_hab_current_routes"
	return "research_corner_probe" if "--research-corner-probe" in OS.get_cmdline_user_args() else "production_ten_station"
func capture_mixed_neighbors() -> void: pass
func verify_motion_and_routes() -> void:
	for argument in OS.get_cmdline_user_args():
		if not argument.begins_with("--review-rooms="): continue
		var database=preload("res://scripts/room_database.gd")
		var compass: Dictionary={"north":Vector2.UP,"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT}
		for room_id in argument.trim_prefix("--review-rooms=").split(","):
			var definition: Dictionary=database.get_room(room_id)
			if definition.is_empty():
				expect(false,"Unknown review room: "+room_id)
				return
			if not database.LAYOUTS.has(definition.layout):
				expect(false,"Unknown review layout: "+str(definition.layout))
				return
			var directions: Array=[]
			for door in database.LAYOUTS[definition.layout].doors:
				if not compass.has(door):
					expect(false,"Unknown review door: "+str(door))
					return
				directions.append(compass[door])
			print("CATALOG REVIEW PORTS: ",room_id," ",database.LAYOUTS[definition.layout].doors)
			await room_current_routes(room_id,directions)
		return
	if "--command-chair-tour" in OS.get_cmdline_user_args():
		await room_current_routes("command_center",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--research-services-tour" in OS.get_cmdline_user_args():
		await room_current_routes("research_lab",[Vector2.DOWN])
		return
	if "--quarantine-services-tour" in OS.get_cmdline_user_args():
		await room_current_routes("quarantine_cell",[Vector2.LEFT,Vector2.RIGHT])
		return
	if "--refinery-transfer-tour" in OS.get_cmdline_user_args():
		await room_current_routes("ore_refinery",[Vector2.UP,Vector2.DOWN])
		return
	if "--battery-group-tour" in OS.get_cmdline_user_args():
		await room_current_routes("battery_array",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--new-room-review-tour" in OS.get_cmdline_user_args():
		await room_current_routes("airlock",[Vector2.DOWN])
		await room_current_routes("tee_corridor",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		expect(not game.grid_view.content_canvases.has(Vector2i(20,20)), "Corridor replacement releases previous airlock furniture canvas")
		return
	if "--routing-detail-tour" in OS.get_cmdline_user_args():
		await room_current_routes("corridor",[Vector2.UP,Vector2.DOWN])
		await room_current_routes("corner",[Vector2.LEFT,Vector2.DOWN])
		return
	if "--thermal-group-tour" in OS.get_cmdline_user_args():
		await room_current_routes("solar_array",[Vector2.LEFT,Vector2.DOWN])
		return
	if "--construction-detail-tour" in OS.get_cmdline_user_args():
		await room_current_routes("construction_drone_bay",[Vector2.UP,Vector2.DOWN])
		return
	if "--office-group-tour" in OS.get_cmdline_user_args():
		await room_current_routes("med_office",[Vector2.UP,Vector2.DOWN])
		return
	if "--biodome-detail-tour" in OS.get_cmdline_user_args():
		await room_current_routes("biodome",[Vector2.UP,Vector2.DOWN])
		return
	if "--drone-detail-tour" in OS.get_cmdline_user_args():
		await room_current_routes("mining_drone_bay",[Vector2.UP,Vector2.DOWN])
		await room_current_routes("salvage_drone_bay",[Vector2.UP,Vector2.DOWN])
		return
	if "--storage-tour" in OS.get_cmdline_user_args():
		await room_current_routes("storage_bay",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--anomaly-tour" in OS.get_cmdline_user_args():
		await room_current_routes("anomaly_lab",[Vector2.DOWN])
		return
	if "--xeno-tour" in OS.get_cmdline_user_args():
		await room_current_routes("xeno_lab",[Vector2.DOWN])
		return
	if "--center-tour" in OS.get_cmdline_user_args():
		await room_current_routes("med_center",[Vector2.UP,Vector2.DOWN])
		return
	if "--loom-tour" in OS.get_cmdline_user_args():
		await room_current_routes("gravity_loom",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--tidal-tour" in OS.get_cmdline_user_args():
		await room_current_routes("tidal_condenser",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--shield-tour" in OS.get_cmdline_user_args():
		await room_current_routes("shield_generator",[Vector2.UP,Vector2.DOWN])
		return
	if "--radio-tour" in OS.get_cmdline_user_args():
		await room_current_routes("radio_lab",[Vector2.LEFT,Vector2.RIGHT])
		return
	if "--holo-tour" in OS.get_cmdline_user_args():
		await room_current_routes("holographic_core",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--bio-tour" in OS.get_cmdline_user_args():
		await room_current_routes("bio_lab",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--clone-tour" in OS.get_cmdline_user_args():
		await room_current_routes("clone_lab",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--archive-tour" in OS.get_cmdline_user_args():
		await room_current_routes("data_archive",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--cryo-tour" in OS.get_cmdline_user_args():
		await room_current_routes("cryo_chamber",[Vector2.UP,Vector2.DOWN])
		return
	if "--reactor-tour" in OS.get_cmdline_user_args():
		await room_current_routes("reactor",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--lounge-tour" in OS.get_cmdline_user_args():
		await room_current_routes("crew_lounge",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--hydro-tour" in OS.get_cmdline_user_args():
		await room_current_routes("hydroponics_bay",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--life-support-tour" in OS.get_cmdline_user_args():
		await room_current_routes("life_support",[Vector2.UP,Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--nursery-tour" in OS.get_cmdline_user_args():
		await room_current_routes("mycelium_nursery",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--med-bay-tour" in OS.get_cmdline_user_args():
		await room_current_routes("med_bay",[Vector2.DOWN])
		return
	if "--crew-hab-tour" in OS.get_cmdline_user_args():
		await room_current_routes("crew_hab",[Vector2.LEFT,Vector2.RIGHT,Vector2.DOWN])
		return
	if "--research-corner-probe" in OS.get_cmdline_user_args():
		# Separate two-room geometry diagnostic, not a whole-manifest acceptance run.
		game.placed_rooms.clear()
		game.occupied.clear()
		game._place_room("battery_array",Vector2i(19,20),true)
		game._place_room("research_lab",Vector2i(19,19),true)
		game._refresh_all()
		var probe=game.BillNPC.new()
		probe.rebuild(game)
		research_corner_probe(probe)
		return
	var batch: Array=JSON.parse_string(FileAccess.get_file_as_string("res://rooms/production-ten/manifest.json"))
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--additional-manifest="):
			var extra: Variant=JSON.parse_string(FileAccess.get_file_as_string(arg.trim_prefix("--additional-manifest=")))
			assert(extra is Array and not extra.is_empty(),"Additional manifest must contain rooms")
			batch.append_array(extra)
	var identities := {}
	for entry in batch:
		expect(not identities.has(entry.id),"Duplicate station identity")
		identities[entry.id]=true
	var trunk_count := ceili(batch.size()/2.0)
	var component_count := 0
	var composition_count := 0
	for entry in batch:
		var source: String=str(entry.get("selected_source",entry.source)).replace("\\","/")
		var expected_hash: String=entry.sha256
		for revision in entry.get("revisions",[]):
			if str(revision.source).replace("\\","/")==source: expected_hash=revision.sha256
		if "--negative-source-check" in OS.get_cmdline_user_args(): expected_hash="intentional-invalid-hash"
		expect(FileAccess.get_sha256("res://"+source)==expected_hash,entry.id+": selected source hash present in build")
		for path in [source,str(entry.integration.card)]:
			var bytes := FileAccess.get_file_as_bytes("res://"+path)
			var image := Image.new()
			expect(not bytes.is_empty() and image.load_png_from_buffer(bytes)==OK,entry.id+": raw source/card PNG decodes")
		for component in entry.get("component_assets",[]):
			var path: String="res://"+str(component.path)
			expect(FileAccess.get_sha256(path)==str(component.sha256),entry.id+": component hash: "+path)
			var image := Image.new()
			expect(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,entry.id+": component decodes: "+path)
			component_count+=1
		for asset in entry.get("composition_assets",[]):
			var path: String="res://"+str(asset.path)
			var expected: String=str(asset.sha256)
			if "--negative-composition-check" in OS.get_cmdline_user_args(): expected="intentional-invalid-hash"
			expect(FileAccess.get_sha256(path)==expected,entry.id+": composition profile hash: "+path)
			var data: Variant=JSON.parse_string(FileAccess.get_file_as_string(path))
			expect(data is Dictionary and data.get("textures") is Dictionary and (data.get("furniture") is Array or data.get("wall_items") is Array),entry.id+": furniture or wall-fitting profile parses")
			composition_count+=1
	if failures>0:
		print("TEN ROOM ASSET CHECK FAILED; station checks skipped")
		return
	print("TEN ROOM ASSETS: %d selected source hashes and %d raw PNG decodes passed"%[batch.size(),batch.size()*2])
	print("ROOM COMPONENT ASSETS: %d additional hashes and PNG decodes passed"%component_count)
	print("ROOM COMPOSITION ASSETS: %d profile hashes and JSON parses passed"%composition_count)
	game.placed_rooms.clear()
	game.occupied.clear()
	for x in range(trunk_count): game._place_room("battery_array",Vector2i(18+x,20),true)
	for i in range(batch.size()):
		var entry: Dictionary=batch[i]
		var cell := Vector2i(18+i%trunk_count,19 if i<trunk_count else 21)
		game._place_room(entry.id,cell,true)
		var desired := 2 if i<trunk_count else 0
		game.occupied[cell].rotation=posmod(desired-int(entry.canonical_ports_nesw[0]),4)
	game._check_synergies()
	for key in game.resources: game.resources[key]=20
	game._apply_room_economy()
	game.hand.assign(["command_center","quarantine_cell","crew_lounge"])
	game._refresh_all()
	game._fit_station_view()
	game.test_walker_cell=Vector2i(18,20)
	game.test_walker_next_cell=Vector2i(-1,-1)
	game.test_walker_previous_cell=Vector2i(-1,-1)
	game.test_walker_state="walk"
	game.test_walker_break_timer=0.0
	game.rng.seed=77321
	if "--controlled-tour" in OS.get_cmdline_user_args():
		await controlled_tour()
		return
	# The autonomous review must satisfy the same recovery gate as normal crew.
	# Keep its unscheduled visitation check distinct from the controlled tour.
	if not game.Architects.present(game,"bill"):
		expect(game.architect_run.core.architect_id=="bill","Autonomous fixture selected Bill for recovery")
		if game.architect_run.core.architect_id!="bill": return
		var was_paused: bool=game.paused
		game.paused=false
		game.Architects.advance_core(game,game.Architects.DURATION)
		game.paused=was_paused
	game._update_test_walker(0.001)
	expect(game.Architects.present(game,"bill") and game.bill_npc.active,"Autonomous review has recovered active Bill")
	if not game.Architects.present(game,"bill") or not game.bill_npc.active: return
	print("AUTONOMOUS CREW SETUP: production recovery; graph nodes=",game.bill_npc.graph.get_point_count())
	var visited: Dictionary={game.test_walker_cell:true}
	var transitions := 0
	await capture("mixed-station-start")
	for step in range(20000):
		var before: Vector2i=game.test_walker_cell
		game._update_test_walker(0.1)
		var after: Vector2i=game.test_walker_cell
		if before!=after:
			expect(game._connected_neighbor_cells(before).has(after),"Walker transition uses a connected door")
			transitions+=1
			visited[after]=true
		if step in [4999,9999,14999,19999]:
			game.visual_time_seconds=step*0.1
			await capture("mixed-station-step-%05d"%step)
	expect(visited.size()==game.placed_rooms.size(),"Walker visits every room in connected station")
	# Retain the visitation gate while exposing whether a miss is unreachable
	# geometry or the current needs-driven controller's choice within this horizon.
	var missing: Array=[]
	var reachable_rooms: Dictionary={}
	var npc=game.bill_npc
	var start_id: int=npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot))
	var frontier: Array=[start_id] if start_id>=0 else []
	var reached: Dictionary={}
	while not frontier.is_empty():
		var node_id: int=frontier.pop_back()
		if reached.has(node_id): continue
		reached[node_id]=true
		reachable_rooms[npc.cell_at(npc.graph.get_point_position(node_id))]=true
		for connected in npc.graph.get_point_connections(node_id):
			if not reached.has(connected): frontier.append(connected)
	for cell in game.occupied:
		if not visited.has(cell): missing.append({"id":game.occupied[cell].id,"cell":[cell.x,cell.y],"graph_reachable":reachable_rooms.has(cell)})
	print("STATION COVERAGE DIAGNOSTIC: graph-reachable rooms=",reachable_rooms.size(),"; unvisited=",JSON.stringify(missing))
	var output := FileAccess.open(capture_dir.path_join("station-summary.json"),FileAccess.WRITE)
	output.store_string(JSON.stringify({"rooms":game.placed_rooms.size(),"visited":visited.size(),"transitions":transitions,"steps":20000,"delta":0.1,"zoom":game.grid_zoom/game.DEFAULT_GRID_ZOOM,"graph_reachable_rooms":reachable_rooms.size(),"unvisited":missing},"\t"))
	print("TEN ROOM MIXED STATION: %d rooms visited, %d connected transitions in 2000 simulated walker seconds"%[visited.size(),transitions])

func prepare_three_crew_review() -> void:
	# Explicit pre-repaired art fixture, not repair-cost/progression acceptance.
	var cell:=Vector2i(-1,-1)
	for candidate in game.occupied:
		if game.occupied[candidate].id=="cryo_chamber": cell=candidate; break
	expect(cell!=Vector2i(-1,-1),"Three-crew review requires a real Cryo Chamber")
	if cell==Vector2i(-1,-1): return
	# The mixed economy can already have produced a clone; add real berths rather
	# than lowering population or overriding the production capacity check.
	var hab_cell:=Vector2i(17,20)
	expect(not game.occupied.has(hab_cell),"Review berth location is free")
	if game.occupied.has(hab_cell): return
	game._place_room("crew_hab",hab_cell,true)
	game._refresh_all()
	var pods: Array=[]
	for original in game.wrecks.keys():
		if game.wrecks[original].kind=="cryo":
			pods.append_array(game.wrecks[original].pods.duplicate(true))
			game.wrecks.erase(original)
	expect(pods.size()==2,"Review retains the two seeded architect pods")
	game.wrecks[cell]={"kind":"cryo","progress":18.0,"active":false,"cleared":true,"paid":true,"rotation":game.occupied[cell].rotation,"pods":pods}
	game.occupied[cell].recovered_derelict=true
	game.powered_room_cells[cell]=true
	if "--negative-crew-thaw-power" in OS.get_cmdline_user_args(): game.powered_room_cells.erase(cell)
	var was_paused: bool=game.paused
	game.paused=false
	for unused in range(2):
		print("REVIEW THAW PRECONDITION: ",game.CryoRecovery.status(game,cell),"; crew=",game.crew_count,"/",game._get_crew_capacity(),"; food=",game.resources.food,"; oxygen=",game.resources.oxygen)
		game.CryoRecovery.advance(game,game.CryoRecovery.WAKE_SECONDS)
	game.paused=was_paused
	for id in game.Architects.IDS:
		expect(game.Architects.present(game,id) and game.Architects.actor_for(game,id).active,"Recovered review crew present: "+id)
	expect(game.recovered_crew.size()==3,"Review recovery produces exactly three roster members")
	print("THREE CREW REVIEW: pre-repaired two-pod chamber; production thaw; active=",[game.bill_npc.active,game.veld_npc.active,game.branforth_npc.active])

func tour_progress(phase: String, cell: Vector2i, step: int=-1) -> void:
	if not "--trace-tour-progress" in OS.get_cmdline_user_args(): return
	var npc=game.bill_npc
	var record:={"phase":phase,"cell":[cell.x,cell.y],"step":step,"ticks_ms":Time.get_ticks_msec(),"foot":[npc.foot.x,npc.foot.y],"path_size":npc.path.size(),"activity":npc.activity}
	var file:=FileAccess.open(capture_dir.path_join("last-tour-progress.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\t"))
	file.close()
	print("TOUR PROGRESS: ",JSON.stringify(record))

func tour_crew_trace() -> Array:
	var records: Array=[]
	for id in game.Architects.IDS:
		var actor=game.Architects.actor_for(game,id)
		var next: Vector2=actor.path[0] if not actor.path.is_empty() else actor.foot
		records.append({"id":id,"active":actor.active,"present":game.Architects.present(game,id),"foot":[actor.foot.x,actor.foot.y],"next":[next.x,next.y],"path_size":actor.path.size(),"activity":actor.activity,"goal":actor.goal,"timer":actor.timer,"traffic_wait":actor.traffic_wait,"traffic_retry":actor.traffic_retry})
	return records

func controlled_tour(return_to_start := false) -> void:
	# Explicit destination scheduling belongs only to this fixture. Use the real
	# graph, smoothing, update, movement, clearance and arrival code for every leg.
	game.bill_npc=TracedNPC.new()
	# Reproducible review only; normal crew retain independent random decisions.
	var crew_seed:=77321
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--crew-seed="): crew_seed=int(arg.trim_prefix("--crew-seed="))
	var seed_records:=[]
	for index in range(game.Architects.IDS.size()):
		var id: String=game.Architects.IDS[index]
		var actor=game.Architects.actor_for(game,id)
		if actor.decision_rng==null: actor.decision_rng=RandomNumberGenerator.new()
		actor.decision_rng.seed=crew_seed+index
		seed_records.append({"id":id,"seed":crew_seed+index})
	var seed_file:=FileAccess.open(capture_dir.path_join("crew-seeds.json"),FileAccess.WRITE)
	seed_file.store_string(JSON.stringify(seed_records,"\t"))
	seed_file.close()
	print("TOUR CREW SEEDS: ",JSON.stringify(seed_records))
	# Dedicated tour setup: complete the real emergency core wake before asking
	# the production updater to move Bill. Do not bypass architect presence gates.
	if not game.Architects.present(game,"bill"):
		expect(game.architect_run.core.architect_id=="bill","Tour fixture selected Bill for core recovery")
		if game.architect_run.core.architect_id!="bill": return
		var was_paused: bool=game.paused
		game.paused=false
		game.Architects.advance_core(game,game.Architects.DURATION)
		game.paused=was_paused
		expect(game.architect_run.core.recovered and game.Architects.present(game,"bill"),"Tour completes production core recovery")
		print("TOUR CREW SETUP: production core recovery; active crew=",[game.bill_npc.active,game.veld_npc.active,game.branforth_npc.active])
	game._update_test_walker(0.001)
	if "--three-crew-review" in OS.get_cmdline_user_args():
		prepare_three_crew_review()
		if failures>0: return
		# Added berths change topology. Let production rebuild before capturing
		# graph IDs and installing the fixture's first scheduled route.
		game._update_test_walker(0.001)
	var npc=game.bill_npc
	expect(npc.active,"Controlled tour initializes the production NPC")
	if not npc.active: return
	var destinations: Array=game.occupied.keys()
	destinations.sort_custom(func(a,b): return a.y<b.y if a.y!=b.y else a.x<b.x)
	if return_to_start: destinations.append(npc.cell_at(npc.foot))
	var visited: Dictionary={npc.cell_at(npc.foot):true}
	var legs: Array=[]
	var transitions:=0
	var samples:=0
	# Stream every peer sample as well as Bill's route, including failed runs.
	var crew_trace:=FileAccess.open(capture_dir.path_join("whole-crew-trace.jsonl"),FileAccess.WRITE)
	expect(crew_trace!=null,"Whole-crew trace opens")
	if crew_trace==null: return
	tour_progress("before start capture",npc.cell_at(npc.foot))
	await capture("controlled-tour-start")
	tour_progress("after start capture",npc.cell_at(npc.foot))
	for cell in destinations:
		tour_progress("before endpoint lookup",cell)
		var start: int=npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot))
		var target: int=npc.nearest_in_room((Vector2(cell)+Vector2.ONE*0.5)*384.0,cell,false)
		expect(start>=0 and target>=0,"Tour endpoints have navigation nodes: "+str(cell))
		if start<0 or target<0: return
		if legs.is_empty() and "--negative-tour-disconnect" in OS.get_cmdline_user_args():
			npc.graph.set_point_disabled(target,true) # Fixture-only unreachable target.
		tour_progress("before graph route",cell)
		var route: PackedVector2Array=npc.graph.get_point_path(start,target)
		expect(not route.is_empty(),"Tour graph route exists: "+str(cell))
		if route.is_empty(): return
		tour_progress("before route smoothing",cell)
		npc.path=npc.smooth_route(route)
		tour_progress("after route smoothing",cell)
		npc.goal="curiosity"
		npc.goal_cell=cell
		npc.timer=0.0
		npc.stage=""
		var endpoint: Vector2=npc.graph.get_point_position(target)
		if "--tour-occupied-target" in OS.get_cmdline_user_args() and game.occupied[cell].id=="holographic_core":
			# Deterministic diagnostic: an otherwise valid destination is occupied.
			# Only this fixture places the peer; production avoidance stays enabled.
			game.veld_npc.active=true
			game.veld_npc.foot=endpoint
			game.veld_npc.path.clear()
			game.veld_npc.goal="curiosity"
			game.veld_npc.goal_cell=cell
			game.veld_npc.timer=600.0 if "--negative-tour-occupied-target" in OS.get_cmdline_user_args() else 60.0
			game.veld_npc.state="idle"
			game.veld_npc.stage=""
		var initial_foot: Vector2=npc.foot
		var leg_samples: Array=[]
		var arrived:=false
		var traffic_replans:=0
		var diagnostic_tail: Array=[]
		var captured_near_prop:=false
		for step in range(5000):
			if step%100==0: tour_progress("before movement sample",cell,step)
			var before: Vector2=npc.foot
			var before_cell: Vector2i=npc.cell_at(before)
			var next_point: Vector2=npc.path[0] if not npc.path.is_empty() else before
			var planned_clear: bool=npc.segment_clear(before,next_point)
			var crew_before:=tour_crew_trace()
			game._update_test_walker(0.1)
			if step%100==0: tour_progress("after movement sample",cell,step)
			var after: Vector2=npc.foot
			var after_cell: Vector2i=npc.cell_at(after)
			diagnostic_tail.append({"step":step,"foot":[after.x,after.y],"before":[before.x,before.y],"next":[next_point.x,next_point.y],"planned_clear":planned_clear,"peer":[game.veld_npc.foot.x,game.veld_npc.foot.y],"peer_active":game.veld_npc.active,"activity":npc.activity,"goal":npc.goal,"path_size":npc.path.size(),"traffic_wait":npc.traffic_wait})
			if diagnostic_tail.size()>40: diagnostic_tail.pop_front()
			diagnostic_tail.back()["crew_before"]=crew_before
			diagnostic_tail.back()["crew_after"]=tour_crew_trace()
			crew_trace.store_line(JSON.stringify({"leg":legs.size(),"step":step,"crew":diagnostic_tail.back()["crew_after"]}))
			expect(before.distance_to(after)<=4.601,"Tour respects production speed; no teleport")
			expect(npc.traveled_distance()<=4.601,"Tour traveled legs respect production speed")
			var collision_clear: bool=npc.can_stand(after) and npc.traveled_clear()
			if not collision_clear:
				print("TOUR COLLISION SAMPLE: "+JSON.stringify({"target_cell":[cell.x,cell.y],"step":step,"before":[before.x,before.y],"after":[after.x,after.y],"cell":[after_cell.x,after_cell.y],"planned_clear":planned_clear,"next":[next_point.x,next_point.y]}))
				print("TOUR TRAVELED POINTS: ",npc.traveled_points)
			expect(collision_clear,"Tour foot and traveled legs clear registered collision")
			if before_cell!=after_cell:
				expect(game._connected_neighbor_cells(before_cell).has(after_cell),"Tour crosses only reciprocal doors")
				transitions+=1
			visited[after_cell]=true
			leg_samples.append([after.x,after.y])
			samples+=1
			if "--crew-visit-review" in OS.get_cmdline_user_args() and not captured_near_prop and after_cell==cell:
				var local_foot: Vector2=after-(Vector2(cell)+Vector2.ONE*0.5)*384.0
				var distance:=INF
				var prop_id:=""
				for prop in npc.geometry[cell].props:
					var blocker: Rect2=prop.rect
					var nearest: Vector2=local_foot.clamp(blocker.position,blocker.end)
					var candidate_distance:=local_foot.distance_to(nearest)
					if candidate_distance<distance:
						distance=candidate_distance
						prop_id=prop.id
				if distance<=32.0:
					await capture_crew_visit(cell,"visit-%02d-%s"%[legs.size()+1,game.occupied[cell].id],distance,"near registered prop",prop_id)
					captured_near_prop=true
			if after.is_equal_approx(endpoint) and npc.path.is_empty():
				arrived=true
				break
			if npc.path.is_empty():
				# The controlled itinerary persists; the production NPC may abandon
				# an occupied target normally. Retry only that explicit traffic case.
				if npc.activity=="waiting for passage" and traffic_replans<24:
					var retry_start: int=npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot))
					var retry_route: PackedVector2Array=npc.graph.get_point_path(retry_start,target) if retry_start>=0 else PackedVector2Array()
					if retry_route.is_empty(): break
					npc.path=npc.smooth_route(retry_route)
					npc.goal="curiosity"
					npc.goal_cell=cell
					traffic_replans+=1
					continue
				break
		expect(arrived and npc.cell_at(npc.foot)==cell,"Tour physically arrives at target: "+str(cell))
		if not arrived:
			crew_trace.flush()
			var diagnostic:={"id":game.occupied[cell].id,"cell":[cell.x,cell.y],"target":[endpoint.x,endpoint.y],"actual":[npc.foot.x,npc.foot.y],"remaining_path":str(npc.path),"tail":diagnostic_tail,"completed_legs":legs.size(),"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd")}
			var failure_file:=FileAccess.open(capture_dir.path_join("controlled-tour-failure.json"),FileAccess.WRITE)
			failure_file.store_string(JSON.stringify(diagnostic,"\t"))
			failure_file.close()
			print("CONTROLLED TOUR FAILURE: ",JSON.stringify(diagnostic))
			await capture("controlled-tour-failure")
			return
		if "--tour-occupied-target" in OS.get_cmdline_user_args() and game.occupied[cell].id=="holographic_core":
			expect(traffic_replans>0,"Occupied-target diagnostic exercises traffic rescheduling")
			print("TOUR OCCUPIED TARGET: physical arrival after ",traffic_replans," traffic replans; production avoidance retained")
		legs.append({"id":game.occupied[cell].id,"cell":[cell.x,cell.y],"rotation":game.occupied[cell].rotation,"start":[initial_foot.x,initial_foot.y],"target":[endpoint.x,endpoint.y],"samples":leg_samples,"traffic_replans":traffic_replans})
		tour_progress("before arrival capture",cell)
		await capture("tour-arrival-%02d-%s"%[legs.size(),str(game.occupied[cell].id)])
		tour_progress("after arrival capture",cell)
		if "--crew-visit-review" in OS.get_cmdline_user_args() and not captured_near_prop:
			await capture_crew_visit(cell,"visit-%02d-%s"%[legs.size(),game.occupied[cell].id],-1.0,"arrival fallback; no near-prop sample","")
	expect(visited.size()==game.placed_rooms.size() and legs.size()==destinations.size(),"Controlled tour covers every room")
	crew_trace.close()
	var trace:=FileAccess.open(capture_dir.path_join("controlled-tour-trace.json"),FileAccess.WRITE)
	trace.store_string(JSON.stringify({"mode":"controlled-tour","delta":0.1,"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd"),"legs":legs},"\t"))
	var summary:=FileAccess.open(capture_dir.path_join("station-summary.json"),FileAccess.WRITE)
	summary.store_string(JSON.stringify({"mode":"controlled-tour","rooms":game.placed_rooms.size(),"visited":visited.size(),"arrivals":legs.size(),"transitions":transitions,"steps":samples,"delta":0.1,"zoom":game.grid_zoom/game.DEFAULT_GRID_ZOOM},"\t"))
	print("CONTROLLED ROOM TOUR: %d arrivals, %d rooms visited, %d reciprocal transitions, %d collision/speed samples; scheduled destinations, production movement"%[legs.size(),visited.size(),transitions,samples])
	if "--composition-review" in OS.get_cmdline_user_args():
		await capture_composition_review()

func capture_crew_visit(cell: Vector2i,name: String,distance: float,trigger: String,prop_id: String) -> void:
	var actors: Array=[game.bill_npc,game.veld_npc,game.branforth_npc]
	var feet: Array=[]
	for actor in actors: feet.append(actor.foot)
	var zoom: float=game.grid_zoom
	var scroll:=Vector2i(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.52)
	await settle()
	game.inspector_focus_button.set_meta("cell",cell)
	game._focus_inspected_room()
	game._refresh_inspector()
	await capture(name)
	var record:=FileAccess.open(capture_dir.path_join(name+".visit.json"),FileAccess.WRITE)
	record.store_string(JSON.stringify({"scope":"Naturally reached pose; prop proximity is not rendered overlap proof","trigger":trigger,"prop_id":prop_id,"prop_distance":distance,"cell":[cell.x,cell.y],"crew_feet":feet.map(func(p): return [p.x,p.y]),"zoom":game.grid_zoom/game.DEFAULT_GRID_ZOOM},"\t"))
	game._set_grid_zoom(zoom)
	await settle()
	game.grid_scroll.scroll_horizontal=scroll.x
	game.grid_scroll.scroll_vertical=scroll.y
	await settle()
	for i in range(actors.size()): expect(actors[i].foot==feet[i],"Visit capture never advances or teleports crew")
	expect(is_equal_approx(game.grid_zoom,zoom),"Visit capture restores tour zoom")

func capture_composition_review() -> void:
	# Actual station renderer and neighbours at the normal initial zoom. This is
	# visual evidence only; no actor teleport or change to the completed tour.
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.52)
	await get_tree().process_frame
	await get_tree().process_frame
	var captured := {}
	var records: Array=[]
	for cell in game.occupied:
		var room: Dictionary=game.occupied[cell]
		if captured.has(room.id): continue
		captured[room.id]=true
		game.inspector_focus_button.set_meta("cell",cell)
		game._focus_inspected_room()
		game._refresh_inspector()
		var name:="composition-52-%s"%room.id
		await capture(name)
		records.append({"id":room.id,"cell":[cell.x,cell.y],"rotation":room.rotation,"capture":name+".png","zoom":game.grid_zoom/game.DEFAULT_GRID_ZOOM,"cell_pixels":game.get_cell_size()})
	var review:=FileAccess.open(capture_dir.path_join("composition-review.json"),FileAccess.WRITE)
	review.store_string(JSON.stringify({"scope":"Station renderer, actual neighbours and retained crew positions at initial 52 percent zoom; not autonomous activity or visual acceptance","rooms":records},"\t"))

func room_current_routes(room_id: String,directions: Array) -> void:
	var base_dir:=capture_dir
	for q in range(4):
		capture_dir=base_dir.path_join("%s-q%d"%[room_id,q])
		DirAccess.make_dir_recursive_absolute(capture_dir)
		game.placed_rooms.clear()
		game.occupied.clear()
		var center:=Vector2i(20,20)
		game._place_room(room_id,center,true)
		game.occupied[center].rotation=q
		game.test_walker_cell=center
		game.test_walker_next_cell=Vector2i(-1,-1)
		game.test_walker_previous_cell=Vector2i(-1,-1)
		for direction in directions:
			var cell:=center+Vector2i(Geometry.turn(direction,q))
			game._place_room("battery_array",cell,true)
			game.occupied[cell].rotation=q
		game._refresh_all()
		game._fit_station_view()
		await controlled_tour(true)
	capture_dir=base_dir
	print("CURRENT ROOM ROUTES: ",room_id,"; four rotated layouts and return to start, scheduled destinations with production movement; per-rotation traces retained")

func research_corner_probe(npc) -> void:
	# Diagnostic only: v22's last safe foot, plus a hypothesized graph waypoint
	# extrapolated from its final two movement samples. Not a captured old route.
	var start:=Vector2(7461.150390625,7702.0302734375)
	var target:=Vector2(7488,7504)
	var blocked: Array=[]
	var count:=ceili(start.distance_to(target)/0.1)
	for i in range(count+1):
		var point:=start.lerp(target,float(i)/count)
		if npc.can_stand(point): continue
		var cell: Vector2i=npc.cell_at(point)
		var local:=point-(Vector2(cell)+Vector2.ONE*0.5)*384.0
		var hits: Array=[]
		for rect in npc.geometry[cell].blockers:
			if rect.has_point(local): hits.append(str(rect))
		blocked.append({"point":[point.x,point.y],"cell":[cell.x,cell.y],"local":[local.x,local.y],"blockers":hits})
	var record:={"scope":"Current geometry probe; target inferred, not retained v22 waypoint","start":[start.x,start.y],"target":[target.x,target.y],"start_clear":npc.can_stand(start),"coarse_clear":npc.segment_clear(start,target),"blocked_dense_samples":blocked,"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd")}
	npc.foot=start
	npc.path=PackedVector2Array([target])
	npc.move(0.1)
	record.movement={"foot":[npc.foot.x,npc.foot.y],"activity":npc.activity,"remaining_waypoints":npc.path.size()}
	var start_id: int=npc.nearest_in_room(start,npc.cell_at(start))
	var target_id: int=npc.nearest_in_room(target,npc.cell_at(target))
	if start_id>=0 and target_id>=0:
		npc.path=npc.smooth_route(npc.graph.get_point_path(start_id,target_id))
		var route: PackedVector2Array=npc.path.duplicate()
		var steps:=0
		var clear:=true
		while not npc.path.is_empty() and steps<1000:
			var previous: Vector2=npc.foot
			npc.move(0.1)
			clear=clear and npc.can_stand(npc.foot) and npc.segment_clear(previous,npc.foot)
			steps+=1
		record.replanned={"route":str(route),"steps":steps,"clear":clear,"arrived":npc.foot.is_equal_approx(target),"activity":npc.activity}
	var file:=FileAccess.open(capture_dir.path_join("research-corner-probe.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\t"))
	print("RESEARCH CORNER PROBE: coarse_clear=",record.coarse_clear,"; dense blocked samples=",blocked.size(),"; single-step result=",JSON.stringify(record.movement),"; full evidence in research-corner-probe.json")
	print("RESEARCH CORNER REPLAN: ",JSON.stringify(record.get("replanned",{})))
