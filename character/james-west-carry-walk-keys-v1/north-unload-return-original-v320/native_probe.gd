extends SceneTree
const MANIFEST="res://character/james-west-carry-walk-keys-v1/north-unload-return-original-v320/bare-review-manifest.json"
const OUT="res://character/james-west-carry-walk-keys-v1/north-unload-return-original-v320/"
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
    checks+=1
    if not ok:failures+=1;push_error(why)
class Board extends Node2D:
    var player
    var elapsed:=0.0
    var phase:=0
    func _draw()->void:
        draw_rect(Rect2(0,0,1600,320),Color("303b40"))
        for column in range(4):
            var key:String=["master","original","candidate","turnend"][column]
            draw_string(ThemeDB.fallback_font,Vector2(column*400+8,24),key+" / provisional unload phase "+str(phase),HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
            var tex:Texture2D=player.frame_at_elapsed(key,elapsed if key in ["original","candidate"] else 0.0)
            for i in range(4):
                var sc:float=[148.0,82.0,54.0,27.0][i]/148.0
                var at:=Vector2(column*400+70+i*100,265)
                draw_texture_rect(tex,Rect2(at-Vector2(128,224)*sc,tex.get_size()*sc),false)
                draw_line(at-Vector2(28,0),at+Vector2(28,0),Color("536469"))
func _init()->void:call_deferred("run")
func run()->void:
    check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
    check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
    check(DisplayServer.get_name()!="headless","Native display required")
    if failures:quit(2);return
    root.size=Vector2i(1600,320);root.content_scale_size=Vector2i.ZERO
    var player=load("res://scripts/crew_sprite_player.gd").new();player.load_manifest(MANIFEST)
    var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(MANIFEST))
    for state in manifest.states:
        check(player.frames[state.id].size()==state.frameCount,"Exact frame count")
        var clock:=0.0
        for i in range(state.frameCount):
            var tex:Texture2D=player.frame_at_elapsed(state.id,clock+0.000001)
            var source:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))
            check(tex.get_image().get_data()==source.get_data(),"Source pixels exact at phase "+str(i))
            check(tex.get_meta("crew_pivot")==Vector2(128,224),"Fixed pivot")
            check(tex.get_meta("crew_standing_height")==148.0,"Declared master ruler")
            clock+=float(state.frameDurationsMs[i])/1000.0
        check(absf(player.cycle_seconds(state.id)-clock)<.000001,"Original finite timing")
        var last:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[-1]))
        check(player.frame_at_elapsed(state.id,clock+1.0).get_image().get_data()==last.get_data(),"Finite endpoint holds")
    check(player.frame_at_elapsed("candidate",0.0).get_image().get_data()==player.frame_at_elapsed("turnend",0.0).get_image().get_data(),"Exact cut continuity")
    check(absf(player.cycle_seconds("candidate")-player.cycle_seconds("original"))<.000001,"Unchanged520ms unloading timing")
    var board:=Board.new();board.player=player;root.add_child(board)
    var clock:=0.0
    for i in range(7):
        board.phase=i;board.elapsed=clock+0.000001;board.queue_redraw()
        await process_frame;await RenderingServer.frame_post_draw
        check(root.get_texture().get_image().save_png(OUT+"native-phase%02d.png"%i)==OK,"Four-size native comparison")
        clock+=float(manifest.states[1].frameDurationsMs[i])/1000.0
    var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":7,"scope":"bare unloading source phases at148/82/54/27; exact turn-end frame0 reuse, not continuous observed motion or actual arrival integration."},"  "))
    if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):
        var uid:=FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES NORTH UNLOAD JOIN: ",checks," checks; ",failures," failures")
    quit(1 if failures else 0)
