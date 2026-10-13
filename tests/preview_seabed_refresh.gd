extends SceneTree
## Native review through the production station lighting and fog.
class Samples extends Node2D:
	var size_value := 200.0
	var view = preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
	func _draw():
		for i in range(3):
			var identity: String = ["basalt-outcrop", "wreck-timbers", "ribbon-kelp"][i]
			var at := Vector2(19.5+i, 19.62)*size_value
			view.draw_asset(self, identity, at, size_value*.38, Color(.65,.76,.75,.9))
func _init(): call_deferred("run")
func run():
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://seabed_refresh_review.json"
	game.run_save_path="user://seabed_refresh_review.loop"
	game.set_meta("site_seed",32)
	root.add_child(game);current_scene=game
	while not game.startup_complete: await process_frame
	game._set_paused(true,false)
	# Dedicated art fixture; not expedition acceptance evidence.
	game.site_layout.scenery.clear()
	for cell in [Vector2i(19,20),Vector2i(21,20),Vector2i(22,20)]: game._place_room("solar_array",cell,true)
	game.paused=false
	game.Architects.advance_core(game,10.0)
	game._advance_cycle()
	game.crew_comms.minimize()
	game._set_paused(true,false)
	while game.grid_scroll.size.x<600 or game.grid_scroll.size.y<300: await process_frame
	game._set_grid_zoom(.35,true,Vector2(21.0,20.0)/40.0)
	var deadline:=Time.get_ticks_msec()+5000
	while game._grid_view_center_ratio().distance_to(Vector2(21.0,20.0)/40.0)>.002 and Time.get_ticks_msec()<deadline:
		await process_frame
	var samples:=Samples.new()
	samples.size_value=game.get_cell_size()
	game.grid_view.env_passes[0].add_child(samples)
	game.grid_view.env_below_key.clear();game.grid_view.queue_redraw()
	await process_frame
	RenderingServer.force_draw(false)
	root.get_texture().get_image().save_png("res://assets/environment/seabed-refresh-v1/review/native-station-v1.png")
	var view=preload("res://assets/environment/seabed-refresh-v1/seabed_refresh_view.gd").new()
	view.prepare()
	for id in view.SOURCES:
		assert(view.textures[id] != null and view.textures[id].get_width()==512)
	assert(preload("res://scripts/safe_image.gd").failures.is_empty())
	print("SEABED REFRESH: 3 textures loaded; native station captured; 0 failures")
	quit()
