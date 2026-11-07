extends SceneTree
const OUT := "res://output/playtest-visual-v1/"
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
	var ids=["brine_core","life_support","quarantine_cell","tidal_condenser","pressure_control","mining_drone_bay"]
	var cells=[Vector2i(20,20),Vector2i(19,20),Vector2i(21,20),Vector2i(19,21),Vector2i(20,21),Vector2i(21,21)]
	for i in range(ids.size()): game._place_room(ids[i],cells[i],true)
	game.running=true
	game.resources.power=100
	game.selected_card_id=""
	game.selected_room_cell=cells[1]
	game._refresh_all()
	await process_frame
	game._fit_station_view()
	await capture("station-on")
	game.room_operation_button.set_process(false)
	game.room_operation_button.amount=1
	game._toggle_inspected_room()
	assert(game.occupied[cells[1]].suspended)
	for step in range(4):
		game.room_operation_button._process(0.06)
		await capture("switch-off-%d"%step)
	game._toggle_inspected_room()
	assert(not game.occupied[cells[1]].suspended)
	game.room_operation_button._process(0.18)
	await capture("station-resumed")
	game.drone_fleet.synchronize(game.placed_rooms)
	var drone=game.drone_fleet.drones.values()[0]
	drone.phase="outbound"
	drone.position=Vector2(20,20)
	await capture("drone-under-hull")
	var under_image=root.get_texture().get_image()
	drone.phase="docked"
	await capture("no-drone-baseline")
	assert(under_image.get_data()==root.get_texture().get_image().get_data(),"Hull completely occludes the ROV")
	drone.phase="outbound"
	drone.position=Vector2(20,19)
	await capture("drone-exterior")
	assert(under_image.get_data()!=root.get_texture().get_image().get_data(),"Exterior ROV remains visible")
	for width in [1280,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16.0))
		await process_frame
		game._fit_station_view()
		await capture("station-%d"%width)
	print("VISUAL REFINEMENT PASS: operation toggle, animation frames, exterior/under-hull captures")
	quit()
