extends SceneTree
## Staged seated contact at reachable live room furniture; no autonomous route claim.
var failures:=0
var checks:=0
var records:Array=[]
var game
func _init():call_deferred("run")
func check(ok: bool, message: String):
	checks+=1
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
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Normal core release roster")
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var output: String="res://character/james-seated-read-phases-v1/continue-bare-native/";DirAccess.make_dir_recursive_absolute(output)
	var captures:=0;var seen: Dictionary={}
	var player=game.grid_view.branforth_player
	for id in ["observation_room"]:
		for test_case in range(0,3):
			var sample_mode:int=test_case/3
			var trigger_stage:String="observation_read_enter" if test_case%3==0 else "observation_read"
			var trigger_elapsed:float=.21 if test_case%3==0 else .75
			var q:=0
			var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
			game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.powered_room_cells[cell]=true
			var actor=game.branforth_npc;actor.rebuild(game);actor.active=true;actor.dead=false;actor.helmet_equipped=sample_mode==1
			var stations: Array=actor.RoomActivity.stations(actor.geometry[cell]);var chosen: Dictionary={};var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
			for station in stations:
				if station.get("mode","") in ["sit","read"] and actor.can_stand(center+station.point):chosen=station;break
			check(not chosen.is_empty(),id+str(q)+" has a reachable seat")
			if chosen.is_empty():continue
			actor.foot=center+chosen.point;actor.path.clear();actor.goal="fatigue" if id=="crew_lounge" else "curiosity";actor.goal_cell=cell;actor.stage="";actor.arrive()
			check(actor.stage in ["life_sit","observation_sit"],id+str(q)+" arrival selects seating")
			game.selected_room_cell=cell;game._refresh_all();game._set_grid_zoom(1.6,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))
			# Wait for the current room and camera, rather than a fixed frame delay.
			game.grid_view.queue_redraw()
			var settled:=false
			for attempt in range(120):
				await process_frame;await RenderingServer.frame_post_draw
				if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1 and game._grid_view_center_ratio().distance_to((Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))<.002:
					settled=true;break
			check(settled,id+str(q)+" room/camera settled before captures")
			var reading: bool=id=="observation_room";seen[actor.direction]=true
			game.paused=false;game.visual_time_seconds=300;player.current_key="";player.last_time=-1
			var resumed:=false;var began_foot:Vector2=actor.foot;var phases:Dictionary={};var previous:String="";var seen_rise:=false;var sim:=0.0
			for step in range(1100):
				var trigger_clock:float=11.04-actor.timer if actor.stage=="observation_read" else actor.action_elapsed()
				if not resumed and actor.stage==trigger_stage and trigger_clock>=trigger_elapsed:
					if test_case%3==2:
						game.powered_room_cells.erase(cell);actor.update(game,1.0/60.0)
						check(actor.stage=="observation_read_exit" and actor.tablet_exit_pose>=0,"Checkpoint dynamic held-to-stow source")
					game.paused=true
					var before_actor:Dictionary=actor.snapshot()
					var before_pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
					var before_playback:Dictionary=player.snapshot()
					var clock:float=game.visual_time_seconds
					var save=preload("res://scripts/run_save.gd")
					var scratch_path:String="user://james-seated-continue-case%d.loop"%test_case
					var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
					check(problem.is_empty(),"Current seated checkpoint valid: "+problem)
					if not problem.is_empty():quit(2);return
					check(save.write(game,scratch_path)==OK,"Actual seated checkpoint writes")
					data=save.read(scratch_path)
					root.remove_child(game);game.queue_free();await process_frame
					game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://branforth_seated.meta";game.run_save_path=scratch_path
					game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
					root.add_child(game);current_scene=game
					while not game.startup_complete:await process_frame
					game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
					check(await save.restore_staged(game,data),"Actual fresh-scene seated disk Continue")
					game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
					actor=game.branforth_npc;player=game.grid_view.branforth_player
					check(actor.snapshot()==before_actor,"Continue actor exact")
					check(game.paused and game.visual_time_seconds==clock,"Continue clock and pause exact")
					check(player.snapshot()==before_playback,"Continue playback exact")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before_pixels,"Continue source RGBA exact")
					game._process(.5)
					check(actor.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused Continue does not advance")
					check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==before_pixels,"Paused Continue source exact")
					game.selected_room_cell=cell;game._refresh_all();game._set_grid_zoom(1.6,true,(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE))
					game.grid_view.queue_redraw()
					for attempt in range(120):
						await process_frame;await RenderingServer.frame_post_draw
						if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game.grid_view.visible_draw_rooms.size()==1:break
					game.paused=false;resumed=true;previous=""
				var frame:Texture2D=game.grid_view._get_branforth_frame(game)
				var key:String=actor.animation_state()+"-"+actor.direction
				var pool:Dictionary=player.frames if sample_mode==0 else player.equipment_frames["diving-helmet"]
				var slot:int=pool.get(key,[]).find(frame);var phase:String=key+":"+str(slot)
				if actor.stage in ["life_rise","observation_rise"]:seen_rise=true
				if seen_rise and actor.stage not in ["life_sit","life_seated","life_rise","observation_sit","observation_read_enter","observation_read","observation_read_exit","observation_rise"]:break
				check(actor.foot.distance_to(began_foot)<.001,"Controller keeps physical seated foot")
				if phase!=previous:
					game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var filename:String="case%02d-mode%d-change%03d.png"%[test_case,sample_mode,captures]
					check(root.get_texture().get_image().save_png(output+filename)==OK,"Advancing source capture")
					records.append({"room":id,"mode":sample_mode,"case":test_case,"resumed":resumed,"sourceHash":game.grid_view._get_branforth_frame_source(game).get_image().get_data().hex_encode().sha256_text(),"tabletExitPose":actor.tablet_exit_pose,"stage":actor.stage,"key":key,"index":slot,"simTime":sim,"timer":actor.timer,"capture":output+filename,"physicalFoot":[actor.foot.x,actor.foot.y]})
					previous=phase;captures+=1;phases[phase]=true
				actor.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0;sim+=1.0/60.0
			check(resumed and seen_rise,"Fresh Continue completes stow and rise")
	var report:=FileAccess.open("res://character/james-seated-read-phases-v1/continue-bare-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"scope":"Six actual disk checkpoints restored into fresh main scenes at partial draw, held reading and interrupted dynamic-held stow, both gears, reachable q0 South sofa. Actor/playback/clock/pause/source exact, normal update to rise. No autonomous travel or other cardinal/rotation claim."},"  "))
	if not FileAccess.file_exists("res://character/james-seated-read-phases-v1/continue-bare.gd.uid"):
		var uid:=FileAccess.open("res://character/james-seated-read-phases-v1/continue-bare.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES SEATED FRESH CONTINUE: %d captures, facings %s, %d failures"%[captures,str(seen.keys()),failures]);quit(1 if failures else 0)
