extends RefCounted
# Ordered primitive packets retain native triangulation and blend order.
# Windows circle fan geometry adapted from Godot Engine canvas ellipse drawing.
# Copyright (c) 2014-present Godot Engine contributors (see AUTHORS.md).
# Copyright (c) 2007-2014 Juan Linietsky, Ariel Manzur.
const LICENSE_NOTICE="res://assets/licenses/godot-engine-MIT.txt"
static var UNIT_CIRCLE=PackedVector2Array([Vector2(1.0,0.0),Vector2(0.9951847195625305,0.0980171412229538),Vector2(0.9807852506637573,0.19509032368659973),Vector2(0.9569403529167175,0.290284663438797),Vector2(0.9238795042037964,0.3826834559440613),Vector2(0.8819212317466736,0.4713967442512512),Vector2(0.8314695954322815,0.5555702447891235),Vector2(0.7730104327201843,0.6343933343887329),Vector2(0.7071067690849304,0.7071067690849304),Vector2(0.6343932747840881,0.7730104327201843),Vector2(0.5555701851844788,0.8314696550369263),Vector2(0.47139665484428406,0.8819212913513184),Vector2(0.3826834261417389,0.9238795042037964),Vector2(0.2902846336364746,0.9569403529167175),Vector2(0.19509023427963257,0.9807853102684021),Vector2(0.0980171337723732,0.9951847195625305),Vector2(-4.371138828673793e-08,1.0),Vector2(-0.09801722317934036,0.9951847195625305),Vector2(-0.19509032368659973,0.9807852506637573),Vector2(-0.2902847230434418,0.9569402933120728),Vector2(-0.38268351554870605,0.9238795042037964),Vector2(-0.4713968336582184,0.8819212317466736),Vector2(-0.5555703639984131,0.8314695358276367),Vector2(-0.6343932747840881,0.7730104923248291),Vector2(-0.7071067690849304,0.7071067690849304),Vector2(-0.7730104923248291,0.6343932747840881),Vector2(-0.8314696550369263,0.5555701851844788),Vector2(-0.8819213509559631,0.47139662504196167),Vector2(-0.9238796234130859,0.38268327713012695),Vector2(-0.9569403529167175,0.2902847230434418),Vector2(-0.9807853102684021,0.19509030878543854),Vector2(-0.9951847195625305,0.09801709651947021),Vector2(-1.0,-8.742277657347586e-08),Vector2(-0.9951847195625305,-0.09801726788282394),Vector2(-0.9807852506637573,-0.19509048759937286),Vector2(-0.9569402933120728,-0.2902848720550537),Vector2(-0.9238795042037964,-0.3826834261417389),Vector2(-0.8819212317466736,-0.4713967740535736),Vector2(-0.8314695358276367,-0.5555703043937683),Vector2(-0.7730103731155396,-0.6343933939933777),Vector2(-0.7071066498756409,-0.70710688829422),Vector2(-0.6343933343887329,-0.7730104327201843),Vector2(-0.5555700063705444,-0.8314697742462158),Vector2(-0.47139668464660645,-0.8819212913513184),Vector2(-0.382683128118515,-0.9238796830177307),Vector2(-0.29028454422950745,-0.9569403529167175),Vector2(-0.1950903832912445,-0.9807852506637573),Vector2(-0.09801693260669708,-0.9951847195625305),Vector2(1.1924880638503055e-08,-1.0),Vector2(0.09801743179559708,-0.9951847195625305),Vector2(0.1950904130935669,-0.9807852506637573),Vector2(0.29028502106666565,-0.956940233707428),Vector2(0.3826836049556732,-0.9238794445991516),Vector2(0.47139671444892883,-0.8819212913513184),Vector2(0.5555704236030579,-0.8314694762229919),Vector2(0.6343933343887329,-0.7730104327201843),Vector2(0.7071070075035095,-0.7071065306663513),Vector2(0.7730105519294739,-0.6343931555747986),Vector2(0.8314695954322815,-0.5555703043937683),Vector2(0.8819213509559631,-0.4713965356349945),Vector2(0.9238795638084412,-0.3826834261417389),Vector2(0.9569404125213623,-0.2902843952178955),Vector2(0.9807853102684021,-0.19509023427963257),Vector2(0.9951847791671753,-0.09801676869392395),Vector2(1.0,1.7484555314695172e-07),Vector2(0,0)])
static var CIRCLE_INDICES=PackedInt32Array([65,0,1,65,1,2,65,2,3,65,3,4,65,4,5,65,5,6,65,6,7,65,7,8,65,8,9,65,9,10,65,10,11,65,11,12,65,12,13,65,13,14,65,14,15,65,15,16,65,16,17,65,17,18,65,18,19,65,19,20,65,20,21,65,21,22,65,22,23,65,23,24,65,24,25,65,25,26,65,26,27,65,27,28,65,28,29,65,29,30,65,30,31,65,31,32,65,32,33,65,33,34,65,34,35,65,35,36,65,36,37,65,37,38,65,38,39,65,39,40,65,40,41,65,41,42,65,42,43,65,43,44,65,44,45,65,45,46,65,46,47,65,47,48,65,48,49,65,49,50,65,50,51,65,51,52,65,52,53,65,53,54,65,54,55,65,55,56,65,56,57,65,57,58,65,58,59,65,59,60,65,60,61,65,61,62,65,62,63,65,63,64])
# Borrowed immutable fan offsets are copied into each packet by append_array.
static var circle_offsets:Dictionary={}
static func _circle_indices_at(base:int)->PackedInt32Array:
	if not circle_offsets.has(base):
		var shifted:=PackedInt32Array()
		for index in CIRCLE_INDICES:shifted.append(base+index)
		if circle_offsets.size()>=32:circle_offsets.erase(circle_offsets.keys()[0])
		circle_offsets[base]=shifted
	return circle_offsets[base]
var points:=PackedVector2Array()
var colors:=PackedColorArray()
var indices:=PackedInt32Array()
var uv:=PackedVector2Array()
func polygon(vertices:PackedVector2Array,tints:PackedColorArray,texture_uv:=PackedVector2Array()):
	var base:int=points.size()
	for index in Geometry2D.triangulate_polygon(vertices):indices.append(base+index)
	points.append_array(vertices);uv.append_array(texture_uv)
	if tints.size()==1:
		var repeated:=PackedColorArray();repeated.resize(vertices.size());repeated.fill(tints[0]);colors.append_array(repeated)
	else:colors.append_array(tints)
func circle(center:Vector2,radius:float,color:Color):
	var base:int=points.size()
	var transform:=Transform2D(Vector2(radius,0),Vector2(0,radius),center)
	points.append_array(transform*UNIT_CIRCLE)
	var repeated:=PackedColorArray();repeated.resize(UNIT_CIRCLE.size());repeated.fill(color);colors.append_array(repeated)
	indices.append_array(_circle_indices_at(base))
func draw(canvas:CanvasItem,texture:Texture2D=null):
	if indices.is_empty():return
	if texture==null:RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),indices,points,colors)
	else:RenderingServer.canvas_item_add_triangle_array(canvas.get_canvas_item(),indices,points,colors,uv,PackedInt32Array(),PackedFloat32Array(),texture.get_rid())
