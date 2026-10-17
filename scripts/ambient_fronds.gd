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
	var geometry:=strip_geometry(rect,clock,seed) if reuse_strip_geometry else reference_strip_geometry(rect,clock,seed)
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),geometry.indices,geometry.points,PackedColorArray([tint]),geometry.uv,PackedInt32Array(),PackedFloat32Array(),art.get_rid())

# Cache only fixed topology (336 packed bytes). Return owned copies with each
# plant's fresh animated positions; callers cannot mutate later plants.
static var reuse_strip_geometry:=true
static var strip_uv:=PackedVector2Array()
static var strip_indices:=PackedInt32Array()
static func strip_geometry(rect:Rect2,clock:float,seed:float)->Dictionary:
	if strip_uv.is_empty():
		for row in range(6):
			var a:=float(row)/6.0;var b:=float(row+1)/6.0;var base:=row*4
			strip_uv.append_array(PackedVector2Array([Vector2(0,a),Vector2(1,a),Vector2(1,b),Vector2(0,b)]))
			strip_indices.append_array(PackedInt32Array([base+3,base,base+1,base+1,base+2,base+3]))
	var amplitude:float=0.0 if Settings.reduced_motion or Settings.effects_quality==0 else (.024*sin(clock*.72+seed)+.008*sin(clock*1.13+seed*1.7))
	var points:=PackedVector2Array();points.resize(24)
	var top:=rect.position+Vector2(pow(1.0-0.0,2)*amplitude*rect.size.x,0.0*rect.size.y)
	var right:=top+Vector2(rect.size.x,0)
	for row in range(6):
		var b:=float(row+1)/6.0
		var bottom:=rect.position+Vector2(pow(1.0-b,2)*amplitude*rect.size.x,b*rect.size.y)
		var bottom_right:=bottom+Vector2(rect.size.x,0)
		var base:=row*4
		points[base]=top;points[base+1]=right;points[base+2]=bottom_right;points[base+3]=bottom
		top=bottom;right=bottom_right
	return {"points":points,"uv":strip_uv.duplicate(),"indices":strip_indices.duplicate()}

# Original command buffers remain available for exact native comparisons.
static func reference_strip_geometry(rect:Rect2,clock:float,seed:float)->Dictionary:
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
	return {"points":points,"uv":uv,"indices":indices}
