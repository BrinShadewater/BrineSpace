extends SceneTree
class Paint extends Node2D:
	var details:Script
	var packet_mode:=false
	var edges:Array=[]
	func _draw():
		var saved:bool=details.batch_thresholds
		details.batch_thresholds=packet_mode
		draw_rect(Rect2(-230,-230,460,460),Color(.16,.23,.29,.7))
		details.draw_thresholds(self,Vector2(.375,-.1875),edges)
		draw_rect(Rect2(-2,-210,4,420),Color(.8,.2,.4,.35))
		details.batch_thresholds=saved
var checks:=0
var failures:=0
var pairs:=0
var savings:Dictionary={}
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	var details:Script=load("res://rooms/floor-profiles-v1/modern_details.gd")
	check(details.get("batch_thresholds")!=null,"Threshold packet capability exists")
	if failures:quit(1);return
	root.size=Vector2i(720,720);root.always_on_top=true
	var views:Array=[];var hosts:Array=[];var paints:Array=[]
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var host:=Node2D.new();host.position=Vector2(360.125,359.75);host.modulate=Color(.87,.94,1,.8);vp.add_child(host);hosts.append(host)
		var paint:=Paint.new();paint.details=details;paint.packet_mode=mode==1;paint.use_parent_material=true;host.add_child(paint);paints.append(paint)
	var tint:=ShaderMaterial.new();tint.shader=Shader.new();tint.shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,1.0); }"
	var flood:=ShaderMaterial.new();flood.shader=load("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",350.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	var center:=Vector2(.375,-.1875)
	var full:Array=[]
	for delta in [Vector2(-192,0),Vector2(192,0),Vector2(0,-192),Vector2(0,192)]:full.append({"port":true,"center":center+delta})
	var mixed:Array=full.duplicate(true)
	mixed.append(full[0].duplicate(true));mixed.append({"port":false,"center":center+Vector2(180,0)});mixed.append({"port":true,"center":center+Vector2(169.99,0)});mixed.append({"port":true,"center":center+Vector2(205.01,0)})
	var cases:Array=[[],full.slice(0,1),full.slice(0,2),full,mixed]
	for material in [null,tint,flood]:
		for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			for q in range(4):
				for factor in [.38,.85,1.2]:
					for case_index in cases.size():
						for host in hosts:host.material=material;host.texture_filter=filtering;host.rotation=q*PI/2;host.scale=Vector2.ONE*factor
						for paint in paints:paint.edges=cases[case_index];paint.queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw;pairs+=1
						var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
						var equal:bool=a.get_data()==b.get_data()
						if not equal and failures==0:a.save_png("user://threshold-reference-failure.png");b.save_png("user://threshold-candidate-failure.png")
						check(equal,"Exact threshold pixels "+str([material,filtering,q,factor,case_index]))
						check(a.get_used_rect().has_area(),"Visible native fixture")
						var counts:Array=[]
						for vp in views:counts.append(RenderingServer.viewport_get_render_info(vp.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
						var expected:int=[0,0,1,3,4][case_index]
						check(counts[0]-counts[1]==expected,"Threshold calls "+str([case_index,counts,expected]))
						savings[case_index]=counts[0]-counts[1]
	views[1].get_texture().get_image().save_png("user://threshold-packets.png")
	var weak:WeakRef=weakref(paints[1])
	for vp in views:vp.queue_free()
	views.clear();hosts.clear();paints.clear()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Packet does not retain its canvas")
	FileAccess.open("user://threshold-packets-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"pairs":pairs,"savings":savings,"failures":failures}))
	print("THRESHOLD_PACKETS ",checks," checks ",pairs," pairs ",failures," failures");quit(1 if failures else 0)
