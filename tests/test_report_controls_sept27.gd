extends SceneTree
var physics_usec:=0
var render_pre_usec:=0
var render_post_usec:=0
var failures := 0
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func _init(): call_deferred("run")
func run():
	if OS.get_environment("BRINE_REPORT_TEST") != "isolated":
		quit(2); return
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://report-controls.json"
	game.run_save_path = "user://report-controls.loop"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop()
	game.running = true
	var Dressing = preload("res://rooms/underwater/corridor_dressing.gd")
	check(Dressing.raised_point(Vector2(52,-192),35,[Vector2i.UP]).y == -192, "Connected corridor return stays below the north room")
	check(Dressing.raised_point(Vector2(52,-192),35,[]).y == -227, "Exposed corridor return retains its height")
	game.bill_npc.active = true
	# The fallback inspector can receive a database room without a station position.
	var details: String = preload("res://scripts/room_flooding.gd").inspector(game, {"id":"reactor"})
	check(details.begins_with("WATER"), "Unplaced room inspector returns water summary without a position")
	game.bill_npc.active = false
	var reactor = game.RoomDatabaseScript.get_room("reactor").duplicate(true)
	reactor.pos = game.placed_rooms[0].pos + Vector2i(1,0)
	reactor.rotation = 0
	game.placed_rooms.append(reactor); game.occupied[reactor.pos] = reactor
	game.resources.power = game._get_power_capacity()
	game._refresh_resources()
	check(not game.resource_labels.power.text.ends_with("FULL"), "Full Power retains a signed rate")
	var button = game.find_child("RoomRepairButton", true, false)
	check(button != null, "Room inspector exposes a repair button")
	if button != null:
		var room = game.placed_rooms[0]
		game.selected_room_cell = room.pos
		game.selected_card_id = ""
		room.hull_crack = 0.2
		room.erase("leak_repair")
		game.resources.metal = 10
		game._refresh_inspector_contents()
		check(button.visible and not button.disabled, "Damaged selected room can request repair")
		button.pressed.emit()
		check(room.has("leak_repair") and game.resources.metal == 8, "Repair button queues existing paid crew work")
		check(button.disabled, "Queued repairs cannot be purchased twice")
		room.erase("leak_repair"); room.hull_crack = 0.0
		game._refresh_inspector_contents()
		check(button.disabled, "Intact room cannot purchase a repair")
	var mining = game.grid_view.mining_view
	for q in range(4):
		mining.configure_embedded(q, [], true, 0.0)
		print("MINING q%d props %s" % [q, mining.props.map(func(p): return p.id)])
		check(mining.props.any(func(p): return p.id == "mining_rov"), "Mining drone and integrated pad survive q%d configuration" % q)
	var saved = preload("res://scripts/run_save.gd").read("user://mining-report.save")
	check(not saved.is_empty(), "Mining report checkpoint can be decoded")
	if not saved.is_empty():
		check(preload("res://scripts/run_save.gd").restore(game,saved), "Mining report checkpoint restores")
		game.run_save_path = "user://report-controls.loop"
		game.set_process(false); game.tick_timer.stop(); game.paused = true
		game.hardware.walls = true
		preload("res://scripts/title_settings.gd").raised_walls = true
		game.selected_card_id = ""; game.hovered_card_id = ""
		for room in game.placed_rooms:
			if room.id == "mining_drone_bay": game.selected_room_cell = room.pos; break
		game._refresh_all()
		for i in range(8): await process_frame
		game._refresh_inspector_contents(); game._focus_inspected_room()
		for i in range(3): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/mining-replay.png")
		print("REPORT REPLAY: %d rooms" % game.placed_rooms.size())
		var grid = game.grid_view
		var snapshot: Array = grid._surface_state().duplicate(true)
		var probe_room = game.occupied[game.selected_room_cell]
		probe_room.survey_clock = 1.0
		check(grid._surface_state() == snapshot, "Live survey clock does not invalidate static surfaces")
		probe_room.erase("survey_clock")
		for room_id in ["construction_drone_bay","salvage_drone_bay","life_support","tee_corridor"]:
			for room in game.placed_rooms:
				if room.id != room_id: continue
				game.selected_room_cell = room.pos
				game._refresh_inspector_contents(); game._focus_inspected_room()
				game.grid_scroll.scroll_vertical -= 80
				for i in range(3): await process_frame
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/"+room_id+"-replay.png")
				break
	var lag = preload("res://scripts/run_save.gd").read("user://lag-report.save")
	check(not lag.is_empty(), "Lag report live station decodes")
	if not lag.is_empty():
		check(preload("res://scripts/run_save.gd").restore(game,lag), "Lag report restores")
		game.run_save_path = "user://report-controls.loop"
		root.gui_disable_input = true
		game.paused = false; game.set_process(true)
		for i in range(60): await process_frame
		var frames: Array[float] = []
		var before = Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)
		var last = Time.get_ticks_usec()
		for i in range(300):
			await process_frame
			var now = Time.get_ticks_usec()
			frames.append(float(now-last)/1000.0); last = now
		frames.sort()
		var rebuilt = Vector2i(game.grid_view.floor_rebuilds,game.grid_view.wall_rebuilds)-before
		print("LAG REPLAY: rooms=%d p95=%.2fms max=%.2fms floor=%d wall=%d" % [game.placed_rooms.size(),frames[284],frames[-1],rebuilt.x,rebuilt.y])
		frames.clear()
		var original_zoom:float=game.grid_zoom
		if OS.get_environment("BRINE_CAMERA_NO_VSYNC")=="1": DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
		game.grid_view.profile_draw=true
		physics_frame.connect(func():physics_usec=Time.get_ticks_usec())
		RenderingServer.frame_pre_draw.connect(func():render_pre_usec=Time.get_ticks_usec())
		RenderingServer.frame_post_draw.connect(func():render_post_usec=Time.get_ticks_usec())
		for factor in [.7,1.3,1.0]:
			game._request_grid_zoom(original_zoom*factor)
			last=Time.get_ticks_usec()
			var requested_at:=Time.get_ticks_usec()
			var moved_at:=0
			var reveal_peak:=0.0
			var airlock_peak:=0
			for i in range(180):
				await process_frame
				if moved_at==0 and game.camera_zoom_moving:
					moved_at=Time.get_ticks_usec()
					check(moved_at-requested_at<1000000,"Cold zoom prepares without a multi-second camera wait")
					print("CAMERA PREPARE: factor=%.1f wait=%.2fms" % [factor,float(moved_at-requested_at)/1000.0])
				var now=Time.get_ticks_usec()
				frames.append(float(now-last)/1000.0);last=now
				if i<30:
					reveal_peak=maxf(reveal_peak,frames[-1])
					for cell in game.grid_view.content_canvases:
						if game.occupied.get(cell,{}).get("id","")=="airlock": airlock_peak=maxi(airlock_peak,game.grid_view.content_canvases[cell].draw_usec)
				if frames[-1]>100:
					print("CAMERA SLOW: ",JSON.stringify({"factor":factor,"frame":i,"ms":frames[-1],"wall_ms":Time.get_unix_time_from_system()*1000.0,"texture_mb":Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)/1048576.0,"static_mb":Performance.get_monitor(Performance.MEMORY_STATIC)/1048576.0,"render_ms":float(render_post_usec-render_pre_usec)/1000.0,"after_render_ms":float(now-render_post_usec)/1000.0,"before_physics_ms":float(physics_usec-render_post_usec)/1000.0,"after_physics_ms":float(now-physics_usec)/1000.0,"engine_ms":Performance.get_monitor(Performance.TIME_PROCESS)*1000.0,"physics_ms":Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)*1000.0,"focused":DisplayServer.window_is_focused(),"vsync":DisplayServer.window_get_vsync_mode(),"draw":game.grid_view.draw_profile_usec,"systems":game.frame_timing_usec}))
					var content:Array=[]
					for cell in game.grid_view.content_canvases:
						var canvas=game.grid_view.content_canvases[cell]
						content.append([game.occupied.get(cell,{}).get("id",""),canvas.draw_usec])
					content.sort_custom(func(a,b): return a[1]>b[1])
					print("CAMERA CONTENT: ",content.slice(0,5))
			print("CAMERA REVEAL: factor=%.1f first30_peak=%.2fms airlock_draw=%.2fms" % [factor,reveal_peak,airlock_peak/1000.0])
			check(airlock_peak<20000,"Airlock first draw does not synchronously decode chamber art")
			check(game.camera_zoom_target<0.0,"Camera reaches its requested zoom")
			if factor==.7:
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png("res://output/owner-report-fixes-2026-09-27/camera-replay-wide.png")
		frames.sort()
		check(frames[-1]<250.0,"Camera replay avoids the reproduced 475 ms cold-decode stall")
		print("CAMERA REPLAY: frames=%d p95=%.2fms max=%.2fms" % [frames.size(),frames[int((frames.size()-1)*.95)],frames[-1]])
		game.set_process(false); game.tick_timer.stop(); game.paused = true
	var fittings=preload("res://rooms/underwater/airlock-v4/fittings.gd")
	check(fittings.textures.has("controller"),"Prepared chamber has its controller")
	var controller=fittings.textures.get("controller")
	fittings.load_assets()
	check(fittings.textures.size()==fittings.source_paths().size(),"Full wall fittings finish after partial chamber preparation")
	check(fittings.textures.get("controller")==controller,"Wall loading reuses the prepared controller")
	if OS.get_environment("BRINE_TEXTURE_AUDIT")=="1": audit_texture_memory(game)
	print("REPORT CONTROLS: %d failures" % failures)
	game.queue_free(); await process_frame
	quit(1 if failures else 0)


func collect_texture_values(value:Variant,label:String,found:Dictionary,depth:int=0) -> void:
	if value is AtlasTexture:
		collect_texture_values(value.atlas,label+"/atlas",found,depth+1)
	elif value is Texture2D:
		var id:int=value.get_instance_id()
		if not found.has(id): found[id]={"label":label,"width":value.get_width(),"height":value.get_height(),"rgba_mib":float(value.get_width())*value.get_height()*4.0/1048576.0,"type":value.get_class()}
	elif depth<4 and value is Dictionary:
		for key in value: collect_texture_values(value[key],label+"/"+str(key),found,depth+1)
	elif depth<4 and value is Array:
		for i in range(value.size()): collect_texture_values(value[i],label+"/"+str(i),found,depth+1)

func audit_texture_memory(game:Node) -> void:
	var found:Dictionary={}
	collect_texture_values(preload("res://scripts/room_asset_library.gd").source_textures,"Library",found)
	collect_texture_values(preload("res://scripts/drone_animation.gd").textures,"Drone cache",found)
	for name in ["human_water_player","veld_player","branforth_player","marsh_player"]:
		var player=game.grid_view.get(name)
		collect_texture_values(player.frames,"Crew/"+name+"/body",found)
		collect_texture_values(player.equipment_frames,"Crew/"+name+"/equipment",found)
	var nodes:Array=[game]
	while not nodes.is_empty():
		var node:Node=nodes.pop_back()
		for property in node.get_property_list():
			if property.type==TYPE_OBJECT or (property.type in [TYPE_ARRAY,TYPE_DICTIONARY] and ("texture" in property.name or "frames" in property.name or "animations" in property.name or "overlays" in property.name)): collect_texture_values(node.get(property.name),str(node.get_path())+"/"+property.name,found)
		nodes.append_array(node.get_children())
	var rows:Array=found.values()
	rows.sort_custom(func(a,b):return a.rgba_mib>b.rgba_mib)
	var file:=FileAccess.open("res://output/owner-report-fixes-2026-09-27/texture-memory-audit.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"engine_mib":Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED)/1048576.0,"drone_cache_mib":preload("res://scripts/drone_animation.gd").cached_bytes/1048576.0,"textures":rows},"  "))
