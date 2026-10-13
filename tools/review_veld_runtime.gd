extends "res://tests/playtest_nursery_art.gd"
const NPC = preload("res://scripts/bill_npc.gd")

func run() -> void:
	capture_dir = "res://output/veld-runtime-integration/native"
	var equipped_review: bool="helmet-review" in OS.get_cmdline_user_args()
	if equipped_review:capture_dir+="-helmet"
	var review_direction: String="north"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("review-direction="):review_direction=arg.trim_prefix("review-direction=")
	if review_direction!="north":capture_dir+="-"+review_direction
	var walk_review: bool="walk-review" in OS.get_cmdline_user_args()
	var walk_direction: String="east"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("walk-direction="):walk_direction=arg.trim_prefix("walk-direction=")
	if walk_review:capture_dir+="-walk"
	if walk_review and walk_direction!="east":capture_dir+="-"+walk_direction
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.Preferences.save_path = "user://veld_visual_settings_%d.cfg" % OS.get_process_id()
	game.meta.save_path = "user://veld_visual_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://veld_visual_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	# This fixture advances the NPC and visual clock explicitly. Match the shared
	# art harness isolation so desktop input cannot alter the captured scene.
	game.set_process(false)
	game.set_process_input(false)
	game.set_process_unhandled_input(false)
	game.set_process_unhandled_key_input(false)
	root.gui_disable_input=true
	root.mode = Window.MODE_WINDOWED
	root.borderless = false
	root.size = Vector2i(1600, 900)
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	game._place_room("storage_bay", origin, true)
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		game._place_room("storage_bay", origin + offset, true)
	for cell in game.occupied: game.powered_room_cells[cell] = true
	game.test_walker_cell = origin
	game.bill_npc = NPC.new()
	game.rng.seed = 2231
	game.veld_npc.decision_rng.seed = 9912
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1, -1)
	game._refresh_all()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	game.architect_run = {"selected":"bill"}
	game.recovered_crew = [{"architect_id":"bill","alive":true,"id":"core_architect","name":game.Architects.NAMES.bill,"origin":game.Architects.CORE_CELL},{"architect_id":"veld","alive":true,"id":"architect_veld","name":game.Architects.NAMES.veld,"origin":game.Architects.CORE_CELL}]
	var spawn_actors := [game.bill_npc, game.veld_npc]
	var spawn_offsets := [Vector2.ZERO, Vector2(100, 0)]
	for i in range(spawn_actors.size()):
		var actor = spawn_actors[i]
		actor.rebuild(game)
		var want: Vector2 = (Vector2(origin)+Vector2.ONE*0.5)*384.0+spawn_offsets[i]
		var best := -1
		var best_distance := INF
		for point_id in actor.room_nodes.get(origin, []):
			var point: Vector2 = actor.graph.get_point_position(point_id)
			if actor.spawn_clear(point) and actor.can_stand(point) and point.distance_squared_to(want) < best_distance:
				best = point_id
				best_distance = point.distance_squared_to(want)
		expect(best >= 0, "Fixture finds clear floor for architect %d" % i)
		if best >= 0:
			actor.foot = actor.graph.get_point_position(best)
			actor.active = true
	game._update_test_walker(0.1)
	game.veld_npc.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":95.0}
	if equipped_review:expect(game.veld_npc.set_helmet_equipped(true),"Fixture equips Veld helmet")
	var npc = game.veld_npc
	game.bill_npc.active = false
	npc.avoidance_position = Vector2.INF
	npc.avoidance_positions.clear() # Removed peer must not leave cached fixture traffic.
	var trace: Array = []
	for direction in ["east", "west", "north", "south"]:
		var vector: Vector2 = {"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[direction]
		var start := Vector2.INF
		var best_distance := INF
		var desired := (Vector2(origin)+Vector2.ONE*0.5)*384.0-vector*46.0
		for point_id in npc.room_nodes.get(origin, []):
			var point: Vector2 = npc.graph.get_point_position(point_id)
			if point.distance_squared_to(desired)<best_distance and npc.can_stand(point) and npc.can_stand(point+vector*92.0) and npc.segment_clear(point,point+vector*92.0):
				start = point
				best_distance = point.distance_squared_to(desired)
		expect(start.is_finite(),"Clear native route " + direction)
		if not start.is_finite(): continue
		npc.foot = start
		npc.direction = direction
		npc.goal = ""
		npc.path.clear()
		npc.state = "idle"
		for i in range(60):
			if i == 10: npc.path = PackedVector2Array([start+vector*92.0])
			if i >= 10 and i < 50: npc.move(0.05)
			if i >= 50: npc.path.clear(); npc.state = "idle"
			if npc.state == "walk": expect(npc.direction == direction,"Requested cardinal facing")
			game.visual_time_seconds += 0.05
			game.grid_view.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var name := "%s-%03d.png" % [direction,i]
			expect(room_pixels(origin).save_png(capture_dir.path_join(name))==OK,"Native capture")
			trace.append({"file":name,"state":npc.state,"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"time":game.visual_time_seconds})
			if i==25:root.get_texture().get_image().save_png(capture_dir.path_join(direction+"-station.png"))
	var log = FileAccess.open(capture_dir.path_join("trace.json"),FileAccess.WRITE)
	log.store_string(JSON.stringify(trace,"  "))
	print("VELD NATIVE INTEGRATION: ",trace.size()," samples, ",failures," failures")
	quit(1 if failures else 0)
