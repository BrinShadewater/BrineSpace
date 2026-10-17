extends SceneTree
const Strokes=preload("res://scripts/water_stroke_triangles.gd")
class Paint extends Node2D:
	var candidate:=false
	var paths:Array=[]
	var width:=1.1
	var factor:=1.0
	var mesh:Dictionary={}
	var topology:Dictionary={}
	func _draw():
		draw_set_transform(Vector2(80.375,90.125),.173,Vector2(factor,factor*.91))
		if candidate:Strokes.draw(self,mesh)
		else:
			for path in paths:draw_polyline(path,Color(.55,.76,.73,.095),width,true)
var views:Array=[]
var paints:Array=[]
var pairs:=0
var failures:=0
var visible_pairs:=0
var cache_checks:=0
func check_cache(ok:bool,label:String):
	cache_checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(256,256)
	for mode in range(2):
		var viewport:=SubViewport.new();viewport.size=Vector2i(256,256);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);views.append(viewport)
		var paint:=Paint.new();paint.candidate=mode==1;paint.modulate=Color(.8,.9,1,.7);viewport.add_child(paint);paints.append(paint)
	var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",95.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	var examples:Array=[PackedVector2Array([Vector2(0,0),Vector2(35,0)]),PackedVector2Array([Vector2(0,0),Vector2(0,0),Vector2(35,20)]),PackedVector2Array([Vector2(0,0),Vector2(20,20),Vector2(21,0)]),PackedVector2Array([Vector2(0,0),Vector2(35,0),Vector2(0,1)])]
	var ribbon:=PackedVector2Array()
	for i in range(7):ribbon.append(Vector2(float(i)*5.375,3*sin(float(i)*PI/6+.375)))
	examples.append(ribbon)
	for path in examples:
		for width in [1.0,1.1,1.3]:
			for factor in [.173,.613,1.0]:
				for mirrored in [false,true]:
					for wet in [false,true]:
						var transformed:=PackedVector2Array()
						for point in path:transformed.append(point*Vector2(-1 if mirrored else 1,1))
						var paths:Array=[transformed,Transform2D(0,Vector2(7.25,1.5))*transformed]
						for paint in paints:
							paint.paths=paths;paint.width=width;paint.factor=factor;paint.material=flood if wet else null;paint.mesh=Strokes.empty(paint.topology)
							for line in paths:
								if not Strokes.add(paint.mesh,line,Color(.55,.76,.73,.095),width):push_error("Unsupported fixture stroke");quit(2);return
							paint.queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw;pairs+=1
						var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
						if a.get_used_rect().has_area():visible_pairs+=1
						if a.get_data()!=b.get_data():
							failures+=1
							if failures==1:a.save_png("user://reference.png");b.save_png("user://candidate.png");print("FIRST ",examples.find(path)," ",width," ",factor," ",mirrored," ",wet)
	packet_cache_checks(paints[1])
	var topology:Dictionary={}
	var strip:=PackedVector2Array([Vector2(1,2),Vector2(2,3),Vector2(3,4),Vector2(4,5)])
	var colors:=PackedColorArray([Color.RED,Color.GREEN,Color.BLUE,Color.WHITE])
	for base in range(1030):
		var mesh:Dictionary=Strokes.empty(topology);mesh.points.resize(base)
		Strokes.add_strip(mesh,strip,colors)
		check_cache(mesh.indices==PackedInt32Array([base,base+1,base+2,base+2,base+1,base+3]),"Native strip triangle order")
		check_cache(topology.size()<=1024,"Topology capacity bounded")
	check_cache(topology.size()==1024 and not topology.has(Vector2i(0,4)),"Old topology evicted")
	var rebuilt:Dictionary=Strokes.empty(topology);Strokes.add_strip(rebuilt,strip,colors)
	check_cache(rebuilt.indices==PackedInt32Array([0,1,2,2,1,3]),"Evicted topology rebuilt")
	rebuilt.indices[0]=99
	check_cache(topology[Vector2i(0,4)][0]==0,"Caller mutation does not corrupt cached indices")
	for i in range(4096):
		var value:float=sin(float(i)*1.173)*1000000.0/float(i+1)
		check_cache(PackedFloat64Array([PackedFloat32Array([value])[0]]).to_byte_array()==PackedFloat64Array([Strokes.f32(value)]).to_byte_array(),"Scalar conversion preserves float32 bits")
	if visible_pairs==0:push_error("Stroke matrix produced no visible output");quit(2);return
	FileAccess.open("user://results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"visible_pairs":visible_pairs,"cache_checks":cache_checks,"failures":failures}))
	for view in views:view.queue_free()
	views.clear();paints.clear();await process_frame;await process_frame
	print("STROKE_PROBE ",pairs," pairs; ",failures," failures");quit(1 if failures else 0)

func packet_cache_checks(canvas:CanvasItem):
	var packet_topology:Dictionary={}
	for n in range(200):
		var direct:Dictionary=Strokes.empty()
		var packet:Dictionary=Strokes.empty(packet_topology,true)
		for line in range(1+n%5):
			var path:=PackedVector2Array()
			for i in range(2+n%31):path.append(Vector2(float(i)*3.75,sin(float(i)*.75+float(line))*2.0))
			check_cache(Strokes.add(direct,path,Color(.55,.76,.73,.095),1.1)==Strokes.add(packet,path,Color(.55,.76,.73,.095),1.1),"Packet stroke acceptance")
		Strokes.draw(canvas,packet)
		for field in ["points","colors","indices"]:check_cache(direct[field].to_byte_array()==packet[field].to_byte_array(),"Packet preserves ordered geometry "+field)
		var layout:PackedInt32Array=packet.strip_counts.duplicate()
		packet.indices[0]=-1
		check_cache(packet_topology[["packet",layout]].to_byte_array()==direct.indices.to_byte_array(),"Packet caller cannot mutate cached indices")
		packet.strip_counts.append(12345)
		check_cache(packet_topology.has(["packet",layout]),"Packet cache snapshots mutable layout keys")
		check_cache(packet_topology.size()<=64,"Packet cache remains bounded")
	check_cache(packet_topology.size()==64,"Packet cache eviction exercised")
	RenderingServer.canvas_item_clear(canvas.get_canvas_item())
