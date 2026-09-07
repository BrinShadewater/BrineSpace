extends "res://tests/playtest_nursery_art.gd"
const NPC = preload("res://scripts/bill_npc.gd")

func run() -> void:
	capture_dir = "res://character/crew-underwater-v1/pilot/native/water-%d" % OS.get_process_id()
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.Preferences.save_path = "user://crew_water_visual_settings_%d.cfg" % OS.get_process_id()
	game.meta.save_path = "user://crew_water_visual_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://crew_water_visual_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.mode = Window.MODE_WINDOWED
	root.borderless = false
	root.size = Vector2i(1600, 900)
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	# Three-crew art fixture bypasses only the architect population setup.
	game.architect_run.clear()
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
	game._update_test_walker(0.1)
	var crew := [game.bill_npc, game.veld_npc, game.branforth_npc]
	if "--swim-revision" in OS.get_cmdline_user_args():
		await review_swim_revision(origin, crew)
		for save_path in [game.meta.save_path, game.run_save_path, game.Preferences.save_path]:
			if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
		print("CREW SWIM REVISION NATIVE: %s" % ("PASS" if failures == 0 else "FAIL"))
		game.free()
		quit(0 if failures == 0 else 1)
		return
	# Exercise full runtime sequences at every authored phase interior.
	for npc in crew:
		npc.path.clear()
		npc.stage = ""
		npc.state = "idle"
		expect(npc.begin_helmet_action(true), "Begin timed donning")
	game.test_walker_state = "equip-helmet"
	game.test_walker_direction = "east"
	var previous_phase := 0.0
	for phase in locker_phase_interiors("equip-helmet"):
		for npc in crew: npc.advance_helmet_action(phase - previous_phase)
		previous_phase = phase
		game.visual_time_seconds = 50.0 + phase
		var before := [game.grid_view._get_human_frame("equip-helmet", "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		verify_locker_sources("equip-helmet", phase, before)
		game.visual_time_seconds += 100.0
		var after := [game.grid_view._get_human_frame("equip-helmet", "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		for index in range(3):
			expect(before[index] != null and before[index] == after[index], "Visual clock cannot advance helmet action")
			expect(before[index].get_size() == Vector2(92,104), "Tall transition size retained")
			expect(not crew[index].helmet_equipped, "Equipment waits for action completion")
		var label := "bill-donning-%04d" % roundi(phase*1000)
		await capture(label)
		room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
	for npc in crew:
		npc.advance_helmet_action(1.0)
		expect(npc.helmet_equipped and npc.state == "idle", "Timed donning completes")
	for npc in crew:
		expect(npc.active, "All three fixture actors are present")
		npc.path.clear()
		npc.direction = "east"
		expect(npc.set_helmet_equipped(true), "Equip for dry action review")
	var action_time := 60.0
	for action in ["idle", "kneel", "repair", "stand", "interact", "idle"]:
		for npc in crew: npc.state = action
		game.test_walker_state = action
		game.test_walker_direction = "east"
		game.visual_time_seconds = action_time
		expect(game.grid_view._get_human_frame(action, "east") != null, "Bill dry action present")
		expect(game.grid_view._get_veld_frame(game) != null, "Veld dry action present")
		expect(game.grid_view._get_branforth_frame(game) != null, "Branforth dry action present")
		for phase in dry_phase_interiors(action):
			game.visual_time_seconds = action_time + phase
			var poses := [game.grid_view._get_human_frame(action, "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
			verify_locker_sources(action, phase, poses, "equipment/dry")
			var label := "helmet-dry-%s-%d-%04d" % [action, int(action_time), roundi(phase*1000)]
			await capture(label)
			room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
		action_time += 2.0
	# Walk is distance-driven: move by the manifest stride fraction, not just time.
	var walk_origins: Array = []
	var walk_cycles: Array = []
	var walk_strides: Array = []
	for actor_index in range(3):
		var actor_name: String = ["major-bill-v2", "dr-veld-v1", "chief-engineer-branforth-v1"][actor_index]
		var source: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/%s/final/manifest.json" % actor_name))
		var total := 0.0
		for clip in source.states:
			if clip.id == "walk-east":
				for duration in clip.frameDurationsMs: total += float(duration) / 1000.0
		walk_cycles.append(total)
		walk_strides.append(float(source.strideDistanceCells.walk))
		walk_origins.append(crew[actor_index].foot)
		crew[actor_index].state = "walk"
	game.test_walker_state = "walk"
	game.visual_time_seconds = action_time
	game.grid_view._get_human_frame("walk", "east")
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	for phase in dry_phase_interiors("walk"):
		for actor_index in range(3):
			var npc = crew[actor_index]
			var target: Vector2 = walk_origins[actor_index] + Vector2.RIGHT * phase / walk_cycles[actor_index] * walk_strides[actor_index] * 384.0
			expect(npc.segment_clear(npc.foot, target), "Sampled dry walk segment remains clear")
			npc.foot = target
		game.visual_time_seconds = action_time + phase
		var poses := [game.grid_view._get_human_frame("walk", "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		verify_locker_sources("walk", phase, poses, "equipment/dry")
		var label := "helmet-dry-walk-%04d" % roundi(phase * 1000)
		await capture(label)
		room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
	var last_walk_phase: float = dry_phase_interiors("walk").back()
	var turn_time := action_time + 2.0
	for facing in ["south", "west", "north", "east"]:
		for npc in crew: npc.direction = facing
		game.test_walker_direction = facing
		game.visual_time_seconds = turn_time
		var turn_poses := [game.grid_view._get_human_frame("walk", facing), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		for actor_index in range(3):
			var actor_id: String = ["bill", "veld", "branforth"][actor_index]
			var expected = preload("res://scripts/crew_sprite_player.gd").new()
			expected.load_manifest("res://character/crew-underwater-v1/equipment/dry/%s-walk-%s/manifest.json" % [actor_id,facing])
			var key: String = "walk-" + facing
			var fraction: float = fmod(last_walk_phase / walk_cycles[actor_index], 1.0)
			var pose: Texture2D = expected.frame_at_elapsed(key, fraction * expected.cycle_seconds(key))
			expect(turn_poses[actor_index].get_image().get_data() == pose.get_image().get_data(), "Native facing turn retains the gait fraction")
		var label: String = "helmet-dry-turn-" + facing
		await capture(label)
		room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
		turn_time += 0.1
	for actor_index in range(3):
		crew[actor_index].foot = walk_origins[actor_index]
		crew[actor_index].direction = "east"
		crew[actor_index].state = "idle"
	var living_snapshots: Array = []
	for npc in crew:
		living_snapshots.append(npc.snapshot())
		npc.die()
	game.test_walker_state = "death-ground"
	game.visual_time_seconds = 75.0
	expect(game.grid_view._get_human_frame("death-ground", "east") != null, "Bill ground helmet death present")
	expect(game.grid_view._get_veld_frame(game) != null, "Veld ground helmet death present")
	expect(game.grid_view._get_branforth_frame(game) != null, "Branforth ground helmet death present")
	for phase in [0.08, 0.4, 0.62, 0.82, 3.0]:
		game.visual_time_seconds = 75.0 + phase
		var label := "helmet-ground-death-%04d" % roundi(phase*1000)
		await capture(label)
		room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
		for npc in crew: expect(npc.dead and npc.path.is_empty(), "Ground death remains terminal")
	for index in range(crew.size()): await crew[index].restore_snapshot(game, living_snapshots[index])
	for npc in crew: expect(npc.begin_helmet_action(false), "Begin timed removal")
	game.test_walker_state = "remove-helmet"
	game.test_walker_direction = "east"
	previous_phase = 0.0
	for phase in locker_phase_interiors("remove-helmet"):
		for npc in crew: npc.advance_helmet_action(phase - previous_phase)
		previous_phase = phase
		var before := [game.grid_view._get_human_frame("remove-helmet", "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		verify_locker_sources("remove-helmet", phase, before)
		game.visual_time_seconds += 100.0
		var after := [game.grid_view._get_human_frame("remove-helmet", "east"), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
		for index in range(3):
			expect(before[index] != null and before[index] == after[index], "Visual clock cannot advance removal")
			expect(crew[index].helmet_equipped, "Removal retains gear until completion")
		var label := "crew-removal-%04d" % roundi(phase * 1000)
		await capture(label)
		room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
	for npc in crew:
		npc.advance_helmet_action(1.0)
		expect(not npc.helmet_equipped and npc.state == "idle", "Timed removal completes before bare water review")
	for npc in crew:
		expect(npc.set_movement_medium("flooded"), "Fixture enters water medium")
		npc.path.clear()
		npc.state = "idle"
		npc.direction = "south"
	# Validate blocked upright behavior before relocating this visual-only sample.
	for npc in crew:
		if npc.swim_segment_clear(npc.foot,npc.foot,"south","south",true): continue
		expect(npc.animation_state() == "swim", "Unsafe upright pose keeps swimmer horizontal")
		var best := Vector2.INF
		var distance := INF
		for node_id in npc.graph.get_point_ids():
			var point: Vector2 = npc.graph.get_point_position(node_id)
			if point.distance_to(npc.foot) >= distance or point.distance_to(npc.foot) > 128.0: continue
			var clear := true
			for facing in ["south","east","north","west"]:
				if not npc.swim_segment_clear(point,point,facing,facing,true): clear = false
			for other in crew:
				if other != npc and point.distance_to(other.foot) < 40.0: clear = false
			if clear:
				best = point
				distance = point.distance_to(npc.foot)
		expect(best != Vector2.INF, "Nearby clear upright review position exists")
		if best != Vector2.INF: npc.foot = best
	game.test_walker_state = game.bill_npc.animation_state()
	game.test_walker_direction = "south"
	game.visual_time_seconds = 90.0
	game.grid_view._get_human_frame("tread", "south")
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	for phase in [0.08,0.4,0.72]:
		game.visual_time_seconds = 90.0 + phase
		await capture("tread-%04d" % roundi(phase*1000))
		room_pixels(origin).save_png(capture_dir.path_join("tread-%04d-crop.png" % roundi(phase*1000)))
		for npc in crew: expect(npc.animation_state() == "tread", "Station selects treading for %s at %s; upright clearance=%s" % [npc.get_script().resource_path, npc.foot, npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,true)])
	for facing in ["east", "north", "west"]:
		for npc in crew: npc.direction = facing
		game.test_walker_direction = facing
		game.visual_time_seconds = 95.0
		game.grid_view._get_human_frame("tread", facing)
		game.grid_view._get_veld_frame(game)
		game.grid_view._get_branforth_frame(game)
		for phase in [0.08, 0.4, 0.72]:
			game.visual_time_seconds = 95.0 + phase
			var label := "tread-%s-%04d" % [facing, roundi(phase*1000)]
			await capture(label)
			room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
	for npc in crew: expect(npc.set_helmet_equipped(true), "Fixture equips NPC helmet")
	for facing in ["south", "east", "north", "west"]:
		for npc in crew: npc.direction = facing
		game.test_walker_direction = facing
		game.visual_time_seconds = 98.0
		expect(game.grid_view._get_human_frame("tread", facing) != null, "Bill equipped frame available")
		expect(game.grid_view._get_veld_frame(game) != null, "Veld equipped frame available")
		expect(game.grid_view._get_branforth_frame(game) != null, "Branforth equipped frame available")
		game.visual_time_seconds = 98.4
		await capture("helmet-tread-" + facing)
		room_pixels(origin).save_png(capture_dir.path_join("helmet-tread-" + facing + "-crop.png"))
	for npc in crew: npc.die()
	game._update_test_walker(0.1)
	game.visual_time_seconds = 100.0
	game.grid_view._get_human_frame("death-water", "east")
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	for phase in [0.0,0.22,0.4,0.6,0.8,1.1,3.0]:
		game.visual_time_seconds = 100.0 + phase
		await capture("helmet-death-%04d" % roundi(phase*1000))
		room_pixels(origin).save_png(capture_dir.path_join("helmet-death-%04d-crop.png" % roundi(phase*1000)))
		for npc in crew: expect(npc.dead and npc.path.is_empty(), "Native death remains terminal")
	for save_path in [game.meta.save_path, game.run_save_path, game.Preferences.save_path]:
		if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
	print("CREW WATER NATIVE: %s" % ("PASS" if failures == 0 else "FAIL"))
	game.free()
	quit(0 if failures == 0 else 1)

func review_swim_revision(origin: Vector2i, crew: Array) -> void:
	var direction := "north" if "--north" in OS.get_cmdline_user_args() else "south" if "--south" in OS.get_cmdline_user_args() else ("west" if "--west" in OS.get_cmdline_user_args() else "east")
	var clip := "swim-" + direction
	var clearance_samples: Array = []
	capture_dir = "res://character/crew-underwater-v1/revisions/native-" + direction
	DirAccess.make_dir_recursive_absolute(capture_dir)
	var players := []
	for actor in ["bill", "veld", "branforth"]:
		var player = preload("res://scripts/crew_sprite_player.gd").new()
		var version := "v3" if actor == "branforth" and direction == "north" else "v2"
		var base := "res://character/crew-underwater-v1/revisions/%s-swim-%s-%s/" % [actor, direction, version]
		var helmet_path := base + "helmet/manifest.json"
		if direction == "north" and actor == "veld":
			base = "res://character/crew-underwater-v1/pilot/veld-swim-north/"
			helmet_path = "res://character/crew-underwater-v1/equipment/fitting/veld-swim-north/manifest.json"
		player.load_manifest(base + "manifest.json")
		expect(player.load_equipment_manifest("diving-helmet", helmet_path), "Revision equipment matches base timing and pivot")
		players.append(player)
	for npc in crew:
		npc.path.clear()
		npc.stage = ""
		npc.state = "walk"
		npc.direction = direction
		expect(npc.set_movement_medium("flooded"), "Revision fixture selects swimming")
	game.test_walker_state = "swim"
	game.test_walker_direction = direction
	# Fixed-position phase samples prove drawing, not swimming navigation.
	game.visual_time_seconds = 10.0
	game.grid_view._get_human_frame("swim", direction)
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	for equipped in [false, true]:
		for npc in crew: expect(npc.set_helmet_equipped(equipped), "Revision helmet toggle")
		for index in range(6):
			var phase := float(index) * 0.16 + 0.08
			game.grid_view.human_animation_phase = phase
			game.grid_view.veld_player.phase = phase
			game.grid_view.branforth_player.phase = phase
			var actual := [game.grid_view._get_human_frame("swim", direction), game.grid_view._get_veld_frame(game), game.grid_view._get_branforth_frame(game)]
			for actor_index in range(3):
				var expected = players[actor_index].equipment_frames["diving-helmet"][clip][index] if equipped else players[actor_index].frames[clip][index]
				expect(actual[actor_index].get_image().get_data() == expected.get_image().get_data(), "Normal runtime loader selects exact revision phase")
				expect(actual[actor_index].get_size() == expected.get_size() and actual[actor_index].get_meta("crew_pivot") == expected.get_meta("crew_pivot"), "Source frame dimensions and shoulder pivot retained")
			for actor_index in range(3):
				var npc = crew[actor_index]
				var texture: Texture2D = actual[actor_index]
				var image := texture.get_image()
				var pixel_scale := 65.28 / 74.0
				var pivot: Vector2 = texture.get_meta("crew_pivot")
				var overlaps: Array = []
				for cell in npc.geometry:
					var center := (Vector2(cell) + Vector2.ONE * 0.5) * 384.0
					for prop in npc.geometry[cell].get("props", []):
						var rect: Rect2 = Rect2(prop.rect.position + center, prop.rect.size)
						var count := 0
						for y in range(image.get_height()):
							for x in range(image.get_width()):
								if image.get_pixel(x,y).a == 0.0: continue
								var pixel := Rect2(npc.foot + (Vector2(x,y)-pivot)*pixel_scale, Vector2.ONE*pixel_scale)
								if pixel.intersects(rect): count += 1
						if count > 0: overlaps.append({"prop":prop.get("id", "unnamed"), "cell":[cell.x,cell.y], "opaquePixels":count})
				clearance_samples.append({"actor":["bill","veld","branforth"][actor_index],"phase":index+1,"helmet":equipped,"foot":[npc.foot.x,npc.foot.y],"propOverlaps":overlaps})
			var label := "%s-phase-%d" % ["helmet" if equipped else "bare", index + 1]
			await capture(label)
			room_pixels(origin).save_png(capture_dir.path_join(label + "-crop.png"))
	var report := FileAccess.open(capture_dir.path_join("prop-clearance.json"), FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Opaque sprite pixels against authored prop rectangles at fixed fixture positions; excludes walls, route sweeps and depth occlusion", "samples":clearance_samples}, "\t"))
	report.close()

func locker_phase_interiors(action: String) -> Array:
	var reference: Array = []
	for actor in ["bill", "veld", "branforth"]:
		var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://character/crew-underwater-v1/locker/%s-%s-east/manifest.json" % [actor, action]))
		var durations: Array = manifest.states[0].frameDurationsMs
		if reference.is_empty(): reference = durations
		else: expect(durations == reference, "Shared locker capture clock matches every actor")
	var phases: Array = []
	var elapsed := 0.0
	for duration in reference:
		phases.append(elapsed + float(duration) / 2000.0)
		elapsed += float(duration) / 1000.0
	return phases

func verify_locker_sources(action: String, elapsed: float, textures: Array, pack_root := "locker") -> void:
	for actor_index in range(3):
		var actor: String = ["bill", "veld", "branforth"][actor_index]
		var path := "res://character/crew-underwater-v1/%s/%s-%s-east/manifest.json" % [pack_root, actor, action]
		var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
		var clip: Dictionary = manifest.states[0]
		var cursor := elapsed
		if clip.loop:
			var total := 0.0
			for duration in clip.frameDurationsMs: total += float(duration) / 1000.0
			cursor = fmod(cursor, total)
		var selected: int = clip.frameFiles.size() - 1
		for index in range(clip.frameFiles.size()):
			var duration: float = float(clip.frameDurationsMs[index]) / 1000.0
			if cursor < duration:
				selected = index
				break
			cursor -= duration
		var source := Image.new()
		var file: String = path.get_base_dir().path_join(clip.frameFiles[selected]).simplify_path()
		expect(source.load_png_from_buffer(FileAccess.get_file_as_bytes(file)) == OK, "Locker source frame loads")
		var texture: Texture2D = textures[actor_index]
		expect(texture != null, "Locker native texture exists")
		if texture != null:
			expect(texture.get_image().get_data() == source.get_data(), "%s %s phase %d uses current source pixels" % [actor, action, selected])
			expect(texture.get_meta("crew_pivot") == Vector2(manifest.pivot[0],manifest.pivot[1]), "Native pivot matches selected source")

func dry_phase_interiors(action: String) -> Array:
	var phases: Array = []
	for actor in ["bill", "veld", "branforth"]:
		var path := "res://character/crew-underwater-v1/equipment/dry/%s-%s-east/manifest.json" % [actor, action]
		var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
		var elapsed := 0.0
		for duration in manifest.states[0].frameDurationsMs:
			var phase: float = elapsed + float(duration) / 2000.0
			if not phases.has(phase): phases.append(phase)
			elapsed += float(duration) / 1000.0
	# Different role actions may have different timing; sample the union.
	phases.sort()
	return phases
