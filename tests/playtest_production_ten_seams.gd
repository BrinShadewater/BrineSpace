extends "res://tests/playtest_nursery_art.gd"
var tested_rooms: Array=[]
func evidence_subject() -> String: return "room_seams: "+str(tested_rooms)
func capture_mixed_neighbors() -> void: pass
func verify_motion_and_routes() -> void:
	var manifest_path := "res://rooms/production-ten/manifest.json"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--manifest="): manifest_path=arg.trim_prefix("--manifest=")
	var batch: Array=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
	assert(not batch.is_empty(),"Seam manifest must contain rooms")
	var pair_count := 0
	var origin := Vector2i(20,20)
	var records: Array=[]
	var crossings := "--crossings" in OS.get_cmdline_user_args()
	for entry in batch:
		tested_rooms.append(entry.id)
		for q in range(4):
			var ports: Array=entry.canonical_ports_nesw if "--all-ports" in OS.get_cmdline_user_args() else [entry.canonical_ports_nesw[0]]
			for port in ports:
				pair_count+=1
				game.placed_rooms.clear()
				game.occupied.clear()
				game._place_room(entry.id,origin,true)
				game.occupied[origin].rotation=q
				var side: int=(int(port)+q)%4
				var neighbor: Vector2i=origin+Geometry.DIRS[side]
				game._place_room("battery_array",neighbor,true)
				game._check_synergies()
				for key in game.resources: game.resources[key]=20
				game._apply_room_economy()
				game.hand.assign([entry.id,"battery_array"])
				game.test_walker_cell=origin
				game.test_walker_next_cell=neighbor
				game.test_walker_previous_cell=Vector2i(-1,-1)
				game.test_walker_state="walk"
				game.test_walker_progress=0.5
				game.visual_time_seconds=0.2
				game._refresh_all()
				game._fit_station_view()
				expect(game._connected_neighbor_cells(origin).has(neighbor),entry.id+": rendered seam connected")
				if not crossings:
					await capture(entry.id+"-p%d-q%d-seam"%[port,q])
					continue
				# Same game zoom in both orientations; retain actual native viewport pixels.
				game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.30)
				await settle()
				game._center_grid_on_station_now()
				game.bill_npc=game.BillNPC.new()
				game._update_test_walker(0.001)
				var npc=game.bill_npc
				var seam := (Vector2(origin)+Vector2.ONE*0.5)*384.0+Vector2(Geometry.DIRS[side])*192.0
				var start: int=npc.nearest_in_room(seam-Vector2(Geometry.DIRS[side])*48.0,origin,false)
				var target: int=npc.nearest_in_room(seam+Vector2(Geometry.DIRS[side])*48.0,neighbor,false)
				expect(npc.active and start>=0 and target>=0,"Crossing has valid NPC endpoints")
				if not npc.active or start<0 or target<0: return
				# Fixture-only spawn; all subsequent movement uses the production controller.
				npc.foot=npc.graph.get_point_position(start)
				npc.path=npc.smooth_route(npc.graph.get_point_path(start,target))
				npc.goal="curiosity"
				npc.goal_cell=neighbor
				npc.timer=0.0
				npc.stage=""
				var endpoint: Vector2=npc.graph.get_point_position(target)
				var length := 0.0
				var cursor: Vector2=npc.foot
				for point in npc.path:
					length+=cursor.distance_to(point)
					cursor=point
				expect(length>0,"Crossing route is nonempty")
				if length<=0: return
				var elapsed := 0.0
				for fraction in [0.0,0.25,0.45,0.5,0.55,0.75,1.0]:
					var until: float=length/46.0*fraction
					while elapsed<until and not npc.path.is_empty():
						var delta: float=minf(0.1,until-elapsed+0.000001)
						var before: Vector2=npc.foot
						game._update_test_walker(delta)
						expect(npc.can_stand(npc.foot) and npc.segment_clear(before,npc.foot),"Crossing segment stays clear")
						expect(before.distance_to(npc.foot)<=46.0*delta+0.001,"Crossing obeys production speed")
						elapsed+=delta
					game.visual_time_seconds=0.2+elapsed
					var name: String=entry.id+"-p%d-q%d-cross-%03d"%[port,q,roundi(fraction*100)]
					await capture(name)
					records.append({"file":name+".png","room":entry.id,"rotation":q,"canonical_port":port,"requested_fraction":fraction,"foot":[npc.foot.x,npc.foot.y],"controller":"bill_npc","cell":[npc.cell_at(npc.foot).x,npc.cell_at(npc.foot).y],"zoom":game.grid_zoom/game.DEFAULT_GRID_ZOOM,"viewport_width":viewport_width})
				expect(npc.path.is_empty() and npc.foot.is_equal_approx(endpoint) and npc.cell_at(npc.foot)==neighbor,entry.id+": production walker arrives")

	if crossings:
		var index := FileAccess.open(capture_dir.path_join("crossings.json"),FileAccess.WRITE)
		index.store_string(JSON.stringify(records,"\t"))
		print("ROOM CROSSINGS: %d production walker arrivals, %d frames at common 30%% zoom; visual review required"%[pair_count,records.size()])
	print("ROOM SEAM CAPTURES: %d connected pairs; visual review required"%pair_count)
