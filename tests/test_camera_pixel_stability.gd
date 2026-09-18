extends SceneTree
var failures := 0
var game
var results := []
func _init() -> void: call_deferred("run")
func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)
func settle() -> void:
	for i in range(3): await process_frame
	await RenderingServer.frame_post_draw
func run() -> void:
	if DisplayServer.get_name() == "headless":
		push_error("Camera sampling regression requires native rendering")
		quit(2)
		return
	root.gui_disable_input = true
	# The window this test measures must be its own doing. It used to inherit whatever display
	# settings the machine had saved - on the owner's PC a borderless 2560x1440 - and the fractional
	# scales below only line up on a window that fills the screen. Test runs read an isolated
	# settings file now, so the test states the window it needs (owner polish pass, Sept 18).
	var screen := DisplayServer.screen_get_size(DisplayServer.window_get_current_screen())
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
	DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_BORDERLESS, true)
	DisplayServer.window_set_position(DisplayServer.screen_get_position(DisplayServer.window_get_current_screen()))
	DisplayServer.window_set_size(screen)
	for i in range(4): await process_frame
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://camera_pixel_test.meta"
	game.run_save_path = "user://camera_pixel_test.loop"
	root.add_child(game)
	current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game._set_paused(true,false)
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	# Setting root.size does not resize a maximized or DPI-scaled window, so the window
	# scale is chosen through the design size: fractional up- and downscales like 1440p,
	# 1600x900-on-2560, 1280x720 and 1600x900 windows showing the 1920x1080 design.
	var window: Vector2i = DisplayServer.window_get_size()
	for window_scale in [4.0/3.0,8.0/5.0,2.0/3.0,5.0/6.0]:
		root.content_scale_size = Vector2i(roundi(window.x/window_scale),roundi(window.y/window_scale))
		await settle()
		var extent: Vector2i = root.get_texture().get_size()
		for zoom in [0.6,1.0]:
			game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * zoom,true,Vector2(20.5,20.5)/40.0)
			await settle()
			var start := Vector2i(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)
			var transform: Transform2D = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()
			var center: Vector2 = transform*(Vector2(20.5,20.5)*game.get_cell_size())
			var crop := Rect2i(Vector2i(center)-Vector2i(48,48),Vector2i(96,96))
			var reference := root.get_texture().get_image()
			var pixels := reference.get_region(crop).get_data()
			var header := reference.get_region(Rect2i(0,0,extent.x,45)).get_data()
			for offset in [Vector2i(1,0),Vector2i(2,0),Vector2i(3,0),Vector2i(0,1),Vector2i(0,3),Vector2i(3,3),Vector2i(-2,-2),Vector2i.ZERO]:
				game.grid_scroll.scroll_horizontal = start.x+offset.x
				game.grid_scroll.scroll_vertical = start.y+offset.y
				await settle()
				var next: Transform2D = root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()
				var shift := Vector2i(next.origin.round()-transform.origin.round())
				var frame := root.get_texture().get_image()
				var moved := frame.get_region(Rect2i(crop.position+shift,crop.size)).get_data()
				var different := 0
				for i in range(0,pixels.size(),4):
					if pixels[i]!=moved[i] or pixels[i+1]!=moved[i+1] or pixels[i+2]!=moved[i+2]: different += 1
				var fraction := float(different)/float(crop.size.x*crop.size.y)
				results.append({"window_scale":snappedf(root.get_stretch_transform().get_scale().x,0.0001),"width":extent.x,"zoom":zoom,"offset":str(offset),"changed_fraction":fraction})
				check(fraction<0.005,"Room art must translate without resampling: "+str(results.back()))
				check(header==frame.get_region(Rect2i(0,0,extent.x,45)).get_data(),"Camera alignment must not move the HUD")
				check(game.grid_view.position==Vector2(-game.grid_scroll.scroll_horizontal,-game.grid_scroll.scroll_vertical),"Logical input coordinates remain owned by ScrollContainer")
	DirAccess.make_dir_recursive_absolute("res://output/camera-shimmer")
	var file := FileAccess.open("res://output/camera-shimmer/regression.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(results,"  "))
	file.close()
	print("CAMERA PIXEL STABILITY %s: %d comparisons / %d failures" % ["PASS" if failures==0 else "FAIL",results.size(),failures])
	quit(1 if failures else 0)
