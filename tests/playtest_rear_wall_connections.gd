extends "res://tests/playtest_nursery_art.gd"
const Study = preload("res://tools/capture_rear_wall_study.gd")
const NPC = preload("res://scripts/bill_npc.gd")

func evidence_subject() -> String: return "rear_wall_connections_proposal"
func capture_mixed_neighbors() -> void: pass

func capture(name: String) -> void:
	for room in game.placed_rooms:
		var view=game.grid_view._bill_room_view(room)
		if view is Study.MiningStudy or view is Study.SalvageStudy:
			view.study_light_level=game.grid_view._room_light_level(room)
	await super.capture(name)

func verify_motion_and_routes() -> void:
	# Swap only fixture-owned view instances; use the production station compositor.
	var mining=Study.MiningStudy.new()
	var salvage=Study.SalvageStudy.new()
	for view in [mining,salvage]:
		view.embedded=true
		view.hide()
		game.grid_view.add_child(view)
	game.grid_view.mining_view.free()
	game.grid_view.salvage_view.free()
	game.grid_view.mining_view=mining
	game.grid_view.salvage_view=salvage
	var south:=Vector2i(20,20)
	var north:=Vector2i(20,19)
	var seam: Vector2=Vector2(20.5*384,20*384)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.unpowered_room_cells.clear()
	game._place_room("mining_drone_bay",south,true)
	game._place_room("salvage_drone_bay",north,true)
	game.powered_room_cells[south]=true
	game.powered_room_cells[north]=true
	game.veld_npc.active=false
	game.branforth_npc.active=false
	game.bill_npc=NPC.new()
	game.bill_npc.active=true
	game.test_walker_cell=south
	game.hover_cell=south
	var poses: Array=[
		{"id":"rear-wall","offset":Vector2(-111,25)},
		{"id":"approach","offset":Vector2(0,78)},
		{"id":"threshold","offset":Vector2.ZERO},
		{"id":"north-side","offset":Vector2(0,-50)},
		{"id":"clear-north","offset":Vector2(0,-130)}]
	var records: Array=[]
	for q in [0,2]:
		game.occupied[south].rotation=q
		game.occupied[north].rotation=q
		game.bill_npc.rebuild(game)
		expect(game._connected_neighbor_cells(south).has(north),"Study has reciprocal north/south connection")
		game.bill_npc.foot=seam+Vector2(0,78)
		game._refresh_all()
		game._fit_station_view()
		var mode_pixels: Dictionary={}
		for mode in ["baseline","all-raised","exterior-only"]:
			mining.wall_rise=56.0 if mode=="all-raised" else 0.0
			salvage.wall_rise=0.0 if mode=="baseline" else 56.0
			salvage.raise_south_boundary=mode=="all-raised"
			for pose in poses:
				game.bill_npc.foot=seam+pose.offset
				game.bill_npc.direction="north"
				game.bill_npc.state="idle"
				game.test_walker_state="idle"
				expect(game.bill_npc.can_stand(game.bill_npc.foot),"Static review foot clears actual geometry: "+pose.id)
				var door_frame: int=game.grid_view._door_frame_for_pair(game,north,south)
				if pose.id=="threshold": expect(door_frame==9,"Actual door fully open at threshold")
				if pose.id in ["rear-wall","clear-north"]: expect(door_frame==0,"Actual door closed away from opening")
				var name:="q%d-%s-%s"%[q,mode,pose.id]
				await capture(name)
				if pose.id=="rear-wall": mode_pixels[mode]=root.get_texture().get_image().get_data()
				records.append({"capture":name,"quarter":q,"mode":mode,"foot":str(game.bill_npc.foot),"door_frame":door_frame})
		expect(mode_pixels.baseline!=mode_pixels["exterior-only"],"Exterior rise changes rendered pixels")
		expect(mode_pixels["all-raised"]!=mode_pixels["exterior-only"],"Raising the actual shared-wall owner changes rendered pixels")
	var report:=FileAccess.open(capture_dir.path_join("connections.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Static native station comparison with real proximity-driven door frames; not continuous crossing, adopted wall art or lighting acceptance","study_sha256":FileAccess.get_sha256("res://tools/capture_rear_wall_study.gd"),"grid_sha256":FileAccess.get_sha256("res://scripts/grid_canvas.gd"),"records":records},"\t"))
	print("REAR WALL CONNECTIONS: ",records.size()," static paired-room captures; actual door compositor; no production changes")
	if "--continuous-and-lifecycle" in OS.get_cmdline_user_args():
		await verify_crossings_and_lifecycle(south,north,seam)

func apply_exterior_study_policy(south: Vector2i,north: Vector2i) -> void:
	# Candidate rule belongs to this fixture until the owner accepts the study.
	game.grid_view.mining_view.wall_rise=0.0 if game.occupied.has(south+Vector2i.UP) else 56.0
	game.grid_view.salvage_view.wall_rise=0.0 if game.occupied.has(north+Vector2i.UP) else 56.0
	game.grid_view.salvage_view.raise_south_boundary=false

func verify_crossings_and_lifecycle(south: Vector2i,north: Vector2i,seam: Vector2) -> void:
	game.bill_npc=preload("res://tests/traced_bill_npc.gd").new()
	var npc=game.bill_npc
	npc.active=true
	var traces: Array=[]
	var ticks:=0
	for q in [0,2]:
		game.occupied[south].rotation=q
		game.occupied[north].rotation=q
		npc.rebuild(game)
		apply_exterior_study_policy(south,north)
		for direction in [1,-1]:
			var start_cell: Vector2i=south if direction==1 else north
			var end_cell: Vector2i=north if direction==1 else south
			var start: int=npc.nearest_in_room(seam+Vector2(0,128*direction),start_cell,false)
			var target: int=npc.nearest_in_room(seam-Vector2(0,128*direction),end_cell,false)
			expect(start>=0 and target>=0,"Crossing has production graph endpoints")
			if start<0 or target<0: return
			npc.foot=npc.graph.get_point_position(start)
			var endpoint: Vector2=npc.graph.get_point_position(target)
			npc.path=npc.smooth_route(npc.graph.get_point_path(start,target))
			expect(not npc.path.is_empty(),"Crossing has a real graph route")
			npc.goal="curiosity"
			npc.goal_cell=end_cell
			var steps: Array=[]
			var saw_threshold:=false
			for step in range(400):
				if npc.path.is_empty(): break
				npc.move(0.1)
				game.visual_time_seconds+=0.1
				game.test_walker_state=npc.state
				expect(npc.traveled_clear(),"Crossing swept legs clear production geometry")
				expect(npc.traveled_distance()<=4.601,"Crossing respects speed")
				var frame: int=game.grid_view._door_frame_for_pair(game,north,south)
				if npc.foot.distance_to(seam)<10:
					saw_threshold=true
					expect(frame==9,"Real door is fully open throughout threshold proximity")
				steps.append({"foot":str(npc.foot),"door_frame":frame,"distance":npc.traveled_distance()})
				ticks+=1
				if step%8==0: await capture("cross-q%d-dir%d-step%03d"%[q,direction,step])
			expect(npc.foot.is_equal_approx(endpoint) and saw_threshold,"Crew physically crossed and arrived")
			await capture("cross-q%d-dir%d-arrived"%[q,direction])
			traces.append({"quarter":q,"direction":direction,"steps":steps})
	# Fixture topology snapshots, not a claim about normal-game demolition UX.
	var lifecycle: Array=[]
	for stage in ["removed","added","removed-again"]:
		if stage=="added":
			game._place_room("salvage_drone_bay",north,true)
			game.powered_room_cells[north]=true
		else:
			for index in range(game.placed_rooms.size()-1,-1,-1):
				if game.placed_rooms[index].pos==north: game.placed_rooms.remove_at(index)
			game.occupied.erase(north)
			game.powered_room_cells.erase(north)
		apply_exterior_study_policy(south,north)
		npc.rebuild(game)
		npc.foot=seam+Vector2(-111,25)
		expect(npc.can_stand(npc.foot),"Lifecycle rear-wall foot is valid")
		game._refresh_all()
		var rise: float=game.grid_view.mining_view.wall_rise
		expect(rise==(0.0 if stage=="added" else 56.0),"Candidate boundary responds to neighbour occupancy")
		await capture("lifecycle-"+stage)
		lifecycle.append({"stage":stage,"rise":rise,"connected":game._connected_neighbor_cells(south).has(north)})
	# Exercise settled light state through the normal room-state binding.
	game.powered_room_cells.erase(south)
	game.unpowered_room_cells[south]=true
	game.grid_view.room_light_levels.erase(south)
	await capture("exterior-offline-study")
	var report:=FileAccess.open(capture_dir.path_join("crossings-lifecycle.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Scheduled single-crew production crossings and fixture topology snapshots; sparse native captures; candidate walls only","ticks":ticks,"crossings":traces,"lifecycle":lifecycle,"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd")},"\t"))
	print("REAR WALL MOTION: 4 crossings, ",ticks," swept ticks; 3 neighbour snapshots; offline study captured")
