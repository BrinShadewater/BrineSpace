from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
source=(R/'character/james-tablet-east-matte-v3/native-arrival-continue.gd').read_text()
prefix=source[:source.index('\n\tvar baseline:bool=false')].replace('res://character/james-tablet-east-matte-v3/','res://character/james-east-cargo-heads-v3/').replace('JAMES TABLET ARRIVAL CONTINUE BOOT','JAMES WORKSHOP BOOT').replace('james-tablet-arrival','james-workshop').replace('"maintenance_bay" if delta==Vector2i.ZERO','"salvage_workshop" if delta==Vector2i.ZERO')
prefix=prefix.replace('func capture(label: String,npc) -> String:\n','func capture(label: String,npc) -> String:\n\tgame.hand_panel.hide();game.card_drag.hide()\n')
body='''
	for room in game.placed_rooms:room.water_level=0.0
	npc.movement_medium="dry"
	var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN])
	check(not stations.is_empty(),"Default workshop has real station")
	if stations.is_empty():quit(2);return
	var contact:Vector2=center+stations[0].point
	var facing:String=stations[0].facing
	var start:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if at.distance_to(contact)<8 or at.distance_to(contact)>100:continue
		if npc.travel_segment_clear(at,contact,npc.travel_heading(at,contact,facing)):start=at;break
	check(start.is_finite(),"Collision-clear actual workshop approach")
	if not start.is_finite():quit(2);return
	for mode in ["bare","helmet"]:
		npc=game.branforth_npc;player=game.grid_view.branforth_player
		npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
		npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		game.visual_time_seconds=100;game.paused=false;player.current_key="";player.motion.clear();player.last_time=-1
		var saved_stages:Dictionary={};var seen_stages:Dictionary={};var poses:Dictionary={};var previous_stage:="";var elapsed:=0.0;var captures:Array=[]
		for tick in range(2500):
			npc.update(game,.02);game.visual_time_seconds+=.02;elapsed+=.02
			var tex:Texture2D=game.grid_view._get_branforth_frame(game)
			check(tex!=null,"Actual workshop selected texture")
			if npc.stage!=previous_stage:
				print("JAMES WORKSHOP STAGE: ",mode," / ",npc.stage," / ",npc.direction," / ",npc.timer," / path",npc.path.size())
				previous_stage=npc.stage
			if npc.stage.begins_with("workshop_"):
				seen_stages[npc.stage]=true;poses[npc.animation_state()]=true
				check(npc.helmet_equipped==(mode=="helmet") and npc.goal=="curiosity","Workshop gear/goal retained")
			if npc.stage in ["workshop_pickup","workshop_carry","workshop_unload"] and not saved_stages.has(npc.stage):
				if npc.stage=="workshop_pickup" and npc.timer>.27:continue
				if npc.stage=="workshop_unload" and npc.timer>1.02:continue
				var stage:String=npc.stage;captures.append(await capture(mode+"-"+stage+"-000",npc));game.paused=true
				var actor:Dictionary=npc.snapshot();var playback:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var clock:float=game.visual_time_seconds
				var save=preload("res://scripts/run_save.gd");var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
				check(problem.is_empty(),"Actual workshop checkpoint valid: "+problem)
				if not problem.is_empty():quit(2);return
				var path:="user://james-workshop.loop";check(save.write(game,path)==OK,"Workshop disk checkpoint writes");data=save.read(path)
				root.remove_child(game);game.queue_free();await process_frame
				game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-workshop.meta";game.run_save_path=path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
				root.add_child(game);current_scene=game
				while not game.startup_complete:await process_frame
				game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				check(await save.restore_staged(game,data),"Workshop fresh-main disk Continue")
				game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==actor,"Workshop Continue actor exact");check(player.snapshot()==playback,"Workshop Continue playback exact");check(game.visual_time_seconds==clock and game.paused,"Workshop Continue pause/clock exact")
				check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Workshop Continue source exact")
				game._process(.5);check(npc.snapshot()==actor and game.visual_time_seconds==clock,"Paused workshop Continue stays fixed")
				game.paused=false;saved_stages[stage]=true
			if seen_stages.has("workshop_unload") and npc.stage.is_empty():break
		check(seen_stages.size()==5,"Actual inspect/work/pickup/carry/unload stages")
		check(saved_stages.size()==3,"Actual pickup/carry/unload fresh disk checkpoints")
		check(npc.stage.is_empty() and absf(npc.needs.curiosity-(90.0+elapsed*.22-65.0))<.02,"Workshop finishes and pays exact65 normal curiosity relief; next chooser may assign a goal")
		results.append({"mode":mode,"stages":seen_stages.keys(),"poses":poses.keys(),"savedStages":saved_stages.keys(),"elapsed":elapsed,"captures":captures,"finalGoal":npc.goal,"finalActivity":npc.activity,"finalCuriosity":npc.needs.curiosity})
		print("JAMES WORKSHOP CASE: ",mode," checks",checks," failures",failures)
	var report:=FileAccess.open(OUT+"native-workshop-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Default rotation0 workshop, prescribed collision-clear approach/curiosity goal, actual NPC.update/arrival/RoomActivity inspect-work-pickup-generated carrying route-unload; both initial gears; three ordinary disk/fresh-main Continues per gear. Main simulation otherwise paused/actor-stepped, not natural scheduling or full cardinal turns/interruptions."},"  "))
	if not FileAccess.file_exists(OUT+"native-workshop.gd.uid"):
		var uid:=FileAccess.open(OUT+"native-workshop.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WORKSHOP: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
'''
(P/'native-workshop.gd').write_text(prefix+body)
