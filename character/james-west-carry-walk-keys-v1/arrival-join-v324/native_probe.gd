extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-west-carry-walk-keys-v1/arrival-join-v324/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
var traces: Array=[]
func check(ok: bool,message: String) -> void:
    checks+=1
    if not ok:failures+=1;push_error(message)
func _init() -> void:
    print("JAMES CARRY ROOM JOURNEY BOOT")
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
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-arrival324.meta";game.run_save_path="user://james-arrival324.loop"
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
        check(bank["unload-north"][0].get_image().get_data()==bank["carry-turn-west-north"][-1].get_image().get_data(),"Exact registered turn endpoint reused as north unloading entrance")
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
                var save=preload("res://scripts/run_save.gd");var path:String="user://arrival324-"+mode+"-"+checkpoint+".loop"
                var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
                check(problem.is_empty(),"Full arriving checkpoint shape: "+problem)
                if not problem.is_empty():quit(2);return
                check(save.write(game,path)==OK,"Arrival actual disk write");data=save.read(path)
                root.remove_child(game);game.queue_free();await process_frame
                game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-arrival324.meta";game.run_save_path=path
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
