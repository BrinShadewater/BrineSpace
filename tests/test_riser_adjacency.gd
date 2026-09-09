extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://riser_test.loop"
	game.meta.save_path="user://riser_test.meta"
	root.add_child(game)
	current_scene=game
	preload("res://scripts/title_settings.gd").raised_walls=true
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	var geometry=preload("res://rooms/whole-room/riser_geometry.gd")
	assert(geometry.HEIGHT==48.0*1.25 and geometry.TOP+geometry.HEIGHT==-192.0,"25% projection increase keeps deck base")
	assert(geometry.CAP_TOP==geometry.TOP-6.0,"Cap follows wall face")
	game.occupied.clear()
	game.placed_rooms.clear()
	game.wrecks.clear()
	for x in range(3): game._place_room(["galley","listening_post","airlock"][x],Vector2i(19+x,20),true)
	assert(game.grid_view._has_raised_wall_at(Vector2i(20,20)))
	assert(not game.grid_view._has_raised_wall_at(Vector2i(18,20)))
	game._place_room("listening_post",Vector2i(20,19),true)
	assert(not game.grid_view._has_raised_wall_at(Vector2i(20,20)),"A room above removes the rear riser")
	assert(game.grid_view._has_raised_wall_at(Vector2i(20,19)))
	game.selected_card_id=""
	game._refresh_all()
	await process_frame
	game._fit_station_view()
	await process_frame
	await RenderingServer.frame_post_draw
	DirAccess.make_dir_recursive_absolute("res://output/room-architecture-v2")
	root.get_texture().get_image().save_png("res://output/room-architecture-v2/adjacency.png")
	game.hardware.power=false
	for room in game.placed_rooms: game.grid_view.room_light_levels[room.pos]=0.0
	game.grid_view.surface_key=[]; game.grid_view.light_surface_key=[]; game.grid_view.queue_redraw()
	await process_frame; await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/room-architecture-v2/adjacency-power-off.png")
	print("RISER ADJACENCY PASS: exposed, adjoining and stepped rear boundaries")
	quit()
