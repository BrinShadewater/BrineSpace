extends SceneTree
const Shell=preload("res://rooms/whole-room/painted_shell.gd")
class Room extends Node:
	var quarter:=0
	var edges:Array=[]
class Paint extends Node2D:
	var context
	var candidate:=false
	var factor:=1.0
	var angle:=0.0
	var offset:=Vector2.ZERO
	func _draw():
		draw_set_transform(Vector2(400,400)+offset,angle,Vector2(factor,factor*.93))
		var script=load("res://rooms/whole-room/painted_shell.gd")
		script.batch_cap_polygons=candidate
		context.tops(self)
var views:Array=[]
var paints:Array=[]
var pairs:=0
var failures:=0
var visible:=0
func _init():call_deferred("run")
func run():
	if OS.get_user_data_dir().replace(char(92),"/")!=OS.get_environment("BRINESPACE_TEST_USER_DIR") or DisplayServer.get_name()=="headless":quit(2);return
	if not Shell.new().has_method("flush_cap_packet"):
		push_error("CAP_BATCH missing ordered polygon packet");quit(1);return
	root.size=Vector2i(600,300);root.always_on_top=true;root.set_disable_input(true)
	OS.set_environment("BRINE_SILENT","1");AudioServer.set_bus_mute(0,true)
	for screen in DisplayServer.get_screen_count():
		if screen!=DisplayServer.get_primary_screen():root.current_screen=screen;break
	for lane in range(2):
		var viewport:=SubViewport.new();viewport.size=Vector2i(800,800);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;root.add_child(viewport);views.append(viewport)
		var paint:=Paint.new();paint.candidate=lane==1;paint.modulate=Color(.83,.71,.9,.73);viewport.add_child(paint);paints.append(paint)
	var flood:=ShaderMaterial.new();flood.shader=preload("res://scripts/flood_submersion.gdshader");flood.set_shader_parameter("waterline_y",120.0);flood.set_shader_parameter("world_scale",.73);flood.set_shader_parameter("depth",.65);flood.set_shader_parameter("clock",1.375)
	for id in ["reactor","crew_hab","life_support"]:
		paints[0].context=Shell.context(null,id);paints[1].context=Shell.context(null,id)
		for paint in paints:
			var room:=Room.new();room.edges=[{"center":Vector2(0,-192),"horizontal":true,"open":true},{"center":Vector2(192,0),"horizontal":false,"open":true},{"center":Vector2(0,192),"horizontal":true,"open":true},{"center":Vector2(-192,0),"horizontal":false,"open":true}]
			paint.add_child(room);paint.context.room=room
		for factor in [.13081395,.5,1.0,1.37]:
			for quarter in range(4):
				for state in range(4):
					for filter in [CanvasItem.TEXTURE_FILTER_NEAREST,CanvasItem.TEXTURE_FILTER_LINEAR]:
						for wet in [false,true]:
							for paint in paints:
								paint.factor=factor;paint.angle=quarter*PI*.5;paint.offset=Vector2(.375,.125) if quarter%2==0 else Vector2.ZERO;paint.texture_filter=filter;paint.material=flood if wet else null;paint.context.room.set_meta("raised_north_visible",bool(state%2))
								paint.context.ports=[0,1,2,3] if state>=2 else []
								for edge in paint.context.room.edges:edge.open=state<2
								paint.queue_redraw()
							await process_frame;await RenderingServer.frame_post_draw
							pairs+=1
							var a:Image=views[0].get_texture().get_image();var b:Image=views[1].get_texture().get_image()
							if a.get_used_rect().has_area():visible+=1
							if a.get_data()!=b.get_data():
								failures+=1
								if failures==1:a.save_png("user://reference.png");b.save_png("user://candidate.png");print("FIRST_DIFF ",id," ",factor," ",quarter," ",state," ",filter," ",wet)
							var counts:=[]
							for view in views:counts.append(RenderingServer.viewport_get_render_info(view.get_viewport_rid(),RenderingServer.VIEWPORT_RENDER_INFO_TYPE_CANVAS,RenderingServer.VIEWPORT_RENDER_INFO_DRAW_CALLS_IN_FRAME))
							if counts[1]>=counts[0]:failures+=1;print("NO_CALL_REDUCTION ",counts)
	FileAccess.open("user://painted-cap-results.json",FileAccess.WRITE).store_string(JSON.stringify({"pairs":pairs,"visible":visible,"failures":failures,"scope":"Ordered cap polygons; native rectangles and closed-door operations retained"}))
	print("PAINTED_CAP_BATCH ",pairs," pairs; visible=",visible," failures=",failures)
	quit(1 if failures>0 else 0)
