extends SceneTree
## Staged seated contact at reachable live room furniture; no autonomous route claim.
var failures:=0
var checks:=0
var records:Array=[]
var output:="res://output/marsh-animation-audit/seated-rooms/"
var game
func _init():call_deferred("run")
func check(ok: bool, message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-output="):output=arg.trim_prefix("--capture-output=").trim_suffix("/")+"/"
	if DisplayServer.get_name()=="headless":quit(2);return
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://marsh_seated.meta";game.run_save_path="user://marsh_seated.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game.recovered_crew.assign([{"architect_id":"marsh","alive":true,"id":"architect_marsh","name":"Marsh","origin":Vector2i(20,20)}])
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	DirAccess.make_dir_recursive_absolute(output)
	if not game.hand_collapsed:game._toggle_hand_collapsed()
	var captures:=0;var seen: Dictionary={}
	for id in ["crew_lounge","observation_room"]:
		for q in range(4):
			var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
			game.selected_rotation=q;game._place_room(id,cell,true);game.occupied[cell].rotation=q;game.powered_room_cells[cell]=true
			var actor=game.marsh_npc;actor.signature="";actor.rebuild(game);actor.active=true;actor.dead=false;actor.battery=100;actor.recharge_docked=false;actor.returning_to_pod=false
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
				var key: String=actor.animation_state()+"-"+actor.direction;var row: Array=game.grid_view.marsh_player.frames[key]
				for i in range(row.size()):
					var elapsed:=0.0
					for j in range(i):elapsed+=float(game.grid_view.marsh_player.timing[key].durations[j])/1000.0
					elapsed+=.01
					actor.timer=.65-elapsed/.8*.65 if stage in ["observation_sit","observation_rise"] else .8-elapsed if stage in ["life_sit","life_rise"] else 8.0-elapsed
					if stage in ["life_seated","observation_read"]:
						var player=game.grid_view.marsh_player
						var clock: float=game.get_visual_time_seconds()
						player.current_key=key;player.started=clock-elapsed;player.last_time=clock-.001;player.last_position=game.get_marsh_position()/game.get_cell_size()
					var texture: Texture2D=game.grid_view._get_marsh_frame(game);check(texture==row[i],"Room renderer selects "+key+" slot "+str(i))
					game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
					var file:String="%s-q%d-%s-%02d.png"%[id,q,actor.animation_state(),i]
					check(root.get_texture().get_image().save_png(output+file)==OK,"Native contact capture saved")
					check(texture.get_image().save_png(output+"source-"+file)==OK,"Actual selected source captured")
					var offset:Vector2=actor.observation_visual_offset()
					var aligned:Vector2=preload("res://scripts/crew_life.gd").head_alignment(actor,game.grid_view.marsh_player)
					var position:Vector2=game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038)+(offset+aligned)*game.get_cell_size()/384.0
					var canvas:Vector2=game.grid_view.get_global_transform_with_canvas()*position
					records.append({"file":file,"sourceFile":"source-"+file,"room":id,"rotation":q,"stage":stage,"key":key,"slot":i,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"offset":[offset.x,offset.y],"headAlignment":[aligned.x,aligned.y],"canvasPosition":[canvas.x,canvas.y],"pivot":texture.get_meta("crew_pivot"),"standingHeight":texture.get_meta("crew_standing_height"),"stagedElapsed":elapsed})
					captures+=1
	var report=FileAccess.open(output+"report.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":records,"facings":seen.keys(),"scope":"Staged actor seating/read/rise at reachable default furniture in two live rooms/four rotations. Actual selected renderer sources and captured poses; no autonomous route,fullsave,continuousplayback or allcardinal claim."},"\t"));report.close()
	print("MARSH SEATED ROOMS: %d captures, facings %s, %d failures"%[captures,str(seen.keys()),failures]);quit(1 if failures else 0)
