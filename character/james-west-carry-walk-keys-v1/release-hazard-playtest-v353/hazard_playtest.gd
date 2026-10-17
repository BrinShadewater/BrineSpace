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
    check(crop.save_png(out+file)==OK,"Native hazard capture saved")
    records.append({"file":file,"case":label,"time":game.visual_time_seconds,"stage":npc.stage,"state":npc.animation_state(),"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"phase":game.grid_view.branforth_player.phase,"source":game.grid_view.branforth_player.last_source.duplicate(true)})
func run()->void:
    check(not OS.is_debug_build(),"Actual release template")
    out=ProjectSettings.globalize_path("user://hazard353/");DirAccess.make_dir_recursive_absolute(out)
    var old=get_tree().current_scene
    if old!=null:old.set_process(false);old.queue_free();get_tree().current_scene=null
    await get_tree().process_frame
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
    game.meta.save_path="user://hazard353.meta";game.run_save_path="user://hazard353.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
    get_tree().root.add_child(game);get_tree().current_scene=game
    while not game.startup_complete:await get_tree().process_frame
    game.set_process(false);game.tick_timer.stop();game.paused=false;game.crew_comms.set_process(false);game.crew_comms.dismiss()
    var store=load("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
    game.running=true;game.Architects.advance_core(game,10)
    for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
    game.test_walker_cell=Vector2i(-1,-1);game.hand_panel.hide();game.card_drag.hide()
    game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
    for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
        var room:Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
        room.pos=ORIGIN+offset;room.rotation=0;room.water_level=.95
        game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
    var npc=game.branforth_npc;var player=game.grid_view.branforth_player
    check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Packaged normal James selection")
    var cases:Array=[]
    for gear in ["bare","helmet"]:
        for direction in ["north","east","south","west"]:
            for outcome in ["recovery","fatal"]:
                game.crew_count=2;game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
                for room in game.placed_rooms:room.water_level=.95
                npc.rebuild(game);npc.active=true;npc.dead=false;npc.goal="";npc.stage="";npc.state="idle";npc.timer=100;npc.path.clear();npc.expedition.clear();npc.direction=direction;npc.helmet_equipped=gear=="helmet";npc.movement_medium="flooded"
                npc.air_recovery=0;npc.air_was_low=false;npc.tank_oxygen=4;npc.breath_oxygen=4;npc.starvation=0;npc.locker_request.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
                npc.set_meta("flood_safety_wait",0.0);npc.set_meta("flood_blocked_warning",false)
                var foot:=Vector2.INF
                for node in npc.room_nodes.get(ORIGIN,[]):
                    var point:Vector2=npc.graph.get_point_position(node)
                    npc.foot=point
                    if npc.can_stand(point) and load("res://scripts/crew_life.gd").clear(npc,"swim-distress"):foot=point;break
                check(foot.is_finite(),"Actual furniture admits full distress silhouette "+gear+" "+direction)
                if not foot.is_finite():continue
                npc.foot=foot
                player.current_key="";player.motion.clear();player.return_plan.clear();player.last_source.clear();player.last_time=-1;player.phase=0;player.current_equipment="diving-helmet" if gear=="helmet" else ""
                game.resources.oxygen=100;game.resources.food=100;game.visual_time_seconds=100
                var label:String=gear+"-"+direction+"-"+outcome
                var states:Array=[];var frames:=0;var recovered:=false;var was_dead:=false
                for tick in range(420):
                    if outcome=="recovery" and tick==90:
                        for room in game.placed_rooms:room.water_level=0.0
                    if not npc.dead:load("res://scripts/room_flooding.gd").step_crew(game,npc,"branforth",1.0/60.0)
                    if game.summary_layer.visible:
                        print("HAZARD FIXTURE END reason=",game.summary_outcome_label.text," crew=",game.crew_count," recovered=",game.recovered_crew," unpowered=",game.unpowered_rooms," integrity=",game.resources.integrity)
                        get_tree().quit(2);return
                    npc.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0
                    game.crew_comms.dismiss()
                    game.grid_view._get_branforth_frame_source(game)
                    var state:String=npc.animation_state()
                    if not states.has(state):states.append(state)
                    recovered=recovered or state=="recover-air"
                    was_dead=was_dead or npc.dead
                    if tick%6==0:await capture(npc,label,frames);frames+=1
                check(states.has("swim-distress"),"Survival exhaustion admits selected distress")
                if outcome=="recovery":
                    check(recovered and not npc.dead and npc.air_recovery==0 and npc.movement_medium=="dry","Breathable air triggers finite recovery without death")
                else:
                    check(was_dead and npc.animation_state()=="death-water","Natural oxygen exhaustion dispatches water death")
                cases.append({"case":label,"states":states,"dead":npc.dead,"recoveryCompleted":recovered and npc.air_recovery==0,"frames":frames,"foot":[foot.x,foot.y]})
    FileAccess.open(out+"review.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":records,"scope":"Exact V351 release survival step_crew and actor update, natural low-air/death dispatch. Scripted initial low reserves/flooding and recovery drain; fixed60Hz clocks,10Hz native captures. Not autonomous route selection, exterior excursion or whole-game water propagation."},"\t"))
    print("JAMES PACKAGED HAZARD checks=",checks," failures=",failures," cases=",cases.size()," captures=",records.size());get_tree().quit(1 if failures else 0)
