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
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	var output: String="res://character/james-seated-read-phases-v1/interrupt-native/";DirAccess.make_dir_recursive_absolute(output)
	var captures:=0;var seen: Dictionary={}
	var player=game.grid_view.branforth_player
	for id in ["observation_room"]:
		for test_case in range(12):
			var sample_mode:int=test_case/6
			var trigger_stage:String="observation_read_enter" if test_case%6<4 else "observation_read"
			var trigger_elapsed:float=[.03,.13,.29,.43,.15,.75][test_case%6]
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
			var interrupted:=false;var reward_before:float=actor.needs["curiosity"];var before_hash:String="";var after_hash:String="";var began_foot:Vector2=actor.foot;var phases:Dictionary={};var previous:String="";var seen_rise:=false;var sim:=0.0
			for step in range(240):
				var trigger_clock:float=11.04-actor.timer if actor.stage=="observation_read" else actor.action_elapsed()
				if not interrupted and actor.stage==trigger_stage and trigger_clock>=trigger_elapsed:
					var original:Texture2D=game.grid_view._get_branforth_frame_source(game)
					before_hash=original.get_image().get_data().hex_encode().sha256_text()
					check(actor.valid_snapshot(actor.snapshot()),"Pre-interruption snapshot admission")
					game.powered_room_cells.erase(cell)
					check(not actor.service_available(game,cell),"Actual room power loss removes service")
					actor.update(game,1.0/60.0)
					var restored:Texture2D=game.grid_view._get_branforth_frame_source(game)
					after_hash=restored.get_image().get_data().hex_encode().sha256_text()
					check(actor.stage=="observation_read_exit" and actor.goal.is_empty(),"Power loss starts tablet stow before rise")
					check(before_hash==after_hash,"Power loss preserves exact current rendered source pixels")
					check(actor.valid_snapshot(actor.snapshot()),"Interrupted stow snapshot admission")
					interrupted=true;previous=""
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
					records.append({"room":id,"mode":sample_mode,"case":test_case,"triggerStage":trigger_stage,"triggerElapsed":trigger_elapsed,"interrupted":interrupted,"beforeHash":before_hash,"afterHash":after_hash,"sourceHash":game.grid_view._get_branforth_frame_source(game).get_image().get_data().hex_encode().sha256_text(),"tabletExitPose":actor.tablet_exit_pose,"stage":actor.stage,"key":key,"index":slot,"simTime":sim,"timer":actor.timer,"capture":output+filename,"physicalFoot":[actor.foot.x,actor.foot.y]})
					previous=phase;captures+=1;phases[phase]=true
				actor.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0;sim+=1.0/60.0
			check(interrupted and seen_rise,"Interrupted controller stows then rises")
			check(actor.needs["curiosity"]>=reward_before,"Cancelled reading earns no completion reward; normal need growth retained")
	var report:=FileAccess.open("res://character/james-seated-read-phases-v1/interrupt-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"scope":"Actual normal NPC update after reachable q0 South sofa arrival, four partial draw and two held power-loss interruptions per gear; exact source pixel continuity, snapshot admission and fixed physical foot. No fresh disk Continue, autonomous travel or other rotation claim."},"  "))
	if not FileAccess.file_exists("res://character/james-seated-read-phases-v1/interrupt.gd.uid"):
		var uid:=FileAccess.open("res://character/james-seated-read-phases-v1/interrupt.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES TABLET INTERRUPTIONS: %d captures, facings %s, %d failures"%[captures,str(seen.keys()),failures]);quit(1 if failures else 0)
