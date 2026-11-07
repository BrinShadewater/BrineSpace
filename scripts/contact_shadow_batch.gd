extends RefCounted
# Restricted equal-radius borderless StyleBox geometry; based on Godot
# ed1daf0bf style_box_flat.cpp (MIT). Supported contact bands only; other geometry retains StyleBox drawing.
# Copyright (c) 2014-present Godot Engine contributors (see AUTHORS.md at godotengine/godot).
# Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
static var cache:Dictionary={}
static var colors_cache:Dictionary={}
static var hits:=0
static var misses:=0
static var fallbacks:=0
static func draw(canvas:CanvasItem,bands:Array)->bool:
	var data:=prepare(canvas,bands)
	if data.is_empty():return false
	if not data.indices.is_empty():RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),data.indices,data.points,data.colors)
	return true

# Read-only cached arrays. Callers must append into their own buffers.
static func prepare(canvas:CanvasItem, bands:Array) -> Dictionary:
	var node:CanvasItem=canvas
	while node!=null and node.oversampling_with_scale==CanvasItem.OVERSAMPLING_WITH_SCALE_PARENT_NODE:
		var parent:=node.get_parent()
		if parent!=null and not parent is CanvasItem and not parent is Viewport:
			fallbacks+=1
			return {}
		node=parent as CanvasItem
	if node!=null and node.oversampling_with_scale==CanvasItem.OVERSAMPLING_WITH_SCALE_ENABLED:
		fallbacks+=1
		return {}
	var aa:float=canvas.get_viewport().get_oversampling()
	if aa<=0.0:aa=1.0
	var key:Array=[aa]
	for band in bands:
		var rect:Rect2=band.rect
		var radius:float=band.radius
		if radius<1.0 or minf(rect.size.x,rect.size.y)<=radius*2.0+1.0/aa:
			fallbacks+=1
			return {}
		key.append_array([rect,radius])
	var data:Dictionary
	if cache.has(key):
		data=cache[key]
		hits+=1
	else:
		misses+=1
		data={"points":PackedVector2Array(),"colors":PackedColorArray(),"indices":PackedInt32Array()}
		for band in bands:
			ring(data,band.rect,band.radius,Color.WHITE,true,aa)
			ring(data,band.rect,band.radius,Color.WHITE,false,aa)
		if cache.size()>=256:cache.clear()
		data.erase("colors")
		cache[key]=data
	var palette:Array=[]
	for band in bands:palette.append(band.color)
	if not colors_cache.has(palette):
		var colors:=PackedColorArray()
		for color in palette:
			for index in 84:
				colors.append(Color(color.r,color.g,color.b,0) if index>=28 and index%2==1 else color)
		if colors_cache.size()>=64:colors_cache.clear()
		colors_cache[palette]=colors
	return {"points":data.points,"indices":data.indices,"colors":colors_cache[palette]}
static func f(value: float) -> float:
	return PackedFloat32Array([value])[0]
static func ring(data: Dictionary, rect: Rect2, radius: float, color: Color, filled: bool, aa_scale: float) -> void:
	var base: int = data.points.size()
	for corner in 4:
		for detail in 7:
			var angle := f((corner + detail / 6.0) * f(PI / 2.0) + PI)
			var cosine := f(cos(angle))
			var sine := f(sin(angle))
			for layer in (1 if filled else 2):
				var delta := f((-0.5 if layer == 0 else 0.5) / aa_scale)
				var inner := rect.grow(delta)
				var r := f(radius + delta)
				# Equal radii fit these footprints: no adjacent-corner overflow.
				var scale := 1.0
				var effective := f(r * scale)
				var center := Vector2(inner.position.x + effective if corner in [0,3] else inner.end.x - effective,
					inner.position.y + effective if corner in [0,1] else inner.end.y - effective)
				data.points.append(Vector2(f(f(f(r*cosine)*scale)+center.x), f(f(f(r*sine)*scale)+center.y)))
				data.colors.append(color if layer == 0 else Color(color.r,color.g,color.b,0))
	var count: int = data.points.size() - base
	if filled:
		for i in range(count / 2 - 1):
			for index in [i,count-i-2,i+1,i,count-i-1,count-i-2]: data.indices.append(base+index)
	else:
		for i in count:
			for index in [i,(i+2)%count,(i+1)%count]: data.indices.append(base+index)

static func colors_for_bands(bands:Array)->PackedColorArray:
	var palette:Array=[]
	for band in bands:palette.append(band.color)
	if not colors_cache.has(palette):
		var colors:=PackedColorArray()
		for color in palette:
			for index in 84:colors.append(Color(color.r,color.g,color.b,0) if index>=28 and index%2==1 else color)
		if colors_cache.size()>=64:colors_cache.clear()
		colors_cache[palette]=colors
	return colors_cache[palette]
