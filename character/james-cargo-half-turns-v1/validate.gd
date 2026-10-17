extends SceneTree
const BODY := "res://character/james-cargo-half-turns-v1/bare-manifest.json"
const HELMET := "res://character/james-cargo-half-turns-v1/helmet-manifest.json"
const OUT := "res://character/james-cargo-half-turns-v1/native"
var checks := 0
var failures := 0
func check(ok: bool, why: String) -> void:
    checks += 1
    if not ok:
        failures += 1
        push_error(why)
class Board extends Node2D:
    var player
    var key := "carry-turn-east-west"
    var elapsed := 0.0
    func _draw() -> void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,24),"James carrying turn / bare and equipped / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        for mode in range(2):
            var tex: Texture2D = player.frame_at_elapsed(key,elapsed,"" if mode==0 else "diving-helmet")
            for size_index in range(4):
                var heights := [148.0,82.0,54.0,27.0]
                var scale: float = heights[size_index]/148.0
                var x: float = 100.0+size_index*150.0+mode*600.0
                var at := Vector2(x,265)
                draw_texture_rect(tex,Rect2(at-Vector2(128,224)*scale,tex.get_size()*scale),false)
                draw_line(at-Vector2(40,0),at+Vector2(40,0),Color("536469"))
func _init() -> void:
    call_deferred("run")
func run() -> void:
    var expected_user_dir := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
    var actual_user_dir := OS.get_user_data_dir().replace("\\","/")
    print("JAMES ISOLATION: "+actual_user_dir)
    if actual_user_dir.to_lower()!=expected_user_dir.to_lower():
        push_error("Scratch user directory mismatch")
        quit(3)
        return
    if DisplayServer.get_name()=="headless":
        quit(2)
        return
    var grid=load("res://scripts/grid_canvas.gd").new()
    grid._load_replacement_crew_animations()
    var player=grid.branforth_player
    player.load_manifest(BODY,true)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Staged height repair")
    var manifests := [BODY,HELMET]
    for mode in range(2):
        var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(manifests[mode]))
        var selected: Dictionary = player.frames if mode==0 else player.equipment_frames["diving-helmet"]
        for state in pack.states:
            var row: Array = selected[state.id]
            check(row.size()==state.frameFiles.size(),state.id+" frame count")
            var elapsed := 0.0
            for i in range(row.size()):
                var expected := Image.load_from_file(manifests[mode].get_base_dir().path_join(state.frameFiles[i]))
                check(row[i].get_image().get_data()==expected.get_data(),state.id+" loaded pixels "+str(i))
                check(row[i].get_meta("crew_pivot")==Vector2(128,224),"Foot pivot")
                check(row[i].get_meta("crew_standing_height")==148.0,"Standing density")
                var sampled: Texture2D = player.frame_at_elapsed(state.id,elapsed+0.0001,"" if mode==0 else "diving-helmet")
                check(sampled.get_image().get_data()==expected.get_data(),"Clock selects frame "+str(i))
                elapsed += float(state.frameDurationsMs[i])/1000.0
            check(absf(elapsed-(1.6))<0.00001,"Authored cargo duration")
    for equipment in ["", "diving-helmet"]:
        for pair in [["east","west"],["west","east"],["north","south"],["south","north"]]:
            player.current_key=""
            player.motion.clear()
            player.frame("carry",pair[0],0.0,Vector2.ZERO,equipment,true)
            player.frame("carry",pair[0],0.2,Vector2(0.05,0),equipment,true)
            player.frame("carry",pair[1],0.3,Vector2(0.06,0),equipment,true)
            var clip:String="carry-turn-"+pair[0]+"-"+pair[1]
            var finish:float=.3+player.cycle_seconds(clip,equipment)
            var last:Texture2D=player.frame("carry",pair[1],finish-.001,Vector2(0.10,0),equipment,true)
            var first:Texture2D=player.frame("carry",pair[1],finish+.001,Vector2(0.11,0),equipment,true)
            var rows:Dictionary=player.frames if equipment.is_empty() else player.equipment_frames[equipment]
            var expected:Texture2D=rows["carry-"+pair[1]][0]
            var turn_expected:Texture2D=rows[clip][-1]
            check(last.get_image().get_data()==turn_expected.get_image().get_data(),"Compact stance retained through last turn frame")
            check(first.get_image().get_data()==expected.get_image().get_data(),"Completed turn resets carry clock to destination0")
    var board := Board.new()
    board.player=player
    root.size=Vector2i(1200,320)
    root.content_scale_size=Vector2i.ZERO
    root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BODY))
    var captures := 0
    for state in pack.states:
        for index in [0,1,int(state.frameCount/2),int(state.frameCount)-1]:
            var elapsed := 0.0
            for i in range(index): elapsed+=float(state.frameDurationsMs[i])/1000.0
            board.key=state.id
            board.elapsed=elapsed+0.0001
            board.queue_redraw()
            await process_frame
            await RenderingServer.frame_post_draw
            var capture := root.get_texture().get_image()
            check(capture.save_png(OUT.path_join(state.id+"-%03d.png"%index))==OK,"Native capture")
            captures+=1
    if not FileAccess.file_exists("res://character/james-cargo-half-turns-v1/validate.gd.uid"):
        var uid_file := FileAccess.open("res://character/james-cargo-half-turns-v1/validate.gd.uid",FileAccess.WRITE)
        uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES INSTALLED HALF TURNS: %d checks, %d failures, %d native captures"%[checks,failures,captures])
    grid.free()
    quit(1 if failures else 0)
