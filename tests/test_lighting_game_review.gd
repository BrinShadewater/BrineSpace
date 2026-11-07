extends SceneTree
const Art = preload("res://scripts/lighting_art.gd")
const Lighting = preload("res://rooms/whole-room/room_lighting.gd")
const Preferences = preload("res://scripts/title_settings.gd")
var directory := ""
var failures := 0
func _initialize() -> void: call_deferred("run")
func capture(game, name: String) -> void:
	Lighting.update_light_map(game)
	game.grid_view.queue_redraw()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(directory.path_join(name+".png")) != OK: failures+=1
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): directory=arg.trim_prefix("--capture-dir=")
	if directory.is_empty(): quit(2); return
	DirAccess.make_dir_recursive_absolute(directory)
	Preferences.save_path="user://lighting-game-review.cfg"
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://lighting-game-review.meta"
	game.run_save_path="user://lighting-game-review.loop"
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	root.size=Vector2i(1600,900)
	game.tick_timer.stop();game._set_paused(true,false)
	game.crew_comms.minimize();game.set_process(false)
	game.testing_free_build=true
	game._place_room("hydroponics_bay",Vector2i(21,19),true)
	game._refresh_all()
	game._set_grid_zoom(game.MAX_GRID_ZOOM*.65)
	await process_frame
	var size: float=game.get_cell_size()
	var target:=Vector2(20,20)*size
	game._set_grid_zoom(game.grid_zoom,true,target/(size*float(game.GRID_SIZE)))
	await process_frame
	var saved:=Art.textures.duplicate()
	for quality in [0,1,2]:
		Preferences.effects_quality=quality;Preferences.reduced_motion=false
		game.visual_time_seconds=12.0
		for reference in [true,false]:
			Art.textures=saved.duplicate()
			if reference:
				for key in Art.PATHS: Art.textures[key]=null
			game.grid_view.underwater_visibility.material.set_shader_parameter("use_caustics_tex",not reference)
			await capture(game,"game-%s-quality-%d"%["procedural" if reference else "authored",quality])
	Art.textures=saved
	Preferences.effects_quality=2;game.power_blackout=true
	for i in range(4):
		game.visual_time_seconds=12.0+float(i)
		await capture(game,"game-blackout-%d"%i)
	Preferences.reduced_motion=true
	await capture(game,"game-reduced-motion")
	print("LIGHTING GAME REVIEW: failures=",failures)
	game.queue_free();await process_frame
	quit(1 if failures else 0)
