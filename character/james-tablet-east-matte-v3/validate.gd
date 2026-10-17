extends SceneTree
const BODY := "res://character/james-tablet-east-matte-v3/bare-manifest.json"
const HELMET := "res://character/james-tablet-east-matte-v3/helmet-manifest.json"
const OUT := "res://character/james-tablet-east-matte-v3/native"
var checks := 0
var failures := 0
func check(ok: bool, why: String) -> void:
    checks += 1
    if not ok:
        failures += 1
        push_error(why)
class Board extends Node2D:
    var player
    var key := "inspect-east"
    var elapsed := 0.0
    func _draw() -> void:
        draw_rect(Rect2(0,0,1200,320),Color("303b40"))
        draw_string(ThemeDB.fallback_font,Vector2(12,24),"James tablet inspection / bare and equipped / "+key,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
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
    print("JAMES EAST SEPARATE TABLET BOOT")
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
    check(player.equipment_frames["diving-helmet"].has("inspect-north"),"Installed tablet inspection")
    var manifests := [BODY,HELMET]
    for mode in range(2):
        var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(manifests[mode]))
        var selected: Dictionary = player.frames if mode==0 else player.equipment_frames["diving-helmet"]
        for state in pack.states:
            var row: Array = selected[state.id]
            check(row.size()==state.frameFiles.size(),state.id+" frame count")
            var elapsed := 0.0
            for i in range(row.size()):
                var expected := Image.load_from_file(ProjectSettings.globalize_path(manifests[mode].get_base_dir().path_join(state.frameFiles[i]).simplify_path()))
                check(row[i].get_image().get_data()==expected.get_data(),state.id+" loaded pixels "+str(i))
                check(row[i].get_meta("crew_pivot")==Vector2(92,172),"Foot pivot")
                check(row[i].get_meta("crew_standing_height")==148.0,"Standing density")
                var sampled: Texture2D = player.frame_at_elapsed(state.id,elapsed+0.0001,"" if mode==0 else "diving-helmet")
                check(sampled.get_image().get_data()==expected.get_data(),"Clock selects frame "+str(i))
                elapsed += float(state.frameDurationsMs[i])/1000.0
            check(absf(elapsed-float(state.frameDurationsMs.reduce(func(a,b): return a+b,0))/1000.0)<0.00001,"Unchanged source clock duration")
    for equipment in ["", "diving-helmet"]:
        var rows: Dictionary = player.frames if equipment.is_empty() else player.equipment_frames[equipment]
        for direction in ["east", "south", "west", "north"]:
            var key: String = "inspect-"+str(direction)
            check(rows[key][0].get_image().get_data()==rows[key][-1].get_image().get_data(),"Closed inspection idle seam")
            player.current_key=""
            player.frame("inspect",direction,0.0,Vector2.ZERO,equipment)
            check(player.frame("inspect",direction,5.999,Vector2.ZERO,equipment).get_image().get_data()==rows[key][-1].get_image().get_data(),"Activity clock ends stowed")
            check(player.frame("inspect",direction,6.001,Vector2.ZERO,equipment).get_image().get_data()==rows[key][0].get_image().get_data(),"Loop returns to exact idle")
            check(player.frame_at_elapsed(key,5.999,equipment).get_image().get_data()==rows[key][-1].get_image().get_data(),"Six-second inspection finishes stowed")
    var life=load("res://scripts/crew_life.gd")
    var actor=InspectionActor.new()
    for stage in ["life_eat","life_drink","life_inspect"]:
        actor.stage=stage
        check(life.pose(actor)=="inspect","Sealed helmet everyday inspection selection")
    var board := Board.new()
    board.player=player
    root.size=Vector2i(1200,320)
    root.content_scale_size=Vector2i.ZERO
    root.add_child(board)
    DirAccess.make_dir_recursive_absolute(OUT)
    var pack: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BODY))
    var captures := 0
    for state in pack.states:
        if not String(state.id).begins_with("inspect-"): continue
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
    if not FileAccess.file_exists("res://character/james-tablet-east-matte-v3/validate.gd.uid"):
        var uid_file := FileAccess.open("res://character/james-tablet-east-matte-v3/validate.gd.uid",FileAccess.WRITE)
        uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
    var report := {"checks":checks,"failures":failures,"captures":captures,"scope":"All new East inspection/interaction source references and sealed-meal compatibility substitutes through normal loader. All-direction inspection seams/clocks retained. Native route/gear journeys not exercised."}
    var report_file := FileAccess.open("res://character/james-tablet-east-matte-v3/validate-evidence.json",FileAccess.WRITE)
    report_file.store_string(JSON.stringify(report,"  "))
    print("JAMES EAST SEPARATE TABLET: %d checks, %d failures, %d native captures"%[checks,failures,captures])
    grid.free()
    quit(1 if failures else 0)

class InspectionActor extends RefCounted:
    var dead := false
    var movement_medium := "dry"
    var air_recovery := 0.0
    var state := "idle"
    var stage := "life_inspect"
    var helmet_equipped := true
