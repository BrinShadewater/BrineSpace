extends SceneTree

class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / PACKAGED CONSUMER REVIEW", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
        draw_string(font,Vector2(90,76),"Bare candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        draw_string(font,Vector2(585,76),"Existing helmet candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        if bare != null:
            draw_texture_rect(bare,Rect2(100,95,368,368),false)
            draw_texture_rect(bare,Rect2(238,510,92,92),false)
        if helmet != null:
            draw_texture_rect(helmet,Rect2(580,95,368,368),false)
            draw_texture_rect(helmet,Rect2(718,510,92,92),false)
        draw_string(font,Vector2(28,645),caption,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        draw_string(font,Vector2(28,680),"Below: 92px canvas / fixed (92,172) source foot / linear filtering. Standalone unselected art fixture.",HORIZONTAL_ALIGNMENT_LEFT,-1,16,Color(0.73,0.78,0.8))

func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var checks := 0
    var errors: Array = []
    var player = preload("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest("res://character/krusher-runtime-candidate-v1/bare-manifest.json")
    if not player.load_equipment_manifest("diving-helmet","res://character/krusher-runtime-candidate-v1/helmet-manifest.json"):
        errors.append("helmet admission")
    var captures: Array = []
    for gear in ["bare","helmet"]:
        var path: String = "res://character/krusher-runtime-candidate-v1/bare-manifest.json" if gear == "bare" else "res://character/krusher-runtime-candidate-v1/helmet-manifest.json"
        var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
        var equipment := "" if gear == "bare" else "diving-helmet"
        for state in manifest.states:
            var cursor := 0.0
            for index in range(state.frameFiles.size()):
                var hold: float = state.frameDurationsMs[index]/1000.0
                var texture: Texture2D = player.frame_at_elapsed(state.id,cursor+hold/2,equipment)
                checks += 1
                if texture == null:
                    errors.append("missing:"+state.id)
                    continue
                var underlying: Texture2D = texture.diffuse_texture if texture is CanvasTexture else texture
                var expected := Image.load_from_file(path.get_base_dir().path_join(state.frameFiles[index]))
                var actual := underlying.get_image()
                checks += 3
                if actual.get_size() != Vector2i(184,184) or actual.get_data() != expected.get_data():errors.append("pixels:"+gear+":"+state.id+":"+str(index))
                if texture.get_meta("crew_pivot") != Vector2(92,172) or texture.get_meta("crew_standing_height") != 148.0:errors.append("registration:"+state.id)
                if not texture is CanvasTexture or texture.texture_filter != CanvasItem.TEXTURE_FILTER_LINEAR:errors.append("filter:"+state.id)
                cursor += hold
            checks += 1
            if absf(player.cycle_seconds(state.id,equipment)-cursor)>0.000001:errors.append("clock:"+state.id)
    root.content_scale_size = Vector2i(1200,720)
    root.size = Vector2i(1200,720)
    var stage := ArtStage.new()
    root.add_child(stage)
    var capture_paths := {
        "idle-west":"res://character/krusher-runtime-candidate-v1/review/native/idle-west.png",
        "walk-south":"res://character/krusher-runtime-candidate-v1/review/native/walk-south.png",
        "terminal-type-west":"res://character/krusher-runtime-candidate-v1/review/native/terminal-type-west.png"}
    for test in [["idle-west",0.02],["walk-south",0.84],["terminal-type-west",0.42]]:
        stage.bare = player.frame_at_elapsed(test[0],test[1])
        stage.helmet = player.frame_at_elapsed(test[0],test[1],"diving-helmet")
        stage.caption = str(test[0])+" / existing CrewSpritePlayer / "+str(test[1])+" seconds"
        stage.queue_redraw()
        await RenderingServer.frame_post_draw
        var output: String = capture_paths[test[0]]
        var capture: String = output.get_file()
        if root.get_texture().get_image().save_png(output)!=OK:errors.append("capture:"+capture)
        captures.append(capture)
    checks += 1
    if not preload("res://scripts/safe_image.gd").failures.is_empty():errors.append("image placeholder")
    var report := {"checks":checks,"errors":errors,"captures":captures,"renderer":DisplayServer.get_name(),"scope":"existing crew sprite player source pixels, per-frame elapsed selection, gear admission, metadata, filters and native samples; no normal selectors or station behavior"}
    var file := FileAccess.open("res://character/krusher-runtime-candidate-v1/review/native/report.json",FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    print("KRUSHER_NATIVE consumer_checks=%d errors=%d" % [checks,errors.size()])
    quit(0 if errors.is_empty() else 1)
