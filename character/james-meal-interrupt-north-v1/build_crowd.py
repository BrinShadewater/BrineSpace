from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-audit.gd').read_text().split('\tvar phases:Array=')[0]
source+='''\tgame.recovered_crew.append({"architect_id":"bill","alive":true,"id":"architect_bill","name":"Bill","origin":cell})
\tvar peer=game.bill_npc
\tpeer.decision_rng=RandomNumberGenerator.new()
\tfor phase in ["eat","drink"]:
\t\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\t\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0
\t\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\t\tpeer.active=false;peer.rebuild(game);npc.rebuild(game);npc.meal_return.clear()
\t\tfor actor in [npc,peer]:
\t\t\tactor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.avoidance_positions.clear();actor.avoidance_position=Vector2.INF;actor.path.clear();actor.goal="";actor.state="idle";actor.timer=0;actor.helmet_equipped=false;actor.movement_medium="dry";actor.needs={"maintenance":0.0,"hunger":0.0,"fatigue":0.0,"curiosity":0.0}
\t\tpeer.active=false;npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2.DOWN*384,cell+Vector2i.DOWN));npc.direction="north";npc.needs.hunger=95;npc.decision_rng.seed=1;npc.choose_goal(game);game.resources.food=1000
\t\tgame.test_walker_cell=Vector2i(-1,-1)
\t\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);var planned_contact:Vector2=center+Vector2(stations[0].point)
\t\tpeer.foot=planned_contact-Vector2(32,0);peer.direction="east";peer.needs.curiosity=95;peer.visits.clear();peer.avoidance_positions.clear();peer.avoidance_position=Vector2.INF
\t\tvar seed_used:=0
\t\tfor seed in range(1,129):
\t\t\tpeer.goal="";peer.path.clear();peer.timer=0;peer.decision_rng.seed=seed;peer.choose_goal(game)
\t\t\tif peer.goal_cell==cell and not peer.path.is_empty() and peer.path[-1].distance_to(planned_contact)<1:seed_used=seed;break
\t\tcheck(seed_used>0,"Peer normal chooser queues same contact before James occupies it")
\t\tvar reached:=false
\t\tfor tick in range(3000):
\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\tif npc.animation_state()==phase and player.frames[phase+"-north"].find(texture)==3:reached=true;break
\t\tcheck(reached,"Normal James meal reaches held gesture")
\t\tgame.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\tcheck(npc.meal_return_active(),"Genuine service-loss return starts")
\t\tgame.powered_room_cells[cell]=true
\t\tvar contact:Vector2=npc.foot;peer.active=true;peer.foot=contact-Vector2(32,0);peer.direction="east";peer.needs.curiosity=95
\t\tcheck(peer.can_stand(peer.foot) and peer.foot.distance_to(contact)>=32,"Real peer starts on clear adjacent floor")
\t\tcheck(not peer.path.is_empty() and peer.path[-1].distance_to(contact)<1,"Queued real peer service intent remains intact")
\t\tvar minimum:=32.0;var moved_while_return:=false;var unfinished_drop:=false;var max_wait:=0.0;var return_ticks:=0;var pictures:Array=[await capture("crowd-"+phase+"-start",npc)]
\t\twhile return_ticks<240 and npc.meal_return_active():
\t\t\tvar old:Vector2=npc.foot;var old_elapsed:float=npc.meal_return.elapsed;var duration:float=npc.meal_return_seconds(npc.meal_return.source,npc.meal_return.index)
\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;return_ticks+=1
\t\t\tminimum=minf(minimum,npc.foot.distance_to(peer.foot));max_wait=maxf(max_wait,peer.traffic_wait)
\t\t\tif npc.foot!=old:moved_while_return=true
\t\t\tif not npc.meal_return_active() and old_elapsed+1.0/120<duration-.0001:unfinished_drop=true
\t\tcheck(not moved_while_return and not unfinished_drop,"Nearby traffic preserves complete stationary held-prop return")
\t\tcheck(minimum>=32-.02,"Two real crew maintain clearance")
\t\tvar peer_service:=false;var follow_ticks:=0
\t\twhile follow_ticks<1200 and not peer_service:
\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;follow_ticks+=1
\t\t\tminimum=minf(minimum,npc.foot.distance_to(peer.foot));max_wait=maxf(max_wait,peer.traffic_wait)
\t\t\tpeer_service=peer.goal_cell==cell and peer.stage in ["life_eat","life_drink"]
\t\tcheck(peer_service,"Queued peer reaches actual galley service after return gives way")
\t\tcheck(minimum>=32-.02,"Follow-up passage keeps real crew clearance")
\t\tpictures.append(await capture("crowd-"+phase+"-end",npc))
\t\tresults.append({"phase":phase,"seed":seed_used,"ticks":return_ticks,"peerService":peer_service,"peerFollowTicks":follow_ticks,"movedWhileReturning":moved_while_return,"unfinishedDrop":unfinished_drop,"minimumSeparation":minimum,"maxPeerWait":max_wait,"captures":pictures,"James":npc.snapshot(),"peer":peer.snapshot()})
\t\tpeer.active=false
\tvar file:=FileAccess.open(OUT+"native-crowd-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two normal James held-meal/cup interruptions with real Bill peer normal chooser targeting same contact during return. Actual shared updates/passage, fixed return and separation checked. Other gear/layouts and final peer service completion separate."},"  "));file.close()
\tprint("JAMES MEAL RETURN CROWD: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-crowd.gd').write_text(source)
print('Created two actual return/peer normal chooser traffic cases')
