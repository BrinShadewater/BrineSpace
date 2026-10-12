extends RefCounted
## Bend existing painted pixels gently; the root, size, palette and placement stay fixed.
const Settings=preload("res://scripts/title_settings.gd")
static func offset(y: float, clock: float, seed: float) -> float:
	if Settings.reduced_motion or Settings.effects_quality==0: return 0.0
	return pow(1.0-y,2)*(.024*sin(clock*.72+seed)+.008*sin(clock*1.13+seed*1.7))
static func draw(canvas: CanvasItem, art: Texture2D, rect: Rect2, clock: float, seed: float, tint: Color) -> void:
	if Settings.reduced_motion or Settings.effects_quality==0:
		canvas.draw_texture_rect(art,rect,false,tint)
		return
	# Adjacent strips share vertices and UV edges. No resampling or new raster grade.
	# Submit the original ordered strip triangles together; retain float tint precision.
	var points:=PackedVector2Array();var uv:=PackedVector2Array();var indices:=PackedInt32Array()
	for row in range(6):
		var a:=float(row)/6.0
		var b:=float(row+1)/6.0
		var top:=rect.position+Vector2(offset(a,clock,seed)*rect.size.x,a*rect.size.y)
		var bottom:=rect.position+Vector2(offset(b,clock,seed)*rect.size.x,b*rect.size.y)
		var base:int=points.size()
		points.append_array(PackedVector2Array([top,top+Vector2(rect.size.x,0),bottom+Vector2(rect.size.x,0),bottom]))
		uv.append_array(PackedVector2Array([Vector2(0,a),Vector2(1,a),Vector2(1,b),Vector2(0,b)]))
		indices.append_array(PackedInt32Array([base+3,base,base+1,base+1,base+2,base+3]))
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),indices,points,PackedColorArray([tint]),uv,PackedInt32Array(),PackedFloat32Array(),art.get_rid())
