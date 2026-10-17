from pathlib import Path
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';review=bank/'release-expedition-playtest-v355';review.mkdir(exist_ok=True)
previous=(bank/'release-escape-playtest-v354/escape_playtest.gd').read_text();head=previous[:previous.index('func run()->void:')]
head=head.replace('Native escape capture saved','Native expedition capture saved')
head=head.replace('"stage":npc.stage','"stage":npc.stage,"tripPhase":npc.expedition.get("phase","complete"),"medium":npc.movement_medium,"tank":npc.tank_oxygen,"airlock":game.occupied.get(home,{}).get("airlock_cycle",{}).duplicate(true)')
head=head.replace('var out:String','var home:Vector2i\nvar out:String')
body='''func run()->void:
    check(not OS.is_debug_build(),"Actual release template")
    out=ProjectSettings.globalize_path("user://expedition355/");DirAccess.make_dir_recursive_absolute(out)
    var old=get_tree().current_scene
    if old!=null:old.set_process(false);old.queue_free();get_tree().current_scene=null
    await get_tree().process_frame
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
    game.meta.save_path="user://expedition355.meta";game.run_save_path="user://expedition355.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
    get_tree().root.add_child(game);get_tree().current_scene=game
    while not game.startup_complete:await get_tree().process_frame
    game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
    var store=load("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
    var cases:Array=[]
    var Trips=load("res://scripts/crew_expedition.gd");var Cycle=load("res://scripts/airlock_cycle.gd")
    for rotation in range(4):
        game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
        game.crew_comms.dismiss();game.hand_panel.hide();game.card_drag.hide()
        var outward:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][rotation]
        var across:=Vector2i(-outward.y,outward.x)
        home=ORIGIN+outward;var target:Vector2i=ORIGIN+outward*2+across
        for step in range(1,4):
            for side in [0,1]:game.wrecks.erase(ORIGIN+outward*step+across*side)
        game._place_room("airlock",home,true);game.occupied[home].rotation=rotation;game.powered_room_cells[home]=true
        game.resources.oxygen=50;game.resources.food=50;game.resources.metal=5;game.resources.data=0
        game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)};game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
        var npc=game.branforth_npc;var player=game.grid_view.branforth_player
        npc.rebuild(game);npc.active=true;npc.dead=false;npc.state="idle";npc.stage="";npc.goal="";npc.path.clear();npc.expedition.clear();npc.movement_medium="dry";npc.helmet_equipped=true;npc.tank_oxygen=60;npc.breath_oxygen=15;npc.air_recovery=0;npc.air_was_low=false;npc.starvation=0;npc.locker_request.clear()
        var start:=Vector2.INF
        for node in npc.room_nodes.get(ORIGIN,[]):
            var point:Vector2=npc.graph.get_point_position(node)
            if npc.can_stand(point):start=point;break
        check(start.is_finite(),"Actual core has clear starting floor")
        if not start.is_finite():get_tree().quit(2);return
        npc.foot=start
        for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false;peer.expedition.clear()
        game.test_walker_cell=Vector2i(-1,-1)
        check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Packaged normal James selection")
        var reason:String=Trips.reason(game,"branforth",home)
        check(Trips.dispatch(game,"branforth",home),"Real expedition dispatch "+reason)
        if npc.expedition.is_empty():print("JAMES DISPATCH FAIL rotation=",rotation," reason=",reason);get_tree().quit(2);return
        var phases:Array=[];var keys:Array=[];var frames:=0;var delivered:=false;var previous:="";var label:String="helmet-rotation-"+str(rotation)
        for tick in range(5400):
            if npc.expedition.is_empty():delivered=true;break
            var phase:String=npc.expedition.phase
            if not phases.has(phase):phases.append(phase)
            check(game.resources.metal==5 and game.resources.data==0,"Cargo credited only after safe return")
            game.visual_time_seconds+=1.0/60.0;Cycle.advance(game,1.0/60.0);game._update_test_walker(1.0/60.0)
            game.crew_comms.dismiss();game.grid_view._get_branforth_frame_source(game)
            var key:String=player.last_source.get("key","")
            if not keys.has(key):keys.append(key)
            if npc.dead or game.summary_layer.visible:check(false,"Expedition remains alive without loop report");break
            var moving:bool=phase in ["approach","enter","leave","outbound","salvage","pickup","return","entry","exit","unload"]
            if phase!=previous or tick%(6 if moving else 30)==0:await capture(npc,label,frames);frames+=1
            previous=phase
        await capture(npc,label,frames);frames+=1
        check(delivered and npc.expedition.is_empty() and not npc.dead and npc.movement_medium=="dry","Real exterior mission completes alive through dry chamber")
        check(game.drone_fleet.sites[target].units==2,"Exactly one salvage unit collected")
        check(game.resources.metal==6 and game.resources.data==1,"Exactly one salvage load delivered")
        check(phases.size()==Trips.PHASES.size(),"All twelve normal expedition phases reached")
        cases.append({"case":label,"rotation":rotation,"phases":phases,"sources":keys,"frames":frames,"delivered":delivered,"tank":npc.tank_oxygen,"siteUnits":game.drone_fleet.sites[target].units,"metal":game.resources.metal,"data":game.resources.data})
        if failures:break
    FileAccess.open(out+"review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Exact V351 release dispatch, normal main crew update including survival, airlock cycle, exterior routing/extraction/cargo return and actual delivery credit. Four airlock rotations, helmet required. Fixture-created nearby salvage sites, scripted starting contact, fixed60Hz updates,10Hz active/2Hz waiting native captures. Not random expedition ecology, real-time pacing, long-session traffic or loaded checkpoint interruption."},"\\t"))
    print("JAMES PACKAGED EXPEDITION checks=",checks," failures=",failures," cases=",cases.size()," captures=",records.size());get_tree().quit(1 if failures else 0)
'''
(review/'expedition_playtest.gd').write_text(head+body)
runner=(bank/'run_escape_playtest_v354.py').read_text().replace('release-escape-playtest-v354','release-expedition-playtest-v355').replace('james-escape-playtest-v354','james-expedition-playtest-v355').replace('JamesEscapePlaytest','JamesExpeditionPlaytest').replace('escape_playtest.gd','expedition_playtest.gd').replace('escape354','expedition355')
(bank/'run_expedition_playtest_v355.py').write_text(runner)
print('Prepared packaged complete exterior expeditions')
