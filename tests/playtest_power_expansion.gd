extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
const Save = preload("res://scripts/run_save.gd")
var game
var elapsed := 0.0
var cycle_elapsed := 0.0
func _init() -> void: call_deferred("run")
func settle() -> void:
	for i in range(5): await process_frame
	await RenderingServer.frame_post_draw
func step() -> void:
	game.paused=false
	game._process(0.5)
	elapsed+=0.5
	cycle_elapsed+=0.5
	if cycle_elapsed>=20:
		cycle_elapsed=0
		game._advance_cycle()
	assert(game.running and game.resources.integrity>0,"Paid opening failed")
func build(id: String, cell: Vector2i, q: int) -> void:
	while not game._can_afford(game.RoomDatabaseScript.get_room(id).cost) and elapsed<300: step()
	assert(game._can_afford(game.RoomDatabaseScript.get_room(id).cost),"Could not afford "+id)
	assert(game.hand.has(id),"Missing offered or earned blueprint "+id)
	game.selected_card_id=id
	game.selected_rotation=q
	assert(game.get_placement_problem(id,cell).is_empty(),game.get_placement_problem(id,cell))
	var before: int=game.resources.metal
	game._on_grid_clicked(cell)
	assert(game.drone_fleet.reserved(cell),"Paid build did not enter construction queue")
	assert(game.resources.metal==before-int(game.RoomDatabaseScript.get_room(id).cost.metal),"Construction cost not paid")
	while not game.occupied.has(cell) and elapsed<300: step()
	assert(game.occupied.has(cell),"Construction never completed")
func await_blueprint(id: String) -> void:
	while not game.meta.unlocked_room_ids.has(id) and elapsed<300: step()
	assert(game.meta.unlocked_room_ids.has(id),"Functioning discovery did not unlock "+id)
	# The earned prototype goes to the top of the pile. Drawing it here isolates
	# advanced-room acceptance from an unrelated full-hand discard decision.
	game.hand.clear()
	game._refill_hand()
	assert(game.hand.has(id),"Earned prototype not drawn")
func run() -> void:
	Preferences.initialized=true
	Preferences.save_path="user://power_native_test.cfg"
	root.size=Vector2i(1600,900)
	root.content_scale_size=Vector2i(1920,1080)
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://power_native_test.meta"
	game.run_save_path="user://power_native_test.loop"
	game.meta.unlocked_room_ids.clear()
	for id in game.RoomDatabaseScript.STARTING_UNLOCKS: game.meta.unlocked_room_ids[id]=true
	game.meta.discovered_synergy_ids.clear()
	game.meta.stabilized_synergy_ids.clear()
	game.meta.selected_architect="bill"
	root.add_child(game)
	current_scene=game
	game._confirm_doctrines()
	game.tick_timer.stop()
	game.set_process(false)
	game.time_speed_index=0
	assert(not game.testing_free_build and not game.testing_disable_failures)
	build("solar_array",Vector2i(20,19),0)
	build("current_turbine",Vector2i(19,20),0)
	build("mining_drone_bay",Vector2i(20,21),0)
	build("hydroponics_bay",Vector2i(18,20),0)
	await_blueprint("biomass_digester")
	build("biomass_digester",Vector2i(18,19),0)
	# A controlled advanced draft; the reactor remains paid and consumes its
	# starting Rare Mineral. No unlocks or resource grants are injected.
	if not game.hand.has("reactor"):
		assert(game.draw_pile.has("reactor") or game.discard_pile.has("reactor"))
		game.draw_pile.erase("reactor")
		game.discard_pile.erase("reactor")
		game.hand.append("reactor")
	build("reactor",Vector2i(20,22),0)
	await_blueprint("heat_recovery")
	build("heat_recovery",Vector2i(21,22),0)
	game._apply_room_economy()
	assert(game.crew_count==1 and game.bill_npc.active,"Starter did not wake and survive the paid opening")
	assert(game.powered_room_cells.has(Vector2i(18,19)) and game.powered_room_cells.has(Vector2i(21,22)),"Advanced generators not functioning")
	var before: Dictionary=game._simulate_room_economy()
	assert(Save.write(game,game.run_save_path)==OK,Save.last_error)
	game.occupied[Vector2i(19,20)].rotation=1
	assert(Save.restore(game,Save.read(game.run_save_path)),Save.last_error)
	assert(game.occupied[Vector2i(19,20)].rotation==0,"Saved intake rotation lost")
	assert(game._simulate_room_economy().generation==before.generation,"Save/Continue changed generation")
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.toast_messages.clear()
	if game.cascade_toast_tween!=null and game.cascade_toast_tween.is_valid(): game.cascade_toast_tween.kill()
	game.cascade_toast.hide()
	game.discovery_bursts.clear()
	Preferences.placement_guides=false
	game.selected_card_id=""
	game.hovered_card_id=""
	game.hover_cell=Vector2i(-1,-1)
	game.selected_room_cell=Vector2i(19,20)
	DirAccess.make_dir_recursive_absolute("res://output/power-rooms")
	for width in [1280,1600,2560]:
		root.size=Vector2i(width,roundi(width*9.0/16))
		game._refresh_all()
		await settle()
		game._fit_station_view()
		game.grid_view.queue_redraw()
		await settle()
		assert(root.get_texture().get_image().save_png("res://output/power-rooms/station-%d.png" % width)==OK)
	var frozen: float=game.get_visual_time_seconds()
	await settle()
	assert(game.get_visual_time_seconds()==frozen,"Paused machinery clock advanced")
	print("POWER PAID PLAYTEST: PASS at %.1f simulated seconds, cycle %d; both discoveries earned, three new rooms paid, disk Save/Continue, three native sizes, pause." % [elapsed,game.cycle])
	for path in [game.meta.save_path,game.run_save_path,Preferences.save_path]:
		for suffix in ["",".bak",".tmp"]:
			if FileAccess.file_exists(path+suffix): DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	game.queue_free()
	await process_frame
	quit()
