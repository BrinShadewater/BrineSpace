extends SceneTree
const OUT := "res://output/floor-station-v3/"
var game
func _init() -> void: call_deferred("run")
func capture(label: String) -> void:
	game.grid_view.queue_redraw()
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	assert(root.get_texture().get_image().save_png(OUT+label+".png")==OK)
func run() -> void:
	DirAccess.make_dir_recursive_absolute(OUT)
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate()
	game.run_save_path="user://visual_refinement_test.loop"
	game.meta.save_path="user://visual_refinement_test.meta"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.occupied.clear()
	game.placed_rooms.clear()
	game.wrecks.clear()
	game.drone_fleet.restore(null)
	var ids=preload("res://scripts/room_database.gd").all_rooms().keys()
	var cells: Array=[]
	for i in range(ids.size()):
		var cell:=Vector2i(20+i%7,20+i/7)
		cells.append(cell)
		game._place_room(ids[i],cell,true)
	assert(game.placed_rooms.size()==ids.size(),"Every current room must appear in the fixture")
	game.running=true
	game.resources.power=100
	game.selected_card_id=""
	game.selected_room_cell=cells[1]
	game._refresh_all()
	await process_frame
	game._fit_station_view()
	await capture("station-on")
	for width in [1280,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		await process_frame
		game._fit_station_view()
		await capture("station-%d"%width)
	print("FLOOR STATION PASS: ",ids.size()," live room identities at 1280, 1600 and 2560 widths")
	quit()
