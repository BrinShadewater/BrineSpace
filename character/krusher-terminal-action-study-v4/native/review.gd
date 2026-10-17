extends SceneTree

class ArtStage extends Node2D:
    var bill: Texture2D
    var krusher: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28, 38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / GODOT ART PREVIEW", HORIZONTAL_ALIGNMENT_LEFT, -1, 22, Color.WHITE)
        draw_string(font, Vector2(90, 76), "Bill source idle", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color.WHITE)
        draw_string(font, Vector2(585, 76), "Krusher terminal candidate", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color.WHITE)
        if bill != null:
            draw_texture_rect(bill, Rect2(100, 95, 368, 368), false)
            draw_texture_rect(bill, Rect2(238, 510, 92, 92), false)
        if krusher != null:
            draw_texture_rect(krusher, Rect2(580, 95, 368, 368), false)
            draw_texture_rect(krusher, Rect2(718, 510, 92, 92), false)
        draw_string(font, Vector2(28, 645), caption, HORIZONTAL_ALIGNMENT_LEFT, -1, 18, Color.WHITE)
        draw_string(font, Vector2(28, 680), "Below: 92px display canvas / 74px standing ruler. Linear texture filtering. Unselected art fixture.", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color(0.73,0.78,0.8))

func _initialize() -> void:
    call_deferred("_run")

func _texture(path: String) -> Texture2D:
    var image := Image.load_from_file(path)
    if image == null or image.is_empty() or image.get_size() != Vector2i(184,184):
        push_error("Invalid native source: " + path)
        return null
    return ImageTexture.create_from_image(image)

func _run() -> void:
    if DisplayServer.get_name() == "headless":
        push_error("Native rendering required")
        quit(2)
        return
    var workspace := OS.get_environment("KRUSHER_REVIEW_ROOT")
    var candidate := workspace.path_join("character/krusher-terminal-action-study-v4")
    var manifest = JSON.parse_string(FileAccess.get_file_as_string(candidate.path_join("action-manifest.json")))
    var stage := ArtStage.new()
    stage.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    root.add_child(stage)
    var bill_root := workspace.path_join("character/crew-runtime-matte-v1/bill")
    var bill_manifest = JSON.parse_string(FileAccess.get_file_as_string(bill_root.path_join("manifest.json")))
    var bill_source := ""
    for bill_state in bill_manifest.states:
        if bill_state.id == "idle-west":
            bill_source = bill_root.path_join(bill_state.frameFiles[0])
    stage.bill = _texture(bill_source)
    if stage.bill == null:
        quit(1)
        return
    var captures := candidate.path_join("review/native")
    DirAccess.make_dir_recursive_absolute(captures)
    var samples: Array = []
    var errors: Array = []
    for state in manifest.states:
        for index in range(state.frameFiles.size()):
            var path: String = state.frameFiles[index]
            var texture := _texture(candidate.path_join(path))
            if texture == null:
                errors.append(path)
                continue
            stage.krusher = texture
            stage.caption = "%s / pose %d of %d / %s" % [state.id,index+1,state.frameFiles.size(),path]
            stage.queue_redraw()
            var start := Time.get_ticks_usec()
            await RenderingServer.frame_post_draw
            var screenshot := root.get_texture().get_image()
            var capture_name := "%s-%02d.png" % [state.id,index]
            var save_error := screenshot.save_png(captures.path_join(capture_name))
            if save_error != OK:
                errors.append(capture_name)
            var intended: int = state.frameDurationsMs[index]
            while (Time.get_ticks_usec()-start)/1000.0 < intended:
                await process_frame
            samples.append({"state":state.id,"index":index,"source":path,"durationMs":intended,"observedHoldMs":(Time.get_ticks_usec()-start)/1000.0,"capture":capture_name,"viewport":[screenshot.get_width(),screenshot.get_height()]})
    var report := {"renderer":DisplayServer.get_name(),"billSource":bill_source,"samples":samples,"errors":errors,"scope":"standalone native art fixture; no station scene or actor integration"}
    var file := FileAccess.open(captures.path_join("report.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    file.close()
    print("KRUSHER_NATIVE samples=%d errors=%d" % [samples.size(),errors.size()])
    stage.queue_free()
    await process_frame
    quit(0 if errors.is_empty() else 1)
