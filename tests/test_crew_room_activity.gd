extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	var desk={"id":"library/tileset-srb2-35","rect":Rect2(-174,42,101.2,100.1)}
	var desk_data={"activity_room":"life_support","props":[desk]}
	var desk_station: Dictionary=Activity.stations(desk_data)[0]
	assert(desk_station.facing=="north" and desk_station.mode=="console","Use keyboard side and standing console action")
	assert(desk_station.point.distance_to(Vector2(-123.4,158.1))<0.01,"Desk contact follows effective furniture rectangle")
	desk_data.blockers=[Rect2(desk_station.point-Vector2.ONE,Vector2.ONE*2)]
	# Props keep one facing through room rotation, so a blocked front is worked from
	# behind; only when both sides are obstructed is there no desk contact.
	var behind: Array=Activity.stations(desk_data)
	assert(behind.size()==1 and behind[0].facing=="south" and behind[0].point.distance_to(Vector2(-123.4,26.0))<0.01,"Blocked front falls back to the back of the desk")
	desk_data.blockers.append(Rect2(behind[0].point-Vector2.ONE,Vector2.ONE*2))
	assert(Activity.stations(desk_data).is_empty(),"Do not offer obstructed desk contact")
	desk_data.erase("blockers");desk.layout_flip=Vector2(1,-1)
	assert(Activity.stations(desk_data).is_empty(),"Unreviewed flipped desk must not inherit front contact")
	desk.layout_flip=Vector2.ONE;desk.rect=Rect2(-150,20,101.2,100.1)
	assert(Activity.stations(desk_data)[0].point.distance_to(Vector2(-99.4,136.1))<0.01,"Contact follows moved furniture without a stale cache")
	var berth={"id":"hab_berth_east","rect":Rect2(-168,-145,84,92),"collision_boxes":[[0.0,0.0,0.74,1.0],[0.74,0.0,0.26,0.51]]}
	var data={"activity_room":"crew_hab","props":[berth]}
	var fixture_bedside: Vector2=berth.rect.position+berth.rect.size*Vector2(0.95,0.67)
	assert(Activity.stations(data)[0].point.distance_to(fixture_bedside)<0.01,"Use clear fixture_bedside notch")
	data.props.append({"id":"fixture_obstruction","rect":Rect2(fixture_bedside-Vector2(5,5),Vector2(10,10))})
	assert(Activity.stations(data)[0].point==Vector2(-56,-99),"Obstructed notch retains outer approach")
	data.props.pop_back();berth.layout_flip=Vector2(-1,1)
	assert(Activity.stations(data)[0].point==Vector2(-56,-99),"Mirrored berth does not use unmirrored notch")
	var depth_view=preload("res://rooms/whole-room/crew_hab_view.gd").new()
	berth.layout_flip=Vector2.ONE;berth.sort_y=berth.rect.end.y;depth_view.props=[berth]
	assert(depth_view.actor_draw_depth(fixture_bedside,null)>berth.sort_y,"Walking crew draw in front of the short cabinet")
	assert(depth_view.actor_draw_depth(Vector2(80,-100),null)==-100,"Distant crew retain ordinary depth")
	assert(depth_view.actor_draw_depth(Vector2(-130,-80),null)==-80,"Bed interior does not inherit notch depth")
	berth.layout_flip=Vector2(-1,1)
	assert(depth_view.actor_draw_depth(fixture_bedside,null)==fixture_bedside.y,"Mirrored art retains its existing depth")
	depth_view.free()
	preload("res://scripts/room_layout_store.gd").path="res://output/crew-activity/no-owner.json"
	DirAccess.make_dir_recursive_absolute("res://output/crew-activity")
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://crew-activity-test.loop"; game.meta.save_path="user://crew-activity-test.meta"
	root.add_child(game); current_scene=game
	await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.bill_npc.active=false; game.veld_npc.active=false; game.branforth_npc.active=false
	var count:=0
	for id in ["life_support"]+Activity.ROOMS:
		var selected_room: String=""
		for arg in OS.get_cmdline_user_args():
			if arg.begins_with("--room="):selected_room=arg.trim_prefix("--room=")
		if not selected_room.is_empty() and id!=selected_room:continue
		for q in range(4):
			game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
			game.selected_rotation=q
			game._place_room(id,Vector2i(20,20),true)
			game.occupied[Vector2i(20,20)].rotation=q
			game.powered_room_cells[Vector2i(20,20)]=true
			for script in ["bill","veld","branforth"]:
				game.powered_room_cells[Vector2i(20,20)]=true
				var npc=load("res://scripts/"+script+"_npc.gd").new()
				npc.decision_rng=RandomNumberGenerator.new(); npc.decision_rng.seed=77321
				npc.rebuild(game); npc.active=true
				var cell:=Vector2i(20,20)
				assert(npc.room_nodes.has(cell))
				if id=="crew_hab":
					for prop in npc.geometry[cell].props:
						if prop.id!="hab_berth_east":continue
						var origin: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384+prop.rect.position
						assert(not npc.can_stand(origin+prop.rect.size*Vector2(0.4,0.8)),"Berth mattress stays solid")
						assert(not npc.can_stand(origin+prop.rect.size*Vector2(0.86,0.25)),"Bedside cabinet stays solid")
						assert(npc.can_stand(origin+prop.rect.size*Vector2(0.99,0.85)),"Empty bedside notch remains walkable")
				var stations:=Activity.stations(npc.geometry[cell]); assert(not stations.is_empty())
				if id=="crew_hab":
					for prop in npc.geometry[cell].props:
						if prop.id=="hab_berth_east" and prop.get("layout_flip",Vector2.ONE)==Vector2.ONE:
							var bedside: Vector2=prop.rect.position+prop.rect.size*Vector2(0.95,0.67)
							assert(stations.any(func(s):return s.point.distance_to(bedside)<0.01),"Sleep uses the close clear bedside approach")
				var target: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384+stations[0].point
				var nodes: Array=npc.room_nodes[cell].duplicate()
				nodes.sort_custom(func(a,b): return npc.graph.get_point_position(a).distance_squared_to(target)>npc.graph.get_point_position(b).distance_squared_to(target))
				var entry_point: Vector2=(Vector2(cell)+Vector2.ONE*0.5)*384
				for side in range(4):
					if npc.Geometry.has_port(npc.geometry[cell].layout[0],side):
						entry_point+=Vector2(npc.Geometry.DIRS[side])*140; break
				npc.foot=npc.graph.get_point_position(npc.nearest_in_room(entry_point,cell))
				for need in npc.needs: npc.needs[need]=0.0
				var need: String="fatigue" if id=="crew_hab" else "maintenance"
				npc.needs[need]=100.0; npc.service_preferences[need]=[id]
				npc.choose_goal(game)
				assert(npc.goal==need,"Must choose authored station "+id+str(q)+script)
				for step in range(1000):
					if npc.path.is_empty(): break
					npc.move(0.1)
				assert(npc.path.is_empty(),"Approach must complete")
				if stations[0].get("exact_approach",false):
					assert(npc.foot.distance_to(target)<0.01,"Bed contact reaches exact entry before sitting")
				npc.arrive()
				assert(npc.direction==stations[0].facing,"Face actual operator side")
				assert(npc.activity in ["checking life support readings","checking manifold gauges","monitoring sonar returns","resting in the berth"],npc.activity)
				assert(npc.valid_snapshot(npc.snapshot()),"Activity remains save-compatible")
				if id=="life_support":
					var console_saved: Dictionary=npc.snapshot()
					var old_contact: Vector2=console_saved.foot+Vector2(20,0)
					assert(npc.can_stand(old_contact),"Stale-contact fixture remains safe floor")
					var stale: Dictionary=console_saved.duplicate(true)
					stale.foot=old_contact
					assert(npc.valid_snapshot(stale),"Old contact remains structurally valid save data")
					npc.restore_snapshot(game,stale)
					if npc.state=="interact":
						push_error("Restored console work at stale furniture contact");quit(1);return
					assert(npc.active and npc.foot==old_contact and npc.goal.is_empty() and npc.timer==0,"Cancel stale work without teleporting or deactivating crew")
					assert(npc.needs==stale.needs,"Stale work gives no need benefit")
					npc.restore_snapshot(game,console_saved)
					assert(npc.state=="interact" and npc.timer==console_saved.timer,"Current console contact still restores")
				if script=="bill" and DisplayServer.get_name()!="headless":
					game.bill_npc=npc
					game._refresh_all()
					game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.52)
					for settle in range(4): await process_frame
					game.inspector_focus_button.set_meta("cell",cell); game._focus_inspected_room()
					game.grid_view.queue_redraw()
					for settle in range(4): await process_frame
					await RenderingServer.frame_post_draw
					root.get_texture().get_image().save_png("res://output/crew-activity/%s-q%d.png"%[id,q])
				if script=="bill" and q==0:
					var saved: Dictionary=npc.snapshot()
					var file:=FileAccess.open("res://output/crew-activity/checkpoint.bin",FileAccess.WRITE)
					file.store_var(saved); file.close()
					file=FileAccess.open("res://output/crew-activity/checkpoint.bin",FileAccess.READ)
					var decoded: Dictionary=file.get_var(); file.close()
					npc.restore_snapshot(game,decoded)
					assert(npc.activity==saved.activity and npc.direction==saved.direction and npc.timer==saved.timer,"Disk restores action")
					if npc.stage=="life_lie":
						npc.timer=0.1; npc.update(game,0.2)
						assert(npc.stage=="life_sleep","Berth settles before sleeping")
						npc.timer=0.1; npc.update(game,0.2)
						assert(npc.stage=="life_get_up","Crew rises before leaving berth")
					npc.timer=0.1; npc.update(game,0.2)
					if id=="life_support":
						assert(npc.needs.maintenance<saved.needs.maintenance,"Console work satisfies maintenance")
					else:
						assert(npc.completed_activity.get("activity","")==saved.activity,"Natural completion emits comms event")
					var serial: int=npc.completed_activity.get("serial",0)
					npc.restore_snapshot(game,decoded)
					game.powered_room_cells.erase(cell)
					npc.update(game,0.25)
					assert(npc.goal!=need,"Unavailable service interrupts action")
					assert(npc.completed_activity.get("serial",0)==serial,"Interruption emits no completion")
					game.powered_room_cells[cell]=true
					if id=="life_support":
						var curious: Dictionary=decoded.duplicate(true)
						curious.goal="curiosity"
						npc.restore_snapshot(game,curious)
						game.powered_room_cells.erase(cell)
						npc.update(game,0.25)
						if npc.state=="interact" and npc.activity=="checking life support readings":
							push_error("Curiosity console visit ignored power loss");quit(1);return
						assert(npc.needs.curiosity>=curious.needs.curiosity,"Interrupted curiosity receives no service reward")
						game.powered_room_cells[cell]=true
				count+=1
	print("CREW ACTIVITY PASS: ",count," room/rotation/actor approaches, facing and save validation")
	quit()

