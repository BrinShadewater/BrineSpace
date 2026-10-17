extends SceneTree

func _initialize() -> void:
    var bill = preload("res://scripts/crew_sprite_player.gd").new()
    var krusher = preload("res://scripts/crew_sprite_player.gd").new()
    bill.load_manifest("res://character/crew-runtime-matte-v1/bill/manifest.json")
    krusher.load_manifest("res://character/krusher-runtime-candidate-v1/bare-manifest.json")
    var errors: Array = []
    var checks := 0
    var time := 0.0
    var position := Vector2.ZERO
    var visited: Dictionary = {}
    for direction in ["south", "east", "north", "west"]:
        var key: String = "walk-" + direction
        visited[key] = []
        checks += 2
        if bill.strides.get(key) != krusher.strides.get(key): errors.append("stride:" + key)
        if bill.timing[key] != krusher.timing[key]: errors.append("timing:" + key)
        # Prescribed small distances exercise gait advancement, stops and facing changes.
        # These are player API inputs, not a station-controller or footplant test.
        for step in range(900):
            time += 1.0 / 60.0
            position.x += 0.0 if step % 150 >= 120 else 0.001
            var a: Texture2D = bill.frame("walk", direction, time, position)
            var b: Texture2D = krusher.frame("walk", direction, time, position)
            var ai: int = bill.frames[key].find(a)
            var bi: int = krusher.frames[key].find(b)
            checks += 3
            if ai != bi: errors.append("pose:" + key + ":" + str(step))
            if absf(bill.phase - krusher.phase) > 0.000001: errors.append("phase:" + key + ":" + str(step))
            if not visited[key].has(bi):
                visited[key].append(bi)
                var at: Texture2D = a.diffuse_texture if a is CanvasTexture else a
                var bt: Texture2D = b.diffuse_texture if b is CanvasTexture else b
                if at.get_image().get_region(Rect2i(0,125,184,59)).get_data() != bt.get_image().get_region(Rect2i(0,125,184,59)).get_data(): errors.append("legs:" + key + ":" + str(bi))
        checks += 1
        if visited[key].size() != krusher.frames[key].size(): errors.append("coverage:" + key)
    var report := {"checks":checks,"errors":errors,"visited":visited,"scope":"Bill versus Krusher movement-driven frame API: matching phase, pose indices, strides, timing and source leg pixels; includes stopped distance and facing changes; no station/controller or footplant acceptance"}
    var file := FileAccess.open("res://character/krusher-runtime-candidate-v1/review/gait-report.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(report,"\t") + "\n")
    print("KRUSHER_GAIT checks=%d errors=%d" % [checks, errors.size()])
    quit(0 if errors.is_empty() else 1)
