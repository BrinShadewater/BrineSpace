extends SceneTree
class Paint extends Node2D:
	var moon:Script
	var packet_mode:=false
	var room:Dictionary={}
	var bounds:=Rect2()
	func _draw():
		var saved:bool=moon.batch_surface_primitives
		moon.batch_surface_primitives=packet_mode
		moon.draw(self,room,bounds)
		moon.batch_surface_primitives=saved
var checks:=0
var failures:=0
var pairs:=0
var reduced_pairs:=0
var minimum_saving:=1000000
var maximum_saving:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	var moon:Script=load("res://rooms/large-rooms/moonbay.gd")
	check(moon.has_method("new_surface_packet"),"Moonbay ordered surface packets are available")
	if failures:quit(1);return
	var supported:bool=OS.get_name()=="Windows"
	root.size=Vector2i(720,720);root.always_on_top=true
	var views:Array=[];var hosts:Array=[];var paints:Array=[]
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var host:=Node2D.new();host.modulate=Color(.87,.94,1,.8);vp.add_child(host);hosts.append(host)
		var paint:=Paint.new();paint.moon=moon;paint.packet_mode=mode==1 and supported;paint.use_parent_material=true;host.add_child(paint);paints.append(paint)
	var tint:=ShaderMaterial.new();tint.shader=Shader.new();tint.shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,1.0); }"
	var flood:=ShaderMaterial.new();flood.shader=load("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",350.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for material in [null,tint,flood]:
		for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			for q in range(4):
				for raised in [false,true]:
					for phase in ["boarding","flood","drain","outbound"]:
						for host in hosts:host.material=material;host.texture_filter=filtering
						var room:Dictionary={"id":"moonbay","rotation":q,"ocean_side":"north" if q%2==0 else "west","raised_walls":raised,"shelf_helmet_visible":true,"water_level":.4 if phase=="drain" else 0.0,"moonbay_mission":{"phase":phase,"progress":.375,"cycle_clock":1.375,"chamber_water":.4,"damage":0},"ports":[{"cell":Vector2i.ZERO,"side":"north"}],"port_open":[.5]}
						for paint in paints:paint.room=room;paint.bounds=Rect2(50.375,55.1875,610 if q%2==0 else 384,610 if q%2==0 else 384);paint.queue_redraw()
						await process_frame;await RenderingServer.frame_post_draw;pairs+=1
						var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
						var equal:bool=a.get_data()==b.get_data()
						if not equal and failures==0:a.save_png("user://surface-reference-failure.png");b.save_png("user://surface-candidate-failure.png")
						check(equal,"Exact Moonbay surface pixels "+str([material,filtering,q,raised,phase]))
						check(a.get_used_rect().has_area(),"Visible native room")
						var counts:Array=[]
						for vp in views:counts.append(RenderingServer.viewport_get_render_info(vp.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
						check(counts[1]<counts[0] if supported else counts[1]==counts[0],"Surface packets reduce native submissions "+str(counts))
						if counts[1]<counts[0]:reduced_pairs+=1
						minimum_saving=mini(minimum_saving,counts[0]-counts[1]);maximum_saving=maxi(maximum_saving,counts[0]-counts[1])
	views[1].get_texture().get_image().save_png("user://surface-packets.png")
	var weak:WeakRef=weakref(paints[1])
	for vp in views:vp.queue_free()
	views.clear();hosts.clear();paints.clear()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Surface packet owner released")
	FileAccess.open("user://surface-packets-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"pairs":pairs,"reduced_pairs":reduced_pairs,"minimum_saved_calls":minimum_saving,"maximum_saved_calls":maximum_saving,"failures":failures}))
	print("MOON_SURFACE_PACKETS ",checks," checks ",pairs," pairs ",failures," failures");quit(1 if failures else 0)
