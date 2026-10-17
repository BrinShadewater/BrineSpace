extends Node
const ORIGIN=Vector2i(20,20)
var game
var checks:=0
var failures:=0
var records:Array=[]
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
    var root=get_tree().root
    var center:Vector2=npc.foot/384.0*game.get_cell_size()
    game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
    game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
    game.grid_view.queue_redraw();await get_tree().process_frame;await RenderingServer.frame_post_draw
    var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(center-Vector2.ONE*game.get_cell_size()*.55,Vector2.ONE*game.get_cell_size()*1.1)
    var screenshot:Image=root.get_texture().get_image()
    var crop:Image=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
    var file:String=label+"-%04d.png"%index
    check(crop.save_png(out+file)==OK,"Native workshop movie capture saved")
    records.append({"file":file,"case":label,"time":game.visual_time_seconds,"stage":npc.stage,"state":npc.animation_state(),"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"phase":game.grid_view.branforth_player.phase,"source":game.grid_view.branforth_player.last_source.duplicate(true)})
func run()->void:
    check(not OS.is_debug_build(),"Actual release template")
    out=ProjectSettings.globalize_path("user://unload363/");DirAccess.make_dir_recursive_absolute(out)
    var old=get_tree().current_scene
    if old!=null:old.set_process(false);old.queue_free();get_tree().current_scene=null
    await get_tree().process_frame
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
    game.meta.save_path="user://unload363.meta";game.run_save_path="user://unload363.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
    get_tree().root.add_child(game);get_tree().current_scene=game
    while not game.startup_complete:await get_tree().process_frame
    game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
    var store=load("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
    game.running=true;game.paused=false;game.Architects.advance_core(game,10)
    for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
    game.test_walker_cell=Vector2i(-1,-1);game.hand_panel.hide();game.card_drag.hide()
    var npc=game.branforth_npc;var player=game.grid_view.branforth_player
    check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Packaged normal James selection")

    # Fixture-only resequencing of exact packaged selected texture objects.
    for equipment in ["","diving-helmet"]:
        var original_bank:Dictionary=player.frames if equipment.is_empty() else player.equipment_frames[equipment]
        var original:Array=original_bank["unload-north"].duplicate()
        check(original.size()==6,"Packaged six-pose selected North unload")
        if original.size()!=6:get_tree().quit(2);return
        var proposal:Array=[]
        for index in [0,1,2,3,4,2,5]:proposal.append(original[index])
        check(proposal[0]==original[0] and proposal[-1]==original[-1],"Exact selected texture endpoints")
        original_bank["unload-north"]=proposal
        var clocks:Dictionary=player.timing if equipment.is_empty() else player.equipment_timing[equipment]
        clocks["unload-north"]={"durations":[80,100,100,90,40,40,70],"loop":false,"seconds":.52}

    var cases:Array=[]
    for rotation in range(4):
        game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear()
        var room:Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop").duplicate(true);room.pos=ORIGIN;room.rotation=rotation;room.water_level=0.0
        game.occupied[ORIGIN]=room;game.placed_rooms.append(room);game.powered_room_cells[ORIGIN]=true
        npc.rebuild(game)
        var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN])
        check(not stations.is_empty(),"Actual rotated workshop has service contact")
        if stations.is_empty():continue
        var station:Dictionary=stations[0]
        for gear in ["bare","helmet"]:
            npc.active=true;npc.dead=false;npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.stage="";npc.state="idle";npc.timer=0;npc.path.clear();npc.expedition.clear();npc.direction=station.facing;npc.movement_medium="dry";npc.helmet_equipped=gear=="helmet"
            npc.foot=(Vector2(ORIGIN)+Vector2.ONE*.5)*384+Vector2(station.point);npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF;npc.needs.curiosity=90;npc.tank_oxygen=60;npc.breath_oxygen=15;npc.starvation=0;npc.air_recovery=0
            player.current_key="";player.motion.clear();player.return_plan.clear();player.last_source.clear();player.last_time=-1;player.phase=0;player.current_equipment="diving-helmet" if gear=="helmet" else ""
            game.visual_time_seconds=100;game.paused=false
            check(npc.can_stand(npc.foot) and npc.begin_room_activity(),"Actual room dispatcher starts workshop activity")
            var label:String=gear+"-rotation-"+str(rotation);var stages:Array=[];var seen_unload:=false;var completed:=false;var travel:=0.0;var frames:=0
            for tick in range(1800):
                var previous:Vector2=npc.foot
                npc.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0
                travel+=previous.distance_to(npc.foot)
                game.grid_view._get_branforth_frame_source(game)
                if not stages.has(npc.stage):stages.append(npc.stage)
                if npc.stage=="workshop_unload":seen_unload=true
                if tick%6==0 or npc.stage=="workshop_unload":
                    await capture(npc,label,frames);frames+=1
                if seen_unload and npc.stage!="workshop_unload":completed=true;await capture(npc,label,frames);frames+=1;break
            check(completed,"Complete real pickup/carry/turn/unload lifecycle")
            check(stages.has("workshop_pickup") and stages.has("workshop_carry") and stages.has("workshop_unload") and travel>16,"Actual routed carry performed before unloading")
            cases.append({"case":label,"rotation":rotation,"gear":gear,"stages":stages,"travel":travel,"completed":completed,"frames":frames,"station":station})
            npc.active=false
    FileAccess.open(out+"review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Actual V351 Windows release actor update, route and renderer across four workshop layouts/both gears. Scripted actual service-contact entry and fixed60Hz updates;10Hz native crops. Fixture-only both-gear North unload resequencing of exact selected packaged texture objects; original mid-rise reused before standing,520ms. Four actual workshop layouts, normal actor/case renderer. 60Hz native captures during unload,10Hz other stages. No normal selection, helmet candidate, autonomous goal choice, real-time pacing, hazards, save interruption or original-master acceptance."},"\t"))
    print("JAMES CANDIDATE UNLOAD checks=",checks," failures=",failures," cases=",cases.size()," captures=",records.size());get_tree().quit(1 if failures else 0)
