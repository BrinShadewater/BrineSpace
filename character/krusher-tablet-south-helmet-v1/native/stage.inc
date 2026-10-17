class ArtStage extends Node2D:
    var bare: Texture2D
    var helmet: Texture2D
    var caption := ""
    func _draw() -> void:
        var font := ThemeDB.fallback_font
        draw_string(font, Vector2(28,38), "KRUSHER DOM / SYSTEM ADMINISTRATOR / SOUTH TABLET HELMET FIT REVIEW", HORIZONTAL_ALIGNMENT_LEFT,-1,22,Color.WHITE)
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
