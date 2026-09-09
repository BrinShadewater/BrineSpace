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
	var corridor=game.grid_view.corridor_layout_views.corridor
	assert(corridor.props.size()==1 and corridor.props[0].id=="library/common-analog_clock")
	var power=game.grid_view._bill_room_view({"id":"current_turbine"})
	var found:=false
	for prop in power.props:
		if prop.id=="library/common-analog_clock": found=true
	assert(found,"New catalog room consumes saved asset additions")
	root.get_texture().get_image().save_png("res://output/layout-editor/catalog-runtime.png")
	print("CATALOG RUNTIME PASS: saved additions visible in corridor and power room")
	quit()
