extends SceneTree

class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / CONTINUOUS CLOCK ART PREVIEW", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
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
    var workspace := OS.get_environment("KRUSHER_REVIEW_ROOT")
    var output := workspace.path_join("character/krusher-terminal-clock-review-v1/review/native")
    var source_root := workspace.path_join("character/krusher-terminal-gear-pair-v1")
    DirAccess.make_dir_recursive_absolute(output)
    var bare = JSON.parse_string(FileAccess.get_file_as_string(source_root.path_join("bare-manifest.json")))
    var helmet = JSON.parse_string(FileAccess.get_file_as_string(source_root.path_join("helmet-manifest.json")))
    var schedule: Array = []
    var textures := {}
    var total := 0
    for si in range(bare.states.size()):
        var state = bare.states[si]
        var gear = helmet.states[si]
        if state.id != gear.id or state.frameDurationsMs != gear.frameDurationsMs:
            push_error("Incompatible gear clocks")
            quit(1)
            return
        for index in range(state.frameFiles.size()):
            var duration: int = state.frameDurationsMs[index]
            var bp: String = state.frameFiles[index]
            var hp: String = gear.frameFiles[index]
            for path in [bp,hp]:
                if not textures.has(path):
                    textures[path] = _texture(source_root.path_join(path))
                    if textures[path] == null:
                        quit(1)
                        return
            schedule.append({"state":state.id,"index":index,"startMs":total,"endMs":total+duration,"durationMs":duration,"bareSource":bp,"helmetSource":hp})
            total += duration
    var stage := ArtStage.new()
    stage.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    root.add_child(stage)
    # Preload before the clock starts. One uninterrupted monotonic timeline owns
    # all states and cycles; rendering/capture overhead never resets a pose clock.
    var started := Time.get_ticks_usec()
    var last_key := ""
    var samples: Array = []
    var errors: Array = []
    var cycles := 3
    while (Time.get_ticks_usec()-started)/1000.0 < total*cycles:
        var elapsed := (Time.get_ticks_usec()-started)/1000.0
        var cycle := int(elapsed/total)
        var within := fmod(elapsed,total)
        var slot := schedule.size()-1
        for i in range(schedule.size()):
            if within < schedule[i].endMs:
                slot = i
                break
        var key := "%d:%d" % [cycle,slot]
        if key == last_key:
            await process_frame
            continue
        last_key = key
        var entry = schedule[slot]
        stage.bare = textures[entry.bareSource]
        stage.helmet = textures[entry.helmetSource]
        stage.caption = "Cycle %d / %s / pose %d / continuous source clock" % [cycle+1,entry.state,entry.index+1]
        stage.queue_redraw()
        await RenderingServer.frame_post_draw
        var drawn := (Time.get_ticks_usec()-started)/1000.0
        var capture := ""
        if cycle == 0:
            capture = "%s-%02d.png" % [entry.state,entry.index]
            if root.get_texture().get_image().save_png(output.path_join(capture)) != OK:
                errors.append(capture)
        samples.append({"cycle":cycle,"slot":slot,"state":entry.state,"index":entry.index,"scheduledStartMs":cycle*total+entry.startMs,"scheduledEndMs":cycle*total+entry.endMs,"observedSelectMs":elapsed,"observedDrawMs":drawn,"bareSource":entry.bareSource,"helmetSource":entry.helmetSource,"capture":capture})
    var observed_total := (Time.get_ticks_usec()-started)/1000.0
    var report := {"renderer":DisplayServer.get_name(),"sourceRoot":source_root,"schedule":schedule,"cycleDurationMs":total,"cycles":cycles,"scheduledTotalMs":total*cycles,"observedTotalMs":observed_total,"samples":samples,"errors":errors,"clockMethod":"single monotonic elapsed timeline, preload, carry overshoot across every pose/state/cycle","scope":"standalone continuous source-clock art review; no station/controller integration"}
    var file := FileAccess.open(output.path_join("report.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    file.close()
    print("KRUSHER_NATIVE clock_events=%d cycles=%d errors=%d" % [samples.size(),cycles,errors.size()])
    stage.queue_free()
    await process_frame
    quit(0 if errors.is_empty() else 1)

