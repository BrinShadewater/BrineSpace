extends SceneTree
## The camera's two limits and its anchoring, headless: pure scroll arithmetic, no pixels.
##
## Zooming out used to stop only when the whole 40x40 grid fitted the frame - far wider
## than any station and too small to read. And the wheel preserved the view's *centre*,
## which the scroll container clamps at the grid edge, so zooming out far and back in
## returned you to the middle of the map instead of to what you were looking at: measured
## at 5.8 cells of drift over three notches before this was fixed.
const Preferences = preload("res://scripts/title_settings.gd")
var game
var failures := 0

func check(ok: bool, message: String) -> void:
	if ok: return
	failures += 1
	push_error(message)

func frame() -> void:
	await process_frame

func settle_zoom() -> void:
	for i in range(60):
		game._update_camera_zoom(1.0 / 60.0)
		await frame()

## The grid cell currently drawn at `inside` (a position in the grid frame).
func cell_under(inside: Vector2) -> Vector2:
	var at: Vector2 = Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical) + inside
	return at / game.get_cell_size()

func _init() -> void: call_deferred("run")

func run() -> void:
	Preferences.save_path = "user://grid_zoom_%d.cfg" % OS.get_process_id()
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://grid_zoom_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://grid_zoom_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600, 900)
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.set_process(false)
	game.tick_timer.stop()
	game.testing_free_build = true
	for resource in game.resources: game.resources[resource] = 1000
	game._place_room("reactor", Vector2i(20, 20), true)
	game._refresh_all()
	for i in range(6): await frame()

	# 1. The far limit shows ZOOM_OUT_EXTENT of the grid, not all of it.
	var furthest: float = game._minimum_map_zoom()
	var across: float = game.grid_scroll.get_rect().size.x / (game.CELL_SIZE * furthest)
	var wanted: float = game.GRID_SIZE * game.ZOOM_OUT_EXTENT
	check(absf(across - wanted) < 0.5,
		"Furthest zoom shows %.1f of the %d cells across, expected %.1f" % [across, game.GRID_SIZE, wanted])
	check(furthest > game.MIN_GRID_ZOOM,
		"The fitted limit should bind before the absolute floor")

	# 2. The wheel holds the grid point under the pointer, from the far limit inward.
	game._set_grid_zoom(furthest)
	for i in range(6): await frame()
	var probe := Vector2(game.grid_scroll.get_rect().size.x * 0.25, game.grid_scroll.get_rect().size.y * 0.75)
	var before := cell_under(probe)
	for notch in range(3):
		game._request_wheel_zoom(0.05, probe)
		await settle_zoom()
	var after := cell_under(probe)
	check(game.grid_zoom > furthest + 0.0001, "Three notches should have zoomed in")
	check(before.distance_to(after) < 0.25,
		"Wheel zoom must hold the cell under the pointer: %.2f,%.2f became %.2f,%.2f (%.2f cells)" % [
			before.x, before.y, after.x, after.y, before.distance_to(after)])

	# 3. Zooming back out to the limit returns what was under the pointer, not the map's middle.
	for notch in range(3):
		game._request_wheel_zoom(-0.05, probe)
		await settle_zoom()
	var returned := cell_under(probe)
	check(before.distance_to(returned) < 0.75,
		"Zooming back out must return to the same place: %.2f,%.2f became %.2f,%.2f" % [
			before.x, before.y, returned.x, returned.y])

	# 4. A zoom that is not the wheel keeps the view's centre, and never inherits the
	#    pointer from an earlier scroll.
	game._set_grid_zoom(furthest)
	for i in range(6): await frame()
	var centre_before: Vector2 = game._grid_view_center_ratio()
	game._request_grid_zoom(game.grid_zoom + 0.1)
	check(game.camera_zoom_anchor == Vector2.INF, "A slider zoom must drop any wheel anchor")
	await settle_zoom()
	var centre_after: Vector2 = game._grid_view_center_ratio()
	check(centre_before.distance_to(centre_after) < 0.02,
		"A slider zoom must hold the view centre: %.3f,%.3f became %.3f,%.3f" % [
			centre_before.x, centre_before.y, centre_after.x, centre_after.y])

	# 5. Neither limit can be crossed.
	game._set_grid_zoom(furthest * 0.25)
	check(absf(game.grid_zoom - furthest) < 0.0001, "Zoom cannot go past the far limit")
	game._set_grid_zoom(game.MAX_GRID_ZOOM * 4.0)
	check(absf(game.grid_zoom - game.MAX_GRID_ZOOM) < 0.0001, "Zoom cannot go past the near limit")

	print("GRID ZOOM %s: far limit %.1f cells across, pointer held to %.2f cells" % [
		"PASS" if failures == 0 else "FAIL", across, before.distance_to(after)])
	quit(1 if failures else 0)
