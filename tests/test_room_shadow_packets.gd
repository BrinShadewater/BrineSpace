extends SceneTree
const Reference=preload("res://rooms/whole-room/room_lighting.gd")
const Candidate=preload("res://rooms/whole-room/room_lighting.gd")
const Batch=preload("res://scripts/contact_shadow_batch.gd")
const OUT="user://"
func _init() -> void:call_deferred("run")
func run() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("Contact-shadow pixel checks require a native display");quit(2);return
	var expected:=OS.get_environment("BRINESPACE_TEST_USER_DIR").replace("\\","/").simplify_path()
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--profile="):expected=arg.trim_prefix("--profile=")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\","/").simplify_path()!=expected:
		push_error("Wrong profile");quit(2);return
	preload("res://tools/release_benchmark.gd").configure_test_window(root)
	root.set_disable_input(true)
	var props:Array=[
		{"rect":Rect2(-145,-100,65,40)},
		{"rect":Rect2(-110,-75,80,50)},
		{"rect":Rect2(162,150,65,60)},
		{"rect":Rect2(-190,-170,23,23)},
		{"rect":Rect2(179.4,40,30,20)},
		{"rect":Rect2(-40,20,60,60),"corner":true,"collision_boxes":[[0,0,.3,1],[.3,.7,.7,.3]]},
		{"rect":Rect2(50,-120,50,80),"footprint":[.1,.8,.5,.02]},
		{"rect":Rect2(40,70,100,80),"registration":{"owns_contact_shadow":true}},
		{"rect":Rect2(10,70,60,80),"layout_hidden":true}]
	var results:=[]
	for aa in [0.8333333333333333,1.0,1.5,2.0]:
		for scale_value in [.5,.73,1.0,1.25]:
			for offset in [0.0,.5]:
				for level in [0.0,.501,.502,1.0]:
					props[0].rect.position.x=-145.0+float(results.size()%3)*.37
					props[1]["layout_hidden"]=results.size()%5==0
					var case_props:Array=props.duplicate(true)
					if level!=.502:
						for i in [3,4,6]:case_props[i].layout_hidden=true
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
						if level==.502:canvas.oversampling_with_scale=CanvasItem.OVERSAMPLING_WITH_SCALE_ENABLED
						canvas.draw.connect(func():
							canvas.draw_set_transform(Vector2.ONE*(256+offset),0,Vector2.ONE*scale_value)
							var previous:bool=Reference.batch_contact_shadows
							Reference.batch_contact_shadows=true
							var previous_combined:bool=Reference.combine_room_shadows
							Reference.combine_room_shadows=mode==1
							if mode==0:Reference.draw_equipment_shadows(canvas,case_props,level)
							else:Candidate.draw_equipment_shadows(canvas,case_props,level)
							Reference.combine_room_shadows=previous_combined
							Reference.batch_contact_shadows=previous)
						views.append(viewport)
					await RenderingServer.frame_post_draw
					var a:Image=views[0].get_texture().get_image()
					var b:Image=views[1].get_texture().get_image()
					var exact:=a.get_data()==b.get_data() and a.get_used_rect().has_area()
					if results.is_empty() or (not exact and results.filter(func(row):return not row.exact).size()<2):
						a.save_png(OUT+"reference-%d.png"%results.size())
						b.save_png(OUT+"candidate-%d.png"%results.size())
					results.append({"aa":aa,"scale":scale_value,"offset":offset,"level":level,"exact":exact,"before":views[0].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME),"after":views[1].get_render_info(Viewport.RENDER_INFO_TYPE_CANVAS,Viewport.RENDER_INFO_DRAW_CALLS_IN_FRAME)})
					for view in views:view.queue_free()
					await process_frame
	FileAccess.open(OUT+"results.json",FileAccess.WRITE).store_string(JSON.stringify({"cases":results,"cache_hits":Batch.hits,"cache_misses":Batch.misses,"fallbacks":Batch.fallbacks,"packet_entries":Candidate.room_shadow_packets.size(),"packet_hits":Candidate.room_shadow_packet_hits,"packet_misses":Candidate.room_shadow_packet_misses,"packet_fallbacks":Candidate.room_shadow_packet_fallbacks},"\t"))
	var exact_count:=results.filter(func(row):return row.exact).size()
	print("CONTACT SHADOW BATCH ",exact_count,"/",results.size()," exact; fallback=",Batch.fallbacks)
	var bounded:bool=Candidate.room_shadow_packet_bytes<=Candidate.ROOM_SHADOW_PACKET_BYTES
	var saved_calls:=results.filter(func(row):return row.exact and row.after<row.before).size()
	print("ROOM SHADOW PACKET saved-call cases=",saved_calls)
	quit(0 if exact_count==results.size() and bounded and saved_calls>0 and Candidate.room_shadow_packets.size()<=128 else 2)
