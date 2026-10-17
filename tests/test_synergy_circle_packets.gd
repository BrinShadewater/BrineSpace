extends SceneTree
class Paint extends "res://scripts/grid_canvas.gd":
	var profile:="flow"
	var clock:=0.0
	var cell:=384.0
	var factor:=1.0
	var angle:=0.0
	var draws:=0
	func _ready():pass
	func _process(_delta):pass
	func _draw():
		draw_target=self;draws+=1
		draw_set_transform(Vector2(360.375,360.1875),angle,Vector2(factor,factor*.91))
		_draw_functioning_synergy({"fx_profile":profile},Vector2(-cell*.5,0),Vector2(cell*.5,0),Color(.31,.64,.55),cell,clock)
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	var probe:=Paint.new()
	check("batch_synergy_circles" in probe,"Ordered synergy circle packet path is available")
	probe.free()
	if failures:quit(1);return
	root.size=Vector2i(720,720);root.always_on_top=true
	var views:Array=[];var paints:Array=[]
	var packets_supported:bool=OS.get_name()=="Windows"
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var paint:=Paint.new();paint.set("batch_synergy_circles",mode==1);vp.add_child(paint);paints.append(paint)
	var shader:=Shader.new();shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,0.8); }"
	var material:=ShaderMaterial.new();material.shader=shader
	for material_on in [false,true]:
		for profile in ["flow","power","signal","care","containment"]:
			for clock in [0.0,.375,16.75]:
				for factor in [.25,.73,1.0,1.3]:
					for angle in [0.0,.173]:
						for paint in paints:
							paint.profile=profile;paint.clock=clock;paint.factor=factor;paint.angle=angle
							paint.modulate=Color(.8,.9,1,.7);paint.material=material if material_on else null;paint.queue_redraw()
						await compare(views,str([material_on,profile,clock,factor,angle]),packets_supported)
	# Repeated construction and native fallback must recover in the next frame.
	for supported in [false,packets_supported]:
		for paint in paints:paint.synergy_geometry_supported=supported;paint.clock=.875;paint.queue_redraw()
		await compare(views,"platform fallback "+str(supported),supported)
	for enabled in [false,true]:
		paints[1].set("batch_synergy_circles",enabled)
		for paint in paints:paint.queue_redraw()
		await compare(views,"packet toggle "+str(enabled),enabled and packets_supported)
	views[1].get_texture().get_image().save_png("user://synergy-packets.png")
	var weak:WeakRef=weakref(paints[1])
	for vp in views:vp.queue_free()
	views.clear();paints.clear()
	for attempt in range(8):
		if weak.get_ref()==null:break
		await process_frame
	check(weak.get_ref()==null,"Packet owner released after scene exit")
	FileAccess.open("user://synergy-packets-result.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"pairs":pairs,"failures":failures}))
	print("SYNERGY_PACKETS ",checks," checks ",pairs," pairs ",failures," failures")
	quit(1 if failures else 0)
func compare(views:Array,label:String,reduced:bool):
	await process_frame;await RenderingServer.frame_post_draw
	var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image();pairs+=1
	check(a.get_data()==b.get_data(),"Exact synergy pixels "+label)
	check(a.get_used_rect().has_area(),"Visible reference "+label)
	var counts:Array=[]
	for vp in views:counts.append(RenderingServer.viewport_get_render_info(vp.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
	check(counts[0]-counts[1]==(7 if reduced else 0),"Ordered packet saves exactly seven submissions "+label+" "+str(counts))
