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
	root.get_texture().get_image().save_png("res://output/env-parity-%s-cached.png" % label)
	mode(false)
	await settle()
	root.get_texture().get_image().save_png("res://output/env-parity-%s-direct.png" % label)
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
	for frame in range(12):
		game.visual_time_seconds += 0.1
		game.grid_view.queue_redraw()
		await settle()
	if Vector2i(game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds) != stable:
		failures += 1
		push_error("Retained environment rebuilt while only animation time advanced")
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
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.8)
	game.visual_time_seconds = 4.25
	await changed_state("zoom")
	print("ENVIRONMENT PARITY CAPTURE %s: rebuild counters below=%d foundations=%d" % ["PASS" if failures==0 else "FAIL",game.grid_view.env_below_rebuilds,game.grid_view.env_foundation_rebuilds])
	game.queue_free()
	await process_frame
	quit(failures)
