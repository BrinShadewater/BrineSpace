extends SceneTree
class Paint extends Node2D:
	var borders:Script
	var packet_mode:=false
	func _draw():
		draw_rect(Rect2(-225,-225,450,450),Color(.3,.34,.39,.7))
		if packet_mode:borders.draw(self)
		else:
			for band in range(4):
				var inset:=float(band)*2.0
				draw_rect(Rect2(-180+inset,-180+inset,360-inset*2,360-inset*2),Color(.015,.025,.03,.055),false,2.0)
		draw_rect(Rect2(-185,-185,25,25),Color(.8,.2,.4,.35))
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	var borders:Script=load("res://scripts/floor_border_packet.gd")
	var supported:bool=OS.get_name()=="Windows"
	check(load("res://rooms/whole-room/room_lighting.gd").batch_floor_borders==supported,"Native border platform fallback")
	var expected:Dictionary=borders.build()
	check(expected.points.size()==40 and expected.colors.size()==40 and expected.indices.size()==96,"Four independent native strips; 1344 packed bytes")
	for index in expected.indices:check(index>=0 and index<40,"Bounded border index")
	root.size=Vector2i(720,720);root.always_on_top=true
	var views:Array=[];var hosts:Array=[];var paints:Array=[]
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var host:=Node2D.new();host.position=Vector2(360.125,359.75);host.modulate=Color(.87,.94,1,.8);vp.add_child(host);hosts.append(host)
		var paint:=Paint.new();paint.borders=borders;paint.packet_mode=mode==1 and supported;paint.use_parent_material=true;host.add_child(paint);paints.append(paint)
	var tint:=ShaderMaterial.new();tint.shader=Shader.new();tint.shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,1.0); }"
	var flood:=ShaderMaterial.new();flood.shader=load("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",350.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for material in [null,tint,flood]:
		for aa in [.8333333333333333,1.0,1.5,2.0]:
			for q in range(4):
				for factor in [.38,.73,1.0,1.25]:
					for vp in views:vp.oversampling_override=aa
					for host in hosts:host.material=material;host.rotation=q*PI/2;host.scale=Vector2.ONE*factor
					for paint in paints:paint.queue_redraw()
					await process_frame;await RenderingServer.frame_post_draw;pairs+=1
					var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
					var equal:bool=a.get_data()==b.get_data()
					if not equal and failures==0:a.save_png("user://border-reference-failure.png");b.save_png("user://border-candidate-failure.png")
					check(equal,"Exact border pixels "+str([material,aa,q,factor]))
					check(a.get_used_rect().has_area(),"Visible native fixture")
					var counts:Array=[]
					for vp in views:counts.append(RenderingServer.viewport_get_render_info(vp.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
					check(counts[0]-counts[1]==(3 if supported else 0),"Border submissions "+str(counts))
	check(borders.packet==expected if supported else borders.packet.is_empty(),"Shared border buffers unchanged by canvas transforms and materials")
	views[1].get_texture().get_image().save_png("user://border-packets.png")
	var weak:WeakRef=weakref(paints[1])
	for vp in views:vp.queue_free()
	views.clear();hosts.clear();paints.clear()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Packet does not retain its canvas")
	FileAccess.open("user://border-packets-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"pairs":pairs,"failures":failures}))
	print("BORDER_PACKETS ",checks," checks ",pairs," pairs ",failures," failures");quit(1 if failures else 0)
