from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'room-journey-v45';out.mkdir(exist_ok=True)
old=(r/'character/james-diagnostics-edge-matte-v30/native-arrival-continue.gd').read_text(encoding='utf-8')
prefix=old.split('\tvar baseline:bool=false')[0].replace('character/james-diagnostics-edge-matte-v30/','character/james-west-carry-walk-keys-v1/room-journey-v45/').replace('JAMES TABLET ARRIVAL CONTINUE BOOT','JAMES CARRY ROOM JOURNEY BOOT').replace('james-tablet-arrival','james-carry-journey').replace('"maintenance_bay"','"salvage_workshop"')
tail='''
    for room in game.placed_rooms:room.water_level=0.0
    npc.movement_medium="dry"
    player.load_manifest("res://character/james-west-carry-walk-keys-v1/master-head-review-v16/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/james-west-carry-walk-keys-v1/master-head-review-v16/helmet-manifest.json"),"Staged49paired walk loaded on normal cargo player")
    for mode in ["bare","helmet"]:
        var gear:String="" if mode=="bare" else "diving-helmet"
        npc.helmet_equipped=mode=="helmet";npc.movement_medium="dry";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="workshop_carry";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.direction="west";npc.timer=0;npc.needs.curiosity=90
        var destination:=Vector2.INF;var start:=Vector2.INF
        for node in npc.room_nodes.get(ORIGIN,[]):
            var at:Vector2=npc.graph.get_point_position(node);var from:=at+Vector2(96,0)
            if npc.travel_segment_clear(from,at,"west") and npc.can_stand(from) and npc.can_stand(at):destination=at;start=from;break
        check(destination.is_finite(),"Real collision-clear west workshop carrying route")
        if not destination.is_finite():quit(2);return
        npc.foot=start;npc.path=PackedVector2Array([destination]);npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
        player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0;player.return_plan.clear();player.last_source.clear()
        game.visual_time_seconds=100;game.paused=false
        var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
        var initial:Texture2D=game.grid_view._get_branforth_frame(game)
        check(initial==frames["carry-west"][0],"Actual grid begins on staged carrying0")
        var captures:Array=[await capture(mode+"-entry-000",npc)]
        var seen:Dictionary={0:true};var ticks:=0;var resumed:=false;var quarter_captured:=false
        while not npc.path.is_empty() and ticks<4000:
            npc.update(game,.005);game.visual_time_seconds+=.005;ticks+=1
            var tex:Texture2D=game.grid_view._get_branforth_frame(game)
            if npc.stage!="workshop_carry":break
            check(npc.direction=="west" and npc.goal=="curiosity" and npc.helmet_equipped==(mode=="helmet"),"Normal carry heading/goal/equipment stable")
            var index:int=frames["carry-west"].find(tex)
            check(index>=0,"Actual grid consumes staged49 source through ordinary NPC update")
            seen[index]=true
            check(tex.get_meta("crew_pivot")==Vector2(128,224) and tex.get_meta("crew_standing_height")==148.0,"World carrying pivot/ruler stable")
            if not quarter_captured and npc.foot.distance_to(start)>=24:
                captures.append(await capture(mode+"-quarter",npc));quarter_captured=true
            if not resumed and npc.foot.distance_to(start)>=48:
                captures.append(await capture(mode+"-before-continue",npc));game.paused=true
                var before_actor:Dictionary=npc.snapshot();var before_playback:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var clock:float=game.visual_time_seconds
                var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-carry-journey.loop";var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
                check(problem.is_empty(),"Staged walk normal checkpoint shape: "+problem)
                if not problem.is_empty():quit(2);return
                check(save.write(game,scratch_path)==OK,"Actual cargo checkpoint disk write");data=save.read(scratch_path)
                root.remove_child(game);game.queue_free();await process_frame
                game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-carry-journey.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
                root.add_child(game);current_scene=game
                while not game.startup_complete:await process_frame
                game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
                player=game.grid_view.branforth_player
                player.load_manifest("res://character/james-west-carry-walk-keys-v1/master-head-review-v16/bare-manifest.json",true)
                check(player.load_equipment_manifest("diving-helmet","res://character/james-west-carry-walk-keys-v1/master-head-review-v16/helmet-manifest.json"),"Explicit candidate bank reinstalled before restore")
                check(await save.restore_staged(game,data),"Actual fresh-scene cargo disk restore")
                game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
                npc=game.branforth_npc;player=game.grid_view.branforth_player;frames=player.frames if gear.is_empty() else player.equipment_frames[gear]
                check(npc.snapshot()==before_actor,"Cargo actor exact across disk restore")
                check(player.snapshot()==before_playback,"Cargo playback exact across disk restore")
                check(game.paused and game.visual_time_seconds==clock,"Cargo pause/clock exact")
                check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Staged cargo pose exact after explicit bank reinstall")
                game._process(.5);check(npc.snapshot()==before_actor and game.visual_time_seconds==clock,"Paused cargo resume stays fixed")
                captures.append(await capture(mode+"-after-continue",npc));game.paused=false;game.set_process(false);resumed=true
        check(npc.foot.distance_to(destination)<.01 and npc.path.is_empty(),"Actual west route completes")
        check(npc.stage=="workshop_unload" and npc.direction=="north","Normal arrival selects north unload")
        check(seen.size()==49,"All49new walking source slots observed in actual room journey")
        check(resumed,"Midroute disk resume exercised")
        captures.append(await capture(mode+"-unload-entry",npc))
        npc.update(game,.4);game.visual_time_seconds+=.4;game.grid_view._get_branforth_frame(game)
        captures.append(await capture(mode+"-unload-held",npc))
        results.append({"gear":gear,"ticks":ticks,"observedWalkSlots":seen.keys(),"freshSceneDiskResume":resumed,"captures":captures,"normalUnloadFacing":npc.direction})
    var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Two prescribed collision-clear96world-unit dry west workshop carrying routes, normal JamesNPC.update/move/arrive and actual grid using staged49 walking bank. Explicit bank reinstall before fresh-scene disk restore. No prep lifecycle, autonomous scheduler, normal adoption/binding, title fresh-process Continue or complete unload material acceptance."},"  "))
    if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):
        var uid_file:=FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES CARRY ROOM JOURNEY: ",checks," checks; ",failures," failures; routes ",results.size())
    quit(1 if failures else 0)
'''
program=prefix.replace('\t','    ')+tail;(out/'native_probe.gd').write_text(program,encoding='utf-8')
files=[out/'native_probe.gd',Path(__file__),r/'scripts/grid_canvas.gd',r/'scripts/james_cargo_player.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/james_cargo_checkpoint.gd',r/'scripts/run_save.gd',r/'character/ACTIVE_ASSETS.json',p/'finite-handoff-v44/review-acceptance.json']
for mode in ['bare','helmet']:
    manifest=p/'master-head-review-v16'/(mode+'-manifest.json');files.append(manifest);pack=json.loads(manifest.read_bytes());files += [r/f.removeprefix('res://') for f in pack['states'][0]['frameFiles']]
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},normalChanged=False),indent=2)+'\n')
print('V45 actual NPC/grid west cargo room-route and staged fresh-scene disk-resume fixture frozen.')
