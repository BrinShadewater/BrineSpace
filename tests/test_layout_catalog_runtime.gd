extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="res://output/layout-editor/catalog-runtime.json"
	Store.defaults_path="res://output/layout-editor/no-defaults.json"
	Store.loaded=true
	Store.data={"room-corridor/0":{"library/common-analog_clock":[-10,0]},"room-current_turbine/0":{"library/common-analog_clock":[90,110]}}
	root.size=Vector2i(1600,900)
	var game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://catalog_runtime_test.loop"; game.meta.save_path="user://catalog_runtime_test.meta"
	root.add_child(game); current_scene=game
	game.set_process(false); game.tick_timer.stop(); game._set_paused(true,false)
	game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
	game._place_room("current_turbine",Vector2i(20,20),true)
	game._place_room("corridor",Vector2i(20,21),true)
	game.selected_card_id=""; game._refresh_all()
	await process_frame
	game._fit_station_view()
	await process_frame
	await RenderingServer.frame_post_draw
	assert(game.grid_view.corridor_layout_views.has("corridor"))
	# September 9 decision: common decorations are Studio dressing only, so a saved
	# clock reaches the live room's layout and is then filtered out of the render.
	var corridor=game.grid_view.corridor_layout_views.corridor
	for prop in corridor.props:
		assert(not str(prop.id).begins_with("library/common-"),"Corridor drops common decorations")
	var power=game.grid_view._bill_room_view({"id":"current_turbine"})
	for prop in power.props:
		assert(not str(prop.id).begins_with("library/common-"),"Power room drops common decorations")
	assert(Store.positions("room-corridor",0).has("library/common-analog_clock"),"The saved addition still loads")
	assert(Store.is_common_decoration({"id":"library/common-analog_clock"}),"The filter is what removes it")
	root.get_texture().get_image().save_png("res://output/layout-editor/catalog-runtime.png")
	print("CATALOG RUNTIME PASS: saved additions load, common decorations stay out of live corridor and power room")
	quit()
