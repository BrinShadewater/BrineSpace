extends SceneTree
const MainScene = preload("res://scenes/main.tscn")
var failures := 0
func check(value: bool, message: String) -> void:
	if not value: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	var game = MainScene.instantiate()
	var prefix := "user://crew_water_station_%d" % OS.get_process_id()
	game.meta.save_path = prefix + ".json"
	game.run_save_path = prefix + ".loop"
	game.Preferences.save_path = prefix + ".cfg"
	root.add_child(game)
	current_scene = game
	game.pending_doctrines.assign(["biosphere","recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.architect_run.clear()
	game.occupied.clear()
	game.placed_rooms.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20,20)
	for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary = game.RoomDatabaseScript.get_room("maintenance_bay" if offset == Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos = origin + offset
		room.rotation = 0
		game.occupied[room.pos] = room
		game.placed_rooms.append(room)
		game.powered_room_cells[room.pos] = true
	var center := (Vector2(origin)+Vector2.ONE*0.5)*384.0
	var north := "--north" in OS.get_cmdline_user_args()
	var south := "--south" in OS.get_cmdline_user_args() or north
	var west := "--west" in OS.get_cmdline_user_args()
	var native := "--native" in OS.get_cmdline_user_args()
	var capture_dir := "res://character/crew-underwater-v1/revisions/native-doorway/run-%d" % OS.get_process_id()
	var captures: Array = []
	if native:
		DirAccess.make_dir_recursive_absolute(capture_dir)
		root.mode = Window.MODE_WINDOWED
		root.size = Vector2i(1600,900)
		game.selected_card_id = ""
		game.hover_cell = Vector2i(-1,-1)
		game._refresh_all()
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*(0.45 if south else 0.9))
		for frame in range(4): await process_frame
		game._center_grid_on_station_now()
		for frame in range(4): await process_frame
	var results: Array = []
	for npc in [game.bill_npc,game.veld_npc,game.branforth_npc]:
		for other in [game.bill_npc,game.veld_npc,game.branforth_npc]: other.active = false
		npc.avoidance_positions.clear()
		npc.avoidance_position = Vector2.INF
		npc.rebuild(game)
		npc.active = true
		npc.direction = "north" if north else ("south" if south else ("west" if west else "east"))
		npc.set_helmet_equipped(true)
		npc.set_movement_medium("flooded")
		var start: int = npc.nearest_in_room(center+(Vector2(0,80) if south else Vector2(-80,40)),origin,false)
		var cross_room := "--cross-room" in OS.get_cmdline_user_args()
		var destination_cell := origin+(Vector2i.DOWN if south else Vector2i.RIGHT) if cross_room else origin
		var desired := center+(Vector2(0,384) if south else Vector2(384,40)) if cross_room else center+Vector2(50,40)
		var target: int = npc.nearest_in_room(desired,destination_cell,false)
		if west or north:
			var previous_start := start
			start = target
			target = previous_start
		check(start >= 0 and target >= 0,"Fixture endpoints exist")
		npc.foot = npc.graph.get_point_position(start)
		var before := Time.get_ticks_usec()
		print("WATER ROUTE START ",npc.get_script().resource_path," nodes=",npc.graph.get_point_count())
		var route: PackedVector2Array = npc.route_between(start,target)
		var elapsed := (Time.get_ticks_usec()-before)/1000.0
		print("WATER ROUTE RESULT ms=",elapsed," points=",route.size())
		if cross_room and route.is_empty():
			print("ENDPOINT CLEAR ",npc.swim_segment_clear(npc.foot,npc.foot,npc.direction)," / ",npc.swim_segment_clear(npc.graph.get_point_position(target),npc.graph.get_point_position(target),npc.direction))
			var clear_lanes: Array = []
			for y in range(-48,49,4):
				var door := center+(Vector2(y,192) if south else Vector2(192,y))
				var step := Vector2(0,16) if south else Vector2(16,0)
				if npc.swim_segment_clear(door-step,door+step,npc.direction): clear_lanes.append(y)
			print("CLEAR DOOR LANES ",clear_lanes)
		check(not route.is_empty(),"Furnished station route found")
		npc.path = npc.smooth_route(route)
		check(not npc.path.is_empty(),"Station route smoothing preserves a usable path")
		var horizontal_holds := 0
		for tick in range(600):
			if npc.path.is_empty(): break
			npc.move(0.1)
			if cross_room and (absf(npc.foot.y-(center.y+192)) if south else absf(npc.foot.x-(center.x+192))) < 12 and not npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,true):
				var previous_state: String = npc.state
				npc.state = "idle"
				check(npc.animation_state() == "swim","Paused crew keeps horizontal pose in narrow passage")
				horizontal_holds += 1
				npc.state = previous_state
			if native and cross_room and (absf(npc.foot.y-(center.y+192)) if south else absf(npc.foot.x-(center.x+192))) < 60:
				game.visual_time_seconds += 0.1
				game._update_test_walker(0.0)
				game.grid_view.queue_redraw()
				for frame in range(2): await process_frame
				await RenderingServer.frame_post_draw
				var screenshot := root.get_texture().get_image()
				var cell_size: float = game.get_cell_size()
				var pair_rect := Rect2(Vector2(origin)*cell_size,(Vector2(1,2) if south else Vector2(2,1))*cell_size)
				var screen: Rect2 = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*pair_rect
				var crop := screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
				var capture_path := capture_dir.path_join("%s-%03d.png" % [npc.get_script().resource_path.get_file().get_basename(),tick])
				crop.save_png(capture_path)
				captures.append(capture_path)
		var arrived: bool = npc.foot.distance_to(npc.graph.get_point_position(target)) < 0.01
		check(arrived,"Crew completes furnished station swim route")
		if cross_room:
			if not south: check(horizontal_holds > 0,"Fixture exercises a passage too narrow for treading")
			check(npc.animation_state() == "tread","Crew resumes treading in clear destination space")
		results.append({"actor":npc.get_script().resource_path,"graphNodes":npc.graph.get_point_count(),"searchMs":elapsed,"routePoints":route.size(),"arrived":arrived,"horizontalHoldSamples":horizontal_holds})
	var evidence_name := "cross-room-route-evidence.json" if "--cross-room" in OS.get_cmdline_user_args() else "station-route-evidence.json"
	if south: evidence_name = ("north-" if north else "south-") + evidence_name
	if west: evidence_name = "west-" + evidence_name
	var report := FileAccess.open("res://character/crew-underwater-v1/revisions/"+evidence_name,FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"One equipped route per actor on a five-room station graph; crossRoom identifies the destination variant; not exterior or concurrent traffic", "crossRoom":"--cross-room" in OS.get_cmdline_user_args(), "results":results,"failures":failures,"captures":captures},"\t"))
	report.close()
	game.free()
	for suffix in [".json",".loop",".cfg"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("CREW WATER STATION: ","PASS" if failures == 0 else "FAIL")
	quit(0 if failures == 0 else 1)
