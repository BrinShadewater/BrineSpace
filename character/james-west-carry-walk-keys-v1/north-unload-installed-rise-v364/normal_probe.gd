extends SceneTree
var checks:=0
var failures:=0
var out:String
func check(ok:bool,why:String)->void:
    checks+=1
    if not ok:failures+=1;push_error(why)
class Board extends Node2D:
    var player
    var elapsed:=0.0
    func _draw()->void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,22),"Installed James North unload / bare and helmet /148,82,54,27px",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color.WHITE)
        for mode in range(2):
            var texture:Texture2D=player.frame_at_elapsed("unload-north",elapsed,"" if mode==0 else "diving-helmet")
            for i in range(4):
                var density:float=[148.0,82.0,54.0,27.0][i]/148.0
                var foot:=Vector2(100+i*150+mode*600,275)
                draw_texture_rect(texture,Rect2(foot-Vector2(128,224)*density,texture.get_size()*density),false)
func _init()->void:
    var appdata:String=OS.get_environment("APPDATA").replace("\\","/")
    if not "brine-james-normal-" in appdata or OS.get_user_data_dir().replace("\\","/").to_lower()!=(appdata+"/Godot/app_userdata/BrineSpace").to_lower():
        push_error("Isolated scratch profile required");quit(3);return
    if DisplayServer.get_name()=="headless":quit(2);return
    out=get_script().resource_path.get_base_dir()
    if not FileAccess.file_exists(get_script().resource_path+".uid"):
        FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
    call_deferred("run")
func run()->void:
    var grid=load("res://scripts/grid_canvas.gd").new()
    grid._load_replacement_crew_animations()
    var player=grid.branforth_player
    check(player.get_script().resource_path=="res://scripts/james_water_player.gd","Normal selected James player")
    for gear in ["","diving-helmet"]:
        var manifest_path:String="res://character/james-cargo-north-v1/bare-manifest.json" if gear.is_empty() else "res://character/james-cargo-north-v1/helmet-manifest.json"
        var manifest=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
        var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
        var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
        for state in manifest.states:
            check(bank[state.id].size()==state.frameFiles.size(),"Normal selected cardinal cargo count")
            var elapsed:=0.0
            for i in range(state.frameFiles.size()):
                var expected:Image=Image.load_from_file(manifest_path.get_base_dir()+"/"+state.frameFiles[i])
                if state.id=="unload-north" and i==0:
                    expected=bank["carry-turn-west-north"][-1].get_image()
                var actual:Texture2D=player.frame_at_elapsed(state.id,elapsed+.0001,gear)
                check(actual!=null and actual.get_image().get_data()==expected.get_data(),"Normal timing selects approved pixels")
                check(actual.get_meta("crew_pivot")==Vector2(128,224),"Selected physical foot pivot")
                check(actual.get_meta("crew_standing_height")==148.0,"Selected source density")
                elapsed+=float(state.frameDurationsMs[i])/1000.0
            check(absf(elapsed-(.84 if state.id=="carry-north" else .52))<.00001,"Original cargo duration retained")
        check(clocks["unload-north"].durations==[80.0,100.0,100.0,90.0,40.0,40.0,70.0],"Seven-pose installed clock")
    if failures>0:
        FileAccess.open(out+"/normal-evidence.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":0,"normalLoader":true}))
        grid.free();quit(1);return
    var board:=Board.new();board.player=player;root.size=Vector2i(1200,320);root.content_scale_size=Vector2i.ZERO;root.add_child(board)
    var elapsed:=0.0
    for i in range(7):
        board.elapsed=elapsed+.0001;board.queue_redraw()
        await process_frame;await RenderingServer.frame_post_draw
        check(root.get_texture().get_image().save_png(out+"/normal-%02d.png"%i)==OK,"Normal installed pose captured")
        elapsed+=float(player.timing["unload-north"].durations[i])/1000.0
    FileAccess.open(out+"/normal-evidence.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":7,"normalLoader":true,"fixtureResequencing":false,"scope":"Actual current Grid selected loader and player; exact source/pivot/duration plus seven native paired equipment/four-size phases. Packaged workflow evidence is V363 fixture; this is not a rebuilt release."}))
    print("JAMES NORMAL NORTH RISE checks=",checks," failures=",failures," captures=7")
    grid.free();quit(1 if failures else 0)
