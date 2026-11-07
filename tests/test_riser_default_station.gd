extends SceneTree
const Pref=preload("res://scripts/title_settings.gd")
const OUT="res://output/riser-departments-v1/"
func _init() -> void: call_deferred("run")
func run() -> void:
	var path="res://tests/test_riser_default_station.gd.uid"
	if not FileAccess.file_exists(path):
		var file=FileAccess.open(path,FileAccess.WRITE)
		file.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	Pref.save_path=OUT+"isolated-settings.cfg";Pref.initialized=false
	if FileAccess.file_exists(Pref.save_path): DirAccess.remove_absolute(Pref.save_path)
	var store=preload("res://scripts/room_layout_store.gd")
	store.path=OUT+"isolated-layout.json";store.loaded=true;store.data={}
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path=OUT+"station.loop";game.meta.save_path=OUT+"station.meta"
	root.add_child(game);current_scene=game
	assert(Pref.raised_walls,"Fresh station uses raised walls without a fixture override")
	game.set_process(false);game.tick_timer.stop();game._set_paused(true,false)
	game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear()
	for x in range(4):game._place_room(["crew_lounge","listening_post","quarantine_cell","mining_drone_bay"][x],Vector2i(19+x,20),true)
	game._place_room("med_bay",Vector2i(20,19),true)
	assert(not game.grid_view._has_raised_wall_at(Vector2i(20,20)))
	assert(game.grid_view._has_raised_wall_at(Vector2i(20,19)))
	game.selected_card_id="";game._refresh_all()
	await process_frame;game._fit_station_view()
	await process_frame;await RenderingServer.frame_post_draw
	var raised=root.get_texture().get_image()
	assert(raised.save_png(OUT+"station-default.png")==OK)
	var before=game.grid_view._surface_state()
	Pref.raised_walls=false
	assert(before!=game.grid_view._surface_state(),"Preference changes invalidate cached room art")
	game.grid_view.queue_redraw()
	await process_frame;await RenderingServer.frame_post_draw
	var low=root.get_texture().get_image()
	assert(low.get_data()!=raised.get_data(),"Display toggle changes the native station")
	assert(low.save_png(OUT+"station-low.png")==OK)
	print("RISER DEFAULT STATION PASS: fresh default, stepped adjacency, cache invalidation and native display toggle")
	quit()
