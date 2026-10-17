from pathlib import Path
P=Path(__file__).resolve().parent
prefix=(P/'native-workshop.gd').read_text().split('\n\tfor room in game.placed_rooms:room.water_level=0.0')[0]
body='''
	for room in game.placed_rooms:room.water_level=0.0
	npc.movement_medium="dry"
	var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN]);check(not stations.is_empty(),"Workshop station")
	if stations.is_empty():quit(2);return
	var contact:Vector2=center+stations[0].point;var facing:String=stations[0].facing;var start:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if at.distance_to(contact)<8 or at.distance_to(contact)>100:continue
		if npc.travel_segment_clear(at,contact,npc.travel_heading(at,contact,facing)):start=at;break
	check(start.is_finite(),"Actual clear approach")
	if not start.is_finite():quit(2);return
	for mode in ["bare","helmet"]:
		for target in ["workshop_pickup","workshop_carry","workshop_unload"]:
			game.powered_room_cells[ORIGIN]=true;game.visual_time_seconds=100;game.paused=false
			npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
			npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
			player.current_key="";player.motion.clear();player.last_time=-1
			var reached:=false;var carry_ticks:=0
			for tick in range(2000):
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
				if npc.stage!=target:continue
				if target=="workshop_pickup" and npc.timer>.27:continue
				if target=="workshop_unload" and npc.timer>1.02:continue
				if target=="workshop_carry":
					carry_ticks+=1
					if carry_ticks<20:continue
				reached=true;break
			check(reached,"Actual stage reached for interruption "+mode+target)
			if not reached:continue
			var before_stage:String=npc.stage;var before_pose:String=npc.animation_state();var before_timer:float=npc.timer;var before_foot:Vector2=npc.foot;var before_motion:Dictionary=player.motion.duplicate(true)
			var before:Texture2D=game.grid_view._get_branforth_frame(game);var stem:String=mode+"-"+target
			before.get_image().save_png(OUT+"arrival-captures/interrupt-"+stem+"-source-before.png")
			var capture_before:String=await capture("interrupt-"+stem+"-before-000",npc)
			game.powered_room_cells.erase(ORIGIN);check(not npc.service_available(game,ORIGIN),"Actual workshop power loss")
			npc.update(game,.02);game.visual_time_seconds+=.02
			var after:Texture2D=game.grid_view._get_branforth_frame(game);after.get_image().save_png(OUT+"arrival-captures/interrupt-"+stem+"-source-after.png")
			var capture_after:String=await capture("interrupt-"+stem+"-after-000",npc)
			results.append({"mode":mode,"target":target,"beforeStage":before_stage,"beforePose":before_pose,"beforeTimer":before_timer,"beforeMotion":before_motion,"afterStage":npc.stage,"afterPose":npc.animation_state(),"afterTimer":npc.timer,"afterMotion":player.motion.duplicate(true),"sameFoot":before_foot==npc.foot,"nextGoal":npc.goal,"captures":[capture_before,capture_after],"sources":["arrival-captures/interrupt-"+stem+"-source-before.png","arrival-captures/interrupt-"+stem+"-source-after.png"]})
			print("JAMES WORKSHOP INTERRUPT: ",mode," ",target," / ",before_pose," -> ",npc.animation_state()," / stage",npc.stage)
	var report:=FileAccess.open(OUT+"interruption-probe-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Diagnostic actual default0 workshop journeys, both initial gears, pickup-mid/carry-mid/unload-mid real power removal +20ms actor update and source/world before/after captures. No corrective motion or Continue acceptance."},"  "))
	if not FileAccess.file_exists(OUT+"interruption-probe.gd.uid"):
		var f:=FileAccess.open(OUT+"interruption-probe.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WORKSHOP INTERRUPTION PROBE: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
'''
(P/'interruption-probe.gd').write_text(prefix+body)
