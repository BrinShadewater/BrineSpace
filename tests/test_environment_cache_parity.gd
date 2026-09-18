extends SceneTree
## Retained environment passes (stars/haze rects/foundations) must render the
## same pixels as the direct single-pass path, and must invalidate on the state
## their keys watch. Clone of the surface-cache parity pattern; native only.
var game
var failures := 0
func _init() -> void: call_deferred("run")
func settle() -> void:
	for frame in range(6): await process_frame
	await RenderingServer.frame_post_draw
func mode(cached: bool) -> void:
	game.grid_view.retain_environment = cached
	game.grid_view.queue_redraw()
func changed_state(label: String, expect_foundations := true) -> void:
	var before := Vector2i(game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds)
	game.grid_view.queue_redraw()
	await RenderingServer.frame_post_draw
	var after := Vector2i(game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds)
	if expect_foundations and after.y <= before.y:
		failures += 1
		push_error("Foundations did not invalidate in the next rendered frame: " + label)
	await settle()
	var cached_image := root.get_texture().get_image()
	cached_image.save_png("res://output/env-parity-%s-cached.png" % label)
	mode(false)
	await settle()
	var direct_image := root.get_texture().get_image()
	direct_image.save_png("res://output/env-parity-%s-direct.png" % label)
	if cached_image.get_data() != direct_image.get_data():
		failures += 1
		push_error("Retained environment pixels differ from the direct path: " + label)
	mode(true)
	await settle()
func run() -> void:
	preload("res://scripts/title_settings.gd").save_path = "user://env_parity.cfg"
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://env_parity.meta"
	game.run_save_path = "user://env_parity.loop"
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600,900)
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.set_process(false)
	game.tick_timer.stop()
	game.hardware_panel.set_process(false) # The WALLS knob eases between captures otherwise.
	game.selected_card_id = ""
	var index := 0
	for id in ["storage_bay","corridor","reactor","galley","hydroponics_bay","cold_store"]:
		game._place_room(id,Vector2i(18+index%3,19+index/3),true)
		index += 1
	game.Architects.advance_core(game,10.0)
	game._set_paused(true,false)
	game._refresh_all()
	await settle()
	game._fit_station_view()
	await settle()
	game._center_grid_on_station_now()
	mode(true)
	await settle()
	# Animation time must not rebuild the retained static passes.
	var stable := Vector2i(game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds)
	var stable_terrain: int = game.grid_view.env_terrain_rebuilds
	for frame in range(12):
		game.visual_time_seconds += 0.1
		game.grid_view.queue_redraw()
		await settle()
	if Vector2i(game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds) != stable:
		failures += 1
		push_error("Retained environment rebuilt while only animation time advanced")
	if game.grid_view.env_terrain_rebuilds != stable_terrain:
		failures += 1
		push_error("Retained rocks and wrecks rebuilt while only animation time advanced")
	game.visual_time_seconds = 4.25
	await changed_state("baseline",false)
	game._place_room("crew_hab",Vector2i(21,19),true)
	game.visual_time_seconds = 4.25
	await changed_state("place")
	var removed: Dictionary = game.occupied[Vector2i(21,19)]
	game.placed_rooms.erase(removed)
	game.occupied.erase(Vector2i(21,19))
	game.visual_time_seconds = 4.25
	await changed_state("remove")
	game.hardware.walls = false
	game.visual_time_seconds = 4.25
	await changed_state("walls-off")
	game.hardware.walls = true
	game.visual_time_seconds = 4.25
	await changed_state("walls-on")
	game.grid_scroll.scroll_horizontal += int(game.get_cell_size()*2)
	game.visual_time_seconds = 4.25
	await changed_state("pan",false)
	# A zoom the camera limits actually allow. The closest zoom is three quarters of the default
	# since the owner playtest of September 17, so DEFAULT * 0.8 clamped to exactly the value the
	# reset above had already produced: the camera never moved, nothing invalidated, and every
	# parity capture failed on a step that was doing nothing.
	game._set_grid_zoom(game.MAX_GRID_ZOOM*0.8)
	game.visual_time_seconds = 4.25
	await changed_state("zoom")
	# Rock clearance, selection and removal must invalidate the retained terrain pass.
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.5)
	await settle() # Centre with the applied cell size, not the pre-zoom one.
	game._center_grid_on_station_now()
	await settle()
	var view := Rect2(Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical),game.grid_scroll.size)
	var rock := Vector2i(-1,-1)
	for cell in game.wrecks:
		if game.wrecks[cell].kind == "basalt" and not game.wrecks[cell].cleared and view.has_point((Vector2(cell)+Vector2.ONE*0.5)*game.get_cell_size()):
			rock = cell
			break
	if rock != Vector2i(-1,-1):
		for step in [["rock-selected",func(): game.selected_room_cell = rock],["rock-progress",func(): game.wrecks[rock].progress = 9.0],["rock-cleared",func(): game.wrecks[rock].cleared = true]]:
			var terrain_before: int = game.grid_view.env_terrain_rebuilds
			step[1].call()
			game.visual_time_seconds = 4.25
			await changed_state(step[0],false)
			if game.grid_view.env_terrain_rebuilds <= terrain_before:
				failures += 1
				push_error("Terrain pass did not invalidate: " + step[0])
	# Unpowered derelict wards are retained too; selection and ward state must invalidate them.
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.25)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	view = Rect2(Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical),game.grid_scroll.size)
	var ward_cell := Vector2i(-1,-1)
	var companion_cell := Vector2i(-1,-1)
	for cell in game.wrecks:
		if game.wrecks[cell].cleared or not view.has_point((Vector2(cell)+Vector2.ONE*0.5)*game.get_cell_size()): continue
		if game.wrecks[cell].kind == "cryo" and ward_cell == Vector2i(-1,-1): ward_cell = cell
		if game.Companions.IDS.has(game.wrecks[cell].kind) and companion_cell == Vector2i(-1,-1): companion_cell = cell
	if ward_cell != Vector2i(-1,-1) and companion_cell != Vector2i(-1,-1):
		for step in [["derelict-selected",func(): game.selected_room_cell = ward_cell],["derelict-progress",func(): game.wrecks[ward_cell].progress = 7.0],["companion-opened",func(): game.wrecks[companion_cell].opened = true]]:
			var derelict_before: int = game.grid_view.env_derelict_rebuilds
			step[1].call()
			game.visual_time_seconds = 4.25
			await changed_state(step[0],false)
			if game.grid_view.env_derelict_rebuilds <= derelict_before:
				failures += 1
				push_error("Derelict pass did not invalidate: " + step[0])
	else:
		failures += 1
		push_error("No cryo and companion ward on screen; derelict invalidation was not exercised: cryo=%s companion=%s" % [ward_cell,companion_cell])
	if rock == Vector2i(-1,-1):
		failures += 1
		push_error("No basalt rock is on screen; terrain invalidation was not exercised: view=%s cell_size=%s basalt=%s" % [view,game.get_cell_size(),game.wrecks.keys().filter(func(c): return game.wrecks[c].kind=="basalt" and not game.wrecks[c].cleared).slice(0,6)])
	print("ENVIRONMENT PARITY CAPTURE %s: rebuild counters below=%d foundations=%d" % ["PASS" if failures==0 else "FAIL",game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds])
	game.queue_free()
	await process_frame
	quit(failures)
