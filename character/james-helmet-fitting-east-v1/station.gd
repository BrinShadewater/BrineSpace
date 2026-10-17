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
    capture_dir="res://character/james-helmet-fitting-east-v1/station"
    DirAccess.make_dir_recursive_absolute(capture_dir)
    game=MainScene.instantiate()
    game.Preferences.save_path="user://james_fitting_east_settings.cfg"
    game.meta.save_path="user://james_fitting_east_meta.json"
    game.run_save_path="user://james_fitting_east_run.json"
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
    game.recovered_crew=[{"architect_id":"branforth","alive":true,"id":"james_fitting_east_review","name":game.Architects.NAMES.branforth,"origin":game.Architects.CORE_CELL}]
    game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*1.4)
    await settle();game._center_grid_on_station_now();await settle()
    game.bill_npc.active=false
    var actor=game.branforth_npc
    actor.rebuild(game)
    var want:Vector2=(Vector2(origin)+Vector2.ONE*.5)*384+Vector2(-75,95)
    var best:=Vector2.ZERO;var distance:=INF
    for id in actor.room_nodes.get(origin,[]):
        var point:Vector2=actor.graph.get_point_position(id)
        if actor.spawn_clear(point) and actor.can_stand(point) and point.distance_squared_to(want)<distance:
            best=point;distance=point.distance_squared_to(want)
    expect(distance<INF,"Clear maintenance floor contact exists")
    var records:Array=[]
    var samples:=0
    var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
    for row in manifest.states:
        var equip:bool=row.id=="equip-helmet-east"
        actor.active=true;actor.foot=best;actor.state="idle";actor.stage="";actor.timer=0.0;actor.direction="east";actor.helmet_equipped=not equip;actor.goal="";actor.path.clear();actor.dead=false;actor.locker_request.clear()
        expect(actor.begin_helmet_action(equip),"Begin selected fitting action")
        var duration:float=actor.timer
        var elapsed:=0.0
        for i in range(row.frameFiles.size()):
            actor.timer=duration-elapsed-0.0001
            expect(actor.foot==best,"Grounded helmet action")
            expect(actor.helmet_equipped==not equip,"Equipment changes only at completion")
            var selected:Texture2D=game.grid_view._get_branforth_frame_source(game)
            var expected:=Image.load_from_file("res://character/james-helmet-fitting-east-v1".path_join(row.frameFiles[i]))
            expect(selected.get_image().get_data()==expected.get_data(),"Production renderer selects fitting frame")
            game.grid_view.queue_redraw()
            await process_frame
            await RenderingServer.frame_post_draw
            var filename:String=row.id+"-%03d"%i
            await capture(filename)
            expect(room_pixels(origin).save_png(capture_dir.path_join(filename+"-crop.png"))==OK,"Station crop saved")
            records.append({"file":filename+"-crop.png","state":actor.state,"frame":i,"elapsed":elapsed,"helmet":actor.helmet_equipped,"foot":[actor.foot.x,actor.foot.y]})
            samples+=1
            elapsed+=float(row.frameDurationsMs[i])/1000.0
        actor.advance_helmet_action(actor.timer+.001)
        expect(actor.helmet_equipped==equip and actor.state=="idle","Equipment committed at completion")
    var trace:=FileAccess.open(capture_dir.path_join("sequence.json"),FileAccess.WRITE);trace.store_string(JSON.stringify(records,"\t"));trace.close()
    if not FileAccess.file_exists("res://character/james-helmet-fitting-east-v1/station.gd.uid"):
        var f:=FileAccess.open("res://character/james-helmet-fitting-east-v1/station.gd.uid",FileAccess.WRITE);f.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES HELMET FITTING STATION: %d failures; %d captures; production renderer clock, fixed contact and equipment checked"%[failures,samples])
    actor=null
    game.queue_free()
    game=null
    await process_frame
    await process_frame
    quit(1 if failures else 0)
