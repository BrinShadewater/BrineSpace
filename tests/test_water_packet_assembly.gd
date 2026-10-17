extends SceneTree
# The established independent-strip path is the exact-buffer oracle.
const Strokes=preload("res://scripts/water_stroke_triangles.gd")
var checks:=0
var failures:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	var target:Script=Strokes
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--packet-source="):target=load(arg.trim_prefix("--packet-source="))
	check(target!=null and target.has_method("add_packet"),"Direct packet assembler is available")
	if failures:quit(1);return
	var rng:=RandomNumberGenerator.new();rng.seed=571831
	for sample in range(3000):
		var reference:Dictionary=Strokes.empty()
		var packet:Dictionary=target.empty({},true)
		var layout:=PackedInt32Array()
		for line in range(1+sample%5):
			var path:=PackedVector2Array()
			var count:int=sample%35
			var magnitude:float=[0.00001,0.1,1.0,1000.0,1000000.0][sample%5]
			for i in range(count):
				var point:=Vector2(float(i)*magnitude,sin(float(i)*rng.randf_range(-3,3))*magnitude)
				if i>0 and (sample+i)%17==0:point=path[-1]
				path.append(point)
			if count>1 and sample%19==0:path[count-1]=path[0]
			var color:=Color(rng.randf(),rng.randf(),rng.randf(),rng.randf())
			var width:float=[0.0,-1.0,0.01,1.0,1.1,1.3,2.5,3.2,5.0,9.0][sample%10]
			var accepted:bool=Strokes.add(reference,path,color,width)
			check(target.add_packet(packet,path,color,width)==accepted,"Packet acceptance matches independent strips")
			if accepted:layout.append_array(PackedInt32Array([count*2+4,count*2+5,count*2+5]))
		check(reference.points.to_byte_array()==packet.points.to_byte_array(),"All ordered vertex bits match")
		check(reference.colors.to_byte_array()==packet.colors.to_byte_array(),"All ordered color bits match")
		check(packet.strip_counts==layout,"Core, left and right strip order matches")
		var before:PackedVector2Array=reference.points.duplicate()
		if not packet.points.is_empty():packet.points[0]=Vector2(991,223)
		check(reference.points==before,"Packet owns its writable geometry")
	# Nearby double inputs and expanded float32 inputs must keep the same
	# native geometry as the independent strips, including width thresholds.
	var widths:Array=[1.0-1e-12,1.0,1.0+1e-12,1.1-1e-12,1.1,1.1+1e-12,Vector2(1.1,0).x,1.3-1e-12,1.3,1.3+1e-12,Vector2(1.3,0).x,2.500009,2.500011,5.000009,5.000011]
	var paths:Array=[PackedVector2Array([Vector2.ZERO,Vector2.ZERO,Vector2(12.375,3.125),Vector2(24.75,-2.5)]),PackedVector2Array([Vector2(-12.5,7.25),Vector2(2,3),Vector2(2,3),Vector2(2,3)]),PackedVector2Array([Vector2.ZERO,Vector2(1e-20,1e-20),Vector2(1e-20,1e-20),Vector2(10,-7)])]
	for width in widths:
		var reference:Dictionary=Strokes.empty()
		var packet:Dictionary=target.empty({},true)
		for path in paths:
			var color:=Color(.55,.76,.73,.095)
			check(target.add_packet(packet,path,color,width)==Strokes.add(reference,path,color,width),"Nearby width acceptance")
		check(reference.points.to_byte_array()==packet.points.to_byte_array(),"Nearby width vertex bits")
		check(reference.colors.to_byte_array()==packet.colors.to_byte_array(),"Nearby width color bits")
	print("WATER_PACKET_ASSEMBLY ",checks," checks ",failures," failures")
	quit(1 if failures else 0)
