from pathlib import Path
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';review=bank/'release-escape-playtest-v354';review.mkdir(exist_ok=True)
previous=(bank/'release-hazard-playtest-v353/hazard_playtest.gd').read_text()
head=previous[:previous.index('func run()->void:')]
head=head.replace('Native hazard capture saved','Native escape capture saved')
body='''func run()->void:
    check(not OS.is_debug_build(),"Actual release template")
    out=ProjectSettings.globalize_path("user://escape354/");DirAccess.make_dir_recursive_absolute(out)
    var old=get_tree().current_scene
    if old!=null:old.set_process(false);old.queue_free();get_tree().current_scene=null
    await get_tree().process_frame
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
    game.meta.save_path="user://escape354.meta";game.run_save_path="user://escape354.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
    get_tree().root.add_child(game);get_tree().current_scene=game
    while not game.startup_complete:await get_tree().process_frame
    game.set_process(false);game.tick_timer.stop();game.paused=false;game.crew_comms.set_process(false);game.crew_comms.dismiss()
    var store=load("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
    game.running=true;game.Architects.advance_core(game,10)
    for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
    game.test_walker_cell=Vector2i(-1,-1);game.hand_panel.hide();game.card_drag.hide()
    var npc=game.branforth_npc;var player=game.grid_view.branforth_player
    check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Packaged normal James selection")
    var cases:Array=[]
    for offset in [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]:
        for gear in ["bare","helmet"]:
            game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
            for cell in [ORIGIN,ORIGIN+offset]:
                var room:Dictionary=game.RoomDatabaseScript.get_room("storage_bay").duplicate(true)
                room.pos=cell;room.rotation=0;room.water_level=.95 if cell==ORIGIN else 0.0
                game.occupied[cell]=room;game.placed_rooms.append(room);game.powered_room_cells[cell]=true
            game.crew_count=2;game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
            npc.rebuild(game);npc.active=true;npc.dead=false;npc.goal="";npc.stage="";npc.state="idle";npc.timer=100;npc.path.clear();npc.expedition.clear();npc.direction="west";npc.helmet_equipped=gear=="helmet";npc.movement_medium="flooded"
            npc.air_recovery=0;npc.air_was_low=false;npc.tank_oxygen=4.8;npc.breath_oxygen=4.8;npc.starvation=0;npc.locker_request.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
            npc.swim_cells={ORIGIN:true}
            npc.set_meta("flood_safety_wait",0.0);npc.set_meta("flood_retreat_check",0.0);npc.set_meta("flood_blocked_warning",false)
            var choices:Array=[]
            for node in npc.room_nodes.get(ORIGIN,[]):choices.append(npc.graph.get_point_position(node))
            var border:Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5+Vector2(offset)*.5)*384
            choices.sort_custom(func(a,b):return a.distance_squared_to(border)<b.distance_squared_to(border))
            var foot:=Vector2.INF;var planned:Dictionary={};var shortest:=INF;var route_count:=0
            for point in choices.slice(0,16):
                npc.foot=point
                if not npc.can_stand(point):continue
                var route:Dictionary=load("res://scripts/flood_safety.gd").escape_route(game,npc)
                if not route.is_empty():shortest=minf(shortest,route.seconds);route_count+=1
                if not route.is_empty() and route.seconds<10 and route.seconds>.1:
                    foot=point;planned=route;break
            check(foot.is_finite(),"Authored connected rooms admit short refuge route "+str(offset)+gear)
            if not foot.is_finite():
                print("ESCAPE FIXTURE missing short route offset=",offset," gear=",gear," nodes=",choices.size()," routes=",route_count," shortest=",shortest," geometry=",npc.geometry[ORIGIN]);get_tree().quit(2);return
            npc.foot=foot;npc.path.clear();npc.goal="";npc.state="idle"
            npc.tank_oxygen=minf(14,planned.seconds+3.5);npc.breath_oxygen=minf(14,planned.seconds+3.5)
            player.current_key="";player.motion.clear();player.return_plan.clear();player.last_source.clear();player.last_time=-1;player.phase=0;player.current_equipment="diving-helmet" if gear=="helmet" else ""
            game.resources.oxygen=100;game.resources.food=100;game.visual_time_seconds=100
            var heading:String="north" if offset==Vector2i.UP else "east" if offset==Vector2i.RIGHT else "south" if offset==Vector2i.DOWN else "west"
            var label:String=gear+"-"+heading;var states:Array=[];var frames:=0;var retreated:=false;var recovered:=false;var arrived:=false;var travel:=0.0
            for tick in range(900):
                var before:Vector2=npc.foot
                if not npc.dead:load("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/60.0)
                npc.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0
                game.crew_comms.dismiss();game.grid_view._get_branforth_frame_source(game)
                travel+=before.distance_to(npc.foot)
                var state:String=npc.animation_state()
                if not states.has(state):states.append(state)
                retreated=retreated or npc.goal=="flood-retreat"
                recovered=recovered or state=="recover-air"
                arrived=arrived or (npc.cell_at(npc.foot)==ORIGIN+offset and npc.movement_medium=="dry")
                if tick%6==0:await capture(npc,label,frames);frames+=1
                if npc.dead or game.summary_layer.visible:check(false,"Actual escape must survive with visible station");break
                if arrived and recovered and npc.air_recovery==0 and npc.path.is_empty():break
            check(retreated and arrived and not npc.dead and travel>8,"Controller independently selects and traverses refuge route")
            check(recovered and npc.air_recovery==0,"Natural low-air recovery completes at reached dry refuge")
            cases.append({"case":label,"states":states,"frames":frames,"retreated":retreated,"arrived":arrived,"recovered":recovered,"dead":npc.dead,"travel":travel,"plannedSeconds":planned.seconds})
    FileAccess.open(out+"review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Exact V351 release flood-safety controller chooses and traverses escape route between authored storage rooms; natural recovery at dry refuge. Scripted short-route starting contacts, low reserves and fixed room water levels; fixed60Hz survival/actor updates,10Hz native capture. No assigned path or goal, scheduled drain, autonomous room generation, full-game water propagation or exterior expedition."},"\\t"))
    print("JAMES PACKAGED ESCAPE checks=",checks," failures=",failures," cases=",cases.size()," captures=",records.size());get_tree().quit(1 if failures else 0)
'''
(review/'escape_playtest.gd').write_text(head+body)
runner=(bank/'run_hazard_playtest_v353.py').read_text().replace('release-hazard-playtest-v353','release-escape-playtest-v354').replace('james-hazard-playtest-v353','james-escape-playtest-v354').replace('JamesHazardPlaytest','JamesEscapePlaytest').replace('hazard_playtest.gd','escape_playtest.gd').replace('hazard353','escape354')
(bank/'run_escape_playtest_v354.py').write_text(runner)
print('Prepared packaged controller-selected refuge routes')
