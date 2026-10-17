extends SceneTree
const BODY := "res://character/james-torch-west-matched-v1/manifest.json"
const HELMET := "res://character/james-shared-helmet-torch-west-v1/manifest.json"
const OUT := "res://character/james-shared-helmet-torch-west-v1/native"
var checks := 0
var failures := 0
func check(ok: bool, why: String) -> void:
    checks += 1
    if not ok:
        failures += 1
        push_error(why)
class Board extends Node2D:
    var player
    var key := "torch-draw-west"
    var elapsed := 0.0
    func _draw() -> void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,24),"James west standing blowtorch / bare and equipped / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        for mode in range(2):
            var tex: Texture2D = player.frame_at_elapsed(key,elapsed,"" if mode==0 else "diving-helmet")
            for size_index in range(4):
                var heights := [148.0,82.0,54.0,27.0]
                var scale: float = heights[size_index]/148.0
                var x: float = 100.0+size_index*150.0+mode*600.0
                var at := Vector2(x,265)
                draw_texture_rect(tex,Rect2(at-Vector2(92,172)*scale,tex.get_size()*scale),false)
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
    var player = load("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest(BODY)
    check(player.load_equipment_manifest("diving-helmet",HELMET),"Staged west torch profile")
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
                check(row[i].get_meta("crew_pivot")==Vector2(92,172),"Foot pivot")
                check(row[i].get_meta("crew_standing_height")==148.0,"Standing density")
                var sampled: Texture2D = player.frame_at_elapsed(state.id,elapsed+0.0001,"" if mode==0 else "diving-helmet")
                check(sampled.get_image().get_data()==expected.get_data(),"Clock selects frame "+str(i))
                elapsed += float(state.frameDurationsMs[i])/1000.0
            check(absf(elapsed-(1.2 if state.id=="weld-west" else .52))<0.00001,"Authored torch duration")
        var idle_path: String = "res://character/crew-runtime-matte-v1/branforth/manifest.json" if mode==0 else "res://character/james-shared-helmet-runtime-v1/manifest.json"
        var idle_pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(idle_path))
        for state in idle_pack.states:
            if state.id=="idle-west":
                var im := Image.load_from_file(idle_path.get_base_dir().path_join(state.frameFiles[0]))
                check(selected["torch-draw-west"][0].get_image().get_data()==im.get_data(),"Exact idle entry")
                check(selected["torch-stow-west"].back().get_image().get_data()==im.get_data(),"Exact idle exit")
        check(selected["torch-draw-west"].back().get_image().get_data()==selected["weld-west"][0].get_image().get_data(),"Exact draw/work join")
        check(selected["weld-west"].back().get_image().get_data()==selected["weld-west"][0].get_image().get_data(),"Exact work loop")
        check(selected["weld-west"].back().get_image().get_data()==selected["torch-stow-west"][0].get_image().get_data(),"Exact work/stow join")
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
    if not FileAccess.file_exists("res://character/james-shared-helmet-torch-west-v1/validate.gd.uid"):
        var uid_file := FileAccess.open("res://character/james-shared-helmet-torch-west-v1/validate.gd.uid",FileAccess.WRITE)
        uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    print("JAMES WEST TORCH CANDIDATE: %d checks, %d failures, %d native captures"%[checks,failures,captures])
    quit(1 if failures else 0)
