from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'pickup-runtime-v47';out.mkdir(exist_ok=True)
prefix=(p/'room-journey-v46/native_probe.gd').read_text(encoding='utf-8').split('    for room in game.placed_rooms:room.water_level=0.0\n')[0].replace('room-journey-v46/','pickup-runtime-v47/').replace('james-carry-open-floor','james-pickup-runtime').replace('JAMES CARRY ROOM JOURNEY BOOT','JAMES PICKUP RUNTIME BOOT')
tail='''
    for room in game.placed_rooms:room.water_level=0.0
    npc.movement_medium="dry"
    var contact:=Vector2.INF
    for node in npc.room_nodes.get(ORIGIN,[]):
        var at:Vector2=npc.graph.get_point_position(node)
        if npc.can_stand(at) and (not contact.is_finite() or at.y>contact.y):contact=at
    check(contact.is_finite(),"Actual clear workshop floor contact")
    if not contact.is_finite():quit(2);return
    for mode in ["bare","helmet"]:
        for facing in ["west","east","north","south"]:
            var gear:String="" if mode=="bare" else "diving-helmet"
            npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.movement_medium="dry";npc.expedition.clear();npc.foot=contact;npc.path.clear();npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.direction=facing;npc.stage="workshop_work";npc.state="interact";npc.timer=.001;npc.needs={"hunger":5.0,"fatigue":5.0,"curiosity":90.0,"maintenance":5.0}
            npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF;player.return_plan.clear();player.last_source.clear();player.current_key="";player.motion.clear();player.last_time=-1;game.visual_time_seconds=100;game.paused=false;game.powered_room_cells[ORIGIN]=true
            npc.update(game,.002)
            check(npc.stage=="workshop_pickup" and npc.timer==.52 and npc.state=="idle","Actual workshop work completion enters pickup")
            check(npc.animation_state()=="pickup" and npc.action_elapsed()==0,"Normal pickup animation hook starts simulation clock")
            var frames:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var key:String="pickup-"+facing;var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
            check(frames[key].size()==6 and absf(player.cycle_seconds(key,gear)-.52)<.000001,"Original six-frame520ms pickup selected")
            var captures:Array=[];var elapsed:=0.0;var previous:=0.0;var resumed:=false
            for index in range(6):
                var sample:float=elapsed+float(clocks[key].durations[index])/2000.0
                npc.update(game,sample-previous);previous=sample;game.visual_time_seconds=100+sample
                var tex:Texture2D=game.grid_view._get_branforth_frame(game)
                check(npc.stage=="workshop_pickup" and npc.foot==contact and npc.path.is_empty(),"Pickup holds real room foot")
                check(absf(npc.action_elapsed()-sample)<.000001,"Pickup follows simulation timer")
                check(tex==frames[key][index],"Actual normal grid selects exact pickup source")
                check(game.grid_view._get_branforth_frame(game)==tex,"Repeated drawing does not advance pickup")
                if index in [0,2,5]:captures.append(await capture(mode+"-"+facing+"-"+str(index).pad_zeros(3),npc))
                if index==2 and facing=="west":
                    game.paused=true;var actor:Dictionary=npc.snapshot();var playback:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var clock:float=game.visual_time_seconds
                    var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-pickup-runtime.loop";var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
                    check(problem.is_empty(),"Normal pickup checkpoint admits actual stage: "+problem)
                    if not problem.is_empty():quit(2);return
                    for mutation in [{"state":"walk"},{"timer":.53},{"timer":-1.0},{"movement_medium":"flooded"},{"dead":true},{"path":PackedVector2Array([contact+Vector2.ONE])}]:
                        var invalid:Dictionary=actor.duplicate(true)
                        for field in mutation:invalid[field]=mutation[field]
                        check(not preload("res://scripts/branforth_npc.gd").valid_branforth_snapshot(invalid),"Malformed/nonstationary pickup checkpoint rejected")
                    check(save.write(game,scratch_path)==OK,"Normal pickup checkpoint disk write");data=save.read(scratch_path)
                    root.remove_child(game);game.queue_free();await process_frame
                    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-pickup-runtime.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
                    root.add_child(game);current_scene=game
                    while not game.startup_complete:await process_frame
                    game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
                    check(await save.restore_staged(game,data),"Actual fresh-scene normal pickup Continue")
                    game.run_save_path=scratch_path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);npc=game.branforth_npc;player=game.grid_view.branforth_player;frames=player.frames if gear.is_empty() else player.equipment_frames[gear];clocks=player.timing if gear.is_empty() else player.equipment_timing[gear]
                    check(npc.snapshot()==actor and player.snapshot()==playback,"Pickup actor/playback exact after normal restore")
                    check(game.paused and game.visual_time_seconds==clock,"Pickup pause/clock exact")
                    check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Pickup pose pixels exact without candidate reinstall")
                    game._process(.5);check(npc.snapshot()==actor and game.visual_time_seconds==clock,"Paused pickup Continue does not advance")
                    game.paused=false;game.set_process(false);resumed=true
                elapsed+=float(clocks[key].durations[index])/1000.0
            npc.update(game,.521-previous);game.visual_time_seconds=100.521
            check(npc.stage=="workshop_carry" and not npc.path.is_empty(),"Existing workshop route starts after full pickup")
            check(npc.animation_state()=="carry" and npc.action_elapsed()<0,"Pickup clock releases to ordinary carrying")
            results.append({"mode":mode,"facing":facing,"normalPickupSlots":6,"diskResume":resumed,"captures":captures,"terminalStage":npc.stage})
    check(results.size()==8,"Eight normal pickup direction/gear cases")
    var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Actual normal James workshop_work timer completion, all48dry pickup source samples through NPC.update/grid in four directions/both gears, two fresh-scene midpoint disk Continues without candidate reinstall, malformed snapshot rejection, existing pickup-to-carry route. Explicit room contact, no autonomous scheduler, title fresh-process Continue, prep/arrival-turn or full visual source acceptance."},"  "))
    if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):
        var uid_file:=FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES PICKUP RUNTIME: ",checks," checks; ",failures," failures; cases ",results.size())
    quit(1 if failures else 0)
'''
(out/'native_probe.gd').write_text(prefix+tail,encoding='utf-8')
files=[out/'native_probe.gd',Path(__file__),r/'scripts/bill_npc.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/branforth_npc.gd',r/'scripts/run_save.gd',r/'scripts/grid_canvas.gd',r/'character/ACTIVE_ASSETS.json']
for mode in ['bare','helmet']:
    manifest=r/'character/james-cargo-material-joined-v1'/(mode+'-manifest.json');files.append(manifest);pack=json.loads(manifest.read_bytes());files += [manifest.parent/f for s in pack['states'] if s['id'].startswith('pickup-') for f in s['frameFiles']]
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},normalRuntimeChanged=True,normalArtSelectionChanged=False),indent=2)+'\n')
print('V47 normal pickup lifecycle/clock/source/validation/Continue fixture frozen.')
