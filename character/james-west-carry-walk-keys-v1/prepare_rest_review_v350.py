from pathlib import Path
p=Path(__file__).resolve().parent;o=p/'release-rest-review-v350';o.mkdir(exist_ok=True)
s=(p/'release-death-review-v349/native_probe.gd').read_text()
s=s[:s.index('\tgame.running=true')]
s=s.replace('release-death-review-v349','release-rest-review-v350').replace('death349','rest350')
s=s.replace('const Player=preload("res://character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/reorient_player.gd")','const LIFE=preload("res://scripts/crew_life.gd")')
s+='''\tgame.running=true;game.Architects.advance_core(game,10)
\tfor peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
\tgame.test_walker_cell=Vector2i(-1,-1)
\tvar npc=game.branforth_npc;var player=game.grid_view.branforth_player
\tvar cases:Array=[]
\tfor room_id in ["crew_hab","crew_lounge"]:
\t\tfor rotation in range(4):
\t\t\tgame.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear()
\t\t\tgame.selected_rotation=rotation;game._place_room(room_id,ORIGIN,true);game.occupied[ORIGIN].rotation=rotation;game.powered_room_cells[ORIGIN]=true
\t\t\tcheck(int(game.occupied[ORIGIN].rotation)==rotation,"Fixture exercises requested actual room rotation")
\t\t\tnpc.rebuild(game)
\t\t\tvar stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN])
\t\t\tcheck(not stations.is_empty(),"Authored rest furniture provides a station")
\t\t\tif stations.is_empty():continue
\t\t\tvar station:Dictionary=stations[0]
\t\t\tfor gear in ["","diving-helmet"]:
\t\t\t\tnpc.active=true;npc.dead=false;npc.goal="fatigue";npc.goal_cell=ORIGIN;npc.stage="";npc.state="idle";npc.path.clear();npc.expedition.clear();npc.movement_medium="dry";npc.helmet_equipped=not gear.is_empty();npc.bunk_motion.clear()
\t\t\t\tnpc.foot=(Vector2(ORIGIN)+Vector2.ONE*.5)*384+Vector2(station.point);npc.direction=station.facing;npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0;npc.air_recovery=0
\t\t\t\tcheck(npc.can_stand(npc.foot),"Actual registered furniture approach standable")
\t\t\t\tcheck(npc.begin_room_activity(),"Actual room activity dispatcher enters rest")
\t\t\t\tvar foot:Vector2=npc.foot;var entry:String=npc.stage;var duration:float=LIFE.seconds(npc,entry)
\t\t\t\tvar label:String=("bare" if gear.is_empty() else "helmet")+"-"+room_id+"-"+str(rotation)
\t\t\t\tplayer.current_key="";player.motion.clear();player.last_time=-1;game.visual_time_seconds=100.0
\t\t\t\tfor amount in [0.0,.5,.999]:
\t\t\t\t\tnpc.timer=duration*(1.0-amount);game.visual_time_seconds=100+duration*amount
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame_source(game)!=null,"Normal selected entry pose available")
\t\t\t\t\tawait capture(label+"-entry-"+str(amount),npc)
\t\t\t\tnpc.timer=.01;npc.update(game,.02)
\t\t\t\tcheck(npc.stage==("life_sleep" if room_id=="crew_hab" else "life_seated"),"Actual update enters held rest")
\t\t\t\tcheck(npc.foot==foot,"Rest retains physical furniture approach")
\t\t\t\tgame.visual_time_seconds+=.1;game.grid_view._get_branforth_frame_source(game);await capture(label+"-held",npc)
\t\t\t\tvar saved:Dictionary=npc.snapshot();npc.restore_snapshot(game,saved)
\t\t\t\tcheck(npc.stage==saved.stage and npc.foot==foot and npc.helmet_equipped==not gear.is_empty(),"Actual actor snapshot preserves held rest and gear")
\t\t\t\tgame.powered_room_cells.erase(ORIGIN);npc.update(game,.01)
\t\t\t\tvar exit:String="life_get_up" if room_id=="crew_hab" else "life_rise"
\t\t\t\tcheck(npc.stage==exit and npc.goal.is_empty(),"Actual service power loss starts finite exit")
\t\t\t\tduration=LIFE.seconds(npc,exit)
\t\t\t\tfor amount in [0.0,.5,.999]:
\t\t\t\t\tnpc.timer=duration*(1.0-amount);game.visual_time_seconds+=.1
\t\t\t\t\tcheck(game.grid_view._get_branforth_frame_source(game)!=null,"Normal selected exit pose available")
\t\t\t\t\tawait capture(label+"-exit-"+str(amount),npc)
\t\t\t\t\tcheck(npc.foot==foot,"Interrupted exit retains physical contact")
\t\t\t\tnpc.timer=.01;npc.update(game,.02)
\t\t\t\tcheck(npc.stage.is_empty() and npc.foot==foot,"Finite exit completes before new route")
\t\t\t\tcases.append({"room":room_id,"rotation":rotation,"gear":gear,"station":station,"entry":entry,"exit":exit})
\t\t\t\tgame.powered_room_cells[ORIGIN]=true;npc.active=false
\tif not FileAccess.file_exists(OUT+"native_probe.gd.uid"):FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")
\tFileAccess.open(OUT+"native-review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Normal James actor and renderer, first actual rest station in each of four authored habitation/lounge rotations, both gears. Actual activity entry, update into held rest, actor snapshot restoration, service power loss and finite exit. Prescribed renderer samples, no autonomous goal selection/arrival, whole-run disk restore or continuous motion claim."},"\\t"))
\tprint("JAMES NATIVE REST checks=",checks," failures=",failures," cases=",cases.size()," captures=",captures.size());game.queue_free();await process_frame;quit(0 if failures==0 else 1)
'''
(o/'native_probe.gd').write_text(s)
print('Prepared actual furniture rest lifecycle review')
