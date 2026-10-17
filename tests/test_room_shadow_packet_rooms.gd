extends SceneTree
const Reference=preload("res://rooms/whole-room/room_lighting.gd")
const Candidate=preload("res://rooms/whole-room/room_lighting.gd")
const Batch=preload("res://scripts/contact_shadow_batch.gd")
const OUT="user://"
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":push_error("Room shadow checks need a native display");quit(2);return
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR")
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--profile="):expected=arg.trim_prefix("--profile=")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected:
		push_error("Wrong profile");quit(2);return
	preload("res://tools/release_benchmark.gd").configure_test_window(root)
	root.set_disable_input(true)
	var results:=[]
	for path in ["res://rooms/underwater/brine-core/brine_core_view.gd","res://rooms/full-wall-v1/life_support_view.gd","res://rooms/full-wall-v1/tidal_condenser_view.gd","res://rooms/full-wall-v1/crew_hab_view.gd"]:
		var room=load(path).new()
		room.embedded=true
		room.hide()
		root.add_child(room)
		for quarter in 4:
			room.configure_embedded(quarter,[],false,0.0)
			for aa in [1.0,2.0]:
				for scale_value in [.73,1.0]:
					for offset in [.5]:
						for level in [0.0,.501,1.0]:
							var views:=[]
							for mode in 2:
								var viewport:=SubViewport.new()
								viewport.size=Vector2i(512,512)
								viewport.transparent_bg=true
								viewport.oversampling_override=aa
								viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS
								root.add_child(viewport)
								var canvas:=Node2D.new()
								viewport.add_child(canvas)
								canvas.draw.connect(func():
									room.render_into(canvas,Vector2.ONE*(256+offset),scale_value,true,false)
									canvas.draw_set_transform(Vector2.ONE*(256+offset),0,Vector2.ONE*scale_value)
									var previous:bool=Reference.batch_contact_shadows
									Reference.batch_contact_shadows=true
									var previous_combined:bool=Reference.combine_room_shadows
									Reference.combine_room_shadows=mode==1
									if mode==0:Reference.draw_equipment_shadows(canvas,room.props,level,room)
									else:Candidate.draw_equipment_shadows(canvas,room.props,level,room)
									Reference.combine_room_shadows=previous_combined
									Reference.batch_contact_shadows=previous)
								views.append(viewport)
							await RenderingServer.frame_post_draw
							var a:Image=views[0].get_texture().get_image()
							var b:Image=views[1].get_texture().get_image()
							var exact:=a.get_data()==b.get_data() and a.get_used_rect().has_area() and a.get_used_rect().has_area()
							if results.is_empty() or (not exact and results.filter(func(row):return not row.exact).size()<2):
								a.save_png(OUT+"reference-%d.png"%results.size())
								b.save_png(OUT+"candidate-%d.png"%results.size())
							results.append({"room":path,"rotation":quarter,"aa":aa,"scale":scale_value,"offset":offset,"level":level,"exact":exact,"before":views[0].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),"after":views[1].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME)})
							for view in views:view.queue_free()
							await process_frame
		room.queue_free()
		await process_frame
	FileAccess.open(OUT+"results.json",FileAccess.WRITE).store_string(JSON.stringify({"cases":results,"cache_hits":Batch.hits,"cache_misses":Batch.misses,"fallbacks":Batch.fallbacks,"packet_hits":Candidate.room_shadow_packet_hits,"packet_misses":Candidate.room_shadow_packet_misses,"packet_fallbacks":Candidate.room_shadow_packet_fallbacks},"\t"))
	var exact_count:=results.filter(func(row):return row.exact).size()
	print("SHADOW RESEARCH ",exact_count,"/",results.size()," exact; fallback=",Batch.fallbacks)
	var bounded:bool=Candidate.room_shadow_packet_bytes<=Candidate.ROOM_SHADOW_PACKET_BYTES
	var saved_calls:=results.filter(func(row):return row.exact and row.after<row.before).size()
	print("ROOM SHADOW PACKET saved-call cases=",saved_calls)
	quit(0 if exact_count==results.size() and bounded and saved_calls>0 else 2)
