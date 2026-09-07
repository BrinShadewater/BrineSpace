extends "res://tests/playtest_nursery_art.gd"
const TracedNPC=preload("res://tests/traced_bill_npc.gd")
func evidence_subject() -> String: return "drone_crew_circuits"
func capture_mixed_neighbors() -> void: pass
func verify_motion_and_routes() -> void:
	var prop_suffix := "hatch" if "--hatch-circuits" in OS.get_cmdline_user_args() else "rov"
	var cell:=Vector2i(20,20)
	var center: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384.0
	var records: Array=[]
	var total_steps:=0
	for kind in ["mining","salvage"]:
		for q in range(4):
			game.placed_rooms.clear()
			game.occupied.clear()
			game.powered_room_cells.clear()
			game._place_room(kind+"_drone_bay",cell,true)
			game.occupied[cell].rotation=q
			game.powered_room_cells[cell]=true
			game.test_walker_cell=cell
			game.veld_npc.active=false
			game.branforth_npc.active=false
			game.bill_npc=TracedNPC.new()
			var npc=game.bill_npc
			npc.rebuild(game)
			npc.active=true
			var view=game.grid_view.mining_view if kind=="mining" else game.grid_view.salvage_view
			view.configure_embedded(q,[],true,0.0)
			var host: Dictionary
			for prop in view.props:
				if prop.id==kind+"_"+prop_suffix: host=prop
			expect(not host.is_empty(),"Circuit subject is registered: "+kind+"_"+prop_suffix)
			if host.is_empty(): return
			var ring: Rect2=host.rect.grow(16)
			var targets: Array[int]=[]
			for point in [ring.position,Vector2(ring.end.x,ring.position.y),ring.end,Vector2(ring.position.x,ring.end.y)]:
				var id: int=npc.nearest_in_room(center+point,cell,false)
				expect(id>=0,"Cradle corner has a navigation point")
				if id<0: return
				expect(npc.graph.get_point_position(id).distance_to(center+point)<=24,"Corner route stays near cradle")
				targets.append(id)
			npc.foot=npc.graph.get_point_position(targets[0])
			game.test_walker_state="walk"
			game._refresh_all()
			game._fit_station_view()
			var trace: Array=[]
			for leg in range(1,5):
				var start: int=npc.nearest_in_room(npc.foot,cell)
				var target: int=targets[leg%4]
				var endpoint: Vector2=npc.graph.get_point_position(target)
				var route: PackedVector2Array=npc.graph.get_point_path(start,target)
				expect(not route.is_empty(),"Cradle circuit leg is connected")
				npc.path=npc.smooth_route(route)
				npc.goal="curiosity"
				npc.goal_cell=cell
				for step in range(400):
					if npc.path.is_empty(): break
					npc.move(0.1)
					game.visual_time_seconds+=0.1
					game.test_walker_state=npc.state
					expect(npc.traveled_clear(),"Cradle circuit clears swept static geometry")
					expect(npc.traveled_distance()<=4.601,"Cradle circuit respects movement speed")
					trace.append([npc.foot.x,npc.foot.y,npc.direction,npc.state])
					total_steps+=1
					if step%8==0: await capture("%s-q%d-leg%d-step%03d"%[kind,q,leg,step])
				expect(npc.foot.is_equal_approx(endpoint),"Cradle circuit physically reaches corner")
				await capture("%s-q%d-leg%d-arrived"%[kind,q,leg])
			records.append({"room":kind,"prop":prop_suffix,"quarter":q,"steps":trace})
	var file:=FileAccess.open(capture_dir.path_join("circuits.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope":"Scheduled continuous production movement around "+prop_suffix+"; single crew, sampled station frames; not autonomous choice, full-speed video or deployment safety","controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd"),"circuits":records},"\t"))
	print("DRONE ",prop_suffix.to_upper()," CIRCUITS: 8 circuits, 32 legs, ",total_steps," swept movement ticks; native frames sampled every 8 ticks")
