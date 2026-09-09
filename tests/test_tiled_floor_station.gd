extends SceneTree
const Store=preload("res://scripts/room_layout_store.gd")
const Floor=preload("res://rooms/whole-room/modular_floor.gd")
func _init() -> void: call_deferred("run")
func run() -> void:
	Store.path="user://floor-station.json"; Store.defaults_path="user://no-floor-defaults.json"; Store.loaded=true; Store.data={}
	Store.save_layout("research-analysis-wall",0,{"floor/material/3/6":3,"floor/material/4/6":3})
	Store.save_layout("room-corridor",0,{"floor/material/3/0":3,"floor/material/4/0":3,"floor/variation":true,"floor/seed":42})
	var game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://floor-station.meta"; game.run_save_path="user://floor-station.loop"
	root.add_child(game); current_scene=game; game._set_paused(true,false); game.tick_timer.stop()
	game.testing_free_build=true; game.testing_disable_failures=true
	game.occupied.clear(); game.placed_rooms.clear(); game.wrecks.clear()
	game._place_room("research_lab",Vector2i(20,19),true)
	game._place_room("corridor",Vector2i(20,20),true)
	game.selected_card_id=""; game._refresh_all(); game.set_process(false)
	assert(game._connected_neighbor_cells(Vector2i(20,19)).has(Vector2i(20,20)))
	var before: Dictionary=game.grid_view.bill_room_geometry(game.occupied[Vector2i(20,19)],[2])
	for material in range(4):
		Store.save_layout("research-analysis-wall",0,{"floor/material/3/6":material})
		var after: Dictionary=game.grid_view.bill_room_geometry(game.occupied[Vector2i(20,19)],[2])
		assert(before.props==after.props,"Floor materials never change furniture collision")
	Store.save_layout("research-analysis-wall",0,{"floor/material/3/6":3,"floor/material/4/6":3})
	for size in [Vector2i(1280,720),Vector2i(1600,900)]:
		root.size=size; await process_frame; await process_frame
		game._fit_station_view(); await process_frame; await process_frame; RenderingServer.force_draw()
		root.get_texture().get_image().save_png("res://output/tiled-floor-pilot/station-%d.png"%size.x)
	game.queue_free(); await process_frame
	var music:=root.get_node_or_null("StationMusic")
	if music!=null: music.queue_free()
	await create_timer(0.15).timeout
	print("TILED STATION PASS: connected pair, saved floor rendering, collision unchanged, two viewport sizes")
	quit()
