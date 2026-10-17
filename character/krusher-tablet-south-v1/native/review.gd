extends SceneTree

class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / SOUTH TABLET ACTION", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
        draw_string(font,Vector2(90,76),"Canonical Krusher idle",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
        draw_string(font,Vector2(585,76),"Action candidate / same registration",HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color.WHITE)
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
    var study = preload("res://scripts/crew_sprite_player.gd").new()
    study.load_manifest("res://character/krusher-tablet-south-v1/bare-manifest.json")
    var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/krusher-tablet-south-v1/bare-manifest.json"))
    var checks := 0
    var errors: Array = []
    for state in manifest.states:
        var clock := 0.0
        for i in range(state.frameFiles.size()):
            var hold: float = state.frameDurationsMs[i] / 1000.0
            var texture: Texture2D = study.frame_at_elapsed(state.id,clock+hold/2)
            checks += 3
            if texture == null:
                errors.append("missing:"+state.id)
            else:
                var raw: Texture2D = texture.diffuse_texture if texture is CanvasTexture else texture
                var image := Image.load_from_file("res://character/krusher-tablet-south-v1/bare-manifest.json".get_base_dir().path_join(state.frameFiles[i]))
                if raw.get_image().get_data()!=image.get_data():errors.append("pixels:"+state.id+str(i))
                if texture.get_meta("crew_pivot")!=Vector2(92,172) or texture.get_meta("crew_standing_height")!=148.0:errors.append("registration:"+state.id)
            clock+=hold
        checks+=1
        if absf(study.cycle_seconds(state.id)-clock)>0.000001:errors.append("clock:"+state.id)
    root.content_scale_size=Vector2i(1200,720)
    root.size=Vector2i(1200,720)
    var stage:=ArtStage.new()
    root.add_child(stage)
    var canonical = preload("res://scripts/crew_sprite_player.gd").new()
    canonical.load_manifest("res://character/krusher-james-canonical-v1/bare-manifest.json")
    var idle: Texture2D = canonical.frame_at_elapsed("idle-south",0.0)
    var samples: Array = [["start",0.0],["lift",1.4],["read",2.75],["return",5.5]]
    var paths: Dictionary = {"start":"res://character/krusher-tablet-south-v1/review/native/start.png","lift":"res://character/krusher-tablet-south-v1/review/native/lift.png","read":"res://character/krusher-tablet-south-v1/review/native/read.png","return":"res://character/krusher-tablet-south-v1/review/native/return.png"}
    for sample in samples:
        stage.bare=idle
        stage.helmet=study.frame_at_elapsed("interact-south",sample[1])
        stage.caption=str(sample[0])+" / canonical idle beside action / source clock and pivot retained"
        stage.queue_redraw()
        await RenderingServer.frame_post_draw
        if root.get_texture().get_image().save_png(paths[sample[0]])!=OK:errors.append("capture")
    var idle_raw: Texture2D=idle.diffuse_texture if idle is CanvasTexture else idle
    for clock in [0.0,5.5,6.5]:
        var pose: Texture2D=study.frame_at_elapsed("interact-south",clock)
        var raw: Texture2D=pose.diffuse_texture if pose is CanvasTexture else pose
        checks+=1
        if raw.get_image().get_data()!=idle_raw.get_image().get_data():errors.append("finite endpoint:"+str(clock))
    var file:=FileAccess.open("res://character/krusher-tablet-south-v1/review/native/report.json",FileAccess.WRITE)
    file.store_string(JSON.stringify({"checks":checks,"errors":errors,"scope":"Existing consumer all141 frame selections, exact textures, clock/pivot, canonical start/return/finite tail and four native samples; not continuous native capture"},"\t")+"\n")
    print("KRUSHER_NATIVE checks=%d errors=%d" % [checks,errors.size()])
    quit(0 if errors.is_empty() else 1)
