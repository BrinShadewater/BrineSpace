extends SceneTree
## Mac trackpad pinch (magnify gesture) zooms the station like Shift+wheel, in both directions, and
## respects the zoom limits and the invert setting.
const Preferences = preload("res://scripts/title_settings.gd")
var game
var failures := 0

func check(ok: bool, message: String) -> void:
	if ok: return
	failures += 1
	push_error(message)

func pinch(factor: float) -> void:
	var event := InputEventMagnifyGesture.new()
	event.factor = factor
	event.position = game.grid_view.get_local_mouse_position()
	game.grid_view._gui_input(event)

func settle() -> void:
	for i in range(60):
		game._update_camera_zoom(1.0 / 60.0)
		await process_frame

func _init() -> void: call_deferred("run")

func run() -> void:
	Preferences.save_path = "user://trackpad_pinch_%d.cfg" % OS.get_process_id()
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://trackpad_pinch_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://trackpad_pinch_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1600, 900)
	while not game.startup_complete: await process_frame
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.set_process(false)
	game.tick_timer.stop()
	Preferences.invert_zoom = false
	game._set_grid_zoom(game.MAX_GRID_ZOOM * 0.5)
	await settle()
	var start: float = game.grid_zoom
	for i in range(6): pinch(1.06)
	await settle()
	check(game.grid_zoom > start + 0.05, "Pinching out zooms in: %.3f -> %.3f" % [start, game.grid_zoom])
	var closer: float = game.grid_zoom
	for i in range(12): pinch(0.94)
	await settle()
	check(game.grid_zoom < closer - 0.05, "Pinching in zooms out: %.3f -> %.3f" % [closer, game.grid_zoom])
	for i in range(200): pinch(1.2)
	await settle()
	check(game.grid_zoom <= game.MAX_GRID_ZOOM + 0.0001, "Pinch stops at the closest zoom")
	Preferences.invert_zoom = true
	var before: float = game.grid_zoom
	for i in range(6): pinch(1.06)
	await settle()
	check(game.grid_zoom < before - 0.05, "Invert zoom also inverts the pinch")
	Preferences.invert_zoom = false
	for path in [Preferences.save_path, game.meta.save_path, game.run_save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("TRACKPAD PINCH: %s failures=%d" % ["PASS" if failures == 0 else "FAIL", failures])
	quit(1 if failures > 0 else 0)
