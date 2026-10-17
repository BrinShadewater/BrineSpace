extends Node
const ORIGIN=Vector2i(20,20)
var game
var checks:=0
var failures:=0
var records:Array=[]
var resume_records:Array=[]
var home:Vector2i
var out:String
func check(ok:bool,label:String)->void:
    checks+=1
    if not ok:failures+=1;push_error(label)
func _ready()->void:
    var isolated:bool="brine-james-release-" in OS.get_environment("APPDATA") and OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/")
    if not isolated:push_error("Resolved scratch APPDATA required");get_tree().quit(2);return
    var uid_path:String=get_script().resource_path+".uid"
    if not FileAccess.file_exists(uid_path):FileAccess.open(uid_path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
    call_deferred("run")
func capture(npc,label:String,index:int)->void:
    check(not game.summary_layer.visible,"Hazard animation is unobscured by expedition report")
    var root=get_tree().root
    var center:Vector2=npc.foot/384.0*game.get_cell_size()
    game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
    game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
    game.grid_view.queue_redraw();await get_tree().process_frame;await RenderingServer.frame_post_draw
    var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(center-Vector2.ONE*game.get_cell_size()*.55,Vector2.ONE*game.get_cell_size()*1.1)
    var screenshot:Image=root.get_texture().get_image()
    var crop:Image=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
    var file:String=label+"-%04d.png"%index
    check(crop.save_png(out+file)==OK,"Native expedition capture saved")
    records.append({"file":file,"case":label,"time":game.visual_time_seconds,"stage":npc.stage,"tripPhase":npc.expedition.get("phase","complete"),"medium":npc.movement_medium,"tank":npc.tank_oxygen,"airlock":game.occupied.get(home,{}).get("airlock_cycle",{}).duplicate(true),"state":npc.animation_state(),"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"phase":game.grid_view.branforth_player.phase,"source":game.grid_view.branforth_player.last_source.duplicate(true)})
func run()->void:
    check(not OS.is_debug_build(),"Actual release template")
    out=ProjectSettings.globalize_path("user://resume357/");DirAccess.make_dir_recursive_absolute(out)
    var old=get_tree().current_scene
    if old!=null:old.set_process(false);old.queue_free();get_tree().current_scene=null
    await get_tree().process_frame
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
    game.meta.save_path="user://resume357.meta";game.run_save_path="user://resume357.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
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
        var resumed:Array=[];var phases:Array=[];var keys:Array=[];var frames:=0;var delivered:=false;var previous:="";var label:String="helmet-rotation-"+str(rotation)
        for tick in range(5400):
            if npc.expedition.is_empty():delivered=true;break
            var phase:String=npc.expedition.phase
            if not phases.has(phase):phases.append(phase)
            if phase in ["return","drain"] and not resumed.has(phase):
                resumed.append(phase)
                await capture(npc,label,frames);frames+=1
                var before:Dictionary={"phase":phase,"foot":npc.foot,"trip":npc.expedition.duplicate(true),"tank":npc.tank_oxygen,"helmet":npc.helmet_equipped,"units":game.drone_fleet.sites[target].units,"metal":game.resources.metal,"data":game.resources.data}
                var Save=load("res://scripts/run_save.gd")
                var save_path:String="user://resume357-"+str(rotation)+"-"+phase+".loop"
                check(Save.write(game,save_path)==OK,"Loaded expedition checkpoint writes: "+Save.last_error)
                var checkpoint:Dictionary=Save.read(save_path)
                check(not checkpoint.is_empty(),"Disk checkpoint reads: "+Save.last_error)
                if checkpoint.is_empty():get_tree().quit(2);return
                game.set_process(false);game.tick_timer.stop();game.queue_free();get_tree().current_scene=null
                await get_tree().process_frame
                Save.pending=checkpoint
                game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
                game.meta.save_path="user://resume357.meta";game.run_save_path=save_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
                get_tree().root.add_child(game);get_tree().current_scene=game
                while not game.startup_complete:await get_tree().process_frame
                game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
                check(game.paused,"Normal staged Continue starts paused")
                check(game.run_save_path==save_path,"Continue keeps checkpoint in scratch folder")
                npc=game.branforth_npc;player=game.grid_view.branforth_player
                check(npc.expedition==before.trip,"Loaded expedition payload and route survive fresh scene")
                check(npc.foot.distance_to(before.foot)<.001,"Exact exterior floor contact restored")
                check(is_equal_approx(npc.tank_oxygen,before.tank) and npc.helmet_equipped==before.helmet,"Tank and helmet survive Continue")
                check(game.drone_fleet.sites[target].units==before.units and game.resources.metal==before.metal and game.resources.data==before.data,"Checkpoint does not duplicate or prematurely deliver salvage")
                check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Continue retains selected normal James player")
                game.run_save_path=save_path;game.paused=false;game.hand_panel.hide();game.card_drag.hide()
                await capture(npc,label,frames);frames+=1
                resume_records.append({"case":label,"phase":phase,"beforeFrame":frames-2,"afterFrame":frames-1,"footError":npc.foot.distance_to(before.foot),"tank":npc.tank_oxygen,"cargo":npc.expedition.get("cargo",{}).duplicate(true)})
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
        check(resumed.size()==2,"Both loaded return and airlock drain resume tested")
        cases.append({"resumed":resumed,"case":label,"rotation":rotation,"phases":phases,"sources":keys,"frames":frames,"delivered":delivered,"tank":npc.tank_oxygen,"siteUnits":game.drone_fleet.sites[target].units,"metal":game.resources.metal,"data":game.resources.data})
        if failures:break
    FileAccess.open(out+"review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"resumes":resume_records,"scope":"Exact V351 release dispatch, normal main crew update including survival, airlock cycle, exterior routing/extraction/cargo return and actual delivery credit. Four airlock rotations, helmet required. Fixture-created nearby salvage sites, scripted starting contact, fixed60Hz updates,10Hz active/2Hz waiting native captures. Two disk checkpoints per journey restored into fresh scenes via normal staged Continue: loaded return and airlock drain. Not title-button interaction, process restart, random expedition ecology, real-time pacing or long-session traffic."},"\t"))
    print("JAMES PACKAGED RESUME checks=",checks," failures=",failures," cases=",cases.size()," captures=",records.size());get_tree().quit(1 if failures else 0)
