extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-west-carry-walk-keys-v1/room-journey-v45/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
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
    game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-carry-journey.meta";game.run_save_path="user://james-carry-journey.loop"
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
