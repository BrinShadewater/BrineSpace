from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'native-audit.gd').read_text().split('\tvar phases:Array=')[0]
source+='''\tfor phase in ["eat","drink"]:
\t\tfor hazard in ["fire","flood","oxygen-loss"]:
\t\t\tprint("HAZARD SETUP ",phase,"/",hazard," prior running=",game.running," paused=",game.paused," crew=",game.crew_count)
\t\t\tgame.running=true;game.paused=false;game.crew_count=1;game.summary_layer.visible=false
\t\t\tgame.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
\t\t\tfor member in game.recovered_crew:
\t\t\t\tif member.get("architect_id","")=="branforth":member.alive=true
\t\t\tfor offset in [Vector2i.ZERO,Vector2i.DOWN]:
\t\t\t\tvar room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
\t\t\t\troom.pos=cell+offset;room.rotation=0;room.water_level=0;room.fire=0
\t\t\t\tgame.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
\t\t\tnpc.rebuild(game);npc.meal_return.clear();npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
\t\t\tnpc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2.DOWN*384,cell+Vector2i.DOWN));npc.direction="north";npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.breath_oxygen=15;npc.starvation=0;npc.visits.clear();npc.decision_rng.seed=1
\t\t\tgame.resources.food=1000;game.resources.oxygen=1000;game.resources.water=0;game.hardware.pumps=false;game.hardware.doors=false
\t\t\tnpc.set_meta("flood_safety_wait",0.0);npc.set_meta("flood_retreat_check",0.0);npc.set_meta("flood_blocked_warning",false);npc.choose_goal(game)
\t\t\tvar reached:=false
\t\t\tfor tick in range(3000):
\t\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\t\t\tvar texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
\t\t\t\tif npc.animation_state()==phase and player.frames[phase+"-north"].find(texture)==3:reached=true;break
\t\t\tcheck(reached,"Normal meal reaches held pose before genuine hazard")
\t\t\tgame.powered_room_cells.erase(cell);game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;check(npc.meal_return_active(),"Normal power-loss return begins")
\t\t\tgame.powered_room_cells[cell]=true
\t\t\tfor tick in range(24):game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\t\tcheck(npc.meal_return_active(),"Hazard interrupts unfinished return")
\t\t\tvar hunger:float=npc.needs.hunger;var old:Vector2=npc.foot
\t\t\tif hazard=="fire":game.occupied[cell].fire=.7
\t\t\telif hazard=="flood":game.occupied[cell].water_level=.95
\t\t\telse:game.resources.oxygen=0;npc.breath_oxygen=.001
\t\t\tgame._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
\t\t\tcheck(not npc.meal_return_active(),"Genuine hazard immediately preempts cosmetic return")
\t\t\tcheck(npc.meal_return.is_empty(),"Hazard clears stale return state")
\t\t\tcheck(npc.needs.hunger>=hunger-.001,"Emergency never grants abandoned meal reward")
\t\t\tprint("HAZARD FIRST ",phase,"/",hazard," running=",game.running," paused=",game.paused," dead=",npc.dead," goal=",npc.goal," return=",npc.meal_return)
\t\t\tif npc.dead:game.summary_layer.visible=false # Reveal actor for capture after real death/report assertions.
\t\t\tvar first:Dictionary=npc.snapshot();var pictures:Array=[await capture("hazard-"+phase+"-"+hazard+"-first",npc)]
\t\t\tvar safe:=false;var moved:bool=npc.foot!=old;var ticks:=0
\t\t\tif hazard=="oxygen-loss":check(npc.dead and npc.animation_state()=="death-ground","Real oxygen depletion selects actual death source");safe=npc.dead
\t\t\telse:
\t\t\t\twhile ticks<3000 and not safe and not npc.dead:
\t\t\t\t\tvar before:Vector2=npc.foot;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
\t\t\t\t\tvar after:Vector2=npc.foot;npc.foot=before
\t\t\t\t\tvar clear:bool=npc.segment_clear(before,after);npc.foot=after
\t\t\t\t\tif not clear:print("HAZARD LEG ",phase,"/",hazard," ",before," -> ",after," goal=",npc.goal," medium=",npc.movement_medium)
\t\t\t\t\tcheck(clear,"Emergency traveled floor leg clears geometry from actual origin")
\t\t\t\t\tmoved=moved or npc.foot!=before
\t\t\t\t\tvar room:Dictionary=game.occupied.get(npc.cell_at(npc.foot),{})
\t\t\t\t\tsafe=not room.is_empty() and npc.cell_at(npc.foot)!=cell and float(room.get("fire",0))<=0 and float(room.get("water_level",0))<.55
\t\t\t\tcheck(safe and moved and not npc.dead,"Actual emergency route reaches live refuge before air expires")
\t\t\tpictures.append(await capture("hazard-"+phase+"-"+hazard+"-end",npc))
\t\t\tresults.append({"phase":phase,"hazard":hazard,"first":first,"safe":safe,"moved":moved,"ticks":ticks,"end":npc.snapshot(),"captures":pictures})
\tvar file:=FileAccess.open(OUT+"native-hazard-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Six actual normal North bowl/cup services, interrupted mid-return by real fire/flood/oxygen depletion through native systems. Immediate preemption/state cleanup/no abandoned reward; real refuge route or real death. Other gears/layouts/changed contacts/crowd hazards and disk hazard restores separate."},"  "));file.close()
\tprint("JAMES MEAL RETURN HAZARDS: ",checks," checks; ",failures," failures")
\tquit(1 if failures else 0)
'''
(P/'native-hazard.gd').write_text(source)
print('Created six genuine fire/flood/oxygen-loss interruption cases')
