extends SceneTree
const Activity=preload("res://scripts/crew_room_activity.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	preload("res://scripts/room_layout_store.gd").path="res://output/crew-activity/no-owner.json"
	DirAccess.make_dir_recursive_absolute("res://output/crew-activity")
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://crew-activity-test.loop"; game.meta.save_path="user://crew-activity-test.meta"
	root.add_child(game); current_scene=game
	await process_frame
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.bill_npc.active=false; game.veld_npc.active=false; game.branforth_npc.active=false
	var count:=0
	for id in Activity.ROOMS:
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
				var stations:=Activity.stations(npc.geometry[cell]); assert(not stations.is_empty())
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
				npc.arrive()
				assert(npc.direction==stations[0].facing,"Face actual operator side")
				assert(npc.activity in ["checking manifold gauges","monitoring sonar returns","resting in the berth"],npc.activity)
				assert(npc.valid_snapshot(npc.snapshot()),"Activity remains save-compatible")
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
					assert(npc.completed_activity.get("activity","")==saved.activity,"Natural completion emits comms event")
					var serial: int=npc.completed_activity.serial
					npc.restore_snapshot(game,decoded)
					game.powered_room_cells.erase(cell)
					npc.update(game,0.25)
					assert(npc.goal!=need,"Unavailable service interrupts action")
					assert(npc.completed_activity.serial==serial,"Interruption emits no completion")
					game.powered_room_cells[cell]=true
				count+=1
	print("CREW ACTIVITY PASS: ",count," room/rotation/actor approaches, facing and save validation")
	quit()

