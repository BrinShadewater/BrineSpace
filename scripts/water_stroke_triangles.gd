extends RefCounted
# Ordered open-stroke triangles retain native antialiasing and blend order.
# Geometry adapted from Godot Engine canvas polyline implementation.
# Copyright (c) 2014-present Godot Engine contributors (see AUTHORS.md).
# Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
const LICENSE_NOTICE="res://assets/licenses/godot-engine-MIT.txt"
const FEATHER=1.25
static func f32(value:float)->float:return Vector2(value,0).x
static func empty(topology:Dictionary={})->Dictionary:return {"points":PackedVector2Array(),"colors":PackedColorArray(),"indices":PackedInt32Array(),"topology":topology}
static func add_strip(mesh:Dictionary,points:PackedVector2Array,colors:PackedColorArray):
	var base:int=mesh.points.size();mesh.points.append_array(points);mesh.colors.append_array(colors)
	var key:=Vector2i(base,points.size())
	var topology:Dictionary=mesh.topology
	if not topology.has(key):
		var indices:=PackedInt32Array();indices.resize((points.size()-2)*3)
		for i in range(2,points.size()):
			var offset: int=(i-2)*3
			indices[offset]=base+i-2 if i%2==0 else base+i-1
			indices[offset+1]=base+i-1 if i%2==0 else base+i-2
			indices[offset+2]=base+i
		if topology.size()>=1024:topology.erase(topology.keys()[0])
		topology[key]=indices
	mesh.indices.append_array(topology[key])
static func add(mesh:Dictionary,path:PackedVector2Array,color:Color,width:float)->bool:
	var count:=path.size()
	if count<2 or path[0].is_equal_approx(path[count-1]) or width<=0:return false
	var first:=Vector2.ZERO;var last:=Vector2.ZERO
	for i in range(1,count):
		first=(path[i]-path[i-1]).normalized()
		if not first.is_zero_approx():break
	for i in range(count-1,0,-1):
		last=(path[i]-path[i-1]).normalized()
		if not last.is_zero_approx():break
	if first.is_zero_approx() or last.is_zero_approx():return false
	width=f32(width)
	if width<=FEATHER*2+0.00001:width=f32(width*.5)
	elif width<=FEATHER*4+0.00001:width=f32(remap(width,FEATHER*2,FEATHER*4,f32(width*.5),f32(width-FEATHER*.5)))
	else:width=f32(width-FEATHER*.5)
	var fade:float=f32(FEATHER*width) if width<1 else FEATHER
	var transparent:=Color(color.r,color.g,color.b,0)
	var core:=PackedVector2Array();var left:=PackedVector2Array();var right:=PackedVector2Array()
	var cc:=PackedColorArray();var lc:=PackedColorArray();var rc:=PackedColorArray()
	core.resize(count*2+4);cc.resize(core.size());left.resize(count*2+5);lc.resize(left.size());right.resize(left.size());rc.resize(left.size())
	cc.fill(color);lc.fill(transparent);rc.fill(transparent)
	var previous:=Vector2.ZERO
	for i in range(count):
		var direction:Vector2=(path[i+1]-path[i]).normalized() if i<count-1 else previous
		if direction.is_zero_approx():direction=previous
		var normal:=first.orthogonal() if i==0 else last.orthogonal() if i==count-1 else Vector2.ZERO
		if i>0 and i<count-1:
			var bisector:Vector2=(previous*direction.length()-direction*previous.length()).normalized()
			var angle:float=f32(atan2(bisector.cross(previous),bisector.dot(previous)))
			var sine:float=f32(sin(angle));var span:=1.0
			if not is_zero_approx(sine) and not direction.is_equal_approx(previous):span=clampf(f32(1.0/sine),-3,3)
			else:bisector=direction.orthogonal()
			if bisector.is_zero_approx():bisector=direction.orthogonal()
			normal=bisector*span
		var half:Vector2=normal*f32(width*.5);var fringe:Vector2=normal*fade;var at:Vector2=path[i];var j:=i*2+2
		core[j]=at+half;core[j+1]=at-half
		left[j]=at+half;left[j+1]=at+half+fringe;lc[j]=color
		right[j]=at-half;right[j+1]=at-half-fringe;rc[j]=color
		if i==0:
			var cap:Vector2=-direction*fade
			core[0]=at+half+cap;core[1]=at-half+cap;cc[0]=transparent;cc[1]=transparent
			left[0]=at+half+cap;left[1]=at+half+cap+fringe;lc[0]=transparent;lc[1]=transparent
			right[0]=at-half+cap;right[1]=at-half+cap-fringe;rc[0]=transparent;rc[1]=transparent
		if i==count-1:
			var cap:Vector2=previous*fade;var end:=count*2+2
			core[end]=at+half+cap;core[end+1]=at-half+cap;cc[end]=transparent;cc[end+1]=transparent
			left[end]=at+half;left[end+1]=at+half+cap+fringe;left[end+2]=at+half+cap;lc[end]=color;lc[end+1]=transparent;lc[end+2]=transparent
			right[end]=at-half;right[end+1]=at-half+cap-fringe;right[end+2]=at-half+cap;rc[end]=color;rc[end+1]=transparent;rc[end+2]=transparent
		previous=direction
	add_strip(mesh,core,cc);add_strip(mesh,left,lc);add_strip(mesh,right,rc);return true
static func draw(canvas:CanvasItem,mesh:Dictionary):
	if mesh.indices.is_empty():return
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),mesh.indices,mesh.points,mesh.colors)
