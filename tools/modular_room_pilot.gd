extends SceneTree
## Isolated renderer experiment. Never loads main.gd, meta_state or player saves.
const PilotCanvas = preload("res://rooms/modular/nursery_view.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")
var canvas: PilotCanvas
var capture_dir := ""
var test_only := false
var require_directional_art := false
var viewport_size := Vector2i(1440, 1000)

func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg == "--test":
			test_only = true
		if arg == "--require-directional-art":
			require_directional_art = true
		if arg.begins_with("--viewport="):
			var dimensions := arg.trim_prefix("--viewport=").split("x")
			if dimensions.size() == 2 and dimensions[0].is_valid_int() and dimensions[1].is_valid_int():
				viewport_size = Vector2i(int(dimensions[0]), int(dimensions[1]))
		if arg.begins_with("--capture-dir="):
			capture_dir = arg.trim_prefix("--capture-dir=")
	call_deferred("start")

func start() -> void:
	var recipe_errors := Geometry.recipe_errors(Geometry.recipe)
	if not recipe_errors.is_empty():
		push_error("ROOM RECIPE INVALID: " + str(recipe_errors))
		quit(1)
		return
	if not verify_geometry():
		quit(1)
		return
	if test_only and not require_directional_art:
		quit(0)
		return
	root.content_scale_size = Vector2i.ZERO
	root.size = viewport_size
	root.title = "BRINE / Modular room laboratory"
	canvas = PilotCanvas.new()
	root.add_child(canvas)
	if require_directional_art:
		var missing: Array[int] = []
		for q in range(4):
			if not canvas.asset_supports("microscope_%d" % q, q):
				missing.append(q)
		if not missing.is_empty():
			push_error("DIRECTIONAL ART INCOMPLETE: microscope missing views %s; geometry pass is not art acceptance" % str(missing))
			quit(2)
			return
		print("DIRECTIONAL COVERAGE PASS: four microscope textures present; visual acceptance remains separate")
		if test_only:
			quit(0)
			return
	if not capture_dir.is_empty():
		if not verify_runtime():
			quit(1)
			return
		if DirAccess.dir_exists_absolute(capture_dir):
			push_error("Capture destination must be new; existing evidence is preserved.")
			quit(1)
			return
		DirAccess.make_dir_recursive_absolute(capture_dir)
		if not await verify_continuous_routes():
			quit(1)
			return
		if not await verify_actor_frames():
			quit(1)
			return
		canvas.operating = true
		canvas.focus_art = false
		canvas.rack_board = true
		canvas.paused = true
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var active_a := root.get_texture().get_image()
		active_a.save_png(capture_dir.path_join("layered-directions.png"))
		canvas.phase += 0.45
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var active_b := root.get_texture().get_image()
		active_b.save_png(capture_dir.path_join("layered-motion-b.png"))
		if active_a.get_data() == active_b.get_data():
			push_error("Layered operation frames did not change")
			quit(1)
			return
		canvas.operating = false
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var offline := root.get_texture().get_image()
		offline.save_png(capture_dir.path_join("layered-offline.png"))
		canvas.phase += 0.45
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		if offline.get_data() != root.get_texture().get_image().get_data():
			push_error("Offline layered rack still animated")
			quit(1)
			return
		print("LAYER PASS: four-view board, active pixels change, offline pixels frozen")
		canvas.operating = true
		canvas.paused = false
		canvas.rack_board = false
		for q in range(4):
			canvas.quarter = q
			canvas.rebuild()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(capture_dir.path_join("rotation-%d.png" % q))
			canvas.focus_art = true
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(capture_dir.path_join("layered-detail-%d.png" % q))
			canvas.focus_art = false
		canvas.quarter = 0
		canvas.rebuild()
		canvas.focus_art = true
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(capture_dir.path_join("art-detail.png"))
		canvas.paused = true
		for running in [true, false]:
			canvas.operating = running
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var first_room := root.get_texture().get_image()
			first_room.save_png(capture_dir.path_join("room-active-a.png" if running else "room-offline-a.png"))
			canvas.phase += 0.65
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var second_room := root.get_texture().get_image()
			second_room.save_png(capture_dir.path_join("room-active-b.png" if running else "room-offline-b.png"))
			if (first_room.get_data() != second_room.get_data()) != running:
				push_error("Whole room operation pixel check failed")
				quit(1)
				return
		print("ROOM PASS: whole-room active pixels change, offline pixels identical")
		canvas.operating = true
		canvas.paused = false
		canvas.focus_art = false
		if not await verify_prop_views():
			quit(1)
			return
		canvas.quarter = 0
		canvas.rebuild()
		var prop: Dictionary = canvas.furnishings[0]
		for behind in [true, false]:
			canvas.actor = Vector2(prop.rect.get_center().x, prop.rect.position.y - 9 if behind else prop.rect.end.y + 9)
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(capture_dir.path_join("depth-behind.png" if behind else "depth-front.png"))
		canvas.paused = true
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var frozen := root.get_texture().get_image()
		frozen.save_png(capture_dir.path_join("paused-a.png"))
		for unused in range(5):
			await process_frame
		await RenderingServer.frame_post_draw
		var frozen_again := root.get_texture().get_image()
		frozen_again.save_png(capture_dir.path_join("paused-b.png"))
		if frozen.get_data() != frozen_again.get_data():
			push_error("Paused native frames changed")
			quit(1)
			return
		print("CAPTURE PASS: four rotations, two depth views and identical paused frames; " + capture_dir)
		quit(0)

func set_route_key(code: Key, pressed: bool) -> void:
	var event := InputEventKey.new()
	event.keycode = code
	event.physical_keycode = code
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()

func verify_continuous_routes() -> bool:
	canvas.set_process(false)
	canvas.paused = false
	canvas.operating = false
	canvas.focus_art = true
	var steps := 0
	var routes := 0
	for q in range(4):
		canvas.quarter = q
		canvas.rebuild()
		for prop in canvas.furnishings:
			if prop.room != 0:
				continue
			var route: Rect2 = prop.rect.grow(12)
			var points := [route.position, Vector2(route.end.x, route.position.y), route.end, Vector2(route.position.x, route.end.y), route.position]
			canvas.actor = points[0]
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var tile := Vector2i(ceil(160 * canvas.world_scale), ceil(230 * canvas.world_scale))
			var board := Image.create_empty(tile.x * 4, tile.y * 2, false, Image.FORMAT_RGBA8)
			board.fill(Color("10191f"))
			for segment in range(4):
				var target: Vector2 = points[segment + 1]
				var offset: Vector2 = target - canvas.actor
				var code: Key = KEY_D if offset.x > 0.1 else (KEY_A if offset.x < -0.1 else (KEY_S if offset.y > 0 else KEY_W))
				set_route_key(code, true)
				var initial_distance := canvas.actor.distance_to(target)
				var midpoint_saved := false
				var segment_steps := 0
				while canvas.actor.distance_to(target) > 0.01:
					canvas._process(minf(0.025, canvas.actor.distance_to(target) / 130.0))
					steps += 1
					segment_steps += 1
					if not Geometry.can_stand(canvas.actor, canvas.layout, canvas.furnishings, canvas.structure) or segment_steps > 100:
						set_route_key(code, false)
						push_error("Perimeter route blocked: %s q%d segment%d" % [prop.kind, q, segment])
						return false
					var remaining := canvas.actor.distance_to(target)
					if (not midpoint_saved and remaining <= initial_distance * 0.5) or remaining <= 0.01:
						canvas.queue_redraw()
						await process_frame
						await RenderingServer.frame_post_draw
						var frame := root.get_texture().get_image()
						var requested := Rect2i(canvas.origin + (prop.rect.get_center() - Vector2(80, 140)) * canvas.world_scale, tile)
						var clipped := requested.intersection(Rect2i(Vector2i.ZERO, frame.get_size()))
						var row := 0 if remaining > 0.01 else 1
						board.blit_rect(frame, clipped, Vector2i(segment * tile.x, row * tile.y) + clipped.position - requested.position)
						midpoint_saved = true
				set_route_key(code, false)
			board.save_png(capture_dir.path_join("walk-review-%s-q%d.png" % [prop.kind, q]))
			routes += 1
	canvas.quarter = 0
	canvas.rebuild()
	canvas.set_process(true)
	print("CONTINUOUS ROUTE PASS: %d input-driven prop circuits, %d collision-checked movement steps" % [routes, steps])
	return true

func verify_actor_frames() -> bool:
	canvas.focus_art = true
	canvas.paused = true
	canvas.operating = false
	canvas.actor = Vector2.ZERO
	canvas.actor_walking = true
	for direction in ["east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east"]:
		canvas.actor_direction = direction
		canvas.actor_clock = 0
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var area := Rect2i(canvas.origin + Vector2(-35, -52) * canvas.world_scale, Vector2(70, 72) * canvas.world_scale)
		var first := root.get_texture().get_image().get_region(area)
		canvas.actor_clock = 0.2
		canvas.queue_redraw()
		await process_frame
		await RenderingServer.frame_post_draw
		var second := root.get_texture().get_image().get_region(area)
		if first.get_data() == second.get_data():
			push_error("Walking frames failed to change: " + direction)
			return false
		first.save_png(capture_dir.path_join("actor-%s-a.png" % direction))
		second.save_png(capture_dir.path_join("actor-%s-b.png" % direction))
	canvas.actor_walking = false
	canvas.actor_direction = "south"
	print("ACTOR PIXEL PASS: all eight walking directions animate at fixed foot registration")
	return true

func verify_prop_views() -> bool:
	canvas.paused = true
	canvas.focus_art = true
	var motion_checks := 0
	for q in range(4):
		canvas.quarter = q
		canvas.rebuild()
		canvas.actor = Vector2.ZERO
		for running in [true, false]:
			canvas.operating = running
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var first := root.get_texture().get_image()
			canvas.phase += 0.65
			canvas.queue_redraw()
			await process_frame
			await RenderingServer.frame_post_draw
			var second := root.get_texture().get_image()
			for prop in canvas.furnishings:
				if prop.room != 0:
					continue
				var area: Rect2 = prop.rect.grow(12)
				area.position.y -= 70
				area.size.y += 70
				var pixels := Rect2i(canvas.origin + area.position * canvas.world_scale, area.size * canvas.world_scale)
				pixels = pixels.intersection(Rect2i(Vector2i.ZERO, first.get_size()))
				var changed := first.get_region(pixels).get_data() != second.get_region(pixels).get_data()
				if changed != running:
					push_error("Per-prop motion mismatch: %s rotation %d operating %s" % [prop.kind, q, running])
					return false
				motion_checks += 1
				first.get_region(pixels).save_png(capture_dir.path_join("prop-%s-q%d-%s-a.png" % [prop.kind, q, "active" if running else "offline"]))
				second.get_region(pixels).save_png(capture_dir.path_join("prop-%s-q%d-%s-b.png" % [prop.kind, q, "active" if running else "offline"]))
		canvas.operating = false
		var tile_size := Vector2i(ceil(150 * canvas.world_scale), ceil(230 * canvas.world_scale))
		var depth_board := Image.create_empty(tile_size.x * 4, tile_size.y * 2, false, Image.FORMAT_RGBA8)
		depth_board.fill(Color("10191f"))
		var prop_index := 0
		for prop in canvas.furnishings:
			if prop.room != 0:
				continue
			for behind in [true, false]:
				canvas.actor = Vector2(prop.rect.get_center().x, prop.rect.position.y - 9 if behind else prop.rect.end.y + 9)
				canvas.queue_redraw()
				await process_frame
				await RenderingServer.frame_post_draw
				var depth_frame := root.get_texture().get_image()
				depth_frame.save_png(capture_dir.path_join("depth-%s-q%d-%s.png" % [prop.kind, q, "behind" if behind else "front"]))
				var review_origin: Vector2 = canvas.origin + (prop.rect.get_center() - Vector2(75, 140)) * canvas.world_scale
				var requested := Rect2i(review_origin, tile_size)
				var clipped := requested.intersection(Rect2i(Vector2i.ZERO, depth_frame.get_size()))
				depth_board.blit_rect(depth_frame, clipped, Vector2i(prop_index * tile_size.x, 0 if behind else tile_size.y) + clipped.position - requested.position)
			prop_index += 1
		depth_board.save_png(capture_dir.path_join("depth-review-q%d.png" % q))
	canvas.focus_art = false
	canvas.operating = true
	print("PROP MOTION PASS: %d per-machine active/offline comparisons across four rotations; 32 depth review captures" % motion_checks)
	return true

func verify_runtime() -> bool:
	# Exercise the actual input/movement path, not only sampled geometry.
	var crossing_keys: Array[Key] = [KEY_S, KEY_A, KEY_W, KEY_D]
	for q in range(4):
		canvas.quarter = q
		canvas.rebuild()
		set_route_key(crossing_keys[q], true)
		for unused in range(120):
			canvas._process(0.025)
		set_route_key(crossing_keys[q], false)
		var expected := Geometry.turn(Vector2(0, 390), q)
		if canvas.actor.distance_to(expected) > 1.0:
			push_error("Input-driven doorway crossing failed at q%d: %s" % [q, canvas.actor])
			return false
	var previous: Vector2 = canvas.actor
	var previous_phase: float = canvas.phase
	var previous_actor_clock: float = canvas.actor_clock
	canvas.paused = true
	canvas._process(0.025)
	if canvas.actor != previous or canvas.phase != previous_phase or canvas.actor_clock != previous_actor_clock:
		return false
	canvas.paused = false
	canvas.operating = false
	canvas._process(0.025)
	if canvas.phase != previous_phase or canvas.actor_clock <= previous_actor_clock:
		return false
	canvas.operating = true
	canvas._process(0.025)
	if canvas.phase <= previous_phase:
		return false
	canvas.quarter = 0
	canvas.rebuild()
	print("RUNTIME PASS: four input-driven doorway crossings, pause, offline stop, operating resume")
	return true

func verify_geometry() -> bool:
	var checks := 0
	for q in range(4):
		var layout := Geometry.rooms(q)
		var structure := Geometry.edges(layout)
		var furnishings := Geometry.props(layout)
		if structure.size() != 7:
			push_error("Expected seven unique edges for two adjacent cells")
			return false
		var shared := 0
		for edge in structure:
			if edge.shared:
				shared += 1
				if not edge.open or Geometry.wall_rects(edge).size() != 2:
					return false
		if shared != 1:
			return false
		# Walk a radius-aware character along the entire connected centerline.
		for step in range(385):
			if not Geometry.can_stand(Geometry.turn(Vector2(0, step), q), layout, furnishings, structure):
				push_error("Centerline blocked at rotation %d step %d" % [q, step])
				return false
			checks += 1
		var seam := Geometry.turn(Vector2(0, Geometry.CELL * 0.5), q)
		for edge in structure:
			if edge.open:
				var aperture := Rect2(edge.center - Vector2(Geometry.OPENING * 0.5, Geometry.WALL * 0.5), Vector2(Geometry.OPENING, Geometry.WALL))
				if not edge.horizontal:
					aperture = Rect2(edge.center - Vector2(Geometry.WALL * 0.5, Geometry.OPENING * 0.5), Vector2(Geometry.WALL, Geometry.OPENING))
				for jamb in Geometry.jamb_rects(edge):
					if jamb.intersects(aperture):
						push_error("Artwork jamb intrudes into clear opening")
						return false
		var lateral := Geometry.turn(Vector2.RIGHT, q)
		for sign_value in [-1, 1]:
			if not Geometry.can_stand(seam + lateral * 40 * sign_value, layout, furnishings, structure):
				return false
			if Geometry.can_stand(seam + lateral * 43 * sign_value, layout, furnishings, structure):
				push_error("Door jamb collision missing")
				return false
		for prop in furnishings:
			if Geometry.can_stand(prop.rect.get_center(), layout, furnishings, structure):
				return false
		var broken := Geometry.rooms(q, [0, 1])
		if Geometry.can_stand(seam, broken, Geometry.props(broken), Geometry.edges(broken)):
			push_error("Nonmatching door masks must close seam")
			return false
	print("GEOMETRY PASS: %d passage samples, all rotations, unique seams, jambs, furniture collision, mismatched-port closure" % checks)
	return true
