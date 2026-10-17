from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-journey-v323';o.mkdir(exist_ok=True)
src=(p/'room-journey-v286/native_probe.gd').read_text(encoding='utf-8')
prefix=src[:src.index('    for room in game.placed_rooms:room.water_level=0.0')]
prefix=prefix.replace('room-journey-v286','arrival-journey-v323').replace('james-carry-latest286','james-arrival323')
tail='''    for room in game.placed_rooms:room.water_level=0.0
    npc.movement_medium="dry"
    npc.decision_rng.seed=953
    for mode in ["bare","helmet"]:
        var gear:String="" if mode=="bare" else "diving-helmet"
        npc=game.branforth_npc;player=game.grid_view.branforth_player
        npc.helmet_equipped=mode=="helmet";npc.movement_medium="dry";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="workshop_carry";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.direction="west";npc.timer=0;npc.needs.curiosity=90
        var destination:=Vector2.INF;var start:=Vector2.INF
        for node in npc.room_nodes.get(ORIGIN,[]):
            var at:Vector2=npc.graph.get_point_position(node);var from:=at+Vector2(96,0)
            if npc.travel_segment_clear(from,at,"west") and npc.can_stand(from) and npc.can_stand(at) and (not destination.is_finite() or at.y>destination.y):destination=at;start=from
        check(destination.is_finite(),"Collision-clear actual workshop approach")
        if not destination.is_finite():quit(2);return
        npc.foot=start;npc.path=PackedVector2Array([destination]);npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
        player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0;player.return_plan.clear();player.last_source.clear()
        game.visual_time_seconds=100;game.paused=false
        var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
        var captures:Array=[await capture(mode+"-carry-entry-000",npc)]
        var ticks:=0
        while not npc.path.is_empty() and ticks<4000:
            npc.update(game,.005);game.visual_time_seconds+=.005;ticks+=1
            game.grid_view._get_branforth_frame(game)
        check(npc.stage=="workshop_unload" and npc.state=="idle" and npc.direction=="north" and npc.workshop_arrival_origin=="west","Movement automatically enters remembered west arrival")
        check(npc.foot.distance_to(destination)<.01,"Carrying route reaches physical target")
        var seen:Dictionary={};var checkpoints:Array=[];var trace:Array=[]
        var until_end:=0
        while npc.stage=="workshop_unload" and until_end<450:
            var clock:float=npc.action_elapsed()
            var plan:Dictionary=preload("res://scripts/james_workshop_arrival.gd").presentation(npc,player,clock,gear)
            check(not plan.is_empty(),"Actual arrival remains eligible")
            if plan.is_empty():quit(2);return
            var tex:Texture2D=game.grid_view._get_branforth_frame(game)
            var index:int=bank[plan.key].find(tex)
            check(index>=0,"Grid selects exact normal arrival source")
            check(npc.foot.distance_to(destination)<.01,"Feet remain physically stationary throughout turn/unload")
            var slot:String=plan.key+":"+str(index)
            if not seen.has(slot):
                seen[slot]=true;captures.append(await capture(mode+"-"+plan.key+"-"+str(index),npc))
            trace.append({"elapsed":clock,"key":plan.key,"index":index,"foot":[npc.foot.x,npc.foot.y]})
            var checkpoint:String="turn" if clock>=.405 and clock<.8 else "unload" if clock>=1.105 else ""
            if not checkpoint.is_empty() and not checkpoints.has(checkpoint):
                checkpoints.append(checkpoint);game.paused=true
                var actor_before:Dictionary=npc.snapshot();var playback_before:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var visual:float=game.visual_time_seconds
                var save=preload("res://scripts/run_save.gd");var path:String="user://arrival323-"+mode+"-"+checkpoint+".loop"
                var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
                check(problem.is_empty(),"Full arriving checkpoint shape: "+problem)
                if not problem.is_empty():quit(2);return
                check(save.write(game,path)==OK,"Arrival actual disk write");data=save.read(path)
                root.remove_child(game);game.queue_free();await process_frame
                game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-arrival323.meta";game.run_save_path=path
                root.add_child(game);current_scene=game
                while not game.startup_complete:await process_frame
                game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
                check(await save.restore_staged(game,data),"Fresh normal scene restores arriving checkpoint without candidate reinstall")
                game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
                npc=game.branforth_npc;player=game.grid_view.branforth_player;bank=player.frames if gear.is_empty() else player.equipment_frames[gear]
                check(npc.snapshot()==actor_before,"Full arrival actor exact after fresh-scene restore")
                check(player.snapshot()==playback_before,"Arrival playback state exact")
                check(game.paused and game.visual_time_seconds==visual,"Arrival pause/visual clock exact")
                check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Exact normal arriving pose after disk restore")
                game._process(.5);check(npc.snapshot()==actor_before and game.visual_time_seconds==visual,"Paused fresh arrival does not advance")
                captures.append(await capture(mode+"-"+checkpoint+"-after-resume",npc));game.paused=false
            npc.update(game,.005);game.visual_time_seconds+=.005;until_end+=1
        check(npc.stage!="workshop_unload" and npc.workshop_arrival_origin.is_empty(),"Completed arrival releases remembered origin")
        check(checkpoints.size()==2,"Mid-turn and mid-unload fresh-scene disk restores")
        var expected_slots:int=bank["carry-turn-west-north"].size()+bank["unload-north"].size()
        check(seen.size()==expected_slots,"All authored normal turn/unload slots observed")
        captures.append(await capture(mode+"-finished",npc))
        results.append({"gear":gear,"carryTicks":ticks,"arrivalTicks":until_end,"observedSlots":seen.keys(),"checkpoints":checkpoints,"captures":captures})
        traces.append({"gear":gear,"samples":trace})
    var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Prescribed collision-clear96-unit routes through actual update/move/arrive, normal paired banks, turn/unload completion and4fresh-scene whole-run disk restores. Not autonomous goal choice, title-screen Continue or continuous visual acceptance."},"  "))
    var trace_file:=FileAccess.open(OUT+"arrival-trace.json",FileAccess.WRITE);trace_file.store_string(JSON.stringify(traces))
    if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):var uid:=FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES ARRIVAL JOURNEY: ",checks," checks; ",failures," failures; routes ",results.size())
    quit(1 if failures else 0)
'''
(o/'native_probe.gd').write_text(prefix+tail,encoding='utf-8')
files=[o/'native_probe.gd',r/'scripts/branforth_npc.gd',r/'scripts/james_workshop_arrival.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/james_cargo_player.gd',r/'character/james-cargo-return-bridges-v1/return_actor.gd',r/'scripts/run_save.gd']
(o/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},candidateBanksLoaded=False),indent=2)+'\n',encoding='utf-8')
print('323 prescribed actual movement, normal-bank arrival and fresh-scene disk probes prepared.')
