extends SceneTree
const MANIFEST="res://character/james-west-carry-walk-keys-v1/north-unload-start-source-v309/bare-review-manifest.json"
const OUT="res://character/james-west-carry-walk-keys-v1/north-unload-start-source-v309/"
var checks:=0
var failures:=0
func check(ok:bool,why:String)->void:
    checks+=1
    if not ok:failures+=1;push_error(why)
class Board extends Node2D:
    var player
    func _draw()->void:
        draw_rect(Rect2(0,0,1600,320),Color("303b40"))
        for column in range(4):
            var key:String=["master","turnend","original","candidate"][column]
            draw_string(ThemeDB.fallback_font,Vector2(column*400+8,24),key+" / north unloading start",HORIZONTAL_ALIGNMENT_LEFT,-1,14,Color.WHITE)
            var tex:Texture2D=player.frame_at_elapsed(key,0.0)
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
        var tex:Texture2D=player.frame_at_elapsed(state.id,0.0)
        var source:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[0]))
        check(player.frames[state.id].size()==1,"Single exact source")
        check(tex.get_image().get_data()==source.get_data(),"Source pixels exact")
        check(tex.get_meta("crew_pivot")==Vector2(128,224),"Fixed pivot")
        check(tex.get_meta("crew_standing_height")==148.0,"Declared master ruler")
        check(absf(player.cycle_seconds(state.id)-.14)<.000001,"Original review hold")
        check(player.frame_at_elapsed(state.id,.2).get_image().get_data()==source.get_data(),"Finite endpoint holds")
    var board:=Board.new();board.player=player;root.add_child(board)
    await process_frame;await RenderingServer.frame_post_draw
    check(root.get_texture().get_image().save_png(OUT+"native-style-review.png")==OK,"Four-size native comparisons")
    var file:=FileAccess.open(OUT+"native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":1,"scope":"Four bare static sources at148/82/54/27; runtime North master, turnend, old and new unload1. Not paired helmet, continuous unload or ordinary arrival."},"  "))
    if not FileAccess.file_exists(OUT+"native_probe.gd.uid"):
        var uid:=FileAccess.open(OUT+"native_probe.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES UNLOAD SOURCE: ",checks," checks; ",failures," failures")
    quit(1 if failures else 0)
