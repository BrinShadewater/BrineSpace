extends SceneTree
const BODY := "res://character/james-west-carry-walk-keys-v1/finite-bridge-v41/bare-manifest.json"
const HELMET := "res://character/james-west-carry-walk-keys-v1/finite-bridge-v41/helmet-manifest.json"
const OUT := "res://character/james-west-carry-walk-keys-v1/finite-bridge-v41/native"
var checks := 0
var failures := 0
func check(ok: bool, why: String) -> void:
    checks += 1
    if not ok:
        failures += 1
        push_error(why)
class Board extends Node2D:
    var player
    var key := "carry-prepare-west"
    var elapsed := 0.0
    func _draw() -> void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,24),"James staged finite carrying preparation / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        for mode in range(2):
            var tex: Texture2D=player.frame_at_elapsed(key,elapsed,"" if mode==0 else "diving-helmet")
            for i in range(4):
                var scale: float=[148.0,82.0,54.0,27.0][i]/148.0
                var at:=Vector2(100+i*150+mode*600,265)
                draw_texture_rect(tex,Rect2(at-Vector2(128,224)*scale,tex.get_size()*scale),false)
                draw_line(at-Vector2(40,0),at+Vector2(40,0),Color("536469"))
func _init() -> void:
    print("JAMES FINITE PREPARATION BOOT")
    call_deferred("run")
func run() -> void:
    var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
    check(OS.get_user_data_dir().replace("\\","/").to_lower()==expected.to_lower(),"Scratch profile isolation")
    if failures or DisplayServer.get_name()=="headless":quit(2);return
    var player=load("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest(BODY)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Paired candidate equipment accepted")
    for mode in range(2):
        var gear: String="" if mode==0 else "diving-helmet"
        var manifest: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BODY if mode==0 else HELMET))
        var rows: Dictionary=player.frames if mode==0 else player.equipment_frames[gear]
        for state in manifest.states:
            check(rows[state.id].size()==4,"Four authored slots")
            check(not player.timing[state.id].loop,"Finite motion")
            check(absf(player.cycle_seconds(state.id,gear)-.25)<.000001,"250ms preparation study")
            var elapsed:=0.0
            for i in range(4):
                var source:=Image.load_from_file(ProjectSettings.globalize_path(state.frameFiles[i]))
                var tex: Texture2D=rows[state.id][i]
                check(tex.get_image().get_data()==source.get_data(),"Exact authored source slot")
                check(tex.get_meta("crew_pivot")==Vector2(128,224),"Fixed foot pivot")
                check(tex.get_meta("crew_standing_height")==148.0,"Unchanged master ruler")
                check(player.frame_at_elapsed(state.id,elapsed+.000001,gear).get_image().get_data()==source.get_data(),"Exact finite clock selection")
                elapsed+=float(state.frameDurationsMs[i])/1000.0
            check(player.frame_at_elapsed(state.id,.251,gear).get_image().get_data()==rows[state.id][-1].get_image().get_data(),"Finite endpoint clamps")
            check(player.frame_at_elapsed(state.id,4.0,gear).get_image().get_data()==rows[state.id][-1].get_image().get_data(),"No late loop/restart")
        for i in range(4):
            check(rows["carry-prepare-west"][i].get_image().get_data()==rows["carry-unprepare-west"][3-i].get_image().get_data(),"Explicit reversed-source study")
    root.size=Vector2i(1200,320)
    root.content_scale_size=Vector2i.ZERO
    var board:=Board.new();board.player=player;root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var captures:=0
    for key in ["carry-prepare-west","carry-unprepare-west"]:
        var elapsed:=0.0
        for i in range(4):
            board.key=key;board.elapsed=elapsed+.000001;board.queue_redraw()
            await process_frame
            await RenderingServer.frame_post_draw
            check(root.get_texture().get_image().save_png(OUT.path_join(key+"-%03d.png"%i))==OK,"Four-size paired native capture")
            captures+=1
            elapsed+=float(player.timing[key].durations[i])/1000.0
    var uid_path:="res://character/james-west-carry-walk-keys-v1/finite-bridge-v41/native_probe.gd.uid"
    if not FileAccess.file_exists(uid_path):
        var uid_file:=FileAccess.open(uid_path,FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    var file:=FileAccess.open("res://character/james-west-carry-walk-keys-v1/finite-bridge-v41/native-evidence.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Isolated staged CrewSpritePlayer finite four-pose preparation/reversed-source studies, exact sources/clocks/pivots/rulers, terminal clamping and eight paired four-size native captures. No normal dispatch, distance-driven cargo journey, real rooms/Continue, full collar/equipment or uninterrupted visual motion acceptance."},"  "))
    print("JAMES FINITE PREPARATION: %d checks, %d failures, %d captures"%[checks,failures,captures])
    quit(1 if failures else 0)
