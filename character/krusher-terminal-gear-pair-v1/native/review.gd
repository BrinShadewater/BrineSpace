extends SceneTree

class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / PAIRED GEAR ART PREVIEW", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
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

func _texture(path: String) -> Texture2D:
    var image := Image.load_from_file(path)
    if image == null or image.is_empty() or image.get_size() != Vector2i(184,184):
        push_error("Invalid paired source: " + path)
        return null
    return ImageTexture.create_from_image(image)

func _run() -> void:
    if DisplayServer.get_name() == "headless":
        quit(2)
        return
    var candidate := OS.get_environment("KRUSHER_REVIEW_ROOT").path_join("character/krusher-terminal-gear-pair-v1")
    var bare = JSON.parse_string(FileAccess.get_file_as_string(candidate.path_join("bare-manifest.json")))
    var helmet = JSON.parse_string(FileAccess.get_file_as_string(candidate.path_join("helmet-manifest.json")))
    var stage := ArtStage.new()
    stage.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    root.add_child(stage)
    var captures := candidate.path_join("review/native")
    DirAccess.make_dir_recursive_absolute(captures)
    var samples: Array = []
    var errors: Array = []
    for si in range(bare.states.size()):
        var state = bare.states[si]
        var gear_state = helmet.states[si]
        if state.id != gear_state.id or state.frameDurationsMs != gear_state.frameDurationsMs or state.frameFiles.size() != gear_state.frameFiles.size():
            errors.append("Mismatched gear state")
            continue
        for index in range(state.frameFiles.size()):
            var bare_path: String = state.frameFiles[index]
            var helmet_path: String = gear_state.frameFiles[index]
            stage.bare = _texture(candidate.path_join(bare_path))
            stage.helmet = _texture(candidate.path_join(helmet_path))
            if stage.bare == null or stage.helmet == null:
                errors.append("Texture admission")
                continue
            stage.caption = "%s / paired pose %d of %d" % [state.id,index+1,state.frameFiles.size()]
            stage.queue_redraw()
            var start := Time.get_ticks_usec()
            await RenderingServer.frame_post_draw
            var screenshot := root.get_texture().get_image()
            var capture_name := "%s-%02d.png" % [state.id,index]
            if screenshot.save_png(captures.path_join(capture_name)) != OK:
                errors.append(capture_name)
            var intended: int = state.frameDurationsMs[index]
            while (Time.get_ticks_usec()-start)/1000.0 < intended:
                await process_frame
            samples.append({"state":state.id,"index":index,"bareSource":bare_path,"helmetSource":helmet_path,"durationMs":intended,"observedHoldMs":(Time.get_ticks_usec()-start)/1000.0,"capture":capture_name})
    var report := {"renderer":DisplayServer.get_name(),"samples":samples,"errors":errors,"scope":"paired standalone native art fixture; no station scene/controller integration"}
    var file := FileAccess.open(captures.path_join("report.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    file.close()
    print("KRUSHER_NATIVE paired_samples=%d errors=%d" % [samples.size(),errors.size()])
    stage.queue_free()
    await process_frame
    quit(0 if errors.is_empty() else 1)
