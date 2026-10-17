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
	var output: String="res://character/james-seated-furniture-consistency-v2/controller-native/";DirAccess.make_dir_recursive_absolute(output)
	var captures:=0;var seen: Dictionary={}
	var player=game.grid_view.branforth_player
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
			var began_foot:Vector2=actor.foot;var phases:Dictionary={};var previous:String="";var seen_rise:=false;var sim:=0.0
			for step in range(1100):
				var frame:Texture2D=game.grid_view._get_branforth_frame(game)
				var key:String=actor.animation_state()+"-"+actor.direction
				var pool:Dictionary=player.frames if sample_mode==0 else player.equipment_frames["diving-helmet"]
				var slot:int=pool.get(key,[]).find(frame);var phase:String=key+":"+str(slot)
				if actor.stage in ["life_rise","observation_rise"]:seen_rise=true
				if seen_rise and actor.stage not in ["life_sit","life_seated","life_rise","observation_sit","observation_read","observation_rise"]:break
				check(actor.foot.distance_to(began_foot)<.001,"Controller keeps physical seated foot")
				if phase!=previous:
					game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var filename:String="%s-mode%d-change%03d.png"%[id,sample_mode,captures]
					check(root.get_texture().get_image().save_png(output+filename)==OK,"Advancing source capture")
					records.append({"room":id,"mode":sample_mode,"stage":actor.stage,"key":key,"index":slot,"simTime":sim,"timer":actor.timer,"capture":output+filename,"physicalFoot":[actor.foot.x,actor.foot.y]})
					previous=phase;captures+=1;phases[phase]=true
				actor.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0;sim+=1.0/60.0
			check(seen_rise,"Controller completes seated held activity and rises")
	var report:=FileAccess.open("res://character/james-seated-furniture-consistency-v2/controller-evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"scope":"Actual normal NPC update timers after reachable q0 furniture station arrival, held activity/rise and source-change native captures, both gears. Fixed60Hz fixture steps and controlled topology; no autonomous incoming/outgoing travel, interruption, fresh Continue or all-rotation claim."},"  "))
	if not FileAccess.file_exists("res://character/james-seated-furniture-consistency-v2/controller.gd.uid"):
		var uid:=FileAccess.open("res://character/james-seated-furniture-consistency-v2/controller.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES SEATED CONTROLLER: %d captures, facings %s, %d failures"%[captures,str(seen.keys()),failures]);quit(1 if failures else 0)
