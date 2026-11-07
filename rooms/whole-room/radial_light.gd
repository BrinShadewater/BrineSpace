extends RefCounted
## Soft illumination projected onto the deck beneath a riser-mounted light.
static var texture: GradientTexture2D
static func draw(canvas: CanvasItem, anchor: Vector2, tint: Color, spread: float, deck_clip := true) -> void:
	if texture==null:
		var gradient:=Gradient.new()
		gradient.offsets=PackedFloat32Array([0.0,.25,.55,.8,1.0])
		gradient.colors=PackedColorArray([Color(1,1,1,.16),Color(1,1,1,.12),Color(1,1,1,.055),Color(1,1,1,.012),Color(1,1,1,0)])
		texture=GradientTexture2D.new()
		texture.gradient=gradient
		texture.width=256; texture.height=256
		texture.fill=GradientTexture2D.FILL_RADIAL
		texture.fill_from=Vector2(.5,.5)
		texture.fill_to=Vector2(1,.5)
	var radius:=112.0*clampf(spread,.25,3.0)
	var center:=anchor+Vector2(0,80) if deck_clip else anchor
	var full:=Rect2(center-Vector2.ONE*radius,Vector2.ONE*radius*2)
	var clipped:=full.intersection(Rect2(-184,-184,368,368)) if deck_clip else full
	if not clipped.has_area(): return
	var source:=Rect2((clipped.position-full.position)/full.size*256,clipped.size/full.size*256)
	canvas.draw_texture_rect_region(texture,clipped,source,tint)
