extends SceneTree
const Save = preload("res://scripts/run_save.gd")
const Loading = preload("res://scripts/loading_transition.gd")
var failures := 0
var capture_dir := ""

func _init() -> void:
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture-dir="):
			capture_dir = argument.trim_prefix("--capture-dir=")
	call_deferred("run")

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func run() -> void:
	root.gui_disable_input = true
	# Set isolated write targets before gameplay's _ready. The overlay itself
	# must prevent simulation while the player reads.
	root.child_entered_tree.connect(func(node: Node):
		if node.get_script() != null and node.get_script().resource_path == "res://scripts/main.gd":
			node.meta.save_path = "user://loading-test.meta"
			node.run_save_path = "user://loading-test.loop"
	)
	var checkpoint := {}
	for continuing in [false,true]:
		var title = load("res://scenes/title_screen.tscn").instantiate()
		title.run_save_path = "user://loading-test.loop"
		root.add_child(title)
		current_scene = title
		Save.pending = checkpoint.duplicate(true)
		title._start_game(continuing)
		var loading: CanvasLayer
		for child in root.get_children():
			if child is Loading: loading = child
		check(loading != null,"Loading screen exists before scene replacement")
		if continuing:
			var skip := InputEventKey.new()
			skip.keycode = KEY_ENTER
			skip.pressed = true
			loading._input(skip)
			check(not loading.finished_reading,"Early Enter cannot acknowledge an unread loading screen")
		await process_frame
		if DisplayServer.get_name() != "headless":
			await RenderingServer.frame_post_draw
			if not capture_dir.is_empty():
				root.get_texture().get_image().save_png(capture_dir.path_join("loading-continue.png" if continuing else "loading-new-loop.png"))
		while is_instance_valid(title): await process_frame
		var game = current_scene
		while not game.startup_complete:
			check(is_instance_valid(loading),"Loading survives asynchronous checkpoint restoration")
			await process_frame
		while loading.continue_button.disabled: await process_frame
		check(loading.transcript.text == Loading.TRANSMISSION,"Complete intro remains available")
		var reserves: Dictionary = game.resources.duplicate(true)
		await create_timer(3.0).timeout
		check(game.resources == reserves,"Reading does not consume station reserves")
		check(is_instance_valid(loading) and not loading.finished_reading,"Ready station waits for explicit Continue")
		check(game.process_mode == Node.PROCESS_MODE_DISABLED,"Gameplay remains frozen during transmission")
		if DisplayServer.get_name() != "headless" and not capture_dir.is_empty():
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(capture_dir.path_join("loading-transmission.png"))
		if continuing:
			var accept := InputEventKey.new()
			accept.keycode = KEY_ENTER
			accept.pressed = true
			loading._input(accept)
		else:
			root.gui_disable_input = false
			var click := InputEventMouseButton.new()
			click.button_index = MOUSE_BUTTON_LEFT
			click.position = loading.continue_button.get_global_rect().get_center()
			click.pressed = true
			root.push_input(click, true)
			click = click.duplicate()
			click.pressed = false
			root.push_input(click, true)
		for frame in range(120):
			if not is_instance_valid(loading): break
			await process_frame
		check(not is_instance_valid(loading),"Explicit Continue closes the loading screen")
		if is_instance_valid(loading): loading.queue_free()
		root.gui_disable_input = true
		check(game.process_mode == Node.PROCESS_MODE_INHERIT,"Continue resumes gameplay processing")
		game.process_mode = Node.PROCESS_MODE_DISABLED
		check(game.visible and game.startup_complete,"Station is ready when loading screen closes")
		if continuing:
			check(game.resources.metal == 41,"Continue restores exact reserves without starter duplication")
		else:
			game.resources.metal = 41
			checkpoint = Save.capture(game)
		game.queue_free()
		await process_frame
	# Reduced motion keeps the same opaque screen without an animated bar.
	preload("res://scripts/title_settings.gd").reduced_motion = true
	var overlay := Loading.new()
	root.add_child(overlay)
	check(overlay.find_children("*","ProgressBar",true,false).is_empty(),"Reduced motion omits the animated indicator")
	check(not overlay.finished_reading and overlay.transcript.text == Loading.TRANSMISSION,"Reduced motion displays the complete transmission immediately")
	overlay.queue_free()
	await process_frame
	var replay := Loading.new()
	replay.replay_mode = true
	root.add_child(replay)
	check(not replay.continue_button.disabled and not replay.finished_reading,"Archive replay waits for Return to Archive")
	replay.continue_button.pressed.emit()
	await process_frame
	check(not is_instance_valid(replay),"Return to Archive closes the recording")
	print("LOADING TRANSITION PASS" if failures == 0 else "LOADING TRANSITION FAIL")
	quit(failures)
