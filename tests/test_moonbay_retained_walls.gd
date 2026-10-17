extends SceneTree
const ReferenceMoon=preload("res://rooms/large-rooms/moonbay.gd")
const Candidate=preload("res://scripts/moonbay_base_canvas.gd")
const Settings=preload("res://scripts/title_settings.gd")
const Store=preload("res://scripts/room_layout_store.gd")
class Immediate extends Node2D:
	var state:Dictionary={}
	var bounds:Rect2
	func _draw():ReferenceMoon.draw(self,state,bounds)
var pairs:int=0
var failures:int=0
var views:Array=[]
var hosts:Array=[]
var reference
var candidate
func _init():call_deferred("run")
func compare(label:String):
	await process_frame;await RenderingServer.frame_post_draw
	var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image();pairs+=1
	if a.get_data()!=b.get_data():
		failures+=1
		if failures==1:
			a.save_png("user://wall-reference-failure.png");b.save_png("user://wall-candidate-failure.png")
			FileAccess.open("user://wall-failure.json",FileAccess.WRITE).store_string(JSON.stringify({"label":label,"state":reference.state,"rect":reference.bounds},"  "))
	if label=="sample":b.save_png("user://wall-accepted-sample.png")
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/") or DisplayServer.get_name()=="headless":quit(2);return
	print("ISOLATION_VERIFIED ",OS.get_user_data_dir())
	root.size=Vector2i(720,720)
	for mode in range(2):
		var vp:=SubViewport.new();vp.size=Vector2i(720,720);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(vp);views.append(vp)
		var host:=Node2D.new();host.modulate=Color(.87,.94,1,.8);vp.add_child(host);hosts.append(host)
	reference=Immediate.new();reference.use_parent_material=true;hosts[0].add_child(reference)
	candidate=Candidate.new();candidate.use_parent_material=true;candidate.retain_wall_commands=true;hosts[1].add_child(candidate)
	var shader:=Shader.new();shader.code="shader_type canvas_item; void fragment(){ COLOR *= vec4(0.8,0.9,0.7,1.0); }"
	var mat:=ShaderMaterial.new();mat.shader=shader
	var saved_motion:bool=Settings.reduced_motion
	for material_on in [false,true]:
		for filtering in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
			for q in range(4):
				for ocean in ["west","north"]:
					for raised in [false,true]:
						for phase in ["boarding","disembark","drain"]:
							for clock_spec in [[.375,false],[.875,false],[.875,true]]:
								Settings.reduced_motion=clock_spec[1]
								for host in hosts:host.material=mat if material_on else null;host.texture_filter=filtering
								var mission:Dictionary={"phase":phase,"cycle_clock":clock_spec[0],"chamber_water":.4 if phase=="disembark" else 1.0 if phase=="drain" else 0.0,"station_open":phase!="disembark","ocean_open":phase=="disembark","damage":0}
								var room:Dictionary={"id":"moonbay","pos":Vector2i.ZERO,"rotation":q,"ocean_side":ocean,"raised_walls":raised,"shelf_helmet_visible":true,"water_level":.4 if phase=="drain" else 0.0,"machine_clock":clock_spec[0],"moonbay_mission":mission,"studio_props":[],"ports":[{"cell":Vector2i.ZERO,"side":"north"},{"cell":Vector2i(1,1),"side":"south"}],"port_open":[0.0,.5 if phase=="drain" else 1.0]}
								var bounds:=Rect2(50.375,55.1875,610 if q%2==0 else 384,610 if q%2==0 else 384)
								reference.state=room;reference.bounds=bounds;reference.queue_redraw();candidate.submit(room,bounds)
								await compare(str([material_on,filtering,q,ocean,raised,phase,clock_spec]))
	# Explicit self tint must fall back to the complete immediate paint, then
	# recover retained order when white returns, in the very next rendered frame.
	for tint in [Color(.9,.75,1,.8),Color.WHITE]:
		reference.self_modulate=tint;candidate.self_modulate=tint
		reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
		await compare("self tint "+str(tint))
	# Mission animation must redraw water/sub/gates without rebuilding the
	# unchanged floor, hull, shelf and grating commands beneath them.
	Settings.reduced_motion=false
	reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
	await compare("live mission baseline")
	var prefix_before:int=candidate.redraws
	for spec in [[1.125,"launch"],[1.875,"work"],[2.375,"return"],[2.75,"outbound"],[3.0,"boarding"],[3.25,"idle"]]:
		var clock:float=spec[0]
		var changed:Dictionary=reference.state.duplicate(true)
		changed.moonbay_mission.phase=spec[1]
		changed.moonbay_mission.cycle_clock=clock
		changed.moonbay_mission.progress=clock*.2
		changed.moonbay_mission.chamber_water=.2+clock*.2
		changed.moonbay_mission.damage=1
		changed.machine_clock=clock
		reference.state=changed;reference.queue_redraw();candidate.submit(changed,reference.bounds)
		await compare("live mission "+str(clock))
		if candidate.redraws!=prefix_before:failures+=1;push_error("Mission-only changes rebuilt static Moonbay prefix")
	# Each of these inputs is read by the retained prefix, including external
	# doors and water around the room. They must invalidate it immediately.
	for mutation in ["port","flood","helmet","locker","bounds"]:
		var changed:Dictionary=reference.state.duplicate(true)
		var bounds:Rect2=reference.bounds
		match mutation:
			"port":changed.port_open[0]=.625
			"flood":changed.water_level=.75
			"helmet":changed.shelf_helmet_visible=false
			"locker":changed.studio_props=[{"id":"library/sp-airlock-4","rect":Rect2(274,-112,76,88)}]
			"bounds":bounds.position+=Vector2(.375,.1875)
		var before:int=candidate.redraws
		reference.state=changed;reference.bounds=bounds;reference.queue_redraw();candidate.submit(changed,bounds)
		await compare("prefix invalidation "+mutation)
		if candidate.redraws<=before:failures+=1;push_error("Static Moonbay prefix missed "+mutation)
	if "retain_base_commands" in candidate:
		for enabled in [false,true]:
			candidate.retain_base_commands=enabled
			reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
			await compare("base retention toggle "+str(enabled))
	var flood:=ShaderMaterial.new();flood.shader=load("res://scripts/flood_submersion.gdshader")
	flood.set_shader_parameter("waterline_y",350.0);flood.set_shader_parameter("world_scale",.73)
	flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for material in [flood,null,mat]:
		for host in hosts:host.material=material
		reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
		await compare("inherited material "+str(material))

	Settings.reduced_motion=saved_motion
	reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
	await compare("sample")
	if candidate.wall_tail==null or candidate.wall_tail.hits<=candidate.wall_tail.redraws:failures+=1;push_error("Static wall reuse not exercised")
	var saved_revision:int=Store.revision
	var old_redraws:int=candidate.wall_tail.redraws
	Store.revision+=1
	reference.queue_redraw();candidate.submit(reference.state,reference.bounds)
	await compare("layout revision")
	if candidate.wall_tail.redraws<=old_redraws:failures+=1;push_error("Studio revision failed to invalidate retained walls")
	Store.revision=saved_revision
	var result:Dictionary={"pairs":pairs,"walls_redraws":candidate.wall_tail.redraws,"walls_hits":candidate.wall_tail.hits,"gates_draws":candidate.wall_tail.gates.draws}
	var release_refs:Array=[weakref(candidate),weakref(candidate.wall_tail),weakref(candidate.wall_tail.gates)]
	if "water_body" in candidate and candidate.water_body!=null:release_refs.append(weakref(candidate.water_body))
	for vp in views:vp.queue_free()
	# Observe destruction rather than assuming a fixed scene-swap delay.
	for attempt in range(8):
		var alive:bool=false
		for ref in release_refs:if ref.get_ref()!=null:alive=true
		if not alive:break
		await process_frame;await RenderingServer.frame_post_draw
	for ref in release_refs:
		if ref.get_ref()!=null:failures+=1;push_error("Retained wall/gate canvas survived scene exit")
	result.failures=failures
	FileAccess.open("user://wall-cache-result.json",FileAccess.WRITE).store_string(JSON.stringify(result,"  "))
	print("MOON_WALL_RASTER pairs=",pairs," failures=",failures," walls=",result.walls_redraws," hits=",result.walls_hits," lifecycle=",failures==0)
	quit(1 if failures else 0)
