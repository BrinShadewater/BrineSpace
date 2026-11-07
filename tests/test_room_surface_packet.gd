extends SceneTree
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR"):quit(2);return
	var script:Script=load("res://scripts/room_surface_packet.gd")
	if script==null:quit(1);return
	for base in range(100):
		var a=script.new();a.points.resize(base);a.colors.resize(base)
		a.circle(Vector2(21.375,29.1875),1.1,Color(.3,.4,.5,.6))
		var expected:=PackedInt32Array()
		for i in range(64):expected.append_array(PackedInt32Array([base+65,base+i,base+i+1]))
		check(a.indices.to_byte_array()==expected.to_byte_array(),"Ordered native fan indices")
		check(a.points.size()==base+66 and a.colors.size()==base+66,"Complete circle geometry and colors")
		var borrowed:PackedInt32Array=script.circle_offsets[base].duplicate()
		a.indices[0]=-100
		check(script.circle_offsets[base]==borrowed,"Caller mutation cannot alter cached offsets")
		check(script.circle_offsets.size()<=32,"Circle offset cache remains bounded")
		var b=script.new();b.points.resize(base);b.colors.resize(base)
		b.circle(Vector2(-19.375,4.1875),2.0,Color(.7,.8,.9,.4))
		check(b.indices==expected,"Independent packet owns its fan indices")
	check(not script.circle_offsets.has(0),"Old offset layout is evicted")
	var rebuilt=script.new();rebuilt.circle(Vector2.ZERO,1,Color.WHITE)
	check(script.circle_offsets.has(0) and rebuilt.indices[0]==65,"Evicted circle offsets reconstruct")
	var packet=script.new();var expected_points:=PackedVector2Array();var expected_uv:=PackedVector2Array();var expected_colors:=PackedColorArray();var expected_indices:=PackedInt32Array()
	for reverse in [false,true]:
		var triangle:=PackedVector2Array([Vector2(1.25,2.75),Vector2(11.5,7.25),Vector2(4.75,17.125)])
		if reverse:triangle.reverse()
		var uv:=PackedVector2Array([Vector2(.2,.3),Vector2(.7,.8),Vector2(.4,.5)])
		var colors:=PackedColorArray([Color(.2,.4,.6,.8)])
		var offset:int=expected_points.size()
		for index in Geometry2D.triangulate_polygon(triangle):expected_indices.append(offset+index)
		expected_points.append_array(triangle);expected_uv.append_array(uv)
		for i in range(3):expected_colors.append(colors[0])
		packet.polygon(triangle,colors,uv)
		triangle[0]=Vector2(999,999);uv[0]=Vector2(999,999);colors[0]=Color.RED
	check(packet.points.to_byte_array()==expected_points.to_byte_array(),"Packet snapshots source vertices")
	check(packet.uv.to_byte_array()==expected_uv.to_byte_array(),"Packet snapshots source UVs")
	check(packet.colors.to_byte_array()==expected_colors.to_byte_array(),"Packet preserves float colors")
	check(packet.indices.to_byte_array()==expected_indices.to_byte_array(),"Native triangle winding and order")
	print("ROOM_SURFACE_PACKET ",checks," checks ",failures," failures");quit(1 if failures else 0)
