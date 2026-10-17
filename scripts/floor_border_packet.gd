extends RefCounted
## Fixed four RoomLighting equipment-shadow outlines, in original native order.
## Native reference: Godot 4.7.2-stable scene/main/canvas_item.cpp draw_rect;
## servers/rendering/renderer_canvas_cull.cpp canvas_item_add_polyline (non-AA),
## compute_polyline_segment_dir and compute_polyline_edge_offset_clamped.
## https://github.com/godotengine/godot/tree/ed1daf0bf001b61586d9930840f2f1394092c079
## Adapted geometry copyright (c) 2014-present Godot Engine contributors;
## copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
## MIT license notice: res://assets/licenses/godot-engine-MIT.txt
## No generic rectangle/stroke API, texture, transform or material mutation.
const LICENSE_NOTICE="res://assets/licenses/godot-engine-MIT.txt"
static var packet:Dictionary={}

static func f32(value:float)->float:
	return Vector2(value,0).x

static func build()->Dictionary:
	var points:=PackedVector2Array()
	var colors:=PackedColorArray()
	var indices:=PackedInt32Array()
	points.resize(40);colors.resize(40);indices.resize(96)
	colors.fill(Color(0.015,0.025,0.03,0.055))
	for band in range(4):
		var inset:=float(band)*2.0
		var rect:=Rect2(-180+inset,-180+inset,360-inset*2,360-inset*2)
		# draw_rect's original five points, including the duplicate close point.
		var path:=PackedVector2Array([rect.position,rect.position+Vector2(rect.size.x,0),rect.position+rect.size,rect.position+Vector2(0,rect.size.y),rect.position])
		var first:Vector2=(path[1]-path[0]).normalized()
		var last:Vector2=(path[4]-path[3]).normalized()
		var previous:=Vector2.ZERO
		for i in range(5):
			# Compute the last direction BEFORE replacing previous for loop closure.
			var direction:Vector2=previous if i==4 else (path[i+1]-path[i]).normalized()
			if direction.is_zero_approx():direction=previous
			if i==0:previous=last
			elif i==4:previous=first
			var bisector:Vector2=(previous*direction.length()-direction*previous.length()).normalized()
			var angle:float=f32(bisector.angle_to(previous))
			var sine:float=f32(sin(angle))
			var span:=1.0
			if not is_zero_approx(sine) and not direction.is_equal_approx(previous):span=clampf(f32(1.0/sine),-3,3)
			else:bisector=direction.orthogonal()
			if bisector.is_zero_approx():bisector=direction.orthogonal()
			# Width is exactly 2; native half-width is exactly 1. No AA feather.
			var edge:Vector2=(bisector*span)*1.0
			points[band*10+i*2]=path[i]+edge
			points[band*10+i*2+1]=path[i]-edge
			previous=direction
		# Preserve each native 10-vertex strip's alternating triangle winding;
		# never connect the end of one outline to the beginning of the next.
		for i in range(2,10):
			var at:int=band*24+(i-2)*3
			indices[at]=band*10+(i-2 if i%2==0 else i-1)
			indices[at+1]=band*10+(i-1 if i%2==0 else i-2)
			indices[at+2]=band*10+i
	return {"points":points,"colors":colors,"indices":indices}

static func draw(canvas:CanvasItem)->void:
	if packet.is_empty():packet=build()
	RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),packet.indices,packet.points,packet.colors)
