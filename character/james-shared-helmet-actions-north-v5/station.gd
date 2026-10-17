extends "res://tests/playtest_nursery_art.gd"
func run() -> void:
    var expected_user_dir := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
    var actual_user_dir := OS.get_user_data_dir().replace("\\","/")
    print("JAMES ISOLATION: "+actual_user_dir)
    if actual_user_dir.to_lower()!=expected_user_dir.to_lower():
        push_error("Scratch user directory mismatch")
        quit(3)
        return
    if DisplayServer.get_name()=="headless":quit(2);return
    capture_dir="res://character/james-shared-helmet-actions-north-v5/station"
    DirAccess.make_dir_recursive_absolute(capture_dir)
    game=MainScene.instantiate()
    game.Preferences.save_path="user://james_north_settings.cfg"
    game.meta.save_path="user://james_north_meta.json"
    game.run_save_path="user://james_north_run.json"
    root.add_child(game);current_scene=game
    while not game.startup_complete:await process_frame
    game.set_process(false);game.set_process_input(false);game.set_process_unhandled_input(false);game.set_process_unhandled_key_input(false);root.gui_disable_input=true
    root.size=Vector2i(1600,900)
    game._confirm_doctrines();game._set_paused(true)
    game.placed_rooms.clear();game.occupied.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
    var origin:=Vector2i(20,20)
    game._place_room("maintenance_bay",origin,true)
    for offset in [Vector2i.LEFT,Vector2i.RIGHT]:game._place_room("storage_bay",origin+offset,true)
    for cell in game.occupied:game.powered_room_cells[cell]=true
    game.test_walker_cell=origin;game.selected_card_id="";game.hover_cell=Vector2i(-1,-1)
    game.architect_run={"selected":"bill"}
    game.recovered_crew=[{"architect_id":"branforth","alive":true,"id":"james_north_review","name":game.Architects.NAMES.branforth,"origin":game.Architects.CORE_CELL}]
    game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*1.4)
    await settle();game._center_grid_on_station_now();await settle()
    game.bill_npc.active=false
    var actor=game.branforth_npc
    actor.rebuild(game)
    var want:Vector2=(Vector2(origin)+Vector2.ONE*.5)*384+Vector2(0,-90)
    var best:=Vector2.ZERO;var distance:=INF
    for id in actor.room_nodes.get(origin,[]):
        var point:Vector2=actor.graph.get_point_position(id)
        if actor.spawn_clear(point) and actor.can_stand(point) and point.distance_squared_to(want)<distance:
            best=point;distance=point.distance_squared_to(want)
    expect(distance<INF,"Clear maintenance floor contact exists")
    var records:Array=[]
    var samples:=0
    for equipped in [false,true]:
        actor.active=true;actor.foot=best;actor.state="kneel";actor.stage="kneel";actor.timer=1.0;actor.direction="north";actor.helmet_equipped=equipped;actor.goal="maintenance";actor.goal_cell=origin;actor.path.clear();actor.dead=false
        actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":95.0}
        game.grid_view.branforth_player.current_key=""
        game.grid_view.branforth_player.current_equipment=""
        var stages:Dictionary={}
        for tick in range(123):
            if tick>0:
                game.visual_time_seconds+=.05
                actor.update(game,.05)
            if actor.state in ["kneel","repair","stand"]:
                expect(actor.foot==best,"Work retains grounded position")
                expect(actor.direction=="north","South direction retained")
                expect(actor.helmet_equipped==equipped,"Equipment retained")
            stages[actor.state]=true
            game.grid_view.queue_redraw()
            await process_frame
            await RenderingServer.frame_post_draw
            if tick in [0,2,6,10,16,19,22,30,40,70,98,104,110,118,122]:
                var filename:String=("helmet" if equipped else "bare")+"-%03d"%tick
                await capture(filename)
                expect(room_pixels(origin).save_png(capture_dir.path_join(filename+"-crop.png"))==OK,"Station crop saved")
                records.append({"file":filename+"-crop.png","state":actor.state,"stage":actor.stage,"time":game.visual_time_seconds,"tick":tick,"helmet":equipped,"foot":[actor.foot.x,actor.foot.y],"paused":game.paused})
                samples+=1
        for state in ["kneel","repair","stand","idle"]:expect(stages.has(state),"Production controller completes "+state)
    var trace:=FileAccess.open(capture_dir.path_join("sequence.json"),FileAccess.WRITE);trace.store_string(JSON.stringify(records,"\t"));trace.close()
    if not FileAccess.file_exists("res://character/james-shared-helmet-actions-north-v5/station.gd.uid"):
        var f:=FileAccess.open("res://character/james-shared-helmet-actions-north-v5/station.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES NORTH STATION: %d failures; %d captures; production stage transitions, fixed contact and equipment checked"%[failures,samples])
    game.free();quit(1 if failures else 0)
