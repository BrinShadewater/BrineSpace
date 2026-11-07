extends SceneTree
const Life = preload("res://scripts/ocean_life.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
var capture_dir := ""
func _initialize() -> void: call_deferred("run")
func capture(game, name: String) -> void:
	game.grid_view.queue_redraw()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var im := root.get_texture().get_image()
	if im.save_png(capture_dir.path_join(name + ".png")) != OK:
		failures += 1
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): capture_dir=arg.trim_prefix("--capture-dir=")
	if capture_dir.is_empty(): quit(2); return
	DirAccess.make_dir_recursive_absolute(capture_dir)
	Preferences.save_path="user://sea-life-review.cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://sea-life-review.meta"
	game.run_save_path="user://sea-life-review.loop"
	root.add_child(game); current_scene=game
	while not game.startup_complete: await process_frame
	root.size=Vector2i(1600,900)
	game.tick_timer.stop(); game._set_paused(true,false)
	game.crew_comms.minimize(); game.set_process(false)
	Preferences.effects_quality=2; Preferences.reduced_motion=false
	game._set_grid_zoom(game.MAX_GRID_ZOOM * 0.75)
	await process_frame
	var size: float=game.get_cell_size()
	var centre: Vector2=Life.station_centre(game)
	for subject in ["lantern","glass","veil","ribbon","tidewalker"]:
		var t:=20.0
		var target:=centre * size
		if subject in ["lantern","glass","veil"]:
			var slot: int=["lantern","glass","veil"].find(subject)
			var e:=Life._epoch(t,slot,Life.DRIFTER_EPOCH)
			var seed: float=e.x*3.1+e.z*17.0
			var base:=centre+Vector2((Life._h(seed,1,0)-0.5)*36,(Life._h(seed,2,0)-0.5)*26)
			var drift:=Vector2((Life._h(seed,3,0)-0.5)*3,-1.4-Life._h(seed,4,0)*2)
			target=(base+drift*(e.y-0.5))*size
		elif subject=="ribbon":
			var e:=Life._epoch(t,20,Life.SHOAL_EPOCH)
			var seed: float=e.x*5.7+e.z*11.0
			var angle:=Life._h(seed,1,0)*TAU
			var dir:=Vector2(cos(angle),sin(angle))
			target=(centre+Vector2(-dir.y,dir.x)*(Life._h(seed,2,0)-0.5)*22+dir*(e.y*60-30))*size
		else:
			t=55.0
			var angle:=Life._h(0,1,0)*TAU
			target=(centre+Vector2(-sin(angle),cos(angle))*(Life._h(0,2,0)-0.5)*16)*size
			game._set_grid_zoom(game.MAX_GRID_ZOOM * 0.25)
			size=game.get_cell_size()
			target=(centre+Vector2(-sin(angle),cos(angle))*(Life._h(0,2,0)-0.5)*16)*size
		game.grid_scroll.scroll_horizontal=int(target.x-game.grid_scroll.size.x*.5)
		game.grid_scroll.scroll_vertical=int(target.y-game.grid_scroll.size.y*.5)
		# Keep the deferred zoom restoration on this same creature, then wait
		# for the actual scroll state rather than an arbitrary startup delay.
		game._set_grid_zoom(game.grid_zoom,true,target/(size*float(game.GRID_SIZE)))
		var wanted:=Vector2(maxf(0,target.x-game.grid_scroll.size.x*.5),maxf(0,target.y-game.grid_scroll.size.y*.5))
		var stable:=0
		for n in range(120):
			await process_frame
			var actual:=Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)
			stable=stable+1 if actual.distance_to(wanted)<2 else 0
			if stable>=2: break
		if stable<2: failures+=1; push_error("Creature camera did not settle: "+subject)
		game.visual_time_seconds=t
		Life.authored_enabled=false
		await capture(game,subject+"-before")
		Life.authored_enabled=true
		await capture(game,subject+"-after")
		if subject in ["lantern","ribbon","tidewalker"]:
			for i in range(8):
				game.visual_time_seconds=t+float(i)/6
				await capture(game,subject+"-motion-%02d"%i)
		var frozen: float=game.get_visual_time_seconds()
		game.set_process(true)
		await process_frame
		if game.get_visual_time_seconds()!=frozen: failures+=1
		game.set_process(false)
		if subject=="tidewalker":
			# Art-only overview below the normal player's zoom stop, to inspect
			# all attachments. Keep the normal gameplay close-up above as well.
			var cells:=target/size
			game.camera_view_revision+=1
			game.grid_zoom=0.045
			game._apply_grid_zoom()
			size=game.get_cell_size()
			game.grid_scroll.scroll_horizontal=int(cells.x*size-game.grid_scroll.size.x*.5)
			game.grid_scroll.scroll_vertical=int(cells.y*size-game.grid_scroll.size.y*.5)
			await capture(game,"tidewalker-art-overview")
	print("SEA LIFE REVIEW: failures=",failures)
	quit(1 if failures else 0)
