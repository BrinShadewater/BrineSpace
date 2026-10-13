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
