extends SceneTree

class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / NORTH IDLE / TABLET / IDLE REVIEW", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
        draw_string(font,Vector2(90,76),"Bare cyan candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        draw_string(font,Vector2(585,76),"Helmet face-fit candidate",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
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
    var player = preload("res://scripts/crew_sprite_player.gd").new()
    player.load_manifest("res://character/krusher-james-canonical-v4/bare-manifest.json")
    if not player.load_equipment_manifest("diving-helmet","res://character/krusher-james-canonical-v4/helmet-manifest.json"):
        quit(1)
        return
    var bare: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-james-canonical-v4/bare-manifest.json"))
    var helmet: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-james-canonical-v4/helmet-manifest.json"))
    var admission_errors:Array=[]
    var admission_checks:=0
    for state in bare.states:
        var clock:=0.0
        for i in range(state.frameFiles.size()):
            var hold:float=state.frameDurationsMs[i]/1000.0
            for gear in ["","diving-helmet"]:
                var texture:Texture2D=player.frame_at_elapsed(state.id,clock+hold/2,gear)
                var raw:Texture2D=texture.diffuse_texture if texture is CanvasTexture else texture
                var rows:Dictionary=bare if gear=="" else helmet
                var selected:Dictionary={}
                for row in rows.states:
                    if row.id==state.id:selected=row
                var path:String="res://character/krusher-james-canonical-v4/bare-manifest.json".get_base_dir().path_join(selected.frameFiles[i])
                var expected:=Image.load_from_file(path)
                admission_checks+=2
                if raw.get_image().get_data()!=expected.get_data():admission_errors.append("texture:"+state.id+str(i)+gear)
                if texture.get_meta("crew_pivot")!=Vector2(92,172) or texture.get_meta("crew_standing_height")!=148.0:admission_errors.append("registration:"+state.id)
            clock+=hold
        admission_checks+=1
        if absf(player.cycle_seconds(state.id)-clock)>0.000001:admission_errors.append("clock:"+state.id)
    var output: String = OS.get_environment("KRUSHER_MOTION_OUTPUT")
    DirAccess.make_dir_recursive_absolute(output)
    var schedule: Array = []
    var total := 0
    for state_id in ["idle-north","interact-north","idle-north"]:
        var state:Dictionary={}
        var equipped_state:Dictionary={}
        for row in bare.states:
            if row.id==state_id:state=row
        for row in helmet.states:
            if row.id==state_id:equipped_state=row
        var state_start := total
        for i in range(state.frameFiles.size()):
            var hold: int = state.frameDurationsMs[i]
            schedule.append({"state":state.id,"index":i,"startMs":total,"endMs":total+hold,"stateStartMs":state_start,"durationMs":hold,"bareSource":state.frameFiles[i],"helmetSource":equipped_state.frameFiles[i]})
            total += hold
    root.content_scale_size = Vector2i(1200,720)
    root.size = Vector2i(1200,720)
    var stage := ArtStage.new()
    root.add_child(stage)
    var started := Time.get_ticks_usec()
    var last := ""
    var samples: Array = []
    var errors: Array = admission_errors
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
            capture = "%04d-%s-%03d.png" % [slot,entry.state,entry.index]
            if root.get_texture().get_image().save_png(output.path_join(capture)) != OK:errors.append(capture)
        samples.append({"cycle":cycle,"slot":slot,"state":entry.state,"index":entry.index,"scheduledStartMs":cycle*total+entry.startMs,"scheduledEndMs":cycle*total+entry.endMs,"observedSelectMs":elapsed,"observedDrawMs":drawn,"capture":capture})
    var report := {"admissionChecks":admission_checks,"reviewOrder":["idle-north","interact-north","idle-north"],"renderer":DisplayServer.get_name(),"schedule":schedule,"cycleDurationMs":total,"cycles":2,"samples":samples,"observedTotalMs":(Time.get_ticks_usec()-started)/1000.0,"errors":errors,"scope":"complete package frame admission plus focused continuous North idle/tablet/idle playback through existing consumer; not station integration or owner artistic acceptance"}
    var file := FileAccess.open(output.path_join("report.json"),FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t")+"\n")
    print("KRUSHER_NATIVE motion_events=%d errors=%d" % [samples.size(),errors.size()])
    quit(0 if errors.is_empty() else 1)
