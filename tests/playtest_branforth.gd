extends "res://tests/playtest_nursery_art.gd"
const NPC = preload("res://scripts/bill_npc.gd")

func walk_room_pixels(cell: Vector2i) -> Image:
	var cell_size: float=game.get_cell_size()
	# A crew head can extend above its foot's room; retain nearby floor context.
	var local_rect:=Rect2(Vector2(cell)*cell_size,Vector2.ONE*cell_size).grow(90.0)
	var screen_rect: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*local_rect
	var frame:=root.get_texture().get_image()
	return frame.get_region(Rect2i(screen_rect.intersection(Rect2(Vector2.ZERO,frame.get_size()))))

func run() -> void:
	capture_dir = "res://output/crew-replacement-2026-09-12/branforth/live-walk-review"
	var equipped_review: bool="helmet-review" in OS.get_cmdline_user_args()
	if equipped_review:capture_dir+="-helmet"
	var walk_direction: String="east"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("walk-direction="):walk_direction=arg.trim_prefix("walk-direction=")
	capture_dir+="-"+walk_direction
	capture_dir+="-padded"
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("review-revision="):
			var revision:=arg.trim_prefix("review-revision=")
			expect(revision.is_valid_int() and int(revision)>0,"Review revision must be a positive integer")
			capture_dir+="-revision-"+str(int(revision))
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.Preferences.save_path = "user://branforth_visual_settings_%d.cfg" % OS.get_process_id()
	game.meta.save_path = "user://branforth_visual_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://branforth_visual_run_%d.json" % OS.get_process_id()
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
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	game._place_room("maintenance_bay", origin, true)
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		game._place_room("storage_bay", origin + offset, true)
	for cell in game.occupied: game.powered_room_cells[cell] = true
	game.test_walker_cell = origin
	game.bill_npc = NPC.new()
	game.rng.seed = 2231
	game.branforth_npc.decision_rng.seed = 9912
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1, -1)
	game._refresh_all()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	game.architect_run = {"selected":"bill"}
	game.recovered_crew = [{"architect_id":"bill","alive":true,"id":"core_architect","name":game.Architects.NAMES.bill,"origin":game.Architects.CORE_CELL},{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":game.Architects.NAMES.branforth,"origin":game.Architects.CORE_CELL}]
	var spawn_actors := [game.bill_npc, game.branforth_npc]
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
	game.branforth_npc.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":95.0}
	if equipped_review:expect(game.branforth_npc.set_helmet_equipped(true),"Fixture equips Branforth helmet")
	game.branforth_npc.choose_goal(game)
	game._update_test_walker(0.1)
	await capture("crew-together")
	room_pixels(origin).save_png(capture_dir.path_join("crew-together-crop.png"))
	var captured := {}
	var walk_review:=true
	var walk_sequence: Array=[]
	var walk_started:=false
	var walk_finished:=false
	var walk_episode_start:=0
	var walk_episode:=0
	for i in range(3600):
		game.visual_time_seconds += 0.1
		game._update_test_walker(0.1)
		var npc = game.branforth_npc
		if walk_review and not walk_finished:
			if not walk_started and npc.state=="walk" and npc.direction==walk_direction and npc.cell_at(npc.foot)==origin:
				walk_started=true
				walk_episode_start=walk_sequence.size()
				walk_episode+=1
			if walk_started:
				game.grid_view.queue_redraw()
				await settle()
				var walk_file: String="walk-sequence-%03d.png"%walk_sequence.size()
				expect(walk_room_pixels(origin).save_png(capture_dir.path_join(walk_file))==OK,"Save live walk sample")
				walk_sequence.append({"file":walk_file,"episode":walk_episode,"time":game.visual_time_seconds,"state":npc.state,"direction":npc.direction,"foot":[npc.foot.x,npc.foot.y],"helmet":npc.helmet_equipped})
				if walk_sequence.size()%20==0:print("WALK CAPTURE PROGRESS: ",walk_direction," episode=",walk_episode," samples=",walk_sequence.size()," state=",npc.state," direction=",npc.direction)
				if npc.state!="walk" or npc.direction!=walk_direction or npc.cell_at(npc.foot)!=origin:
					# Preserve brief path-facing adjustments as evidence, then keep
					# observing until a reviewable continuous segment occurs.
					walk_finished=walk_sequence.size()-walk_episode_start>6
					walk_started=false

		if npc.cell_at(npc.foot) != origin and npc.state != "interact": continue
		var local: Vector2 = npc.foot - (Vector2(origin) + Vector2.ONE * 0.5) * 384
		var key: String = npc.state
		if key == "walk":
			if absf(local.x) < 40 or absf(local.y) < 30: continue
			key += "-" + npc.direction
		if captured.has(key): continue
		# Let each action's first pose advance before capturing it.
		game.grid_view._get_branforth_frame(game)
		await capture(key)
		room_pixels(npc.cell_at(npc.foot)).save_png(capture_dir.path_join(key + "-crop.png"))
		captured[key] = true
	if walk_review:
		var walk_trace:=FileAccess.open(capture_dir.path_join("walk-sequence.json"),FileAccess.WRITE)
		walk_trace.store_string(JSON.stringify(walk_sequence,"\t"));walk_trace.close()
		expect(walk_finished and walk_sequence.size()>6,"Continuous requested walk and exit captured")
		for sample in walk_sequence:expect(sample.helmet==equipped_review,"Equipment retained during walk")
	for required in ["walk-north", "walk-south", "walk-east", "walk-west", "kneel", "repair", "stand", "interact"]:
		expect(captured.has(required), "Native engineer coverage: " + required)
	expect(captured.has("repair"), "Native renderer displays Branforth's autonomous equipment service")
	for save_path in [game.meta.save_path, game.run_save_path, game.Preferences.save_path]:
		if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
	print("BRANFORTH NATIVE: %s; %s" % ["PASS" if failures == 0 else "FAIL", captured.keys()])
	game.free()
	quit(0 if failures == 0 else 1)
