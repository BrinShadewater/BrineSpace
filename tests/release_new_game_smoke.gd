extends Node
var failures := 0
func check(ok: bool, message: String):
	if not ok:
		failures += 1
		push_error(message)
func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	call_deferred("run")
func run():
	check(not OS.is_debug_build(), "Must execute in the actual release template")
	for i in range(10): await get_tree().process_frame
	var title = get_tree().current_scene
	check(title != null and title.has_method("_start_game"), "Configured title scene loaded")
	if title == null or not title.has_method("_start_game"):
		get_tree().quit(1); return
	title._start_game()
	var game
	for i in range(1800):
		await get_tree().process_frame
		game = get_tree().current_scene
		if game != null and game != title and game.get("startup_complete") == true: break
	check(game != null and game != title and game.get("startup_complete") == true, "New Game completes in release")
	if game == null or game == title:
		get_tree().quit(1); return
	for child in get_tree().root.get_children():
		if child.has_method("finish_after_scene_change"):
			child._continue()
	for i in range(5): await get_tree().process_frame
	game.crew_comms.minimize()
	if game.paused: game._toggle_pause()
	var before: float = game.visual_time_seconds
	for i in range(240): await get_tree().process_frame
	check(game.visual_time_seconds > before, "Station simulation advances")
	check(not get_tree().paused and game.process_mode != Node.PROCESS_MODE_DISABLED, "Station process restored after Continue")
	check(game.grid_view.visible_draw_rooms.size() > 0, "Station renders after New Game")
	var report = get_tree().root.get_node("BugReport")
	var key := InputEventKey.new(); key.keycode=KEY_F8; key.pressed=true
	report._input(key)
	check(get_tree().paused and report.overlay.visible, "Release F8 opens and pauses")
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("user://release-report.png")
	var path: String = report.save_report("Release New Game smoke")
	check(not path.is_empty(), "Release report is written")
	report._hide_overlay()
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("user://release-game.png")
	print("ACTUAL RELEASE NEW GAME + F8: %d failures; debug=%s" % [failures, OS.is_debug_build()])
	get_tree().quit(1 if failures else 0)
