extends SceneTree
## Staged seated contact at reachable live room furniture; no autonomous route claim.
var failures:=0
var game
func _init():call_deferred("run")
func check(ok: bool, message: String):
	if not ok:failures+=1;push_error(message)
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
	if OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://branforth_seated.meta";game.run_save_path="user://branforth_seated.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var output: String="res://character/james-seated-family-v1/native-rooms/";DirAccess.make_dir_recursive_absolute(output)
	var captures:=0;var seen: Dictionary={}
	var player=game.grid_view.branforth_player
	for mode in ["bare","helmet"]:
		var manifest_path: String="res://character/james-seated-family-v1/"+mode+"-manifest.json"
		var pack: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
		var selected: Dictionary=player.frames if mode=="bare" else player.equipment_frames["diving-helmet"]
		for state in pack.states:
			check(selected.has(state.id),"Installed "+state.id)
			var elapsed:=0.0
			for i in range(state.frameFiles.size()):
				var expected_image=Image.load_from_file(ProjectSettings.globalize_path(manifest_path.get_base_dir().path_join(state.frameFiles[i]).simplify_path()))
				var frame: Texture2D=selected[state.id][i]
				check(frame.get_image().get_data()==expected_image.get_data(),"Installed pixels "+mode+state.id+str(i))
				check(frame.get_meta("crew_depth_offset")==float(state.depthOffsets[i]),"Furniture depth")
				check(frame.get_meta("crew_pivot")==Vector2(92,172),"Foot pivot")
				check(frame.get_meta("crew_standing_height")==148.0,"Standing scale")
				check(player.frame_at_elapsed(state.id,elapsed+.0001,"" if mode=="bare" else "diving-helmet").get_image().get_data()==expected_image.get_data(),"Actual action clock")
				elapsed+=float(state.frameDurationsMs[i])/1000.0
	for id in ["crew_lounge","observation_room"]:
		for sample_mode in range(2):
			var q:=0
			var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
			game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.powered_room_cells[cell]=true
			var actor=game.branforth_npc;actor.rebuild(game);actor.active=true;actor.dead=false;actor.helmet_equipped=sample_mode==1
			var stations: Array=actor.RoomActivity.stations(actor.geometry[cell]);var chosen: Dictionary={};var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
			for station in stations:
				if station.get("mode","") in ["sit","read"] and actor.can_stand(center+station.point):chosen=station;break
			check(not chosen.is_empty(),id+str(q)+" has a reachable seat")
			if chosen.is_empty():continue
			actor.foot=center+chosen.point;actor.path.clear();actor.goal="fatigue" if id=="crew_lounge" else "curiosity";actor.goal_cell=cell;actor.stage="";actor.arrive()
			check(actor.stage in ["life_sit","observation_sit"],id+str(q)+" arrival selects seating")
			game.selected_room_cell=cell;game._refresh_all();game._set_grid_zoom(.75,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))
			# Wait for the current room and camera, rather than a fixed frame delay.
			game.grid_view.queue_redraw()
			var settled:=false
			for attempt in range(120):
				await process_frame;await RenderingServer.frame_post_draw
				if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1 and game._grid_view_center_ratio().distance_to((Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))<.002:
					settled=true;break
			check(settled,id+str(q)+" room/camera settled before captures")
			var reading: bool=id=="observation_room";seen[actor.direction]=true
			for stage in (["observation_sit","observation_read","observation_rise"] if reading else ["life_sit","life_seated","life_rise"]):
				actor.stage=stage
				var key: String=actor.animation_state()+"-"+actor.direction;var row: Array=game.grid_view.branforth_player.frames[key] if sample_mode==0 else game.grid_view.branforth_player.equipment_frames["diving-helmet"][key]
				for i in range(row.size()):
					var elapsed:=0.0
					for j in range(i):elapsed+=float(game.grid_view.branforth_player.timing[key].durations[j])/1000.0
					elapsed+=.01
					actor.timer=.65-elapsed/.8*.65 if stage in ["observation_sit","observation_rise"] else .8-elapsed if stage in ["life_sit","life_rise"] else 8.0-elapsed
					if stage in ["life_seated","observation_read"]:
						var seating_player=game.grid_view.branforth_player
						var clock: float=game.get_visual_time_seconds()
						seating_player.current_key=key;seating_player.started=clock-elapsed;seating_player.last_time=clock-.001;seating_player.last_position=game.get_chief_branforth_position()/game.get_cell_size()
					var texture: Texture2D=game.grid_view._get_branforth_frame(game);check(texture==row[i],"Room renderer selects "+key+" slot "+str(i))
					game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					root.get_texture().get_image().save_png(output+"%s-mode%d-q%d-%s-%02d.png"%[id,sample_mode,q,actor.animation_state(),i]);captures+=1
	print("JAMES SEATED ROOMS: %d captures, facings %s, %d failures"%[captures,str(seen.keys()),failures]);quit(1 if failures else 0)
