from pathlib import Path
P = Path(__file__).resolve().parent
source = (P / 'native-locker.gd').read_text()
source = source.split('\tfor q in range(4):', 1)[0]
source = source.replace('OUT+"captures/', 'OUT+"refill-captures/').replace('OUT+"captures"', 'OUT+"refill-captures"')
source = source.replace('game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])', 'game.running=true;game.paused=false;game.Architects.advance_core(game,10)\n\tcheck(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")')
source += '''	for q in range(4):
		game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
		var inside:Vector2i=[Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP,Vector2i.RIGHT][q]
		for offset in [Vector2i.ZERO,inside]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("airlock" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=0
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.stage="";npc.expedition.clear();npc.console_motion.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(inside)*384,cell+inside));npc.direction="north";npc.goal="";npc.path.clear();npc.state="idle";npc.timer=0;npc.helmet_equipped=true;npc.movement_medium="dry"
		npc.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0};npc.tank_oxygen=0;npc.breath_oxygen=15;npc.starvation=0
		player.motion.clear();player.current_key="";player.last_time=-1;game.visual_time_seconds=100
		var target:Dictionary=Service.locker(game,cell);check(not target.is_empty(),"Actual locker discovered")
		check(Service.request(game,"branforth",cell,true),"Actual refill request accepted")
		var ticks:=0;var started:=false;var contact:=Vector2.INF;var arrival_oxygen:=0.0
		while ticks<8000 and not started:
			var before:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
			check(npc.can_stand(npc.foot) and npc.segment_clear(before,npc.foot),"Actual refill approach clear")
			if npc.activity=="refilling oxygen tank":started=true;contact=npc.foot;arrival_oxygen=npc.tank_oxygen
		check(started and npc.direction=="east" and contact.distance_to(target.interaction_point)<.1,"Refill arrives at selected east contact")
		var reservation:bool=Service.busy(game,cell,game.bill_npc)
		check(reservation,"Actual refill holds locker reservation for another actor")
		check(not Service.request(game,"branforth",cell,true) and not Service.request(game,"branforth",cell),"Repeated refill and helmet-change requests refused during hold")
		var elapsed:=0.0;var restored:=false;var captures:Array=[]
		while npc.activity=="refilling oxygen tank" and elapsed<6:
			var before_oxygen:float=npc.tank_oxygen;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;elapsed+=1.0/120
			if npc.activity!="refilling oxygen tank":break
			check(npc.foot==contact and npc.helmet_equipped and npc.movement_medium=="dry","Refill keeps registered contact and fitted gear")
			check(npc.tank_oxygen>=before_oxygen and npc.tank_oxygen<=60,"Normal vitals refill monotonically")
			check(player.equipment_frames["diving-helmet"]["idle-east"].has(game.grid_view._get_branforth_frame_source(game)),"Selected matte east idle cycle throughout current refill")
			if not restored and elapsed>=2.5:
				captures.append(await capture("q%d-refill-held"%q,npc))
				game.paused=true;var before_actor:Dictionary=npc.snapshot();var clock:float=game.visual_time_seconds;var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-refill.loop"
				check(save.problem(save.capture(game)).is_empty(),"Refill checkpoint valid")
				check(save.write(game,scratch_path)==OK,"Actual refill disk write")
				check(await save.restore_staged(game,save.read(scratch_path)),"Actual refill disk Continue")
				game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==before_actor and game.paused and game.visual_time_seconds==clock,"Refill Continue keeps full actor and clock")
				check(Service.busy(game,cell,game.bill_npc) and not Service.request(game,"branforth",cell,true),"Continue retains refill reservation and rejects duplicate request")
				game._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused refill does not advance")
				game.set_process(false);game.paused=false;restored=true
		check(restored and npc.tank_oxygen>=59.9 and npc.activity!="refilling oxygen tank","Refill completes full tank and leaves finite hold")
		check(not Service.busy(game,cell,game.bill_npc),"Completed refill releases reservation")
		npc.path.clear();npc.goal="";npc.stage="";npc.state="idle";npc.timer=0;npc.foot=contact;npc.tank_oxygen=20
		check(Service.request(game,"branforth",cell,true),"New refill accepted after completion")
		game._update_test_walker(1.0/120)
		check(Service.refilling(npc),"Contact refill begins normally")
		game.powered_room_cells.erase(cell);Service.check_service(game,npc)
		var offline_oxygen:float=npc.tank_oxygen
		check(not Service.refilling(npc) and not Service.busy(game,cell,game.bill_npc),"Offline service ends hold and releases reservation")
		game._update_test_walker(1.0/120)
		check(npc.tank_oxygen==offline_oxygen and not Service.request(game,"branforth",cell,true),"Offline refill grants no oxygen and refuses restart")
		results.append({"rotation":q,"reservationDuringHold":reservation,"arrivalOxygen":arrival_oxygen,"refillElapsed":elapsed,"restored":restored,"captures":captures})
	var file:=FileAccess.open(OUT+"native-locker-refill-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Four actual standard rotated airlock refill routes with equipped James, normal vitals and five-second idle hold, four actual disk Continue restores, pause and selected equipped idle-cycle pixels. Reservation, duplicate request rejection, post-completion release and power-loss/no-credit checks. No new refill animation authored; crowd body journeys/exterior return not exercised."},"  "));file.close()
	print("JAMES LOCKER REFILL: ",checks," checks; ",failures," failures; ",results.size()," actual refill journeys")
	quit(1 if failures else 0)
'''
(P / 'native-locker-refill.gd').write_text(source)
print('Created actual four-rotation refill/Continue fixture with reservation diagnostic')
