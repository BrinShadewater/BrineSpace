extends RefCounted
## Static room-local decay. No simulation RNG, collision or saved condition state.
static var decay_texture: Texture2D
static func floor_wear(painter: CanvasItem, center: Vector2) -> void:
	if decay_texture == null:
		var source:=Image.new()
		if preload("res://scripts/safe_image.gd").load_png(source,"res://rooms/derelict-condition-v1/floor-decay.png") != OK: return
		decay_texture=ImageTexture.create_from_image(source)
	painter.draw_texture_rect(decay_texture,Rect2(center-Vector2.ONE*176,Vector2.ONE*352),false)
static func wall_wear(view) -> void:
	var rng:=RandomNumberGenerator.new()
	rng.seed=5192
	for edge in view.edges:
		for rect in view.Geometry.wall_rects(edge):
			# Actual wall segments keep openings and jambs intact in every rotation.
			for i in range(5):
				var p: Vector2=rect.position+Vector2(rng.randf_range(0.12,0.83)*rect.size.x,rng.randf_range(0.15,0.75)*rect.size.y)
				var size:=Vector2(minf(11,rect.size.x*0.3),minf(7,rect.size.y*0.4))
				p=p.min(rect.end-size)
				view.painter.draw_rect(Rect2(p,size),Color(0.25,0.20,0.14,0.72))
				view.painter.draw_rect(Rect2(p+Vector2(1,1),size*0.55),Color("394542"))
