extends SceneTree
class Original extends "res://scripts/room_content_canvas.gd":
	func paint(slot: DrawSlot) -> void:
		var started := Time.get_ticks_usec() if profile_enabled else 0
		if slot.item.has("prop") and slot.item.prop.get("layout_hidden",false): return
		var saved := {}
		for field in view_state:
			saved[field] = renderer.get(field)
			renderer.set(field,view_state[field])
		var previous_painter: CanvasItem = renderer.painter
		var previous_actor: Vector2 = renderer.actor
		var previous_texture: Texture2D = renderer.external_actor_texture
		slot.draw_set_transform(draw_origin,0,Vector2.ONE*draw_scale)
		renderer.painter = slot
		if slot.item.kind in ["prop","prop_pass","prop_base","prop_effects","library_base","library_live"]:
			preload("res://scripts/room_layout_store.gd").draw_flip(renderer,slot,slot.item.prop,draw_origin,draw_scale)
		match slot.item.kind:
			"prop":
				var artwork: Dictionary=slot.item.prop.duplicate()
				artwork.id=artwork.get("copy_source",artwork.id)
				if artwork.get("library_asset",false) and not artwork.get("custom_library_draw",false): preload("res://scripts/room_asset_library.gd").draw(renderer,artwork)
				else: renderer.draw_registered_prop(artwork)
			"library_base", "library_live":
				var artwork: Dictionary = slot.item.prop.duplicate()
				artwork.id = artwork.get("copy_source",artwork.id)
				if slot.item.kind == "library_base": preload("res://scripts/room_asset_library.gd").draw_base(renderer,artwork)
				else: preload("res://scripts/room_asset_library.gd").draw_live(renderer,artwork)
			"prop_pass": renderer.call(slot.item.method,slot.item.prop)
			"prop_base": renderer.draw_prop_base(slot.item.prop)
			"prop_effects": renderer.draw_prop_animation(slot.item.prop)
			"actor": renderer.draw_actor()
			"crew":
				renderer.actor = slot.item.member.position
				renderer.external_actor_texture = slot.item.member.texture
				renderer.draw_actor()
		renderer.painter = previous_painter
		renderer.actor = previous_actor
		renderer.external_actor_texture = previous_texture
		for field in saved: renderer.set(field,saved[field])
		if slot.live: live_redraws += 1
		else: static_redraws += 1
	
		if profile_enabled: draw_usec += Time.get_ticks_usec()-started

const Candidate=preload("res://scripts/room_content_canvas.gd")
const Settings=preload("res://scripts/title_settings.gd")
class Renderer extends Node2D:
	var painter:CanvasItem
	var machine_clock:=91.0
	var operating:=false
	var quarter:=0
	var actor:=Vector2(1,2)
	var external_actor_texture:Texture2D
	func prop_visual_bounds(prop:Dictionary)->Rect2:return prop.rect
var checks:=0
var failures:=0
var pairs:=0
func check(ok:bool,label:String):
	checks+=1
	if not ok:failures+=1;push_error(label)
func _init():call_deferred("run")
func frame():
	await process_frame
	await RenderingServer.frame_post_draw
func run():
	if OS.get_environment("BRINESPACE_TEST_USER_DIR")!=OS.get_user_data_dir().replace(char(92),"/"):quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(512,512)
	var cap:=SubViewport.new();cap.size=Vector2i(512,512);cap.transparent_bg=true;cap.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(cap)
	var parent:=Node2D.new();parent.position=Vector2(230.375,250.1875);parent.scale=Vector2(.91,1.03);parent.modulate=Color(.8,.9,1,.7);cap.add_child(parent)
	var reference:=Original.new();var candidate:=Candidate.new();parent.add_child(reference);parent.add_child(candidate)
	var renderer:=Renderer.new();root.add_child(renderer);reference.renderer=renderer;candidate.renderer=renderer;candidate.profile_enabled=true
	var patterns_host=preload("res://scripts/grid_canvas.gd").new()
	candidate.screen_patterns=patterns_host.screen_patterns
	var a:=Original.DrawSlot.new();var b:=Candidate.DrawSlot.new();reference.add_child(a);candidate.add_child(b)
	var reg:Dictionary={"width":512,"height":512,"pivot":Vector2(256,256),"operating_screens":[[20,20,200,120],[230,20,240,90],[20,190,90,120]],"operating_screen_color":"#35bbc7","effects":[{"kind":"specimen_glow","area":[.1,.65,.2,.2]},{"kind":"field","area":[.4,.65,.2,.2]},{"kind":"hologram","area":[.7,.65,.2,.2]}]}
	var prop:Dictionary={"id":"copied","copy_source":"library/sp-fixture","registration":reg,"rect":Rect2(-120,-120,240,240),"layout_flip":Vector2.ONE}
	a.item={"kind":"library_live","prop":prop};b.item=a.item.duplicate(true)
	var old_motion:bool=Settings.reduced_motion
	for flip in [Vector2.ONE,Vector2(-1,1)]:
		a.item.prop.layout_flip=flip;b.item.prop.layout_flip=flip
		for reduced in [false,true]:
			Settings.reduced_motion=reduced
			for operating in [false,true]:
				a.live=operating;b.live=operating
				for clock in [0.0,.375,3.125]:
					for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
						parent.texture_filter=filter
						var state:Dictionary={"operating":operating,"machine_clock":clock,"quarter":2,"actor":Vector2(9,7)}
						reference.view_state=state.duplicate();candidate.view_state=state.duplicate()
						reference.show();candidate.hide();a.queue_redraw();await frame()
						var expected:PackedByteArray=cap.get_texture().get_image().get_data()
						check(renderer.painter==null and renderer.machine_clock==91.0 and not renderer.operating and renderer.quarter==0 and renderer.actor==Vector2(1,2),"Original restores renderer")
						reference.hide();candidate.show();b.queue_redraw();await frame();pairs+=1
						check(expected==cap.get_texture().get_image().get_data(),"Exact library screen/effect raster")
						check(renderer.painter==null and renderer.machine_clock==91.0 and not renderer.operating and renderer.quarter==0 and renderer.actor==Vector2(1,2),"Candidate preserves renderer")
	check(b.prepared_screens!=null and b.prepared_screens.screens.size()==3,"Prepared monitor path exercised")
	var actual_assets:=0
	var Library=load("res://scripts/room_asset_library.gd")
	Settings.reduced_motion=false
	var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",260.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for id in Library.entries():
		if not str(id).begins_with("library/sp-"):continue
		var data:Dictionary=Library.entries()[id].data
		if data.has("drone_dock") or data.has("aquarium") or (data.get("operating_screens",[]).is_empty() and data.get("effects",[]).is_empty()):continue
		var region:Array=data.region
		var registration:Dictionary={"width":float(region[2]),"height":float(region[3]),"pivot":Vector2(region[0]+region[2]*.5,region[1]+region[3]),"pieces":[]}
		for key in ["effects","operating_screens","operating_screen_color"]:
			if data.has(key):registration[key]=data[key]
		if data.get("mirror_horizontal",false):registration=Library.mirror_registration(registration)
		var artwork:Dictionary={"id":id,"registration":registration,"rect":Rect2(-100,-100,200,200.0*float(region[3])/float(region[2])),"layout_flip":Vector2.ONE}
		a.item={"kind":"library_live","prop":artwork};b.item=a.item.duplicate(true);a.live=true;b.live=true
		actual_assets+=1
		for wet in [false,true]:
			a.material=flood if wet else null;b.material=a.material
			var state:Dictionary={"operating":true,"machine_clock":1.375,"quarter":0,"actor":Vector2(9,7)}
			reference.view_state=state.duplicate();candidate.view_state=state.duplicate()
			reference.show();candidate.hide();a.queue_redraw();await frame()
			var expected:PackedByteArray=cap.get_texture().get_image().get_data()
			reference.hide();candidate.show();b.queue_redraw();await frame();pairs+=1
			check(expected==cap.get_texture().get_image().get_data(),"Actual registration exact "+str(id))
	a.material=null;b.material=null
	a.item={"kind":"library_live","prop":prop.duplicate(true)}
	b.item=a.item.duplicate(true)
	a.item.prop.layout_flip=Vector2.ONE;b.item.prop.layout_flip=Vector2.ONE
	Settings.reduced_motion=false
	for fps in [30,60,120]:
		for speed in [1.0,2.0,4.0]:
			for tick in [0,1,7,19,31,fps]:
				var state:Dictionary={"operating":true,"machine_clock":float(tick)/fps*speed,"quarter":0,"actor":Vector2(9,7)}
				reference.view_state=state.duplicate();candidate.view_state=state.duplicate()
				reference.show();candidate.hide();a.queue_redraw();await frame()
				var expected:PackedByteArray=cap.get_texture().get_image().get_data()
				reference.hide();candidate.show();b.queue_redraw();await frame();pairs+=1
				check(expected==cap.get_texture().get_image().get_data(),"Waveform clock exact: %d FPS / %s speed / %d tick"%[fps,speed,tick])
	check(candidate.simple_library_paints>0,"Fast path exercised")
	check(candidate.library_draw_context.painter==null,"No painter retained")
	check(reference.static_redraws==candidate.static_redraws and reference.live_redraws==candidate.live_redraws,"Redraw counters preserved")
	b.item.prop.layout_flip=Vector2.ONE
	b.item.prop.registration=reg.duplicate(true)
	for key in ["aquarium","drone_dock"]:
		b.item.prop.registration[key]={};check(not candidate._can_draw_simple_library(b),"Special registration falls back");b.item.prop.registration.erase(key)
	b.item.prop.layout_flip=Vector2.ONE
	b.item.prop.custom_library_draw=true;check(not candidate._can_draw_simple_library(b),"Custom artwork falls back");b.item.prop.erase("custom_library_draw")
	b.item.prop.portable_view=renderer;check(not candidate._can_draw_simple_library(b),"Portable artwork falls back");b.item.prop.erase("portable_view")
	b.item.prop.erase("layout_flip");check(not candidate._can_draw_simple_library(b),"Uncached flip falls back")
	check(candidate.screen_patterns.builds>0 and candidate.screen_patterns.builds<pairs,"Shared waveform reuse exercised")
	check(candidate.screen_patterns.waves.size()<=64,"Waveform cache is bounded")
	var patterns_ref:WeakRef=weakref(candidate.screen_patterns)
	patterns_host.free()
	var prepared_ref:WeakRef=weakref(b.prepared_screens)
	Settings.reduced_motion=old_motion;parent.queue_free();renderer.queue_free();await frame()
	check(prepared_ref.get_ref()==null,"Prepared monitor geometry releases with its slot")
	check(patterns_ref.get_ref()==null,"Shared waveform cache releases with scene")
	FileAccess.open("user://context.json",FileAccess.WRITE).store_string(JSON.stringify({"checks":checks,"failures":failures,"raster_pairs":pairs,"actual_registrations":actual_assets}))
	print("LIVE_CONTEXT ",checks," checks; ",failures," failures");quit(1 if failures else 0)
