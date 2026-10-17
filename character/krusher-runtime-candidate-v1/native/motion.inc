func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    var player = preload("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest("res://character/krusher-runtime-candidate-v1/bare-manifest.json")
    if not player.load_equipment_manifest("diving-helmet","res://character/krusher-runtime-candidate-v1/helmet-manifest.json"):
        quit(1)
        return
    var bare: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-runtime-candidate-v1/bare-manifest.json"))
    var helmet: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-runtime-candidate-v1/helmet-manifest.json"))
    var output: String = OS.get_environment("KRUSHER_MOTION_OUTPUT")
    DirAccess.make_dir_recursive_absolute(output)
    var schedule: Array = []
    var total := 0
    for si in range(bare.states.size()):
        var state = bare.states[si]
        var state_start := total
        for i in range(state.frameFiles.size()):
            var hold: int = state.frameDurationsMs[i]
            schedule.append({"state":state.id,"index":i,"startMs":total,"endMs":total+hold,"stateStartMs":state_start,"durationMs":hold,"bareSource":state.frameFiles[i],"helmetSource":helmet.states[si].frameFiles[i]})
            total += hold
    root.content_scale_size = Vector2i(1200,720)
    root.size = Vector2i(1200,720)
    var stage := ArtStage.new()
    root.add_child(stage)
    var started := Time.get_ticks_usec()
    var last := ""
    var samples: Array = []
    var errors: Array = []
    while (Time.get_ticks_usec()-started)/1000.0 < total*2:
        var elapsed := (Time.get_ticks_usec()-started)/1000.0
        var cycle := int(elapsed/total)
        var within := fmod(elapsed,total)
        var slot := schedule.size()-1
        for i in range(schedule.size()):
            if within < schedule[i].endMs:
                slot = i
                break
        var key := "%d:%d" % [cycle,slot]
        if key == last:
            await process_frame
            continue
        last = key
        var entry = schedule[slot]
        var local_elapsed: float = (within-entry.stateStartMs)/1000.0
        stage.bare = player.frame_at_elapsed(entry.state,local_elapsed)
        stage.helmet = player.frame_at_elapsed(entry.state,local_elapsed,"diving-helmet")
        if stage.bare != player.frames[entry.state][entry.index] or stage.helmet != player.equipment_frames["diving-helmet"][entry.state][entry.index]:
            errors.append("consumer selection:"+key)
        stage.caption = "Cycle %d / %s / pose %d / actual CrewSpritePlayer elapsed selection" % [cycle+1,entry.state,entry.index+1]
        stage.queue_redraw()
        await RenderingServer.frame_post_draw
        var drawn := (Time.get_ticks_usec()-started)/1000.0
        var capture := ""
        if cycle == 0:
            capture = "%s-%02d.png" % [entry.state,entry.index]
            if root.get_texture().get_image().save_png(output.path_join(capture)) != OK:errors.append(capture)
        samples.append({"cycle":cycle,"slot":slot,"state":entry.state,"index":entry.index,"scheduledStartMs":cycle*total+entry.startMs,"scheduledEndMs":cycle*total+entry.endMs,"observedSelectMs":elapsed,"observedDrawMs":drawn,"capture":capture})
    var report := {"renderer":DisplayServer.get_name(),"schedule":schedule,"cycleDurationMs":total,"cycles":2,"samples":samples,"observedTotalMs":(Time.get_ticks_usec()-started)/1000.0,"errors":errors,"scope":"complete package continuous playback through existing consumer; not station integration or owner artistic acceptance"}
    var file := FileAccess.open(output.path_join("report.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    print("KRUSHER_NATIVE motion_events=%d errors=%d" % [samples.size(),errors.size()])
    quit(0 if errors.is_empty() else 1)
