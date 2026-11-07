extends SceneTree
const Settings=preload("res://scripts/title_settings.gd")
var game
func _init(): call_deferred("run")
func capture(label: String):
	game.grid_view.surface_key=[]
	game._refresh_all()
	for frame in range(4): await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/riser-light-"+label+".png")
func run():
	Settings.save_path="user://riser_light_fixture.cfg"
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://riser_light_fixture.meta"
	game.run_save_path="user://riser_light_fixture.loop"
	root.add_child(game); current_scene=game
	game.set_process(false); game.tick_timer.stop()
	game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	game.wrecks.clear(); game.drone_fleet.sites.clear(); game.drone_fleet.sites_initialized=true
	game._place_room("life_support",Vector2i(21,20),true)
	game.selected_card_id=""
	game._set_grid_zoom(.55,true,Vector2(21,20.4)/40)
	var room: Dictionary=game.occupied[Vector2i(20,20)]
	Settings.raised_walls=false
	assert(not game.grid_view._riser_fixtures_visible(room),"Cutaway riser hides its fixtures")
	await capture("hidden")
	Settings.raised_walls=true
	assert(game.grid_view._riser_fixtures_visible(room),"Visible exposed riser retains its fixtures")
	await capture("visible")
	game.hardware.walls=false
	assert(not game.grid_view._riser_fixtures_visible(room),"Hardware wall hiding also hides fixtures")
	await capture("walls-off")
	game.hardware.walls=true
	game._place_room("life_support",Vector2i(20,19),true)
	assert(not game.grid_view._riser_fixtures_visible(room),"Neighbor-hidden riser has no floating fixtures")
	await capture("neighbor")
	game.queue_free()
	var music=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	await process_frame
	await create_timer(.15).timeout
	print("RISER LIGHT VISIBILITY PASS")
	quit()
