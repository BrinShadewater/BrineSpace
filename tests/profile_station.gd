extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var game
var samples: Array = []
func _init() -> void: call_deferred("run")
func run() -> void:
	Preferences.save_path = "user://full_profile.cfg"
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://full_profile.meta"
	game.run_save_path = "user://full_profile.loop"
	root.add_child(game)
	current_scene = game
	Preferences.pause_unfocused = false
	root.size = Vector2i(1600,900)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.pending_doctrines.assign(["industry","biosphere"])
	game._confirm_doctrines()
	game.tick_timer.stop()
	game.set_process(false)
	# Dialogue deliberately pauses gameplay; dismiss it for active rendering samples.
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.grid_view.profile_draw = true
	await sample("small-active")
	var ids := ["reactor","life_support","hydroponics_bay","research_lab","storage_bay","crew_hab","corridor","med_bay"]
	for y in range(5):
		for x in range(5):
			var cell := Vector2i(18+x,18+y)
			if game.occupied.has(cell): continue
			game._place_room(ids[(x+y*5)%ids.size()],cell,true)
	game.selected_card_id = ""
	game._refresh_all()
	game._fit_station_view()
	await sample("expanded-active")
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
	game._center_grid_on_station()
	await sample("expanded-close-active")
	game._set_paused(true,false)
	await sample("expanded-paused")
	if DisplayServer.get_name() != "headless":
		game.grid_view.cull_room_drawing = false
		game.grid_view.queue_redraw()
		await RenderingServer.frame_post_draw
		var all_image := root.get_texture().get_image()
		game.grid_view.cull_room_drawing = true
		game.grid_view.queue_redraw()
		await RenderingServer.frame_post_draw
		var culled_image := root.get_texture().get_image()
		print("CULL PIXEL PARITY: ", all_image.get_data() == culled_image.get_data())
	var file := FileAccess.open("res://output/full-profile.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(samples,"\t"))
	file.close()
	for path in [Preferences.save_path,game.meta.save_path,game.run_save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("STATION PROFILE COMPLETE")
	quit()
func sample(label: String) -> void:
	game._set_paused(label == "expanded-paused",false)
	for frame in range(120):
		game._process(1.0/60.0)
		await process_frame
	assert(game.paused == (label == "expanded-paused"), "Profile sample pause state must match its label")
	var begin := Time.get_ticks_usec()
	var cpu := 0.0
	var draw_totals := {}
	for frame in range(120):
		var step_begin := Time.get_ticks_usec()
		game._process(1.0/60.0)
		cpu += (Time.get_ticks_usec() - step_begin) / 1000.0
		await process_frame
		for key in game.grid_view.draw_profile_usec:
			draw_totals[key] = float(draw_totals.get(key,0.0)) + float(game.grid_view.draw_profile_usec[key])/120000.0
		for canvas in game.grid_view.content_canvases.values():
			if not canvas.visible: continue
			var key: String = "props_"+canvas.renderer.get_script().resource_path.get_file().get_basename()
			draw_totals[key] = float(draw_totals.get(key,0.0))+float(canvas.prepare_usec+canvas.draw_usec)/120000.0
	var row := {"scenario":label,"rooms":game.placed_rooms.size(),"mean_frame_ms":(Time.get_ticks_usec()-begin)/120000.0,"mean_main_process_ms":cpu/120.0,"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)}
	samples.append(row)
	row["mean_draw_stage_ms"] = draw_totals if not game.paused else {}
	print(JSON.stringify(row))
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/full-profile-"+label+".png")
