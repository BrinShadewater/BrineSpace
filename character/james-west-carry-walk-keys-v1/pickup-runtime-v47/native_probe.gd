extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-west-carry-walk-keys-v1/pickup-runtime-v47/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
    checks+=1
    if not ok:failures+=1;push_error(message)
func _init() -> void:
    print("JAMES PICKUP RUNTIME BOOT")
    call_deferred("run")
func endpoint(npc,desired: Vector2,cell: Vector2i,d: String) -> int:
    var best: int=-1;var distance: float=INF
    for node in npc.room_nodes.get(cell,[]):
        var at: Vector2=npc.graph.get_point_position(node)
        if not npc.swim_segment_clear(at,at,d,d,true):continue
        if not npc.swim_segment_clear(at,at,d,d,false,npc.action_clearance["helmet" if npc.helmet_equipped else "bare"]["transition-"+d]):continue
        if at.distance_squared_to(desired)<distance:best=node;distance=at.distance_squared_to(desired)
    return best
func capture(label: String,npc) -> String:
    game.hand_panel.hide();game.card_drag.hide()
    var center: Vector2=npc.foot/384.0*game.get_cell_size()
    game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
    game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
    game.grid_view.queue_redraw()
    await process_frame
    await RenderingServer.frame_post_draw
    var screenshot:=root.get_texture().get_image()
    var cell_size: float=game.get_cell_size()
    var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
    var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
    var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
    var file: String=OUT+"arrival-captures/"+label+".png"
    check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
    check(crop.save_png(file)==OK,"Save route capture")
    if label.ends_with("-000"):
        var texture: Texture2D=game.grid_view._get_branforth_frame(game)
        var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
        var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
        var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
        var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
        var before: PackedByteArray=screenshot.get_region(roi).get_data()
        npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
        var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
        for i in range(mini(before.size(),after.size())):
            if absi(int(before[i])-int(after[i]))>=5:differences+=1
        check(differences>25,"Actor on/off render difference "+label)
        npc.active=true;game.grid_view.queue_redraw();await process_frame
    return file
func run() -> void:
    check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
    check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
    if failures:quit(2);return
    root.size=Vector2i(1600,900)
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-pickup-runtime.meta";game.run_save_path="user://james-pickup-runtime.loop"
    game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
    root.add_child(game);current_scene=game
    while not game.startup_complete:await process_frame
    game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
    var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
    game.running=true;game.paused=false;game.Architects.advance_core(game,10)
    check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Actual core release supplies valid roster")
    game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();pass # Preserve normal architect/wreck registry for valid disk saves.
    for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
        var room: Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
        room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
        game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
    for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
    game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
    check(not game.recovered_crew.is_empty(),"Normal recovered roster retained")
    var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
    npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
    var player=game.grid_view.branforth_player
    game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
    await process_frame;game._center_grid_on_station_now();await process_frame
    DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
    var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0



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
