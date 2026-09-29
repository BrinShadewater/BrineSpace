extends SceneTree
## Alien sea life (spec 2026-09-29-lighting-atmosphere-design.md): a drifter shows up in the water at Medium
## and High, and nothing is drawn at Low or under Reduced Motion. Native lane (reads the rendered frame).
const Life = preload("res://scripts/ocean_life.gd")
const TitleSettings = preload("res://scripts/title_settings.gd")
var failures := 0
func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func _initialize() -> void: call_deferred("run")

func region_difference(a: Image, b: Image, centre: Vector2, half: int) -> float:
	var total := 0.0
	var count := 0
	for y in range(maxi(0, int(centre.y) - half), mini(a.get_height(), int(centre.y) + half)):
		for x in range(maxi(0, int(centre.x) - half), mini(a.get_width(), int(centre.x) + half)):
			var ca := a.get_pixel(x, y)
			var cb := b.get_pixel(x, y)
			total += absf(ca.r - cb.r) + absf(ca.g - cb.g) + absf(ca.b - cb.b)
			count += 1
	return total / float(maxi(1, count))

func run() -> void:
	TitleSettings.save_path = "user://ocean_life_%d.cfg" % OS.get_process_id()
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://ocean_life_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://ocean_life_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	root.size = Vector2i(1600, 900)
	game.tick_timer.stop()
	game._set_paused(true, false)
	game.testing_free_build = true
	game._place_room("hydroponics_bay", Vector2i(21, 19), true)
	game._refresh_all()
	game._set_grid_zoom(game.MAX_GRID_ZOOM * 0.5)
	var size: float = game.get_cell_size()
	# Where drifter slot 1 is at t = 20 s, from the same formulas the drawing uses.
	var centre: Vector2 = Life.station_centre(game)
	var e: Vector3 = Life._epoch(20.0, 1, Life.DRIFTER_EPOCH)
	var seed: float = e.x * 3.1 + e.z * 17.0
	var base := centre + Vector2((Life._h(seed, 1.0, 0.0) - 0.5) * 36.0, (Life._h(seed, 2.0, 0.0) - 0.5) * 26.0)
	var drift := Vector2((Life._h(seed, 3.0, 0.0) - 0.5) * 3.0, -1.4 - Life._h(seed, 4.0, 0.0) * 2.0)
	var target := (base + drift * (e.y - 0.5)) * size
	game.visual_time_seconds = 20.0
	var shots := {}
	# Same settings each time; only the life is switched on or off, so the difference is the creatures.
	for mode in ["warm", "life_on", "life_off", "still_on", "still_off"]:
		Life.enabled = mode in ["warm", "life_on", "still_on"]
		TitleSettings.effects_quality = 1
		TitleSettings.reduced_motion = mode.begins_with("still")
		game.grid_scroll.scroll_horizontal = int(target.x - game.grid_scroll.size.x * 0.5)
		game.grid_scroll.scroll_vertical = int(target.y - game.grid_scroll.size.y * 0.5)
		for i in 40: await process_frame
		game.grid_view.queue_redraw()
		await create_timer(0.5).timeout
		await RenderingServer.frame_post_draw
		shots[mode] = root.get_texture().get_image()
	Life.enabled = true
	var k: Vector2 = Vector2(shots.life_on.get_size()) / root.get_visible_rect().size
	var spot: Vector2 = (game.grid_scroll.global_position + game.grid_scroll.size * 0.5) * k
	var half := int(size * 0.5 * k.x)
	var visible_difference := region_difference(shots.life_off, shots.life_on, spot, half)
	var still_difference := region_difference(shots.still_off, shots.still_on, spot, half)
	expect(visible_difference > 0.005, "A drifter is drawn at Medium (difference %.4f)" % visible_difference)
	expect(still_difference < 0.0005, "Reduced Motion draws no sea life (difference %.4f)" % still_difference)
	print("OCEAN LIFE: ", "PASS" if failures == 0 else "FAIL", " failures=", failures)
	quit(1 if failures > 0 else 0)
